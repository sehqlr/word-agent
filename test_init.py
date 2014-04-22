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
txt_bf = Buffer()
txt_bx = bob.get_object("editorTextBox")
txt_bx.set_buffer(txt_bf)
print(txt_bf)
print(txt_bx)

print("Init main window")
win = bob.get_object("mainWindow")
print(win)

print("Init differ and file_clerk")
diff = Differ()
clrk = FileClerk()
print(diff)
print(clrk)

print("Connecting signals from Handler")
bob.connect_signals(SignalHandler(txt_bf, diff, clrk))
