#! /usr/bin/env python3
# file: modules/backend.py

import io, redis

# Constants

REDIS_DEFAULT_DB = 10
REDIS_FILE_SET = "files"
SEGMENT_DEFAULT_FILE_ID = 1
SEGMENT_DEFAULT_FILENAME = "default_seg"
SEGMENT_DEFAULT_CONTENT = "Welcome to Word Agent!"

# Class definitions

class Segment:
    """
    Encapsulates a segment, including the text, edit history, and filepath

    TODO: finish data schema and file formats/path
    TODO: add in versioning scheme w/ diffs
    """

    # redis server access point for all segments
    r_server = redis.Redis(db=REDIS_DEFAULT_DB)

    def __init__(self, file_id, filename, content):

        self._file_id = file_id

        self.r_server.sadd(REDIS_FILE_SET, self.file_id)
        self.r_server.set(self.redis_key, filename)
        self.r_server.rpush(self.edits_key, 'nil')
        self.r_server.rpush(self.edits_key, content)
        self.r_server.set("current", self.file_id)

    @staticmethod
    def current():
        return Segment.r_server.get("current").decode()

    @staticmethod
    def new(file_id=SEGMENT_DEFAULT_FILE_ID,
            filename=SEGMENT_DEFAULT_FILENAME,
            content=SEGMENT_DEFAULT_CONTENT):

        return Segment(file_id, filename, content)

    @staticmethod
    def open(file_id):
        file_ids = Segment.r_server.sort(REDIS_FILE_SET, desc=True)
        if file_id in file_ids:
            print("opening segment id", file_id)
            filename = self.r_server.get("file:" + file_id)
            content = self.r_server.lindex(self.edits_key, -1)
            return Segment(file_id, filename, content)
        else:
            file_id = int(file_ids[0]) + 1
            filename = None
            content = ""
            return Segment.new(filename, content)

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
        edits = [edit.decode() for edit in edits]
        return edits

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
