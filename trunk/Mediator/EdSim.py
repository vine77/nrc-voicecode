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
# (C)2000, National Research Council of Canada
#
##############################################################################

"""VoiceCode editor simulator."""

import os, posixpath, re, sys
import auto_test, debug
import AppState, AppStateNonCached, as_services, SourceBuffEdSim

class EdSim(AppStateNonCached.AppStateNonCached):
    """VoiceCode editor simulator.

    This class is used to simulate an external programming editor.

    Useful for debugging VoiceCode mediator in isolation from external editor.
    
    **INSTANCE ATTRIBUTES**

    *BOOL* multiple -- does the instance support multiple buffers?
  
    *BOOL* instance_reporting -- flag which turns on diagnostic reporting 
    to check on proper allocation/de-allocation

    *STR* active_buffer_name -- name of the currently active buffer

    [AS_ServiceBreadcrumbs] *breadcrumbs_srv* -- The VoiceCode level
    breadcrumbs service used by EdSim.
    
    **CLASS ATTRIBUTES**
    
    *none* -- 

    ..[AS_ServiceBreadcrumbs] file:///./AppState.AS_ServiceBreadcrumbs.html"""

    buffer_methods = AppState.AppState.buffer_methods[:]
    buffer_methods.append('print_buff')
    
    def __init__(self, multiple = 0, instance_reporting = 0, **attrs):
        self.init_attrs({'breadcrumbs_srv': as_services.AS_ServiceBreadcrumbs(app=self)})
        self.deep_construct(EdSim,
                            {'active_buffer_name': "",
			    'instance_reporting': instance_reporting,
			    'multiple': multiple},
                            attrs)
	self.add_owned('breadcrumbs_srv')
	if self.instance_reporting:
	    print 'EdSim.__init__'
        self.open_buffers[self.active_buffer_name] = \
	    self.new_compatible_sb(buff_name = self.active_buffer_name)
  
    def __del__(self):
	"destructor"
	if self.instance_reporting:
	    print 'EdSim.__del__'

    def remove_other_references(self):
	"""additional cleanup to ensure that this object's references to
	its owned objects are the last remaining references

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
# subclasses must call their parent class's remove_other_references
# function, before performing their own duties
	if self.instance_reporting:
	    print 'EdSim.remove_other_references'
	AppStateNonCached.AppStateNonCached.remove_other_references(self)

    def new_compatible_sb(self, buff_name):
        """Creates a new instance of [SourceBuff].

        Note: The class used to instantiate the [SourceBuff] needs to
        be compatible with the class of *self*. With a few exceptions
        (if any), each subclass of *AppState* will have to redefine
        *new_compatible_sb* in order to generate a [SourceBuff] of the
        appropriate class.
        
        **INPUTS**
                
        STR *buff_name* -- unique name of the source buffer.
        
        **OUTPUTS**
        
        *none* -- 

        ..[SourceBuff] file:///./SourceBuff.SourceBuff.html"""
        
        return SourceBuffEdSim.SourceBuffEdSim(app=self, buff_name=buff_name, 
	    instance_reporting = self.instance_reporting)

        
    def recog_begin(self, window_id):
        
        """EdSim can't block user input and always allows user to dictate"""

        return 1


    def recog_end(self):
        
        """EdSim can't block user input"""
        pass


    def updates_from_app(self, what=[], exclude=1):
        """For EdSim, no need to get updates from external editor.

        We always get the state from EdSim directly, and every EdSim
        command that writes to the buffers will update the V-E map
        directly.
        
        **INPUTS**
        
        [STR] *what* -- List of items to be included/excluded in the updates.

        BOOL *exclude* -- Indicates if *what* is a list of items to be
        included or excluded from updates.
        
        **OUTPUTS**
        
        [ [AS_Update] ] *updates* -- List of updates retrieved from the
        external app.
        
        ..[AS_Update] file:///./AppState.AS_Update.html"""
        
        return []

    def app_active_buffer_name(self):
        
	"""Returns the file name of the buffer currently active in the
	external application.

        Note that this may or may not be the same the buffer that
        VoiceCode is currently bound to (see [curr_buffer_name]
        method for a description of buffer binding).

        **INPUTS**

        *none* --
        
	**OUTPUTS**

	*STR* -- file name of current buffer

        file:///./AppState.AppState.html#curr_buffer_name"""

	return self.active_buffer_name

    def app_change_buffer(self, buff_name=None):
	"""Changes the external application's active buffer.

        This variant only changes the buffer in the external
        application. It does not resynchronise VoiceCode with external
        application.

        This should NOT bind the *AppState* to the new buffer. This
        should be done only by [change_buffer].
        See [curr_buffer_name] for a description of buffer binding.

        **INPUTS**
        
        STR *buff_name=None* -- Name of the buffer to switch to.
       
        **OUTPUTS**
        
        *BOOL* -- true if buff_name exists and the external application
	successfully switches to it
        
            
        file:///./AppState.AppState.html#curr_buffer_name"""

        if self.query_buffer_from_app(buff_name):
	    self.active_buffer_name = buff_name
	    return 1
	return 0
     

    def drop_breadcrumb(self, buffname=None, pos=None):

        """Drops a breadcrumb

        *INT pos* is the position where to drop the crumb. *STR
         buffname* is the name of the source buffer.
        
        If *pos* not specified, drop breadcrumb at cursor position.

        If *buff* not specified either, drop breadcrumb in current buffer
	"""
        self.breadcrumbs_srv.drop_breadcrumb(buffname, pos)


    def pop_breadcrumbs(self, num=1, gothere=1):
        """Pops breadcrumbs from the breadcrumbs stack

        *INT num* is the number of crumbs to pop. If None, then pop 1 crumb.

        if *BOOL gothere* is true, then move cursor to the last popped
        breadcrumb.
        """
        self.breadcrumbs_srv.pop_breadcrumbs(num, gothere)

    def tell_editor_to_open_file(self, file_name):
        """See [AppState.tell_editor_to_open_file()] for doc.

        ..[AppState.tell_editor_to_open_file()] file:///./AppState.AppState.html#tell_editor_to_open_file"""

        try:
            source_file = open(file_name, 'r')
            source = source_file.read()
            source_file.close()
        except Exception, err:
            source = ''
# If the file was not opened successfully, treat it as an empty file
# (contrary to the docstring for tell_editor_to_open_file) because
# otherwise the regression testing gets messed up.
	if not self.multiple_buffers() and self.curr_buffer_name() != None:
	    name = self.curr_buffer_name()
	    self.close_buffer(name, 0)

	self.active_buffer_name = file_name
        self.open_buffers[self.active_buffer_name] = \
            SourceBuffEdSim.SourceBuffEdSim(app = self, buff_name=file_name,
                                            initial_contents = source,
					    instance_reporting =
					    self.instance_reporting)

        return self.active_buffer_name

    def query_buffer_from_app(self, buff_name):
	"""query the application to see if a buffer by the name of buff_name 
	exists.

        **INPUTS**

	*STR* buff_name -- name of the buffer to check

        **OUTPUTS**

	*BOOL* -- does the buffer exist?
	"""
	return buff_name in self.open_buffers_from_app()

    def open_buffers_from_app(self):
	"""retrieve a list of the names of open buffers from the
	application.

        **INPUTS**

	*none*

        **OUTPUTS**

	*[STR]* -- list of the names of open buffers
	"""
	return self.open_buffers.keys()


    def app_save_file(self, full_path = None, no_prompt = 0):
        """Save the current buffer.

        **INPUTS**
	
	*STR full_path* -- full path under which to save the file, or
	*None* to use the buffer name

	*BOOL no_prompt* -- overwrite any existing file without
	prompting.  No_prompt should only be set to true if the caller
	has already prompted the user.

	**OUTPUTS**

	*STR* -- new buffer name if successful, or None if the save 
	failed

        """
	f_path = full_path
	if f_path == None:
	    f_path = self.curr_buffer_name()
	elif not no_prompt:
	    if self.curr_buffer_name() != f_path \
		  and os.path.exists(f_path):
		print 'overwrite file %s (y/n)?' % (f_path)
		answer = sys.stdin.readline()
		answer = answer[:len(answer)-1]
	       
		while 1:
		    if answer == 'y':
			overwrite = 1
			break
		    elif answer == 'n':
			overwrite = 0
			return None
		    print "\nPlease answer 'y' or 'n'."
        try:
            source_file = open(f_path, 'w')
            source_file.write(self.curr_buffer().contents())
            source_file.close()
        except Exception, err:
            return None
	path, short = os.path.split(f_path)
	if path:
	    self.curr_dir = path
	old_name = self.curr_buffer_name()
	if not old_name or old_name != f_path:
	    self.active_buffer_name = f_path
# buffer has been renamed.  add a new reference to the open_buffers map,
# and then delete the old one
	    self.open_buffers[f_path] = self.open_buffers[old_name]
	    del self.open_buffers[old_name]
	return f_path


    def multiple_buffers(self):
      	"""does editor support multiple open buffers?

	**INPUTS**

	*none*

	**OUTPUTS**
	
	*BOOL* -- true if editor supports having multiple buffers open 
	at the same time"""
	return self.multiple

    def bidirectional_selection(self):
      	"""does editor support selections with cursor at left?

	**INPUTS**

	*none*

	**OUTPUTS**
	
	*BOOL* -- true if editor allows setting the selection at the
	left end of the selection"""
	return 0

    def app_close_buffer(self, buff_name, save):
        """Close a buffer.
        
        **INPUTS**

        STR *buff_name* -- name of buffer to close

        INT *save* -- *-1* -> don't save the buffer
                            *0* -> query user if buffer needs saving
                            *1* -> save without querying user

        **OUTPUTS**
        
        *none* -- 

        ..[SourceBuff] file:///./SourceBuff.SourceBuff.html"""

#        print '-- EdSim.close_buffer: called'
	buff = self.find_buff(buff_name)
	if buff == None:
	    return 0
	self.active_buffer_name = None
	self.open_buffers[buff_name].cleanup()
	del self.open_buffers[buff_name]
	return 1
        



