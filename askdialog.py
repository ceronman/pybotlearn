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

import os

import cairo
import gtk

from gladewindow import GladeWindow
from dialogglobe import draw_dialog_globe, text_size
import config


class AskLayout(gtk.Layout):
    def __init__(self, question):
        super(AskLayout, self).__init__()
        path = os.path.join('gui', 'robot_empty.png')
        self.robot_image = cairo.ImageSurface.create_from_png(path)
        self.connect('expose_event', self.on_expose)
        self.question = question
        
        dummy_context = cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 0,0))
        width, height = text_size(dummy_context, self.question)
        
        width  += 100
        height += 50
        
        self.set_size_request(width, height)

        
    def on_expose(self, widget, event):
        context = self.bin_window.cairo_create()
        
        x = 10
        y = 10
        
        globe_x = 60
        globe_y = 10
        
        context.set_source_surface(self.robot_image, x, y)
        context.paint()
        
        size = config.canvas_grid_size
        
        draw_dialog_globe(context, 10 + size, y + size/2, globe_x, globe_y, self.question)
        
        return True
    
    
class AskDialog(GladeWindow):
    glade_file = glade_file = os.path.join('gui', 'pybotlearn.glade')
    
    def __init__(self, question):
        super(AskDialog, self).__init__()
        self.dialog_box.pack_start(AskLayout(question), True, True)
        self.show_all()
        
    def ask(self):
        self.run()
        buffer = self.textview.get_buffer()
        answer = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter())
        self.destroy()
        return answer
        
