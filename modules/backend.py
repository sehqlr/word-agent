#! /usr/bin/env python3
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
    def __init__(self, designation, content):

        self._designation = str(designation)
        r_server.rpush(self.edits, 'nil')
        r_server.rpush(self.edits, content)

        self._matcher = SequenceMatcher()

    @staticmethod
    def new(designation="default_seg", content="DEFAULT TEXT"):
        return Segment(designation, content)

    # properties, listed alphabetically
    @property
    def base_edit(self):
        base_edit = self.edits_list[0]
        if base_edit != b'nil':
            return base_edit.decode()
        else:
            return None

    @property
    def curr_edit(self):
        return self.edits_list[-1].decode()

    @property
    def edits(self):
        return "segments:" + self._designation + ":edits"

    @property
    def edits_list(self):
        return r_server.lrange(self.edits, 0, -1)

    @property
    def redis_hash(self):
        return self._designation

    @property
    def matcher(self):
        return self._matcher

    @property
    def prev_edit(self):
        prev_edit = self.edits_list[-2]
        if prev_edit != b'nil':
            return prev_edit.decode()
        else:
            return None

    # SAVE METHOD
    def add_edit(self, text):
        """
        Add text to edits, as long as there have been changes
        """
        try:
            text = str(text)
            if (text == self.curr_edit):
                return False

            r_server.rpush(self.edits, text)

            # clears out old edits using sentinel value
            while self.base_edit is not None:
                r_server.lpop(self.edits)

            return True
        except IOError as e:
            error_msg(e)

    # UNDO/REDO METHODS
    def undo(self):
        """
        Reverts segment to earlier state of edits
        """

        # if prev_edit is None, we've rotated to oldest change
        if self.prev_edit:
            tmp = r_server.rpop(self.edits)
            r_server.lpush(self.edits, tmp)
        else:
            print("Nothing to undo")

    def redo(self):
        """
        Reverts segment to later state, if it still exists
        """
        # if base_edit is None, we've rotated all the way back
        if self.base_edit:
            tmp = r_server.lpop(self.edits)
            r_server.rpush(self.edits, tmp)
        else:
            print("Nothing to redo")


if __name__ == '__main__':

    print("Begin backend self testing")
    r_server = redis.Redis()
    r_server.delete("segment")

    if (r_server.ping()):
        print("Redis server ping sucessful")
    else:
        print("Redis server ping failed")

    default_seg = Segment.new()
    print("edits list after init: ", default_seg.edits_list)

    test_edits = ["first", "second", "third", "fourth", "fifth"]
    print("test edits list: ", test_edits)

    for edit in test_edits:
        default_seg.add_edit(edit)

    print("edits list after adding test edits: ", default_seg.edits_list)
