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

"""class which owns and manages AppState objects corresponding to
editor instances
"""

import debug
import string
from Object import Object, OwnerObject
import RecogStartMgr
import TargetWindow, WinIDClient

class InstanceInfo(Object):
    """class for storing information about editor application instances

    **INSTANCE ATTRIBUTES**

    *STR* instance_name -- unique name assigned by AppMgr

    *STR* application_name -- name of the corresponding editor
    application
    """
    def __init__(self, name, application_name, **args):
	self.deep_construct(InstanceInfo, 
                           {'instance_name': name,
			   'application_name': application_name
			   },
			   args)
	
    def name(self):
	"""return name of instance

	**INPUTS**

	*none*

	**OUTPUTS**

	**STR** -- the instance name
	"""
	return self.instance_name

    def application(self):
	"""return name of application

	**INPUTS**

	*none*

	**OUTPUTS**

	**STR** -- the application name
	"""
	return self.application_name

class AppMgr(OwnerObject):
    """class defining basic interface for keeping track of 
    target applications and windows

    **INSTANCE ATTRIBUTES**

    *RecogStartMgr* recog_mgr -- reference to a RecogStartMgr object

    *{STR : [STR]}* instance_names -- map from editor application name 
    to currently managed instance names

    *{STR : INT}* past_instances -- map from editor application name 
    to number of current and past instances

    *{INT : [STR]}* windows -- map from currently known windows to
    lists of associated instance names, sorted in the order of instances
    most recently known to be active

    *{STR : InstanceInfo}* instance_data  -- map from instance names to
    corresponding instance-specific data

    *{STR : AppState}* instances -- map from instance names to
    corresponding AppState interfaces

    **CLASS ATTRIBUTES**
    
    *none*
    """

    def __init__(self, recog_mgr, **args):
	"""
	**INPUTS**

	*RecogStartMgr* recog_mgr -- reference to a RecogStartMgr object
	
	"""
        self.deep_construct(AppMgr,
                            {'instance_names': {}, 
			    'instances': {}, 'instance_data': {},
			    'recog_mgr': recog_mgr,
			    'past_instances' : {}},
                            args)
	self.add_owned_list(['recog_mgr', 'instances'])
	self.recog_mgr.set_app_mgr(self)
	self.recog_mgr.activate()

    def remove_other_references(self):
	self.recog_mgr.deactivate()
	OwnerObject.remove_other_references(self)

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

    def app_name(self, instance):
	"""names of application corresponding to an instance

	**INPUTS**
	
	*STR* instance -- name of the application instance

	**OUTPUTS**
	
	*STR* -- name of corresponding application, or None if the
	instance is unknown
	"""
	if not self.instance_data.has_key(instance):
	    return None
	return self.instance_data[instance].application()

    def add_module(self, module):
	"""add a new KnownTargetModule object to the RecogStartMgr

	**INPUTS**

	*KnownTargetModule* module -- the new module

	**OUTPUTS**

	*BOOL* -- true unless a module of the same name already exists
	"""
	self.recog_mgr.add_module(module)

    def known_window(self, window):
	"""is window a known window ID?

	**INPUTS**
    
	*INT* window -- window handle of the window

	**OUTPUTS**
	
	*BOOL* -- true if window is a known window associated with one or more
	editor instances
	"""
	return self.recog_mgr.known_window(window)

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
	return self.recog_mgr.known_windows(instance)

    def window_info(self):
	"""find the window id, title, and module of the current window

	**INPUTS**

	*none*

	**OUTPUTS**

	*(INT, STR, STR)* -- the window id, title, and module name
	"""
	return self.recog_mgr.window_info()

    def _add_new_instance(self, app_name, title_prefix, app):
	"""private method called internally to do the work of
	new_instance, except for notifying the recog_mgr.

	**INPUTS**

	*STR* app_name -- name of the application 
	(e.g. "Emacs (Win)", "jEdit")

	*STR* title_prefix -- a unique string for each application, used
	as the prefix of the title string (which is in turn included as
	a substring of the window title, if the editor can do so)

	*AppState* app --  AppState interface corresponding to the new
	instance

	**OUTPUTS**

	*STR* -- name of the application instance.  Necessary
	if you want to add windows to the application in the future.
	"""
	if app_name not in self.app_names():
	    self.instance_names[app_name] = []
	    self.past_instances[app_name] = 0
	n = self.past_instances[app_name]
	new_name = app_name + "(%d)" % (n)
	self.past_instances[app_name] = n + 1
	self.instances[new_name] = app
	app.set_manager(self)
	app.set_name(new_name)
	self.instance_names[app_name].append(new_name)
	self.instance_data[new_name] = InstanceInfo(new_name, app_name)
	app.set_instance_string("(%s %d)" % (title_prefix, n))
#	print 'new instance ' + new_name + ' app = '
#	print repr(app)
	return new_name

    def new_instance(self, app_name, title_prefix, app, check_window = 1):
	"""add a new application instance

	**INPUTS**

	*STR* app_name -- name of the application 
	(e.g. "Emacs (Win)", "jEdit")

	*STR* title_prefix -- a unique string for each application, used
	as the prefix of the title string (which is in turn included as
	a substring of the window title, if the editor can do so)

	*AppState* app --  AppState interface corresponding to the new
	instance

	*BOOL* check_window -- should we check to see if the
	current window belongs to this instance?

	**OUTPUTS**

	*STR* -- name of the application instance.  Necessary
	if you want to add windows to the application in the future.
	"""
	new_name = self._add_new_instance(app_name, title_prefix, app)
	self.recog_mgr.new_instance(new_name, check_window)
#	print repr(self.app_instance(new_name))
	return new_name

    def new_universal_instance(self, app_name, title_prefix, app,
	exclusive = 1):
	"""add a new application instance

	**INPUTS**

	*STR* app_name -- name of the application 
	(e.g. "Emacs (Win)", "jEdit")

	*STR* title_prefix -- a unique string for each application, used
	as the prefix of the title string (which is in turn included as
	a substring of the window title, if the editor can do so)

	*AppState* app --  AppState interface corresponding to the new
	instance

	*BOOL* exclusive -- use exclusive grammars?

	**OUTPUTS**

	*STR* -- name of the application instance.  Necessary
	if you want to add windows to the application in the future.
	"""
	new_name = self._add_new_instance(app_name, title_prefix, app)
	self.recog_mgr.new_universal_instance(new_name, exclusive)
#	print repr(self.app_instance(new_name))
	return new_name


    def delete_instance(self, instance):
	"""remove named instance from management

	**INPUTS**

	*STR* instance -- name of the application instance to be removed
    
	**OUTPUTS**

	*none*
	"""
	if self.instances.has_key(instance):
	    app_name = self.instance_data[instance].application()
	    self.instance_names[app_name].remove(instance)
	    self.recog_mgr.delete_instance(instance)
	    del self.instance_data[instance]
	    self.instances[instance].cleanup()
	    del self.instances[instance]

    def new_window(self, instance):
	"""called when the editor notifies us of a new window for the 
	specified instance

	**INPUTS**

	*STR* instance -- name of the application instance

	**OUTPUTS**

	*BOOL* -- true if window is added
	"""
	if self.known_instance(instance): 
#	    print 'am new window'
#	    print instance, self.app_instance(instance)
	    return self.recog_mgr.app_new_window(instance)
	return 0
    
    def specify_window(self, instance):
	"""called to indicate that user has manually identified a
	known instance with the current window 

	**INPUTS**

	*STR* instance -- name of the application instance

	**OUTPUTS**

	*BOOL* -- true if window is added
	"""
# we still want to check for consistency
#	print 'app specify'
	if not self.known_instance(instance):
#	    print 'app specify unknown instance'
	    return 0
	return self.recog_mgr.specify_window(instance)

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
	if self.known_instance(instance): 
	    return self.recog_mgr.delete_window(instance, window)
	return 0

    def known_instance(self, instance):
	"""checks whether a specific instance name is known

	**INPUTS**

	*STR* instance -- name of the instance

	**OUTPUTS**

	*BOOL* -- true if an instance by that name is being managed
	"""
	return self.instances.has_key(instance)

    def window_instances(self, window):
	"""returns the list of known instances corresponding to a given
	window handle, in the order of most recent activation

	**INPUTS**

	*INT* window -- the window handle 

	**OUTPUTS**

	*[STR]* -- list of names of instances associated with the
	window, or None if the window is unknown
	"""
	return self.recog_mgr.window_instances(window)
 
    def app_instance(self, instance):
	"""return a reference to the AppState object corresponding to a
	particular instance. **Note:** Use only temporarily.  Storing 
	this reference is unsafe, and may lead to mediator crashes on 
	calls to its methods, and to failure to free resources.

	**INPUTS**

	*STR* instance -- name of the application instance 

	**OUTPUTS**

	*AppState* -- temporary reference to the corresponding AppState
	object
	"""
	if not self.instances.has_key(instance):
	    return None
	return self.instances[instance]

    def instance_module(self, instance):
	"""returns the module associated with the given instance

	**INPUTS**

	*STR* instance -- the name of the instance

	**OUTPUTS**

	*STR* -- the name of the module associated with the instance, or
	None if it is unknown (because the instance has not yet been
	associated with any windows)
	"""
	if self.known_instance(instance): 
	    return self.recog_mgr.instance_module(instance)
	return None
     
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
# WinIDClient support is not yet implemented
	return None


# defaults for vim - otherwise ignore
# vim:sw=4