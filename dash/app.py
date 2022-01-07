import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import flask
from requests_timeline import get_requests_timeline

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True


def layout():
    return html.Div(
        children=[
            html.H1(children="Hello Dash 2020"),
            html.Div(children="""Dash: A web application framework for Python."""),
            dcc.Graph(
                id="example-graph",
                figure=get_requests_timeline()
            ),
        ]
    )


app.layout = layout

if __name__ == "__main__":
    import os

    debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True
    app.run_server(host="0.0.0.0", port=8050, debug=debug)
