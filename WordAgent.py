#!/usr/bin/env python3

import os
import tempfile
import difflib
from gi.repository import Gtk

class SignalHandler:
    """Handles signals from user events"""

    def __init__(self, seg_bfr, differ, file_clerk):
        self.seg_bfr = seg_bfr
        self.differ = differ
        self.file_clerk = file_clerk

    def gtk_main_quit(self, *args):
        Gtk.main_quit(*args)

    def on_segmentBuffer_modified_changed(self, widget):
        seq1 = self.seg_bfr.saves[-1]
        seq2 = self.seg_bfr.props.text
        ratio_changed = self.differ.diff_ratio(seq1, seq2)
        if ratio_changed < 1.0:
            self.seg_bfr.save_edit(self.differ)

    def on_undoButton_clicked(self, widget):
        self.seg_bfr.undo_edit()

    def on_redoButton_clicked(self, widget):
        self.seg_bfr.redo_edit()

    def on_saveButton_clicked(self, widget):
        self.seg_bfr.save_edit(self.differ)


class SegmentBuffer(Gtk.TextBuffer):
    """Extends text buffer to include version lists"""
    def __init__(self, segment="Default text"):
        Gtk.TextBuffer.__init__(self)
        self.diffs = []
        self.redos = []
        self.saves = []

        self.segment = segment
        self.set_text(self.segment, len(self.segment))
        self.add_bf(self.saves, self.props.text)

    def add_bf(self, buffer_name, element):
        buffer_name.append(element)

    def pop_bf(self, buffer_name, index= -1):
        return buffer_name.pop(index)

    def save_edit(self, text):
        self.add_bf(self.saves, text)
        self.redos.clear()

    def undo_edit(self):
        self.add_bf(self.saves, self.props.text)
        self.set_text(self.saves[-1], len(self.saves[-1]))

    def redo_edit(self):
        self.add_bf(self.saves, self.props.text)
        self.self.pop_bf(self.redos)


class Differ(difflib.SequenceMatcher):
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
