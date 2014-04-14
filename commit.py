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

import subprocess as sub

class WAVersionControl:
	"""A class for version control"""
	vsdir = "/usr/bin/hg"
	def init(self):
		sub.check_call([vsdir, "init"])
	def commit(message = None):
		if message is None:
			sub.check_call([vsdir, "commit"])
		else:
			sub.check_call([vsdir, "commit", "-m", message])
	def status():
		sub.check_call([vsdir, "status"])
	def log():
		sub.check_call([vsdir, "log"])

if __name__ == "__main__":
	print("Nothing to test at this time")
