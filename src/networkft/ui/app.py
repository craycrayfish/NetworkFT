from typing import Dict
from datetime import datetime
import pandas as pd
from dash import Dash
import dash_bootstrap_components as dbc

from networkft.ui.layouts.main import create_main_layout


def create_dash_app(
        ui_datasets: Dict[datetime, Dict[str, pd.DataFrame]]
):
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = create_main_layout(ui_datasets)

    return app