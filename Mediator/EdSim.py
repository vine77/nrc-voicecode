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

    (STR, INT, INT, STR, INT, INT) *last_search* -- Remember the details of
    the last regepx search that was done with method *search_for*, so
    that if the user repeats the same search, we don't end up
    returning the same occurence over and over. The first four entries
    of the tuple correspond to the value that were passed to
    *search_for* for the following arguments: *regexp*, *direction*,
    *where*, *f_name*. In the case of *f_name*, if the passed value
    was *None*, the fourth entry will be the name of the buffer which
    was active at the time when the search was invoked. The last entry
    correspond to the position where cursor was put after last
    search.

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
        self.init_attrs({'last_search': None})        
        self.deep_construct(EdSim, {'breadcrumbs': breadcrumbs}, attrs)

    def search_for(self, regexp, direction=1, num=1, where=1, f_name=None):
        
        """Moves cursor to the next occurence of regular expression
           *STR regexp* in buffer with file name *STR f_name*.

           *INT* direction -- if positive, search forward, otherwise
            search backward

           *INT* num -- number of occurences to search for

           *INT* where -- if positive, move cursor after the occurence,
           otherwise move it before

           *STR* f_name -- name of the file in buffer where the search
            should be done. If *None*, use [self.curr_buffer].

           Returns *None* if no occurence was found. Otherwise,
           returns a match object.
           
        .. [self.curr_buffer] file:///AppState.AppState.html"""

#        print '-- EdSim.search_for: regexp=%s, direction=%s, num=%s, where=%s, f_name=%s' % (regexp, direction, num, where, f_name)
        success = None
        buff = self.find_buff(f_name)
        f_name = buff.file_name
        
        #
        # Find position of all matches
        #
        reobject = re.compile(regexp)        
        pos = 0; all_matches_pos = []
        while 1:
           a_match = reobject.search(buff.content, pos)
           if a_match and pos < len(buff.content):
               pos = a_match.start() + 1
               all_matches_pos = all_matches_pos + [(a_match.start(), a_match.end())]               
           else:
               break

#        print '-- EdSim.search_for: all_matches_pos=%s' % all_matches_pos

        #
        # Look in the list of matches for the one closest to the cursor
        # in the right direction
        #
        closest_match = None
        for ii in range(len(all_matches_pos)):
#            print '-- EdSim.search_for: closest_match=%s, buff.cur_pos()=%s, ii=%s, all_matches_pos[ii][0]=%s, all_matches_pos[ii][1]=%s' % (closest_match, buff.cur_pos(), ii, all_matches_pos[ii][0], all_matches_pos[ii][1])

            
            if direction < 0:
                if all_matches_pos[ii][0] >= buff.cur_pos():
                    #
                    # Searching backward but we have passed cursor.
                    #
                    break
                else:
                    #
                    # Searching backward and this is closest occurence
                    # before cursor yet.
                    #
                    if not self.same_as_previous_search(regexp, direction,
                                                   where, f_name,
                                                   all_matches_pos[ii]):
                        closest_match = ii
            elif direction > 0:
                if all_matches_pos[ii][0] >= buff.cur_pos():
                    #
                    # Searching forward and we have just passed cursor. So this
                    # is the closest occurence after cursor
                    #
                    if not self.same_as_previous_search(regexp, direction,
                                                   where, f_name,
                                                   all_matches_pos[ii]):
                        closest_match = ii
                        break

#        print '-- EdSim.search_for: closest_match=%s' % closest_match
        new_cur_pos = None
        if closest_match != None:
            if direction > 0:
                the_match_index = closest_match + num - 1
                if the_match_index >= len(all_matches_pos):
                    the_match_index = len(all_matches_pos) - 1
            else:
                the_match_index = closest_match - num + 1
                if the_match_index < 0:
                    the_match_index = 0

#            print '-- EdSim.search_for: the_match_index=%s' % the_match_index                                      
            if where > 0:
                new_cur_pos = all_matches_pos[the_match_index][1]
            else:
                new_cur_pos = all_matches_pos[the_match_index][0]

#        print '-- EdSim.search_for: new_cur_pos=%s' % new_cur_pos

        #
        # Log the search
        #
        self.last_search = (regexp, direction, where, f_name, new_cur_pos)
        
        if new_cur_pos != None:
            buff.goto(new_cur_pos)
            success = 1
        else:
            succses = 0
            
        return success


    def same_as_previous_search(self, regexp, direction, where, f_name, match):
        
        """Determines whether a particular match found by *search_for* is the
        same as the one found by its last invocation.
        
        **INPUTS**
        
        *STR* regexp -- The regexp for current *search_for*
        
        *INT* direction -- Direction of the search 
        
        *INT* where -- Put cursor at end or start of occurence
        
        *STR* f_name -- Name of the buffer for current search
        
        *(INT, INT)* match -- Star and end position of the match
        

        **OUTPUTS**
        
        *BOOL* -- true if this is the same match as last invocation of
        *search_for*
        """

#        print '-- EdSim.same_as_previous_search: self.last_search=%s' % repr(self.last_search)
        answer = 0
        if self.last_search != None:
            if (regexp, direction, where, f_name) == self.last_search[0:4]:
                prev_search_pos = self.last_search[4]
                if where < 0 and match[0] == prev_search_pos or \
                   where > 0 and match[1] == prev_search_pos:
                    answer = 1
#        print '-- EdSim.same_as_previous_search: returning answer=%s' % answer
        return answer
          
        

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



