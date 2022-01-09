import time

from flask import Flask
import os
import logging
import random
import numpy as np
from flask import jsonify
from datetime import datetime

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
healthy = True
log = logging.getLogger('werkzeug')


@app.route('/')
def hello():
    global healthy
    if healthy:
        return f"Hello from {os.environ['HOST']}!\n"
    else:
        return "Unhealthy", 503


@app.route('/bench_timed')
def bench_timed():
    recv_time = time.time()
    global healthy
    if healthy:
        resp_send_time = time.time()
        return jsonify(instance=os.environ['HOST'], resp_snd_time=resp_send_time, resp_rcv_time=recv_time)
    else:
        return "Unhealthy", 503


@app.route('/bench')
def bench():
    global healthy
    if healthy:
        return f"Bench from {os.environ['HOST']}!\n"
    else:
        return "Unhealthy", 503


@app.route('/bench_slow_random')
def bench_slow_random():
    recv_time = time.time()
    global healthy
    sleep_time_ms = np.random.lognormal(1.5, 1, 1)[0]/1000
    log.warning(sleep_time_ms)
    time.sleep(sleep_time_ms)
    if healthy:
        resp_send_time = time.time()
        return jsonify(instance=os.environ['HOST'], resp_snd_time=resp_send_time, resp_rcv_time=recv_time)
    else:
        return "Unhealthy", 503


@app.route('/healthy')
def healthy():
    global healthy
    healthy = True
    return f"[{os.environ['HOST']}] Set to healthy\n", 201


@app.route('/unhealthy')
def unhealthy():
    global healthy
    healthy = False
    return f"[{os.environ['HOST']}] Set to unhealthy\n", 201


if __name__ == "__main__":
    random.seed(datetime.now())
    formatter = logging.Formatter(fmt="%(asctime)s.%(msecs)03d %(levelname)s %(module)s: %(message)s",
                                  datefmt="%H:%M:%S")
    log.setLevel(logging.WARNING)
    file_handler = logging.FileHandler(f"/logs/{os.environ['HOST']}.log")
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=False)
