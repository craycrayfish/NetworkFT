"""Layout to create graph in plotly"""
from typing import Dict
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd

from networkft.ui.utils.node_operations import calculate_node_positions
from networkft.ui.utils.edge_operations import calculate_edges


def create_graph(graph: pd.DataFrame, graph_params: Dict[str, str]):
    """ Creates graph using plotly traces

    Args:
        graph: dataframe containing all edges of the network
        graph_params: parameters used to create graph, containing cols and other
        collection label

    Returns:
        graph layout object
    """
    node_positions = calculate_node_positions(graph, graph_params)
    edges = calculate_edges(graph, graph_params, node_positions)