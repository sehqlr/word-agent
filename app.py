#!/usr/bin/env python3
from flask import Flask, request, render_template, flash, url_for, redirect
import sys

from backend import Segment

app = Flask(__name__)
app.secret_key = "something secret"

Segment.r_server.flushdb()
segment = Segment.new()

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html',
                            filename=Segment.r_server.get("curr_seg"),
                            body="Welcome to the index page")

@app.route("/editor", methods=["GET", "POST"])
def editor():
    return render_template('editor.html',
                            filename=Segment.r_server.get("curr_seg"),
                            text=segment.curr_edit)

@app.route("/api", methods=["GET", "POST"])
def api():
    return render_template('api.html',
                            body="Welcome to the API",
                            filename=Segment.r_server.get("curr_seg"))

@app.route("/api/open", methods=["GET"])
def open():
    if request.args.get("file_id"):
        file_id = request.args.get("file_id")
        segment = Segment.open(file_id=file_id)
    else:
        segment = Segment.new()
    flash("opened file " + str(Segment.current.file_id))
    return redirect(url_for('editor'))

@app.route("/api/save", methods=["POST"])
def save():
    Segment.r_server.bgsave()
    flash("saved")
    return redirect(url_for('editor'))

@app.route("/api/undo", methods=["POST"])
def undo():
    result = segment.undo()
    flash("undid: " + str(result))
    return redirect(url_for('editor'))

@app.route("/api/redo", methods=["POST"])
def redo():
    result = segment.redo()
    flash("redid: " + str(result))
    return redirect(url_for('editor'))

@app.route("/api/add_edit", methods=["POST"])
def add_edit():
    text = request.form.get("text")
    result = segment.add_edit(text)
    flash("added the edit: " + str(result))
    return redirect(url_for('editor'))

if __name__ == "__main__":
    app.debug = True
    app.run()
