"""State information for the programming environment."""


import debug
from Object import Object

class AppState(Object):
    """State information for the programming environment.    

    Stores information about the state of the programming environment
    being run through the Mediator.
    
    **INSTANCE ATTRIBUTES**
    
    *STR app_name=None* -- name of the programming environment
    
    *[* [SpeechCommand] *] history=[]* -- Array of recent speech commands
     that have been applied
    
    *[* [SourceBuff] *] open_buffers=[]* -- List of source buffers that
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

    [SourceBuff] *curr_buffer=None* -- Current source buffer

    **CLASSS ATTRIBUTES**
    
    *none* --

    .. [SpeechCommand] file:///./SpeechCommand.SpeechCommand.html
    .. [SourceBuff] file:///SourceBuff.SourceBuff.html
    .. [self.curr_buffer] file:///AppState.AppState.html"""
    
    def __init__(self, app_name=None, history=[], open_buffers=[],\
                 curr_dir=None, active_field=None, curr_buffer=None, **attrs):
        Object.__init__(self)
        self.def_attrs({'app_name': None, 'history': [], 'open_buffers': [],\
                        'curr_dir': None, 'active_field': None, 'curr_buffer': None})
        self.init_attrs(attrs)



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

        debug.not_implemented()


    def find_buff(self, buff_name=None):
        """Returns the open buffer with name *STR buff_name*.
        
        If no such buffer, returns *None*.
        
        If *buff_name* is *None*, return [self.curr_buffer].
        .. [self.curr_buffer] AppState"""
        
        debug.not_implemented()        
        
    def insert(self, text, start=None, to=None, f_name=None):
        """Replace text in source buffer with name *STR f_name*
        between positions *INT start* and *INT to* with text *STR
        text*.
        
        If *f_name* is *None*, use source buffer [self.curr_buffer].
        
        If *to* is *None*, use attribute [self.cur_pos] of the source buffer.
        
        If *start* is *None*, use attribute [self.cur_pos] of source buffer.

        .. [self.cur_pos] AppState
        .. [self.curr_buffer] AppState"""
        debug.not_implemented()


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
        
        debug.not_implemented()
        
    def goto(self, pos, f_name=None):

        """Moves the cursor to position *INT pos* of source buffer
        associated to file with name *STR f_name*.

        If *f_name* is *None*, use [self.curr_buffer].

        .. [self.curr_buffer] AppState"""
        
        debug.not_implemented()

    def search_for(self, regexp, f_name=None):
        
        """Moves cursor to the next occurence of regular expression
           *STR regexp* in buffer with file name *STR f_name*.

           Returns 1 if and only if an occurence was found, and 0 otherwise.               
           If *f_name* is *None*, [self.curr_buffer].

           .. [self.curr_buffer] AppState
        """

        debug.not_implemented()


    def drop_breadcrumb(self, buff=None, pos=None):

        """Drops a breadcrumb at position *INT pos* in source buffer
        [SourceBuff] *buff*.
        
        If *pos* not specified, drop breadcrumb at position
        [self.cur_pos] of buffer.

        If *buff* not specified either, drop breadcrumb [self.curr_buffer].

        .. [SourceBuff] file:///SourceBuff.SourceBuff.html
        .. [self.cur_pos] AppState        
        .. [self.curr_buffer] AppState"""
        debug.notImplementedYet()
              



    def open_file(self, name):
        """Open a file.

        Open file with name *STR name*.        
        """
        debug.not_implemented()


