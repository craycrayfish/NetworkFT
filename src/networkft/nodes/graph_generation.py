"""Nodes to generate graph of capital flow between projects"""
from typing import Dict, List
import pandas as pd
from typing import List


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
        dataframe with directionsin unidirectional format

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


def agg_df(
        df: pd.DataFrame,
        cols: List,
        agg: Dict,
        time_cols: Dict = None
):
    """ Performs groupby and aggregate functions on dataframe

    Args:
        df: dataframe to be grouped
        cols: list of columns to group by (including datetime columns)
        agg: dictionary of aggregate methods for pandas e.g. {"col": "sum}
        time_cols: dictionary of datetime columns with key representing interval to
        group by

    Returns:
        aggregated dataframe
    """
    df_agg = df.groupby(
        [
            pd.Grouper(key=col, freq=time_cols[col]) if col in time_cols else col
            for col in cols
        ],
    ).agg(agg).reset_index()
    return df_agg
