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
# (C) 2000, National Research Council of Canada
#
##############################################################################

"""Interface to the programming environment."""


import debug, messaging, sys
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




def use_update_class(action):
    """Returns the class to be used for a particular type of update action.
        
    **INPUTS**
        
    STR *action* -- Name of the update action 
        

    **OUTPUTS**
        
    CLASS *upd_class* -- The class object (not an instannce) for
    *action*. Assumed to be a subclass of [AS_Update].
    
    ..[AS_Update] file:///./AppState.AS_Update.html"""
        
    use_class = {'delete': SB_UpdDelete, 'insert': SB_UpdInsert,
                 'set_selection': SB_UpdSetSelection, 'goto': SB_UpdGoto
                }

    
    return use_class[action]


def updates_factory(upd_descr):
        
    """Creates an AS_Update object based on the description of the
    update to be created.
    
    **INPUTS**
    
    {STR: ANY} *upd_descr* -- A description of the update object
    to be created. We assume that there is at least an 'action' key
    (used to decide which class of updates to generate).
    
    
    **OUTPUTS**
    
    *none* -- 
    """

    upd_class = use_update_class(upd_descr['action'])
    upd_object = upd_class(descr=upd_descr)
    return upd_object


class AS_Update(Object):
            
    """An object describing an update to be done on an application
    (e.g. insert some text in a source buffer).

    
    **INSTANCE ATTRIBUTES**

    {STR: ENCODABLE} *descr* -- A description of the parameters of the update.
    
    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, descr, **args_super):
        self.deep_construct(AS_Update, 
                            {'descr': descr}, 
                            args_super, 
                            {})
        
class SB_Update(AS_Update):
            
    """An object describing an update to be done on a source buffer or
    an application (e.g. insert some text in a source buffer).

    
    **INSTANCE ATTRIBUTES**

    STR *sb_name* -- Name of the source buff to be updated
    
    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, **args_super):
        self.deep_construct(SB_Update, 
                            {}, 
                            args_super, 
                            {})

    def on_buff_named(self):
        """Returns name of the buffer on which to do the update."""
        return self.descr['buff_name']


    def apply(self, on_app):

        """Carry out the update on the appropriate source buffer.

        **INPUTS**
        
        [AppState] *on_app* --
    
        **OUTPUTS**
        
        *none* --

        ..[AppState] file:///./AppState.AppState.html"""
        
        #
        # Forward SourceBuff updates to the appropriate source buffer
        #                
        buff = on_app.find_buff(self.on_buff_named())
        self.apply_to_buff(buff)

    def apply_to_buff(self, on_buff):
        
        """Carry out a buffer update on a specific buffer.
        
        **INPUTS**
        
        [SourceBuff] *on_buff* -- The buffer on which to do the update. 
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        debug.virtual('SB_Update.apply_to_buff')


    def apply_to_VE_map(self, on_app):
        
        """Update the V-E map to take into account this buffer update.
        
        **INPUTS**
        
        [AppState] *on_app* -- Application on which the update is being done.
        

        **OUTPUTS**
        
        *none* -- 
        """

        debug.virtual('SB_Update.apply_to_VE_map')
        

class SB_UpdDelete(SB_Update):
    """Update class for a deletion.
    
    **INSTANCE ATTRIBUTES**
    
    *none*-- 
    
    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, **args_super):
        self.deep_construct(SB_UpdDelete, 
                            {}, 
                            args_super, 
                            {})

    def apply_to_buff(self, on_buff):
        
        """Carry out a delete update on a specific buffer.
        
        **INPUTS**
        
        [SourceBuff] *on_buff* -- The buffer on which to do the update. 
        

        **OUTPUTS**
        
        *none* -- 
        """
        range = messaging.messarg2intlist(self.descr['range'])
        on_buff.delete_cbk(range=range)


class SB_UpdInsert(SB_Update):
    """Update class for an insertion.
    
    **INSTANCE ATTRIBUTES**
    
    *none*-- 
    
    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, **args_super):
        self.deep_construct(SB_UpdInsert,
                            {}, 
                            args_super, 
                            {})

    def apply_to_buff(self, on_buff):
        
        """Carry out an insertion update on a specific buffer.
        
        **INPUTS**
        
        [SourceBuff] *on_buff* -- The buffer on which to do the update. 
        

        **OUTPUTS**
        
        *none* -- 
        """
        range = messaging.messarg2intlist(self.descr['range'])
        on_buff.insert_cbk(range=range, text=self.descr['text'])


class SB_UpdSetSelection(SB_Update):
    """Update class for setting the selection.
    
    **INSTANCE ATTRIBUTES**
    
    *none*-- 
    
    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, **args_super):
        self.deep_construct(SB_UpdSetSelection,
                            {}, 
                            args_super, 
                            {})

    def apply_to_buff(self, on_buff):
        
        """Carry out a set selection update on a specific buffer.
        
        **INPUTS**
        
        [SourceBuff] *on_buff* -- The buffer on which to do the update. 
        

        **OUTPUTS**
        
        *none* -- 
        """

        cursor_at = None
        if self.descr.has_key('cursor_at'):
            cursor_at = int(self.descr['cursor_at'])
        range = messaging.messarg2intlist(self.descr['range'])
        if cursor_at != None:
            on_buff.set_selection_cbk(range=range, cursor_at=cursor_at)
        else:
            on_buff.set_selection_cbk(range)


class SB_UpdGoto(SB_Update):
    """Update class for moing the cursor.
    
    **INSTANCE ATTRIBUTES**
    
    *none*-- 
    
    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, **args_super):
        self.deep_construct(SB_UpdGoto,
                            {}, 
                            args_super, 
                            {})

    def apply_to_buff(self, on_buff):
        
        """Carry out a cursor movementupdate on a specific buffer.
        
        **INPUTS**
        
        [SourceBuff] *on_buff* -- The buffer on which to do the update. 
        

        **OUTPUTS**
        
        *none* -- 
        """

        on_buff.goto_cbk(pos=int(self.descr['pos']))
            
	
class AppState(Object):
    """Interface to the programming environment.    

    Implements methods for manipulating and querying a programming
    environment that is being driven by VoiceCode.

    This is mostly a virtual class providing an abstract interface to
    the programming environment.

    But some of the methods implement concrete behaviour such as:
    
    - managing the history of voice commands for that programming
      environement

    - dispatching certain methods to an appropriate source buffer
      (implemented as an instance of [SourceBuff]).

    **INSTANCE ATTRIBUTES**
    
    *STR app_name=None* -- name of the programming environment
    
    *[(STR,* [Context], [Action]*) *] history=[]* -- Array of recent
    commands that have been executed. Each is entry is a 2ple. The first
    entry is the context in which the command was applied. The second
    entry is the action that was executed.
    
    *{STR: * [SourceBuff] *} open_buffers={}* -- List of source buffers that
     are currently open in the programming environment.
    
    *INT* max_history=100 --  Maximum length of the command history.

    *BOOL* translation_is_off -- If true, then translation of CSCs and
     LSAs isturned off for that applications. Everything should be
     typed as dictated text, except for commands that turn the
     translation back on (NOT IMPLEMENTED FOR NOW).

    STR *bound_buffer_name=None* -- Name of the buffer that VoiceCode
    is currently bound to operate on. If *None*, use editor's active
    buffer. See [curr_buffer] method for a description of buffer
    binding.
     
    **CLASS ATTRIBUTES**
    
    *(STR)* buffer_methods -- list of names of buffer methods which
    AppState should forward to SourceBuff.  Subclasses of AppState
    should include those from AppState and add their own 

    .. [Action] file:///./actions_gen.Action.html
    .. [Context] file:///./Context.Context.html
    .. [SourceBuff] file:///./SourceBuff.SourceBuff.html
    .. [curr_buffer] file:///./AppState.AppState.html#curr_buffer"""

    buffer_methods = ['is_language', 'region_distance', 'cur_pos',
    'get_selection', 'goto_end_of_selection', 'set_selection', 
    'contents', 'get_text', 'distance_to_selection', 'get_visible',
    'make_position_visible', 'line_num_of', 'len', 'make_within_range', 
    'move_relative', 'insert', 'indent', 'insert_indent', 
    'delete', 'goto', 'goto_line', 'move_relative_line',
    'move_relative_page', 'search_for',
    'refresh_if_necessary', 'refresh', 'incr_indent_level',
    'decr_indent_level']

    def __getattr__( self, name):
	if name in self.buffer_methods:
	    return ForwardToBuffer(self, name)
	raise AttributeError(name)
    
    def __init__(self, app_name=None, translation_is_off=0,
                 max_history=100, **attrs):
        
        self.init_attrs({'breadcrumbs': [], 'history': []})
        self.deep_construct(AppState, 
                            {'app_name': app_name,
                             'rec_utterances': [], 
                             'open_buffers': {},
			     'bound_buffer_name': None,
                             'max_history': max_history, 
                             'translation_is_off': translation_is_off},
                            attrs)

    def recog_begin(self):
        """Invoked at the beginning of a recognition event.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        # Give the user a visual indication that he shouldn't be
        # typing/mousing.
        self.recog_indicator('on')

        #
        # Ask the editor to stop responding to user kbd and mouse events
        # (if it's able to)
        #
        self.stop_responding()


    def stop_responding(self):
        
        """When an utterance is heard, VoiceCode invokes this to ask
        the editor to stop responding to user input. This is to
        prevent a bunch of problems that can arise if the user types
        while VoiceCode is still processing an utterance. In such
        cases, the results of the utterance interpretation can be
        unpredictable, especially when it comes to correction.

        Each external editor will respond to that message as best it can.

        Ideally, the editor would:

        - Start recording user actions to a log Then execute those
        - actions later when [start_responding()] is invoked.

        If the editor is able to stop responding to user input, but is
        not able to record them and/or execute them later, then it
        should:

        - Stop responding to user input until [start_responding()] is
          later invoked.

        If the editor is not even able to stop responding to user
        input, then it should:

        - Do nothing
        

        NOTE: This method may be invoked more than once before
        [start_responding()] is invoked. In such cases, only the first
        call to the method should do anything.

        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 

        ..[start_responding()] file:///./AppState.AppState.html#start_responding"""
        
        debug.virtual('AppState.stop_responding')


    def recog_end(self):
        """Invoked at the end of a recognition event.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        # Tell the editor it can start responding to user kbd and mouse
        # events again
        self.start_responding()


        # Give the user a visual indication that he can start typing/mousing
        # again
        self.recog_indicator('off')

    def start_responding(self):
        
        """Invoked when VoiceCode has finished processing an
        utterance. This tells the editor to start responding to user
        input again, and possibly to execute any user inputs it may
        have recorded since [stop_responding()] was invoked.
        
        Each external editor will respond to that message as best it can.

        Ideally, the editor would:

        - Execute all actions that were logged
        
        - Stop recording user actions to a log, and execute them as
          they arrrive instead.
        
        If the editor is able to stop responding to user input, but is
        not able to record them and/or execute them later, then it
        should:

        - Start responding to user input again

        If the editor is not even able to stop responding to user
        input, then it should:

        - Do nothing

        NOTE: This method may be invoked more than once before
        [stop_responding()] is invoked. In such cases, only the first
        call to the method should do anything.

        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 

        ..[stop_responding()] file:///./AppState.AppState.html#stop_responding"""

        debug.virtual('AppState.start_responding')




    def recog_indicator(self, status):
        """Sets a \"recognition in progress\" visual indicator.
        
        **INPUTS**
        
        STR *status* -- 'on' or 'off'
        

        **OUTPUTS**
        
        *none* -- 
        """

        #
        # Do nothing for now
        #
        pass


    def synchronize_with_app(self, what=[], exclude=1, updates=None):

        """Make sure that VoiceCode is in sync with the state of the
        external editor.
        
        **INPUTS**
        
        [STR] *what=[]* -- List of what is to be synchronised. Valid
        entries are: 'buff_name', 'content', 'cur_pos', 'selection'.
        *exclude=1*, this should be interpreted as a list of items that
        don't need to be synchronised. If *exclude=0*, then it should be
        interpreted as a list of items that need to be syncrhonized.

        [ [AS_Update] ] updates -- Updates to be applied in the
        synchronisation. If *None*, get updates from the external
        editor.
                
        **OUTPUTS**
        
        *none* -- 
        """
        if updates == None:
            updates = self.updates_from_app(what, exclude)
        self.apply_updates(updates)



    def apply_updates(self, updates):
        """Applies a list of updates returned by the external application.
        
        **INPUTS**
        
        [ [AS_Updates] ] *updates* -- List of updates
        

        **OUTPUTS**
        
        *none* -- 

        ..[AS_Updates] file:///./AppState.AS_Updates.html"""
        
        for an_update_descr in updates:
            an_update = create_update(an_update_descr)
            an_update.apply(self)



    def updates_from_app(self, what=[], exclude=1):
        """Gets a list of updates from the external app.

        Note: the list of updates must ALWAYS include the name of the
        external app's active buffer.
        
        **INPUTS**
        
        [STR] *what* -- List of items to be included/excluded in the updates.

        BOOL *exclude* -- Indicates if *what* is a list of items to be
        included or excluded from updates.
        
        **OUTPUTS**
        
        [ [AS_Update] ] *updates* -- List of updates retrieved from the
        external app.
        
        ..[AS_Update] file:///./AppState.AS_Update.html"""
        
        debug.virtual('AppState.updates_from_app')


    def curr_buffer(self):
        """Returns the SourceBuff corresponding to the default editor buffer,
	or the current buffer if the default is not set
        
        If no such buffer, returns *None*.
        
        """
	return self.find_buff(self.curr_buffer_name())


    def curr_buffer_name(self):
        
	"""Returns the file name of the buffer that VoiceCode
	currently operates on.

        This may or may not be the same as the active buffer in the
        editor (this is returned by method [app_active_buffer_name]).

        When interpreting an utterance, VoiceCode binds the *AppState* to the
        buffer that was active in the editor at the moment when the
        utterance started. This is so that the utterance will always
        go to that buffer, even if the user clicks on a different
        buffer while the utterance is still being processed.

        Note however that if the user utters a command that switches
        the active buffer in mid-utterance, VoiceCode will then bind
        the *AppState* to that new buffer so that the rest of the utterance
        goes there.

        WARNING: DO NOT OVERRIDE THIS METHOD UNLESS YOU KNOW WHAT YOU
        ARE DOING!!!

	**OUTPUTS**

	*STR* -- file name of current buffer

        file:///./AppState.AppState.html#app_active_buffer_name"""

        #
        # Check to see if the AppState is bound to a particular buffer.
        # If not, use the editor's active buffer.
        #
        buff_name = self.is_bound_to_buffer()
        if buff_name == None:
            buff_name = self.app_active_buffer_name()

        return buff_name


    def app_active_buffer_name(self):
        
	"""Returns the file name of the buffer currently active in the
	external application.

        Note that this may or may not be the same the buffer that
        VoiceCode is currently bound to (see [curr_buffer_name]
        method for a description of buffer binding).

        **INPUTS**

        *none* --
        
	**OUTPUTS**

	*STR* -- file name of current buffer

        file:///./AppState.AppState.html#curr_buffer_name"""

        debug.virtual('AppState.app_active_buffer_name')


    def is_bound_to_buffer(self):
        """Returns the name of the buffer that AppState is currently bound to.

        See [curr_buffer] for a description of buffer binding.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 

        ..[curr_buffer] file:///./AppState.AppState.html#curr_buffer"""
        
        return self.bound_buffer_name


    def bind_to_buffer(self, buff_name):
        """Binds the AppState to a particular buffer.

        See [curr_buffer] for a description of buffer binding.
        
        **INPUTS**
        
        STR *buff_name* -- Name of the buffer to bind to.
        

        **OUTPUTS**
        
        *none* -- 

        ..[curr_buffer] file:///./AppState.AppState.html#curr_buffer"""
        
        self.bound_buffer_name = buff_name



    def change_buffer(self, buff_name, bind=1):

	"""Changes the active buffer.

        May also bind the AppState to that buffer depending on the
        value of *bind*. See [curr_buffer_name] for a description of
        buffer binding.

        **INPUTS**
        
        STR *buff_name* -- Name of the buffer to switch to.

        BOOL *bind* -- Indicates whether or not the AppState should be
        bound to operate on that new buffer or not.
        
        **OUTPUTS**
        
        *none* --         
        
        file:///./AppState.AppState.html#curr_buffer_name"""

        self.change_buffer_dont_bind(buff_name)
        if bind:
            self.bind_to_buffer(buff_name)


    def change_buffer_dont_bind(self, buff_name=None):

	"""Changes the external application's active buffer.

        This should NOT bind the *AppState* to the new buffer. This
        should be done only by [change_buffer].

        See [curr_buffer_name] for a description of buffer binding.
        
        WARNING: DO NOT OVERRIDE THIS METHOD UNLESS YOU KNOW WHAT YOU
        ARE DOING!!!

        **INPUTS**
        
        STR *buff_name=None* -- Name of the buffer to switch to.
       
        **OUTPUTS**
        
        *none* --         
        
        file:///./AppState.AppState.html#curr_buffer_name"""

        #
        # Change the buffer in the external application, then
        # synchronize.
        #
        self.change_buffer_dont_bind_from_app(buff_name)
        self.synchronize_with_app()


    def change_buffer_dont_bind_from_app(self, buff_name=None):

	"""Changes the external application's active buffer.

        This variant only changes the buffer in the external
        application. It does not resynchronise VoiceCode with external
        application.

        This should NOT bind the *AppState* to the new buffer. This
        should be done only by [change_buffer].

        See [curr_buffer_name] for a description of buffer binding.

        **INPUTS**
        
        STR *buff_name=None* -- Name of the buffer to switch to.
       
        **OUTPUTS**
        
        *none* --         
        
        file:///./AppState.AppState.html#curr_buffer_name"""

        debug.virtual('AppState.change_buffer_dont_bind_from_app')


    def multiple_buffers(self):
      	"""does editor support multiple open buffers?

	**INPUTS**

	*none*

	**OUTPUTS**
	
	*BOOL* -- true if editor supports having multiple buffers open 
	at the same time"""
        
	debug.virtual('AppState.multiple_buffers')

    def bidirectional_selection(self):
      	"""does editor support selections with cursor at left?

	**INPUTS**

	*none*

	**OUTPUTS**
	
	*BOOL* -- true if editor allows setting the selection at the
	left end of the selection"""
        
	debug.virtual('AppState.bidirectional_selection')

    def active_field(self):
	"""indicates what part of the editor has the focus.

	**INPUTS**

	*none*

	**OUTPUTS**

	*(STR)* -- Name of the active Field. Elements of
	the array refer to a sequence of objects in the user interface
	that lead to the active field.

	If *None*, then the buffer [self.curr_buffer()] has the focus. 

	Example: in VisualBasic, it might be: *('menu bar', 'File', 'Save
	as', 'file name')*.

	Example: in Emacs, it might be *('find-buffer', 'buffer-name')*
	where find-buffer is the name of the command that was invoked and
	buffer-name refers to the argument that is being asked for.
	"""

        #
        # For now, we don't support voice enabling fields of the external
        # editor. We just focus on code dictation and navigation in the
        # source buffers.
        #
	return None


    def focus_is_source(self, lang_name):
        """Check if prog. env. focus is a source buffer

        Returns *true* if and only if focus of programming environment
        is a source buffer written in language *STR lang_name*.
        """

        if (self.active_field() != None):
            answer = (lang_name == None) or (self.curr_buffer().is_language(lang_name))
            
        return answer

    def find_buff(self, buff_name=None):
        """Returns the open buffer with name *STR buff_name*.
        
        If no such buffer, returns *None*.
        
        If *buff_name* is *None*, return [self.curr_buffer].

        .. [self.curr_buffer] file:///AppState.AppState.html
        """

        if (buff_name == None):
            buff_name = self.curr_buffer_name()
            
        if buff_name != None:
            if self.open_buffers.has_key(buff_name):
                return self.open_buffers[buff_name]
            else:
                new_buff = self.new_source_buffer(buff_name)
                return new_buff
        else:
            return None


    def drop_breadcrumb(self, buffname=None, pos=None):

        """Drops a breadcrumb

        *INT pos* is the position where to drop the crumb. *STR
         buffname* is the name of the source buffer.
        
        If *pos* not specified, drop breadcrumb at cursor position.

        If *buff* not specified either, drop breadcrumb in current buffer
	"""
        debug.virtual('AppState.drop_breadcrumb')

    def pop_breadcrumbs(self, num=1, gothere=1):
        """Pops breadcrumbs from the breadcrumbs stack

        *INT num* is the number of crumbs to pop. If None, then pop 1 crumb.

        if *BOOL gothere* is true, then move cursor to the last popped
        breadcrumb.
        """
        debug.virtual('AppState.pop_breadcrumbs')        




    def open_file_cbk(self, name):
        """Editor invokes this method to notify VoiceCode that it opened a new source file.
        
        **INPUTS**
        
        STR *name* -- Name of the buffer         

        **OUTPUTS**
        
        [SourceBuff] *new_buff* -- The [SourceBuff] instance created
        to represent this new file.
        
        ..[SourceBuff] file:///./SourceBuff.SourceBuff.html"""
        
        #
        # First make sure we don't already have a buffer by that name
        #
        if not self.find_buff(buff_name=name):
            new_buff = self.new_source_buffer(name)
        return new_buff
            


    def new_compatible_sb(self, fname):
        """Creates a new instance of [SourceBuff].

        Note: The class used to instantiate the [SourceBuff] needs to
        be compatible with the class of *self*. With a few exceptions
        (if any), each subclass of *AppState* will have to redefine
        *new_compatible_sb* in order to generate a [SourceBuff] of the
        appropriate class.
        
        **INPUTS**
                
        STR *fname* -- Name of the source buffer.
        
        **OUTPUTS**
        
        *none* -- 

        ..[SourceBuff] file:///./SourceBuff.SourceBuff.html"""
        
        return SourceBuff.SourceBuff(self, fname=fname)


    def new_source_buffer(self, fname):
        
        """Creates a new [SourceBuff] instances and adds it to the
        list of open buffers.
        
        **INPUTS**
        
        STR *fname* -- Name of the new buffer
        

        **OUTPUTS**
        
        """

        new_buff = self.new_compatible_sb(fname=fname)
        self.open_buffers[fname] = new_buff

    def open_file(self, name, lang = None):
        """Tell the external editor to open a file.

        Open file with name *STR name* and written in language *STR lang*. 
        """
        debug.virtual('AppState.open_file')

    def save_file(self, full_path = None, no_prompt = 0):
        """Tell the external editor to save the current buffer.

        **INPUTS**
	
	*STR full_path* -- full path under which to save the file, or
	None to use the buffer name

	*BOOL no_prompt* -- overwrite any existing file without
	prompting.  No_prompt should only be set to true if the caller
	has already prompted the user.

	**OUTPUTS**

	*BOOL* -- true if the file was successfully saved
        """
	debug.virtual('AppState.save_file')

    def active_language(self):
        """Returns name of active programming language.

        If no active programming language, then returns *None*.
        
        **INPUTS**
        
        *none* -- 
        
        **OUTPUTS**
        
        *STR* language -- Name of active programming language (*None*
        if no programming language is active).
        """

        buff = self.curr_buffer()
        language = buff.language_name()
        return self.curr_buffer().language_name()



    def log_cmd(self, cont, action):
        """Logs a command in the application's history
        
        **INPUTS**
        
        [Context] cont -- Context in which the command was invoked.
        
        [Action] action -- Action that was executed in response to the command

        **OUTPUTS**
        
        *none* -- 
        """
        
        if len(self.history) > self.max_history:
#            self.history = self.history[:len(self.history)-1]
# should drop oldest command, right?
            self.history = self.history[1:]
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

#        print '-- AppState.get_history: nth=%s' % nth
        hist_entry = None
        if nth <= len(self.history):
            entry_pos = len(self.history) - nth
            hist_entry = self.history[entry_pos]
        return hist_entry
