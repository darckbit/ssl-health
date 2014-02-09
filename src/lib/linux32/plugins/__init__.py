#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:         __init__.py
# Purpose:      PluginsFinder class for the SSLyze plugins package.
#
# Author:       alban, aaron
#
# Copyright:    2012 SSLyze developers
#
#   SSLyze is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 2 of the License, or
#   (at your option) any later version.
#
#   SSLyze is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with SSLyze.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------


import os
import sys
import inspect
from imp import load_module, find_module

import plugins
import plugins.PluginBase


class PluginsFinder:
    
    
    def __init__(self):
        """
        Opens the plugins folder and looks at every .py module in that directory.
        Finds available plugins by looking at any class defined in those modules
        that implements the PluginBase abstract class.
        Returns a list of plugin classes.
        """
        self._plugin_classes = set([])
        self._commands = {}
        
        plugin_dir = plugins.__path__[0]
        full_plugin_dir = os.path.join(sys.path[0], plugin_dir)
    
        if os.path.exists(full_plugin_dir):
            for (root, dirs, files) in os.walk(full_plugin_dir):
                del dirs[:] # Do not walk into subfolders of the plugin directory
                # Checking every .py module in the plugin directory
                for source in (s for s in files if s.endswith(".py")):
                    module_name = os.path.splitext(os.path.basename(source))[0]
                    full_name = os.path.splitext(source)[0].replace(os.path.sep,'.')
    
                    try: # Try to import the plugin package
                    # The plugin package HAS to be imported as a submodule
                    # of module 'plugins' or it will break windows compatibility
                        (file, pathname, description) = \
                            find_module(full_name, plugins.__path__)
                        module = load_module('plugins.' + full_name, file,
                                                pathname, description)
                    except Exception as e:
                        print '  ' + module_name + ' - Import Error: ' + str(e)
                        continue
    
                    # Check every declaration in that module
                    for name in dir(module):
                        obj = getattr(module, name)
                        if inspect.isclass(obj):
                            # A class declaration was found in that module
                            # Checking if it's a subclass of PluginBase
                            # Discarding PluginBase as a subclass of PluginBase
                            if obj != plugins.PluginBase.PluginBase:
                                if issubclass(obj, plugins.PluginBase.PluginBase):
                                    # A plugin was found, keep it
                                    self._plugin_classes.add(obj)
                                    
                                    # Store the plugin's commands
                                    for cmd in obj.get_interface().get_commands_as_text():
                                        self._commands[cmd] = obj
                                    
                                    
    def get_plugins(self):
        return self._plugin_classes

    
    def get_commands(self):
        return self._commands
        
