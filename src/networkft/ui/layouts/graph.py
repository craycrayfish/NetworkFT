"""Layout to create graph in plotly"""
import pandas as pd
import plotly.graph_objects as go

from networkft.ui.styles import Styles


def create_graph(nodes: pd.DataFrame, edges: pd.DataFrame):
    """Creates graph using plotly traces

    Args:
        nodes: dataframe containing all nodes of the network
        edges: dataframe containing all edges of the network

    Returns:
        graph layout object
    """

    fig = go.Figure(layout=go.Layout(**Styles.graph_layout))
    fig.add_trace(go.Scatter(x=nodes["x"], y=nodes["y"], mode="markers"))

    fig.update_xaxes(**Styles.axes)
    fig.update_yaxes(**Styles.axes)

    return fig
