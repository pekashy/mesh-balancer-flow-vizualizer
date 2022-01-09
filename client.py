import sys
from collections import Counter
import json
import time
from typing import Dict, Any
import aiohttp
import asyncio

url, n_requests = sys.argv[1], int(sys.argv[2])

count = Counter()
count_fail = 0
start = time.time()


async def make_request(session) -> Dict[str, Any]:
    req_snd_time = time.time()
    async with session.get(url) as resp:
        resp_rcv_time = time.time()
        data = await resp.json()
        data.update({'req_snd_time': req_snd_time, 'resp_rcv_time': resp_rcv_time})
        return data


async def make_requests():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(n_requests):
            tasks.append(asyncio.ensure_future(make_request(session)))

        return await asyncio.gather(*tasks)


async def main():
    request_times_list = await make_requests()
    with open('results/request_times.json', 'w') as f:
        json.dump(request_times_list, f)

    finish = time.time()
    for k in count:
        print(f"{k}: actual weight {count[k] / n_requests * 100}%")
    print(f"RPS: {n_requests / (finish - start)}")
    print(f"Failed: {count_fail}")


asyncio.run(main())
