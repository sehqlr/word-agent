import os
import tempfile
import difflib
from gi.repository import Gtk

from WordAgent import *

print("Begin initialization testing suite")

print("Init Gtk.Builder as bob; adding UI file")
bob = Gtk.Builder()
bob.add_from_file("WordAgentApp.glade")
print(bob)

print("Init text buffer and text view objects")
seg_bfr = SegmentBuffer()
txt_dis = bob.get_object("editorTextBox")
txt_dis.set_buffer(seg_bfr)
print(seg_bfr)
print(txt_dis)

print("Init main window")
win = bob.get_object("mainWindow")
print(win)

print("Init differ and file_clerk")
diff = SequenceDiffer()
clrk = FileClerk()
print(diff)
print(clrk)

print("Connecting signals from Handler")
bob.connect_signals(SignalHandler(txt_bf, diff, clrk))
