"""State information for the programming environment."""


import debug, sys
from Object import Object


"""can we auto-forward stuff from App to buff"""

# (C)2000 David C. Fox

class ForwardToBuffer:
    """subsidiary class used to forward buffer-specific messages from
    AppState to SourceBuff

    **INSTANCE ATTRIBUTES**

    *AppState* application -- forwarding application

    *FCT* ( *SourceBuff* , ...) -- method to call

    **CLASS ATTRIBUTES**
    
    *none* --

    """
    def __init__(self, application, method):
	self.application = application
	self.method = method
    def __call__(self, *positional, **keys):
	f_name = None
	if keys.has_key("f_name"):
	    which = keys["f_name"]
	    del keys["f_name"]
	buffer = self.application.find_buff(f_name)
	if buffer:
	    return apply(getattr(buffer, self.method), positional, keys)
	
class AppState(Object):
    """State information for the programming environment.    

    Stores information about the state of the programming environment
    being run through the Mediator.
    
    **INSTANCE ATTRIBUTES**
    
    *STR app_name=None* -- name of the programming environment
    
    *[(STR,* [Context], [Action]*) *] history=[]* -- Array of recent
    commands that have been executed. Each is entry is a 2ple. The first
    entry is the context in which the command was applied. The third
    entry is the action that was executed.
    
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

    *INT* max_history=100 --  Maximum length of the command history.

    *BOOL* translation_is_off -- If true, then translation of CSCs and
     LSAs isturned off for that applications. Everything should be
     typed as dictated text, except for commands that turn the
     translation back on (NOT IMPLEMENTED FOR NOW).

    **CLASS ATTRIBUTES**
    
    *(STR)* buffer_methods -- list of names of buffer methods which
    AppState should forward to SourceBuff.  Subclasses of AppState
    should include those from AppState and add their own 

    .. [Action] file:///./actions_gen.Action.html
    .. [Context] files:///./Context.Context.html
    .. [SourceBuff] file:///SourceBuff.SourceBuff.html
    .. [self.curr_buffer] file:///AppState.AppState.html"""

    buffer_methods = ['is_language', 'region_distance', 'cur_pos',
    'get_selection', 'goto_end_of_selection', 'set_selection', 
    'contents', 'get_text', 'distance_to_selection', 'get_visible',
    'make_position_visible', 'line_num_of', 'len', 'make_within_range', 
    'move_relative', 'insert', 'indent', 'insert_indent', 
    'delete', 'goto', 'goto_line', 'move_page', 'search_for',
    'refresh_if_needed', 'refresh']

    def __getattr__( self, name):
	if name in self.buffer_methods:
	    return ForwardToBuffer(self, name)
	raise AttributeError(name)
    
    def __init__(self, app_name=None, translation_is_off=0, curr_dir=None,
                 active_field=None, curr_buffer=None, max_history=100,
                 **attrs):
        self.init_attrs({'breadcrumbs': [], 'history': []})
        self.deep_construct(AppState, 
                            {'app_name': app_name,
                             'rec_utterances': [], 
                             'open_buffers': {},
                             'curr_dir': curr_dir, 
                             'active_field': active_field,
                             'curr_buffer': curr_buffer,
                             'max_history': max_history, 
                             'translation_is_off': translation_is_off},
                            attrs)


    def bidirectional_selection(self):
      	"""does editor support selections with cursor at left?

	**INPUTS**

	*none*

	**OUTPUS**
	
	*BOOL* -- true if editor allows setting the selection at the
	left end of the selection"""
	debug.virtual('AppState.bidirectional_selection')

    def focus_is_source(self, lang_name):
        """Check if prog. env. focus is a source buffer

        Returns *true* if and only if focus of programming environment
        is a source buffer written in language *STR lang_name*.
        """

        if (self.active_field != None):
            answer = (lang_name == None) or (self.curr_buffer.is_languaage(lang_name))
        return answer

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

    def drop_breadcrumb(self, buffname=None, pos=None):

        """Drops a breadcrumb

        *INT pos* is the position where to drop the crumb. *STR
         buffname* is the name of the source buffer.
        
        If *pos* not specified, drop breadcrumb at cursor position.

        If *buff* not specified either, drop breadcrumb in current buffer
	"""
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

    def active_language(self):
        """Returns name of active programming language.

        If no active programming language, then returns *None*.
        
        **INPUTS**
        
        *none* -- 
        
        **OUTPUTS**
        
        *STR* language -- Name of active programming language (*None*
        if no programming language is active).
        """
        
        language = None
        if self.curr_buffer != None:
            language = self.curr_buffer.language
        return language



    def log_cmd(self, cont, action):
        """Logs a command in the application's history
        
        **INPUTS**
        
        [Context] cont -- Context in which the command was invoked.
        
        [Action] action -- Action that was executed in response to the command

        **OUTPUTS**
        
        *none* -- 
        """
        
        if len(self.history) > self.max_history:
            self.history = self.history[:len(self.history)-1]
        self.history.append((cont, action))


    def get_history(self, nth):
        """Gets the *nth* most recent entry in the application's command
        history
        
        **INPUTS**
        
        *INT* nth -- Index of the requested entry (from the end)
        

        **OUTPUTS**
        
        *(* [Context], [Action]*)* hist_entry -- The context and action of the *nth* most
        recent command in the application's command history.

        .. [Context] file:///./Context.Context.html
        .. [Action] files:///./Action.Action.html"""

        hist_entry = None
        if nth <= len(self.history):
            hist_entry = self.history[len(self.history) - nth - 1]
        return hist_entry
