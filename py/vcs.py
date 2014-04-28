#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  vcs.py
#
#  Copyright 2014 Sam Hatfield <samuel.e.hatfield@gmail.com>
#
#  This module is for integrated version control system functionality.
#  As of now, it supports calls to hg (Mercurial) using subprocess calls.

import subprocess as sub

class WAVersionControlSystem:
	"""A class for version control"""
	vsdir = "/usr/bin/hg"
	def init(self):
		try:
			sub.check_call([vsdir, "init"])
		except IOError as err:
    			print("I/O error: {0}".format(err))
	def commit(message = None):
		if message is None:
			sub.check_call([vsdir, "commit"])
		else:
			sub.check_call([vsdir, "commit", "-m", message])
	def status():
		sub.check_call([vsdir, "status"])
	def log():
		sub.check_call([vsdir, "log"])

# If the module is being run from the command line by itself, then it is
# for debugging purposes. Therefore, this part should contain unit testing

if __name__ == "__main__":
	print("Nothing to test at this time")
