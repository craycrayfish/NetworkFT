"""Integration test for int pipeline"""
import pandas as pd
import pytest
from kedro.runner import SequentialRunner

from networkft.pipelines.int import create_int_covalent_pipeline


def test_parse_convert_timestamp_integration(
        test_catalog,
        raw_tx_path,
        params,
        df_tx
):
    pipe = create_int_covalent_pipeline()
    runner = SequentialRunner()
    runner.run(pipe, test_catalog)
    df = test_catalog.load("int_covalent_txs")

    pd.testing.assert_frame_equal(df, df_tx)
