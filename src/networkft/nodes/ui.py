"""Nodes to generate dashboard"""
from datetime import datetime
from typing import Dict

import numpy as np
import pandas as pd

from networkft.ui.app import create_dash_app


def generate_ui_datasets(
    graph: pd.DataFrame, graph_params: Dict
) -> Dict[datetime, Dict[str, pd.DataFrame]]:
    """Generates the data required to plot the graph on front-end

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
        edge_positions = calculate_edge_positions(edges, node_positions)
        node_sizes = calculate_node_sizes(edges)
        nodes = node_positions.merge(node_sizes, on="node")
        output[timestamp] = {"nodes": nodes, "edges": edge_positions}
    return output


def calculate_node_positions(
    graph: pd.DataFrame, graph_params: Dict[str, str]
) -> pd.DataFrame:
    """Calculates node xy coordinate positions

    Args:
        graph: dataframe containing all edges of the network for a specific timestamp
        graph_params: parameters used to create graph

    Returns:
        Dictionary of nodes and their x, y coordinates
    """
    # First get all nodes
    nodes = pd.concat([graph["node_from"], graph["node_to"]]).unique().tolist()
    if graph_params["other_node_label"] in nodes:
        nodes.remove(graph_params["other_node_label"])

    # Generate coordinates assuming equidistant along perimeter of circle
    theta = 2 * np.pi / len(nodes)
    node_positions = {
        node: [np.sin(theta * i), np.cos(theta * i)] for i, node in enumerate(nodes)
    }
    # Other nodes should be in the center
    node_positions[graph_params["other_node_label"]] = [0, 0]
    return (
        pd.DataFrame.from_dict(node_positions, orient="index", columns=["x", "y"])
        .reset_index()
        .rename(columns={"index": "node"})
    )


def calculate_edges(
    _graph: pd.DataFrame,
) -> pd.DataFrame:
    """Calculates the widths of total flow edge and net flow edge

    Args:
        _graph: dataframe containing all edges of the network at a specific timestamp

    Returns:
        dataframe of edges, their coordindates and normalised widths of total
        transactions and net transactions. Cols are {"node_from",
        "node_to", "node", "total_value", "net_value"}
    """
    # Group by first to reduce size of dataframe
    graph = _graph.groupby(["node_from", "node_to"], as_index=False).agg(
        {"value": "sum"}
    )

    # Created sorted list so that groupby is agnostic of direction
    graph["nodes"] = graph.apply(
        lambda x: ",".join(sorted([x["node_from"], x["node_to"]])), axis=1
    )
    graph["directional_value"] = graph.apply(
        lambda x: x["value"]
        if x["nodes"].split(",")[0] == x["node_from"]
        else -x["value"],
        axis=1,
    )
    edges = graph.groupby("nodes", as_index=False).agg(
        total_value=("directional_value", lambda x: x.abs().sum()),
        net_value=("directional_value", "sum"),
    )
    edges[["node_from", "node_to"]] = pd.DataFrame(
        edges["nodes"].str.split(",").to_list()
    )
    return edges


def calculate_node_sizes(_edges: pd.DataFrame) -> pd.DataFrame:
    """Calculates the relative size of each node by finding the total volume of
    liquidity flowing into and out of the node in a time period

    Args:
        _edges: dataframe of all edges for each timestamp

    Returns:
        dataframe of node size for each timestamp
    """
    edges = _edges.copy()
    edges["node"] = edges["nodes"].str.split(",")
    edges_exploded = edges.explode("node")
    sizes = edges_exploded.groupby("node", as_index=False).agg(
        total_flow=("total_value", "sum")
    )
    return sizes[["node", "total_flow"]]


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


def calculate_edge_positions(_edges: pd.DataFrame, node_positions: pd.DataFrame):
    """Calculates the coordindates required to plot an edge from (x, y) and to (x, y)

    Args:
        _edges: dataframe of edges
        node_positions: dataframe of x and y positions of each node

    Returns:
        dataframe of edges (node_from, node_to) and their coordinates (
        x_from, y_from, x_to, y_to)

    """
    edges = _edges.copy()
    for direction in ["from", "to"]:
        edges = edges.merge(
            node_positions.rename(columns=lambda x: x + f"_{direction}"),
            on=f"node_{direction}",
            how="left",
        )
    return edges
