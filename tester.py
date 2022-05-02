import asyncio
import json
import random
import sys
import time
from typing import Dict, Any, List

import aiohttp

n_requests = int(sys.argv[1])
urls10 = ["http://0.0.0.0:30000/bench10"]*int(n_requests/3)
urls50 = ["http://0.0.0.0:30000/bench50"]*int(n_requests/3)
urls500 = ["http://0.0.0.0:30000/bench500"]*int(n_requests/3)

urls = list()
urls.extend(urls10)
urls.extend(urls50)
urls.extend(urls500)
random.shuffle(urls)
start = time.time()


async def make_request(session, url) -> Dict[str, Any]:
    req_snd_time = time.time()
    async with session.get(url) as resp:
        data = await resp.json()
        resp_rcv_time = time.time()
        data.update({'req_snd_time': req_snd_time, 'resp_rcv_time': resp_rcv_time})
        return data


async def make_requests():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(make_request(session, url)))

        return await asyncio.gather(*tasks)


async def main():
    request_times_list = await make_requests()
    with open('results/request_times.json', 'w') as f:
        json.dump(request_times_list, f)

    finish = time.time()
    print(f"RPS: {n_requests / (finish - start)}")


asyncio.run(main())
