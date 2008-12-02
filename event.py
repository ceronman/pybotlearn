# -*- coding: utf-8 -*-

# Twist'em All !
# Author: Manuel Cerón <ceronman@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

class Event(object):
	
	def __init__(self):
		self.handlers = []
		
	def add_handler(self, handler):
		self.handlers.append(handler)
		
	def remove_handler(self, handler):
		self.handlers.remove(handler)
		
	def call(self, *args, **kwargs):
		for handler in self.handlers:
			handler(*args, **kwargs)
