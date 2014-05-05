from collections import deque
from difflib import SequenceMatcher, ndiff, restore
from gi.repository import Gtk, Gdk
import io
import tempfile

# FIXME: there should be WordAgent.functions that encode much of what SignalHandler does now.

# DIALOG METHODS

def about_app_dialog():
    """Launch an About dialog window"""
    dialog = Gtk.AboutDialog.new()
    dialog.set_program_name("Word Agent")
    dialog.set_authors(["Sam Hatfield", None])
    dialog.set_version("0.1")
    dialog.set_website("https://github.com/sehqlr/word-agent")
    dialog.set_website_label("Fork us on GitHub!")
    dialog.set_comments("A minimal text editor with a big future.")
    response = dialog.run()
    if response:
        print("About closed")
        dialog.destroy()

def open_file_dialog(file_database):
    """Launch a File/Open dialog window"""
    dialog = Gtk.FileChooserDialog("Open a project", None,
        Gtk.FileChooserAction.OPEN,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
         Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        print("Open clicked")
        file_database.add_file(dialog.get_filename())
        dialog.destroy()
    if response == Gtk.ResponseType.CANCEL:
        print("Cancel clicked")
        dialog.destroy()

def save_file_dialog(file_database, segment_buffer):
    """Launch a File/Save dialog window"""
    dialog = Gtk.FileChooserDialog("Save your project", None,
        Gtk.FileChooserAction.SAVE,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
         Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        print("Save clicked")
        file_database.add_file(dialog.get_filename())
        file_database.save_curr(segment_buffer)
        dialog.destroy()
    if response == Gtk.ResponseType.CANCEL:
        print("Cancel clicked")
        dialog.destory()


class SignalHandler:
    """Handles user events and file IO"""
    # FIXME: It would be better to have this class focus on error checking and logging.
    def __init__(self, segment_buffer, file_database):
        self.bfr = segment_buffer
        self.fdb = file_database
        self.msg = "HANDLER: "

        # adding custom signals here
        self.id_chngd = self.bfr.connect("changed", self.buffer_changed)

    def gtk_main_quit(self, *args):
        print(self.msg, "gtk_main_quit")
        self.fdb.close_project_files()
        Gtk.main_quit(*args)

    def buffer_changed(self, widget):
        """Custom signal for SegmentBuffer class"""
        print(self.msg, "buffer_changed")
        self.bfr.save_edit()

    def on_newButton_clicked(self, widget):
        print(self.msg, "on_newButton_clicked")
        self.fdb.add_file("untitled")

    def on_openButton_clicked(self, widget):
        print(self.msg, "on_openButton_clicked")
        open_file_dialog(self.fdb)

    def on_saveButton_clicked(self, widget):
        print(self.msg, "on_saveButton_clicked")
        if self.fdb.curr_file is None:
            save_file_dialog(self.fdb, self.bfr)
        self.fdb.save_curr(self.bfr)

    def on_saveasButton_clicked(self, widget):
        print(self.msg, "on_saveButton_clicked")
        save_file_dialog(self.fdb, self.bfr)

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
        cut_to_clipboard(self.bfr)

    def on_copyButton_clicked(self, widget):
        print(self.msg, "on_copyButton_clicked")
        copy_to_clipboard()

    def on_pasteButton_clicked(self, widget):
        print(self.msg, "on_pasteButton_clicked")
        paste_from_clipboard()

    def on_aboutButton_clicked(self, widget):
        print(self.msg, "on_aboutButton_clicked")
        about_app_dialog()

class SegmentBuffer(Gtk.TextBuffer):
    """With autosave, undo/redo, cut/copy/paste, sequence matcher"""
    def __init__(self, segment="Default text"):
        Gtk.TextBuffer.__init__(self)

        # None is a sentinel value. The newline is for setting text.
        self.edits = deque([None, segment + '\n'])

        self.set_text(segment)
        self.prev = segment
        self.curr = segment

        self.matcher = SequenceMatcher()
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.add_selection_clipboard(self.clipboard)


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

    # UNDO/REDO BUTTON ACTIONS
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

    # CUT/COPY/PASTE BUTTON ACTIONS
    def cut_to_clipboard(self):
        if self.get_has_selection():
            self.cut_clipboard(self.clipboard, True)

    def copy_to_clipboard(self):
        if self.get_has_selection():
            self.copy_clipboard(self.clipboard)

    def paste_from_clipboard(self):
        self.paste_clipboard(self.clipboard, None, True)

class FileDatabase:
    """Handles file I/O and organizes segments and projects"""
    def __init__(self):
        self.file_suffix = ".wa.txt"
        self.open_files = []
        self._curr_file = None

    @property
    def curr_file(self):
        return self._curr_file

    @curr_file.setter
    def curr_file(self, value):
        self._curr_file = value

    def add_file(self, name):
        name = str(name) + self.file_suffix
        addf = open(name, "w")
        self.open_files.append(addf)
        return addf

    def fetch_file(self, index= -1):
        self.curr_file = self.open_files[index]

    # NEW/OPEN/SAVE METHODS

    def save_curr(self, segment_buffer):
        if self.curr_file is None:
            newf = self.add_file("untitled")
            self.curr_file = newf
        self.curr_file.write(segment_buffer.curr)

    def close_project_files(self):
        for f in self.open_files:
            try:
                f.close()
            except AttributeError:
                print(f, "is not a file object.")
