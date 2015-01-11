#! /usr/bin/env python3
# file: modules/backend.py

import io, redis, datetime

# Dispatch functions
def file_new(**kwargs):
    if kwargs is not None:
        designation = kwargs.pop("designation")
        content     = kwargs.pop("content")
        return Segment.new(designation=designation, content=content)
    else:
        return Segment.new()

def file_open(**kwargs):
    if kwargs is not None:
        designation = kwargs.pop("designation")
        content     = kwargs.pop("content")
        return Segment.open(designation=designation, content=content)
    else:
        return Segment.open()

def file_save():
    r_server.bgsave()

def edit_undo():
    segment.undo()

def edit_redo():
    segment.redo()

def edit_add(text):
    text = str(text)
    segment.add_edit(text)

# dict of dispatch funcs
dispatcher = {
    "file_new": file_new,
    "file_open": file_open,
    "file_save": file_save,
    "edit_undo": edit_undo,
    "edit_redo": edit_redo,
    "edit_add": edit_add,
    }

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

    @staticmethod
    def new(designation="default_seg", content="DEFAULT TEXT"):
        segment = Segment(designation, content)
        print("new segment, redis hash", segment.designation)
        return segment

    @staticmethod
    def open(designation, content):
        redis_key = "segments:" + designation
        if r_server.keys(redis_key):
            segment = Segment(designation, content)
            print("opening segment from key", segment.designation)
            return segment
        else:
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
    import test
    test.test()
else:
    r_server = redis.Redis(db=10)
