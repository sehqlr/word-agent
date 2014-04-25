import os
import tempfile
import difflib
from gi.repository import Gtk

from WordAgent import *

print("Begin editing testing suite")

edits = ["I'm a different starting buffer",
"I've changed the buffer",
"I'm going to write a story",
"Once upon a time...",
"Once upone a time, in a land far far away...",
"Macabre murder mysteries make more money.",
"Macabre murder mysteries make much more money!",
"Macabre murder mysteries make much more money!"]

seg_bfr = SegmentBuffer()
print("Initialized {}".format(seg_bfr))

diff = SequenceDiffer()
print("Initialized {}".format(diff))

clerk = FileClerk()
print("Initialized {}".format(clerk))

signal = SignalHandler(seg_bfr, diff, clerk)
print("Initialized {}".format(signal))

print("Starting to loop through edits.")
edits = enumerate(edits)
for e in edits:
    num, txt = e
    print("LOOP #{}: ".format(num))
    print("Text of edit: {}".format(txt))
    print("BEFORE: seg_bfr.copy is {}".format(seg_bfr.copy))
    print("BEFORE: seg_bfr.undos is {}".format(seg_bfr.undos))
    print("BEFORE: seg_bfr.redos is {}".format(seg_bfr.redos))
    print("Saving edit to save buffer")
    seg_bfr.set_text(txt, len(txt))
    #~ ratio = diff.set_seqs(txt, seg_bfr.props.text)
    #~ print("Sequence Matcher quick_ratio: {}".format(ratio))
    signal.on_segmentBuffer_modified_changed()
    print("AFTER: seg_bfr.curr is {}".format(seg_bfr.copy))
    print("AFTER: seg_bfr.undos is {}".format(seg_bfr.undos))
