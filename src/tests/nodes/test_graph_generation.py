"""Tests for graph generation nodes"""
import pandas as pd
from datetime import datetime, timezone

from networkft.nodes.graph_generation import (
    convert_to_unidirectional,
    agg_df
)

DT_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def test_convert_to_unidirectional(df_tx):
    df = convert_to_unidirectional(df_tx)
    expected_df = pd.DataFrame(
        {
            "collection": ["test"] * 4,
            "token_id": ["0", "1", "0", "1"],
            "timestamp": [
                datetime.strptime("2022-01-01T01:23:45Z", DT_FORMAT).replace(
                    tzinfo=timezone.utc
                ),
                datetime.strptime("2022-12-31T01:23:45Z", DT_FORMAT).replace(
                    tzinfo=timezone.utc
                ),
                datetime.strptime("2022-01-01T01:23:45Z", DT_FORMAT).replace(
                    tzinfo=timezone.utc
                ),
                datetime.strptime("2022-12-31T01:23:45Z", DT_FORMAT).replace(
                    tzinfo=timezone.utc
                ),
            ],
            "entity": [
                "0xed5af388653567af2f388e6224dc7c4b3241c544",
                "0x0000000000000000000000000000000000000000",
                "0xd45058bf25bbd8f586124c479d384c8c708ce23a",
                "0xd45058bf25bbd8f586124c479d384c8c708ce23a",
            ],
            "value": [0.0, 1.0, 0.0, 1.0],
            "name": ["Transfer", "Test", "Transfer", "Test"],
            "direction": ["in", "in", "out", "out"],
        }
    )
    pd.testing.assert_frame_equal(df, expected_df)


def test_agg_df(df_tx):
    df = agg_df(
        df_tx,
        ["timestamp", "collection"],
        {"value": "sum"},
        {"timestamp": "1Y"}
    )
    expected_df = pd.DataFrame(
        {
            "timestamp": [
                datetime.strptime("2022-12-31T00:00:00Z", DT_FORMAT).replace(
                    tzinfo=timezone.utc
                )
            ],
            "collection": ["test"],
            "value": [1.0]
        }
    )
    pd.testing.assert_frame_equal(df, expected_df)
