import plotly.express as px
import pandas as pd
import json


def get_requests_timeline():
    probe_events = list()
    with open('/results/request_times.json') as data_file:
        probe_events_raw = json.load(data_file)

    for probe_event_raw in probe_events_raw:
        probe_events.append(dict(Instance=probe_event_raw.get('instance'),
                                 Start=pd.to_datetime(probe_event_raw.get('req_snd_time'), unit='s'),
                                 Finish=pd.to_datetime(probe_event_raw.get('resp_rcv_time'), unit='s')))
    df = pd.DataFrame(probe_events)
    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Instance")
    fig.update_yaxes(autorange="reversed")
    return fig
