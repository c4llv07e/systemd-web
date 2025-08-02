#!/usr/bin/env python3
from flask import request, Flask, render_template, redirect, url_for
import os
import sys
import time
from urllib.parse import urlencode

program_name = "aoeu"
title = "Adventure space server management"

app = Flask(__name__, static_url_path='')

def eprint(*args, **kwargs):
    return print(*args, file=sys.stderr, **kwargs)

def spawn(file, args):
    pid = os.fork()
    if pid == -1:
        eprint("can't fork to execute", file)
        return -1
    if pid == 0:
        os.execvp(file, args)
        # What you even do in failed to exec, but forked app?
        eprint("can't execvp", file)
        os.exit(-1)
    return os.waitpid(pid, 0)[1]

@app.route("/control", methods=["POST"])
def route_control():
    action = request.form.get("action")
    if action is None:
        return redirect("/?" + urlencode(values={"message": "wrong action"}))
    if action == "restart":
        status = spawn("zenity", ["zenity", "--info", "--text", program_name])
        # status = spawn("systemctl", ["systemctl", "restart", program_name])
        if status == 0:
            return redirect("/?" + urlencode({"message": "service restarted"}))
        return redirect("/?" + urlencode({"message": f"error on restarting service, status code: {status}"}))
    return redirect("/?" + urlencode({"message", "unknown action"}))

@app.route("/", methods=["GET"])
def route_root():
    message = request.args.get("message")
    return render_template("index.html", title=title, message=message)

if __name__ == '__main__':
    debug = "DEV_MODE" in os.environ
    app.run(host="0.0.0.0", port="8939", debug=debug)
    pass

