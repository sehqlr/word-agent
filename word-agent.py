#!/usr/bin/env python3

import os
import tempfile
import difflib
from gi.repository import Gtk

class Builder(Gtk.Window):
	"""Houses handler calls and other things"""

	def __init__(self):
		Gtk.Window.__init__(self, title="Word Agent")
		self.sig_msg = "Signal recieved: "
		self.src_path = "/home/sam/Development/word-agent/"
		self.usr_path = "/home/sam/Documents/testing/"
		self.main_window_file = self.src_path + "WordAgentApp.glade"

	def signal_message(self, signal):
		print(self.sig_msg + signal)

	def set_interface(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.main_window_file)
		print("Interface initialized")

	def set_signals(self, handler):
		self.builder.connect_signals(handler)
		print("Signals initialized")

	def set_main_window(self):
		self.main_window = self.builder.get_object("mainWindow")
		print("Main Window initialized")

	def set_buffers(self):
		self.text_buffer = self.builder.get_object("segmentBuffer")
		self.diff_buffer = AutoDiffBuffer(self.text_buffer)
		print("Buffers initialized")


class AppHandler:

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


def main(self):
	print("Running as main")
	mainApp = MainApp()
	mainApp.set_interface()
	mainApp.set_signals(AppHandlerandler())
	mainApp.set_buffers()
	mainApp.set_main_window()

	os.chdir(mainApp.usr_path)
	print("Changed working directory to " + mainApp.usr_path)

	mainApp.main_window.show()
	print("Showing main window")

	print("Calling Gtk.main")
	Gtk.main()

if __name__ is "__main__":
	main()
