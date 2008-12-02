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

from gettext import gettext as _
import gtk
from gtk import glade
from gtk import gdk
import gobject

class GladeWindow(object):
	glade_file = ''
	
	def __init__(self):
		root = self.__class__.__name__
		filename = self.__class__.glade_file
		self.__dict__['_glade'] = glade.XML(filename, root)
		self.__dict__['_window'] = self._glade.get_widget(root)
		self._glade.signal_autoconnect(self)
		
	def __getattr__(self, name):
		widget = self._glade.get_widget(name)
		if widget is not None:
			return widget
		
		return getattr(self._window, name)
		
	def __setattr__(self, name, value):
		if hasattr(self._window, name):
			setattr(self._window, name, value)
		else:
			self.__dict__[name] = value
			
	def show_error(self, message):
		dialog = gtk.MessageDialog(self._window, 
								gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
								gtk.MESSAGE_ERROR,
								gtk.BUTTONS_OK,
								)
		dialog.set_title(_('Error'))
		dialog.set_markup(message)
		response = dialog.run()
		dialog.destroy()
		return response
	
	def gtk_main_quit(self, *args):
		gtk.main_quit()
		
	def on_delete_event(self, *args):
		self.destroy()
		
	def set_watch_cursor(self):
		self._window.window.set_cursor(gdk.Cursor(gdk.WATCH))
		
	def set_normal_cursor(self):
		self._window.window.set_cursor(None)
		
		
def threaded(function):
	def substitute(*args, **kwargs):
		gobject.idle_add(function, *args, **kwargs)
		
	return substitute

def add_text_column_to_treeview(treeview, title, field_id, is_float=False):
	renderer = gtk.CellRendererText()
	column = gtk.TreeViewColumn(title, renderer, text=field_id)
	column.set_sort_column_id(field_id)
	if is_float:
		def celldatafunction(column, cell, model, iter, user_data=None):
			cell.props.text = '%.2f' % model[iter][field_id]
		column.set_cell_data_func(renderer, celldatafunction)
	treeview.append_column(column)
	
def init_treeview(treeview, *args):
	model = gtk.ListStore(*args)
	treeview.set_model(model)
	
def init_text_combobox(combobox, item_list, active=0):
	model = gtk.ListStore(str)
	for venue in item_list:
		model.append([venue])
		
	combobox.set_model(model)	
	cell = gtk.CellRendererText()
	combobox.pack_start(cell)
	combobox.add_attribute(cell, 'text', 0)
	combobox.set_active(active)

