#!/usr/bin/env python3
#  editor.py
#
#  Copyright 2014 Sam Hatfield <sam@gaja-dev>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
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
import tempfile, difflib
import subprocess as sub
from gi.repository import Gtk
from builder import AppBuilder

"""

The main idea behind the undo/redo scheme is to tie it into the autosave
and vcs systems. Each edit to the file creates a delta file that is added
to a "autosave" file genenerated during runtime. When the user commits
changes, this autosave file is not effected. The autosave file is temporary

"""

class AutoDiffBuffer:
	"""A class for maintaining the auto-diff save/commit feature"""

	def __init__(self, temp_file = None, text_buffer = None,
				 text_content_curr = None, text_content_prev = None):
		self.temp_file = temp_file

	def
		self._start = text_buffer.get_start_iter()
		self._end = text_buffer.get_end_iter()

	def open_temp_file(self):
		self.temp_file = tempfile.NamedTemporaryFile(mode='w+')

	def set_text_buffer(self, text_buffer=None):
		if text_buffer == None:
			print("No text buffer specified.")
		else:
			self.text_buffer = text_buffer

	def get_text_state(self)
		return text_buffer.get_text(_start, _end)

	def get_diff(self):
		if self.text_buffer == None:
			print("Call method 'set_text_buffer' first.")
		else:







if __name__ == "__main__":
	builder = Gtk.Builder()
	builder.add_from_file("word-agent.glade")

	text_buffer = Gtk.TextBuffer()
