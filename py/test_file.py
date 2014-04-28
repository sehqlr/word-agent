import os
from collections import deque
from difflib import SequenceMatcher, ndiff, restore
from gi.repository import Gtk

from WordAgent import *

text = "Stuff and stuff and stuff and some more stuff"
seg_bfr = SegmentBuffer(text)

os.chdir("/home/sam/Documents/testing")
project = open("test.wa.txt", "w+")

project.write(seg_bfr.fetch_text())
