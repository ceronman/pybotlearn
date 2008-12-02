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

import math
import pangocairo

class Point2D(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __sub__(self, other):
        return Point2D(self.x - other.x, self.y - other.y)
    def __add__(self, other):
        return Point2D(self.x - other.x, self.y - other.y)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
        
class Corner (Point2D):
    def __init__(self, x, y, round):
        super(Corner, self).__init__(x, y)
        self.round = round
        
class TopLeftCorner(Corner):        
    def get_round1(self):
        return Point2D(self.x, self.y + self.round)
    def get_round2(self):
        return Point2D(self.x + self.round, self.y,)
    
class TopRightCorner(Corner):        
    def get_round1(self):
        return Point2D(self.x - self.round, self.y)
    def get_round2(self):
        return Point2D(self.x, self.y + self.round)
    
class BottomRightCorner(Corner):        
    def get_round1(self):
        return Point2D(self.x, self.y - self.round)
    def get_round2(self):
        return Point2D(self.x - self.round, self.y)
    
class BottomLeftCorner(Corner):        
    def get_round1(self):
        return Point2D(self.x + self.round, self.y)
    def get_round2(self):
        return Point2D(self.x, self.y - self.round)
    
def distance(p1, p2):
    p = p1 - p2
    return math.sqrt(p.x**2 + p.y**2)

def text_size(context, text):
    context = pangocairo.CairoContext(context)
    pango_layout = context.create_layout()
    pango_layout.set_text(text)
    return pango_layout.get_pixel_size()

def draw_dialog_globe(context, origin_x, origin_y, x, y, text, background=(0,1,0, 0.5), foreground=(0,0,0,1), round=10):
    context = pangocairo.CairoContext(context)
    pango_layout = context.create_layout()
    pango_layout.set_text(text)
    margin = 10
    
    width, height = pango_layout.get_pixel_size()
    width = max(50, width + margin * 2)
    height = height + margin * 2
       
    origin = Point2D(origin_x, origin_y)
    
    topleft = TopLeftCorner(x, y, round)
    topright = TopRightCorner(x+width, y, round)
    bottomright = BottomRightCorner(x+width, y+height, round)
    bottomleft = BottomLeftCorner(x, y+height, round)
    
    corners = [topleft, topright, bottomright, bottomleft]
    
    rounds_corner = {}
    for c in corners:
        rounds_corner[c.get_round1()] =  c
        rounds_corner[c.get_round2()] =  c
        
    rounds = rounds_corner.keys()
    distances = list(distance(r, origin) for r in rounds)
    distances_round = dict(zip(distances, rounds))
    nearest_round = distances_round[min(distances)]
    nearest_corner = rounds_corner[nearest_round]
    
    def walk(corners, start_from, clockwise):
        if not clockwise:
            corners.reverse()
        sequence = range(len(corners))
        start = corners.index(start_from)
        sequence = sequence[start:] + sequence[:start]
        for i in sequence:
            yield corners[i]
          
    clockwise = nearest_round == nearest_corner.get_round1()
    
    context.save()
    context.set_line_width(1)
    context.move_to(origin.x, origin.y)
    for corner in walk(corners, nearest_corner, clockwise):
        r1 = corner.get_round1() if clockwise else corner.get_round2()
        r2 = corner.get_round2() if clockwise else corner.get_round1()
        context.line_to(r1.x, r1.y)
        context.curve_to(corner.x, corner.y, corner.x, corner.y, r2.x, r2.y)
    nearest_corner.round = corner.round * 3
    final_point = nearest_corner.get_round1() if clockwise else nearest_corner.get_round2()
    context.line_to(final_point.x, final_point.y)
    context.line_to(origin.x, origin.y)
    context.set_source_rgba(*background)
    context.fill_preserve()
    context.set_source_rgba(*foreground)
    context.stroke()
    
    context.move_to(topleft.x + margin, topleft.y + margin)
    context.show_layout(pango_layout)
    context.restore()
    
    
