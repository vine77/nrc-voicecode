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

"""Source buffer with automatic indentation done at the Mediator level instead
of the Editor level."""


import re
import SourceBuff

class SourceBuffIndent(SourceBuff.SourceBuff):
    
    """Class representing a source buffer that knows how to indent code
    without without the need for Editor level indentation functionality.

    Use this class with editors that do not have automatic indentation
    functionality.
        
    **INSTANCE ATTRIBUTES**

    *INT* indent_level=None -- If not *None*, the mediator will replace tab
    characters by this number of spaces before inserting code in a source
    buffer.

    *BOOL* indent_to_curr_level=None -- If true, then when the mediator inserts
    code, it will indent it to the level of the insertion point.
    
    CLASS ATTRIBUTES**
    
    """
    
    def __init__(self, indent_level=None, indent_to_curr_level=None,
                 **attrs):
        self.deep_construct(SourceBuffIndent,
                            {'indent_level': indent_level,
                             'indent_to_curr_level': indent_to_curr_level},
                            attrs
                            )                    

    def insert_indent(self, code_bef, code_after, range = None):
        
        """Insert code into source buffer and indent it. We use Mediator
        level indentation functionality as opposed to Editor level one. More
        precisely:

        - code is indented at the sane level as cursor position *range[0]*
        - tab characters inside the code are replaced by *self.indent_level*
        blanks

        Replace code in range with the concatenation of code *STR
        code_bef* and *str code_after*. Cursor is put right after code
        
        *STR bef*.

	**INPUTS**

	*STR* code_bef -- code to be inserted before new cursor location
        
	*STR* code_bef -- code to be inserted after new cursor location

	*(INT, INT)* range -- code range to be replaced.  If None,
	defaults to the current selection.

	**OUTPUTS**

	*none*
	"""
#        print '-- SourceBuffIndent.insert_indent: called, self.indent_level=%s, self.indent_to_curr_level=%s' % (self.indent_level, self.indent_to_curr_level)

	if range == None:
	    range = self.get_selection()
	range = self.make_valid_range(range)

        #
        # Carry out mediator level indentation
        #
        # First replace tabs by appropriate number of space
        #
        if self.indent_level != None:
            code_bef = self.replace_tabs(code_bef)
            code_after = self.replace_tabs(code_after)

        #
        # Then indent the code by the number of blanks before the
        # insertion point.
        #
        if self.indent_to_curr_level:
            curr_level = self.indentation_at(range[0])
            code_bef = self.indent_by_spaces(code_bef, curr_level)
            code_after = self.indent_by_spaces(code_after, curr_level)

        #
        # Insert the code and invoke editor level indentation
        #
        self.insert(code_bef, range = range)
	start = range[0]
        self.indent((start, self.cur_pos()))
        self.app.drop_breadcrumb()
        start = self.cur_pos()
        self.insert(code_after)
        self.indent((start, self.cur_pos()))
        self.app.pop_breadcrumbs()


    def incr_indent_level(self, levels=1, code_range=None):
        
        """Increase the indentation of a region of code by a certain number of
        levels. This version uses Mediator level indentation functionality
        as opposed to Editor level one.
        
        **INPUTS**
        
        *INT* levels=1 -- Number of levels to indent by.
        
        *(INT, INT)* code_range=None -- Region of code to be indented 
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        #
        # AD: Note the use of *code_range* instead of *range* for the argument
        # name. Otherwise, it conflicts with the range() function in
        # for loops below.
        #
        if code_range == None:
            code_range = self.get_selection()
        code_range = self.make_valid_range(code_range)

        #
        # Indent from start of first line in range
        #
        start = self.beginning_of_line(code_range[0]) - 1
        if start < 0: start = 0
        end = code_range[1]
        code_to_indent = self.contents()[start:end]

        #
        # Indent the code
        #
        num_spaces = levels * self.indent_level
        indented_code = self.indent_by_spaces(code_to_indent, num_spaces)

        self.delete((start, end))
        self.goto(start)
        self.insert(indented_code)
        

    def decr_indent_level(self, levels=1, range=None):

        """Decrease the indentation of a region of code by a certain number of
        levels. This version uses Mediator level indentation functionality
        as opposed to Editor level one.        
        
        **INPUTS**
        
        *STR* levels=1 -- Number of levels to unindent

        *(INT, INT)* range=None -- Start and end position of code
        to be indent.  If *None*, use current selection

        **OUTPUTS**
        
        *none* -- 
        """

        if range == None:
            range = self.get_selection()
        range = self.make_valid_range(range)

        #
        # Unindent from start of first line in range
        #
        start = self.beginning_of_line(range[0])
        end = range[1]
        code_to_unindent = self.contents()[start:end]
#        print '-- SourceBuffIndent.decr_indent_level: code_to_unindent=\'%s\'' % code_to_unindent

        #
        # Unindent the code using a regexp
        #
        regexp = '(^|\n) {0,%s}' % (levels * self.indent_level)
#        print '-- SourceBuffIndent.decr_indent_level: regexp=%s' % regexp
        unindented_code = re.sub(regexp, '\\1', code_to_unindent)
#        print '-- SourceBuffIndent.decr_indent_level: unindented_code=\'%s\'' % unindented_code    

#        print '-- SourceBuffIndent.decr_indent_level: start=%s, end=%s, len(self.contents()=%s)' % (start, end, len(self.contents()))
        self.delete((start, end))
        self.goto(start)
        self.insert(unindented_code)
        

    def replace_tabs(self, code):
        """Replaces tabs in a piece of code, by the appropriate number of
        spaces. This is done solely by the mediator, i.e. we do not invoke
        the editor's indentation capabilities.
        
        **INPUTS**
        
        *STR* code -- Code for which we want to replace tabs.
        

        **OUTPUTS**
        
        *STR* fixed_code -- The code with tabs replaced.
        """

        fixed_code = code
        if self.indent_level != None:
            spaces = ' ' * self.indent_level
            fixed_code = re.sub('\t', spaces, fixed_code)
        return fixed_code


    def indent_by_spaces(self, code, num_spaces):
        """Indents each line in *code* by *num_spaces* blanks.
        
        **INPUTS**
        
        *STR* code -- code to be indented. 
        
        *INT* num_spaces -- number of spaces to indent the code by 
        

        **OUTPUTS**
        
        *STR* indented_code -- Code after indentation.
        """

#        print '-- SourceBuffIndent.indent_by_spaces: num_spaces=%s' % num_spaces
        indented_code = code
        spaces = ' ' * num_spaces
        indented_code = re.sub('\n', '\n' + spaces, indented_code)
        return indented_code


    def indentation_at(self, pos):

        """Determines the indentation level (in number of spaces) of
        line at position *pos*.
        
        **INPUTS**
        
        *INT* pos -- Position at which we want to know indentation.
        

        **OUTPUTS**
        
        *INT* num_spaces -- Number of spaces before the start of line at *pos*
        """
        
#        print '-- SourceBuffIndent.indentation_at: pos=%s' % pos
        
        content = self.contents()
        pos_newline = None
        pos_line_start = pos

        #
        # Go back from pos until we meet a newline character. Remember position
        # of closest non blank.
        #
        keep_going = 1        
        while keep_going:
            pos = pos - 1
            if pos >= 0:
                if not re.match('\s', content[pos]):
                    pos_line_start = pos
                if re.match('\n', content[pos]):
                    # reached beginning of line
                    keep_going = 0
            else:
                #
                # Reached pos = 0
                #
                keep_going = 0

        #
        # Compute number of spaces. Note that *pos* went 1 character
        # passed the beginning of the line
        #
        num_spaces = pos_line_start - (pos + 1)

#        print '-- SourceBuffIndent.indentation_at: returning num_spaces=%s' % num_spaces
        
        return num_spaces

