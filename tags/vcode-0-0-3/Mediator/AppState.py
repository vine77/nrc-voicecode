"""State information for the programming environment."""


import debug
from Object import Object

class AppState(Object):
    """State information for the programming environment.    

    Stores information about the state of the programming environment
    being run through the Mediator.
    
    **INSTANCE ATTRIBUTES**
    
    *STR app_name=None* -- name of the programming environment
    
    *[* [[SpeechCommand]] *] rec_utterances=[]* -- Array of recent
     utterances that have been recognised. Each utterance is a list of
     [SpeechComand] objects that speech commands that have been
     interpreted for that utterance.
    
    *{STR: * [SourceBuff] *} open_buffers={}* -- List of source buffers that
     are currently open in the programming environment.
    
    *STR curr_dir=None* -- Current directory for the programming environment
    
    *(STR) active_field=None* -- Name of the active Field. Elements of
     the array refer to a sequence of objects in the user interface
     that lead to the active field.

     If *None*, then the buffer [self.curr_buffer] has the focus. 

     Example: in VisualBasic, it might be: *('menu bar', 'File', 'Save
     as', 'file name')*.

     Example: in Emacs, it might be *('find-buffer', 'buffer-name')*
     where find-buffer is the name of the command that was invoked and
     buffer-name refers to the argument that is being asked for.

    SourceBuff curr_buffer=None -- Current source buffer

    *[(STR, INT)]* breadcrumbs -- stack of breadcrumbs. Each entry of
     the stack is a couple where the first entry is the name of the
     source buffer and the second is the position in that buffer where
     the crumb was dropped.

    **CLASSS ATTRIBUTES**
    
    *none* --

    .. [SpeechCommand] file:///./SpeechCommand.SpeechCommand.html
    .. [SourceBuff] file:///SourceBuff.SourceBuff.html
    .. [self.curr_buffer] file:///AppState.AppState.html"""
    
    def __init__(self, app_name=None, rec_utterances=[], open_buffers={},\
                 curr_dir=None, active_field=None, curr_buffer=None, breadcrumbs = [], **attrs):
        self.deep_construct(AppState, \
                            {'app_name': app_name,\
                             'rec_utterances': rec_utterances, \
                             'open_buffers': open_buffers,\
                             'curr_dir': curr_dir, \
                             'active_field': active_field, \
                             'curr_buffer': curr_buffer,\
                             'breadcrumbs': breadcrumbs},
                            attrs)




    def focus_is_source(self, lang_name):
        """Check if prog. env. focus is a source buffer

        Returns *true* if and only if focus of programming environment
        is a source buffer written in language *STR lang_name*.
        """

        if (self.active_field != None):
            answer = (lang_name == None) or (self.curr_buffer.is_languaage(lang_name))
        return answer



    def move_to(self, pos, f_name=None):
        """Move cursor to position *INT pos* of buffer *STR f_name*.

        If *f_name* is *None*, then use buffer [self.curr_buffer].
        .. [self.curr_buffer] file:///AppState.AppState.html"""

        debug.virtual('move_to')


    def find_buff(self, buff_name=None):
        """Returns the open buffer with name *STR buff_name*.
        
        If no such buffer, returns *None*.
        
        If *buff_name* is *None*, return [self.curr_buffer].

        .. [self.curr_buffer] file:///AppState.AppState.html
        """
        if (buff_name == None):
            return self.curr_buffer
        elif (self.open_buffers.has_key(buff_name)):
            return self.open_buffers[buff_name]
        #
        # Buffer not found
        #
        return None


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

        debug.virtual('insert_indent')
        
        
    def insert(self, text, start=None, to=None, f_name=None):
        """Replace text in source buffer with name *STR f_name*
        between positions *INT start* and *INT to* with text *STR
        text*.
        
        If *f_name* is *None*, use source buffer [self.curr_buffer].
        
        If *to* is *None*, use attribute [self.cur_pos] of the source buffer.
        
        If *start* is *None*, use attribute [self.cur_pos] of source buffer.

        .. [self.cur_pos] AppState
        .. [self.curr_buffer] AppState"""
        debug.virtual('insert')

    def indent(self, start, end, f_name=None):
        """Indent code in a source buffer region.

        Indent code in source buffer with name *STR f_name* between
        positions *INT start* and *INT end*.
        
        If *f_name* is *None*, use source buffer [self.curr_buffer].
        
        .. [self.curr_buffer] AppState"""
        debug.virtual('indent')


    def delete(self, start=None, end=None, f_name=None):
        """Delete text in a buffer.

        Delete text from position *INT start* to position *INT end* in
        source buffer with name *STR f_name*.

        If *f_name* is *None*, use buffer [self.curr_buffer].

        If *end* is *None*, delete til end of buffer.

        If *start* is *None*, delete from position [self.cur_pos] of the
        buffer.
        .. [self.cur_pos] AppState        
        .. [self.curr_buffer] AppState"""
        
        debug.virtual('delete')
        
    def goto(self, pos, f_name=None):

        """Moves the cursor to position *INT pos* of source buffer
        associated to file with name *STR f_name*.

        If *f_name* is *None*, use [self.curr_buffer].

        .. [self.curr_buffer] AppState"""
        
        debug.virtual('goto')



    def select(self, start, end, f_name=None):
        """Selects from position *INT start* up to *INT end* of source buffer
        associated to file with name *STR f_name*.

        If *f_name* is *None*, use [self.curr_buffer].

        .. [self.curr_buffer] AppState"""
                
        debug.virtual('select')


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
        
        debug.virtual('search_for')


    def drop_breadcrumb(self, buffname=None, pos=None):

        """Drops a breadcrumb

        *INT pos* is the position where to drop the crumb. *STR
         buffname* is the name of the source buffer.
        
        If *pos* not specified, drop breadcrumb at position
        [self.cur_pos] of buffer.

        If *buff* not specified either, drop breadcrumb [self.curr_buffer].

        .. [SourceBuff] file:///SourceBuff.SourceBuff.html
        .. [self.cur_pos] AppState        
        .. [self.curr_buffer] AppState"""

        buff = self.find_buff(buffname)
        buffname = buff.file_name
        if not pos: pos = buff.cur_pos
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



    def open_file(self, name):
        """Open a file.

        Open file with name *STR name*.        
        """
        debug.virtual('AppState.open_file')




    def select_region(self, start, end):
        """Sets the selection in current buffer to a particular region.
        
        **INPUTS**
        
        *INT* start -- start of region 
        
        *INT* end -- end of region 


        **OUTPUTS**
        
        *none* -- 
        """
        
        self.curr_buffer.selection_start = start
        self.curr_buffer.selection_end = end
        self.goto(start)
