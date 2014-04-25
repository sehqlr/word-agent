#!/usr/bin/env python3

import os
import tempfile
import difflib
from gi.repository import Gtk

class SignalHandler:
    """Handles signals from user events"""
    def __init__(self, segment_buffer, differ, file_clerk):
        self.objs = {"buffer": segment_buffer,
                    "differ": differ,
                    "fclerk": file_clerk}

        # adding custom signals here
        self.objs["buffer"].connect("changed", self.on_buffer_changed)

    def gtk_main_quit(self, *args):
        print("SIGNAL: gtk_main_quit")
        Gtk.main_quit(*args)

    def on_buffer_changed(self, widget):
        """Custom signal for SegmentBuffer class"""
        print("SIGNAL: on_buffer_changed")
        bfr = self.objs["buffer"]
        dfr = self.objs["differ"]
        ratio_changed = dfr.diff_ratio(bfr.copy, bfr.undos[-1])
        if ratio_changed < 1.0:
            bfr.save_edit()

    def on_undoButton_clicked(self, widget):
        print("SIGNAL: on_undoButton_clicked")
        self.objs["buffer"].undo_edit()

    def on_redoButton_clicked(self, widget):
        print("SIGNAL: on_redoButton_clicked")
        self.objs["buffer"].redo_edit()


class SegmentBuffer(Gtk.TextBuffer):
    """Extends text buffer to include version lists"""
    def __init__(self, segment="Default text"):
        Gtk.TextBuffer.__init__(self)

        # TODO: explain why using empty string in list instead of just empty list
        self.undos = [""]
        self.redos = [""]

        self.set_text(segment, len(segment))

        self.copy = self.props.text

    def add_bf(self, buffer_name, element):
        buffer_name.append(element)

    def pop_bf(self, buffer_name, index= -1):
        return buffer_name.pop(index)

    # makes a copy of the text content
    def copy_text(self):
        self.copy = self.props.text

    def save_edit(self):
        self.copy_text()
        self.redos.clear()

    def undo_edit(self):
        self.add_bf(self.redos, self.copy)
        undo = self.pop_bf(self.undos)
        self.set_text(undo, len(undo))

    def redo_edit(self):
        self.add_bf(self.undos, self.copy)
        redo = self.pop_bf(self.redos)
        self.set_text(redo, len(redo))


class SequenceDiffer(difflib.SequenceMatcher):
    """Generates deltas and compares strings with difflib"""
    def __init__(self):
        difflib.SequenceMatcher.__init__(self)
        self.ndiff = difflib.ndiff
        self.restore = difflib.restore

    def restore_diff(self, diff, which):
        return ''.join(self.restore(diff, which))

    def diff_ratio(self, seq1, seq2):
        self.set_seqs(seq1, seq2)
        return self.quick_ratio()


class FileClerk:
    """The class for saving files"""
    pass
