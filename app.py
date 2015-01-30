#!/usr/bin/env python3
from flask import Flask, request, render_template, flash, url_for, redirect
import sys

from backend import Segment

app = Flask(__name__)
app.secret_key = "something secret"


def get_segment():
    seg_id = Segment.get_current()
    return Segment.open(seg_id)

@app.route("/", methods=["GET", "POST"])
def index():
    seg = get_segment()
    return render_template('index.html',
                            filename=seg.filename,
                            body="Welcome to the index page")

@app.route("/editor", methods=["GET", "POST"])
def editor():
    seg = get_segment()
    return render_template('editor.html',
                            filename=seg.filename,
                            text=seg.curr_edit)

@app.route("/api", methods=["GET", "POST"])
def api():
    seg = seg_segment()
    return render_template('api.html',
                            body="Welcome to the API",
                            filename=seg.filename)

@app.route("/api/open", methods=["GET"])
def open():
    seg_id = request.args.get("seg_id")
    if seg_id:
        Segment.open(seg_id)
        flash("opened file " + Segment.get_current())
    else:
        flash("could not open file")
    return redirect(url_for('editor'))

@app.route("/api/save", methods=["POST"])
def save():
    Segment.save()
    flash("saved")
    return redirect(url_for('editor'))

@app.route("/api/undo", methods=["POST"])
def undo():
    segment = get_segment()
    result = segment.undo()
    flash("undid: " + str(result))
    return redirect(url_for('editor'))

@app.route("/api/redo", methods=["POST"])
def redo():
    segment = get_segment()
    result = segment.redo()
    flash("redid: " + str(result))
    return redirect(url_for('editor'))

@app.route("/api/add_edit", methods=["POST"])
def add_edit():
    segment = get_segment()
    text = request.form.get("text")
    result = segment.add_edit(text)
    flash("added the edit: " + str(result))
    return redirect(url_for('editor'))

if __name__ == "__main__":
    Segment.r_server.flushdb()
    app.debug = True
    app.run()
