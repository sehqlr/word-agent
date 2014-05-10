#!/usr/bin/env python3
import os
import io
from collections import deque
from difflib import SequenceMatcher, ndiff, restore
from gi.repository import Gtk, Gdk

import py.WordAgent as WA

if __name__ == "__main__":
    win = WA.MainWindow()
    win.show_all()
    Gtk.main()
