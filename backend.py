#! /usr/bin/env python3
# file: modules/backend.py

import io, redis

# Constants

REDIS_DEFAULT_DB = 10
SEGMENT_DEFAULT_FILENAME = "untitled"
SEGMENT_DEFAULT_CONTENT = ""

# Class definitions

class Segment:
    """
    Encapsulates a segment, including the text, edit history, and filepath

    TODO: finish data schema and file formats/path
    TODO: add in versioning scheme w/ diffs
    """

    # redis server access point for all segments
    r_server = redis.Redis(db=REDIS_DEFAULT_DB)

    def __init__(self, file_id):

        self._file_id = file_id
        self.r_server.rpush(self.edits_key, 'nil')
        self.r_server.set("current", self.file_id)

    @staticmethod
    def count():
        count = Segment.r_server.get("count")
        if count:
            return count.decode()
        else:
            return "0"

    @staticmethod
    def current():
        current = Segment.r_server.get("current")
        if current:
            return current.decode()
        else:
            return Segment.count()

    @staticmethod
    def new(filename=SEGMENT_DEFAULT_FILENAME,
            content=SEGMENT_DEFAULT_CONTENT):

        Segment.r_server.incr("count")
        file_id = Segment.count()
        new_seg = Segment(file_id)
        Segment.r_server.set(new_seg.redis_key, filename)
        Segment.r_server.rpush(new_seg.edits_key, content)
        return new_seg

    @staticmethod
    def open(file_id):
        max_file_id = Segment.count()
        if file_id <= max_file_id:
            filename = Segment.r_server.get("file:" + file_id)
            content = Segment.r_server.lindex("edits:" + file_id, -1)
            return Segment.new(filename=filename, content=content)
        else:
            filename = SEGMENT_DEFAULT_FILENAME
            content = ""
            return Segment.new(filename=filename,content=content)

    @staticmethod
    def save(file_id):
        file_id = str(file_id)
        filename = Segment.r_server.get("file:"+file_id)
        content = Segment.r_server.lindex("edits:"+file_id, -1)
        with open(filename, "w") as file:
            file.write(content.decode())
        return filename.decode()

    # properties, listed alphabetically
    @property
    def base_edit(self):
        base_edit = self.edits[0]
        if base_edit != 'nil':
            return base_edit
        else:
            return None

    @property
    def curr_edit(self):
        curr_edit = self.edits[-1]
        if curr_edit != 'nil':
            return curr_edit
        else:
            return "The edit queue is empty"

    @property
    def edits(self):
        edits = self.r_server.lrange(self.edits_key, 0, -1)
        decoded = [edit.decode() for edit in edits]
        return decoded

    @property
    def edits_key(self):
        return "edits:" + self.file_id

    @property
    def file_id(self):
        return str(self._file_id)

    @property
    def filename(self):
        filename = self.r_server.get(self.redis_key)
        return filename.decode()

    @property
    def prev_edit(self):
        prev_edit = self.edits[-2]
        if prev_edit != 'nil':
            return prev_edit
        else:
            return None

    @property
    def redis_key(self):
        return "file:" + self.file_id

    # Edit functions
    def add_edit(self, text):
        """
        Add text to edits, as long as there have been changes
        """
        if (text == self.curr_edit):
            return False

        self.r_server.rpush(self.edits_key, text)

        # clears out old edits using sentinel value
        while self.base_edit is not None:
            self.r_server.lpop(self.edits_key)

        return True

    def undo(self):
        """
        Reverts segment to earlier state of edits
        """
        # if prev_edit is None, we've rotated to oldest change
        if self.prev_edit:
            tmp = self.r_server.rpop(self.edits_key)
            self.r_server.lpush(self.edits_key, tmp)
            return True
        else:
            return False

    def redo(self):
        """
        Reverts segment to later state, if it still exists
        """
        # if base_edit is None, we've rotated all the way back
        if self.base_edit:
            tmp = self.r_server.lpop(self.edits_key)
            self.r_server.rpush(self.edits_key, tmp)
            return True
        else:
            return False
