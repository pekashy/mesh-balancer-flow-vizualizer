import heapq
import json
from collections import deque
from datetime import datetime

import pandas as pd
import plotly.express as px
from numpy import finfo

NUMBER_OF_POINTS = 200


def get_active_request_count_chart():
    with open('/results/request_times.json') as data_file:
        probe_events_raw = json.load(data_file)
    probe_events_raw_sorted_end = deque(sorted(probe_events_raw, key=lambda e: (e.get('req_snd_time', finfo('d').max))))
    start_time = probe_events_raw_sorted_end[0].get('req_snd_time')
    end_time = max(probe_events_raw, key=lambda r: r.get('resp_rcv_time')).get('resp_rcv_time')
    timespan = end_time - start_time
    timedelta = timespan / NUMBER_OF_POINTS
    active_requests_per_instance = {'total': 0}
    pending_request_end_times_per_instance = {"total": []}
    active_requests_chart = []
    for i in range(NUMBER_OF_POINTS):
        currtime = start_time + timedelta * i

        while len(probe_events_raw_sorted_end) > 0:
            event = probe_events_raw_sorted_end.popleft()
            event_snd_time = event.get('req_snd_time')

            if event_snd_time > currtime:
                probe_events_raw_sorted_end.appendleft(event)
                break

            event_resp_rcv_time = event.get('resp_rcv_time')
            active_requests_per_instance['total'] += 1
            heapq.heappush(pending_request_end_times_per_instance['total'], event_resp_rcv_time)
            instance = event.get('instance')

            if instance not in active_requests_per_instance:
                active_requests_per_instance[instance] = 0
                pending_request_end_times_per_instance[instance] = []

            active_requests_per_instance[instance] += 1
            heapq.heappush(pending_request_end_times_per_instance[instance], event_resp_rcv_time)

        for instance in pending_request_end_times_per_instance:
            while len(pending_request_end_times_per_instance[instance]) > 0:
                closest_pending_req_end_time = heapq.heappop(pending_request_end_times_per_instance[instance])

                if closest_pending_req_end_time <= currtime:
                    active_requests_per_instance[instance] -= 1
                else:
                    heapq.heappush(pending_request_end_times_per_instance[instance], closest_pending_req_end_time)
                    break

            active_requests_chart.append(dict(ActiveRequests=active_requests_per_instance[instance],
                                              Time=pd.to_datetime(currtime, unit='s'), instance=instance))

    df = pd.DataFrame(active_requests_chart)
    df.to_pickle("/results/active_requests_count_" + str(datetime.now().minute) + ".pkl")
    fig = px.line(df, x='Time', y='ActiveRequests', title='Active Requests for instance', color='instance')
    return fig
