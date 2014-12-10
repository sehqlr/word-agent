#! /usr/bin/env python
# file: wa_backend.py

"""
NOTE ABOUT THIS FILE:

This is the 'back end' version. I will work on making this module independent
from GTK. This is where I hope to inplement the other features as well.
Then, the GTK front end module will have most of the same functionality, 
except with an import from here.

I'm going to make sure that this module is complete before I remove
functionality from the 'classic version'. 
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
    Writes text content to filename on disk
    """
    if filename:
        with open(filename, "w") as f:
            f.write(content)

# CLASS DEFINITIONS
class Project:
    """
    This class initializes and analyzes a project's files. This prepares
    the data to be used by the Collections.
    """
    def __init__(self, root_dir):
        """
        This loads in the metadata file for a project
        """
        self._root_dir = root_dir
        self._metadata_file = read_from_file(None) #TODO: implement parsing of a metadata file. This is the main purpose of the constructor

    @staticmethod
    def new(self, root_dir):
        return Project(root_dir)

    def read(self):
        """
        This loads in an existing project's files, and creates objects
        to load it into RAM
        """
        pass

    def write(self):
        """
        This saves the data to disk
        """
        pass

class Resource:
    """
    This class represents the data about resources in the work, including
    characters, places, references, etc. It is similar to a Segment.
    """
    def __init__(self):

        self.fields = {
                "type": None,
                "name": None,
                "notes": None,
                "img": None,
                "appears_in": None #Matches from self.find()
                }
    
    @staticmethod
    def find(resource):
        """
        Compiles a re to find the resource within the segments
        """
        pass

    @staticmethod
    def new():
        # Resource.find()
        return Resource()

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
        return Segment(filename, content)

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
    def autosave(self):
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

"""
Front ends should invoke these methods.
"""

class API:
    """
    API for Word Agent.
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
            }

    def change_buffer(self, filename=None):
        text = read_from_file(filename)
        if text is "":
            self.seg = Segment.new()
            self.win.view.set_buffer(self.seg.buffer)
        else:
            self.seg = Segment.new(filename=filename, content=text)
            self.win.view.set_buffer(self.seg.buffer)

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

if __name__ == '__main__':
    print("The backend is not done yet."
else:
    print("Word Agent, by Sam Hatfield. Enjoy!")
