"""Style settings for dashboard layouts"""


class Colors:
    """Global colors (dark mode)
    """

    background = "#033538"
    primary = "#0CC4CC"
    secondary = "#CC5B10"

    text_heading = "#DDDDDD"
    text_primary = "#BFBFBF"
    text_secondary = "#888888"


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