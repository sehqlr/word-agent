import os
import tempfile
import difflib
from gi.repository import Gtk

from WordAgent import *

bob = Gtk.Builder()
bob.add_from_file("WordAgentApp.glade")

txt_bf = Buffer()
txt_bx = bob.get_object("editorTextBox")
txt_bx.set_buffer(txt_bf)

win = bob.get_object("mainWindow")

diff = Differ()
clrk = FileClerk()
bob.connect_signals(Handler(txt_bf, diff, clrk))

win.show_all()
Gtk.main()
