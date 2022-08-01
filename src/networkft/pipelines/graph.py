"""Pipeline to prepare graph data table which creates a table of node and edges
representing a graph of money flow between projects
"""
from kedro.pipeline import Pipeline, node

from networkft.nodes.graph_generation import (
    agg_df,
    convert_to_unidirectional,
    generate_edges,
)


def create_graph_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=convert_to_unidirectional,
                inputs=[
                    "pri_txs",
                    "params:covalent.convert_unidirectional.cols",
                    "params:covalent.convert_unidirectional.entity_col",
                ],
                outputs="pri_txs_uni",
                name="graph_convert_unidirectional",
            ),
            node(
                func=agg_df,
                inputs=[
                    "pri_txs_uni",
                    "params:covalent.groupby",
                    "params:covalent.agg",
                    "params:covalent.time_cols",
                ],
                outputs="pri_txs_uni_agg",
                name="graph_agg_collection",
            ),
            node(
                func=generate_edges,
                inputs=[
                    "pri_txs_uni_agg",
                    "params:graph.cols",
                    "params:graph.other_node_label",
                ],
                outputs="graph",
                name="generate_graph_edges",
            ),
        ]
    )
