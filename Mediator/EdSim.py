"""VoiceCode editor simulator."""

import os, posixpath, sys
import debug
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
        AppState.__init__(self)
        self.def_attrs({})
        self.init_attrs(attrs)

    def move_to(self, pos, f_name=None):
        """Move cursor to position *INT pos* of buffer *STR f_name*.

        If *f_name* is *None*, then use buffer [self.curr_buffer].

        .. [self.curr_buffer] file:///AppState.AppState.html"""

        buff = self.find_buff(f_name)
        buff.cur_pos = pos



    def find_buff(self, buff_name=None):
        """Returns the open buffer with name *STR buff_name*.
        
        If no such buffer, returns *None*.
        
        If *buff_name* is *None*, return [self.curr_buffer].

        .. [self.curr_buffer] file:///AppState.AppState.html
        """
        if (buff_name == None):
            return self.curr_buffer
        else:
            for a_buff in self.open_buffers:
                if (a_buff.file_name == buff_name):
                    return a_buff
        #
        # Buffer not found
        #
        return None

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

        """Moves the cursor to position *INT pos* of source buffer
        associated to file with name *STR f_name*.

        If *f_name* is *None*, use [self.curr_buffer].        

        .. [self.curr_buffer] file:///AppState.AppState.html"""
        
        buff = self.find_buff(f_name)
        if (pos < 0):
            pos = 0
        elif (pos > len(buff.content)):
            pos = len(buff.content)
        buff.cur_pos = pos



    def search_for(self, regexp, f_name=None):
        
        """Moves cursor to the next occurence of regular expression
           *STR regexp* in buffer with file name *STR f_name*.

           Returns 1 if and only if an occurence was found, and 0 otherwise.               
           If *f_name* is *None*, [self.curr_buffer.
           
        .. [self.curr_buffer] file:///AppState.AppState.html"""
        success = 0
        buff = find_buff(f_name)
        the_match = re.search(buff.cont, re.compile(regexp), pos=buf.cur_pos)
        if (the_match):
            success = 1
            buff.cur_pos = buff.cur_pos + the_match.start() + 1
        return success
        


    def drop_breadcrumb(self, buff=None, pos=None):

        """Drops a breadcrumb at position *INT pos* in source buffer
        [SourceBuff] *buff*.
        
        If *pos* not specified, drop breadcrumb at position
        [cur_pos] of buffer.

        If *buff* not specified either, drop breadcrumb [self.curr_buffer].

        .. [SourceBuff] file:///SourceBuff.SourceBuff.html
        .. [cur_pos] file:///SourceBuff.SourceBuff.html
        .. [self.curr_buffer] file:///AppState.AppState.html"""
        Debug.notImplementedYet()
              
    def open_file(self, name, lang='C'):
        """Open a file.

        Open file with name *STR name* and written in language *STR lang*.        
        """
        self.curr_buffer =  SourceBuff(file_name=name, language=lang)
        source_file = open(name)
        source = source_file.read()
        source_file.close()
        self.curr_buffer.content = source
        
    def print_buff_content(self, file_name=None):
        """Prints the content of a source  buffer to the VoiceCode console.

        *[STR file_name]* is the name of the source file for the buffer to
        print. If *None*, then print current buffer.    
        """

        Debug.not_implemented('print_buff_content')
        buff = self.find_buff(file_name)
        pos = buff.cur_pos
        cont = self.curr_buffer.content
        sys.stdout.write("*** Start of source buffer ***\n")
        sys.stdout.write(cont[:pos])
        sys.stdout.write('<CURSOR>')
        sys.stdout.write(cont[pos+1:])
        sys.stdout.write("\n*** End of source buffer ***\n")



###############################################################################
# Regression testing
###############################################################################        

def self_test():
    """Self test for EdSim.py."""

    test_buff = posixpath.expandvars('$VCODE_HOME' + os.sep + 'Data' + os.sep + 'TestData' + os.sep + 'small_buff.c')
    sim = EdSim()
    test_buff2 = posixpath.expandvars('$VCODE_HOME' + os.sep + 'Data' + os.sep + 'TestData' + os.sep + 'small_buff2.c')

    print "sim.open_file(%s)" % test_buff
    sim.open_file(test_buff)    
    sim.print_buff_content()

    print "sim.move_to(5)"
    sim.move_to(5)
    sim.print_buff_content()

if (__name__ == '__main__'):
    self_test()
