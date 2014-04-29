#!/usr/bin/env python3

import io
import tempfile
from collections import deque
from difflib import SequenceMatcher, ndiff, restore
from gi.repository import Gtk, Gdk

class SignalHandler:
    """Handles user events and file IO"""
    def __init__(self, segment_buffer, project_name):
        self.bfr = segment_buffer
        self.pf = open(project_name, "w+")

        self.src_path = "/home/sam/Development/word-agent"
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
        tempfile.NamedTemporaryFile

    def on_openButton_clicked(self, widget):
        print(self.msg, "on_openButton_clicked")
        bob = Gtk.Builder.new()
        bob.add_from_file(self.src_path + "/ui/OpenFileDialog.glade")
        win = bob.get_object("OpenFileChooserDialog")
        win.show()

    def on_saveButton_clicked(self, widget):
        print(self.msg, "on_saveButton_clicked")
        text = self.bfr.curr
        self.pf.write(text)

    def on_saveasButton_clicked(self, widget):
        print(self.msg, "on_saveButton_clicked")
        bob = Gtk.Builder.new()
        bob.add_from_file(self.src_path + "/ui/SaveFileDialog.glade")
        win = bob.get_object("SaveFileChooserDialog")
        win.show()

    def on_undoButton_clicked(self, widget):
        print(self.msg, "on_undoButton_clicked")
        with self.bfr.handler_block(self.id_chngd):
            self.bfr.undo_edit()

    def on_redoButton_clicked(self, widget):
        print(self.msg, "on_redoButton_clicked")
        with self.bfr.handler_block(self.id_chngd):
            self.bfr.redo_edit()

    def on_cutButton_clicked(self, widget):
        print(self.msg, "on_cutButton_clicked")

    def on_copyButton_clicked(self, widget):
        print(self.msg, "on_copyButton_clicked")

    def on_pasteButton_clicked(self, widget):
        print(self.msg, "on_pasteButton_clicked")

    def on_aboutButton_clicked(self, widget):
        print(self.msg, "on_aboutButton_clicked")

    def on_CancelOpenButton_clicked(self, widget):
        print(self.msg, "on_CancelOpenButton_clicked")

    def on_AcceptOpenButton_clicked(self, widget):
        print(self.msg, "on_AcceptOpenButton_clicked")

    def on_CancelSaveButton_clicked(self, widget):
        print(self.msg, "on_CancelSaveButton_clicked")

    def on_AcceptSaveButton_clicked(self, widget):
        print(self.msg, "on_AcceptSaveButton_clicked")


class SegmentBuffer(Gtk.TextBuffer):
    """Extended with undo/redo, clipboard, and sequence matcher"""
    def __init__(self, segment="Default text"):
        Gtk.TextBuffer.__init__(self)

        # None is a sentinel value. The newline is for setting text.
        self.edits = deque([None, segment + '\n'])

        self.set_text(segment)
        self.prev = segment
        self.curr = segment

        self.matcher = SequenceMatcher()
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)


    # AUTOSAVE METHODS
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


    # UNDO BUTTON ACTIONS
    def undo_edit(self):
        if self.edits[-1] is not None:
            self.edits.rotate(1)
            undo = self.edits[-1]
            if undo is not None:
                self.set_text(undo)


    # REDO BUTTON ACTIONS
    def redo_edit(self):
        if self.edits[0] is not None:
            self.edits.rotate(-1)
            redo = self.edits[-1]
            if redo is not None:
                self.set_text(redo)
        else:
            self.set_text(self.curr)

    # CUT BUTTON ACTIONS

    # COPY BUTTON ACTIONS

    # PASTE BUTTON ACTIONS
