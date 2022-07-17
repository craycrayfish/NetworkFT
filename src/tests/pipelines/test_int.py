"""Integration test for int pipeline"""
import pandas as pd
import pytest
from kedro.runner import SequentialRunner

from networkft.pipelines.int import create_int_covalent_pipeline


def test_parse_convert_timestamp_integration(
        test_catalog,
        conf_loader,
        raw_tx_path
):
    pipe = create_int_covalent_pipeline().from_inputs(
        "raw_covalent_txs"
    ).to_outputs(
        "raw_covalent_txs_parsed_ts"
    )
    runner = SequentialRunner()
    runner.run(pipe, test_catalog)

    df = test_catalog.load("raw_covalent_txs_parsed_ts")

    assert isinstance(df, pd.DataFrame)
    for col in conf_loader["covalent"]["convert_timestamp"]:
        assert df.dtypes[col] == "datetime64[ns, UTC]"
