"""Style settings for dashboard layouts"""


class Colors:
    """Global colors (dark mode)
    """
    background = "#001417"
    primary = "#0CC4CC"
    secondary = "#CC5B10"

    text_heading = "#DDDDDD"
    text_primary = "#BFBFBF"
    text_secondary = "#888888"


class Layout:
    """Layout formatting
    """
    left_col = 2
    right_col = 8


class Format:
    """Formatting for python objects like datetime
    """
    dt = "%d-%b-%y"


class Styles:
    """Style settings for elements
    """
    background_container = {
        "backgroundColor": Colors.background,
        "color": Colors.text_primary,
        "height": "100vh",
        "width": "100vw"
    }

    text = {
        "color": Colors.text_primary
    }

    graph_layout = {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)"
    }

    axes = {
        "showline": False,
        "showgrid": False,
        "zeroline": False,
        "showticklabels": False
    }
