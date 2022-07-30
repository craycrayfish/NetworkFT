"""Elements to be used in main layout
"""
from typing import List
from dash import dcc
from datetime import datetime

from networkft.ui.styles import Format


def timestamp_slider(_timestamps: List, max_marks: int = 5) -> dcc.Slider:
    """ Creates slider to select timestamp to display

    Args:
        _timestamps: list of all timestamps to include
        max_marks: max number of marks in slider

    Returns:
        slider object
    """
    timestamps = sorted(_timestamps)
    interval = int(len(timestamps) / max_marks)
    # Find required remainder for the last timestamp to be shown
    mod = len(timestamps) % interval - 1
    marks = {
        i: {"label": datetime.strftime(ts, Format.dt)}
        if i % interval == mod
        else {"label": ""}
        for i, ts in enumerate(timestamps)
    }
    timestamp_values = list(marks)
    return dcc.Slider(
        min=timestamp_values[0],
        max=timestamp_values[-1],
        value=timestamp_values[-1],
        step=None,
        marks=marks
    )
