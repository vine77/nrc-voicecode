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
from SourceBuff import *

from Object import Object

class SourceBuffTB(SourceBuff):
    """implementation of (most of) SourceBuff as a wrapper around an
    object which inherits multiple interfaces: TextBuffer, VisibleBuffer, 
    and NumberedLines.

    **INSTANCE ATTRIBUTES**

    *TextBuffer, VisibleBuffer, NumberedLines underlying* -- underlying
    TextBuffer (also supporting VisibleBuffer and NumberedLines) 
    
    CLASS ATTRIBUTES**
    
    """
    
    def __init__(self, underlying_buffer, **attrs):
        self.deep_construct(SourceBuffTB,
                            {'underlying': underlying_buffer},
                            attrs
                            )

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
        
	if range == None:
	    range = self.get_selection()
	range = self.make_valid_range(range)
	self.insert(code_bef, range=range)
	self.app.drop_breadcrumb()
	self.insert(code_after)
	self.app.pop_breadcrumbs()
        
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

    def indent(self, range = None):
        """Indent code in a source buffer region.

	**INPUTS**

	*(INT, INT)* range -- code range to be replaced.  If None,
	defaults to the current selection.

	**OUTPUTS**

	*none*
	"""

	pass

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
