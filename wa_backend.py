#! /usr/bin/env python3
# file: wa_backend.py

"""
NOTE ABOUT THIS FILE:

This is the 'back end' version. I will work on making this module independent
from GTK. This is where I hope to inplement the other features as well.
Then, the GTK front end module will have most of the same functionality, 
except with an import from here.

I'm going to make sure that this module is complete before I remove
functionality from the 'classic version'. Obviously, I won't push these
changes to the master branch until it is stable. Then I think I can call
it v0.3.
"""

from collections import deque
from difflib import SequenceMatcher
import io

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
class ProjectManager:
    """
    This class initializes and analyzes a project's files. This prepares
    the data to be used by the Collections.
    """
    def __init__:
        # dir_dict maps the project's directory
        self._dir_dict = {resrc=[], segs=[], meta=[]}

    def initProject:
        pass

    def readProject:
        pass

    def writeProject:
        pass


class Resource:
    """
    This class represents the data about resources in the work, including
    characters, places, references, etc. It is similar to a Segment.
    """
    pass

class ResourceCollection:
    """
    This class is similar to SegmentCollection, but for Resources.
    """
    pass

class Segment:
    """
    Model for Word Agent. Encapsulates a segment
    """
    def __init__(self, filename, content):

        # stores the text as a string
        self._text = content

        # instead of a file object, we keep/update the name only
        self._filename = filename

        # matcher limits number of autosave operations
        # see text_comparison and autosave methods for more details
        self._matcher = SequenceMatcher()

        # edits is the double ended queue (deque) for autosave feature
        self._edits = deque([None, content])

    @staticmethod
    def new(filename="untitled", content="DEFAULT TEXT"):
        new = Segment(filename, content)
        return new

    # properties, listed alphabetically
    @property
    def base_edit(self):
        return self._edits[0]

    @property
    def curr_text(self):
        return self._text

    @curr_text.setter
    def curr_text(self, value):
        if isinstance(value, str):
            self._text = value

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
        # if base_edit is None, we've rotated all the way back
        if self.base_edit:
            self.edits.rotate(-1)
            self.curr_text = self.prev_edit
        else:
            print("Nothing to redo")

class SegmentCollection:
    """
    This class will be a factory for Segments, loading text from disk to RAM, 
    then passing the data to the front end as needed. I want to have this
    perform most of the file I/O and OS operations.
    """
    pass

"""
I want the Application class to be rewritten to be a CommandParser.
It's similar to an event handler, but CommandParser will interface
with the back end. Front ends should invoke these methods.
"""

class CommandParser:
    """
    Controller for Word Agent.
    """
    def __init__(self):
        self.seg = Segment.new()

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
            if "Q" in keystroke:
                Gtk.main_quit()
            elif "N" in keystroke:
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

if __name__ == '__main__':
    print("The backend is not done yet."
else:
    print("Word Agent, by Sam Hatfield. Enjoy!")
