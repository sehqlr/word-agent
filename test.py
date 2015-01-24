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
        self.median = (len(self.seg.edits) // 2) + 1
        self.mix = self.seg.edits[self.median:] + self.seg.edits[:self.median]

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
        #TODO: add in asserts that aren't dumb

    def tearDown(self):
        self.seg.r_server.flushdb()

if __name__ == "__main__":
    unittest.main()

