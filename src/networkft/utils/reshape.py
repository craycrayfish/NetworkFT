"""Util functions for changing the shape of data structures"""
from collections.abc import MutableMapping
from typing import Dict


def flatten_dict(d: Dict, parent_key: str = '', sep: str = "."):
    """ Flattens a dictionary nested multiple times

    Args:
        d: dictionary object to flatten
        parent_key: (optional) root of key names
        sep: separator for keys of different levels

    Returns:
        flattened dictionary
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
