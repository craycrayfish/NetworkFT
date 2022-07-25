"""Test filtering nodes"""
import pandas as pd
import pytest

from networkft.nodes.filtering import filter_dataframe


@pytest.fixture
def filter_columns_string():
    return {
        "from": {
            "condition": "!=",
            "value": "0x0000000000000000000000000000000000000000",
        }
    }


@pytest.fixture
def filter_columns_numeric():
    return {"value": {"condition": "<=", "value": 0}}


def test_node_filter_dataframe(df_tx, filter_columns_string, filter_columns_numeric):
    """Test that node is able to filter both string and numeric successfully"""
    df = filter_dataframe(df_tx, filter_columns_string)
    expected_df = df_tx.iloc[0:1, :]
    pd.testing.assert_frame_equal(df, expected_df)

    df = filter_dataframe(df_tx, filter_columns_numeric)
    pd.testing.assert_frame_equal(df, expected_df)
