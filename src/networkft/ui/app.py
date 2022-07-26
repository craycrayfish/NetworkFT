import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html


def create_dash_app(graph):
    app = Dash(__name__)

    df = pd.DataFrame(
        {
            "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
            "Amount": [4, 1, 2, 2, 4, 5],
            "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
        }
    )

    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

    app.layout = html.Div(
        children=[
            html.H1(children="Hello Dash"),
            html.Div(
                children="""
            Dash: A web application framework for your data.
        """
            ),
            dcc.Graph(id="example-graph", figure=fig),
        ]
    )

    return app
