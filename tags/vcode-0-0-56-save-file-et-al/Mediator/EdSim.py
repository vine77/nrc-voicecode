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
import AppState
from SourceBuffEdSim import SourceBuffEdSim

class EdSim(AppState.AppState):
    """VoiceCode editor simulator.

    This class is used to simulate an external programming editor.

    Useful for debugging VoiceCode mediator in isolation from external editor.
    
    **INSTANCE ATTRIBUTES**

    *SourceBuffEdSim* only_buffer -- THE buffer
    
    *STR* only_buffer_name -- its name 


    *none* --
    
    **CLASSS ATTRIBUTES**
    
    *none* -- 
    """
    buffer_methods = AppState.AppState.buffer_methods[:]
    buffer_methods.append('print_buff')
    
    def __init__(self, **attrs):
        self.deep_construct(EdSim, {'only_buffer': None,
	    'only_buffer_name': ""}, attrs)
	self.only_buffer = SourceBuffEdSim(app = self, file_name = "",
	    language =None)
        self.open_buffers[self.only_buffer_name] = self.only_buffer

    def curr_buffer_name_from_app(self):

	"""return the name of the current buffer

        **OUTPUTS**

	*STR*  -- current buffer
	"""
	return self.only_buffer_name
    
    def open_file(self, name, lang=None):
        """Open a file.

        Open file with name *STR name* and written in language *STR lang*.        
        """
        try:
            source_file = open(name, 'r')
            source = source_file.read()
            source_file.close()
        except Exception, err:
            source = ''
	if self.curr_buffer_name() != None:
	    del self.open_buffers[self.curr_buffer_name()]


        self.only_buffer =  SourceBuffEdSim(app = self, file_name=name, language=lang, \
	    initial_contents = source)
	self.only_buffer_name = name

        self.open_buffers[name] = self.only_buffer

    def save_file(self, full_path):
        """Save the current buffer.

        Save file with path *STR full_path*.        
        """
        try:
            source_file = open(full_path, 'w')
            source_file.write(self.curr_buffer().contents())
            source_file.close()
        except Exception, err:
            return
	path, short = os.path.split(full_path)
	if path:
	    self.curr_dir = path
	old_name = self.curr_buffer_name()
	if not old_name or old_name != full_path:
	    self.only_buffer_name = full_path
	    self.open_buffers[full_path] = self.only_buffer
	    del self.open_buffers[old_name]
	    self.the_editor.set_name(short) 
	if self.curr_buffer_name() != None:
	    del self.open_buffers[self.curr_buffer_name()]

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




