"""Tests for schema enforcement nodes"""
from datetime import datetime, timezone

import pandas as pd
import pytest
from web3 import Web3

from networkft.nodes.schema_enforcement import convert_timestamp, convert_wei


@pytest.fixture
def df_tx():
    return pd.DataFrame(
        {
            "collection": ["test_1", "test_2"],
            "token_id": ["0", "1"],
            "block_signed_at": ["2022-01-01T01:23:45Z", "2022-12-31T01:23:45Z"],
            "from": [
                "0x0000000000000000000000000000000000000000",
                "0x1111111111111111111111111111111111111111",
            ],
            "to": [
                "0x2222222222222222222222222222222222222222",
                "0x3333333333333333333333333333333333333333",
            ],
            "value": [None, Web3.toWei(1, "ether")],
            "name": ["test", "Transfer"],
        }
    )


def test_convert_timestamp(df_tx):
    df = convert_timestamp(df_tx, col="block_signed_at")

    expected_df = df_tx.copy()
    expected_df["block_signed_at"] = [
        datetime(2022, 1, 1, 1, 23, 45, tzinfo=timezone.utc),
        datetime(2022, 12, 31, 1, 23, 45, tzinfo=timezone.utc),
    ]

    pd.testing.assert_frame_equal(df, expected_df)


def test_convert_wei(df_tx):
    df = convert_wei(df_tx, col="value")

    expected_df = df_tx.copy()
    expected_df["value"] = [0.0, 1.0]
    # import pdb; pdb.set_trace()
    pd.testing.assert_frame_equal(df, expected_df)
