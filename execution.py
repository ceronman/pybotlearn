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

from event import Event

namespace = {}
robot = None

on_command_executed = Event()

def format(name, *args, **kwargs):
    args = ( repr(arg) for arg in args )
    args = ','.join(args)
    kwargs = ('%s=%s' % (name, kwargs[name]) for name in kwargs)
    kwargs = ','.join(kwargs)
    kwargs = (', ' + kwargs) if len(kwargs) > 0 else ''
            
    function_text = '%s (%s%s)' % (name, args, kwargs)
    return function_text

def execute_command(command):
    exec command in namespace

def robot_command(method):
    name = method.__name__
    def unbound_method(*args, **kwargs):
        ret_val = method(robot, *args, **kwargs)
        on_command_executed.call(format(name, *args, **kwargs))
        return ret_val
        
    namespace[name] = unbound_method
        
    return method
        
