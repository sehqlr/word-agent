#!/usr/bin/env python3
import os
import io
from collections import deque
from difflib import SequenceMatcher, ndiff, restore
from gi.repository import Gtk, Gdk

import py.WordAgent as WA

# Path Strings
src_path = os.getcwd()
main_glade_file = os.path.join(src_path + "/ui/MainApp.glade")
testing_dir = src_path + "/testing"

# Bob the Gtk.Builder
bob = Gtk.Builder.new()
bob.add_from_file(main_glade_file)

# SegmentBuffer and associated TextView
txt = bob.get_object("editTextView")
bfr = WA.SegmentBuffer(text_view=txt)
txt.set_buffer(bfr)

pf = open("untitled.wa.txt", "w")

bob.connect_signals(WA.SignalHandler(bfr, pf))

app = bob.get_object("topWindow")
app.show()
Gtk.main()
