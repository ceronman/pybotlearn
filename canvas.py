import gtk

import config
from robot import Robot

class Canvas(gtk.Layout):
       
    def __init__(self):
        super(Canvas, self).__init__()
        self.connect('expose_event', self.on_expose)
        self.connect('button-press-event', self.on_button)
        self.connect('size-allocate', self.on_allocation)
        self.set_events(gtk.gdk.ALL_EVENTS_MASK)
        self.set_flags(gtk.CAN_FOCUS)
        
        self.set_size(config.canvas_width, config.canvas_height)
        self.set_size_request(config.canvas_width, config.canvas_height)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFFFFF'))
        
        self.width = config.canvas_width
        self.height = config.canvas_height
        
        self.robot = Robot(self)
        
    def set_width(self, value):
        self.width = value
        self.set_size(self.width, self.height)
        
    def set_height(self, value):
        self.height = value
        self.set_size(self.width, self.height)
        
    def on_expose(self, widget, event):
        context = self.bin_window.cairo_create()
        self.draw_grid(context)
        self.robot.draw(context)
        context.stroke()
        return True
    
    def on_allocation(self, widget, allocation):
        if self.width < allocation.width:
            self.set_width(allocation.width)
        if self.height < allocation.height:
            self.set_height(allocation.width)
    
    def on_button(self, widget, event):
        self.grab_focus()
        
    def draw_grid(self, context):
        width = self.width
        height = self.height
        context.save()
        context.set_line_width(1.0)
        context.set_source_rgb(*config.canvas_grid_color)
        x_values = xrange(0, width, config.canvas_grid_size)
        x_values = [value + 0.5 for value in x_values]
        for x in x_values:
            context.move_to(x, 0.0)
            context.line_to(x, height)
            context.stroke()
            
        y_values = xrange(0, height, config.canvas_grid_size)
        y_values = [value + 0.5 for value in y_values]
        for y in y_values:
            context.move_to(0.0, y)
            context.line_to(width, y)
            context.stroke()
            
        context.restore()
        
    def robot_moved(self):
        size = config.canvas_grid_size
        x = self.robot.get_pixel_x()
        y = self.robot.get_pixel_y()
        if (x + size) > self.width:
            self.set_width(x + size)
        if (y + size) > self.height:
            self.set_height(y + size)
        self.repaint()
        self.scroll_to_robot()
        
    def scroll_to_robot(self):
        scroll_x = self.get_hadjustment()
        scroll_y = self.get_vadjustment()
        
        robot_x = self.robot.get_pixel_x()
        robot_y = self.robot.get_pixel_y()
        
        size = config.canvas_grid_size
        
        if robot_x < scroll_x.value:
            scroll_x.value = robot_x
        if robot_x + size > scroll_x.value + scroll_x.page_size:
            scroll_x.value = robot_x + size - scroll_x.page_size
        if robot_y < scroll_y.value:
            scroll_y.value = robot_y
        if robot_y + size > scroll_y.value + scroll_y.page_size:
            scroll_y.value = robot_y + size - scroll_y.page_size
                
    def repaint(self):
        self.queue_draw()
        
    def visible_rect(self):
        x = self.get_hadjustment().value
        y = self.get_vadjustment().value
        width = self.get_hadjustment().page_size
        height = self.get_vadjustment().page_size
        return gtk.gdk.Rectangle(int(x), int(y), int(width), int(height))