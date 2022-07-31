"""Test functions used to create the datasets required for ui"""
import numpy as np
import pandas as pd
import pytest

from networkft.nodes.ui import (
    calculate_edge_positions,
    calculate_edges,
    calculate_node_positions,
    calculate_node_sizes,
    generate_ui_datasets,
)


@pytest.fixture
def graph_params():
    return {"other_node_label": "O"}


@pytest.fixture
def graph():
    """Corresponds to the edges below"""
    return pd.DataFrame(
        {
            "node_from": ["A", "B", "A", "A"],
            "node_to": ["B", "A", "B", "C"],
            "value": [1, 2, 3, 4],
        }
    )


@pytest.fixture
def edges():
    """Corresponds to the graph above"""
    return pd.DataFrame(
        {
            "nodes": ["A,B", "A,C"],
            "total_value": [6, 4],
            "net_value": [2, 4],
            "node_from": ["A", "A"],
            "node_to": ["B", "C"],
        }
    )


def test_generate_ui_datasets(graph, graph_params, edges):
    graph_with_ts = graph.copy()
    graph_with_ts["timestamp"] = [0, 0, 0, 0]
    ui_datasets = generate_ui_datasets(graph_with_ts, graph_params)
    expected_ui_datasets = {
        0: {
            "nodes": pd.DataFrame(
                {
                    "node": ["A", "B", "C"],
                    "x": [0.0, np.sin(np.pi * 2 / 3), np.sin(np.pi * 4 / 3)],
                    "y": [1.0, np.cos(np.pi * 2 / 3), np.cos(np.pi * 4 / 3)],
                    "total_flow": [10, 6, 4],
                }
            ),
            "edges": pd.concat(
                [
                    edges,
                    pd.DataFrame(
                        {
                            "x_from": [0.0, 0.0],
                            "y_from": [1.0, 1.0],
                            "x_to": [np.sin(np.pi * 2 / 3), np.sin(np.pi * 4 / 3)],
                            "y_to": [np.cos(np.pi * 2 / 3), np.cos(np.pi * 4 / 3)],
                        }
                    ),
                ],
                axis=1,
            ),
        }
    }
    for ts, datasets in ui_datasets.items():
        for element, df in datasets.items():
            pd.testing.assert_frame_equal(df, expected_ui_datasets[ts][element])


def test_calculate_node_positions(graph, graph_params):
    positions = calculate_node_positions(graph, graph_params)
    expected_positions = pd.DataFrame(
        {
            "node": ["A", "B", "C", "O"],
            "x": [0.0, np.sin(np.pi * 2 / 3), np.sin(np.pi * 4 / 3), 0],
            "y": [1.0, np.cos(np.pi * 2 / 3), np.cos(np.pi * 4 / 3), 0],
        }
    )
    pd.testing.assert_frame_equal(positions, expected_positions, check_exact=False)


def test_calculate_edges(graph, edges):
    pd.testing.assert_frame_equal(calculate_edges(graph), edges)


def test_calculate_node_sizes(edges):
    node_sizes = calculate_node_sizes(edges)
    expected_node_sizes = pd.DataFrame(
        {"node": ["A", "B", "C"], "total_flow": [10, 6, 4]}
    )
    pd.testing.assert_frame_equal(node_sizes, expected_node_sizes)


def test_calculate_edges_positions(edges):
    positions = pd.DataFrame({"node": ["A", "B", "C"], "x": [0, 1, 2], "y": [1, 2, 3]})
    edge_positions = calculate_edge_positions(edges, positions)
    expected_edge_positions = pd.DataFrame(
        {
            "node_from": ["A", "A"],
            "node_to": ["B", "C"],
            "x_from": [0, 0],
            "y_from": [1, 1],
            "x_to": [1, 2],
            "y_to": [2, 3],
        }
    )
    pd.testing.assert_frame_equal(
        edge_positions[list(expected_edge_positions)], expected_edge_positions
    )
