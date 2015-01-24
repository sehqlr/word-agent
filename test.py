#!/usr/bin/env python3
import redis, unittest
from backend import Segment
from app import app

TEST_EDITS_LIST = ["first", "second", "third", "fourth", "fifth"]

class SegmentEditingTestCase(unittest.TestCase):
    """Test editing methods for Segments"""

    def setUp(self):
        self.seg = Segment.new(content="zeroth")
        for edit in TEST_EDITS_LIST:
            self.seg.add_edit(edit)
        self.median = (len(self.seg.edits) // 2) + 1
        self.mix = self.seg.edits[self.median:] + self.seg.edits[:self.median]

    def tearDown(self):
        self.seg.r_server.flushdb()

    def test_properties(self):
        """Test edit-related read-only properties"""
        self.assertEqual(self.seg.base_edit, None)
        self.assertEqual(self.seg.prev_edit, 'fourth')
        self.assertEqual(self.seg.curr_edit, 'fifth')

    def test_undo_redo(self):
        """Test editing actions undo and redo"""
        undo_case = self.mix
        redo_case = self.seg.edits

        for i in range(1, self.median):
            self.seg.undo()
        self.assertEqual(self.seg.edits, undo_case)

        for i in range(0, self.median):
            self.seg.redo()
        self.assertEqual(self.seg.edits, redo_case)

    def test_undo_redo_excessive(self):
        """Test excessive undo/redo actions"""
        undo_case = self.seg.edits[2:] + self.seg.edits[:2]
        redo_case = self.seg.edits
        excessive = 100

        for i in range(1, excessive):
            self.seg.undo()
        self.assertEqual(self.seg.edits, undo_case)

        for i in range(1, excessive):
            self.seg.redo()
        self.assertEqual(self.seg.edits, redo_case)

    def test_edit_truncation(self):
        case = self.seg.edits[0:self.median]
        case.append("sixth")

        for i in range(1, self.median):
            self.seg.undo()
        self.seg.add_edit("sixth")

        self.assertEqual(self.seg.edits, case)

class SegmentRedisTestCase(unittest.TestCase):
    """Tests Segment redis methods"""
    def setUp(self):
        self.segment = Segment.new()

    def tearDown(self):
        Segment.r_server.flushdb()

    def test_redis_ping(self):
        rv = Segment.r_server.ping()
        self.assertTrue(rv)

    def test_save(self):
        pass

    def test_properties(self):
        self.assertEqual(self.segment.edits_key, "edits:1")
        self.assertEqual(self.segment.file_id, "1")
        self.assertEqual(self.segment.filename, "default_seg")
        self.assertEqual(self.segment.redis_key, "file:1")

    def test_open(self):
        Segment.r_server.sadd("files", 2)
        segment2 = Segment.open(2)
        self.assertIsInstance(segment2, Segment)

    def test_current(self):
        self.assertEqual(Segment.current(), self.segment.file_id)

class WebTestCase(unittest.TestCase):
    """Test case for Flask frontend"""
    def setUp(self):
        self.app = app.test_client()
        self.segment = Segment.new()

    def tearDown(self):
        Segment.r_server.flushdb()

    def test_edits_list(self):
        edits_list = self.segment.edits
        self.assertGreater(len(edits_list), 0)

    def test_index(self):
        rv = self.app.get("/")
        b = b'Welcome to the index page'
        self.assertIn(b, rv.data)

    def test_editor(self):
        rv = self.app.get("/editor")
        b = self.segment.curr_edit.encode('utf-8')
        self.assertIn(b, rv.data)

    def test_api(self):
        rv = self.app.get("/api")
        b = b'Welcome to the API'
        self.assertIn(b, rv.data)

    def test_add_edit(self):
        rv = self.app.post("/api/add_edit",
                data=dict(text="new edit"),
                follow_redirects=True)
        b = self.segment.curr_edit.encode("utf-8")
        self.assertIn(b, rv.data)

if __name__ == "__main__":
    unittest.main()
