#!/usr/bin/env python3

import os
import tempfile
import difflib
from gi.repository import Gtk

class Handler:
    """Handles signals from user events"""

    def __init__(self, seg_buffer, differ, file_clerk):
        self.seg_buffer = seg_buffer
        self.differ = differ
        self.file_clerk = file_clerk

    def gtk_main_quit(self, *args):
        Gtk.main_quit(*args)

    def on_segmentBuffer_modified_changed(self, widget):
        self.seg_buffer.save_edit(self.differ)

    def on_undoButton_clicked(self, widget):
        self.seg_buffer.undo_edit()

    def on_redoButton_clicked(self, widget):
        self.seg_buffer.redo_edit()

    def on_saveButton_clicked(self, widget):
        self.seg_buffer.save_edit(self.differ)


class SegmentBuffer(Gtk.TextBuffer):
    """Extends text buffer to include version lists"""
    def __init__(self, segment="Default text"):
        Gtk.TextBuffer.__init__(self)
        self.diffs = []
        self.redos = []
        self.saves = []
        self.segment = segment

        self.text = self.set_text(self.segment, len(self.segment))
        self.add_bf(self.saves, self.text)

    def add_bf(self, buffer, element):
        buffer.append(element)

    def pop_bf(self, buffer, index= -1):
        return buffer.pop(index)

    def get_diff(self, differ, str1, str2):
        return differ.ndiff(str1, str2)

    def save_edit(self, differ):
        """Handles the AutoSave Feature"""
        self.add_bf(self.saves, self.text)
        if len(self.saves) >= 2:
            differ.set_seqs(self.text, self.saves[-1])
            ratio = differ.quick_ratio()
            if ratio is not 1.0:
                self.add_bf(saves, self.text)
                self.redos.clear()

    def undo_edit(self):
        self.add_bf(self.saves, self.text)
        self.text = self.saves[-1]

    def redo_edit(self):
        self.add_bf(self.saves, self.text)
        self.text = self.pop_bf(self.redos)


class Differ(difflib.SequenceMatcher):
    """Generates deltas and compares strings with difflib"""
    def __init__(self):
        difflib.SequenceMatcher.__init__(self)
        self.ndiff = difflib.ndiff
        self.restore = difflib.restore

    def restore_diff(self, diff, which):
        return ''.join(self.restore(diff, which))


class FileClerk:
    """The class for saving files"""
    pass
