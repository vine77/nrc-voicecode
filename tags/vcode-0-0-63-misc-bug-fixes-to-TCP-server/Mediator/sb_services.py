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
# (C) 2001, National Research Council of Canada
#
##############################################################################

"""Support services for [SourceBuff] subclasses.

This module defines a series of services that can be used by various
[SourceBuff] subclasses to implement concrete methods.

The concrete behaviour is factored into services as opposed to being
implemented directly as methods of [SourceBuff] subclasses. This is to
allow more flexible mixin of implementation of behaviours than can be
supported through subclassing.

For example, class SourceBuffX may need to implement some methods like
class SourceBuffY, but other methods like class SourceBuffZ. With
subclassing, SourceBuffX would have to derive from both SourceBuffY and
SourceBuffZ, which means that either SourceBuffY would have to derive from
SourceBuffZ or vice-versa (can't use multiple inheritance to make
SourceBuffX inherit from both SourceBuffY and SourceBuffZ because that would
result in method name clashes). But maybe SourceBuffY and SourceBuffZ need
to be on different branches of the inheritance hierarchy.

By implementing variants of a given methods as variants of a given
service, we make it possible for two classes to use the same variant
of a method even if they are not on the same branch of the inheritance
hierarchy. Without such an approach, the code implementing that
variant would have to be cloned and copied to the two classes.


..[SourceBuff] file:///./SourceBuff.SourceBuff.html"""

import Object
import re

class SB_Service(Object.Object):
    """Support service for SourceBuff classes.

    Class for defining some sort of service that can be used by various
    [SourceBuff] subclasses to implement concrete methods.

    For more details on *SB_Service*'s reason for existence,
    consult documentation of the [sb_services] module.
    
    **INSTANCE ATTRIBUTES**
    
    [SourceBuff] *buff* -- The buffer for which we are providing the service.

    CLASS ATTRIBUTES**
    
    *none* -- 


    ..[SourceBuff] file:///./SourceBuff.SourceBuff.html
    ..[sb_services] file:///./sb_services.sb_services.html"""
    
    def __init__(self, buff=None, **args_super):        
        self.deep_construct(SB_Service, 
                            {'buff': buff}, 
                            args_super, 
                            {})



class SB_ServiceLang(SB_Service):

    """Provides services for determining the programming language of a
    particular buffer.

    This service is implemented completely at the VoiceCode level so
    that it can be used by [SourceBuff] classes for editors that are
    not language aware.
    
    **INSTANCE ATTRIBUTES**
    
    *none*-- 
    
    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, language_names=None, **args_super):
        self.init_attrs({'file_language': {'c': 'C', 'h': 'C', 'C': 'C', 'cpp': 'C', 'cc' : 'C', 'py': 'python'}})
                        
        self.deep_construct(SB_ServiceLang, 
                            {'language_names': language_names}, 
                            args_super, 
                            {})

    def language_name(self):
        """Returns the name of the language a file is written in
        
        **INPUTS**        

	*none*

        **OUTPUTS**

        *STR* -- the name of the language
        """

        language = None
        fname = self.buff.file_name()
        if  fname != None:
            language = self.file_language_name(fname)
        return language

    def file_language_name(self, fname):
        language = None
        a_match = re.match('^.*?\.([^\.]*)$', fname)
        extension = ""
        if a_match:
            extension = a_match.group(1)
            
        if self.file_language.has_key(extension):
            language =  self.file_language[extension]
        return language


    def is_language(self, lang):
        """Check if a source buffer is in a particular language.

        Outputs *true* if and only if *self.buff* is displaying a file
        written in programming language *STR lang*.
        """
        return (self.buff.language == lang)



class SB_ServiceLineManip(SB_Service):
        
    """Provides line numbering services.

    Some [SourceBuff] subclasses may decide to use the editor's
    line manipulation capabilities instead of the ones provided by
    this class.
    
    **INSTANCE ATTRIBUTES**
    
    *none*-- 
    
    CLASS ATTRIBUTES**
    
    *none* -- 

    ..[SourceBuff] file:///./SourceBuff.SourceBuff.html"""
                        
    def __init__(self, **args_super):
        self.deep_construct(SB_ServiceLineManip, 
                            {}, 
                            args_super, 
                            {})

    def line_num_of(self, position = None):
	"""
        Returns the line number for a particular cursor position
        
        **INPUTS**
        
        *INT* position -- The position.  (defaults to the current position)
        
        **OUTPUTS**
        
        *INT line_num* -- The line number of that position
        """
        
        #
        # Make sure the position is within range
        #
	if position == None:
	    position = self.buffcur_pos()
        position = self.buff.make_within_range(position)

        
        #
        # Find line number of position
        #
        regexp = re.compile('($|%s)' % self.buff.newline_regexp())        
        line_start_pos = 0
	line_num = 1
        curr_line = 1
        while (1):
            a_match = regexp.search(self.buff.contents(), line_start_pos)
            if not a_match:
                break
            else:
                line_end_pos = a_match.start()
                if position >= line_start_pos and position <= line_end_pos:
                    line_num = curr_line
                    break
                line_start_pos = a_match.start() + 1
                curr_line = curr_line + 1                            

        
        return line_num


    def line_num_of_old(self, position = None):
	"""
        Returns the line number for a particular cursor position
        
        **INPUTS**
        
        *INT* position -- The position.  (defaults to the current position)
        
        **OUTPUTS**
        
        *INT line_num* -- The line number of that position
        """
        
        #
        # Make sure the position is within range
        #
	if position == None:
	    position = self.buffcur_pos()
        position = self.buff.make_within_range(position)
        
        #
        # Find line number of position
        #
        regexp = re.compile(self.buff.newline_regexp())
        lines = regexp.split(self.buff.contents())
        line_start_pos = None
        line_end_pos = 0
	line_num = 1
        curr_line = 0
        for a_line in lines:
            curr_line = curr_line + 1
            line_start_pos = line_end_pos
            line_end_pos = line_end_pos + len(a_line) 
            if position >= line_start_pos and position < line_end_pos:
                line_num = curr_line
                break
            
        return line_num
	


    def number_lines(self, astring, startnum=1):
        """Assign numbers to lines in a string.

        Used mainly for the purpose of doing a printout of the buffer
        content around the cursor (usually during regression testing).

        *STR astring* is the string in question.

        *INT startnum* is the number of the first line in *astring*
        
        Returns a list of pairs *[(INT, STR)]* where first entry is
        the line number and the second entry is the line."""

        #
        # Note: need to split using regexp self.buff.newline_regexp()
        #       but for now this will do.
        #

        regexp = re.compile(self.buff.newline_regexp())
        lines = regexp.split(astring)
        result = []

        if (astring != ''):
	    lineno = startnum
#            if (if re.match(self.buff.newline_regexp(), astring):
#                lineno = startnum + 1
#  this would make all lines off by 1
                
            for aline in lines:
                result[len(result):] = [(lineno, aline)]
                lineno = lineno + 1
            
        return result


    def beginning_of_line(self, pos):
        """Returns the position of the beginning of line at position *pos*
        
        **INPUTS**
        
        *INT* pos -- Position for which we want to know the beginning of line.
        

        **OUTPUTS**
        
        *INT* beg_pos -- Position of the beginning of the line
        """

        contents = self.buff.contents()        
        from_pos = 0
        regexp = re.compile(self.buff.newline_regexp())

        #
        # Find all occurences of a newline and chose the one closest
        # to the cursor
        #
        closest = 0
        closest_dist = pos
        from_pos = 0
        while 1:            
            a_match = regexp.search(contents, pos=from_pos)
            if a_match:
                dist = pos - a_match.end()
                if dist < 0:
                    break
                if closest == None or (dist < closest_dist):
                    closest = a_match.end()
                    closest_dist = dist
                from_pos = a_match.end()
            else:
                #
                # No more matches
                #
                break                

        return closest

    def end_of_line(self, pos):
        """Returns the position of the end of line at position *pos*
        
        **INPUTS**
        
        *INT* pos -- Position for which we want to know the end of line.
        

        **OUTPUTS**
        
        *INT* end_pos -- Position of the end of the line
        """

        contents = self.buff.contents()
        a_match = re.find(self.newline_regexp(), contents, pos)
        return a_match.start()

    def goto_line(self, linenum, where=-1):
        """Go to a particular line in a buffer.

        *INT linenum* is the line number.

        *INT where* indicates if the cursor should go at the end
         (*where > 0*) or at the beginning (*where < 0*) of the line.
	"""
	self.buff.goto(0)
	ii = 1; found = 1
	while (ii < linenum and found):
	    found = self.buff.search_for('\n', 1)
	    ii = ii + 1
        if (where > 0):
            found = self.buff.search_for('\n', 1)
            if not found:
                self.buff.goto(self.buff.len())
                

class SB_ServiceIndent(SB_Service):
        
    """Provides code indentation services.

    Some [SourceBuff] subclasses may decide to use the editor's
    code indentation  capabilities instead of the ones provided by
    this class.
    
    **INSTANCE ATTRIBUTES**
    
    *INT* indent_level=None -- If not *None*, the mediator will replace tab
    characters by this number of spaces before inserting code in a source
    buffer.

    *BOOL* indent_to_curr_level=None -- If true, then when the mediator inserts
    code, it will indent it to the level of the insertion point.
    
    
    CLASS ATTRIBUTES**
    
    *none* -- 

    ..[SourceBuff] file:///./SourceBuff.SourceBuff.html"""

    def __init__(self, indent_level, indent_to_curr_level=None,
                 **attrs):
        self.deep_construct(SB_ServiceIndent,
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
        code_bef* and *str code_after*. Cursor is put right after *code_bef*.

	**INPUTS**

	*STR* code_bef -- code to be inserted before new cursor location
        
	*STR* code_bef -- code to be inserted after new cursor location

	*(INT, INT)* range -- code range to be replaced.  If None,
	defaults to the current selection.

	**OUTPUTS**

	*none*
	"""        
	if range == None:
	    range = self.buff.get_selection()
	range = self.buff.make_valid_range(range)


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
        # Now insert the code
        #
        self.buff.insert(code_bef, range)
        pos = self.buff.cur_pos()
        self.buff.insert(code_after)
        self.buff.goto(pos)


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
            code_range = self.buff.get_selection()
        code_range = self.buff.make_valid_range(code_range)

        #
        # Indent from start of first line in range
        #
        start = self.buff.beginning_of_line(code_range[0]) - 1
        if start < 0: start = 0
        end = code_range[1]
        code_to_indent = self.buff.contents()[start:end]

        #
        # Indent the code
        #
        num_spaces = levels * self.indent_level
        indented_code = self.indent_by_spaces(code_to_indent, num_spaces)

        self.buff.delete((start, end))
        self.buff.goto(start)
        self.buff.insert(indented_code)
        

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
            range = self.buff.get_selection()
        range = self.buff.make_valid_range(range)


        #
        # Unindent from start of first line in range
        #
        start = self.buff.beginning_of_line(range[0])
        end = range[1]

        code_to_unindent = self.buff.contents()[start:end]

        #
        # Unindent the code using a regexp
        #
        regexp = '(^|%s) {0,%s}' % (self.buff.newline_regexp(), levels * self.indent_level)
        unindented_code = re.sub(regexp, '\\1', code_to_unindent)
        
        self.buff.delete((start, end))
        self.buff.goto(start)
        self.buff.insert(unindented_code)
        

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

        indented_code = code
        spaces = ' ' * num_spaces
        indented_code = re.sub(self.buff.newline_regexp(), self.buff.pref_newline_convention() + spaces, indented_code)
        return indented_code


    def indentation_at(self, pos):

        """Determines the indentation level (in number of spaces) of
        line at position *pos*.
        
        **INPUTS**
        
        *INT* pos -- Position at which we want to know indentation.
        

        **OUTPUTS**
        
        *INT* num_spaces -- Number of spaces before the start of line at *pos*
        """

        content = self.buff.contents()
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
                if re.match(self.buff.newline_regexp(), content[pos]):
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
        
        return num_spaces


