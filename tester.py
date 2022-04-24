import sys
import json
import time
from typing import Dict, Any
import aiohttp
import asyncio

n_requests = int(sys.argv[1])
urls = ["http://0.0.0.0:30000/bench15", "http://0.0.0.0:30000/bench150", "http://0.0.0.0:30000/bench600"]
start = time.time()


async def make_request(session) -> Dict[str, Any]:
    req_snd_time = time.time()
    for url in urls:
        async with session.get(url) as resp:
            data = await resp.json()
            resp_rcv_time = time.time()
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
    print(f"RPS: {n_requests / (finish - start)}")


asyncio.run(main())
