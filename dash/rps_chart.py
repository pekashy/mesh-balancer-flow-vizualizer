import plotly.express as px
import pandas as pd
import json

from numpy import finfo


def get_rps_chart():
    with open('/results/request_times.json') as data_file:
        probe_events_raw = json.load(data_file)
    start_time = min(probe_events_raw, key=lambda x: x.get('req_snd_time', finfo('d').max)) \
        .get('req_snd_time', finfo('d').max)
    probe_events_raw_sorted_end = sorted(probe_events_raw, key=lambda e: (e.get('resp_rcv_time', finfo('d').max)))
    rpses = list()
    for request_id, probe_event_raw in enumerate(probe_events_raw_sorted_end):
        resp_recv_time = probe_event_raw.get('resp_rcv_time')
        req_snd_time = probe_event_raw.get('req_snd_time')
        time_passed = resp_recv_time - start_time
        rps = request_id / time_passed
        rpses.append(dict(RPS=rps, TimeSent=pd.to_datetime(req_snd_time, unit='s'),
                          TimeReceived=pd.to_datetime(resp_recv_time, unit='s')))
    df = pd.DataFrame(rpses)
    fig = px.line(df, x='TimeReceived', y='RPS', title='RPS for time')
    return fig
