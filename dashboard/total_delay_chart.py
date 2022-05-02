import json
from datetime import datetime

import pandas as pd
import plotly.express as px
from numpy import finfo


def get_total_delay_chart():
    with open('/results/request_times.json') as data_file:
        probe_events_raw = json.load(data_file)
    probe_events_raw_sorted_end = sorted(probe_events_raw, key=lambda e: (e.get('req_snd_time', finfo('d').max)))
    delays = list()
    for request_id, probe_event_raw in enumerate(probe_events_raw_sorted_end):
        resp_recv_time = probe_event_raw.get('resp_rcv_time')
        req_snd_time = probe_event_raw.get('req_snd_time')
        time_passed = resp_recv_time - req_snd_time
        delays.append(dict(ServiceDelay=time_passed, TimeSent=pd.to_datetime(req_snd_time, unit='s')))
    df = pd.DataFrame(delays)
    df.to_pickle("/results/pre_processing_delay_" + str(datetime.now().minute) + ".pkl")
    fig = px.line(df, x='TimeSent', y='ServiceDelay', title='Service delay by request send time')
    return fig
