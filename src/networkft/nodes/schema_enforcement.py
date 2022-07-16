"""Nodes to enforce column schema"""
from typing import Union, List
import pandas as pd
from web3 import Web3


def convert_timestamp(
    df: pd.DataFrame,
    col: Union[str, List],
    dt_format: str = None,
    errors: str = "raise",
):
    """Converts a specific column or list of columns in a dataframe to datetime format

    Args:
        df: dataframe with columns to be converted
        col: column or list of columns with timestamp to be converted
        dt_format: string showing strftime format to convert columns on
        errors: behaviour if error encountered; can be "raise", "ignore" or "coerce"

    Returns:
        dataframe with column(s) converted
    """
    if isinstance(col, str):
        col = [col]

    if format:
        infer = True
    else:
        infer = False

    for column in col:
        df[column] = pd.to_datetime(
            df[column], errors=errors, format=dt_format, infer_datetime_format=infer
        )

    return df


def convert_wei(input_df: pd.DataFrame, col: Union[str, List]):
    """Converts a specific column of list of columns from wei units to ether

    Args:
        df: dataframe with columns to be converted
        col: column or list of columns to be converted

    Returns:
        dataframe with columns converted
    """
    df = input_df.copy()

    if isinstance(col, str):
        col = [col]

    df[col] = df[col].apply(
        lambda x: [
            float(Web3.fromWei(val, "ether")) if pd.notnull(val) else 0.0 for val in x
        ]
    )
    return df
