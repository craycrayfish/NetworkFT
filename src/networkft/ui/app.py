from datetime import datetime
from typing import Dict

import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash

from networkft.ui.layouts.main import create_main_layout


def create_dash_app(ui_datasets: Dict[datetime, Dict[str, pd.DataFrame]]):
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = create_main_layout(ui_datasets)

    return app
