#! /usr/bin/env python
# file: backend.py

"""
NOTE ABOUT THIS FILE:

This is the backend of the RESTful API for Word Agent.

I'm going to make sure that this module is complete before I remove
functionality from the 'classic version'.

TODO: Reimplement the deque as a Redis data store.
I'll be able to have multiple segments represented in memory
with their own edit deques and other metadata.
"""

from collections import deque
from difflib import SequenceMatcher
import io, redis

# UTILITY FUNCTIONS
def error_msg(error):
    return "A problem occured: {}".format(error)

# CLASS DEFINITIONS
class ProjectIO:
    """
    Performs IO operations/checking between RAM, disk, and networks
    """
    def __init__(self):
        """
        This loads in the metadata file for a project
        """
        try:
            self._redis_server = redis.Redis('localhost')
        except IOError as e:
            error_msg(e)

    @property
    def redis(self):
        return self._redis_server

    def insert(filename):
        """
        Opens, reads, and returns the text contents of filename
        """
        content = None
        if filename:
            with open(filename, "r") as textfile:
                for line in textfile:
                    content += line
        return content

    def export(filename, content):
        """
        Writes text content to filename on disk
        """
        if filename:
            with open(filename, "w") as f:
                f.write(content)

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

    TODO: refactor to wrap around Redis functions for data
    TODO: add in versioning scheme w/ diffs
    TODO: add in lexical analysis wi/ NLTK
    """
    def __init__(self, text):
        """
        Requirements: deque
        """
        self._edits = deque([None, text])

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

    @curr_edit.setter
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


if __name__ == '__main__':

    print("Begin backend self testing")
    project = ProjectIO()

    if (project.redis.ping()):
        print("Redis server ping sucessful")
    else:
        print("Redis server ping failed")


