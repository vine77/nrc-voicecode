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

    *SourceBuffEdSim* only_buffer -- THE buffer
    
    *STR* only_buffer_name -- its name 

    [AS_ServiceBreadcrumbs] *breadcrumbs_srv* -- The VoiceCode level
    breadcrumbs service used by EdSim.
    
    **CLASSS ATTRIBUTES**
    
    *none* -- 
    """
    buffer_methods = AppState.AppState.buffer_methods[:]
    buffer_methods.append('print_buff')
    
    def __init__(self, **attrs):
        self.init_attrs({'breadcrumbs_srv': as_services.AS_ServiceBreadcrumbs(app=self)})
        self.deep_construct(EdSim,
                            {'only_buffer': None,
                             'only_buffer_name': ""},
                            attrs)
	self.only_buffer = SourceBuffEdSim.SourceBuffEdSim(app = self, buff_id = "",
	    language =None)
        self.open_buffers[self.only_buffer_name] = self.only_buffer

    def new_compatible_sb(self, buff_id):
        """Creates a new instance of [SourceBuff].

        Note: The class used to instantiate the [SourceBuff] needs to
        be compatible with the class of *self*. With a few exceptions
        (if any), each subclass of *AppState* will have to redefine
        *new_compatible_sb* in order to generate a [SourceBuff] of the
        appropriate class.
        
        **INPUTS**
                
        STR *buff_id* -- ID of the source buffer.
        
        **OUTPUTS**
        
        *none* -- 

        ..[SourceBuff] file:///./SourceBuff.SourceBuff.html"""
        
        return SourceBuffEdSim.SourceBuffEdSim(app=self, buff_id=buff_id)

        
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

	return self.only_buffer_name

    def change_buffer_dont_bind_from_app(self, buff_name=None):
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
        
        *none* --         
        
        file:///./AppState.AppState.html#curr_buffer_name"""

        self.only_buffer_name = buff_name
    

    def drop_breadcrumb(self, buffname=None, pos=None):

        """Drops a breadcrumb

        *INT pos* is the position where to drop the crumb. *STR
         buffname* is the name of the source buffer.
        
        If *pos* not specified, drop breadcrumb at cursor position.

        If *buff* not specified either, drop breadcrumb in current buffer
	"""
        self.breadcrumbs_srv.drop_breadcrumbs(buffname, pos)


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
	if self.curr_buffer_name() != None:
	    del self.open_buffers[self.curr_buffer_name()]

        self.only_buffer =  \
            SourceBuffEdSim.SourceBuffEdSim(app = self, buff_id=file_name,
                                            initial_contents = source)
	self.only_buffer_name = file_name
        self.open_buffers[file_name] = self.only_buffer               


        return self.only_buffer.buff_id


    def save_file(self, full_path = None, no_prompt = 0):
        """Save the current buffer.

        **INPUTS**
	
	*STR full_path* -- full path under which to save the file, or
	*None* to use the buffer name

	*BOOL no_prompt* -- overwrite any existing file without
	prompting.  No_prompt should only be set to true if the caller
	has already prompted the user.

	**OUTPUTS**

	*BOOL* -- true if the file was successfully saved
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
			return 0
		    print "\nPlease answer 'y' or 'n'."
        try:
            source_file = open(f_path, 'w')
            source_file.write(self.curr_buffer().contents())
            source_file.close()
        except Exception, err:
            return 0
	path, short = os.path.split(f_path)
	if path:
	    self.curr_dir = path
	old_name = self.curr_buffer_name()
	if not old_name or old_name != f_path:
	    self.only_buffer_name = f_path
	    self.open_buffers[f_path] = self.only_buffer
	    del self.open_buffers[old_name]
	return 1


    def multiple_buffers(self):
      	"""does editor support multiple open buffers?

	**INPUTS**

	*none*

	**OUTPUTS**
	
	*BOOL* -- true if editor supports having multiple buffers open 
	at the same time"""
	return 0

    def bidirectional_selection(self):
      	"""does editor support selections with cursor at left?

	**INPUTS**

	*none*

	**OUTPUTS**
	
	*BOOL* -- true if editor allows setting the selection at the
	left end of the selection"""
	return 0

    def close_buffer(self, buff_name, save):
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
        if self.bound_buffer_name == buff_name:
            self.bound_buffer_name = None
        self.only_buffer_name = None
        del self.open_buffers[buff_name]
        



