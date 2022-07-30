"""Creates layout for main dashboard"""
from datetime import datetime
from typing import Dict

import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html

from networkft.ui.layouts.elements import timestamp_slider
from networkft.ui.styles import Layout, Styles


def create_main_layout(ui_datasets: Dict[datetime, Dict[str, pd.DataFrame]]):
    layout = html.Div(
        [
            dbc.Row(
                [dbc.Col(html.Div(html.H1("NetworkFT")), width=Layout.left_col)],
                style=Styles.header_row,
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div("menu"), width=Layout.left_col),
                    dbc.Col(dcc.Graph(id="graph"), width=Layout.right_col),
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

    return layout
