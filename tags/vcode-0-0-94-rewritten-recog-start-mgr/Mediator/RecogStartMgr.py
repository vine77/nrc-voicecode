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
import re
from Object import Object, OwnerObject

import GramMgr

import TargetWindow, KnownTargetModule, WinIDClient

class KnownInstance(Object):
    """class which stores data about instances known to RecogStartMgr

    **INSTANCE ATTRIBUTES**

    *STR* module_name -- name of the module corresponding to this
    instance (all windows of an instance belong to the same
    module)
    
    *[INT]* instance_windows -- list of handles of known windows
    corresponding to this instance

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, initial_window = None, module_name = None, **args):
	"""create the KnownInstance object

	**INPUTS**

	*INT* initial_window -- handle of the initial window for the
	instance, if any

	*STR* module_name -- name of the module of the initial window
	"""
	self.deep_construct(KnownInstance,
			    {'module_name': module_name,
			     'instance_windows': []
			    },
			    args)
	if initial_window != None:
	    self.instance_windows.append(initial_window)
	
    def module(self):
	"""return the name of the module corresponding to this instance

	**INPUTS**

	*none*

	**OUTPUTS**

	*STR* -- the name of the module, or None if it is unknown
	because the instance has no known windows yet
	"""
	return self.module_name

    def windows(self):
	"""return the windows known to be associated with this module

	**INPUTS**

	*none*

	**OUTPUTS**

	*[INT]* -- the list of window handles associated with the
	instance
	"""
	return self.instance_windows

    def add_window(self, window):
	"""add a new window to the list of windows associated with this
	module

	**INPUTS**

	*INT* window -- handle of the new window

	**OUTPUTS**

	*BOOL* -- true if the window was not already known
	"""
	if window in self.instance_windows:
	    return 0
	self.instance_windows.append(window)
	return 1

    def delete_window(self, window):
	"""remove a window from the list of windows associated with this
	module

	**INPUTS**

	*INT* window -- handle of the new window

	**OUTPUTS**

	*BOOL* -- true if the window was known
	"""
	try:
	    self.instance_windows.remove(window)
	    return 1
	except ValueError:
	    return 0


# Note: While handling recognition-starting callbacks is the primary function 
# of the recognition starting manager, the abstract base class RecogStartMgr 
# does not set the callback, or define the function which handles it directly.
# This is because the number, type, and meaning of arguments passed to that 
# callback function may depend on the speech engine and/or the platform.
# Instead, it defines the private method _recognition_starting which
# the concrete subclass's callback function should invoke.

class RecogStartMgr(OwnerObject):
    """abstract class defining interface for an object which receives 
    recognition-starting (or onBegin/gotBegin) callbacks, figures out which
    application and buffer are active, and tells the GramMgr to activate the
    appropriate grammars.

    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**
    
    *none*
    """

    def __init__(self, **args):
        self.deep_construct(RecogStartMgr,
                            {
			    },
                            args)
	
    def set_app_mgr(self, manager):
	"""fill in the reference to the parent AppMgr

	**INPUTS**

	*AppMgr* manager -- the parent AppMgr

	**OUTPUTS**

	*none*
	"""
	debug.virtual('RecogStartMgr.set_app_mgr')
	
    def window_info(self):
	"""find the window id, title, and module of the current window

	**INPUTS**

	*none*

	**OUTPUTS**

	*(INT, STR, STR)* -- the window id, title, and module name
	"""
	debug.virtual('RecogStartMgr.window_info')

    def activate(self):
	"""activate the RecogStartMgr

	**INPUTS**

	*none*

	**OUTPUTS**

	*BOOL* -- true if activated successfully
	"""
        debug.virtual('RecogStartMgr.activate')

    def deactivate(self):
	"""deactivate the RecogStartMgr, and disable all window-specific
	grammars

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
        debug.virtual('RecogStartMgr.deactivate')

    def remove_other_references(self):
	self.deactivate()
	OwnerObject.remove_other_references(self)
# GramMgr is not currently an OwnerObject, but performs cleanup on
# __del__.  As long as RecogStartMgr gets deleted, so should its grammar 
# managers and their grammars, so this should be sufficient


    def add_module(self, module):
	"""add a new KnownTargetModule object

	**INPUTS**

	*KnownTargetModule* module -- the new module

	**OUTPUTS**

	*BOOL* -- true unless a module of the same name already exists
	"""
	debug.virtual('RecogStartMgr.add_module')

    def known_window(self, window):
	"""is window a known window ID?

	**INPUTS**
    
	*INT* window -- window handle of the window

	**OUTPUTS**
	
	*BOOL* -- true if window is a known window 
	"""
	debug.virtual('RecogStartMgr.window_info')

    def shared_window(self, window):
	"""is window a shared window?

	**INPUTS**
    
	*INT* window -- window handle of the window

	**OUTPUTS**
	
	*BOOL* -- true if window is a known window  and is shared (or
	shareable).  None if window is unknown
	"""
	debug.virtual('RecogStartMgr.shared_window')

    def single_display(self, window):
	"""is window a single-window display?

	**INPUTS**
    
	*INT* window -- window handle of the window

	**OUTPUTS**
	
	*BOOL* -- true if window is a known window  and is a
	single-window display.  None if window is unknown
	"""
	debug.virtual('RecogStartMgr.single_display')

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
	debug.virtual('RecogStartMgr.known_windows')


    def known_module(self, module):
	"""is this module known?

	**INPUTS**

	*STR* module -- name of the module (executable as seen by the
	local system)

	**OUTPUTS**

	*BOOL* -- true if the module name is known
	"""
	debug.virtual('RecogStartMgr.known_module')
    
    def known_instance(self, instance):
	"""is this instance known?

	**INPUTS**

	*STR* instance -- the name of the instance

	**OUTPUTS**

	*BOOL* -- true if the instance is known
	"""
	debug.virtual('RecogStartMgr.known_instance')

    def known_instances(self):
	"""returns the list of known instances

	**INPUTS**

	*none*

	**OUTPUTS**

	*[STR]* -- list of names of known instances
	"""
	debug.virtual('RecogStartMgr.known_instances')

    def window_instances(self, window):
	"""returns a list of the known instances associated with a given
	window

	**INPUTS**

	*INT* window -- the window handle 

	**OUTPUTS**

	*[STR]* -- list of names of instances associated with the
	window, or None if the window is unknown
	"""
	debug.virtual('RecogStartMgr.window_instances')

    def instance_module(self, instance):
	"""returns the module associated with the given instance

	**INPUTS**

	*STR* instance -- the name of the instance

	**OUTPUTS**

	*STR* -- the name of the module associated with the instance, or
	None if it is unknown (because the instance has not yet been
	associated with any windows)
	"""
	debug.virtual('RecogStartMgr.instance_module')
    
    def new_instance(self, instance, check_window = 1):
	"""method called by AppMgr to notify RecogStartMgr that a new
	editor instance has been added, and (optionally) to tell it to 
	check if the current window belongs to (or contains) that instance
    
	**INPUTS**

	*STR* instance -- name of the editor instance

	*BOOL* check_window -- should we check to see if the
	current window belongs to this instance?

	**OUTPUTS**

	*none*
	"""
	debug.virtual('RecogStartMgr.new_instance')

    def delete_instance(self, instance):
	"""method called by AppMgr to notify RecogStartMgr that an
	editor instance has been deleted
    
	**INPUTS**

	*STR* instance -- name of the editor instance

	**OUTPUTS**

	*BOOL* -- true if instance was known
	"""
	debug.virtual('RecogStartMgr.delete_instance')

    def specify_window(self, instance):
	"""called to indicate that user has manually identified a
	known instance with the current window 

	**INPUTS**

	*STR* instance -- name of the application instance

	**OUTPUTS**

	*BOOL* -- true if window is added
	"""
	debug.virtual('RecogStartMgr.specify_window')

    def app_new_window(self, instance):
	"""called when the editor notifies us of a new window for the 
	specified instance

	**INPUTS**

	*STR* instance -- name of the application instance

	**OUTPUTS**

	*BOOL* -- true if window is added
	"""
	debug.virtual('RecogStartMgr.app_new_window')

    def delete_window(self, instance, window):
	"""remove window from list of known windows
	corresponding to an editor application instance.

	**INPUTS**

	*STR* instance -- name of the application instance 
    
	*INT* window -- window handle of the window

	**OUTPUTS**

	*BOOL* -- true if window and instance are known (otherwise, does
	nothing)
	"""
	debug.virtual('RecogStartMgr.delete_window')
    
    def activate_instance_window(self, instance, window):
	"""raise instance to front of list of most recently active instances 
	for that window

	**INPUTS**

	*STR* instance -- name of the application instance 

	*INT* window -- window handle of the window

	**OUTPUTS**

	*BOOL* -- true if window and instance are known (otherwise, does
	nothing)
	"""
	debug.virtual('RecogStartMgr.activate_instance_window')

    def _recognition_starting(self, window, title, module_name = None):
	"""private method which a concrete subclass will call to handle
	the recognition starting event.

	**INPUTS**

	*INT* window -- window handle (unique identifier) of the current 
	window

	*STR* title -- title of the window 

	*STR* module -- filename of the application corresponding to
	this window, or None if the particular subclass of RecogStartMgr
	cannot detect it.  **Note**: the module may not
	be the name of the editor.  For example, for remote editors, the
	module will generally be the name of the telnet/X server
	program, and any application written in python will show up as PYTHON.

	**OUTPUTS**

	*none*
	"""
	debug.virtual('RecogStartMgr._recognition_starting')
    
class RSMInfrastructure(RecogStartMgr):
    """abstract class defining interface for an object which receives 
    recognition-starting (or onBegin/gotBegin) callbacks, figures out which
    application and buffer are active, and tells the GramMgr to activate the
    appropriate grammars.

    **INSTANCE ATTRIBUTES**

    *{INT : TargetWindow}* windows -- map from currently known window 
    IDs to TargetWindow objects

    *{STR : KnownTargetModule}* modules -- map from currently known
    module names to KnownTargetModule objects

    *{STR : [INT]}* instances -- map from instance names to 
    KnownInstance objects

    *{STR: GramMgr}* grammars -- map from instance names to 
    grammar managers for creating, activating, and deactivating 
    grammars for that instance

    *GramMgrFactory* GM_factory -- GramMgrFactory to create GramMgr
    objects for new instances

    *AppMgr* editors -- the parent AppMgr object, which provides
    information about editor application instances

    *BOOL* active -- flag indicating whether the RecogStartMgr is
    active

    **CLASS ATTRIBUTES**
    
    *none*
    """

    def __init__(self, editors, GM_factory, **args):
	"""
	**INPUTS**

	*AppMgr* editors -- the editors AppMgr object, which provides
	information about editor application instances

	*GramMgrFactory* GM_factory -- GramMgrFactory to create GramMgr
	objects for new instances
	
	"""
        self.deep_construct(RSMInfrastructure,
                            {'active': 0,
			     'editors': editors,
			     'GM_factory': GM_factory,
			     'grammars': {},
			     'windows': {},
			     'modules': {},
			     'instances': {}
			    },
                            args)
	self.name_parent('editors')
	
    def set_app_mgr(self, manager):
	"""fill in the reference to the parent AppMgr

	**INPUTS**

	*AppMgr* manager -- the parent AppMgr

	**OUTPUTS**

	*none*
	"""
	self.editors = manager
	
    def add_module(self, module):
	"""add a new KnownTargetModule object

	**INPUTS**

	*KnownTargetModule* module -- the new module

	**OUTPUTS**

	*BOOL* -- true unless a module of the same name already exists
	"""
	module_name = module.name()
	if self.known_module(module_name):
	    return 0
	self.modules[module_name] = module
	return 1

    def known_window(self, window):
	"""is window a known window ID?

	**INPUTS**
    
	*INT* window -- window handle of the window

	**OUTPUTS**
	
	*BOOL* -- true if window is a known window 
	"""
	if not self.windows.has_key(window):
	    return 0
#	if self.windows[window].instances() == 0:
#	    return 0
	return 1

    def shared_window(self, window):
	"""is window a shared window?

	**INPUTS**
    
	*INT* window -- window handle of the window

	**OUTPUTS**
	
	*BOOL* -- true if window is a known window  and is shared (or
	shareable).  None if window is unknown
	"""
	if self.known_window(window):
	    return self.windows[window].shared()
	return None

    def single_display(self, window):
	"""is window a single-window display?

	**INPUTS**
    
	*INT* window -- window handle of the window

	**OUTPUTS**
	
	*BOOL* -- true if window is a known window  and is a
	single-window display.  None if window is unknown
	"""
	if self.known_window(window):
	    return self.windows[window].single_display()
	return None

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
	    return self.windows.keys()

	if not self.instances.has_key(instance):
	    return []
	return self.instances[instance].windows()

    def known_module(self, module):
	"""is this module known?

	**INPUTS**

	*STR* module -- name of the module (executable as seen by the
	local system)

	**OUTPUTS**

	*BOOL* -- true if the module name is known
	"""
	if self.modules.has_key(module):
	    return 1
	return 0
    
    def known_instance(self, instance):
	"""is this instance known?

	**INPUTS**

	*STR* instance -- the name of the instance

	**OUTPUTS**

	*BOOL* -- true if the instance is known
	"""
	if self.instances.has_key(instance):
	    return 1
	return 0

    def known_instances(self):
	"""returns the list of known instances

	**INPUTS**

	*none*

	**OUTPUTS**

	*[STR]* -- list of names of known instances
	"""
	return self.instances.keys()

    def window_instances(self, window):
	"""returns a list of the known instances associated with a given
	window

	**INPUTS**

	*INT* window -- the window handle 

	**OUTPUTS**

	*[STR]* -- list of names of instances associated with the
	window, or None if the window is unknown
	"""
	if not self.known_window(window):
	    return None
	return self.windows[window].instance_names()

    def instance_module(self, instance):
	"""returns the module associated with the given instance

	**INPUTS**

	*STR* instance -- the name of the instance

	**OUTPUTS**

	*STR* -- the name of the module associated with the instance, or
	None if it is unknown (because the instance has not yet been
	associated with any windows)
	"""
	if not self.known_instance(instance):
	    return None
	return self.instances[instance].module()
    
    def _add_instance(self, instance, window_id = None, module = None):
	"""private method to add a new instance with a given target
	window and module

	**INPUTS**

	*STR* instance -- the name of the instance

	*INT* window_id -- the initial window handle of the instance,
	or None if the instance has no associated window yet

	*STR* module -- the module name corresponding to the window, 
	or None if the instance has no associated window yet

	**OUTPUTS**

	*BOOL* -- true if instance is added successfully.  False if
	there is already an instance with that name.

	"""
	if self.known_instance(instance):
	    return 0
	self.instances[instance] = KnownInstance(window_id, module)
	self.grammars[instance] = \
		self.GM_factory.new_manager(self.editors.app_instance(instance))
	return 1

    def _add_known_window(self, window_id, window, instance):
	"""private method called internally to add a new
	TargetWindow object to the map of windows

	**INPUTS **

	*INT* window_id -- the window handle of the newly identified
	window

	*TargetWindow* window -- the TargetWindow object

	*STR* instance -- the name of the corresponding instance

	**OUTPUTS**

	*BOOL* -- true if the window was added successfully
	"""
	if self.known_window(window_id):
	    return 0
	if not self.known_window(window_id):
	    self.windows[window_id] = window
	if not self.instances.has_key(instance):
	    module_name = window.module_name()
	    success = self._add_instance(instance, window_id, module_name)
	    if success:
		app = self.editors.app_instance(instance)
		module = self.modules[module_name]
		title_escape = module.title_escape_sequence()
		app.title_escape_sequence(title_escape[0], title_escape[1])
	    return success
	else:
	    old_module = self.instances[instance].module()
	    success = self.instances[instance].add_window(window_id)
	    if success and old_module == None:
		app = self.editors.app_instance(instance)
		module_name = window.module_name()
		module = self.modules[module_name]
		title_escape = module.title_escape_sequence()
		app.title_escape_sequence(title_escape[0], title_escape[1])
	    return success

    
    def _add_instance_to_window(self, window, instance):
	"""private method called internally to add a new
	instance to a TargetWindow object 

	**INPUTS **

	*INT* window -- the window handle of the newly identified
	window

	*STR* instance -- the name of the corresponding instance

	**OUTPUTS**

	*BOOL* -- true if the instance was added successfully
	"""
	if not self.known_window(window):
	    return 0
	if self.known_instance(instance):
	    return 0
	if not self.windows[window].add_instance(instance):
	    return 0
	if not self.instances.has_key(instance):
	    old_module = None
	    module_name = self.windows[window].module_name()
	    self._add_instance(instance, window, module_name)
	else:
	    old_module = self.instances[instance].module()
	self.instances[instance].add_window(window)
	if old_module == None:
	    app = self.editors.app_instance(instance)
	    module_name = self.windows[window].module_name()
	    module = self.modules[module_name]
	    title_escape = module.title_escape_sequence()
	    app.title_escape_sequence(title_escape[0], title_escape[1])
	return 1

    def _new_instance_known_window(self, window, title, instance, 
	trust = 0):
	"""private method called internally to verify that the named
	instance belongs to the given known window, and if so to add 
	it to the window 

	**INPUTS**

	*INT* window -- the handle of the known window

	*STR* title -- the current title of the window

	*STR* instance -- the name of the instance

	*BOOL* trust -- trust that instance belongs to the window, even
	if we can't verify it definitively, because the user has
	manually specified the window

	**OUTPUTS**

	*BOOL* -- true if the instance was added successfully
	"""
	debug.virtual('RSMInfrastructure._new_instance_known_window')

    def _new_instance_known_module(self, window, title, instance, module_name,
	trust = 0):
	"""private method called internally to verify that the named
	instance belongs to the given unknown window.  If so, a 
	TargetWindow object is created and added to the 
	known windows map.

	**INPUTS**

	*INT* window -- the handle of the known window

	*STR* title -- the current title of the window

	*STR* instance -- the name of the instance

	*STR* module_name -- name of the module 

	*BOOL* trust -- trust that instance belongs to the window, even
	if we can't verify it definitively, because the user has
	manually specified the window

	**OUTPUTS**

	*BOOL* -- true if the instance was added successfully
	"""
	debug.virtual('RSMInfrastructure._new_instance_known_module')

    def new_instance(self, instance, check_window = 1):
	"""method called by AppMgr to notify RecogStartMgr that a new
	editor instance has been added, and (optionally) to tell it to 
	check if the current window belongs to (or contains) that instance
    
	**INPUTS**

	*STR* instance -- name of the editor instance

	*BOOL* check_window -- should we check to see if the
	current window belongs to this instance?

	**OUTPUTS**

	*none*
	"""
	if check_window:
	    window, title, module_name = self.window_info()
	    if self.known_window(window):
		self._new_instance_known_window(window, title, instance)
	    elif self.known_module(module_name):
		self._new_instance_known_module(window, title, 
		    instance, module_name)
	else:
	    self._add_instance(instance)

    def delete_instance(self, instance):
	"""method called by AppMgr to notify RecogStartMgr that an
	editor instance has been deleted
    
	**INPUTS**

	*STR* instance -- name of the editor instance

	**OUTPUTS**

	*BOOL* -- true if instance was known
	"""
	if not self.instances.has_key(instance):
	    return 0
	windows = self.known_windows(instance)
	for window in windows:
	    self.windows[window].delete_instance(instance)
	    if self.windows[window].instances() == 0:
		del self.windows[window]
	del self.instances[instance]
	del self.grammars[instance]

    def specify_window(self, instance):
	"""called to indicate that user has manually identified a
	known instance with the current window 

	**INPUTS**

	*STR* instance -- name of the application instance

	**OUTPUTS**

	*BOOL* -- true if window is added
	"""
# we still want to check for consistency
	if not self.known_instance(instance):
	    return 0
	window, title, module_name = self.window_info()
	if self.known_window(window):
	    return self._new_instance_known_window(window, 
		title, instance, trust = 1)
	elif self.known_module(module_name):
	    return self._new_instance_known_module(window, title, 
		instance, module_name, trust = 1)


    def app_new_window(self, instance):
	"""called when the editor notifies us of a new window for the 
	specified instance

	**INPUTS**

	*STR* instance -- name of the application instance

	**OUTPUTS**

	*BOOL* -- true if window is added
	"""
	if not self.known_instance(instance):
	    return 0
	window, title, module_name = self.window_info()
	if self.known_window(window):
	    return 0
	if not self.known_module(module_name):
	    return 0
	old_module = self.instances[instance].module()
	if old_module != None:
	    if module_name != old_module:
		return 0
	return self._new_instance_known_module(window, title, 
		instance, module_name)

    def delete_window(self, instance, window):
	"""remove window from list of known windows
	corresponding to an editor application instance.

	**INPUTS**

	*STR* instance -- name of the application instance 
    
	*INT* window -- window handle of the window

	**OUTPUTS**

	*BOOL* -- true if window and instance are known (otherwise, does
	nothing)
	"""
	if not self.known_instance(instance):
	    return 0
	if window not in self.known_windows(instance):
	    return 0
	self.windows[window].delete_instance(instance)
	if self.windows[window].instances() == 0:
	    del self.windows[window]
	self.instances[instance].delete_window(window)
	return 1
    
    def activate_instance_window(self, instance, window):
	"""raise instance to front of list of most recently active instances 
	for that window

	**INPUTS**

	*STR* instance -- name of the application instance 

	*INT* window -- window handle of the window

	**OUTPUTS**

	*BOOL* -- true if window and instance are known (otherwise, does
	nothing)
	"""
	if not self.known_instance(instance):
	    return 0
	if window not in self.known_windows(instance):
	    return 0
	return self.windows[window].activate_instance(instance)

    def _activate_grammars(self, app, instance_name, window):
	"""private method used to activate grammars for the current
	buffer of an identified editor and window, assuming that the
	buffer is VoiceCode-enabled
	
	**INPUTS**

	*AppState* app -- the editor application interface

	*STR* instance -- instance name

	*INT* window -- window handle of the window to be speech-enabled

	**OUTPUTS**

	*none*
	"""
	self.activate_instance_window(instance_name, window)
	buff_name = app.curr_buffer_name()
	dictation_allowed = app.recog_begin(window)
	if self.app.active_field() == None and dictation_allowed:
	    self.grammars[instance].activate(buff_name, window)
	else:
	    self.grammars[instance].deactivate_all(window)
	for editor in self.windows[window].instances():
	    if editor != instance:
		self.grammars[editor].deactivate_all(window)
	
    def _deactivate_grammars(self, window):
	"""private method used to deactivate all grammars for a given
	window
	
	**INPUTS**

	*INT* window -- window handle 

	**OUTPUTS**

	*none*
	"""
	for instance in self.windows[window].instances():
	    self.grammars[instance].deactivate_all(window)
	
    def _recognition_starting_known_window(self, window, title):
	"""private method called by _recognition_starting when the
	current window is known.

	**INPUTS**

	*INT* window -- window handle (unique identifier) of the current 
	window

	*STR* title -- title of the window 

	**OUTPUTS**

	*none*
	"""
	win = self.windows[window]
	instance = win.active_instance(title)
	if instance == None:
	    self._deactivate_grammars(window)
	    return
	app = self.editors.app_name(instance)
	if app == None:
	    self._deactivate_grammars(window)
	    return
	self._activate_grammars(app, instance, window)
	return

    def _recognition_starting_known_module(self, window, title, module_name):
	"""private method called by _recognition_starting when the
	current window is not a previously known window, but the 
	current module is known.

	**INPUTS**

	*INT* window -- window handle (unique identifier) of the current 
	window

	*STR* title -- title of the window 

	*STR* module_name -- filename of the application corresponding to
	this window.  **Note**: the module may not
	be the name of the editor.  For example, for remote editors, the
	module will generally be the name of the telnet/X server
	program, and any application written in python will show up as PYTHON.

	**OUTPUTS**

	*none*
	"""
	debug.virtual('RSMInfrastructure._recognition_starting_known_module')
    
    def _recognition_starting(self, window, title, module_name = None):
	"""private method which a concrete subclass will call to handle
	the recognition starting event.

	**INPUTS**

	*INT* window -- window handle (unique identifier) of the current 
	window

	*STR* title -- title of the window 

	*STR* module -- filename of the application corresponding to
	this window, or None if the particular subclass of RecogStartMgr
	cannot detect it.  **Note**: the module may not
	be the name of the editor.  For example, for remote editors, the
	module will generally be the name of the telnet/X server
	program, and any application written in python will show up as PYTHON.

	**OUTPUTS**

	*none*
	"""
	if self.known_window(window):
	    self._recognition_starting_known_window( window, title)
	elif self.known_module(module_name):
	    self._recognition_starting_known_module(window, title, module_name)
    
    def _assign_ID_client(self, module_name, window, title):
	"""check if there is a WinIDClient not yet assigned to a window.
	If so, attempt to assign it to the specified window, and return
	a TargetWindow object.

	**INPUTS**

	*STR* module_name -- the name of the module corresponding to the
	window

	*INT* window -- the window handle of the window

	*STR* title -- the title of the window
    
	**OUTPUTS**

	*TargetWindow* -- an object of subclass of TargetWindow managed
	by the unassigned WinIDClient, or None if there is no unassigned 
	client, or the given window is not managed by that client.
	"""
# for now, WinIDClient objects are handled by the AppMgr
	return self.editors._assign_ID_client(module_name, window, title)

class RSMBasic(RSMInfrastructure):
    """partially concrete subclass of RSMInfrastructure, defining the
    basic algorithms for handling recognition-starting 
    (or onBegin/gotBegin) callbacks

    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**
    
    *none*
    """

    def __init__(self, **args):
	"""
	see RecogStartMgr

	"""
        self.deep_construct(RSMBasic,
                            {
			    },
                            args)
	
    def _new_instance_known_window(self, window, title, instance, 
	trust = 0):
	"""private method called internally to verify that the named
	instance belongs to the given known window, and if so to add 
	it to the window 

	**INPUTS**

	*INT* window -- the handle of the known window

	*STR* title -- the current title of the window

	*STR* instance -- the name of the instance

	*BOOL* trust -- trust that instance belongs to the window, even
	if we can't verify it definitively, because the user has
	manually specified the window

	**OUTPUTS**

	*BOOL* -- true if the instance was added successfully
	"""
	win = self.windows[window]
	if not win.shared():
# window is known and dedicated, so it cannot belong to the new instance
	    return 0
	app = self.editors.app_instance(instance)
	if win.single_display() or app.shared_window():
	    verified = win.verify_new_instance(title, instance, self.editors)
	    if verified == 1 or (trust and verified == None):
		return self._add_instance_to_window(window, instance)
	    return 0
# otherwise, instance says it uses dedicated windows, whereas the window
# is shared, and is not a single-window display, so
# it cannot belong to the new instance
	return 0


    def _new_instance_known_module(self, window, title, instance, module_name,
	trust = 0):
	"""private method called internally to verify that the named
	instance belongs to the given unknown window.  If so, a 
	TargetWindow object is created and added to the 
	known windows map.

	**INPUTS**

	*INT* window -- the handle of the known window

	*STR* title -- the current title of the window

	*STR* instance -- the name of the instance

	*STR* module_name -- name of the module 

	*BOOL* trust -- trust that instance belongs to the window, even
	if we can't verify it definitively, because the user has
	manually specified the window

	**OUTPUTS**

	*BOOL* -- true if the instance was added successfully
	"""
# unknown window but known module
	module = self.modules[module_name]
	if module.dedicated():
	    if module.editor() != self.editors.app_name(instance):
		return 0
	if module.single_display(window, title):
# check if we have a WinIDClient not yet assigned to a window.
	    target = self._assign_ID_client(module_name, window, title)
	    if target == None:
		return 0
	    return self._new_instance_known_window(window, title, 
		instance, trust)

# otherwise, verify
	verified = module.verify_new_instance(window, title, instance, 
	    self.editors)
	if verified == 1 or (trust and verified == None):
	    target = module.new_window(window, title, instance)
	    if target != None:
		return self._add_known_window(window, target, instance)
	    return 0
	return 0

    def _recognition_starting_known_module(self, window, title, module_name):
	"""private method called by _recognition_starting when the
	current window is not a previously known window, but the 
	current module is known.

	**INPUTS**

	*INT* window -- window handle (unique identifier) of the current 
	window

	*STR* title -- title of the window 

	*STR* module_name -- filename of the application corresponding to
	this window.  **Note**: the module may not
	be the name of the editor.  For example, for remote editors, the
	module will generally be the name of the telnet/X server
	program, and any application written in python will show up as PYTHON.

	**OUTPUTS**

	*none*
	"""
# unknown window
	module = self.modules[module_name]
	if module.single_display(window, title):
# check if we have a WinIDClient not yet assigned to a window.
	    target = self._assign_ID_client(module_name, window, title)
	    if target == None:
		return 
	    self._recognition_starting_known_window(window, title)
	    return
	for instance in self.known_instances():
	    info = self.instances[instance]
	    editor = self.editors.app_instance(instance)
	    instance_module = info.module()
	    if module.dedicated():
		app_name = self.editors.app_name(instance)
		if module.editor() != app_name or editor.shared_window():
		    continue
	    elif not editor.shared_window():
		continue
	    if instance_module == None or \
	       (instance_module == module_name and editor.multiple_windows()):
# if the instance has no module, it must be a fresh instance with no
# windows yet, so the current window might belong to it. Alternatively,
# if the instance's module matches that of the current window, and the
# editor supports multiple windows (and the module is not a
# single-window-display, which we've already ruled out above) then this
# might be a new window for the existing instance.  In either case,
# attempt to verify
		verified = module.verify_new_instance(window, title, 
		    instance, self.editors)
		if verified == 1:
		    target = module.new_window(window, title, instance)
		    if target != None:
			if self._add_known_window(window, target, instance):
			    self._recognition_starting_known_window(self, 
			        window, title)
		    return
		continue
		
class CurrWindow(Object):
    """abstract class for supplying information about the current window

    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, **args):
	self.deep_construct(CurrWindow, {}, args)
    
    def window_info(self):
	"""find the window id, title, and module of the current window

	**INPUTS**

	*none*

	**OUTPUTS**

	*(INT, STR, STR)* -- the window id, title, and module name
	"""
	debug.virtual('CurrWindow.window_info')

class CurrWindowDummy(Object):
    """dummy implementation of CurrWindow for testing purposes.

    **INSTANCE ATTRIBUTES**

    
    *INT* window -- the window id of the current window

    *STR* module -- the module name of the current window

    *AppState* instance -- the current instance

    *STR* app_name -- application name

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, window = None, module = None, instance = None, 
	app_name = None, **args):
	"""Initialize with specified window information

	**INPUTS**

	*INT* window -- the window id of the current window

	*STR* module -- the module name of the current window

	*AppState* instance -- the current instance
	
	*STR* app_name -- application name

	**OUTPUTS**

	*none*
	"""

	self.deep_construct(CurrWindowDummy, 
			    {'window': window,
			     'module': module,
			     'instance': instance,
			     'app_name': app_name
			    }, args)
    
    def window_info(self):
	"""find the window id, title, and module of the current window

	**INPUTS**

	*none*

	**OUTPUTS**

	*(INT, STR, STR)* -- the window id, title, and module name
	"""
#	print 'current is ', (self.window, self.title, self.module)
	title = ""
	if self.app_name != None:
	    title = self.app_name + " - "
	if self.instance != None:
	    title = title + self.instance.title_string()
	return (self.window, title, self.module)

    def set_info(self, window = None, module = None, instance = None, 
	app_name = None):
	"""set specified window information

	**INPUTS**

	*INT* window -- the window id of the current window

	*STR* module -- the module name of the current window

	*AppState* instance -- the current instance
	
	*STR* app_name -- application name

	**OUTPUTS**

	*none*
	"""
	self.window = window
	self.module = module
	self.instance = instance
	self.app_name = app_name

class RSMExtInfo(RSMBasic):
    """subclass of RSMBasic which uses an external object to
    get window information

    **INSTANCE ATTRIBUTES**

    *CurrWindow* find_info -- CurrWindow object for querying the current
    window

    **CLASS ATTRIBUTES**
    
    *none*
    """

    def __init__(self, win_info, **args):
	"""
	**INPUTS**

	*AppMgr* editors -- the editors AppMgr object, which provides
	information about editor application instances

	*GramMgrFactory* GM_factory -- GramMgrFactory to create GramMgr
	objects for new instances
	
	"""
        self.deep_construct(RSMExtInfo,
                            {'find_info': win_info
			    },
                            args)
	
    def window_info(self):
	"""find the window id, title, and module of the current window

	**INPUTS**

	*none*

	**OUTPUTS**

	*(INT, STR, STR)* -- the window id, title, and module name
	"""
	return self.find_info.window_info()

class RSMDummy(RSMExtInfo):
    """dummy subclass of RSMExtInfo not connected to the speech 
    engine, for testing purposes

    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**
    
    *none*
    """

    def __init__(self, **args):
        self.deep_construct(RSMDummy,
                            {},
                            args)
	
    def activate(self):
	"""activate the RecogStartMgr

	**INPUTS**

	*none*

	**OUTPUTS**

	*BOOL* -- true if activated successfully
	"""
	return 1

    def deactivate(self):
	"""deactivate the RecogStartMgr, and disable all window-specific
	grammars

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	return 1


# defaults for vim - otherwise ignore
# vim:sw=4

