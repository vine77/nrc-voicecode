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

    def drop_breadcrumb(self, buffname=None, pos=None):

        """Drops a breadcrumb

        *INT pos* is the position where to drop the crumb. *STR
         buffname* is the name of the source buffer.
        
        If *pos* not specified, drop breadcrumb at cursor position

        If *buff* not specified either, drop breadcrumb [self.curr_buffer].
	"""

        buff = self.find_buff(buffname)
        buffname = buff.file_name
        if not pos: pos = buff.cur_pos()
        self.breadcrumbs = self.breadcrumbs + [[buffname, pos]]


    def pop_breadcrumbs(self, num=1, gothere=1):
        """Pops breadcrumbs from the breadcrumbs stack

        *INT num* is the number of crumbs to pop. If None, then pop 1 crumb.

        if *BOOL gothere* is true, then move cursor to the last popped
        breadcrumb.
        """
        stacklen = len(self.breadcrumbs)
        lastbuff, lastpos = self.breadcrumbs[stacklen - num]
        self.breadcrumbs = self.breadcrumbs[:stacklen - num - 1]
        if gothere:
            self.goto(lastpos, f_name=lastbuff)



