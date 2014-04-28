#!/usr/bin/env python3

import io
from collections import deque
from difflib import SequenceMatcher, ndiff, restore
from gi.repository import Gtk, Gdk

class SignalHandler:
    """Handles signals from user events"""
    def __init__(self, segment_buffer, project_name):
        self.bfr = segment_buffer
        self.cpbd = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.pf = open(project_name, "w+")

        self.msg = "HANDLER: "

        # adding custom signals here
        self.id_chngd = self.bfr.connect("changed", self.buffer_changed)

    def gtk_main_quit(self, *args):
        print(self.msg, "gtk_main_quit")
        self.pf.close()
        Gtk.main_quit(*args)

    def buffer_changed(self, widget):
        """Custom signal for SegmentBuffer class"""
        print(self.msg, "buffer_changed")
        self.bfr.save_edit()

    def on_newButton_clicked(self, widget):
        print(self.msg, "on_newButton_clicked")


    def on_undoButton_clicked(self, widget):
        print(self.msg, "on_undoButton_clicked")
        with self.bfr.handler_block(self.id_chngd):
            self.bfr.undo_edit()

    def on_redoButton_clicked(self, widget):
        print(self.msg, "on_redoButton_clicked")
        with self.bfr.handler_block(self.id_chngd):
            self.bfr.redo_edit()

    def on_saveButton_clicked(self, widget):
        print(self.msg, "on_saveButton_clicked")
        text = self.bfr.curr
        self.pf.write(text)


class SegmentBuffer(Gtk.TextBuffer):
    """Extends text buffer to include version lists"""
    def __init__(self, segment="Default text"):
        Gtk.TextBuffer.__init__(self)

        # None is a sentinel value. The newline is for setting text.
        self.edits = deque([None, segment + '\n'])

        self.set_text(segment)
        self.prev = segment
        self.curr = segment

        self.matcher = SequenceMatcher()

    def text_comparison(self):
        self.matcher.set_seqs(self.curr, self.prev)
        ratio = self.matcher.quick_ratio()
        print("matcher ratio: ", ratio)
        return ratio

    def text_updates(self):
        self.curr = self.props.text
        if self.text_comparison() < 0.99:
            self.prev = self.curr

    def clear_old_edits(self):
        """clears out the previous edits if any"""
        while self.edits[0] is not None:
            self.edits.popleft()

    def save_edit(self):
        self.text_updates()
        self.edits.append(self.prev)
        self.clear_old_edits()

    def undo_edit(self):
        if self.edits[-1] is not None:
            self.edits.rotate(1)
            undo = self.edits[-1]
            if undo is not None:
                self.set_text(undo)

    def redo_edit(self):
        if self.edits[0] is not None:
            self.edits.rotate(-1)
            redo = self.edits[-1]
            if redo is not None:
                self.set_text(redo)
        else:
            self.set_text(self.curr)


class WindowBuilder(Gtk.Builder):
