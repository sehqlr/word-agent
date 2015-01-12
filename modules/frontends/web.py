#!/usr/bin/env python3
from flask import request, render_template, flash, url_for, redirect

from modules.backend import segment, r_server

class Controller:
    """
    Executes commands received from app
    """

    def view_root_index(self):
        return render_template('index.html', body=segment.curr_edit)

    def api_greeting(self):
        return render_template('api.html',
                                body="Welcome to the API",
                                dispatchers=dispatcher)

    def execute(self, call):
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

class Dispatcher:
    # Dispatch functions
    def __init__(self):
        dispatchers = {
            "file_new": file_new,
            "file_open": file_open,
            "file_save": file_save,
            "edit_undo": edit_undo,
            "edit_redo": edit_redo,
            "edit_add": edit_add,
            }

    def file_new(self, **kwargs):
        print("dispatch file_new")
        if kwargs is not None:
            designation = kwargs.pop("designation")
            content     = kwargs.pop("content")
            return Segment.new(designation=designation, content=content)
        else:
            return Segment.new()

    def file_open(self, **kwargs):
        print("dispatch file_open")
        if kwargs is not None:
            designation = kwargs.pop("designation")
            content     = kwargs.pop("content")
            return Segment.open(designation=designation, content=content)
        else:
            return Segment.open()

    def file_save(self):
        print("dispatch file_save")
        r_server.bgsave()

    def edit_undo(self):
        print("dispatch edit_undo")
        segment.undo()

    def edit_redo(self):
        print("dispatch edit_redo")
        segment.redo()

    def edit_add(self, text):
        print("dispatch edit_add")
        text = str(text)
        segment.add_edit(text)


if __name__ == "__main__":
    print("testing for this module has not been implemented yet")
