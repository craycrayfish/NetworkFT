"""Nodes to generate graph of capital flow between projects"""
from typing import Dict, List

import pandas as pd


def convert_to_unidirectional(
    _df: pd.DataFrame,
    cols: Dict = {"from": "in", "to": "out"},
    entity_col: str = "entity",
):
    """Node to convert table of transactions from bidirectional to unidirectional
    format.
    Initial: | from | to | value |  Final: | entity | value | direction |
             | AA   | BB | 1.0   |         | AA     | 1.0   | in        |
                                           | BB     | 1.0   | out       |

    Args:
        _df: df representing transactions with columns for sending and receiving parties
        cols: column labels for the sending and receiving addresses, and their
        respective directions
        entity_col: column label to be created containing the from and to addresses

    Returns:
        dataframe with directions in unidirectional format

    """
    assert len(cols) == 2, "`cols` should contain only the from and to labels"

    dfs = []
    for col, direction in cols.items():
        df = _df.copy()
        df["direction"] = direction
        df = df.rename(columns={col: entity_col}).drop(
            [c for c in cols if c != col], axis=1
        )
        dfs.append(df)

    return pd.concat(dfs).reset_index(drop=True)


def agg_df(df: pd.DataFrame, cols: List, agg: Dict, time_cols: Dict = None):
    """Performs groupby and aggregate functions on dataframe

    Args:
        df: dataframe to be grouped
        cols: list of columns to group by (including datetime columns)
        agg: dictionary of aggregate methods for pandas e.g. {"col": "sum}
        time_cols: dictionary of datetime columns with key representing interval to
        group by

    Returns:
        aggregated dataframe
    """
    df_agg = (
        df.groupby(
            [
                pd.Grouper(key=col, freq=time_cols[col]) if col in time_cols else col
                for col in cols
            ],
        )
        .agg(agg)
        .reset_index()
    )
    return df_agg


def generate_edges(df: pd.DataFrame, cols_to_keep: List, other_node_label: str = "O"):
    """Generates edges for a dataframe of transactions. Input dataframe should
    contain the columns timestamp, entity, node, direction, value

    Args:
        df: dataframe to generate edges from
        cols_to_keep: columns to keep in returned dataframe
        other_node_label: label for nodes not included in dataset

    Returns:
        dataframe containing edges
    """
    # Find groups of trades that contain liquidity flow between nodes
    # Internal means liquidity is contained within network
    node_dir_count = (
        df.groupby(["timestamp", "entity"])
        .agg(
            node_count=("node", lambda x: x.nunique()),
            direction_count=("direction", lambda x: x.nunique()),
        )
        .reset_index()
    )

    df_direction = df.merge(node_dir_count, on=["timestamp", "entity"])

    internal_mask = (df_direction["direction_count"] > 1) & (
        df_direction["node_count"] > 1
    )

    internal_edges = generate_internal_edges(
        df_direction[internal_mask], other_node_label
    )
    external_edges = generate_external_edges(
        df_direction[~internal_mask], other_node_label
    )
    df_edges = pd.concat([internal_edges, external_edges]).reset_index(drop=True)
    return df_edges[cols_to_keep]


def generate_internal_edges(df: pd.DataFrame, other_node_label: str):
    """Generates edges contained within the network of nodes in the dataframe

    Args:
        df: dataframe containing transactions aggregated at a timestamp, node,
        entity level
        other_node_label: label for nodes not included in dataset

    Returns:
        dataframe of internal edges (and external where necessary)
    """
    dfs = []
    # First calculate liquidity flow within the nodes
    for index, group in df.groupby("entity"):
        # Get total value going into and out of the network
        df_from = group[group["direction"] == "in"].copy()
        df_from["total_value"] = df_from["value"].sum()

        df_to = group[group["direction"] == "out"].copy()
        df_to["total_value"] = df_to["value"].sum()

        # Generates all from-to permutations
        df_from_to = df_from.merge(df_to, on="timestamp", suffixes=("_from", "_to"))

        # Determine expected transfer values using to and from values (not accounting
        # for liquidity constrains within the network)
        df_from_to["expected_value_from"] = (
            df_from_to["value_from"]
            * df_from_to["value_to"]
            / df_from_to["total_value_to"]
        )
        df_from_to["expected_value_to"] = (
            df_from_to["value_to"]
            * df_from_to["value_from"]
            / df_from_to["total_value_from"]
        )
        # Actual value transferred is constrained by the minimum
        df_from_to["value"] = df_from_to[
            ["expected_value_from", "expected_value_to"]
        ].min(axis=1)

        dfs.append(df_from_to)

    df_edge_inter = pd.concat(dfs)

    # Next calculate liquidity injections and outflows
    df_edge_inter["outflow"] = (
        df_edge_inter["expected_value_from"] - df_edge_inter["expected_value_to"]
    )

    outflow_mask = df_edge_inter["outflow"] > 0

    outflows = (
        df_edge_inter[outflow_mask]
        .groupby(["timestamp", "node_to"])
        .agg(value=("outflow", "sum"))
        .reset_index()
    )
    outflows["node_from"] = other_node_label

    inflows = (
        df_edge_inter[~outflow_mask]
        .groupby(["timestamp", "node_from"])
        .agg(value=("outflow", "sum"))
        .abs()
        .reset_index()
    )
    inflows["node_to"] = other_node_label

    return pd.concat([df_edge_inter, inflows, outflows])[
        ["timestamp", "node_to", "node_from", "value"]
    ].reset_index(drop=True)


def generate_external_edges(df: pd.DataFrame, other_node_label: str):
    """Generates edges leading to nodes outside the network

    Args:
        df: dataframe containing transactions aggregated at a timestamp, node,
        entity level
        other_node_label: label for nodes not included in dataset

    Returns:
        dataframe of external edges
    """
    in_mask = df["direction"] == "in"
    df_in = (
        df[in_mask].copy().rename({"node": "node_to"}, axis=1).reset_index(drop=True)
    )
    df_in["node_from"] = other_node_label

    return df_in
