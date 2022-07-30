"""Layout to create graph in plotly"""
from typing import Dict
from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

from networkft.ui.styles import Styles


def create_graph(graph: pd.DataFrame, graph_params: Dict[str, str]):
    """ Creates graph using plotly traces

    Args:
        graph: dataframe containing all edges of the network
        graph_params: parameters used to create graph, containing cols and other
        collection label

    Returns:
        graph layout object
    """

    fig = go.Figure(layout=go.Layout(**Styles.graph_layout))
    fig.add_trace(
        go.Scatter(
            x=node_positions["x"],
            y=node_positions["y"],
            mode="markers"
        )
    )

    fig.update_xaxes(**Styles.axes)
    fig.update_yaxes(**Styles.axes)

    return fig
