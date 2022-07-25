"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

from networkft.pipelines.intermediate import create_int_pipeline
from networkft.pipelines.primary import create_pri_pipeline
from networkft.pipelines.graph import create_graph_pipeline


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    covalent_pipeline = (
        create_int_pipeline() + create_pri_pipeline() + create_graph_pipeline()
    )
    return {"__default__": covalent_pipeline, "covalent": covalent_pipeline}
