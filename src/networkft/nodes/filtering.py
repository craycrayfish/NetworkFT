"""Nodes to filter dataframe in various ways"""
from typing import Dict
import pandas as pd
import logging

LOGGER = logging.Logger


def node_filter_dataframe(_df: pd.DataFrame, filter_columns: Dict):
    """ Filters dataframe based on the conditions defined in yml.
    Expects conditions to be defined in the following format
    filter_columns:
      column_1:
        condition: "<"
        value: 1

    Args:
        df: dataframe to be filtered
        filter_columns: dictionary containing rules to filter

    Returns:
        filtered dataframe
    """
    df = _df.copy()

    for col, rule in filter_columns.items():
        assert col in df, f"`{col}` column defined in `filter_columns does not exist"

        assert "condition" in rule and "value" in rule, (
            "`condition` or `rule` not defined in `filter_columns`"
        )

        df = df.query(f"{col} {rule['condition']} {rule['value']}")

    return df
