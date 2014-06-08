#! /usr/bin/env python3

from collections import deque
from difflib import SequenceMatcher
from gi.repository import Gtk, Gdk
import io

# TODO: keep welcome message updated!
welcome_message = """
Welcome to the Word Agent, the novel project management app!

Keyboard shortcuts are listed in the Help message (Press F1).

If you have any questions, concerns, or comments, please create an \
issue on our GitHub page or email me with the details.
"""

# UTILITY FUNCTIONS


def read_from_file(filename):
    """
    Opens, reads, and returns the text contents of filename
    """
    content = ""
    if filename:
        with open(filename, "r") as textfile:
            for line in textfile:
                content += line
    return content

def write_to_file(filename, content):
    """
    Writes content to filename on disk
    """
    if filename:
        with open(filename, "w") as f:
            f.write(content)

# CLASS DEFINITIONS

class Segment:
    """
    Model for Word Agent. Encapsulates a segment
    """
    def __init__(self, filename, content):

        # creates TextBuffer and Clipboard
        self._buffer = Gtk.TextBuffer()
        self._buffer.set_text(content)

        self._clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self._buffer.add_selection_clipboard(self._clipboard)

        # instead of a file object, we keep/update the name only
        self._filename = filename

        # matcher limits number of autosave operations
        # see text_comparison and autosave methods for more details
        self._matcher = SequenceMatcher()

        # edits is the double ended queue (deque) for autosave feature
        self._edits = deque([None, content])

        # connecting custom signal
        self.sig_id = self._buffer.connect("changed", self.autosave)

    @staticmethod
    def new(filename="untitled", content=welcome_message):
        new = Segment(filename, content)
        return new

    # properties, listed alphabetically
    @property
    def base_edit(self):
        return self._edits[0]

    @property
    def buffer(self):
        return self._buffer

    @property
    def clipboard(self):
        return self._clipboard

    @property
    def curr_text(self):
        return self._buffer.props.text

    @curr_text.setter
    def curr_text(self, value):
        self._buffer.set_text(value, len(value))

    @property
    def edits(self):
        return self._edits

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

    @property
    def matcher(self):
        return self._matcher

    @property
    def prev_edit(self):
        return self._edits[-1]

    # AUTOSAVE METHOD
    def autosave(self, widget):
        """
        If enough changes have been made, add text to edits deque
        """
        # IDEA: percentage here could be changed in Settings.
        if self.prev_edit is None:
            self.edits.append("")
        self.matcher.set_seqs(self.curr_text, self.prev_edit)
        ratio = self.matcher.quick_ratio()
        if ratio < 0.99:
            print("Text autosaved")
            self.edits.append(self.curr_text)

        # clears out old edits using sentinel value
        while self.base_edit is not None:
            self.edits.popleft()

    # UNDO/REDO METHODS
    def undo(self):
        """
        Reverts TextBuffer to earlier state, from the edits deque
        """
        with self.buffer.handler_block(self.sig_id):
            # because autosave is not the most current edit
            if self.base_edit is None:
                self.edits.append(self.curr_text)

            # rotate the most recent addition to the back of the deque
            self.edits.rotate(1)

            # if prev_edit is None, we've rotated all the way around
            if self.prev_edit:
                self.curr_text = self.prev_edit
            else:
                print("Nothing to undo")

    def redo(self):
        """
        Reverts TextBuffer to later state, if it still exists
        """
        with self.buffer.handler_block(self.sig_id):
            # if base_edit is None, we've rotated all the way back
            if self.base_edit:
                self.edits.rotate(-1)
                self.curr_text = self.prev_edit
            else:
                print("Nothing to redo")

    # CUT/COPY/PASTE BUTTON METHODS
    def cut(self):
        """
        Basic edit/cut function
        """
        if self.buffer.get_has_selection():
            self.buffer.cut_clipboard(self.clipboard, True)

    def copy(self):
        """
        Basic edit/copy function
        """
        if self.buffer.get_has_selection():
            self.buffer.copy_clipboard(self.clipboard)

    def paste(self):
        """
        Basic edit/paste function
        """
        self.buffer.paste_clipboard(self.clipboard, None, True)


class EditorWindow(Gtk.Window):
    """
    View for word-agent. Hardcodes UI definitions
    """
    def __init__(self):
        # basic init stuff for window
        Gtk.Window.__init__(self, title="Word Agent")
        self.connect("destroy", Gtk.main_quit)
        self.set_default_size(600, 600)

        # create the Box container 
        self.box = Gtk.Box.new(1 , 3)
        self.add(self.box)

        # button_dict keeps a list of button objects, and their handlers
        self.buttons = {}
        self.create_toolbar()

        # boolean to keep track of fullscreen
        self.is_fullscreen = False

        # scrolled window to contain TextView
        self.scroll = Gtk.ScrolledWindow.new(None, None)
        self.box.pack_start(self.scroll, True, True, 0)

        # TextView's wrap mode won't split words
        self.view = Gtk.TextView.new()
        self.view.set_wrap_mode(2)
        self.scroll.add(self.view)

    # DIALOG METHODS
    def dialog_about(self):
        """
        Launch an About dialog window
        """

        # build an about dialog
        dialog = Gtk.AboutDialog.new()
        dialog.set_program_name("Word Agent")
        dialog.set_authors(["Sam Hatfield", None])
        dialog.set_version("0.2.3-dev")
        dialog.set_website("https://github.com/sehqlr/word-agent")
        dialog.set_website_label("Fork us on GitHub!")
        dialog.set_comments("A simple text editor with a big future.")
        dialog.set_copyright("Copyright 2014 and onward by Sam Hatfield")

        # wait until user closes dialog
        response = dialog.run()
        if response:
            dialog.destroy()

    def dialog_file_open(self):
        """
        Launch a File/Open dialog window
        """
        dialog = Gtk.FileChooserDialog("Open a project", None,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        # plaintext filter
        filter_text = Gtk.FileFilter.new()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")

        # all files filter
        filter_all = Gtk.FileFilter.new()
        filter_all.set_name("All")
        filter_all.add_pattern("*")

        # add filters, set overwrite alert to yes
        dialog.add_filter(filter_text)
        dialog.add_filter(filter_all)
        dialog.set_do_overwrite_confirmation(True)        

        # get the response, return filename or None
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            dialog.destroy()
            return filename
        if response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            return None

    def dialog_file_save_as(self):
        """
        Launch a File/Save dialog window
        """
        dialog = Gtk.FileChooserDialog("Save your project", None,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        # plaintext filter
        filter_text = Gtk.FileFilter.new()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")

        # all files filter
        filter_all = Gtk.FileFilter.new()
        filter_all.set_name("All")
        filter_all.add_pattern("*")

        # add filters, set overwrite alert to yes
        dialog.add_filter(filter_text)
        dialog.add_filter(filter_all)
        dialog.set_do_overwrite_confirmation(True)        

        # get the response, return filename or None
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            dialog.destroy()
            return filename
        if response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            return None

    def dialog_help(self):
        """
        Launch a help message
        """
        shortcuts = """
FILE SHORTCUTS:
Control + N = New File
Control + O = Open File
Control + S = Save File
Control + Shift + S = Save File As

EDIT SHORTCUTS:
Control + Z = Undo Edit
Control + Y = Redo Edit
Control + X = Cut Selection
Control + C = Copy Selection
Control + V = Paste Clipboard

VIEW SHORTCUTS
F1 = Help
F2 = About
F3 = Toggle Toolbar

F11 = Toggle Fullscreen
"""
        # generate help message dialog    
        dialog = Gtk.MessageDialog(message_format="Keyboard Shortcuts")
        dialog.set_property("message_type", Gtk.MessageType.INFO)
        dialog.format_secondary_text(shortcuts)
        dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        response = dialog.run()
        if response:
            dialog.destroy()

    # UI DEFINITION METHODS
    # IDEA: Loading glade files and CSS?

    def create_toolbar(self):
        """
        Loads toolbar with 10 stock buttons, adds them to dict
        """
        self.toolbar = Gtk.Toolbar.new()
        self.box.pack_start(self.toolbar, False, False, 0)
        buttons = self.buttons

        # NEW button
        button_new = Gtk.ToolButton.new_from_stock(Gtk.STOCK_NEW)
        self.toolbar.insert(button_new, 0)
        buttons["file_new"] = button_new

        # OPEN button
        button_open = Gtk.ToolButton.new_from_stock(Gtk.STOCK_OPEN)
        self.toolbar.insert(button_open, 1)
        buttons["file_open"] = button_open

        # SAVE button
        button_save = Gtk.ToolButton.new_from_stock(Gtk.STOCK_SAVE)
        self.toolbar.insert(button_save, 2)
        buttons["file_save"] = button_save

        # SAVE AS button
        button_save_as = Gtk.ToolButton.new_from_stock(Gtk.STOCK_SAVE_AS)
        self.toolbar.insert(button_save_as, 3)
        buttons["file_save_as"] = button_save_as

        # UNDO button
        button_undo = Gtk.ToolButton.new_from_stock(Gtk.STOCK_UNDO)
        self.toolbar.insert(button_undo, 4)
        buttons["edit_undo"] = button_undo

        # REDO button
        button_redo = Gtk.ToolButton.new_from_stock(Gtk.STOCK_REDO)
        self.toolbar.insert(button_redo, 5)
        buttons["edit_redo"] = button_redo

        # CUT button
        button_cut = Gtk.ToolButton.new_from_stock(Gtk.STOCK_CUT)
        self.toolbar.insert(button_cut, 6)
        buttons["edit_cut"] = button_cut

        # COPY button
        button_copy = Gtk.ToolButton.new_from_stock(Gtk.STOCK_COPY)
        self.toolbar.insert(button_copy, 7)
        buttons["edit_copy"] = button_copy

        # PASTE button
        button_paste = Gtk.ToolButton.new_from_stock(Gtk.STOCK_PASTE)
        self.toolbar.insert(button_paste, 8)
        buttons["edit_paste"] = button_paste

        # ABOUT button
        button_about = Gtk.ToolButton.new_from_stock(Gtk.STOCK_ABOUT)
        self.toolbar.insert(button_about, 9)
        buttons["view_about"] = button_about


class Application:
    """
    Controller for Word Agent. Connects signals for windows
    """
    def __init__(self):
        self.seg = Segment.new()
        self.win = EditorWindow()
        self.win.view.set_buffer(self.seg.buffer)

        # boolean for File/Save(as) functions
        self.file_is_saved_as = False

        # button keywords match from EditorWindow.buttons
        self.handlers = {
            "file_new": self.do_file_new,
            "file_open": self.do_file_open,
            "file_save": self.do_file_save,
            "file_save_as": self.do_file_save_as,
            "edit_undo": self.do_edit_undo,
            "edit_redo": self.do_edit_redo,
            "edit_cut": self.do_edit_cut,
            "edit_copy": self.do_edit_copy,
            "edit_paste": self.do_edit_paste,
            "view_about": self.do_view_about,
            "view_help": self.do_view_help,
            "view_typewriter": self.do_view_typewriter,
            "view_fullscreen": self.do_view_fullscreen,
            }

        self.connections()
        self.win.show_all()

        self.win.connect("key-press-event", self.execute_operation)

    def connections(self):
        for name, widget in self.win.buttons.items():
            if name in self.handlers:
                widget.connect("clicked", self.handlers[name])

    def change_buffer(self, filename=None):
        text = read_from_file(filename)
        if text is "":
            self.seg = Segment.new()
            self.win.view.set_buffer(self.seg.buffer)
        else:
            self.seg = Segment.new(filename=filename, content=text)
            self.win.view.set_buffer(self.seg.buffer)

    def execute_operation(self, widget, event):
        keystroke = Gtk.accelerator_get_label(event.keyval, event.state)
        if "Ctrl" in keystroke:
            if "N" in keystroke:
                self.handlers["file_new"](None)
            elif "O" in keystroke:
                self.handlers["file_open"](None)
            elif "S" in keystroke:
                if "Shift" in keystroke:
                    self.handlers["file_save_as"](None)
                else:
                    self.handlers["file_save"](None)
            elif "Z" in keystroke:
                self.handlers["edit_undo"](None)
            elif "Y" in keystroke:
                self.handlers["edit_redo"](None)
        elif "F1" in keystroke:
            if "F11" in keystroke:
                self.handlers["view_fullscreen"](None)
            else:
                self.handlers["view_help"](None)
        elif "F2" in keystroke:
            self.handlers["view_about"](None)
        elif "F3" in keystroke:
            self.handlers["view_typewriter"](None)

    # FILE handlers
    def do_file_new(self, widget):
        """
        Create a new Segment, with default filename and content
        """
        self.change_buffer()
        self.file_is_saved_as = False

    def do_file_open(self, widget):
        """
        Loads text from a file and creates Segment with that text
        """
        filename = self.win.dialog_file_open()
        if filename:
            self.change_buffer(filename)
            self.file_is_saved_as = True

    def do_file_save(self, widget):
        """
        Overwrites old file, prompts file/save-as if needed
        """
        if self.file_is_saved_as is False:
            self.seg.filename = self.win.dialog_file_save_as()

        if self.seg.filename:
            write_to_file(self.seg.filename, self.seg.curr_text)
            self.file_is_saved_as = True

    def do_file_save_as(self, widget):
        """
        Ensures Save As... prompt for do_file_save
        """
        self.file_is_saved_as = False
        self.do_file_save(widget)

    # EDIT handlers
    def do_edit_undo(self, widget):
        """
        Sets the text back one edit
        """
        self.seg.undo()

    def do_edit_redo(self, widget):
        """
        The opposite of undo
        """
        self.seg.redo()

    def do_edit_cut(self, widget):
        """
        Implements basic edit/cut
        """
        self.seg.cut()

    def do_edit_copy(self, widget):
        """
        Implements basic edit/copy
        """
        self.seg.copy()

    def do_edit_paste(self, widget):
        """
        Implements basic edit/paste
        """
        self.seg.paste()

    # VIEW handlers
    def do_view_typewriter(self, widget):
        """
        Toggles whether the toolbar is visible
        """
        if self.win.toolbar.get_visible():
            self.win.toolbar.set_visible(False)
        else:
            self.win.toolbar.set_visible(True)

    def do_view_about(self, widget):
        """
        Launches about dialog from MainWindow
        """
        self.win.dialog_about()

    def do_view_fullscreen(self, widget):
        """
        Toggles fullscreen mode
        """
        if self.win.is_fullscreen:
            self.win.unfullscreen()
            self.win.is_fullscreen = False
        else:
            self.win.fullscreen()
            self.win.is_fullscreen = True

    def do_view_help(self, widget):
        """
        Launches help dialog from MainWindow
        """
        self.win.dialog_help()

def main():
    """
    Gets things rolling
    """
    print("Starting Word Agent")
    app = Application()
    Gtk.main()

if __name__ == '__main__':
    main()
else:
    print("Word Agent, by Sam Hatfield. Enjoy!")
