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


import re, string, sys

from Object import Object
import SourceBuffIndent
import find_difference


#
# default value of window_size (unless overridden by the constructor argument)
#
print_window_size = 3


class SourceBuffEdSim(SourceBuffIndent.SourceBuffIndent):
    """concrete class representing a disconnected source buffer for the
    editor simulator EdSim.

    **INSTANCE ATTRIBUTES**
    
    *INT pos=0* -- Cursor position (in number of chars) in the buffer
    *(INT, INT)* selection_range -- the current selection as
      character offsets into contents.
    *STR content=None* -- Content of the source buffer
    *INT window_size* -- When printing the content of the current buffer, 
     only print this number of lines before and after the current line
    *BOOL global_selection* -- makes the 'visible' region the whole
    buffer (useful for regression testing)

    CLASS ATTRIBUTES**

    *none*
    """
    
    def __init__(self, indent_level=3, indent_to_curr_level=1, init_pos=0,
                 init_selection = None, initial_contents="",
                 window_size = print_window_size, global_selection = 1,
                 **attrs):


        self.deep_construct(SourceBuffEdSim,
                            {'pos': init_pos, 
                             'selection': init_selection, 
                             'content': initial_contents, 
			     'window_size': window_size, 
			     'global_selection': global_selection,
                             'indent_level': indent_level,
                             'indent_to_curr_level': indent_to_curr_level,
			     }, 
                            attrs
                            )

	self.pos = self.make_within_range(self.pos)
	if not self.selection:
	    self.selection = (self.pos, self.pos)
	s, e = self.get_selection()
	if (s < e):
	    self.selection = (self.pos, self.pos)

    def cur_pos(self):
	return self.pos

    def get_selection(self):
	return self.selection
    
    def set_selection(self, range, cursor_at = 1):
	start, end = self.make_valid_range(range)
	self.selection = (start, end)
	self.pos = end

    def get_text(self, start = None, end = None):
	if start == None:
	    start = 0
	if end == None:
	    end = self.len()
	start, end = self.make_valid_range((start, end))
	return self.content[ start: end]

    def set_text(self, text, start = None, end = None):
	if start == None:
	    start = 0
	if end == None:
	    end = self.len()
	start, end = self.make_valid_range((start, end))
	before = self.content[0:start]
        after = self.content[end:]
        self.content = before + text + after

    def get_visible(self):
	if self.global_selection:
	    return (0, self.len())
	top, bottom = self.lines_around_cursor()
        lines = string.split(self.contents(), '\n')
	s = 0
	for line in lines[0: top -1]:
	    s = s + len(line) + 1
	e = s
	for line in lines[top: bottom -1]:
	    e = e + len(line) + 1
	e = e + len(lines[bottom])
	return s, e

    def make_position_visible(self, position = None):
	target = self.line_num_of(position)
	top, bottom = self.lines_around_cursor()
	if target < top:
	    destination = target +self.window_size
	elif target > bottom:
	    destination = target -self.window_size
	else:
	    return
	self.goto_line(destination)

    def len(self):
	return len(self.content)

    def refresh_if_necessary(self):
	self.print_buff()

    def refresh(self):
	self.print_buff()
    
    def print_buff(self, from_line=None, to_line=None):
        """Prints buffer to STDOUT
        
        **INPUTS**
        
        *INT* from_line = None -- First line to be printed. If *None*, then
        print *window_size* lines around cursor.

        *INT* to_line = None -- Last line to be printed.

        **OUTPUTS**
        
        *none* -- 
        """

        #
        # Figure out the first and last line to be printed
        #
        if from_line == None:
           from_line, to_line = self.lines_around_cursor()

#	print from_line, to_line
        #
        # Figure out the text before/withing/after the selection
        #
	selection_start, selection_end = self.get_selection()

        before_content = self.get_text(0, selection_start)
        selection_content = self.get_text(selection_start, selection_end)
        after_content = self.get_text(selection_end)

	printed = before_content
	if selection_content == '':
	    printed = printed + '<CURSOR>'
	else:
	    printed = printed + '<SEL_START>'
	    printed = printed + selection_content
	    printed = printed + '<SEL_END>'
	printed = printed + after_content

	lines_with_num = self.number_lines(printed, startnum = 1)
        
	if from_line == 1:
	    sys.stdout.write("*** Start of source buffer ***\n")
	for aline in lines_with_num[from_line-1:to_line]:
	    sys.stdout.write('%3i: %s\n' % (aline[0], aline[1]))
	if to_line == len(lines_with_num):
	    sys.stdout.write("\n*** End of source buffer ***\n")
	return

    def lines_around_cursor(self):
        """Returns the line numbers of lines around cursor
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *(INT from_line, INT to_line)*

        *INT from_line* -- First line of the window.

        *INT to_line* -- Last line of the window.
        """

        curr_line = self.line_num_of(self.cur_pos())
        from_line = curr_line - self.window_size
        to_line = curr_line + self.window_size
	if from_line < 1:
	    from_line = 1
	last_line = self.line_num_of(self.len())
	if to_line > last_line:
	    to_line = last_line
        return from_line, to_line
        
        
    def line_num_of(self, position = None):
        """Returns the line number for a particular cursor position
        
        **INPUTS**
        
        *INT* position -- The position.
        

        **OUTPUTS**
        
        *INT line_num* -- The line number of that position
        """
        
        #
        # Make sure the position is within range
        #
	if position == None:
	    position = self.cur_pos()
        position = self.make_within_range(position)
        
        #
        # Find line number of position
        #        
        lines = string.split(self.contents(), '\n')
        line_start_pos = None
        line_end_pos = 0
	line_num = 1
        curr_line = 0
        for a_line in lines:
            curr_line = curr_line + 1
            line_start_pos = line_end_pos
            line_end_pos = line_end_pos + len(a_line) + 1
            if position >= line_start_pos and position < line_end_pos:
                line_num = curr_line
                break
            
        return line_num


    def move_relative_page(self, direction=1, num=1):
        """Moves up or down a certain number of pages
        
        **INPUTS**
        
        *INT* direction=1 -- If positive, page down. If negative, page up.
        
        *INT* num=1 -- Number of pages to move.
        

        **OUTPUTS**
        
        *none* -- 
        """

        num_lines = 2*self.window_size + 1
        self.move_relative_line(direction=direction, num=num_lines)


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
	    range = self.get_selection()
	range = self.make_valid_range(range)
	start, end = range
	before = self.get_text(0,start)
	after = self.get_text(end)
	self.content = before + text + after
	self.goto(start + len(text))

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
	    range = self.get_selection()
	range = self.make_valid_range(range)
	start, end = range
	before = self.content[0:start]
        after = self.content[end:]
        self.content = before + after
        self.goto(start)

        
    def goto(self, pos):

        """Moves the cursor to position *INT pos* of source buffer
	(and make selection empty) 
        """
        
	pos = self.make_within_range(pos)
	self.pos = pos
	self.selection = (pos, pos)

    def goto_line(self, linenum, where=-1):
        """Go to a particular line in a buffer.

        *INT linenum* is the line number.

        *INT where* indicates if the cursor should go at the end
         (*where > 0*) or at the beginning (*where < 0*) of the line.
	"""
	self.goto(0)
	ii = 1; found = 1
	while (ii < linenum and found):
	    found = self.search_for('\n', 1)
	    ii = ii + 1
        if (where > 0):
            found = self.search_for('\n', 1)
            if not found:
                self.goto(self.len())
                


