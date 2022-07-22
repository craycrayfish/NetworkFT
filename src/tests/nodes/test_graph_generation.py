"""Tests for graph generation nodes"""
import pandas as pd
from datetime import datetime, timezone

from networkft.nodes.graph_generation import node_convert_to_unidirectional


def test_node_convert_to_unidirectional(df_tx):
    df = node_convert_to_unidirectional(df_tx)
    dt_format = "%Y-%m-%dT%H:%M:%SZ"
    expected_df = pd.DataFrame(
        {
            "collection": ["test"] * 4,
            "token_id": ["0", "1", "0", "1"],
            "block_signed_at": [
                datetime.strptime("2022-01-01T01:23:45Z", dt_format).replace(
                    tzinfo=timezone.utc
                ),
                datetime.strptime("2022-12-31T01:23:45Z", dt_format).replace(
                    tzinfo=timezone.utc
                ),
                datetime.strptime("2022-01-01T01:23:45Z", dt_format).replace(
                    tzinfo=timezone.utc
                ),
                datetime.strptime("2022-12-31T01:23:45Z", dt_format).replace(
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
