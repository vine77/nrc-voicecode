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

    *[(STR, INT)]* breadcrumbs -- stack of breadcrumbs. Each entry of
     the stack is a couple where the first entry is the name of the
     source buffer and the second is the position in that buffer where
     the crumb was dropped.
    
    **CLASSS ATTRIBUTES**
    
    *none* -- 
    """
    buffer_methods = AppState.AppState.buffer_methods[:]
    buffer_methods.append('print_buff')
    
    def __init__(self, breadcrumbs = [], **attrs):
        self.deep_construct(EdSim, {'breadcrumbs': breadcrumbs}, attrs)

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
        
        If *pos* not specified, drop breadcrumb at position
        [self.cur_pos] of buffer.

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



