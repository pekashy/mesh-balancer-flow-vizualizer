import plotly.express as px
import pandas as pd
import json
from numpy import finfo


def get_pre_processing_delay_chart():
    with open('/results/request_times.json') as data_file:
        probe_events_raw = json.load(data_file)
    probe_events_raw_sorted_end = sorted(probe_events_raw, key=lambda e: (e.get('req_snd_time', finfo('d').max)))
    delays = list()
    for request_id, probe_event_raw in enumerate(probe_events_raw_sorted_end):
        req_snd_time = probe_event_raw.get('req_snd_time')
        processing_started_time = probe_event_raw.get('req_rcv_time')
        proc_delay = processing_started_time - req_snd_time
        delays.append(dict(PreProcessingDelay=proc_delay, TimeSent=pd.to_datetime(req_snd_time, unit='s')))
    df = pd.DataFrame(delays)
    fig = px.line(df, x='TimeSent', y='PreProcessingDelay', title='Delay before processing by request send time')
    return fig
