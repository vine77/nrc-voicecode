import re, string, sys

from Object import Object

file_language = {'c': 'C', 'h': 'C', 'py': 'python'}

#
# When printing the content of the current buffer, only print this number of
# lines before and after the current line
#
print_window_size = 3


class SourceBuff(Object):
    """Class representing a source buffer.

    This class implements methods for manipulating buffer containing
    source code in some programming language.
    
    **INSTANCE ATTRIBUTES**
    
    *STR file_name=None* -- Name of the source file loaded into buffer
    *STR language=None* -- Name of language of the source file
    *INT cur_pos=0* -- Cursor position (in number of chars) in the buffer
    *INT visible_start=None* -- Start position (in number of chars) of the visible portion of the source buffer
    *INT visible_end=None* -- End position (in number of chars) of the visible portion of the source buffer
    *INT selection_start=None* -- Start position (in number of chars) of the current selection
    *INT selection_end=None* -- End position (in number of chars) of the current selection
    *STR content=None* -- Content of the source buffer

    CLASS ATTRIBUTES**
    
    *{STR: STR}* file_language -- key is a standard file extension and
    value is the programming language associated with that extension
    """
    
    def __init__(self, file_name=None, language=None, cur_pos=0, visible_start=0, visible_end=0, selection_start=None, selection_end=None, content=None, **attrs):
        self.deep_construct(SourceBuff,
                            {'file_name': file_name, \
                             'language': language, \
                             'cur_pos': cur_pos, \
                             'visible_start': visible_start, \
                             'visible_end': visible_end, \
                             'selection_start': selection_start, \
                             'selection_end': selection_end, \
                             'content': content}, \
                            attrs \
                            )


        #
        # Set the language name if it hasn't been set already
        #
        if self.language == None and self.file_name != None:
            self.language = self.language_name(file_name)
            


    #
    # Note: this method can be called even if *self* is not an actual
    #       class.
    #
    def language_name(self, file_name):
        """Returns the name of the language a file is written in
        
        **INPUTS**
        
        *STR* file_name -- name of the file 
        

        **OUTPUTS**

        *STR* -- the name of the language
        """
        global file_language

        language = None
        if file_name != None:
            a_match = re.match('^.*?\.([^\.]*)$', file_name)
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



    def distance_to_selection(self, start, *opt_end):
        """Coputes the distance of a region to the current selection.
        
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
        if self.selection_start != None and self.selection_end != None:
            start2 = self.selection_start
            end2 = self.selection_end
        else:
            start2 = self.cur_pos
            end2 = self.cur_pos
        return self.region_distance(start, end, start2, end2)
        

    def print_buff(self, from_line=None, to_line=None):
        """Prints buffer to STDOUT
        
        **INPUTS**
        
        *INT* from_line = None -- First line to be printed. If *None*, then
        print *print_window_size* lines around cursor.

        *INT* to_line = None -- Last line to be printed.

        **OUTPUTS**
        
        *none* -- 
        """

        #
        # Figure out the first and last line to be printed
        #
        if from_line == None:
           from_line, to_line = self.lines_around_cursor()

        #
        # Figure out the text before/withing/after the selection
        #
        if self.selection_start != None or self.selection_end != None:
            if self.selection_start <= self.selection_end:
                selection_start = self.selection_start
                selection_end = self.selection_end
            else:
                selection_start = self.selection_end
                selection_end = self.selection_start
        else:
            selection_start = self.cur_pos
            selection_end = self.cur_pos

        before_content = self.content[:selection_start]
        selection_content = self.content[selection_start:selection_end]
        after_content = self.content[selection_end:]
        
        sys.stdout.write("*** Start of source buffer ***\n")

        #
        # Print region before the selection.
        #
        curr_line_num = 1
        lines_with_num = self.number_lines(before_content, startnum=curr_line_num)
        for aline in lines_with_num[:len(lines_with_num)-1]:
            if curr_line_num >= from_line and curr_line_num <= to_line:
                sys.stdout.write('%3i: %s\n' % (aline[0], aline[1]))
            curr_line_num = curr_line_num + 1
            
        if len(lines_with_num) > 0 and curr_line_num >= from_line and curr_line_num <= to_line:
             lastline = lines_with_num[len(lines_with_num)-1]
             sys.stdout.write('%3i: %s' % (lastline[0], lastline[1]))
             curr_line_num = curr_line_num + 1
        
        if selection_content == '':
            sys.stdout.write('<CURSOR>')            
        else:
            sys.stdout.write('<SEL_START>')

        #
        # Print the selection
        #
        lines_with_num = self.number_lines(selection_content, startnum=curr_line_num)
        if (len(lines_with_num) > 0 and curr_line_num >= from_line and curr_line_num <= to_line):
            firstline = lines_with_num[0]
            sys.stdout.write('%s\n' % firstline[1])
            for aline in lines_with_num[1:]:
                if curr_line_num >= from_line and curr_line_num <= to_line:
                    sys.stdout.write('%3i: %s\n' % (aline[0], aline[1]))
                curr_line_num = curr_line_num + 1
        if selection_content != '': sys.stdout.write('<SEL_END>')

        #
        # Print region after the selection
        #
        lines_with_num = self.number_lines(after_content, startnum=curr_line_num)
        if (len(lines_with_num) > 0 and curr_line_num >= from_line and curr_line_num <= to_line):
            firstline = lines_with_num[0]
            sys.stdout.write('%s\n' % firstline[1])
            for aline in lines_with_num[1:]:
                if curr_line_num >= from_line and curr_line_num <= to_line:
                    sys.stdout.write('%3i: %s\n' % (aline[0], aline[1]))
                curr_line_num = curr_line_num + 1
        sys.stdout.write("\n*** End of source buffer ***\n")
        


    def lines_around_cursor(self):
        """Returns the line numbers of lines around cursor
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *(INT from_line, INT to_line)*

        *INT from_line* -- First line of the window.

        *INT to_line* -- Last line of the window.
        """

        curr_line = self.line_num_of(self.cur_pos)
        from_line = self.make_within_range(curr_line - print_window_size)
        to_line = self.make_within_range(curr_line + print_window_size)
        return from_line, to_line
        
        
    def line_num_of(self, position):
        """Returns the line number for a particular cursor position
        
        **INPUTS**
        
        *INT* position -- The position.
        

        **OUTPUTS**
        
        *INT line_num* -- The line number of that position
        """
        
        #
        # Make sure the position is within range
        #
        position = self.make_within_range(position)
        
        #
        # Find line number of position
        #        
        lines = string.split(self.content, '\n')
        line_start_pos = None
        line_end_pos = 0
        curr_line = 0
        for a_line in lines:
            curr_line = curr_line + 1
            line_start_pos = line_end_pos
            line_end_pos = line_end_pos + len(a_line) + 1
            if position >= line_start_pos and position <= line_end_pos:
                line_num = curr_line
                break
            
        return line_num

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


    def make_within_range(self, position):
        """Makes sure a position is within the buffer's range.
        
        **INPUTS**
        
        *INT* position -- The position. If outside of bounds, bring it back
        to the first or last position of the buffer.
        

        **OUTPUTS**
        
        *INT* position -- The possibly corrected position
        """

        if position < 0:
            position = 0
        elif position > len(self.content) - 1 and len(self.content) > 0:
            position = len(self.content) - 1
        return position

        
        
