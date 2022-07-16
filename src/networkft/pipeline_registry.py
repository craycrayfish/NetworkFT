"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

from networkft.pipelines.int import create_int_covalent_pipeline


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    covalent_pipeline = create_int_covalent_pipeline()
    return {"__default__": covalent_pipeline, "covalent": covalent_pipeline}
