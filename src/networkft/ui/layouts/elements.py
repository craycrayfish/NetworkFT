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
    mod = len(timestamps) % interval
    marks = {
        i: {"label": datetime.strptime(ts, Format.dt)}
        if i % interval == mod
        else {"label": ""}
        for i, ts in enumerate(timestamps)
    }
    return dcc.Slider(
        min=timestamps[0],
        max=timestamps[-1],
        value=timestamps[-1],
        step=None,
        marks=marks
    )
