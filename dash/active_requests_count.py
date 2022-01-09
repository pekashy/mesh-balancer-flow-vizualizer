from collections import deque

import plotly.express as px
import pandas as pd
import json
from numpy import finfo
import heapq


def get_active_request_count_chart():
    with open('/results/request_times.json') as data_file:
        probe_events_raw = json.load(data_file)
    probe_events_raw_sorted_end = deque(sorted(probe_events_raw, key=lambda e: (e.get('req_snd_time', finfo('d').max))))
    start_time = probe_events_raw_sorted_end[0].get('req_snd_time')
    end_time = max(probe_events_raw, key=lambda r: r.get('resp_rcv_time')).get('resp_rcv_time')
    timespan = end_time - start_time
    timedelta = timespan / 1000.0
    active_requests = 0
    pending_request_end_times = []
    active_requests_chart = []
    for i in range(1000):
        currtime = start_time + timedelta*i

        while len(probe_events_raw_sorted_end) > 0:
            event = probe_events_raw_sorted_end.popleft()
            event_snd_time = event.get('req_snd_time')
            if event_snd_time > currtime:
                probe_events_raw_sorted_end.appendleft(event)
                break

            event_resp_rcv_time = event.get('resp_rcv_time')
            active_requests += 1
            heapq.heappush(pending_request_end_times, event_resp_rcv_time)

        while len(pending_request_end_times) > 0:
            closest_pending_req_end_time = heapq.heappop(pending_request_end_times)
            if closest_pending_req_end_time <= currtime:
                active_requests -= 1
            else:
                heapq.heappush(pending_request_end_times, closest_pending_req_end_time)
                break

        active_requests_chart.append(dict(ActiveRequests=active_requests, Time=pd.to_datetime(currtime, unit='s')))

    df = pd.DataFrame(active_requests_chart)
    fig = px.line(df, x='Time', y='ActiveRequests', title='Active Requests for time')
    return fig
