#!/usr/bin/env python3
import subprocess
from flask import request, Flask, render_template, redirect, url_for
import os
import sys
import time
from urllib.parse import urlencode

def eprint(*args, **kwargs):
    return print(*args, file=sys.stderr, **kwargs)

def get_env_or_exit(env):
    if env not in os.environ:
        eprint(f"Error, {env} is unset")
        sys.exit(-1)
    return os.environ[env]

program_name = get_env_or_exit("SERVICE_NAME")
title = os.getenv("TITLE", "Service monitoring")
host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "8939")
subpath = os.getenv("SUBPATH", "/")
subpath = subpath if subpath[0] == "/" else "/" + subpath
print(subpath)

app = Flask(__name__, static_url_path='')

@app.route(subpath, methods=["POST"])
def route_control():
    action = request.form.get("action")
    if action is None:
        return redirect(subpath + "?" + urlencode(values={"message": "wrong action"}))
    if action == "restart":
        try:
            process = subprocess.run(["systemctl", "restart", program_name])
            status = process.returncode
            if status == 0:
                return redirect(subpath + "?" + urlencode({"message": "service restarted"}))
        except FileNotFoundError:
            eprint("can't run systemctl")
            status = -1
        return redirect(subpath + "?" + urlencode({"message": f"error on restarting service, status code: {status}"}))
    return redirect(subpath + "?" + urlencode({"message", "unknown action"}))

@app.route(subpath, methods=["GET"])
def route_root():
    message = request.args.get("message")
    return render_template("index.html", title=title, message=message)

if __name__ == '__main__':
    debug = "DEV_MODE" in os.environ
    app.run(host=host, port=port, debug=debug)
    pass

