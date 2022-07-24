"""Pipeline to prepare primary data table which filters the table of transactions
found in the intermediate layer.
"""
from kedro.pipeline import Pipeline, node

from networkft.nodes.filtering import filter_dataframe


def create_pri_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=filter_dataframe,
                inputs=[
                    "int_covalent_txs",
                    "params:covalent.filter_columns",
                ],
                outputs="pri_txs",
                name="pri_filter",
            )
        ]
    )
