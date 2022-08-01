"""Layout to create graph in plotly"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from networkft.ui.styles import Colors, Graph, Styles


def draw_graph(nodes: pd.DataFrame, edges: pd.DataFrame):
    """Creates graph using plotly traces

    Args:
        nodes: dataframe containing all nodes of the network
        edges: dataframe containing all edges of the network

    Returns:
        graph layout object
    """
    fig = go.Figure(layout=go.Layout(**Styles.graph_layout))

    # Draw nodes
    size_scaled = np.power(nodes["total_flow"], Graph.node_scaling)
    size_coeff = Graph.max_node_size / sorted(size_scaled)[-1]
    size = [max(s * size_coeff, Graph.min_node_size) for s in size_scaled]
    fig.add_trace(
        go.Scatter(
            x=nodes["x"],
            y=nodes["y"],
            mode="markers+text",
            marker={"size": size, "color": Colors.node["azuki"]},
            text=nodes["node"],
            textposition="bottom center",
            textfont=Graph.annotation_text,
            customdata=nodes["total_flow"],
            hovertemplate="%{customdata:,.1f}",
            name="",
        )
    )

    # Draw edges
    edges_scaled = np.power(edges["total_value"], Graph.edge_scaling)
    edge_coeff = Graph.max_edge_width / sorted(edges_scaled)[-1]
    for index, edge in edges.iterrows():
        # Total value edge
        fig.add_trace(
            go.Scatter(
                x=[edge["x_from"], edge["x_to"]],
                y=[edge["y_from"], edge["y_to"]],
                mode="lines",
                line={
                    **Graph.total_value_line,
                    "width": max(
                        edge_coeff * edges_scaled[index], Graph.min_edge_width
                    ),
                },
            )
        )
        # Add invisible node in the center for hovertext
        fig.add_trace(
            go.Scatter(
                x=[0.5 * (edge["x_from"] + edge["x_to"])],
                y=[0.5 * (edge["y_from"] + edge["y_to"])],
                mode="markers",
                marker={
                    **Graph.total_value_line,
                    "size": max(edge_coeff * edges_scaled[index], Graph.min_edge_width),
                },
                customdata=[edge["total_value"]],
                hovertemplate="%{customdata:,.1f}",
                name="",
            )
        )
        # Net value edge
        if abs(edge["net_value"]) > 0.1:
            fig.update_layout(
                annotations=[
                    {
                        "x": edge["x_to"],
                        "y": edge["y_to"],
                        "ax": edge["x_from"],
                        "ay": edge["y_from"],
                        "arrowside": "end" if edge["net_value"] < 0 else "start",
                        **Graph.net_value_arrow,
                    }
                ]
            )

    fig.data = fig.data[::-1]
    fig.update_xaxes(**Styles.axes)
    fig.update_yaxes(**Styles.axes, **Styles.yaxes)
    fig.update_layout(showlegend=False)

    return fig
