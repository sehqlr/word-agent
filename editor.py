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
	"""A class for maintaining the autosave/diff feature"""

	def __init__(self, text_buffer = None):

		self.text_buffer = text_buffer
		self.ndiffer = difflib.Differ.ndiff()
		self.restorer = difflib.Differ.restore()
		self.save_buffer, self.redo_buffer = [], []

	def get_text(self):
		text_start = text_buffer.get_start_iter()
		text_end = text_buffer.get_end_iter()
		return self.text_buffer.get_text(text_start, text_end)

	def get_diff(self):
		if isinstance(save_buffer[-1], str):
			if isinstance(save_buffer[-2], str):
				first_str = save_buffer.pop()
				second_str = save_buffer.pop()
				return self.ndiffer(first_str, second_str)
		return

	def save_text(self):
		delta = get_diff())
		if delta is None:
			save_buffer.append(get_text())
		else:
			save_buffer.append(delta)
		redo_buffer.clear()
		print("Text Saved!")

	def restore_undo(self):
		# the idea behind this one is to use the restore method
		# to travel back through the deltas. This will also populate the
		# redo list. If you notice above, the redo list gets cleared
		# when the user is making a new save.


class FileDiffBuffer:
	"""Brings the autosave/diff buffer into a file for longer storage"""

if __name__ == "__main__":

