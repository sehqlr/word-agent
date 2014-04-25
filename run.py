import os
import tempfile
import difflib
from gi.repository import Gtk

from WordAgent import *

welcome_message = """
    Welcome to the Word Agent, the novel project management app!

    Features currently in development:
        Undo/Redo
        File IO

    Next Feature in the works:
        Project management
        "Post Production" formatting (Scribus integration?)

    Future Features:
        Version Control System integration
        Cloud Collaboration with WebRTC
"""

bob = Gtk.Builder()
bob.add_from_file("WordAgentApp.glade")

seg_bfr = SegmentBuffer(welcome_message)
txt_box = bob.get_object("editView")
txt_box.set_buffer(seg_bfr)

win = bob.get_object("mainWindow")
diff = SequenceDiffer()
clrk = FileClerk()

bob.connect_signals(SignalHandler(seg_bfr, diff, clrk))

win.show_all()
Gtk.main()
