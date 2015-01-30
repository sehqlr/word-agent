#! /usr/bin/env python3

import io, redis

# Class definitions

class Segment:
    """
    Encapsulates a segment, including the text, edit history, and filepath

    TODO: finish data schema and file formats/path
    TODO: add in versioning scheme w/ diffs
    """

    REDIS_KEY = "segments"
    FILEPATH_KEY = "filepath"
    CURRENT_KEY = "current"
    EDITS_KEY = "edits"
    FILEPATH = "full.txt"
    SEG_ID_KEY = "file"
    REDIS_DB = 10
    REDIS_NONE = 'nil'

    # redis server access point for all segments
    r_server = redis.Redis(db=REDIS_DB)

    def __init__(self, seg_id):

        self._seg_id = seg_id
        self.r_server.set(Segment.CURRENT_KEY, self.seg_id)

    @staticmethod
    def get_count():
        return Segment.r_server.llen(Segment.REDIS_KEY)

    @staticmethod
    def get_current():
        current = Segment.r_server.get(Segment.CURRENT_KEY)
        if current:
            return current.decode()
        else:
            return Segment.get_count()

    @staticmethod
    def get_collection():
        collection = []
        for seg_id in Segment.get_all_seg_ids():
            seg = Segment(seg_id)
            collection.append(seg)
        return collection

    @staticmethod
    def get_all_seg_ids():
        return Segment.r_server.lrange(Segment.REDIS_KEY, 0, -1)

    @staticmethod
    def new(content=""):

        count = Segment.get_count()
        if count > 0:
            seg_id = Segment.get_count() + 1
        else:
            seg_id = 1

        new_seg = Segment(seg_id)
        new_seg.add_edit(Segment.REDIS_NONE)
        new_seg.add_edit(content)
        Segment.r_server.lpush(Segment.REDIS_KEY, new_seg.seg_id)

        return new_seg

    @staticmethod
    def open(seg_id):
        if seg_id in Segment.get_all_seg_ids():
            return Segment(seg_id)
        else:
            return Segment.new()

    @staticmethod
    def save():
        Segment.r_server.bgsave()

        filepath = Segment.FILEPATH
        with open(filepath, mode='a') as f:
            collection = Segment.get_collection()
            for seg in collection:
                f.write(seg.curr_edit)
            Segment.r_server.set(Segment.FILEPATH_KEY, str(f))

    # properties, listed alphabetically
    @property
    def base_edit(self):
        base_edit = self.edits[0]
        if base_edit != Segment.REDIS_NONE:
            return base_edit
        else:
            return None

    @property
    def curr_edit(self):
        curr_edit = self.edits[-1]
        if curr_edit != Segment.REDIS_NONE:
            return curr_edit
        else:
            return None

    @property
    def edits(self):
        edits = self.r_server.lrange(self.edits_key, 0, -1)
        decoded = [edit.decode() for edit in edits]
        return decoded

    @property
    def edits_key(self):
        edits_key = Segment.EDITS_KEY + ":" + self.seg_id
        return edits_key

    @property
    def seg_id(self):
        return str(self._seg_id)

    @property
    def id_key(self):
        return Segment.SEG_ID_KEY + ":" + self.seg_id

    @property
    def prev_edit(self):
        prev_edit = self.edits[-2]
        if prev_edit != Segment.REDIS_NONE:
            return prev_edit
        else:
            return None

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
