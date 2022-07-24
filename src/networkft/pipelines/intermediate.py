"""Pipeline to parse transaction data downloaded from covalent api.
Transforms raw data to intermediate layer
"""

from kedro.pipeline import Pipeline, node

from networkft.nodes.column_typing import convert_timestamp, convert_wei, rename_columns
from networkft.nodes.covalent_txs import parse_covalent_txs


def create_int_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=parse_covalent_txs,
                inputs=[
                    "raw_covalent_txs",
                    "params:covalent.tx_metadata",
                    "params:covalent.tx_params",
                ],
                outputs="raw_covalent_txs_parsed",
                name="int_parse_covalent_txs",
            ),
            node(
                func=convert_timestamp,
                inputs=["raw_covalent_txs_parsed", "params:covalent.convert_timestamp"],
                outputs="raw_covalent_txs_parsed_ts",
                name="int_convert_ts_covalent_txs",
            ),
            node(
                func=convert_wei,
                inputs=["raw_covalent_txs_parsed_ts", "params:covalent.convert_wei"],
                outputs="raw_covalent_txs_parsed_ts_wei",
                name="int_convert_wei_covalent_txs",
            ),
            node(
                func=rename_columns,
                inputs=[
                    "raw_covalent_txs_parsed_ts_wei",
                    "params:covalent.rename_columns"
                ],
                outputs="int_covalent_txs",
                name="int_rename_columns"
            )
        ]
    )
