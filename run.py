import os
import tempfile
import difflib
from gi.repository import Gtk

from WordAgent import *

print("Running as main")
bob = Gtk.Builder()
bob.add_from_file("WordAgentApp.glade")
txt = bob.get_object("segmentBuffer")
win = bob.get_object("mainWindow")
diff = Differ(txt)
filr = Filer()
bob.connect_signals(Handler(diff, filr))

print("Showing main window")
win.show_all()

print("Calling Gtk.main")
Gtk.main()
