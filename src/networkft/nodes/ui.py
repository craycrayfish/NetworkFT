"""Nodes to generate dashboard"""
from typing import Dict
from datetime import datetime
import numpy as np
import pandas as pd

from networkft.ui.app import create_dash_app


def generate_ui_datasets(
        graph: pd.DataFrame,
        graph_params: Dict
) -> Dict[datetime, Dict[str, pd.DataFrame]]:
    """ Generates the data required to plot the graph on front-end

    Args:
        graph: dataframe containing all edges of the network of liquidity flow
        graph_params: parameters used to create graph

    Returns:
        dictionary where top-level is timestamp, and each timestamp has a value of a
        dictionary containing node positions, node sizes and edges
    """
    output = {}
    for timestamp, group in graph.groupby("timestamp"):
        node_positions = calculate_node_positions(group, graph_params)
        edges = calculate_edges(group)
        node_sizes = calculate_node_sizes(edges)
        nodes = node_positions.merge(
            node_sizes, left_on="node", right_on="collection"
        ).drop(
            columns=["collection"]
        )
        output[timestamp] = {"nodes": nodes, "edges": edges}
    return output


def calculate_node_positions(
        graph: pd.DataFrame,
        graph_params: Dict[str, str]
) -> pd.DataFrame:
    """Calculates node xy coordinate positions

    Args:
        graph: dataframe containing all edges of the network for a specific timestamp
        graph_params: parameters used to create graph

    Returns:
        Dictionary of nodes and their x, y coordinates
    """
    # First get all nodes
    nodes = pd.concat(
        [graph["collection_from"], graph["collection_to"]]
    ).unique().tolist()
    if graph_params["other_collection_label"] in nodes:
        nodes.remove(graph_params["other_collection_label"])

    # Generate coordinates assuming equidistant along perimeter of circle
    theta = 2 * np.pi / len(nodes)
    node_positions = {
        i: [node, np.sin(theta * i), np.cos(theta * i)]
        for i, node in enumerate(nodes)
    }
    return pd.DataFrame.from_dict(
        node_positions,
        orient="index",
        columns=["node", "x", "y"]
    )


def calculate_edges(
    _graph: pd.DataFrame,
) -> pd.DataFrame:
    """Calculates the widths of total flow edge and net flow edge

    Args:
        _graph: dataframe containing all edges of the network at a specific timestamp

    Returns:
        dataframe of edges, their coordindates and normalised widths of total
        transactions and net transactions
    """
    # Group by first to reduce size of dataframe
    graph = _graph.groupby(
        ["collection_from", "collection_to"],
        as_index=False
    ).agg(
        {"value": "sum"}
    )

    # Created sorted list so that groupby is agnostic of direction
    graph["collection"] = graph.apply(
        lambda x: ",".join(sorted([x["collection_from"], x["collection_to"]])),
        axis=1
    )
    graph["directional_value"] = graph.apply(
        lambda x: x["value"]
        if x["collection"].split(",")[0] == x["collection_from"]
        else -x["value"],
        axis=1
    )
    edges = graph.groupby("collection", as_index=False).agg(
        total_value=("directional_value", lambda x: x.abs().sum()),
        net_value=("directional_value", "sum")
    )
    edges[["collection_from", "collection_to"]] = pd.DataFrame(
        edges["collection"].str.split(",").to_list()
    )
    return edges


def calculate_node_sizes(
    _edges: pd.DataFrame
) -> pd.DataFrame:
    """ Calculates the relative size of each node by finding the total volume of
    liquidity flowing into and out of the collection in a time period

    Args:
        _edges: dataframe of all edges for each timestamp

    Returns:
        dataframe of node size for each timestamp
    """
    edges = _edges.copy()
    edges["collection"] = edges["collection"].str.split(",")
    edges_exploded = edges.explode("collection")
    sizes = edges_exploded.groupby(
        "collection",
        as_index=False
    ).agg(
        total_flow=("total_value", "sum")
    )
    sizes["size"] = sizes["total_flow"] / sizes["total_flow"].max()
    return sizes[["collection", "total_flow", "size"]]


def run_dashboard(
        ui_datasets: Dict[datetime, Dict[str, pd.DataFrame]],
        run_params: Dict,
):
    """Node to create and run frontend dashboard

    Args:
        ui_datasets: dictionary with the following format
        {
            timestamp: {
                "edges": dataframe of edges,
                "nodes": dataframe of nodes
            }
        }
        run_params: parameters for run app
    """
    app = create_dash_app(ui_datasets)

    app.run_server(**run_params)
