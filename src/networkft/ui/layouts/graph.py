"""Layout to create graph in plotly"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from networkft.ui.styles import Styles, Graph


def draw_graph(nodes: pd.DataFrame, edges: pd.DataFrame):
    """Creates graph using plotly traces

    Args:
        nodes: dataframe containing all nodes of the network
        edges: dataframe containing all edges of the network

    Returns:
        graph layout object
    """
    size_scaled = np.power(nodes["total_flow"], Graph.node_scaling)
    size_coeff = Graph.max_node_size / sorted(size_scaled)[-1]
    size = [
        max(s * size_coeff, Graph.min_node_size)
        for s in size_scaled
    ]

    fig = go.Figure(layout=go.Layout(**Styles.graph_layout))
    # Draw nodes
    fig.add_trace(
        go.Scatter(
            x=nodes["x"],
            y=nodes["y"],
            mode="markers+text",
            marker={
                "size": size,
            },
            text=nodes["node"],
            textposition="bottom center",
            textfont=Graph.annotation_text,
            customdata=nodes["total_flow"],
            hovertemplate="%{customdata:.1f}",
            name="",
        )
    )
    # Mapping for node positions {node: [x, y]}
    nodes_map = {node["node"]: [node["x"], node["y"]] for i, node in nodes.iterrows()}

    # Draw edges
    edges_scaled = np.power(edges["total_value"], Graph.edge_scaling)
    edge_coeff = Graph.max_edge_width / sorted(edges_scaled)[-1]
    for index, edge in edges.iterrows():
        fig.add_trace(
            go.Scatter(

            )
        )

    fig.update_xaxes(**Styles.axes)
    fig.update_yaxes(**Styles.axes, **Styles.yaxes)

    return fig
