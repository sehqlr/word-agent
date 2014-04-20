#!/usr/bin/env python3

import os
import tempfile
import difflib
from gi.repository import Gtk

class Handler:
	"""Handles signals from user events"""

	def __init__(self, segment_buffer, differ, file_clerk):
		self.segment_buffer = segment_buffer
		self.file_clerk = file_clerk

	def gtk_main_quit(self, *args):
		Gtk.main_quit(*args)

	def	on_segmentBuffer_modified_changed(self, widget):
		self.differ.save_edit()

	def on_undoButton_clicked(self, widget):
		self.differ.undo_edit()

	def	on_redoButton_clicked(self, widget):
		self.differ.redo_edit()

	def on_saveButton_clicked(self, widget):
		self.differ.save_edit()

class Buffer(Gtk.TextBuffer):
	def __init__(self):
		self.diffs = []
		self.redos = []
		self.saves = []

		self.undoing = False

	def add_save(self):
		self.saves.append(self.text)

	def add_diff(self, differ, str1, str2):
		self.diffs.append(differ.get_diff(str1, str2))

	def add_redo(self):
		"""Pops element from saves, pushes it to redos"""
		self.redos.append(self.saves.pop())

	def undo_edit(self):
		self.undoing = True
		self.add_redo()
		self.text = self.saves[-1]



class Differ(difflib.Differ):
	"""Generates deltas using diff functions"""

	def get_diff(self, older, newer):
		try:
			return self.ndiff(newer_edit, older_edit)
		except TypeError:
			print("Inputs must be strings.")

	def restore_diff(self, diff, which):
		return ''.join(self.restore(diff, which))


class FileClerk:
	"""The class for saving files"""
	pass
