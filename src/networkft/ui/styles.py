"""Style settings for dashboard layouts"""


class Colors:
    """Global colors (dark mode)"""

    background = "#001417"
    primary = "#0CC4CC"
    secondary = "#CC5B10"

    text_heading = "#DDDDDD"
    text_primary = "#BFBFBF"
    text_secondary = "#888888"

    node = {"azuki": "rgba(192,53,64,1)"}


class Layout:
    """Layout formatting"""

    left_col = {"size": 1, "offset": 1}
    right_col = {"size": 8}


class Format:
    """Formatting for python objects like datetime"""

    dt = "%d-%b-%y"


class Styles:
    """Style settings for elements"""

    background_container = {
        "backgroundColor": Colors.background,
        "color": Colors.text_primary,
        "height": "100vh",
        "width": "100vw",
    }

    text = {"color": Colors.text_primary}

    header_row = {"margin": "0 0 1rem 0"}
    body_row = {"margin": "1rem 0"}

    graph = {"height": "70vh"}

    graph_layout = {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
    }

    axes = {
        "showline": False,
        "showgrid": False,
        "zeroline": False,
        "showticklabels": False,
    }

    yaxes = {"scaleanchor": "x", "scaleratio": 1}


class Graph:
    """Arguments to control graph formatting"""

    node_scaling = 0.5
    max_node_size = 180
    min_node_size = 30

    edge_scaling = 0.5
    max_edge_width = 20
    min_edge_width = 2

    annotation_text = {"color": Colors.text_primary}

    total_value_line = {"color": "rgba(0.7,0.7,0.7,0.6)"}

    net_value_arrow = {
        "arrowsize": 3,
        "arrowwidth": 1,
        "arrowhead": 1,
        "arrowcolor": "white",
        "font": {"color": Colors.text_primary, "size": 12},
    }
