"""Util functions for node-related operations"""
import pandas as pd
import numpy as np
from typing import Dict


def calculate_edges(
    _graph: pd.DataFrame,
    graph_params: Dict,
    node_positions: pd.DataFrame
) -> pd.DataFrame:
    """Calculates the widths of total flow edge and net flow edge

    Args:
        graph: dataframe containing all edges of the network
        graph_params: parameters used to create graph, containing cols and other
        collection label
        node_positions: dataframe containing nodes and their positions

    Returns:
        dataframe of edges, their coordindates and normalised widths of total
        transactions and net transactions
    """
    # Group by first to reduce size of dataframe
    graph = _graph.groupby(
        ["timestamp", "collection_from", "collection_to"],
        as_index=False
    ).agg(
        {"value": "sum"}
    )

    # Created sorted list so that groupby is agnostic of direction
    graph["collection"] = graph.apply(
        lambda x: sorted([x["collection_from"], x["collection_to"]]),
        axis=1
    )
    graph["directional_value"] = graph.apply(
        lambda x: x["value"] if x["collection"] == x["collection_from"]
        else -x["value"],
        axis=1
    )
    edges = graph.groupby(
        ["timestamp", "collection"]
    ).agg(
        total_value=("value", lambda x: x.abs().sum()),
        net_value=("value", "sum")
    )

    edges[["collection_from", "collection_to"]] = pd.DataFrame(
        edges["collection"].to_list()
    )
    return edges
