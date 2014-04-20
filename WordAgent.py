#!/usr/bin/env python3

import os
import tempfile
import difflib
from gi.repository import Gtk

class Handler:
	"""Handles signals from user events"""

	def __init__(self, segment_buffer, differ, file_clerk):
		self.segment_buffer = segment_buffer
		self.differ = differ
		self.file_clerk = file_clerk

	def gtk_main_quit(self, *args):
		Gtk.main_quit(*args)

	def	on_segmentBuffer_modified_changed(self, widget):
		self.segment_buffer.save_edit()

	def on_undoButton_clicked(self, widget):
		self.segment_buffer.undo_edit()

	def	on_redoButton_clicked(self, widget):
		self.segment_buffer.redo_edit()

	def on_saveButton_clicked(self, widget):
		self.segment_buffer.save_edit(self.differ)


class Buffer(Gtk.TextBuffer):
	"""Extends text buffer to include version lists"""
	def __init__(self):
		Gtk.TextBuffer.__init__(self)
		self.diffs = []
		self.redos = []
		self.saves = []

		self.message = """
	Welcome to the Word Agent, the novel project management app!

	Features currently in development:
		Undo/Redo
		File IO

	Next Feature in the works:
		Project management
		"Post Production" formatting (Scribus integration?)

	Future Features:
		Version Control System integration
		Cloud Collaboration with WebRTC
"""
		self.text = self.set_text(self.message, len(self.message))
		self.add_save()

	def add_save(self):
		self.saves.append(self.text)

	def pop_save(self, index=-1):
		try:
			return self.saves.pop(index)
		except IndexError:
			print("{}.saves list is empty".format(self))

	def add_diff(self, differ, str1, str2):
		self.diffs.append(differ.generate_diff(str1, str2))

	def pop_diff(self, index=-1):
		try:
			return self.diff.pop(index)
		except IndexError:
			print("{}.diff list is empty".format(self))

	def enque_redo(self):
		"""Pops element from saves, enques it to redos"""
		self.redos.append(self.pop_save())

	def deque_redo(self):
		"""Pops redo from the front, as a queue"""
		return self.redos.pop(0)

	def save_edit(self, differ):

		if len(self.saves) <= 2:
			self.add_save()

		else:
			differ.set_seqs(self.text, self.saves[-1])
			ratio = differ.quick_ratio()

			if ratio is not 1.0:
				self.add_save()
				self.redos.clear

	def undo_edit(self):
		self.enque_redo()
		self.text = self.saves[-1]

	def redo_edit(self):
		self.add_save()
		redo = self.deque_redo()
		self.text = redo

class Differ(difflib.SequenceMatcher):
	"""Generates deltas and compares strings with difflib"""
	def __init__(self):
		difflib.SequenceMatcher.__init__(self)
		self.ndiff = difflib.ndiff
		self.restore = difflib.restore

	def generate_diff(self, older='', newer=''):
		try:
			return self.ndiff(newer, older)
		except TypeError:
			print("generate_diff inputs must be strings")

	def restore_diff(self, diff, which):
		return ''.join(self.restore(diff, which))



class FileClerk:
	"""The class for saving files"""
	pass
