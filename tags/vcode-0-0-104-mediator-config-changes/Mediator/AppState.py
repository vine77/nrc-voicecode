#############################################################################
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
from Object import Object, ChildObject, OwnerObject


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
	buff_name = None
	if keys.has_key("buff_name"):
	    buff_name = keys["buff_name"]
	    del keys["buff_name"]
	buffer = self.application.find_buff(buff_name)
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
                 'select': SB_UpdSetSelection, 'goto': SB_UpdGoto,
                 'close_buff': AS_UpdCloseBuffer,
                 'open_buff': AS_UpdOpenBuffer}

    
    return use_class[action]


def create_update(upd_descr):
        
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


    def apply(self, on_app):

        """Carry out the update.

        **INPUTS**
        
        [AppState] *on_app* --
    
        **OUTPUTS**
        
        *none* --

        ..[AppState] file:///./AppState.AppState.html"""
        debug.virtual('AS_Update.apply')        


class AS_UpdOpenBuffer(AS_Update):
            
    """Update class for opening a buffer.
    
    **INSTANCE ATTRIBUTES**

    {STR: ENCODABLE} *descr* -- A description of the parameters of the update.
    
    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, descr, **args_super):
        self.deep_construct(AS_UpdOpenBuffer, 
                            {'descr': descr}, 
                            args_super, 
                            {})
        
    def apply(self, on_app):
        on_app.open_buffer_cbk(self.descr['buff_name'])

        
class AS_UpdCloseBuffer(AS_Update):
            
    """Update class for closing a buffer.
    
    **INSTANCE ATTRIBUTES**

    {STR: ENCODABLE} *descr* -- A description of the parameters of the update.
    
    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, descr, **args_super):
        self.deep_construct(AS_UpdCloseBuffer, 
                            {'descr': descr}, 
                            args_super, 
                            {})
        
    def apply(self, on_app):
        on_app.close_buffer_cbk(self.descr['buff_name'])

        
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
        range = on_buff.make_valid_range(range)
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

	
class AppState(OwnerObject):
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
    
    *{STR: * [SourceBuff] *} open_buffers={}* -- List of source
     buffers that are currently open in the programming
     environment. The key is the buffer name (not necessarily 
     the file name!) and the value is the [SourceBuff] object.
    
    *INT* max_history=100 --  Maximum length of the command history.

    *BOOL* translation_is_off -- If true, then translation of CSCs and
     LSAs isturned off for that applications. Everything should be
     typed as dictated text, except for commands that turn the
     translation back on (NOT IMPLEMENTED FOR NOW).

    *BOOL* print_buff_when_changed=0 -- If true, then print the content
    of the current buffer whenever it changes (used mostly for regression
    testing external editor).

    *AppMgr* manager -- the AppMgr object which owns this AppState.
    Certain callback methods (close_app_cbk, new_buffer_cbk) will notify 
    the manager.  If we are using the old mediator infrastructure, manager 
    may be None.  Therefore, AppState must check whether manager == None
    before sending such notifications.

    *STR* instance_name -- the name of this editor instance, assigned by
    AppMgr, and used to identify the editor in callbacks to the manager.

    *STR* bound_buffer_name=None -- Name of the buffer that VoiceCode
    is currently bound to operate on. If *None*, use editor's active
    buffer. See [curr_buffer_name] method for a description of buffer
    binding.
     
    **CLASS ATTRIBUTES**
    
    *(STR)* buffer_methods -- list of names of buffer methods which
    AppState should forward to SourceBuff.  Subclasses of AppState
    should include those from AppState and add their own 

    .. [Action] file:///./actions_gen.Action.html
    .. [Context] file:///./Context.Context.html
    .. [SourceBuff] file:///./SourceBuff.SourceBuff.html
    .. [curr_buffer_name] file:///./AppState.AppState.html#curr_buffer_name"""

    buffer_methods = ['is_language', 'region_distance', 'cur_pos',
    'get_selection', 'goto_end_of_selection', 'set_selection', 
    'contents', 'get_text', 'distance_to_selection', 'get_visible',
    'make_position_visible', 'line_num_of', 'len', 'make_within_range', 
    'move_relative', 'insert', 'indent', 'insert_indent', 
    'delete', 'goto', 'goto_line', 'move_relative_line',
    'move_relative_page', 'search_for', 'log_search',
    'print_buff_if_necessary', 'refresh', 'incr_indent_level',
    'decr_indent_level', 'print_buff', 'closest_occurence_to_cursor']

    def __getattr__( self, name):
	if name in self.buffer_methods:
	    return ForwardToBuffer(self, name)
	raise AttributeError(name)
    
    def __init__(self, app_name=None, translation_is_off=0,
                 max_history=100, print_buff_when_changed=0, 
		 instance_name = None, manager = None, **attrs):
        
        self.init_attrs({'breadcrumbs': [], 'history': []})
        self.deep_construct(AppState, 
                            {'app_name': app_name,
			     'manager': manager,
			     'instance_name': instance_name,
                             'rec_utterances': [], 
                             'open_buffers': {},
			     'bound_buffer_name': None,
                             'max_history': max_history, 
                             'translation_is_off': translation_is_off,
                             'print_buff_when_changed': print_buff_when_changed},
                            attrs)
	self.add_owned('open_buffers')
	self.name_parent('manager')
      
    def name(self):
	"""the unique name (assigned by the AppMgr) to this editor
	instance

	**INPUTS**

	*none*

	**OUTPUTS**

	*STR* -- the name of the instance, or None if the manager has
	not given it one.
	"""
	return self.instance_name

    def set_name(self, name):
	"""assign a unique name to this editor instance.  
	**NOTE:** only AppMgr should call this method.

	**INPUTS**

	*STR* name -- the name of the instance

	**OUTPUTS**

	*none*
	"""
	self.instance_name = name

    def current_manager(self):
	"""returns a reference to the AppMgr which owns this AppState

	**INPUTS**

	*none*

	**OUTPUTS**
	
	*AppMgr* -- the AppMgr object which owns this AppState, or None
	if there is none.
	"""
	return self.manager

    def set_manager(self, manager):
	"""indicates the AppState's manager.  Normally called only by 
	the manager.  

	**INPUTS**
	
	*AppMgr* manager -- the AppMgr object which owns this AppState.

	**OUTPUTS**

	*none*
	"""
	self.manager = manager

    def recog_begin(self, window_id):
        """Invoked at the beginning of a recognition event.

        The editor then returns telling VoiceCode whether or not the user
        is allowed to speak into window *window_id*.

        If possible, the editor should also stop responding to user
        input until method [recog_end()] is invoked. This is to
        prevent a bunch of problems that can arise if the user types
        while VoiceCode is still processing an utterance. In such
        cases, the results of the utterance interpretation can be
        unpredictable, especially when it comes to correction.

        Each external editor will respond to that message as best it can.

        Ideally, the editor would:

        - Start recording user actions to a log
        - execute those actions later when [recog_end()] is invoked.

        If the editor is able to stop responding to user input, but is
        not able to record them and/or execute them later, then it
        should:

        - Stop responding to user input until [recog_end()] is
          later invoked.

        If the editor is not even able to stop responding to user
        input, then it should:

        - Do nothing
        

        NOTE: This method may be invoked more than once before
        [recog_end()] is invoked. In such cases, only the first
        call to the method should do anything.

        
        **INPUTS**
        
        STR *window_id* -- The ID of the window that was active when
        the recognition began.                

        **OUTPUTS**
        
        BOOL *can_talk* -- *true* iif editor allows user to speak into window
        with ID *window_id*
        
        .. [recog_end()] file:///./AppState.AppState.html#recog_end"""

        debug.virtual("AppState.recog_begin")


    def recog_end(self):
        """Invoked at the end of a recognition event.

        This tells the editor to start responding to user
        input again, and possibly to execute any user inputs it may
        have recorded since [recog_begin()] was invoked.
        
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
        [recog_begin()] is invoked. In such cases, only the first
        call to the method should do anything.

        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 

        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 

        ..[recog_begin()] file:///./AppState.AppState.html#recog_begin"""

        debug.virtual('AppState.recog_end')


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

    def mediator_closing(self):
	"""method called to inform AppState that the mediator is
	closing.    Internal editors should exit.  They may prompt the
	user to save modified files, but must not allow the user to
	cancel and leave the editor running.  External editors should
	disconnect but not close.  **Note:** this method should not
	block.  For external editors, that means the corresponding
	message should have a response for which to wait.  Otherwise, a
	single hung or disconnected editor hang the mediator and prevent
	it from closing or from notifying the rest of the connected
	editors that it was closing.  

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	debug.virtual('AppState.mediator_closing')
	

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

        See [curr_buffer_name] for a description of buffer binding.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 

        ..[curr_buffer_name] file:///./AppState.AppState.html#curr_buffer_name"""
        
        return self.bound_buffer_name


    def unbind_from_buffer(self):
        """unbinds the AppState from a particular buffer.

        See [curr_buffer_name] for a description of buffer binding.
        
        **INPUTS**

        *none* -- 
        
        **OUTPUTS**
        
        *none* -- 

        ..[curr_buffer_name] file:///./AppState.AppState.html#curr_buffer_name"""
        
        self.bound_buffer_name = None

    def bind_to_buffer(self, buff_name):
        """Binds the AppState to a particular buffer.

        See [curr_buffer_name] for a description of buffer binding.
        
        **INPUTS**
        
        STR *buff_name* -- Name of the buffer to bind to.
        

        **OUTPUTS**
        
        *BOOL* -- true if buffer exists and AppState can be bound to it

        ..[curr_buffer_name] file:///./AppState.AppState.html#curr_buffer_name"""
        
	buff = self.find_buff(buff_name)
	if buff == None:
	    return 0
        self.bound_buffer_name = buff_name
	if buff_name == None:
	    self.bound_buffer_name = self.curr_buffer_name()
# Here, we don't tell the application to switch to the found buffer, but
# we do when a CSC calls change_buffer while the AppState is bound.
# That way, if the user speaks, and then changes the buffer before the
# utterance has been interpreted, the result of the utterance will go
# into the buffer which was active when the user began to speak.
# However, the editor focus will remain in the new buffer (unless a CSC
# from the utterance switches the buffer -- a necessary exception,
# otherwise CSCs to switch buffers would never have a permanent
# effect).
# I'm not sure this is the best design.  We may later decide to call
# change_buffer here as well.
	return 1



    def change_buffer(self, buff_name):

	"""Changes the active buffer.

        Will also bind the AppState to that buffer if the application is
	currently bound to a buffer.
        See [curr_buffer_name] for a description of
        buffer binding.

        **INPUTS**
        
        STR *buff_name* -- Name of the buffer to switch to.

        **OUTPUTS**
        
        *BOOL* -- true if buff_name exists and the external application
	successfully switches to it
        
        file:///./AppState.AppState.html#curr_buffer_name"""

        if self.app_change_buffer(buff_name):
	    if self.is_bound_to_buffer() != None:
		self.bind_to_buffer(buff_name)
	    self.synchronize_with_app()
	    return 1
	return 0


    def app_change_buffer(self, buff_name):

	"""Changes the external application's active buffer.

        This variant only changes the buffer in the external
        application. It does not resynchronise VoiceCode with external
        application.

        This should NOT bind the *AppState* to the new buffer. This
        should be done only by [change_buffer].

        See [curr_buffer_name] for a description of buffer binding.

        **INPUTS**
        
        STR *buff_name* -- Name of the buffer to switch to.
       
        **OUTPUTS**
        
        *BOOL* -- true if buff_name exists and the external application
	successfully switches to it
        
        file:///./AppState.AppState.html#curr_buffer_name"""

        debug.virtual('AppState.app_change_buffer')

    def is_active(self):
	"""is the editor application active (not suspended)?

	Usually true, except for remote editors running in a (Unix)
	shell.  GUI editors tend to minimize instead of suspending, so
	their process should still be active.

	**INPUTS**

	*none*

	**OUTPUTS**
	
	*BOOL* -- true if editor is active (i.e. has not been suspended)
	"""
	debug.virtual('AppState.is_active')

    def is_active_is_safe(self):
	"""can is_active safely be queried, without blocking?

	For example, Emacs provides a suspend-hook and a
	suspend-resume-hook, so a properly written AppStateEmacs can
	set a flag on suspend and clear it on resume, and will therefore
	be able to respond to is_active without querying Emacs.

	Also, except for remote editors running in a (Unix)
	shell, this is usually true.  GUI editors tend to minimize 
	instead of suspending, so their process should still be active.

	**INPUTS**

	*none*

	**OUTPUTS**
	
	*BOOL* -- true if is_active can be queried without blocking,
	even if the editor has been suspended. 
	"""
	debug.virtual('AppState.is_active_is_safe')

    def shared_window(self):
        """is the editor running in a window which could be shared with
	another editor instance (because it is a shell window,
	and this instance could be suspended or closed)

	Usually false for GUI editors.

	Note: remote editors running in a remote display
	which appears as a single window to be local operating system 
	(X servers in single window mode, VNC) will also appear to be
	shared windows.  However, the mediator will perform a separate 
	check to detect this, so for remote editors which do not share windows 
	on the remote system, AppState.shared_window should report
	false.
	
	**INPUTS**

	*none*

	**OUTPUTS**
	
	*BOOL* -- true if editor is running in a potentially shared window
	"""
        
	debug.virtual('AppState.shared_window')

    def set_instance_string(self, instance_string):
        """specifies the identifier string for this editor instance.  If the 
	editor is capable of setting the window title to include this string, 
	it should (and then should return this string when the
	instance_string method is called.  

	**INPUTS**

	*STR* instance_string -- the identifying string to be included in the
	window title if possible.

	**OUTPUTS**
	
	*none*
	"""
	debug.virtual('AppState.set_instance_string')

    def instance_string(self):
        """returns the identifier string for this editor instance (which 
	should be a substring of the window title)

	Note: multiple windows of remote editors running in a remote display
	which appears as a single window to be local operating system 
	(X servers in single window mode, VNC) will not be able to set 
	the overall title.  
	However, the mediator will perform a 
	separate check to detect this, so remote editors which support
	identifying title strings should still return the appropriate
	string.

	**INPUTS**

	*none*

	**OUTPUTS**
	
	*STR* -- the identifying string, or None if the editor was not given 
	such a string or cannot set the window title.
	"""
        
	debug.virtual('AppState.instance_string')

    def title_escape_sequence(self, before = "", after = ""):
	"""gives the editor a (module-dependent) hint about the escape
	sequence which can be used to set the module's window title, if
	any.  If the editor has its own mechanism for setting the window
	title, it should simply ignore this method.  

	**INPUTS**

	*STR* before -- the escape sequence to be sent before the string
	to place in the window title, or the empty string if there is no
	escape sequence

	*STR* after -- the escape sequence which terminates the window
	title value

	**OUTPUTS**

	*none*
	"""
	debug.virtual('AppState.title_escape_sequence')

    def multiple_windows(self):
        """does editor support multiple windows per instance?

	Note: the purpose of this function is to allow the RecogStartMgr
	to determine whether a previously unknown window could belong to
	this known instance.  Therefore, Emacs running in text mode 
	should return false, even though it can have (sub-)windows in 
	a single frame.  
	
	Note: multiple windows of remote editors running in a remote display
	which appears as a single window to be local operating system 
	(X servers in single window mode, VNC) will not appear to the mediator 
	as having separate windows.  However, the mediator will perform a 
	separate check to detect this, so remote editors which support
	multiple windows should return true, regardless of the remote
	display method.

	**INPUTS**

	*none*

	**OUTPUTS**
	
	*BOOL* -- true if editor supports opening multiple editor windows.  
	"""
        
	debug.virtual('AppState.multiple_windows')

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

#        print '-- AppState.find_buff: buff_name=%s' % buff_name

        if (buff_name == None):
            buff_name = self.curr_buffer_name()
            
        if buff_name != None:
# This ends up querying the application extremely frequently, which is
# probably not necessary.  Instead, I'll assume that the synchronization
# at the start of the utterance updates the list of open buffers, and
# that methods which open or close buffers during the utterance make the
# appropriate changes as well.
#	    if not self.query_buffer_from_app(buff_name):
#		return None
            if self.open_buffers.has_key(buff_name):
                return self.open_buffers[buff_name]
            else:
# Don't create a new buffer in the application, but if the application has a
# buffer with no corresponding SourceBuff, then create a corresponding
# SourceBuff.
		if not self.query_buffer_from_app(buff_name):
		    return None
                new_buff = self._new_source_buffer(buff_name)
# This is still problematic if an existing buffer has just been renamed
# (e.g. by "Save As...").  I'm not sure of any good way to avoid this
# problem, except for the editor to notify AppState of renamings (or,
# when the save is mediator-initiated, for AppState to check after the
# save whether the buffer has been renamed).
                return new_buff
        else:
            return None

    def query_buffer_from_app(self, buff_name):
	"""query the application to see if a buffer by the name of buff_name 
	exists.

        **INPUTS**

	*STR* buff_name -- name of the buffer to check

        **OUTPUTS**

	*BOOL* -- does the buffer exist?
	"""
	debug.virtual('AppState.query_buffer_from_app')

    def open_buffers_from_app(self):
	"""retrieve a list of the names of open buffers from the
	application.

        **INPUTS**

	*none*

        **OUTPUTS**

	*[STR]* -- list of the names of open buffers
	"""
	debug.virtual('AppState.open_buffers_from_app')

    def new_window_cbk(self):
	"""editor invokes this method to notify AppState that it has
	opened a new window

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	if self.current_manager() and self.name():
	    self.current_manager().new_window(self.name())

    def close_app_cbk(self):
	"""editor invokes this method to notify AppState that it is
	about to close

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	if self.current_manager() and self.name():
	    self.current_manager().delete_instance(self.name())

    def close_buffer_cbk(self, buff_name):
	"""editor invokes this method to notify AppState that a
	buffer has been closed

	**INPUTS**

	*STR* buff_name -- the name of the buffer which has been closed

	**OUTPUTS**

	*none*
	"""
	buff = self.find_buff(buff_name)
        if buff != None:
	    self.open_buffers[buff_name].cleanup()
            del self.open_buffers[buff_name]
	if self.is_bound_to_buffer() == buff_name:
	    self.unbind_from_buffer()

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



    def tell_editor_to_open_file(self, file_name):
        """Tell the editor to open a file in a new buffer.
        
        **INPUTS**
        
        STR *file_name* -- The full path of the file to be opened.
        
        **OUTPUTS**
        
        STR *buff_name* -- Unique name of the buffer in which the file
        was opened. Returns *None* if the editor was not able to open
        the file.
        
        """
        
        debug.virtual('AppState.tell_editor_to_open_file')
        
    def rename_buffer_cbk(self, old_buff_name, new_buff_name):
        
        """Editor invokes this method to notify VoiceCode that it
        has renamed an existing text buffer.
        
        **INPUTS**

        STR *old_buff_name* -- old name of the buffer.
        STR *new_buff_name* -- new name of the buffer.
        
        **OUTPUTS**
        
        *none*
        
        ..[SourceBuff] file:///./SourceBuff.SourceBuff.html"""

        if new_buff_name != old_buff_name:
	    if not self.open_buffers.has_key(new_buff_name):
		self.open_buffers[new_buff_name] = \
		    self.open_buffers[old_buff_name]
		del self.open_buffers[old_buff_name]
	    if self.is_bound_to_buffer() == old_buff_name:
		self.bind_to_buffer(old_buff_name)
        buff = self.find_buff(new_buff_name)
	buff.rename_buffer_cbk(new_buff_name)

    def open_buffer_cbk(self, buff_name):
        
        """Editor invokes this method to notify VoiceCode that it
        opened a new text buffer.
        
        **INPUTS**

        STR *buff_name* -- unique name of the buffer.
        
        **OUTPUTS**
        
        *none*
        
        ..[SourceBuff] file:///./SourceBuff.SourceBuff.html"""

#        print '-- AppState.open_buffer_cbk: buff_name=%s' % buff_name
        
        #
        # First make sure we don't already have a buffer by that name
        #
        if not self.open_buffers.has_key(buff_name):
            self._new_source_buffer(buff_name)
            
    def new_compatible_sb(self, buff_name):
        """Creates a new instance of [SourceBuff].

        Note: The class used to instantiate the [SourceBuff] needs to
        be compatible with the class of *self*. With a few exceptions
        (if any), each subclass of *AppState* will have to redefine
        *new_compatible_sb* in order to generate a [SourceBuff] of the
        appropriate class.
        
        **INPUTS**
                
        STR *buff_name* -- unique name for the source buffer.
        
        **OUTPUTS**
        
        *SourceBuff* -- the new buffer

        ..[SourceBuff] file:///./SourceBuff.SourceBuff.html"""
        
        debug.virtual('AppState.new_compatible_sb')


    def _new_source_buffer(self, buff_name):
        
        """Creates a new [SourceBuff] instances and adds it to the
        list of open buffers.

	Note: this method should not only be called by other AppState
	methods, not from outside AppState, and only if such methods
	have already verified that self.open_buffers doesn't already
	have a key matching buff_name
        
        **INPUTS**
        
        STR *buff_name* -- unique name of the new buffer
        
        **OUTPUTS**

	*SourceBuff* -- the new buffer
        
        """

#        print '-- AppState._new_source_buffer: buff_name=%s' % buff_name
        new_buff = self.new_compatible_sb(buff_name=buff_name)
        self.open_buffers[buff_name] = new_buff
        return new_buff

    def open_file(self, file_name):
        """Tell the external editor to open a file, and create a local buffer
        for that file.

        Open file with name *STR name*.

        Right now, this is used mostly so that the regression testing
        procedure can tell the external editor to open a test
        file. But in the future, it may be used to voice-enable the
        open-file dialogue using pseudo-code dictation of file names.

        **INPUTS**

        STR *file_name* -- Full path of the file to be opened.

        """

#        print '-- AppState.open_file: file_name="%s"' % file_name
        buff_name = self.tell_editor_to_open_file(file_name)

        if buff_name:
            self.open_buffer_cbk(buff_name)

    def save_file(self, full_path = None, no_prompt = 0):
        """Tell the external editor to save the current buffer.

        **INPUTS**
	
	*STR full_path* -- full path under which to save the file, or
	None to use the buffer name

	*BOOL no_prompt* -- overwrite any existing file without
	prompting.  No_prompt should only be set to true if the caller
	has already prompted the user.

	**OUTPUTS**

	*BOOL* -- true if file was saved successfully
        """
	buff_name = self.curr_buffer_name()
        new_buff_name = self.app_save_file(full_path, no_prompt)

        if new_buff_name != None and new_buff_name != buff_name:
	    self.rename_buffer_cbk(buff_name, new_buff_name)

    def app_save_file(self, full_path = None, no_prompt = 0):
        """Tell the external editor to save the current buffer.

        **INPUTS**
	
	*STR full_path* -- full path under which to save the file, or
	None to use the buffer name

	*BOOL no_prompt* -- overwrite any existing file without
	prompting.  No_prompt should only be set to true if the caller
	has already prompted the user.

	**OUTPUTS**

	*STR* -- new buffer name if successful, or None if the save 
	failed
        """
	debug.virtual('AppState.app_save_file')

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
        
        *(* [Context], [Action] *)* hist_entry -- The context and action of the *nth* most
        recent command in the application's command history.

        .. [Context] file:///./Context.Context.html
        .. [Action] files:///./Action.Action.html"""

#        print '-- AppState.get_history: nth=%s' % nth
        hist_entry = None
        if nth <= len(self.history):
            entry_pos = len(self.history) - nth
            hist_entry = self.history[entry_pos]
        return hist_entry



    def init_for_test(self):
        
        """Reinitialise the *AppState* so that it is ready for a new
        regression test.

        When running several regression tests using the same
        *AppState* (for example, an *AppState* connected to an
        external editor), we need to reinitialise it after every test.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        #
        # Just ask the editor to close all buffers known to VoiceCode
        #
        self.close_all_buffers(-1)



    def close_all_buffers(self, save=0):
        """Tell the editor to close all buffers known to VoiceCode
        
        **INPUTS**
        
        INT *save* -- *-1* -> don't save the buffer
                            *0* -> query user if buffer needs saving
                            *1* -> save without querying user
        

        **OUTPUTS**
        
        *none* -- 
        """

#        print '-- AppState.close_all_buffers: called'
        for a_buff_name in self.open_buffers.keys():
            self.close_buffer(a_buff_name, save)

    def close_buffer(self, buff_name, save=0):
        """close a buffer
        
        **INPUTS**
        
        STR *buff_name* -- name of buffer to close

        INT *save* -- *-1* -> don't save the buffer
                            *0* -> query user if buffer needs saving
                            *1* -> save without querying user

        **OUTPUTS**
        
        *BOOL* -- true if the editor does close the buffer
        """
        if self.app_close_buffer(buff_name, save):
	    self.close_buffer_cbk(buff_name)
	    return 1
	return 0
        

    def app_close_buffer(self, buff_name, save=0):
        """Ask the editor to close a buffer.
        
        **INPUTS**
        
        STR *buff_name* -- name of buffer to close

        INT *save* -- *-1* -> don't save the buffer
                            *0* -> query user if buffer needs saving
                            *1* -> save without querying user

        **OUTPUTS**
        
        *BOOL* -- true if the editor does close the buffer
        """
        
        debug.virtual('AppState.app_close_buffer')


# defaults for vim - otherwise ignore
# vim:sw=4



