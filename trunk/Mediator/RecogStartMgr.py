##############################################################################
# VoiceCode, a programming-by-voice environment
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# (C)2000, David C. Fox
#
##############################################################################

"""abstract class defining interface for an object which receives 
recognition-starting (or onBegin/gotBegin) callbacks, figures out which
application and buffer are active, and tells the GramMgr to activate the
appropriate grammars.
"""

import debug
import string
from Object import Object

import GramMgr


class RecogStartMgr(Object):
    """abstract class defining basic interface for keeping track of 
    target applications and windows, in order to handle
    recognition-starting callbacks

    **INSTANCE ATTRIBUTES**

    *{STR : [STR]}* instance_names -- map from editor application name 
    to currently managed instance names

    *{STR : STR}* instance_apps -- map from editor application instance
    names to the application name

    *{STR : INT}* past_instances -- map from editor application name 
    to number of current and past instances

    *{INT : STR}* windows -- map from currently known windows to
    instance names

    *{STR : [INT]}* instance_windows -- map from instance names to
    currently known windows

    *{STR : AppState}* instances -- map from instance names to
    corresponding AppState interfaces
    
    **CLASS ATTRIBUTES**
    
    *none*
    """

    def __init__(self, **args):
	"""
	**INPUTS**
	
	*none* -- (abstract base class)
	"""
        self.deep_construct(RecogStartMgr,
                            {'instance_names': {}, 'windows': {},
			    'instances': {}, 'instance_windows': {},
			    'instance_apps' : {}, 'past_instances' : {}},
                            args)

    def app_instances(self, app_name = None):
	"""names of application instances being managed
	**INPUTS**
	
	*STR* app_name -- list names of instances corresponding only to
	this application name (or list all instances if app_name is
	None)

	**OUTPUTS**
	
	*[STR]* -- list of names of applications being managed (e.g.
	"Emacs (Win)", "jEdit")
	"""
	if app_name == None:
	    all_instances = []
	    for application in self.app_names():
		all_instances.extend(self.app_instances(application))
	    return all_instances
	if app_name not in self.app_names():
	    return []
	return self.instance_names[app_name]
	
    def app_names(self):
	"""names of applications being managed
	**INPUTS**
	
	*none* 

	**OUTPUTS**
	
	*[STR]* -- list of names of applications being managed (e.g.
	"Emacs (Win)", "jEdit")
	"""
	return self.instance_names.keys()
    
    def known_windows(self, instance = None):
	"""list of windows known to be associated with  a particular
	named application instance.

	**INPUTS**
    
	*STR* instance -- list names of windows corresponding to this
	instance name (or list all known windows if instance is
	None)

	**OUTPUTS**
	
	*[INT]* -- list of window handles
	"""
	if instance == None:
	    all_handles = []
	    for name, handles in self.instance_windows:
		all_handles.extend(handles)
	    return all_handles

	if instance not in self.instance_windows.keys():
	    return []
	return self.instance_windows[instance]

    def new_window(self, instance, window):
	"""add a new window to the list of windows corresponding to an
	editor application instance.

	**INPUTS**

	*STR* instance -- name of the application instance

	*INT* window -- window handle of the window
    
	**OUTPUTS**

	*none*
	"""
	if self.instance_windows.has_key(instance):
	    if window not in self.windows:
		self.windows[window] = instance
		self.instance_windows[instance].append(window)
	    
    def new_instance(self, app_name, app, initial_window = None):
	"""add a new application instance

	**INPUTS**

	*STR* app_name -- name of the application 
	(e.g. "Emacs (Win)", "jEdit")

	*AppState* app --  AppState interface corresponding to the new
	instance

	*INT* initial_window -- window handle of an initial window
	corresponding to the instance
    
	**OUTPUTS**

	*STR* -- name of the application instance.  Necessary
	if you want to add windows to the application in the future.
	"""
	if app_name not in self.app_names():
	    self.instance_names[app_name] = []
	    self.past_instances[app_name] = 0
	n = self.past_instances[app_name]
	new_name = self.app_name + "(%d)" % (n)
	self.past_instances[app_name] = n + 1
	self.instances[new_name] = app
	self.instance_windows[new_name] = []
	self.instance_apps[new_name] = app_name
	if initial_window != None:
	    if initial_window not in self.windows.keys():
		self.windows[initial_window] = new_name
		self.instance_windows[ new_name].append(initial_window)
	return new_name

    def delete_instance(self, instance):
	"""remove named instance from management

	**INPUTS**

	*STR* instance -- name of the application instance to be removed
    
	**OUTPUTS**

	*none*
	"""
	if self.instances.has_key(instance):
	    app_name = self.instance_apps[instance]
	    del self.instance_apps[instance]
	    instance_names = self.instance_names[app_name]
	    for i in range(instance_names):
		if instance_names[i] == instance:
		    del instance_names[i]
		    break
	    del self.windows[window]
	    windows = self.instance_windows[instance]
	    for window in windows:
		del self.windows[window]
	    del self.instance_windows[instance]
	    del self.instances[instance]

    def delete_window(self, window):
	"""remove window from list of known windows
	corresponding to an editor application instance.

	**INPUTS**

	*INT* window -- window handle of the window
    
	**OUTPUTS**

	*none*
	"""
	if self.windows.has_key(window):
	    instance = self.windows[window]
	    windows = self.instance_windows[instance]
	    for i in range(windows):
		if windows[i] == window:
		    del windows[i]
		    break
	    del self.windows[window]

