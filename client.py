import sys
import urllib.request
from collections import Counter
import json
import time

url, n_requests = sys.argv[1], int(sys.argv[2])

count = Counter()
count_fail = 0
start = time.time()

request_times_list = list()

for i in range(n_requests):
    try:
        req_snd_time = time.time()
        with urllib.request.urlopen(url) as resp:
            resp_rcv_time = time.time()
            instance, req_rcv_time, resp_snd_time = resp.read().decode("utf-8").strip().split(',')
            print(f"Request send time: {req_snd_time}; Request recv time: {req_rcv_time}; \
            Response send time: {resp_snd_time}, Response received time: {resp_rcv_time}")
            request_times_list.append({'instance': instance, 'req_snd_time': req_snd_time,
                                       'req_rcv_time': req_rcv_time, 'resp_snd_time': resp_snd_time,
                                       'resp_rcv_time': resp_rcv_time})
            count[instance] += 1
    except:
        count_fail += 1

with open('results/request_times.json', 'w') as f:
    json.dump(request_times_list, f)

finish = time.time()
for k in count:
    print(f"{k}: actual weight {count[k] / n_requests * 100}%")
print(f"RPS: {n_requests / (finish - start)}")
print(f"Failed: {count_fail}")
