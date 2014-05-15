from collections import deque
from difflib import SequenceMatcher
from gi.repository import Gtk, Gdk
import io

welcome_message = """
Welcome to the Word Agent, the novel project management app!

We are in v0.2, which means that current features and bugfixes will be
worked on, not new features. New features to come in v0.3.

If you have any questions, concerns, or comments, please create an
issue on our GitHub page or email me with the details.

New features coming in v0.3:
    Project management
    Document rendering (to ODF at first, more formats coming later)

Future Features:
    Version Control System integration
    Cloud Collaboration with WebRTC
    "Post Production" formatting (e.i. Markdown)
"""


class Segment:
    """Encapsulates a segment, including its buffer, view, file, etc"""

    def __init__(self, filename="untitled", content=welcome_message):

        # creates TextBuffer, TextView, and Clipboard
        self._buffer = Gtk.TextBuffer()
        self._buffer.set_text(content)
        self._view = Gtk.TextView.new_with_buffer(self._buffer)
        self._clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self._buffer.add_selection_clipboard(self._clipboard)

        # instead of a file object, we keep/update the name only
        self._filename = filename

        # matcher limits number of autosave operations
        # see text_comparison and autosave methods for more details
        self._matcher = SequenceMatcher()

        # edits is the double ended queue (deque) for autosave feature
        self._edits = deque([None, content])

    # coding 'private' members via properties, listed alphabetically
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
    def base_edit(self):
        self._edits[0]

    @property
    def matcher(self):
        return self._matcher

    @property
    def prev_edit(self):
        return self._edits[-1]

    @property
    def view(self):
        return self._view

    # AUTOSAVE METHOD
    def autosave(self):
        """If enough changes have been made, add text to _edits"""
        # IDEA: percentage here could be changed in Settings.
        self.matcher.set_seqs(self.curr_text, self.prev_edit)
        ratio = self.matcher.quick_ratio()
        if ratio < 0.99:
            print("Text autosaved")
            self.edits.append(self.curr_text)

        # clears out old edits using sentinel value
        while self.base_edit is not None:
            self.edits.popleft()

    # UNDO/REDO BUTTON METHODS
    def undo(self):
        """Reverts TextBuffer to earlier state, from the edits deque"""
        # TODO: Change this so things don't get duplicated
        if self.base_edit is None:
            self.edits.append(self.curr_text)
            self.edits.rotate(1)
        if self.prev_edit is not None:
            self.edits.rotate(1)
            if self.prev_edit is not None:
                self.curr_text = self.prev_edit
        elif self.prev_edit is None:
            print("Nothing to undo")

    def redo(self):
        """Reverts TextBuffer to later state, if it still exists"""
        if self.prev_edit is not None:
            self.edits.rotate(-1)
            if self.prev_edit is not None:
                self.curr_text = self.prev_edit
        elif self.base_edit is None:
            print("Nothing to redo")

    # CUT/COPY/PASTE BUTTON METHODS
    def cut(self):
        """Basic edit/cut function"""
        if self.buffer.get_has_selection():
            self.buffer.cut_clipboard(self.clipboard, True)

    def copy(self):
        """Basic edit/copy function"""
        if self.buffer.get_has_selection():
            self.buffer.copy_clipboard(self.clipboard)

    def paste(self):
        """Basic edit/paste function"""
        self.buffer.paste_clipboard(self.clipboard, None, True)

    # NEW/OPEN/SAVE BUTTON METHODS
    def save(self):
        """Write curr_text to file"""
        with open(self.filename, "w") as textfile:
            textfile.write(self.curr_text)

    def open(self):
        """Opens and reads the text contents of self.filename"""
        # NOTE: Make sure you set self.filename to desired file first!
        content = ""
        with open(self.filename, "r") as textfile:
            for line in textfile:
                content += line
        self.curr_text = content

class MainWindow(Gtk.Window):
    """Hardcodes basic UX for Word Agent"""
    def __init__(self):
        # basic init stuff for window
        Gtk.Window.__init__(self, title="Word Agent")
        self.connect("destroy", self.gtk_main_quit)
        self.set_default_size(600, 600)

        # create the Box container and add toolbar and scrolled window
        self.box = Gtk.Box.new(1 , 3)
        self.add(self.box)
        self.create_toolbar()
        self.scroll = Gtk.ScrolledWindow.new(None, None)
        self.box.pack_start(self.scroll, True, True, 0)

        # creates new segment, connecting its custom signal
        self.seg = Segment()
        sig_id = self.seg.buffer.connect("changed", self.buffer_changed)
        self.sig_buffer_changed = sig_id

        # add view to scroll and show it
        self.scroll.add(self.seg.view)
        self.seg.view.show()

    def set_segment(self, filename):
        if filename:
            self.seg.filename = filename
            self.seg.open()
        else:
            self.seg.filename = "untitled"
            self.curr_text = welcome_message
        self.seg.edits.clear()
        self.seg.edits.append(None)

    # DIALOG METHODS
    # IDEA: Hide dialogs? That would require self.dialog-type members
    # TODO: Add file type filters to FileChooser dialogs
    def dialog_about(self):
        """Launch an About dialog window"""
        dialog = Gtk.AboutDialog.new()
        dialog.set_program_name("Word Agent")
        dialog.set_authors(["Sam Hatfield", None])
        dialog.set_version("0.2")
        dialog.set_website("https://github.com/sehqlr/word-agent")
        dialog.set_website_label("Fork us on GitHub!")
        dialog.set_comments("A simple text editor with a big future.")
        response = dialog.run()
        if response:
            print("About closed")
            dialog.destroy()

    def dialog_file_open(self):
        """Launch a File/Open dialog window"""
        dialog = Gtk.FileChooserDialog("Open a project", None,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            dialog.destroy()
        if response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        return filename

    def dialog_file_save_as(self):
        """Launch a File/Save dialog window"""
        dialog = Gtk.FileChooserDialog("Save your project", None,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            dialog.destroy()
        if response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        return filename

    # UI DEFINITION METHODS
    # IDEA: Loading glade files and CSS?
    def create_toolbar(self):
        """Loads ten Gtk Stock toolbar buttons, connects signals"""
        toolbar = Gtk.Toolbar.new()
        self.box.pack_start(toolbar, False, False, 0)

        # NEW button
        button_new = Gtk.ToolButton.new_from_stock(Gtk.STOCK_NEW)
        button_new.connect("clicked", self.do_file_new)
        toolbar.insert(button_new, 0)

        # OPEN button
        button_open = Gtk.ToolButton.new_from_stock(Gtk.STOCK_OPEN)
        button_open.connect("clicked", self.do_file_open)
        toolbar.insert(button_open, 1)

        # SAVE button
        button_save = Gtk.ToolButton.new_from_stock(Gtk.STOCK_SAVE)
        button_save.connect("clicked", self.do_file_save)
        toolbar.insert(button_save, 2)

        # SAVE AS button
        button_saveas = Gtk.ToolButton.new_from_stock(Gtk.STOCK_SAVE_AS)
        button_saveas.connect("clicked", self.do_file_saveas)
        toolbar.insert(button_saveas, 3)

        # UNDO button
        button_undo = Gtk.ToolButton.new_from_stock(Gtk.STOCK_UNDO)
        button_undo.connect("clicked", self.do_edit_undo)
        toolbar.insert(button_undo, 4)

        # REDO button
        button_redo = Gtk.ToolButton.new_from_stock(Gtk.STOCK_REDO)
        button_redo.connect("clicked", self.do_edit_redo)
        toolbar.insert(button_redo, 5)

        # CUT button
        button_cut = Gtk.ToolButton.new_from_stock(Gtk.STOCK_CUT)
        button_cut.connect("clicked", self.do_edit_cut)
        toolbar.insert(button_cut, 6)

        # COPY button
        button_copy = Gtk.ToolButton.new_from_stock(Gtk.STOCK_COPY)
        button_copy.connect("clicked", self.do_edit_copy)
        toolbar.insert(button_copy, 7)

        # PASTE button
        button_paste = Gtk.ToolButton.new_from_stock(Gtk.STOCK_PASTE)
        button_paste.connect("clicked", self.do_edit_paste)
        toolbar.insert(button_paste, 8)

        # ABOUT button
        button_about = Gtk.ToolButton.new_from_stock(Gtk.STOCK_ABOUT)
        button_about.connect("clicked", self.do_about)
        toolbar.insert(button_about, 9)

    # SIGNAL HANDLERS
    def gtk_main_quit(self, *args):
        """End program methods"""
        print("HANDLER: gtk_main_quit")
        Gtk.main_quit(*args)

    # autosave handler
    def buffer_changed(self, widget):
        """Custom signal for Segment.buffer"""
        print("HANDLER: on_buffer_changed")
        self.seg.autosave()

    # file handlers
    def do_file_new(self, widget):
        """Create a new Segment"""
        print("HANDLER: do_file_new")
        self.set_segment()
        self.file_is_saved_as = False

    def do_file_open(self, widget):
        """Loads text from a file and creates Segment with that text"""
        print("HANDLER: do_file_open")
        filename = self.dialog_file_open()
        self.set_segment(filename)
        self.file_is_saved_as = True

    def do_file_save(self, widget):
        """Overwrites old file, prompts file/save-as if needed"""
        print("HANDLER: do_file_save")
        if self.file_is_saved_as is not True:
            self.seg.filename = self.dialog_file_save_as()
        self.seg.write_to_file()
        self.file_is_saved_as = True

    def do_file_saveas(self, widget):
        """Ensures file/save-as prompt for do_file_save"""
        print("HANDLER: do_file_saveas")
        self.file_is_saved_as = False
        self.do_file_save()

    # edit handlers
    def do_edit_undo(self, widget):
        """Blocks custom signal for buffer to traverse autosave deque"""
        print("HANDLER: do_edit_undo")
        with self.seg.buffer.handler_block(self.sig_buffer_changed):
            self.seg.undo()

    def do_edit_redo(self, widget):
        """Moves the opposite way of undo in autosave deque"""
        print("HANDLER: do_edit_redo")
        with self.seg.buffer.handler_block(self.sig_buffer_changed):
            self.seg.redo()

    def do_edit_cut(self, widget):
        """Implements basic edit/cut"""
        print("HANDLER: do_edit_cut")
        self.seg.cut()

    def do_edit_copy(self, widget):
        """Implements basic edit/copy"""
        print("HANDLER: do_edit_copy")
        self.seg.copy()

    def do_edit_paste(self, widget):
        """Implements basic edit/paste"""
        print("HANDLER: do_edit_paste")
        self.seg.paste()

    def do_about(self, widget):
        """Launches about dialog from MainWindow"""
        print("HANDLER: on_about")
        self.dialog_about()
