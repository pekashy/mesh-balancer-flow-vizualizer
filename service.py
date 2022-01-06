from flask import Flask
import os
import logging

app = Flask(__name__)
healthy = True
log = logging.getLogger('werkzeug')


@app.route('/')
def hello():
    global healthy
    if healthy:
        return f"Hello from {os.environ['HOST']}!\n"
    else:
        return "Unhealthy", 503


@app.route('/bench')
def bench():
    global healthy
    log.warning('Hello World!')
    if healthy:
        return f"Bench from {os.environ['HOST']}!\n"
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
    formatter = logging.Formatter(fmt="%(asctime)s.%(msecs)03d %(levelname)s %(module)s: %(message)s",
                                  datefmt="%H:%M:%S")
    log.setLevel(logging.WARNING)
    file_handler = logging.FileHandler(f"/logs/{os.environ['HOST']}.log")
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)
    app.run(host='0.0.0.0', port=8000, debug=False)
