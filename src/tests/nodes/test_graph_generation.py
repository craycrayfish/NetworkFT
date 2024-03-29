"""Tests for graph generation nodes"""
from datetime import datetime, timezone

import pandas as pd

from networkft.nodes.graph_generation import (
    agg_df,
    convert_to_unidirectional,
    generate_edges,
    generate_external_edges,
    generate_internal_edges,
)

DT_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def test_convert_to_unidirectional(df_tx):
    df = convert_to_unidirectional(df_tx)
    expected_df = pd.DataFrame(
        {
            "node": ["test"] * 4,
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
    df = agg_df(df_tx, ["timestamp", "node"], {"value": "sum"}, {"timestamp": "1Y"})
    expected_df = pd.DataFrame(
        {
            "timestamp": [
                datetime.strptime("2022-12-31T00:00:00Z", DT_FORMAT).replace(
                    tzinfo=timezone.utc
                )
            ],
            "node": ["test"],
            "value": [1.0],
        }
    )
    pd.testing.assert_frame_equal(df, expected_df)


def test_generate_internal_edges(df_tx_graph):
    df = generate_internal_edges(df_tx_graph, "O")
    expected_df = pd.DataFrame(
        {
            "timestamp": [0] * 9,
            "node_to": ["C", "D", "C", "D", "D", "D", "O", "O", "D"],
            "node_from": ["A", "A", "B", "B", "A", "B", "A", "B", "O"],
            "value": [
                1.8181818,
                3.18181818,
                3.63636,
                6.36363,
                1.125,
                1.875,
                2.33333,
                4.66666,
                5.0,
            ],
        }
    )
    pd.testing.assert_frame_equal(
        df,
        expected_df,
        check_exact=False,
    )


def test_generate_external_edges(df_tx_graph):
    df = generate_external_edges(df_tx_graph, "O")
    df_expected = pd.DataFrame(
        {
            "timestamp": [0] * 4,
            "node_to": ["A", "B", "A", "B"],
            "entity": [1, 1, 2, 2],
            "direction": ["in"] * 4,
            "value": [5, 10, 3, 5],
            "node_from": ["O"] * 4,
        }
    )
    pd.testing.assert_frame_equal(df, df_expected)


def test_generate_edges(df_tx_graph):
    df_tx_graph_extra = pd.concat(
        [
            df_tx_graph,
            pd.DataFrame(
                {
                    "timestamp": [1],
                    "node": ["A"],
                    "entity": [1],
                    "direction": ["in"],
                    "value": [5],
                }
            ),
        ]
    )

    df = generate_edges(
        df_tx_graph_extra,
        cols_to_keep=["timestamp", "node_from", "node_to", "value"],
    )
    expected_df = pd.DataFrame(
        {
            "timestamp": [0] * 9 + [1],
            "node_from": ["A", "A", "B", "B", "A", "B", "A", "B", "O", "O"],
            "node_to": ["C", "D", "C", "D", "D", "D", "O", "O", "D", "A"],
            "value": [
                1.8181818,
                3.18181818,
                3.63636,
                6.36363,
                1.125,
                1.875,
                2.33333,
                4.66666,
                5.0,
                5.0,
            ],
        }
    )
    pd.testing.assert_frame_equal(df, expected_df, check_exact=False)
