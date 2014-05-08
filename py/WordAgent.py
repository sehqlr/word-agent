from collections import deque
from difflib import SequenceMatcher
from gi.repository import Gtk, Gdk
import io

welcome_message = """
    Welcome to the Word Agent, the novel project management app!

    Features currently in development:
        Cut/Copy/Paste
        New/Open files
        Dialog boxes

    Next Feature in the works:
        Project management

    Future Features:
        Version Control System integration
        Cloud Collaboration with WebRTC
        "Post Production" formatting (Scribus integration?)
"""

class DialogMaker:
    """Provides static methods to build dialog windows"""

    @staticmethod
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

    @staticmethod
    def open_file_dialog():
        """Launch a File/Open dialog window"""
        dialog = Gtk.FileChooserDialog("Open a project", None,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            project_name = dialog.get_filename()
            dialog.destroy()
        if response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
            dialog.destroy()
        return project_file

    @staticmethod
    def saveas_file_dialog(text):
        """Launch a File/Save dialog window"""
        dialog = Gtk.FileChooserDialog("Save your project", None,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Save clicked")
            project_name = dialog.get_filename()
            dialog.destroy()
        if response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
            dialog.destory()
        return project_file


class SignalHandler:
    """Handles user events and file IO"""
    # TODO: Transistion this class to error handling and logging after v0.2. Each handler should have less than 10 lines of code, except for error checking.
    def __init__(self, segment):
        self.seg = segment
        self.file_is_saved_as = False
        self.msg = "HANDLER: "

        # adding custom signal here
        sig_id = self.seg.buffer.connect("changed", self.buffer_changed)
        self.sig_buffer_changed = sig_id

    def gtk_main_quit(self, *args):
        print(self.msg, "gtk_main_quit")
        Gtk.main_quit(*args)

    def on_buffer_changed(self, widget):
        """Custom signal for Segment.buffer"""
        print(self.msg, "on_buffer_changed")
        self.seg.autosave()

    def on_newButton_clicked(self, widget):
        print(self.msg, "on_newButton_clicked")
        self.seg = Segment()
        self.file_is_saved_as = False

    def on_openButton_clicked(self, widget):
        print(self.msg, "on_openButton_clicked")
        filename = DialogMaker.open_file_dialog()
        content = Segment.read_from_file(filename)
        self.seg = Segment(content)
        self.file_is_saved_as = True

    def on_saveButton_clicked(self, widget):
        print(self.msg, "on_saveButton_clicked")
        if self.file_is_saved_as is not True:
            self.pf = DialogMaker.saveas_file_dialog(self.bfr.curr)
        else:
            self.pf.write(self.bfr.curr)

    def on_saveasButton_clicked(self, widget):
        print(self.msg, "on_saveButton_clicked")
        self.pf = DialogMaker.saveas_file_dialog(self.bfr.curr)
        self.file_is_saved_as = True

    def on_undoButton_clicked(self, widget):
        print(self.msg, "on_undoButton_clicked")
        with self.bfr.handler_block(self.sig_buffer_changed):
            self.seg.undo()

    def on_redoButton_clicked(self, widget):
        print(self.msg, "on_redoButton_clicked")
        with self.bfr.handler_block(self.sig_buffer_changed):
            self.seg.redo()

    def on_cutButton_clicked(self, widget):
        print(self.msg, "on_cutButton_clicked")
        self.seg.cut()

    def on_copyButton_clicked(self, widget):
        print(self.msg, "on_copyButton_clicked")
        self.seg.copy()

    def on_pasteButton_clicked(self, widget):
        print(self.msg, "on_pasteButton_clicked")
        self.seg.paste()

    def on_aboutButton_clicked(self, widget):
        print(self.msg, "on_aboutButton_clicked")
        DialogMaker.about_app_dialog()


class Segment:
    """Organizes a segment, including its buffer, view, file, etc"""
    def __init__(self, filename="untitled.wa" content=welcome_message):
        self._buffer = Gtk.TextBuffer()
        self._buffer.set_text(content)

        self._view = Gtk.TextView.new_with_buffer(self.buffer)

        self._clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self._buffer.add_selection_clipboard(self._clipboard)

        self._filename = filename

        self._matcher = SequenceMatcher()

        # None is a sentinel value. The newline is for setting text.
        self._edits = deque([None, welcome_message])

    @staticmethod
    def read_from_file(filename):
        content = ""
        with open(filename, "r") as textfile:
            for line in textfile:
                content += line

        return content

    @property
    def buffer(self):
        return self._buffer

    @property
    def view(self):
        return self._view

    @property
    def clipboard(self):
        return self._clipboard

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

    @property
    def edits(self):
        return self._edits

    @property
    def curr_text(self):
        return self._buffer.props.text

    @curr_text.setter
    def curr_text(self, value):
        self._buffer.set_text(value, len(value))

    @property
    def prev_edit(self):
        return self._edits[-1]

    # AUTOSAVE METHODS
    def text_comparison(self):
        self.matcher.set_seqs(self.curr_text, self.prev_edit)
        ratio = self.matcher.quick_ratio()
        print("matcher ratio: ", ratio)
        return ratio

    def autosave(self):
        # IDEA: percentage here could be changed in Settings.
        if self.text_comparison() < 0.99:
            self.edits.append(self.curr_text)

        # clears out old edits using sentinel value
        while self.edits[0] is not None:
            self.edits.popleft()

    # UNDO/REDO BUTTON METHODS
    def undo(self):
        self.edits.append(self.curr_text)
        self.edits.rotate(1)
        if self.prev_edit is not None:
            self.edits.rotate(1)
            if self.prev_edit is not None:
                self.curr_text = self.prev_edit

    def redo(self):
        if self.prev_edit is not None:
            self.edits.rotate(-1)
            if self.prev_edit is not None:
                self.curr_text = self.prev_edit
        elif self.edits[0] is None:
            pass

    # CUT/COPY/PASTE BUTTON METHODS
    def cut(self):
        if self.buffer.get_has_selection():
            self.buffer.cut_clipboard(self.clipboard, True)

    def copy(self):
        if self.buffer.get_has_selection():
            self.buffer.copy_clipboard(self.clipboard)

    def paste(self):
        self.buffer.paste_clipboard(self.clipboard, None, True)

    # NEW/OPEN/SAVE BUTTON METHODS
    def write_to_file(self):
        with open(self.file_name, "w") as textfile:
            textfile.write(self.curr_text)

