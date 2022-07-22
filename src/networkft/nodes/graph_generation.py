"""Nodes to generate graph of capital flow between projects"""
from typing import Dict
import pandas as pd


def node_convert_to_unidirectional(
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
