from typing import Dict
import pandas as pd
from dash import Dash
import dash_bootstrap_components as dbc

from networkft.ui.layouts.main import create_main_layout


def create_dash_app(graph: pd.DataFrame, graph_params: Dict):
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = create_main_layout(graph, graph_params)

    return app
