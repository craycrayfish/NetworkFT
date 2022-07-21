"""Nodes to generate graph of capital flow between projects"""
from typing import List
import pandas as pd


def node_convert_to_unidirectional(
        _df: pd.DataFrame,
        cols: List = ["from", "to"],
        entity_col: str = "entity"
):
    """Node to convert table of transactions from bidirectional to unidirectional
    format.

    Args:
        _df:
        cols:
        entity_col:

    Returns:

    """
    df = _df.copy()
    return df
