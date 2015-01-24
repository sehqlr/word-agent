import redis, unittest
from backend import *
"""
Testing module for word agent's backend
"""

TEST_EDITS_LIST = ["first", "second", "third", "fourth", "fifth"]

class SegmentEditTestCase(unittest.TestCase):
    """Test editing methods for Segments"""

    def setUp(self):
        self.seg = Segment.new(content="zeroth")
        for edit in TEST_EDITS_LIST:
            self.seg.add_edit(edit)
        self.test_edits = self.seg.edits

    def test_properties(self):
        self.assertEqual(self.seg.base_edit, None)
        self.assertEqual(self.seg.prev_edit, 'fourth')
        self.assertEqual(self.seg.curr_edit, 'fifth')

    def test_undo(self):
        test_case = self.test_edits[:-1]
        test_case.append("nil")
        for i in range(0, len(self.test_edits)):
            self.seg.undo()
            #TODO: add in asserts for base, prev, and curr edits
        self.assertEqual(self.seg.edits, self.test_edits)
        self.assertNotEqual(self.seg.edits, test_case)
        #TODO: add in asserts that aren't dumb

    def test_redo(self):
        test_case = self.test_edits[1:]
        test_case.append("nil")
        for i in range(0, len(self.test_edits)):
            self.seg.redo()
        self.assertEqual(self.seg.edits, self.test_edits)
        self.assertNotEqual(self.seg.edits, test_case)
        #TODO: add in asserts that aren't dumb

    def test_edit_truncation(self):
        mid = len(self.test_edits)//2
        test_case = self.test_edits[mid:] + self.test_edits[:mid]
        for i in range(0, mid):
            self.seg.redo()
        self.assertEqual(self.seg.edits, self.test_edits)
        self.assertNotEqual(self.seg.edits, test_case)
        #TODO: add in asserts that aren't dumb

    def tearDown(self):
        self.seg.r_server.flushdb()

if __name__ == "__main__":
    unittest.main()

