#!/usr/bin/env python3
from flask import Flask, request, render_template, flash, url_for, redirect
import redis

from modules.backend import dispatcher, Segment, r_server

app = Flask(__name__)
app.secret_key = "some secret"

print("Redis ping: ", r_server.ping())
segment = Segment.new(designation="113", content="Hello World")


@app.route("/")
def index():
    return render_template('index.html', body=segment.curr_edit)

@app.route("/api/")
def api_greeting():
    return render_template('api.html',
                            body="Welcome to the API",
                            dispatchers=dispatcher)

@app.route("/api/<call>", methods=['GET', 'POST'])
def execute(call):
    try:
        if request.method == "GET" and call in dispatcher:
            return dispatch[call](request.args)
        elif request.method == "POST" and call in dispatcher:
            return dispatch[call](request.form)
        else:
            flash("Command/method not recognized")
    except Exception as e:
        flash("An error occured: ", str(e))

    return redirect("/api/")

if __name__ == "__main__":
    app.run(debug=True)
