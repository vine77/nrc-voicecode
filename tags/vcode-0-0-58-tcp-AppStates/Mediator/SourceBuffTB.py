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

"""State information for the programming environment."""


import debug
import re, string, sys
import sb_services, SourceBuffIndent


from Object import Object
import SourceBuffState

class SourceBuffTB(SourceBuffIndent.SourceBuffIndent):
    """implementation of (most of) SourceBuff as a wrapper around an
    object which inherits multiple interfaces: TextBuffer, VisibleBuffer, 
    and NumberedLines.

    **INSTANCE ATTRIBUTES**

    *TextBuffer, VisibleBuffer, NumberedLines underlying* -- underlying
    TextBuffer (also supporting VisibleBuffer and NumberedLines) 
    
    CLASS ATTRIBUTES**
    
    """
    
    def __init__(self, underlying_buffer, **attrs):

        self.init_attrs({'lang_srv': sb_services.SB_ServiceLang(buff=self),
                         'indent_srv': sb_services.SB_ServiceIndent(buff=self),
                         'line_srv': sb_services.SB_ServiceLineManip(buff=self)})
        self.deep_construct(SourceBuffTB,
                            {'underlying': underlying_buffer},
                            attrs
                            )
    def file_name(self):
        return self.fname

    def language_name(self):
        """Returns the name of the language a file is written in
        
        **INPUTS**
        
        *none*
        
        **OUTPUTS**
        
        *STR* -- the name of the language
        """
        return self.lang_srv.language_name()    

    def cur_pos(self):
	"""retrieves current position of cursor .  Note: the current
	position should coincide with either the start or end of the
	selection.  

	**INPUTS**

	*none*
	
	**OUTPUTS**

	*INT* pos -- offset into buffer of current cursor position
	"""

	return self.underlying.cur_pos()


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
	return self.underlying.get_selection()

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
	self.underlying.set_selection(range[0], range[1])

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
	return self.underlying.get_text(start, end)
      
    def set_text(self, text, start = None, end = None):
	"""changes a portion of the buffer.  Note: this is a low level
	interface.  Usually, higher level interfaces like insert and
	delete are preferable.

	**INPUTS**

	*STR text* is the new text.
	
	*INT start* is the offset into the buffer of the text to the
	replaced.  Defaults to start of buffer.

	*INT end* is the offset into the buffer of the character following 
	the text to be replaced (this matches Python's slice convention).
	Defaults to end of buffer.

	**OUTPUTS**

	*none*
	"""
	self.underlying.set_text(text, start, end)

    def get_visible(self):
	""" get start and end offsets of the currently visible region of
	the buffer.  End is the offset of the first character not
	visible (matching Python's slice convention)

	**INPUTS**

	*none*

	**OUTPUTS**

	*INT* (start, end)
	"""
	return self.underlying.get_visible()

    def make_position_visible(self, position = None):
	"""scroll buffer (if necessary) so that  the specified position
	is visible

	**INPUTS**

	*INT* position -- position to make visible (defaults to the
	current position)

	**OUTPUTS**

	*none*
	"""
	self.underlying.make_position_visible(position)
    
    def line_num_of(self, position = None):
	"""
        Returns the line number for a particular cursor position
        
        **INPUTS**
        
        *INT* position -- The position.  (defaults to the current position)
        
        **OUTPUTS**
        
        *INT line_num* -- The line number of that position
        """
        
	return self.underlying.line_num_of(position)
      
    def len(self):
	"""return length of buffer in characters.

	**INPUTS**

	*none*

	**OUTPUTS**

	*INT* length 
	"""
	return self.underlying.len()

    def beginning_of_line(self, pos):
        """Returns the position of the beginning of line at position *pos*
        
        **INPUTS**
        
        *INT* pos -- Position for which we want to know the beginning of line.
        

        **OUTPUTS**
        
        *INT* beg_pos -- Position of the beginning of the line
        """
        return self.line_srv.beginning_of_line(pos)


    def end_of_line(self, pos):
        """Returns the position of the end of line at position *pos*
        
        **INPUTS**
        
        *INT* pos -- Position for which we want to know the end of line.
        

        **OUTPUTS**
        
        *INT* end_pos -- Position of the end of the line
        """
        return self.line_srv.end_of_line(pos)


    def move_relative_page(self, direction=1, num=1):
        """Moves up or down a certain number of pages
        
        **INPUTS**
        
        *INT* direction=1 -- If positive, page down. If negative, page up.
        
        *INT* num=1 -- Number of pages to move.
        

        **OUTPUTS**
        
        *none* -- 
        """
        
	range = self.underlying.get_visible()
	first, last = self.underlying.line_nums_of_range(range)
	height = last -first + 1
	if direction < 0:
	    num = - num
	current = self.underlying.line_num_of()
	self.underlying.goto_line(current + num)
       
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

	if range == None:
	    start, end = self.get_selection()
	else:
	    start, end = self.make_valid_range(range)
	self.underlying.set_text(text, start, end)

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
        
        self.indent_srv.insert_indent(code_bef, code_after, range)

    def indent(self, range = None):
        """Indent code in a source buffer region.

	**INPUTS**

	*(INT, INT)* range -- code range to be replaced.  If None,
	defaults to the current selection.

	**OUTPUTS**

	*none*
	"""

        self.indent_srv.indent(range)

    def incr_indent_level(self, levels=1, range=None):
        
        """Increase the indentation of a region of code by a certain
        number of levels.
        
        **INPUTS**
        
        *INT* levels=1 -- Number of levels to indent by.
        
        *(INT, INT)* range=None -- Region of code to be indented 
        

        **OUTPUTS**
        
        *none* -- 
        """

        self.indent_srv.incr_indent_level(levels, range)

    def decr_indent_level(self, levels=1, range=None):

        """Decrease the indentation of a region of code by a certain number
        of levels.
        
        **INPUTS**hello
        
        *STR* levels=1 -- Number of levels to unindent

        *(INT, INT)* range=None -- Start and end position of code to be indent.
        If *None*, use current selection

        **OUTPUTS**
        
        *none* -- 
        """

        self.indent_srv.decr_indent_level(levels, range)


    def delete(self, range = None):
        """Delete text in a source buffer range.

	**INPUTS**

	*(INT, INT)* range -- code range to be deleted.  If None,
	defaults to the current selection.

	**OUTPUTS**

	*none*
	"""
	if range == None:
	    start, end = self.get_selection()
	else:
	    start, end = self.make_valid_range(range)
	self.underlying.set_text('', start, end)
        
    def goto(self, pos):

        """Moves the cursor to position *INT pos* of source buffer
	(and make selection empty)
        """

	self.underlying.set_selection(pos, pos)

    def goto_line(self, linenum, where=-1):
        """Go to a particular line in a buffer.

        *INT linenum* is the line number.

        *INT where* indicates if the cursor should go at the end
         (*where > 0*) or at the beginning (*where < 0*) of the line.
	"""
	self.underlying.goto_line(linenum, where)


    def _state_cookie_class(self):
	"""returns the class object for the type of cookie used by
	store_current_state.

	**INPUTS**

	*none*

	**OUTPUTS**

	*CLASS* -- class of state cookies corresponding to this
	SourceBuff

	"""
	return SourceBuffState.SourceBuffState
	
    def store_current_state(self):
	"""stores the current state of the buffer, including both the
	contents and the current selection, for subsequent restoration.
	Store_current_state returns a "cookie" which can be passed to
	restore_state or compare_with_current.  The type and attributes
	of the cookie will depend on the specific subclass of
	SourceBuff.  In the most straightforward implementation, it 
	may include a copy of the entire contents of the
	buffer and the selection.  In other cases, particularly when the
	editor or SourceBuff provides an internal undo stack, it may simply be a
	reference to a point in this stack.
	
	Important Notes:
	
        You should only pass the cookie to methods of
	the SAME SourceBuff object from which it came.  Generally,
	cookies can not be pickled and retrieved.

	The type of cookie will vary with the concrete subclass 
	of SourceBuff.  The corresponding class object is 
	returned by _state_cookie_class.  However, external callers
	should not depend on the type, attributes, or methods 
	of the cookie.

	**INPUTS**

	*none*

	**OUTPUTS**

	*SourceBuffState* -- state cookie (see above)
	"""
	cookie = SourceBuffState.SourceBuffState(file_name = self.file_name, 
	    contents = self.contents(), selection =
	    self.get_selection())
	return cookie

    def restore_state(self, cookie):
	"""restores the buffer to its state at the time when
	the cookie was returned by store_current_state.  Both the
	contents and the selection will be restored.  However, other
	data, such as the search history, may not.  The restore
	operation can fail, which will be indicated by a return value of
	0, so the caller should always check the return value.
	
	**INPUTS**

	*SourceBuffState cookie* -- see above.

	**OUTPUTS**

	*BOOL* -- true if restore was successful

	"""
	if not self.valid_cookie(cookie):
	    return 0
	self.set_text(cookie.contents())
	self.set_selection(cookie.get_selection())
	self.refresh_if_necessary()
	return 1


    def compare_with_current(self, cookie, selection = 0):
	"""compares the current buffer state to its state at the time when
	the cookie was returned by store_current_state.  By default,
	only the buffer contents are compared, not the selection, unless
	selection == 1.  If the state corresponding to the cookie has
	been lost, compare_with_current will return false.

	**INPUTS**

	*SourceBuffState cookie* -- see store_current_state.

	*BOOL* selection -- compare selection as well as contents

	**OUTPUTS**

	*BOOL* -- true if state is the same, false if it is not, or
	it cannot be determined due to expiration of the cookie
	"""
	if not self.valid_cookie(cookie):
	    return 0
# unable to make comparison, so treat as false
	if self.contents() != cookie.contents():
	    return 0
	if not selection:
	    return 1
	return self.get_selection() == cookie.get_selection()
	
    def valid_cookie(self, cookie):
	"""checks whether a state cookie is valid or expired.
	If the state corresponding to the cookie has
	been lost, valid_cookie will return false.

	**INPUTS**

	*SourceBuffState cookie* -- see store_current_state. 

	**OUTPUTS**

	*BOOL* -- true if cookie is valid (i.e. restore_state should be
	able to work)
	"""
# this is not intended to be a complete test.  Basically, valid_cookie
# is more important for SourceBuffs which have an internal undo-stack or
# change history.  In the case, however, given the brute force implementation of
# SourceBuffState, there isn't really much point in trying to detect whether 
# the caller has forged a cookie.

# do make sure that it is at least a subclass of SourceBuffState,
# otherwise other cookie-related SourceBuffTB methods will fail
	if not issubclass(cookie.__class__, self._state_cookie_class):
	    return 0

	return self.file_name == cookie.name()


    def newline_conventions(self):
        
        """Returns a list of the forms of newline the editor can
        recognise for this buffer.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        return ['\n']


    def pref_newline_convention(self):
        """Returns the form of newline that the editor prefers for this buffer.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        return '\n'

