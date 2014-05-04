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

# Path Strings
# FIXME: These should not be hard-coded in for just my machine.
src_path = "/home/sam/Development/word-agent/"
main_glade_file = src_path + "ui/MainApp.glade"
module_dir = src_path + "py/"
testing_dir = "/home/sam/Development/testing"

bob = Gtk.Builder.new()
bob.add_from_file(main_glade_file)

seg_bfr = SegmentBuffer(welcome_message)
txt_box = bob.get_object("editTextView")
txt_box.set_buffer(seg_bfr)

os.chdir(testing_dir)
project_name = "default.wa.txt"

bob.connect_signals(SignalHandler(seg_bfr, project_name))

app = bob.get_object("topWindow")
app.show()
Gtk.main()
