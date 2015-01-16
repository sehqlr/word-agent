#!/usr/bin/env python3
from flask import Flask, request, render_template, flash, url_for, redirect
import sys

from backend import Segment, segment, r_server

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return render_template('index.html',
                            filename=segment.designation,
                            body="Welcome to the index page")

@app.route("/editor")
def editor():
    return render_template('editor.html',
                            filename=segment.designation,
                            text=segment.curr_edit)

@app.route("/api")
def api():
    return render_template('api.html',
                            body="Welcome to the API",
                            dispatchers=dispatcher)

@app.route("/api/open")
def open():
    if request.method == "GET":
        designation = request.args.get("designation")
        return Segment.open(designation=designation)
    else:
        return Segment.new()
    flash("opened")

@app.route("/api/save")
def save():
    r_server.bgsave()
    flash("saved")

@app.route("/api/undo")
def undo():
    segment.undo()
    flash("undid")

@app.route("/api/redo")
def redo():
    segment.redo()
    flash("redid")

@app.route("/api/add_edit")
def add_edit():
    if request.method == "POST":
        text = request.form.get("text")
        segment.add_edit(text)
        flash("added the edit")


if __name__ == "__main__":
    app.run()
else:
    print("testing for this module has not been implemented yet")
