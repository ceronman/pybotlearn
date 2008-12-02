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
from gettext import gettext as _

import cairo

import config
from execution import robot_command
from dialogglobe import draw_dialog_globe, text_size
from askdialog import AskDialog

class Robot(object):
    def __init__(self, canvas):
        self.canvas = canvas
        
        path = os.path.join('gui', 'robot_empty.png')
        self.empty_image = cairo.ImageSurface.create_from_png(path)
        
        path = os.path.join('gui', 'robot_full.png')
        self.full_image = cairo.ImageSurface.create_from_png(path)
        
        self.current_image = self.empty_image
        
        self.x = 0
        self.y = 0
        
        self.saying = False
        self.text = ''
        
        self.error_happened = False
        self.error_text = ''
        
        self.warning_happened = False
        self.warning_text = ''
        
    def get_pixel_x(self):
        return self.x * config.canvas_grid_size
    
    def get_pixel_y(self):
        return self.y * config.canvas_grid_size
        
    def draw(self, context):
        context.save()
        context.set_source_surface(self.current_image, self.get_pixel_x(), self.get_pixel_y())
        context.paint()
        
        if self.saying:
            self.draw_dialog(context)
            self.saying = False
            
        if self.error_happened:
            self.draw_error(context)
            self.error_happened = False
            
        if self.warning_happened:
            self.draw_warning(context)
            self.warning_happened = False
            
        context.restore()
        
    @robot_command
    def move_to(self, x, y):
        if x < 0 or y <0:
            self.error(_("I can't move there"))
            return
        self.x = x
        self.y = y
        self.canvas.robot_moved()
        
    @robot_command
    def move_left(self):
        self.move_to(self.x-1, self.y)
    
    @robot_command
    def move_right(self):
        self.move_to(self.x+1, self.y)
    
    @robot_command    
    def move_up(self):
        self.move_to(self.x, self.y-1)
    
    @robot_command
    def move_down(self):
        self.move_to(self.x, self.y+1)
    
    @robot_command  
    def say(self, *args):
        text = ' '.join(str(a) for a in args)
        self.saying = True
        self.text = str(text)
        self.canvas.repaint()
   
    @robot_command     
    def error(self, text):
        self.error_happened = True
        self.error_text = str(text)
        self.canvas.repaint()
        
    @robot_command     
    def warning(self, text):
        self.warning_happened = True
        self.warning_text = str(text)
        self.canvas.repaint()
        
    @robot_command
    def ask(self, question):
        dialog = AskDialog(question)
        return dialog.ask()
    
    def draw_dialog(self, context):
        origin_x, origin_y, globe_x, globe_y = self.good_globe_position(context, self.text)
        draw_dialog_globe(context, origin_x, origin_y, globe_x, globe_y, self.text)
        
    def draw_warning(self, context):
        origin_x, origin_y, globe_x, globe_y = self.good_globe_position(context, self.warning_text)
        draw_dialog_globe(context, origin_x, origin_y, globe_x, globe_y, self.warning_text, (1, 1, 0, 0.5))
        
    def draw_error(self, context):
        origin_x, origin_y, globe_x, globe_y = self.good_globe_position(context, self.error_text)
        draw_dialog_globe(context, origin_x, origin_y, globe_x, globe_y, self.error_text, (1, 0, 0, 0.5))
    
    def good_globe_position(self, context, text):
        size = config.canvas_grid_size
        screen = self.canvas.visible_rect()
        left_margin = self.get_pixel_x()
        right_margin = screen.width - (self.get_pixel_x() + size)
        top_margin = self.get_pixel_y()
        bottom_margin = screen.height - (self.get_pixel_y() + size)
        
        text_width, text_height = text_size(context, text)
        
        if left_margin < right_margin:
            origin_x = self.get_pixel_x() + size
            globe_x = origin_x + size/2
        else:
            origin_x = self.get_pixel_x()
            globe_x = origin_x - size/2 - text_width
        
        if top_margin < bottom_margin:
            origin_y = self.get_pixel_y() + size
            globe_y = origin_y + size/2
        else:
            origin_y = self.get_pixel_y()
            globe_y = origin_y - size - text_height
            
        return origin_x, origin_y, globe_x, globe_y
        
        
    def change_image_to_empty(self):
        self.current_image = self.empty_image
        
    def change_image_to_full(self):
        self.current_image = self.full_image
    
        
    
    
    
