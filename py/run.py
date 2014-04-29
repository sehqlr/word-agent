#!/usr/bin/env python3
import os

from WordAgent import *

welcome_message = """
    Welcome to the Word Agent, the novel project management app!

    Features currently in development:
        Cut/Copy/Paste
        New/Open files
        GUI building methods

    Next Feature in the works:
        Project management
        "Post Production" formatting (Scribus integration?)

    Future Features:
        Version Control System integration
        Cloud Collaboration with WebRTC
"""

bob = Gtk.Builder.new()
bob.add_from_file("../ui/MainApp.glade")

seg_bfr = SegmentBuffer(welcome_message)
txt_box = bob.get_object("editTextView")
txt_box.set_buffer(seg_bfr)

os.chdir("/home/sam/Documents/testing")
project_name = "default.wa.txt"

bob.connect_signals(SignalHandler(seg_bfr, project_name))

app = bob.get_object("topWindow")
app.show()
Gtk.main()
