#!/usr/bin/env python3
import os
import io
from collections import deque
from difflib import SequenceMatcher, ndiff, restore
from gi.repository import Gtk, Gdk

import py.WordAgent as WA

welcome_message = """
    Welcome to the Word Agent, the novel project management app!

    Features currently in development:
        Cut/Copy/Paste
        New/Open files
        Dialog boxes

    Next Feature in the works:
        Project management

    Future Features:
        Version Control System integration
        Cloud Collaboration with WebRTC
        "Post Production" formatting (Scribus integration?)
"""

# Path Strings
src_path = os.getcwd()
main_glade_file = os.path.join(src_path + "/ui/MainApp.glade")
testing_dir = src_path + "/testing"

# Bob the Builder
bob = Gtk.Builder.new()
bob.add_from_file(main_glade_file)

# SegmentBuffer and associated TextView
bfr = WA.SegmentBuffer(welcome_message)
txt = bob.get_object("editTextView")
txt.set_buffer(bfr)

fdb = WA.FileDatabase()

os.chdir(testing_dir)

bob.connect_signals(WA.SignalHandler(bfr, fdb))

app = bob.get_object("topWindow")
app.show()
Gtk.main()
