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

"""AppState wrapper over the simple pythoon-based GUI editor (WaxEdit)."""

import os, posixpath, re, sys
import auto_test, debug
import AppState, AppStateNonCached, as_services
from SourceBuffTB import SourceBuffTB

class AppStateWaxEdit(AppStateNonCached.AppStateNonCached):
    """This class is a an AppState wrapper on top of WaxEdit.

    It is used to decouple from any external editor so that we can
    test it without resorting to the IPC infrastructure for
    communicating with external editors.

    Instead of an external editor, we use WaxEdit, a simple editor written
    in Python.
    
    **INSTANCE ATTRIBUTES**

    *WaxEdit* the_editor -- The WaxEdit editor wrapped into *self*.

    *SourceBuffTB* only_buffer -- THE buffer
    
    *STR* only_buffer_name -- its name

    [AS_ServiceBreadcrumbs] breadcrumbs_srv -- Breadcrumbs service used by
    this AppState.
    
    **CLASS ATTRIBUTES**
    
    *none* -- 

    ..[AS_ServiceBreadcrumbs] file:///./AppState.AS_ServiceBreadcrumbs.html"""
    
    buffer_methods = AppState.AppState.buffer_methods[:]
    buffer_methods.append('print_buff')
    
    def __init__(self, editor, **attrs):
        self.deep_construct(AppStateWaxEdit,
                            {'the_editor': editor, 
                             'only_buffer': None, 'only_buffer_name' : "",
                             'breadcrumbs_srv': as_services.AS_ServiceBreadcrumbs(self)},
                            attrs,
                            )
        self.only_buffer =  SourceBuffTB(app = self, buff_name="", \
	    underlying_buffer = self.the_editor.editor_buffer(),
	    language=None)
        self.open_buffers[self.only_buffer_name] = self.only_buffer


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
        
        return SourceBuffTB.SourceBuffTB(app=self, buff_name=buff_name)

        
    def recog_begin(self, window_id):
        
        """Haven't figured out how to make WaxEdit block user input"""

        return 1

    def recog_end(self):
        
        """Haven't figured out how to make WaxEdit block user input"""

        pass


    def updates_from_app(self, what=[], exclude=1):
        
        """For AppStateWaxEdit, no need to get updates from external editor.

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

        
    def active_field(self):
	"""indicates what part of the editor has the focus.

	**INPUTS**

	*none*

	**OUTPUTS**

	*(STR)* -- Name of the active Field. Elements of
	the array refer to a sequence of objects in the user interface
	that lead to the active field.

	If *None*, then the buffer [self.curr_buffer] has the focus. 

	Example: in VisualBasic, it might be: *('menu bar', 'File', 'Save
	as', 'file name')*.

	Example: in Emacs, it might be *('find-buffer', 'buffer-name')*
	where find-buffer is the name of the command that was invoked and
	buffer-name refers to the argument that is being asked for.
	"""
	if not self.the_editor.is_active():
	    return ('inactive')
	if self.the_editor.editor_has_focus():
	    return None
	return ('unknown')


    def tell_editor_to_open_file(self, file_name):
        """See [AppState.tell_editor_to_open_file()] for doc.

        ..[AppState.tell_editor_to_open_file()] file:///./AppState.AppState.html#tell_editor_to_open_file"""


        buff_name = None                
	path, short = os.path.split(file_name)
	if path:
	    self.curr_dir = path
	else:
	    path = self.curr_dir
	    file_name = os.path.join(path, short)
	success = self.the_editor.open_file_in_buffer(file_name)
        
	# WaxEdit only supports one open buffer at a time
	if success:
	    if self.curr_buffer_name() != None:
		del self.open_buffers[self.curr_buffer_name()]
	    self.only_buffer =  SourceBuffTB(app = self, buff_name=file_name, 
		underlying_buffer = self.the_editor.editor_buffer(),
		indent_level=3, indent_to_curr_level=1)
	    self.only_buffer_name = file_name
            self.open_buffers[file_name] = self.only_buffer            
	    self.the_editor.set_name(short)
            buff_name = self.only_buffer.buff_name

        return buff_name

        
    def save_file(self, full_path = None, no_prompt = 0):
        """Save the current buffer.

        **INPUTS**
	
	*STR full_path* -- full path under which to save the file, or
	None to use the buffer name

	*BOOL no_prompt* -- overwrite any existing file without
	prompting.  No_prompt should only be set to true if the caller
	has already prompted the user.

	**OUTPUTS**

	*BOOL* -- true if the file was successfully saved
        """
	f_path = full_path
	quiet = no_prompt
	if not f_path:
	    f_path = self.curr_buffer_name()
	    quiet = 1
	if not quiet and f_path != self.curr_buffer_name():
	    if not os.path.exists(f_path):
		quiet = 1
	success = self.the_editor.save_file(f_path, quiet)
#         try:
#             source_file = open(name, 'rw')
#             source = source_file.read()
#             source_file.close()
#         except Exception, err:
# 	    return
	# WaxEdit only supports one open buffer at a time
	if not success:
	    return 0
	path, short = os.path.split(f_path)
	print path
	print short
	if path:
	    self.curr_dir = path
	old_name = self.curr_buffer_name()
	if not old_name or old_name != f_path:
	    self.only_buffer_name = f_path
	    self.open_buffers[f_path] = self.only_buffer
	    del self.open_buffers[old_name]
	self.the_editor.set_name(short)
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

    def drop_breadcrumb(self, buffname=None, pos=None):

        """Drops a breadcrumb

        *INT pos* is the position where to drop the crumb. *STR
         buffname* is the name of the source buffer.
        
        If *pos* not specified, drop breadcrumb at cursor position.

        If *buff* not specified either, drop breadcrumb in current buffer
	"""
        self.breadcrumbs_srv.drop_breadcrumb(self, buffname, pos)


    def pop_breadcrumbs(self, num=1, gothere=1):
        """Pops breadcrumbs from the breadcrumbs stack

        *INT num* is the number of crumbs to pop. If None, then pop 1 crumb.

        if *BOOL gothere* is true, then move cursor to the last popped
        breadcrumb.
        """
        self.breadcrumbs_srv.pop_breadcrumbs(num, gothere)



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
