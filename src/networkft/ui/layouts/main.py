"""Creates layout for main dashboard"""
from typing import Dict
from datetime import datetime
import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc

from networkft.ui.styles import Styles, Layout
from networkft.ui.layouts.graph import create_graph
from networkft.ui.layouts.elements import timestamp_slider


def create_main_layout(
        ui_datasets: Dict[datetime, Dict[str, pd.DataFrame]]
):
    layout = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div(html.H1("NetworkFT")), width=Layout.left_col)
                ],
                style=Styles.header_row
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div("menu"), width=Layout.left_col),
                    dbc.Col(dcc.Graph(id="graph"), width=Layout.right_col)
                ],
                style=Styles.body_row
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div(), width=Layout.left_col),
                    dbc.Col(
                        timestamp_slider(list(ui_datasets)),
                        width=Layout.right_col
                    )
                ]
            )
        ],
        style=Styles.background_container
    )

    return layout
