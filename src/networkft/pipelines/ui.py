"""Pipeline to create dash application
"""
from kedro.pipeline import Pipeline, node

from networkft.nodes.ui import run_dashboard


def create_ui_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=run_dashboard,
                inputs=["graph", "params:ui.run_params"],
                outputs=None,
                name="ui",
            )
        ]
    )
