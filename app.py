#!/usr/bin/env python3
from flask import Flask, request, render_template, flash, url_for, redirect
import redis

from modules.backend import Segment
from modules.dispatch import dispatchers

app = Flask(__name__)
app.secret_key = "some secret"

r_server = redis.Redis(db=10)
segment = Segment.new(designation="113", content="Hello World")

@app.route("/")
def index():
    return render_template('index.html', body=segment.curr_edit)

@app.route("/api/")
def api_greeting():
    return render_template('api.html', body="Welcome to the API")

@app.route("/api/<call>", methods=['GET', 'POST'])
def execute(call):
    try:
        if request.method == "GET" and call in dispatch:
            return dispatch[call](request.args)
        elif request.method == "POST" and call in dispatch:
            return dispatch[call](request.form)
        else:
            flash("Command/method not recognized")
    except:
        flash("An error occured")

    return redirect("/api/")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
