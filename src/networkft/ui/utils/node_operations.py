"""Util functions for node-related operations"""
import pandas as pd
import numpy as np
from typing import Dict


def calculate_node_positions(
        graph: pd.DataFrame,
        graph_params: Dict[str, str]
) -> pd.DataFrame:
    """Calculates node xy coordinate positions

    Args:
        graph: dataframe containing all edges of the network
        graph_params: parameters used to create graph

    Returns:
        Dictionary of nodes and their x, y coordinates
    """
    # First get all nodes
    nodes = pd.concat(
        [graph["collection_from"], graph["collection_to"]]
    ).unique().tolist()
    nodes.remove(graph_params["other_collection_label"])

    # Generate coordinates assuming equidistant along perimeter of circle
    theta = 2 * np.pi / len(nodes)
    node_positions = {
        node: [np.sin(theta * i), np.cos(theta * i)]
        for i, node in enumerate(nodes)
    }
    return pd.DataFrame.from_dict(
        node_positions,
        orient="index",
        columns=["x", "y"]
    )
