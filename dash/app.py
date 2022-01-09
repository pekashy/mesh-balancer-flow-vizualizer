import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import flask

from active_requests_count import get_active_request_count_chart
from pre_processing_delay import get_pre_processing_delay_chart
from total_delay_chart import get_total_delay_chart
from rps_chart import get_rps_chart
from requests_timeline import get_requests_timeline


def layout():
    return html.Div(
        children=[
            html.Div(children="""Request Flow for multiple instances of service"""),
            dcc.Graph(
                id="instance-timeline",
                figure=get_requests_timeline()
            ),
            dcc.Graph(
                id="active_requests-for-time-chart",
                figure=get_active_request_count_chart()
            ),
            dcc.Graph(
                id="rps-chart",
                figure=get_rps_chart()
            ),
            dcc.Graph(
                id="total-delay-chart",
                figure=get_total_delay_chart()
            ),
            dcc.Graph(
                id="pre-proc-delay-chart",
                figure=get_pre_processing_delay_chart()
            ),
        ]
    )


server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True
app.layout = layout

if __name__ == "__main__":
    import os
    debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True
    app.run_server(host="0.0.0.0", port=8050, debug=debug)
