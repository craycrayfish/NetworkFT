"""Tests for schema enforcement nodes"""
from datetime import datetime, timezone

import pandas as pd

from networkft.nodes.column_typing import convert_timestamp, convert_wei


def test_convert_timestamp(df_tx):
    df = convert_timestamp(df_tx, col="block_signed_at")
    expected_df = df_tx.copy(deep=True)

    expected_df["block_signed_at"] = [
        datetime(2022, 1, 1, 1, 23, 45, tzinfo=timezone.utc),
        datetime(2022, 12, 31, 1, 23, 45, tzinfo=timezone.utc),
    ]
    print(df.iloc[:, 3])
    print(expected_df.iloc[:, 3])
    pd.testing.assert_frame_equal(df, expected_df)


def test_convert_wei(df_tx):
    df = convert_wei(df_tx, col="value")

    expected_df = df_tx.copy()
    expected_df["value"] = [0.0, 1.0e-18]
    pd.testing.assert_frame_equal(df, expected_df)
