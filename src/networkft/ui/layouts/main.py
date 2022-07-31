"""Creates layout for main dashboard"""
from datetime import datetime
from typing import Dict

import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, dcc, html
from dash.dash import Dash

from networkft.ui.layouts.elements import timestamp_slider
from networkft.ui.layouts.graph import draw_graph
from networkft.ui.styles import Layout, Styles


def create_main_layout(app: Dash, ui_datasets: Dict[datetime, Dict[str, pd.DataFrame]]):
    layout = html.Div(
        [
            dbc.Row(
                [dbc.Col(html.Div(html.H1("NetworkFT")), width=Layout.left_col)],
                style=Styles.header_row,
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div(), width=Layout.left_col),
                    dbc.Col(
                        dcc.Graph(id="graph", style=Styles.graph),
                        width=Layout.right_col,
                    ),
                ],
                style=Styles.body_row,
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div(), width=Layout.left_col),
                    dbc.Col(
                        timestamp_slider(list(ui_datasets)), width=Layout.right_col
                    ),
                ]
            ),
        ],
        style=Styles.background_container,
    )

    @app.callback(Output("graph", "figure"), Input("timestamp_slider", "value"))
    def update_graph(timestamp):
        """Updates the graph based on the selected timestamp

        Args:
            timestamp: integer index of the selected timestamp

        Returns:
            graph object
        """
        dataset = ui_datasets[list(ui_datasets)[timestamp]]
        return draw_graph(dataset["nodes"], dataset["edges"])

    return layout
