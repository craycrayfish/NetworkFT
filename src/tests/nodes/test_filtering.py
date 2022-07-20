"""Test filtering nodes"""
import pytest
import pandas as pd

from networkft.nodes.filtering import node_filter_dataframe


@pytest.fixture
def filter_columns():
    return {
        "from": {
            "condition": "!=",
            "value": "0x0000000000000000000000000000000000000000"
        }
    }


def test_node_filter_dataframe(df_tx, filter_columns):
    df = node_filter_dataframe(df_tx)
    expected_df = df_tx.iloc[0, :]
    pd.testing.assert_frame_equal(df, expected_df)
