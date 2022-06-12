"""Parse transaction data downloaded from covalent"""

from typing import Dict, List, Set
import pandas as pd


def parse_covalent_txs(
    raw_data: Dict, tx_metadata: List, tx_params: List
) -> pd.DataFrame:
    """Parses a json formatted nft_transactions response from covalent. Expects
    all tokens for multiple nft collections.

    Format should look like:
    {
        "nft_collection_1: {
            "token_id_1": {
                "updated_at": "2022-06-12T08:37:19.634079643Z",
                "txs": [
                    {
                        "block_signed_at": "2022-01-12T04:17:28Z",
                        "block_height": 123456,
                        "raw_log_topics": ["some_hash", ... ]
                        ...
                        "decoded": {
                            "name": "Transfer",
                            "signature": "some_string",
                            "params": [
                                {
                                    "name": "from",
                                    "type": "address",
                                    "indexed": true,
                                    "value": "hash_or_number_or_null"
                                },
                                ...
                            ]
                        }
                    },
                    ...
                ]
            },
            "token_id_2": ...
        },
        "nft_collection_2": ...
    }

    Args:
        txs: json response from covalent api as saved by covalent io
        tx_metadata: list of keys to extract from each txs dictionary
        tx_params: list of parameters to to extract from each transaction param dictionary

    Returns:
        dataframe of transactions containing collection, token_id, timestamp, type of transaction,
        from and to addresses
    """

    parsed_data = []

    # Sets for quicker querying
    tx_metadata = set(tx_metadata)
    tx_params = set(tx_params)

    for collection_name, collection in raw_data.items():
        for token_id in collection:
            # List of transaction data
            parsed_tx_data = parse_tx_data(
                collection[token_id]["txs"], tx_metadata, tx_params
            )

            # Add transaction data + token metadata
            for tx_data in parsed_tx_data:
                parsed_data.append(
                    {"collection": collection_name, "token_id": token_id, **tx_data}
                )
    return pd.DataFrame.from_records(parsed_data)


def parse_tx_data(txs: List, tx_metadata: Set, tx_params: Set) -> List:
    """Parses the list of transactions to a dictionary containing the key info for each transaction
    Improvements: enforce type checks for params

    Args:
        txs: list of transactions as follows from the "tx" key of the input found in
        parse_covalent_txs
        tx_metadata: list of keys to extract from each txs dictionary
        tx_params: set of parameters to to extract from the transaction param entries

    Returns:
        list of dicts, each containing block_signed_at, tx_type, from, to, value, name
    """
    parsed_txs = []
    for tx in txs:
        try:
            params = tx["decoded"]["params"]
        except KeyError:
            # skip if transaction is empty
            continue

        parsed_tx = {data: tx[data] if data in tx else None for data in tx_metadata}
        parsed_params = {
            param["name"]: param["value"]
            for param in params
            if param["name"] in tx_params
        }

        parsed_txs.append({**parsed_tx, **parsed_params, "name": tx["decoded"]["name"]})
    return parsed_txs
