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
import AppState
from SourceBuffTB import SourceBuffTB

class AppStateWaxEdit(AppState.AppState):
    """This class is a an AppState wrapper on top of WaxEdit.

    It is used to decouple from any external editor so that we can
    test it without resorting to the IPC infrastructure for
    communicating with external editors.

    Instead of an external editor, we use WaxEdit, a simple editor written
    in Python.
    
    **INSTANCE ATTRIBUTES**

    *WaxEdit* the_editor -- The WaxEdit editor wrapped into *self*.
    
    **CLASS ATTRIBUTES**
    
    *none* -- 
    """
    buffer_methods = AppState.AppState.buffer_methods[:]
    buffer_methods.append('print_buff')
    
    def __init__(self, editor, **attrs):
        self.deep_construct(AppStateWaxEdit, {'the_editor': editor}, attrs)
        self.curr_buffer =  SourceBuffTB(app = self, file_name="", \
	    underlying_buffer = self.the_editor.editor_buffer(),
	    language=None)
        self.open_buffers[""] = self.curr_buffer
      
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

    def open_file(self, name, lang=None):
        """Open a file.

        Open file with name *STR name* and written in language *STR lang*.        
        """
	path, short = os.path.split(name)
	if path:
	    self.curr_dir = path
	else:
	    path = self.curr_dir
	    name = os.path.join(path, short)
        try:
            source_file = open(name, 'rw')
            source = source_file.read()
            source_file.close()
        except Exception, err:
            source = ''
	# WaxEdit only supports one open buffer at a time
	if self.curr_buffer:
	    del self.open_buffers[self.curr_buffer.file_name]
        self.curr_buffer =  SourceBuffTB(app = self, file_name=name, 
	    underlying_buffer = self.the_editor.editor_buffer(),
	    language=lang, indent_level=3, indent_to_curr_level=1)
	self.the_editor.editor_buffer().set_text(source)

        self.open_buffers[name] = self.curr_buffer
        
    def bidirectional_selection(self):
      	"""does editor support selections with cursor at left?

	**INPUTS**

	*none*

	**OUTPUTS**
	
	*BOOL* -- true if editor allows setting the selection at the
	left end of the selection"""
	return 0




