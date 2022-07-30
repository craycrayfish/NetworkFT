"""Pipeline to create dash application
"""
from kedro.pipeline import Pipeline, node

from networkft.nodes.ui import generate_ui_datasets, run_dashboard


def create_ui_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=generate_ui_datasets,
                inputs=["graph", "params:graph"],
                outputs="ui_datasets",
                name="generate_ui_datasets",
            ),
            node(
                func=run_dashboard,
                inputs=["ui_datasets", "params:ui.run_params"],
                outputs=None,
                name="ui",
            ),
        ]
    )
