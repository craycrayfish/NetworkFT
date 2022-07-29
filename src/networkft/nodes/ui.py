"""Nodes to generate dashboard"""
from typing import Dict

import pandas as pd

from networkft.ui.app import create_dash_app


def run_dashboard(graph: pd.DataFrame, run_params: Dict, graph_params: Dict):
    """Node to create and run frontend dashboard

    Args:
        graph: dataframe containing all edges of the network of liquidity flow
        run_params: parameters for run app
        graph_params: parameters used to create graph
    """
    app = create_dash_app(graph, graph_params)

    app.run_server(**run_params)
