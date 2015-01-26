#!/usr/bin/env python3
import random, redis, unittest
from collections import deque
from pathlib import Path

from backend import *
from app import app, get_segment

EXCESSIVE = 100
TEST_FILE_ID = "0"
TEST_FILE_NAME = "test"

def gen_test_segment():
    fid = TEST_FILE_ID
    fname = TEST_FILE_NAME
    edits_list = [str(n) for n in range(0, EXCESSIVE)]
    segment = Segment(file_id=fid)

    Segment.r_server.set("file:"+fid, fname)
    for edit in edits_list:
        Segment.r_server.rpush("edits:"+fid, edit)
    Segment.r_server.set("count", fid)
    return segment

class SegmentEditingTestCase(unittest.TestCase):
    """Test editing methods for Segments"""

    def setUp(self):
        self.seg = gen_test_segment()

    def tearDown(self):
        self.seg.r_server.flushdb()

    def test_properties(self):
        """Test edit-related read-only properties"""
        case = [None] + [str(i) for i in range(0, EXCESSIVE)]
        self.assertEqual(self.seg.base_edit, case[0])
        self.assertEqual(self.seg.prev_edit, case[-2])
        self.assertEqual(self.seg.curr_edit, case[-1])

    def test_edits_list(self):
        self.assertGreater(len(self.seg.edits), 0)

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

    def test_edit_truncation(self):
        """Tests to ensure that edits list gets trimmed"""
        #FAILING TEST
        median = EXCESSIVE//2
        case = self.seg.edits[:median] + [str(EXCESSIVE+1)]

        for i in range(0, median+1):
            self.seg.undo()
        self.seg.add_edit(EXCESSIVE+1)

        self.assertEqual(self.seg.edits, case)

class SegmentRedisTestCase(unittest.TestCase):
    """Tests Segment redis methods"""
    def setUp(self):
        self.seg = gen_test_segment()

    def tearDown(self):
        Segment.r_server.flushdb()

    def test_redis_ping(self):
        rv = Segment.r_server.ping()
        self.assertTrue(rv)

    def test_save(self):
        rv = Segment.save(0)
        path = Path(rv)
        self.assertTrue(path.exists())

    def test_properties(self):
        fid = str(TEST_FILE_ID)
        case_edits_key = "edits:" + fid
        case_redis_key = "file:" + fid
        self.assertEqual(self.seg.edits_key, case_edits_key)
        self.assertEqual(self.seg.file_id, fid)
        self.assertEqual(self.seg.filename, TEST_FILE_NAME)
        self.assertEqual(self.seg.redis_key, case_redis_key)

    def test_current(self):
        self.assertEqual(Segment.current(), self.seg.file_id)

class WebTestCase(unittest.TestCase):
    """Test case for Flask frontend"""
    def setUp(self):
        self.app = app.test_client()
        self.seg = gen_test_segment()

    def tearDown(self):
        Segment.r_server.flushdb()

    def test_index(self):
        rv = self.app.get("/")
        b = b'Welcome to the index page'
        self.assertIn(b, rv.data)

    def test_editor(self):
        seg = get_segment()
        rv = self.app.get("/editor")
        b = seg.curr_edit.encode('utf-8')
        self.assertIn(b, rv.data)

    def test_api(self):
        rv = self.app.get("/api")
        b = b'Welcome to the API'
        self.assertIn(b, rv.data)

    def test_add_edit(self):
        seg = get_segment()
        rv = self.app.post("/api/add_edit",
                data=dict(text="new edit"),
                follow_redirects=True)
        b = seg.curr_edit.encode("utf-8")
        self.assertIn(b, rv.data)

    def test_open(self):
        fid = Segment.current()
        rv = self.app.get("/api/open?file_id=0", follow_redirects=True)
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
