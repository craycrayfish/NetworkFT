"""Nodes to filter dataframe in various ways"""
import logging
from typing import Dict

import pandas as pd

LOGGER = logging.Logger


def filter_dataframe(_df: pd.DataFrame, filter_columns: Dict):
    """Filters dataframe based on the conditions defined in yml.
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

        assert (
            "condition" in rule and "value" in rule
        ), "`condition` or `rule` not defined in `filter_columns`"

        if isinstance(rule["value"], str):
            value = f"'{rule['value']}'"
        else:
            value = rule["value"]

        df = df.query(f"`{col}` {rule['condition']} {value}")

    return df
