import os
import tempfile
import difflib
from gi.repository import Gtk

from WordAgent import *

print("Begin editing testing suite")

print("Init Gtk.Builder as bob; adding UI file")
bob = Gtk.Builder()
bob.add_from_file("WordAgentApp.glade")
print(bob)

print("Init text buffer object")
txt_bf = Buffer()
print(txt_bf)

print("Init differ")
diff = Differ()
print(diff)

print("Showing text buffer text property")
print(txt_bf.text)
