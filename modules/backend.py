#! /usr/bin/env python3
# file: modules/backend.py

from difflib import SequenceMatcher
import io, redis

class Segment:
    """
    Encapsulates a segment, including the text, edit history,
    and lexical analysis.

    TODO: add in versioning scheme w/ diffs
    TODO: add in lexical analysis wi/ NLTK
    """
    def __init__(self, designation, content):

        self._designation = str(designation)
        r_server.rpush(self.edits, 'nil')
        r_server.rpush(self.edits, content)

    @staticmethod
    def new(designation="default_seg", content="DEFAULT TEXT"):
        segment = Segment(designation, content)
        print("new segment, redis hash", segment.redis_hash)
        return segment

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
        return "segments:" + self._designation + ":edits"

    @property
    def edits_list(self):
        return r_server.lrange(self.edits, 0, -1)

    @property
    def redis_hash(self):
        return self._designation

    @property
    def prev_edit(self):
        prev_edit = self.edits_list[-2]
        if prev_edit != b'nil':
            return prev_edit.decode()
        else:
            return None

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
    print("Begin backend self testing")
    print()
    print('Connecting to redis server, using db 14... ')
    r_server = redis.Redis(db=14)

    if (r_server.ping()):
        print("server ping sucessful")
    else:
        print("server ping failed")

    print("flushing db 14")
    r_server.flushdb()
    print()

    print("init default_segment")
    default_seg = Segment.new()
    print("edits list after init: ", default_seg.edits_list)
    print("edits list length: ", len(default_seg.edits_list))
    print()

    words = ["first", "second", "third", "fourth"]
    test_edits = []
    for word in words:
        test_edits.append(word)
    print("test edits list: ", test_edits)
    print("test edits length: ", len(test_edits))
    print()

    for edit in test_edits:
        default_seg.add_edit(edit)

    print("edits list after adding test edits: ", default_seg.edits_list)
    print("edits list length: ", len(default_seg.edits_list))
    print()

    print("testing undo action...")
    for i in range(0,(len(words)-1)):
        default_seg.undo()
        print("Undo #", i, ": ", default_seg.edits_list)
        print("edits list length: ", len(default_seg.edits_list))
        print("base_edit: ", default_seg.base_edit)
        print("prev_edit: ", default_seg.prev_edit)
        print("curr_edit: ", default_seg.curr_edit)
        print()

    print("testing redo action")
    for i in range(0,(len(words)-3)):
        default_seg.redo()
        print("Redo #", i, ": ", default_seg.edits_list)
        print("edits list length: ", len(default_seg.edits_list))
        print("base_edit: ", default_seg.base_edit)
        print("prev_edit: ", default_seg.prev_edit)
        print("curr_edit: ", default_seg.curr_edit)
        print()

    print("add edit, should truncate old edits from list")
    default_seg.add_edit("fifth")
    print("edits list after adding new edit: ", default_seg.edits_list)
    print("edits list length: ", len(default_seg.edits_list))
    print("base_edit: ", default_seg.base_edit)
    print("prev_edit: ", default_seg.prev_edit)
    print("curr_edit: ", default_seg.curr_edit)
    print()
