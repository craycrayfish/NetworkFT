"""Pipeline to parse transaction data downloaded from covalent api.
Transforms raw data to intermediate layer
"""

from kedro.pipeline import Pipeline, node

from networkft.nodes.covalent_txs import parse_covalent_txs


def create_int_covalent_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=parse_covalent_txs,
                inputs=[
                    "raw_covalent_nft_txs",
                    "params:covalent.tx_metadata",
                    "params:covalent.tx_params",
                ],
                outputs="int_covalent_nft_txs",
                name="int_parse_covalent_txs_node",
            )
        ]
    )
