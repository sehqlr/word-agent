#! /usr/bin/env python
# file: backend.py

"""
NOTE ABOUT THIS FILE:

This is the backend of the RESTful API for Word Agent.

I'm going to make sure that this module is complete before I remove
functionality from the 'classic version'. 
"""

from collections import deque
from difflib import SequenceMatcher
import io

# UTILITY FUNCTIONS

def error_msg(error):
    return "A problem occured: {}".format(error)

def read_from_file(filename):
    """
    Opens, reads, and returns the text contents of filename
    """
    content = None
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
    This is the collection 
    """
    def __init__(self, metadata_file):
        """
        This loads in the metadata file for a project
        """
        try:
            self._metadata = read_from_file(metadata_file)
        except IOError as e:
            error_msg(e)

    @staticmethod
    def new(metadata_file):
        return Project(metadata_file)

    @property
    def metadata(self):
        return self._metadata

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

resource_fields = {
    "type": None,
    "name": None,
    "notes": None,
    "img": None,
    "appears_in": None #Matches from self.find()
}

class Segment: 
    """
    Encapsulates a segment, including the text, edit history, 
    and lexical analysis. 
    """
    def __init__(self, text):
        """
        Requirements: deque
        """
        self._edits = deque([None, "", text])

    @staticmethod
    def new(content="DEFAULT TEXT"):
        return Segment(content)

    # properties, listed alphabetically
    @property
    def base_edit(self):
        return self._edits[0]

    @property
    def curr_edit(self):
        return self._edits[-1]

    @curr_text.setter
    def curr_edit(self, value):
        try:
            self._edits[-1] = str(value)
        except IOError as e:
            error_msg(e)

    @property
    def edits_list(self):
        return list(self._edits)

    @property
    def matcher(self):
        return self._matcher

    @property
    def prev_edit(self):
        return self._edits[-2]

    # SAVE METHOD
    def save(self, text):
        """
        Add text to edits deque, as long as there have been changes
        """
        try:
            text = str(text)
            if (text == self.curr_text):
                return False

            self.edits.append(text)

            # clears out old edits using sentinel value
            while self.base_edit is not None:
                self.edits.popleft()

            return True
        except IOError as e:
            error_msg(e)

    # UNDO/REDO METHODS
    def undo(self):
        """
        Reverts segment to earlier state, from the edits deque
        """

        # rotate the most recent addition to the back of the deque
        self.edits.rotate(1)

        # if prev_edit is None, we've rotated all the way around
        if self.prev_edit:
            self.curr_text = self.prev_edit
        else:
            print("Nothing to undo")

    def redo(self):
        """
        Reverts segment to later state, if it still exists
        """
        # if base_edit is None, we've rotated all the way back
        if self.base_edit:
            self.edits.rotate(-1)
            self.curr_text = self.prev_edit
        else:
            print("Nothing to redo")

#API functions
api_handlers = {
        "file": {
            "new": do_file_new,
            "open": do_file_open,
            "save": do_file_save,
            },
        "edit": {
            "undo": do_edit_undo,
            "redo": do_edit_redo,
            },
        }

# FILE handlers
def do_file_new(segment):
    """
    Create a new Segment, with default filename and content
    """
    change_buffer()
    file_is_saved_as = False

def do_file_open(segment):
    """
    Loads text from a file and creates Segment with that text
    """
    filename = win.dialog_file_open()
    if filename:
        change_buffer(filename)
        file_is_saved_as = True

def do_file_save(segment):
    """
    Overwrites old file, prompts file/save-as if needed
    """
    if file_is_saved_as is False:
        seg.filename = win.dialog_file_save_as()

    if seg.filename:
        write_to_file(seg.filename, seg.curr_text)
        file_is_saved_as = True

# EDIT handlers
def do_edit_undo(segment):
    """
    Sets the text back one edit
    """
    seg.undo()

def do_edit_redo(segment):
    """
    The opposite of undo
    """
    seg.redo()

if __name__ == '__main__':
    print("Unit tests have not been implemented yet.")
