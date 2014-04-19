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

class AutoDiffBuffer:
	"""A class for maintaining the autosave/diff feature"""

	def __init__(self, text_buffer = None):

		self.text_buffer = text_buffer
		self.ndiffer = difflib.ndiff
		self.restorer = difflib.restore
		self.save_buffer, self.redo_buffer = [], []

	def get_edit(self):
		text_start = self.text_buffer.get_start_iter()
		text_end = self.text_buffer.get_end_iter()
		return self.text_buffer.get_text(text_start, text_end, False)

	def get_diff(self):
		if self.save_buffer is not None:
			newer_edit = self.save_buffer[-1]
			older_edit = self.save_buffer[-2]
			if isinstance(newer_edit, str) and isinstance(older_edit, str):
				return self.ndiffer(newer_edit, older_edit)
		return None

	def save_edit(self):
		if len(self.save_buffer) < 2:
			self.save_buffer.append(self.get_edit())
		else:
			delta = self.get_diff()
			if delta is None:
				self.save_buffer.append(get_edit())
			else:
			# this keeps the two top elements text buffer strings
				self.save_buffer[-2] = delta
				self.save_buffer.append(self.get_edit())
				self.redo_buffer.clear()
		self.text_buffer.set_modified(False)
		print("Text Saved!")

	def restore_edit(self):
		old_edit = self.save_buffer[-1]
		if isinstance(old_edit, str) is False:
			old_edit = self.restore_diff(old_edit)
		self.text_buffer.set_text(old_edit, len(old_edit))

	def restore_diff(self, diff):
		return ''.join(self.restorer(diff, 1))

	def undo_edit(self):
		self.redo_buffer.append(self.save_buffer.pop())
		self.restore_edit()
		print("Undo complete")

	def redo_edit(self):
		self.save_buffer.append(self.redo_buffer.pop(0))
		self.restore_edit()
		print("Redo complete")


class FileDiffBuffer:
	"""Brings the autosave/diff buffer into a file for longer storage"""
	pass

if __name__ == "__main__":
	editList = ["I'm a sentence.",
				"I'm the sentence.",
				"I've written the sentence.",
				"We've written a sentence.",
				"We've written a story."]

	textBox = Gtk.TextBuffer()
	ad = AutoDiffBuffer(textBox)

	for e in editList:
		print("Current edit: " + e)
		textBox.set_text(e, len(e))
		ad.save_edit()


	for i in [1, 2, 3]:
		print("UNDO #" + str(i))
		print("autoDiffer.save_buffer before:" + str(ad.save_buffer[-1]))
		ad.undo_edit()
		print("autoDiffer.get_text: " + ad.get_edit())
		print("autoDiffer.save_buffer after: " + str(ad.save_buffer[-1]))
		print("autoDiffer.redo_buffer: " + str(ad.redo_buffer[-1]))

	print("End of testing")
