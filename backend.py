#! /usr/bin/env python3
# file: modules/backend.py

import datetime, io, redis

# Constants

REDIS_DEFAULT_DB = 10
SEGMENT_DEFAULT_DESIGNATION = "default_seg"
SEGMENT_DEFAULT_CONTENT = "Welcome to Word Agent!"

# Class definitions

class Segment:
    """
    Encapsulates a segment, including the text, edit history,
    and lexical analysis.

    TODO: add in versioning scheme w/ diffs
    TODO: add in lexical analysis wi/ NLTK
    """
    def __init__(self, designation, content):

        self._designation = str(designation)

        r_server.set(self.redis_key, datetime.datetime.utcnow())
        r_server.rpush(self.edits, 'nil')
        r_server.rpush(self.edits, content)

        print("new segment, redis key", self.designation)

    @staticmethod
    def new(designation=SEGMENT_DEFAULT_DESIGNATION,
            content=SEGMENT_DEFAULT_CONTENT):

        return Segment(designation, content)

    @staticmethod
    def open(designation):
        redis_key = "segments:" + designation
        if r_server.keys(redis_key):
            print("opening segment from key", designation)
            content = r_server.lindex(redis_key+"edits", -1)
            return Segment(designation, content)
        else:
            content = ""
            return Segment.new(designation, content)

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
        curr_edit = self.edits_list[-1]
        if curr_edit != b'nil':
            return curr_edit.decode()
        else:
            return "The edit queue is empty"

    @property
    def edits(self):
        return self.redis_key + ":edits"

    @property
    def edits_list(self):
        return r_server.lrange(self.edits, 0, -1)

    @property
    def designation(self):
        return self._designation

    @property
    def prev_edit(self):
        prev_edit = self.edits_list[-2]
        if prev_edit != b'nil':
            return prev_edit.decode()
        else:
            return None

    @property
    def redis_key(self):
        return "segments:" + self.designation

    # Edit functions
    def add_edit(self, text):
        """
        Add text to edits, as long as there have been changes
        """
        if (text == self.curr_edit):
            return False

        r_server.rpush(self.edits, text)

        # clears out old edits using sentinel value
        while self.base_edit is not None:
            r_server.lpop(self.edits)

        return True

    def undo(self):
        """
        Reverts segment to earlier state of edits
        """
        # if prev_edit is None, we've rotated to oldest change
        if self.prev_edit:
            tmp = r_server.rpop(self.edits)
            r_server.lpush(self.edits, tmp)
            return True
        else:
            return False

    def redo(self):
        """
        Reverts segment to later state, if it still exists
        """
        # if base_edit is None, we've rotated all the way back
        if self.base_edit:
            tmp = r_server.lpop(self.edits)
            r_server.rpush(self.edits, tmp)
            return True
        else:
            return False


if __name__ == '__main__':
    import test
    test.backend_test()
else:
    r_server = redis.Redis(db=REDIS_DEFAULT_DB)
    print("redis server ping: ", r_server.ping())
    r_server.flushdb()
    segment = Segment.new()
