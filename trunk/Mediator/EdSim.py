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

    *none* --
    
    **CLASSS ATTRIBUTES**
    
    *none* -- 
    """
    buffer_methods = AppState.AppState.buffer_methods[:]
    buffer_methods.append('print_buff')
    
    def __init__(self, **attrs):
        self.deep_construct(EdSim, {}, attrs)
	self.curr_buffer = SourceBuffEdSim(app = self, file_name = "",
	    language =None)

    def open_file(self, name, lang=None):
        """Open a file.

        Open file with name *STR name* and written in language *STR lang*.        
        """
        try:
            source_file = open(name, 'rw')
            source = source_file.read()
            source_file.close()
        except Exception, err:
            source = ''
        self.curr_buffer =  SourceBuffEdSim(app = self, file_name=name, language=lang, \
	    initial_contents = source)

        self.open_buffers[name] = self.curr_buffer
        
    def bidirectional_selection(self):
      	"""does editor support selections with cursor at left?

	**INPUTS**

	*none*

	**OUTPUTS**
	
	*BOOL* -- true if editor allows setting the selection at the
	left end of the selection"""
	return 0




