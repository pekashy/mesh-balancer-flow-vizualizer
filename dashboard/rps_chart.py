import json
from collections import deque
from datetime import datetime

import pandas as pd
import plotly.express as px
from numpy import finfo


def get_rps_chart():
    with open('/results/request_times.json') as data_file:
        probe_events_raw = json.load(data_file)
    probe_events_raw_sorted_end = deque(
        sorted(probe_events_raw, key=lambda e: (e.get('resp_rcv_time', finfo('d').max))))
    start_time = min(probe_events_raw, key=lambda r: r.get('req_snd_time')).get('req_snd_time')
    end_time = probe_events_raw_sorted_end[-1].get('resp_rcv_time')
    timespan = end_time - start_time
    timedelta = timespan / 1000.0
    reqs_finished = 0
    rps_chart = []
    for i in range(1000):
        currtime = start_time + timedelta * i
        while len(probe_events_raw_sorted_end) > 0:
            event = probe_events_raw_sorted_end.popleft()
            event_resp_rcv_time = event.get('resp_rcv_time')

            if event_resp_rcv_time > currtime:
                probe_events_raw_sorted_end.appendleft(event)
                break
            reqs_finished += 1

        rps = 1.0 * reqs_finished / (timedelta * (i + 1))
        rps_chart.append(dict(RPS=rps, Time=pd.to_datetime(currtime, unit='s')))

    df = pd.DataFrame(rps_chart)
    df.to_pickle("/results/pre_processing_delay_" + str(datetime.now().minute) + ".pkl")
    fig = px.line(df, x='Time', y='RPS', title='RPS for time')
    return fig
