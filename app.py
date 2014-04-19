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

class WordAgentMainApp:

	def __init__(self, text_buffer, diff_buffer):
		self.sig_msg = "Signal recieved: "
		self.text_buffer = text_buffer
		self.diff_buffer = diff_buffer

	def signal_message(self, signal):
		print(self.sig_msg + signal)

	def gtk_main_quit(self):
		signal_message("gtk_main_quit")
		Gtk.main_quit()

	def	on_segmentBuffer_modified_changed(self):
		signal_message("on_segmentBuffer_modified_changed")
		self.diff_buffer.save_edit()

	def on_undoButton_clicked(self):
		signal_message("on_undoButton_clicked")
		self.diff_buffer.undo_edit()

	def	on_redoButton_clicked(self):
		signal_message("on_redoButton_clicked")
		self.diff_buffer.redo_edit()

	def	on_editorTextBox_preedit_changed(self):
		signal_message("on_editorTextBox_preedit_changed")

def main():

	builder = AppBuilder()
	builder.add_from_file(builder.mainWindowFile)

	textBuffer = builder.get_object("segmentBuffer")
	textView = builder.get_object("editorTextBox")
	diffBuffer = AutoDiffBuffer(textBuffer)

	mainWindow = builder.get_object("mainWindow")

	os.chdir(builder.getUsrPath())

	builder.connect_signals(handlers)
	mainWindow.show()

	Gtk.main()
	return 0

if __name__ == "__main__":
	main()
