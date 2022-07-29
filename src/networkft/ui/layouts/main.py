"""Creates layout for main dashboard"""
from typing import Dict
import pandas as pd
from dash import html
import dash_bootstrap_components as dbc

from networkft.ui.styles import Styles
from networkft.ui.layouts.graph import create_graph

def create_main_layout(graph: pd.DataFrame, graph_params: Dict):
    layout = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div("menu"), width=3),
                    dbc.Col(create_graph(graph, graph_params))
                ]
            )
        ],
        style=Styles.background_container
    )

    return layout
