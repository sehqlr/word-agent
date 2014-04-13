#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  word-agent.py
#
#  Copyright 2014 Sam Hatfield <samuel.e.hatfield@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from gi.repository import Gtk
import commit, functions

def launchWindow(self, window):
	if type(window) is Gtk.Window:
		win = builder.get_object(window)
	else: win = None
	return win

def main():
	path = '/home/sam/Development/word-agent'
	handlers = {
		"gtk_main_quit": Gtk.main_quit,
		"on_compositionButton_clicked": launchWindow("compositionWindow"),
		"on_vcsButton_clicked": launchWindow("vcsWindow")
	}

	builder = Gtk.Builder()
	builder.add_from_file(path + "word-agent.glade")
	builder.connect_signals(handlers)

	wavc = WAVersionControl()

	app = builder.get_object("mainWindow")
	app.show_all()
	app.maximize()

	Gtk.main()
	return 0

if __name__ == "__main__":
	main()
