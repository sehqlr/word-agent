#!/usr/bin/env python3
import random, redis, tempfile, unittest
from collections import deque
from pathlib import Path

from backend import *
from app import app, get_segment

EXCESSIVE = 100
TEST_SEG_ID = "1"
TEST_FILEPATH = "test"

def gen_test_segment():
    #this tries to not to rely on methods I wrote
    #to gen the testing environment
    seg_id = TEST_SEG_ID
    edits_list = ['nil', ''] + [str(n) for n in range(0, EXCESSIVE)]
    segment = Segment(seg_id)

    Segment.r_server.set("filepath", TEST_FILEPATH)
    for edit in edits_list:
        Segment.r_server.rpush("edits:"+seg_id, edit)

    Segment.r_server.lpush(Segment.REDIS_KEY, seg_id)

    return segment

class SegmentInstanceTestCase(unittest.TestCase):
    """Test instance methods for Segments"""

    def setUp(self):
        self.seg = gen_test_segment()

    def tearDown(self):
        self.seg.r_server.flushdb()

    def test_properties(self):
        """Test edit-related read-only properties"""
        seg_id = str(TEST_SEG_ID)
        edits = [None, ''] + [str(i) for i in range(0, EXCESSIVE)]
        edits_key = "edits:" + seg_id
        id_key = "file:" + seg_id

        self.assertEqual(self.seg.base_edit, edits[0])
        self.assertEqual(self.seg.curr_edit, edits[-1])

        # nil/None difference between Redis/Python
        self.assertEqual(self.seg.edits, ['nil']+edits[1:])

        self.assertEqual(self.seg.edits_key, edits_key)
        self.assertEqual(self.seg.seg_id, seg_id)
        self.assertEqual(self.seg.id_key, id_key)
        self.assertEqual(self.seg.prev_edit, edits[-2])

    def test_undo_redo(self):
        """Test editing actions undo and redo"""
        edits_deque = deque(self.seg.edits)

        for i in range(1, EXCESSIVE):
            rv = self.seg.undo()
            if rv:
                edits_deque.rotate(1)
            self.assertEqual(self.seg.edits, list(edits_deque))

        for i in range(0, EXCESSIVE):
            rv = self.seg.redo()
            if rv:
                edits_deque.rotate(-1)
            self.assertEqual(self.seg.edits, list(edits_deque))

class SegmentStaticTestCase(unittest.TestCase):
    """Tests Segment static methods"""
    def setUp(self):
        self.seg = gen_test_segment()

    def tearDown(self):
        Segment.r_server.flushdb()

    def test_get_count(self):
        self.assertEqual(str(Segment.get_count()), self.seg.seg_id)

    def test_get_current(self):
        self.assertEqual(Segment.get_current(), self.seg.seg_id)

    def test_get_collection(self):
        collection = Segment.get_collection()
        list_len = Segment.r_server.llen(Segment.REDIS_KEY)
        self.assertEqual(len(collection), list_len)

    def test_new(self):
        pass

    def test_open(self):
        pass

    def test_save(self):
        Segment.save()
        f = Segment.r_server.get(Segment.FILEPATH_KEY)
        path = Path(f)
        self.assertTrue(path.exists())


class WebTestCase(unittest.TestCase):
    """Test case for Flask frontend"""
    def setUp(self):
        self.app = app.test_client()
        gen_test_segment()

    def tearDown(self):
        Segment.r_server.flushdb()

    def test_index(self):
        rv = self.app.get("/")
        b = b'Welcome to the index page'
        self.assertIn(b, rv.data)

    def test_editor(self):
        rv = self.app.get("/editor")
        seg = get_segment()
        b = seg.curr_edit.encode('utf-8')
        self.assertIn(b, rv.data)

    def test_api(self):
        rv = self.app.get("/api")
        b = b'Welcome to the API'
        self.assertIn(b, rv.data)

    def test_add_edit(self):
        rv = self.app.post("/api/add_edit",
                data=dict(text="new edit"),
                follow_redirects=True)
        seg = get_segment()
        b = seg.curr_edit.encode("utf-8")
        self.assertIn(b, rv.data)

    def test_open(self):
        fid = Segment.get_current()
        rv = self.app.get("/api/open?seg_id="+fid, follow_redirects=True)
        b = b'opened file ' + fid.encode("utf-8")
        self.assertIn(b, rv.data)

    def test_undo(self):
        rv = self.app.post("/api/undo", follow_redirects=True)
        b = b'undid: True'
        self.assertIn(b, rv.data)

    def test_redo(self):
        rv = self.app.post("/api/redo", follow_redirects=True)
        b = b'redid: True'
        self.assertIn(b, rv.data)

if __name__ == "__main__":
    unittest.main()
