"""VoiceCode editor simulator."""

import os, posixpath, re, sys
import auto_test, debug
from AppState import AppState
from SourceBuff import SourceBuff

class EdSim(AppState):
    """VoiceCode editor simulator.

    This class is used to simulate an external programming editor.

    Useful for debuggin VoiceCode mediator in isolation from external editor.
    
    **INSTANCE ATTRIBUTES**

    *none* -- 
    
    **CLASSS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, **attrs):
        self.deep_construct(EdSim, {}, attrs)

    def move_to(self, pos, f_name=None):
        """Move cursor to position *INT pos* of buffer *STR f_name*.

        If *f_name* is *None*, then use buffer [self.curr_buffer].

        .. [self.curr_buffer] file:///AppState.AppState.html"""

        buff = self.find_buff(f_name)
        buff.cur_pos = pos

    def insert_indent(self, code_bef, code_after, start=None, end=None, f_name=None):
        """Insert code into source buffer and indent it.

        Replace code in source buffer with name *STR f_name* between
        positions *INT start* and *INT to* with the concatenation of
        code *STR code_bef* and *str code_after*. Cursor is put right
        after code *STR bef*.
        
        If *f_name* is *None*, use source buffer [self.curr_buffer].
        
        If *to* is *None*, use attribute [self.cur_pos] of the source buffer.
        
        If *start* is *None*, use attribute [self.cur_pos] of source buffer.

        .. [self.cur_pos] AppState
        .. [self.curr_buffer] AppState"""

#        print '-- EdSim.insert_indent: code_bef=%s, code_after=%s' % (code_bef, code_after)
        buff = self.find_buff(f_name)
        start_reg = buff.cur_pos
        self.insert(code_bef, start=start, to=end, f_name=f_name)
        self.indent(start_reg, buff.cur_pos, f_name=f_name)
        self.drop_breadcrumb()
        start_reg = buff.cur_pos
        self.insert(code_after, f_name=f_name)
        self.indent(start_reg, buff.cur_pos, f_name=f_name)
        self.pop_breadcrumbs()

    def insert(self, text, start=None, to=None, f_name=None):
        """Replace text in source buffer with name *STR f_name*
        between positions *INT start* and *INT to* with text *STR
        text*.
        
        If *f_name* is *None*, use source buffer [self.curr_buffer].
        
        If *to* is *None*, use attribute [cur_pos] of the source buffer.
        
        If *start* is *None*, use attribute [cur_pos] of source buffer.

        .. [self.curr_buffer] file:///AppState.Appstate.html
        .. [cur_pos] file:///SourceBuff.SourceBuff.html"""
        
        buff = self.find_buff(f_name)
        if (start == None): start = buff.cur_pos
        if (to == None): to = buff.cur_pos
        before = buff.content[0:start]
        after = buff.content[to:]
        buff.content = before + text + after
        self.move_to(start + len(text), f_name)
        
    def indent(self, start, end, f_name=None):
        """Indent code in a source buffer region.

        Indent code in source buffer with name *STR f_name* between
        positions *INT start* and *INT end*.
        
        If *f_name* is *None*, use source buffer [self.curr_buffer].
        
        .. [self.curr_buffer] AppState"""

        #
        # In this simulator editor, we indent every line by 3 spaces
        #
        padding = '   '
        buff = self.find_buff(f_name)
        code_to_indent = buff.content[start:end]
        self.delete(start=start, end=end, f_name=f_name)
        lines_to_indent = re.split('\n', code_to_indent)

        #
        # Check to see if first bit is in the middle of a line
        #
        if len(lines_to_indent) > 0:
            a_line = lines_to_indent[0]
            if len(lines_to_indent) > 1:
                lines_to_indent = lines_to_indent[1:]
            else:
                lines_to_indent = []
            if len(buff.content) == 0 or buff.content[start - 1] == '\n':
                self.insert(padding + a_line, f_name=f_name)
            else:
                self.insert(a_line, f_name=f_name)
            for a_line in lines_to_indent:
                self.insert('\n   ' + a_line, f_name=f_name)
                if (len(code_to_indent) > 0 and code_to_indent[len(code_to_indent) - 1] == '\n'):
                    print '\n'


    def delete(self, start=None, end=None, f_name=None):
        """Delete text in a buffer.

        Delete text from position *INT start* to position *INT end* in
        source buffer with name *STR f_name*.

        If *f_name* is *None*, use buffer [curr_buffer].

        If *end* is *None*, delete til end of buffer.

        If *start* is *None*, delete from position [curr_pos] of the
        buffer.

        .. [self.curr_buffer] file:///AppState.AppState.html
        .. [cur_pos] file:///SourceBuff.SourceBuff.html"""

        buff = self.find_buff(f_name)
        if (start == None):start = buff.cur_pos
        if (end == None): end = len(buff.content)
        before = buff.content[0:start]
        after = buff.content[end:]
        buff.content = before + after
        self.move_to(start, f_name)

    def goto(self, pos, f_name=None):

        """Moves the cursor to a position in a buffer.

        *INT pos* is the position.

        *STR f_name* is the name of the file associated with the
         buffer. If *f_name* is *None*, use [self.curr_buffer].

        .. [self.curr_buffer] file:///AppState.AppState.html"""

        buff = self.find_buff(f_name)
        if (pos < 0):
            pos = 0
        elif (pos > len(buff.content)):
            pos = len(buff.content)
        buff.cur_pos = pos
        buff.selection_start = None
        buff.selection_end = None



    def goto_line(self, linenum, where=-1, f_name=None):
        """Go to a particular line in a buffer.

        *INT linenum* is the line number.

        *INT where* indicates if the cursor should go at the end
         (*where > 0*) or at the beginning (*where < 0*) of the line.
        
        *STR f_name* is the name of the file associated with the
         buffer. If *f_name* is *None*, use [self.curr_buffer].

        .. [self.curr_buffer] file:///AppState.AppState.html"""

        if (linenum == 1):
            self.goto(1, f_name=f_name)
        else:
            ii = 1; found = 1
            while (ii < linenum and found):
                found = self.search_for('\n', 1)
                ii = ii + 1
        if (where > 0):
            found = self.search_for('\n', 1)
            if not found:
                buff = self.find_buff(f_name)
                self.goto(len(buff.content) - 1)
                
    def select(self, start, end, f_name=None):
        """Selects from position *INT start* up to *INT end* of source buffer
        associated to file with name *STR f_name*.

        If *f_name* is *None*, use [self.curr_buffer].

        .. [self.curr_buffer] AppState"""

        buff = self.find_buff(f_name)
        buff.selection_start = start
        buff.selection_end = end
        buff.cur_pos= start
        self.print_buff_content()

        
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
            if (astring[0] == '\n'):
                lineno = startnum + 1
            else:
                lineno = startnum
                
            for aline in lines:
                result[len(result):] = [(lineno, aline)]
                lineno = lineno + 1
            
        return result
        
        
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

           Returns 1 if and only if an occurence was found, and 0 otherwise.                          
        .. [self.curr_buffer] file:///AppState.AppState.html"""
        
        success = 0
        buff = self.find_buff(f_name)
        reobject = re.compile(regexp)
        the_match = reobject.search(buff.content, pos=buff.cur_pos)
        if (the_match):
            success = 1
            if (where > 0):
                buff.cur_pos = the_match.end()
            else:
                buff.cur_pos = the_match.start()
        return success
        
              
    def open_file(self, name, lang=None):
        """Open a file.

        Open file with name *STR name* and written in language *STR lang*.        
        """
        self.curr_buffer =  SourceBuff(file_name=name, language=lang)
        try:
            source_file = open(name, 'rw')
            source = source_file.read()
            source_file.close()
        except Exception, err:
            source = ''

        self.curr_buffer.content = source
        self.open_buffers[name] = self.curr_buffer
        

