"""Test util functions for node-related operations"""
import pandas as pd

from networkft.ui.utils.node_operations import calculate_node_positions


def test_calculate_node_positions():
    graph = pd.DataFrame(
        {
            "collection_from": ["a", "b", "c", "d", "O"],
            "collection_to": ["b", "c", "d", "a", "O"]
        }
    )
    graph_params = {"other_collection_label": "O"}
    positions = calculate_node_positions(graph, graph_params)

    expected_positions = pd.DataFrame(
        {
            "x": [0., 1, 0, -1],
            "y": [1., 0, -1, 0]
        },
        index=["a", "b", "c", "d"]
    )
    pd.testing.assert_frame_equal(positions, expected_positions, check_exact=False)
