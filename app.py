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

import os
import subprocess as sub
from gi.repository import Gtk
from builder import AppBuilder
from editor import AutoDiffBuffer

def text_buffer_modified(self, diffBuffer):
	print("Preedit text sent to buffer")
	diffBuffer.save_edit()

def print_preedit_signal(self):
	print("Preedit text signal sent")

class WordAgentApp:
	self

def main():

	builder = AppBuilder()
	builder.add_from_file(builder.mainWindowFile)

	textBuffer = builder.get_object("segmentBuffer")
	textView = builder.get_object("editorTextBox")
	diffBuffer = AutoDiffBuffer(textBuffer)

	app = builder.get_object("mainWindow")

	os.chdir(builder.getUsrPath())

	handlers = {
		"gtk_main_quit": Gtk.main_quit,
		"on_segmentBuffer_modified_changed": text_buffer_modified,
		"on_undoButton_clicked": diffBuffer.undo_edit,
		"on_redoButton_clicked": diffBuffer.redo_edit,
		"on_editorTextBox_preedit_changed": print_preedit_signal,
	}


	builder.connect_signals(handlers)
	app.show_all()
	app.maximize()

	Gtk.main()
	return 0

if __name__ == "__main__":
	main()
