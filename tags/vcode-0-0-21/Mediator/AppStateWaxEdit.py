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
from SourceBuffAppState import SourceBuffAppState

class AppStateWaxEdit(AppState.AppState):
    """This class is a an AppState wrapper on top of WaxEdit.

    It is used to decouple from any external editor so that we can
    test it without resorting to the IPC infrastructure for
    communicating with external editors.

    Instead of an external editor, we use WaxEdit, a simple editor written
    in Python.
    
    **INSTANCE ATTRIBUTES**

    *WaxEdit* the_editor -- The WaxEdit editor wrapped into *self*.
    
    **CLASSS ATTRIBUTES**
    
    *none* -- 
    """
    buffer_methods = AppState.AppState.buffer_methods[:]
    buffer_methods.append('print_buff')
    
    def __init__(self, **attrs):
        self.deep_construct(AppStateWaxEdit, {}, attrs)

    def open_file(self, name, lang=None):
        """Open a file.

        Open file with name *STR name* and written in language *STR lang*.        
        """
        self.the_editor.open_file(name)
        self.curr_buffer =  SourceBuffAppState(app = self, file_name=name, language=lang, \
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




