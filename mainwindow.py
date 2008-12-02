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

import gtk

from gladewindow import GladeWindow
from canvas import Canvas
from console import PythonConsole
import execution


class MainWindow(GladeWindow):
    glade_file = os.path.join('gui', 'pybotlearn.glade')
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.canvas = Canvas()
        self.canvas.connect('key-press-event', self.on_key)
        self.robot = self.canvas.robot
        execution.robot = self.robot
        self.canvas_sw.add(self.canvas)
        self.console = PythonConsole(execution.namespace)
        self.main_paned.pack2(self.console)
        self.show_all()
        
        self.canvas.get_hadjustment().connect('value-changed', self.on_scroll)
        self.canvas.get_vadjustment().connect('value-changed', self.on_scroll)
    
    def on_up(self, *args):
        self.console.eval('move_up()', True)
        
    def on_down(self, *args):
        self.console.eval('move_down()', True)
        
    def on_right(self, *args):
        self.console.eval('move_right()', True)
    
    def on_left(self, *args):
        self.console.eval('move_left()', True)
        
    def on_key(self, sender, event):
        if event.keyval == gtk.keysyms.Up:
            self.on_up()
            return True
        elif event.keyval == gtk.keysyms.Down:
            self.on_down()
            return True
        elif event.keyval == gtk.keysyms.Left:
            self.on_left()
            return True
        elif event.keyval == gtk.keysyms.Right:
            self.on_right()
            return True
        
    def on_say(self, button):
        text = self.say_textview.get_buffer()
        text = text.get_text(text.get_start_iter(), text.get_end_iter())
        self.console.eval('say(%s)' % repr(text), True)
        
    def on_scroll(self, *args):
        scroll_x = self.canvas.get_hadjustment()
        scroll_y = self.canvas.get_vadjustment()
        
        robot_x = self.robot.get_pixel_x()
        robot_y = self.robot.get_pixel_y()
        
        self.hruler.set_range(scroll_x.value, scroll_x.value + scroll_x.page_size, robot_x, self.canvas.width)
        self.vruler.set_range(scroll_y.value, scroll_y.value + scroll_y.page_size, robot_y, self.canvas.height)
