"""State information for the programming environment."""


import debug
import re, string, sys

from Object import Object

file_language = {'c': 'C', 'h': 'C', 'py': 'python'}

def language_name(file_name):
    """Returns the name of the language a file is written in
    
    **INPUTS**
    
    *STR* file_name -- name of the file 
    
    **OUTPUTS**

    *STR* -- the name of the language
    """
    global file_language

    #
    # Create a temporary SourceBuff instance and return its language 
    #
    tmp = SourceBuff(None, file_name=file_name)
    return tmp.language_name()



class SourceBuff(Object):
    """Class representing a source buffer.

    This abstract class defines interface for manipulating buffer containing
    source code in some programming language.
    
    **INSTANCE ATTRIBUTES**
    
    *STR file_name=None* -- Name of the source file loaded into buffer
    
    *STR language=None* -- Name of language of the source file
    
    *AppState app* -- application object containing the buffer

    (STR, INT, INT, INT) *last_search* -- Remember the
    details of the last regepx search that was done with method
    *search_for*, so that if the user repeats the same search, we
    don't end up returning the same occurence over and over. The first
    3 entries of the tuple correspond to the value that were passed to
    *search_for* for the following arguments: *regexp*, *direction*,
    *where*. The last entry correspond to the position where cursor
    was put after last search.
    

    CLASS ATTRIBUTES**
    
    *{STR: STR}* file_language -- key is a standard file extension and
    value is the programming language associated with that extension
    """
    
    def __init__(self, app, file_name=None, language=None, **attrs):
        self.init_attrs({'last_search': None})        
        self.deep_construct(SourceBuff,
                            {'app': app,
			     'file_name': file_name,
                             'language': language},
                            attrs
                            )


        #
        # Set the language name if it hasn't been set already
        #
        if self.language == None and self.file_name != None:
            self.language = self.language_name()
            


    #
    # Note: this method can be called even if *self* is not an actual
    #       class.
    #
    def language_name(self):
        """Returns the name of the language a file is written in
        
        **INPUTS**        

        **OUTPUTS**

        *STR* -- the name of the language
        """
        global file_language

        language = self.language
        if language == None and self.file_name != None:
            a_match = re.match('^.*?\.([^\.]*)$', self.file_name)
            extension = a_match.group(1)
            if file_language.has_key(extension):
                language =  file_language[extension]
        return language


    def is_language(self, lang):
        """Check if a source buffer is in a particular language.

        Outputs *true* if and only if *self* is displaying a file
        written in programming language *STR lang*.
        """
        return (self.language == lang)


    def region_distance(self, region1_start, region1_end, region2_start, region2_end):
        """Computes the distance between two regions of text
        
        **INPUTS**
        
        *INT* region1_start -- start position of first region
        
        *INT* region1_end -- end position of first region
        
        *INT* region2_start -- start position of 2nd region
        
        *INT* region2_end -- end position of 2nd region
        

        **OUTPUTS**
        
        *INT* distance -- distnace between the two regions of text
        """

        distance = min(abs(region1_start - region2_start), abs(region1_start - region2_end), abs(region1_end - region2_start), abs(region1_end - region2_end))
        return distance

    def cur_pos(self):
	"""retrieves current position of cursor .  Note: the current
	position should coincide with either the start or end of the
	selection.  

	**INPUTS**

	*none*
	
	**OUTPUTS**

	*INT* pos -- offset into buffer of current cursor position
	"""

	debug.virtual('SourceBuff.cur_pos')


    def get_selection(self):
	"""retrieves range of current selection.  Note: the current
	position should coincide with either the start or end of the
	selection. 

	**INPUTS**

	*none*
	
	**OUTPUTS**

	*INT* (start, end)

	start is the offset into the buffer of the start of the current
	selection.  end is the offset into the buffer of the character 
	following the selection (this matches Python's slice convention).
	"""
	debug.virtual('SourceBuff.get_selection')	

    def bidirectional_selection(self):
	"""does editor support selections with cursor at left?

	**INPUTS**

	*none*

	**OUTPUS**
	
	*BOOL* -- true if editor allows setting the selection at the
	left end of the selection"""
	return self.app.bidirectional_selection()

    def goto_end_of_selection(self, end = 1):
	"""moves cursor to one end of the selection, clearing the
	selection.

	**INPUTS**

	*INT* end -- left (0) or right (1) end of selection

	**OUTPUT**

	*none*
	"""
	target = self.get_selection()[end]
	self.goto(target)

    def set_selection(self, range, cursor_at = 1):
	"""sets range of current selection, and sets the position to 
	beginning or end of the selection.

	**INPUTS**

	*(INT, INT)* range -- offsets into buffer of the start and end
	of the selection.  end is the offset into the buffer of the character 
	following the selection (this matches Python's slice convention).

	*INT* cursor_at -- indicates whether the cursor should be
	placed at the left (0) or right (1) end of the selection.  Note:
        cursor_at is ignored unless the application supports this
	choice, as indicated by bidirectional_selection.  
	Most Windows applications do not.

	**OUTPUTS**

	*none*
	"""
	debug.virtual('SourceBuff.set_selection')

    def get_text(self, start = None, end = None):
	"""retrieves a portion of the buffer

	**INPUTS**

	*INT start* is the start of the region returned.
	Defaults to start of buffer.

	*INT end* is the offset into the buffer of the character following 
	the region to be returned (this matches Python's slice convention).
	Defaults to end of buffer.

	**OUTPUTS**

	*STR* -- contents of specified range of the buffer
	"""
	debug.virtual('SourceBuff.get_text')

    def contents(self):
	"""retrieves entire contents of the buffer
    
	**INPUTS**

	*none*

	**OUTPUTS**

	*STR* contents 
	"""
	return self.get_text()

    def distance_to_selection(self, start, *opt_end):
        """Computes the distance of a region to the current selection.
        
        **INPUTS**
        
        *INT* start -- start position of region
        
        *[INT]* *opt_end -- end position of region (optional)
        

        **OUTPUTS**
        
        *INT* -- the distance
        """
        if len(opt_end) > 0:
            end = opt_end[0]
        else:
            end = start
        # make sure start < end and start2 < end2
        if start > end:
            tmp = end
            end = start
            start = tmp            
	start2, end2 = self.get_selection()
        # make sure start2 < end2
        if start2 > end2:
            tmp = end2
            start2 = end2
            end2 = tmp        
	if start2 == None or end2 == None:
            start2 = self.cur_pos()
            end2 = start2
        return self.region_distance(start, end, start2, end2)
        
    def get_visible(self):
	""" get start and end offsets of the currently visible region of
	the buffer.  End is the offset of the first character not
	visible (matching Python's slice convention)

	**INPUTS**

	*none*

	**OUTPUTS**

	*INT* (start, end)
	"""
	debug.virtual('SourceBuff.get_visible')

    def make_position_visible(self, position = None):
	"""scroll buffer (if necessary) so that  the specified position
	is visible

	**INPUTS**

	*INT* position -- position to make visible (defaults to the
	current position)

	**OUTPUTS**

	*none*
	"""
	debug.virtual('SourceBuff.make_position_visible')
    
    def line_num_of(self, position = None):
	"""
        Returns the line number for a particular cursor position
        
        **INPUTS**
        
        *INT* position -- The position.  (defaults to the current position)
        
        **OUTPUTS**
        
        *INT line_num* -- The line number of that position
        """
        
	debug.virtual('SourceBuff.line_num_of')

    def number_lines(self, astring, startnum=1):
        """Assign numbers to lines in a string.

        *STR astring* is the string in question.

        *INT startnum* is the number of the first line in *astring*
        
        Returns a list of pairs *[(INT, STR)]* where first entry is
        the line number and the second entry is the line.
        
        .. [self.curr_buffer] file:///AppState.AppState.html"""

        lines = re.split('\n', astring)
        result = []

        if (astring != ''):
	    lineno = startnum
#            if (astring[0] == '\n'):
#                lineno = startnum + 1
#  this would make all lines off by 1
                
            for aline in lines:
                result[len(result):] = [(lineno, aline)]
                lineno = lineno + 1
            
        return result



    def len(self):
	"""return length of buffer in characters.

	**INPUTS**

	*none*

	**OUTPUTS**

	*INT* length 
	"""
	debug.virtual('SourceBuff.len')

    def make_valid_range(self, range):
        """Makes sure a region is increasing and within the buffer's range.
	
	**INPUTS** 
	
	*(INT, INT)* range -- offsets of initial range
	
	**OUTPUTS**
	
	*(INT, INT)* -- increasing range within bounds
	"""
	start, end = range
	if end < start:
	    start, end = range[1], range[0]
	start = self.make_within_range(start)
	end = self.make_within_range(end)
	return start, end
  
    def make_within_range(self, position):
        """Makes sure a position is within the buffer's range.
        
        **INPUTS**
        
        *INT* position -- The position. If outside of bounds, bring it back
        to the first or last position of the buffer.
        

        **OUTPUTS**
        
        *INT* position -- The possibly corrected position
        """

	length = self.len()
        if position < 0:
            position = 0
# cursor can be after last character in the buffer
        elif position > length and length > 0:
            position = length  
        return position
        
    def move_relative(self, rel_movement):
        """Move cursor to plus or minus a certain number of characters

	**INPUTS** 

        *INT rel_movement* -- number of characters to move, relative to 
	current position.  If < 0 then move to the left. Otherwise, move to the
        right.

	**OUTPUTS**

	*none*
	"""
        pos = self.cur_pos()+rel_movement
	self.goto(pos)
        

# DCF - fix - never replaces selection, and independent defaults for
# start and end don't support replacing selection - 
    def insert_indent(self, code_bef, code_after, range = None):
        """Insert code into source buffer and indent it.

        Replace code in range 
        with the concatenation of
        code *STR code_bef* and *str code_after*. Cursor is put right
        after code *STR bef*.

	**INPUTS**

	*STR* code_bef -- code to be inserted before new cursor location
        
	*STR* code_bef -- code to be inserted after new cursor location

	*(INT, INT)* range -- code range to be replaced.  If None,
	defaults to the current selection.

	**OUTPUTS**

	*none*
	"""
        
        debug.virtual('insert_indent')
        
        
    def insert(self, text, range = None):
        """Replace text in range with 
        with text

	**INPUTS**

	*STR text* -- new text

	*(INT, INT)* range -- code range to be replaced.  If None,
	defaults to the current selection.

	**OUTPUTS**

	*none*
	"""

        debug.virtual('insert')

    def indent(self, range = None):
        """Indent code in a source buffer region.

	**INPUTS**

	*(INT, INT)* range -- code range to be replaced.  If None,
	defaults to the current selection.

	**OUTPUTS**

	*none*
	"""

        debug.virtual('indent')


    def delete(self, range = None):
        """Delete text in a source buffer range.

	**INPUTS**

	*(INT, INT)* range -- code range to be deleted.  If None,
	defaults to the current selection.

	**OUTPUTS**

	*none*
	"""
        debug.virtual('delete')
        
    def goto(self, pos):

        """Moves the cursor to position *INT pos* of source buffer
	(and make selection empty)
        """
        
        debug.virtual('goto')

    def goto_line(self, linenum, where=-1):
        """Go to a particular line in a buffer.

        *INT linenum* is the line number.

        *INT where* indicates if the cursor should go at the end
         (*where > 0*) or at the beginning (*where < 0*) of the line.
	"""
	debug.virtual('SourceBuff.goto_line')
                
    def refresh_if_needed(self):
	"""Refresh buffer if necessary"""
# note: this method is included primarily for the benefit of EdSim,
# which, being a line editor, needs to refresh its display by reprinting
# several lines of context around the current cursor position.  Most
# other editors will automatically refresh the screen on any change, so
# they need not override this default (no-op) behavior.
	debug.virtual('SourceBuff.refresh_if_needed')

    def refresh(self):
	"""Force a refresh of the buffer"""
	debug.virtual('SourceBuff.refresh')

    def search_for(self, regexp, direction=1, num=1, where=1):
        
        """Moves cursor to the next occurence of regular expression
           *STR regexp* in buffer.

           *INT* direction -- if positive, search forward, otherwise
            search backward

           *INT* num -- number of occurences to search for

           *INT* where -- if positive, move cursor after the occurence,
           otherwise move it before

           Returns *None* if no occurence was found. Otherwise,
           returns a match object.
           
        .. [self.curr_buffer] file:///AppState.AppState.html"""

#        print '-- SourceBuff.search_for: regexp=%s, direction=%s, num=%s, where=%s' % (regexp, direction, num, where)
        success = None
        
        #
        # Find position of all matches
        #
        reobject = re.compile(regexp)        
        pos = 0; all_matches_pos = []
        while 1:
           a_match = reobject.search(self.get_text(), pos)
           if a_match and pos < len(self.get_text()):
               pos = a_match.start() + 1
               all_matches_pos = all_matches_pos + [(a_match.start(), a_match.end())]               
           else:
               break

#        print '-- SourceBuff.search_for: all_matches_pos=%s' % all_matches_pos

        #
        # Look in the list of matches for the one closest to the cursor
        # in the right direction
        #
        closest_match = None
        for ii in range(len(all_matches_pos)):
#            print '-- SourceBuff.search_for: closest_match=%s, self.cur_pos()=%s, ii=%s, all_matches_pos[ii][0]=%s, all_matches_pos[ii][1]=%s' % (closest_match, self.cur_pos(), ii, all_matches_pos[ii][0], all_matches_pos[ii][1])

            if direction < 0:
                if all_matches_pos[ii][0] >= self.cur_pos():
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
                                                   where, all_matches_pos[ii]):
                        closest_match = ii
            elif direction > 0:
                if all_matches_pos[ii][0] >= self.cur_pos():
                    #
                    # Searching forward and we have just passed cursor. So this
                    # is the closest occurence after cursor
                    #
                    if not self.same_as_previous_search(regexp, direction,
                                                   where, all_matches_pos[ii]):
                        closest_match = ii
                        break

#        print '-- SourceBuff.search_for: closest_match=%s' % closest_match
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

#            print '-- SourceBuff.search_for: the_match_index=%s' % the_match_index                                      
            if where > 0:
                new_cur_pos = all_matches_pos[the_match_index][1]
            else:
                new_cur_pos = all_matches_pos[the_match_index][0]

#        print '-- SourceBuff.search_for: new_cur_pos=%s' % new_cur_pos

        #
        # Log the search
        #
        self.last_search = (regexp, direction, where, new_cur_pos)
        
        if new_cur_pos != None:
            self.goto(new_cur_pos)
            success = 1
        else:
            succses = 0
            
        return success


    def same_as_previous_search(self, regexp, direction, where, match):
        
        """Determines whether a particular match found by *search_for* is the
        same as the one found by its last invocation.
        
        **INPUTS**
        
        *STR* regexp -- The regexp for current *search_for*
        
        *INT* direction -- Direction of the search 
        
        *INT* where -- Put cursor at end or start of occurence
                
        *(INT, INT)* match -- Star and end position of the match
        

        **OUTPUTS**
        
        *BOOL* -- true if this is the same match as last invocation of
        *search_for*
        """

#        print '-- SourceBuff.same_as_previous_search: self.last_search=%s' % repr(self.last_search)
        answer = 0
        if self.last_search != None:
            if (regexp, direction, where) == self.last_search[0:3]:
                prev_search_pos = self.last_search[3]
                if where < 0 and match[0] == prev_search_pos or \
                   where > 0 and match[1] == prev_search_pos:
                    answer = 1
#        print '-- SourceBuff.same_as_previous_search: returning answer=%s' % answer
        return answer
          
        
