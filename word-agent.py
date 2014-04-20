#!/usr/bin/env python3

import os
import tempfile
import difflib
from gi.repository import Gtk

class WordAgent_Handler:
	"""Handles signals from user events"""

	def gtk_main_quit(self, *args):
		Gtk.main_quit(*args)

	def	on_segmentBuffer_modified_changed(self):
		MainApp.diff_buffer.save_edit()

	def on_undoButton_clicked(self):
		MainApp.diff_buffer.undo_edit()

	def	on_redoButton_clicked(self):
		MainApp.diff_buffer.redo_edit()

	def on_editorTextBox_preedit_changed(self):
		print("Preedit Signal")


class WordAgent_DiffBuffer:
	"""Maintains the autosave/diff feature"""

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


class FileIO:
	"""The class for saving files"""
	pass


def main():
	print("Running as main")
	bob = Gtk.Builder()
	bob.add_from_file("WordAgentApp.glade")
	txt = bob.get_object("segmentBuffer")
	win = bob.get_object("mainWindow")
	diff = WordAgent_DiffBuffer()
	bob.connect_signals(WordAgent_Handler())

	os.chdir(bob.usr_path)
	print("Changed working directory to " + bob.usr_path)

	print("Showing main window")
	win.show_all()

	print("Calling Gtk.main")
	Gtk.main()

if __name__ is "__main__":
	main()
