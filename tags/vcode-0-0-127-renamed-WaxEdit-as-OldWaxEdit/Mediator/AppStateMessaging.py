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

"""Application state for an external editor communicating through a messaging protocol."""


import debug, sys
from Object import Object

import AppState, AppStateCached, messaging, SourceBuffMessaging


	
class AppStateMessaging(AppStateCached.AppStateCached):
    
    """Application state for an external editor communicating through
    a messaging protocol.

    **INSTANCE ATTRIBUTES**
    
    STR *id* -- Unique identifier for the external application instance.

    [Messenger] *listen_msgr* -- Messenger used to listen for commands
    from external application.

    [Messenger] *talk_msgr* -- Messenger used to send commands
    to external application. 

    **CLASS ATTRIBUTES**
    

    .. [Messenger] file:///messaging.Messenger.html"""

    
    def __init__(self, listen_msgr=None, talk_msgr=None, id=None, **attrs):
        self.init_attrs({'multiple_buffer_support' : 0,
	    'bidirectional_selection_support' : 0})        
        self.deep_construct(AppStateMessaging, 
                            {'id': id,
                             'listen_msgr': listen_msgr,
                             'talk_msgr': talk_msgr
			    },
                            attrs)
	self.multiple_buffer_support =  self._multiple_buffers_from_app()
	self.bidirectional_selection_support = \
	    self._bidirectional_selection_from_app()
        self.init_cache()


    def new_compatible_sb(self, buff_name):
        """Creates a new instance of [SourceBuff].

        Note: The class used to instantiate the [SourceBuff] needs to
        be compatible with the class of *self*. With a few exceptions
        (if any), each subclass of *AppState* will have to redefine
        *new_compatible_sb* in order to generate a [SourceBuff] of the
        appropriate class.
        
        **INPUTS**
                
        STR *buff_name* -- unique name of the source buffer.
        
        **OUTPUTS**
        
        *none* -- 

        ..[SourceBuff] file:///./SourceBuff.SourceBuff.html"""
        
        return SourceBuffMessaging.SourceBuffMessaging(app=self, buff_name=buff_name)


    def config_from_external(self):
        
        """Lets the external editor configure the *AppStateMessaging*.

        Configuration is done through messages on the connection. The
        messages may vary from editor to editor.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        debug.virtual('AppStateMessaging.config_from_external')

    def recog_begin(self, window_id, block = 0):
        """Invoked at the beginning of a recognition event.

        The editor then returns telling VoiceCode whether or not the user
        is allowed to speak into window *window_id*.

        **INPUTS**
        
        STR *window_id* -- The ID of the window that was active when
        the recognition began.                

	*BOOL block* -- true if the speech engine can detect recog_end
	events reliably.  If so, and if the editor is capable of doing so, 
        the editor may (at its discretion) also stop responding to user
        input until method [recog_end()] is invoked.  This is to
        prevent a bunch of problems that can arise if the user types
        while VoiceCode is still processing an utterance. In such
        cases, the results of the utterance interpretation can be
        unpredictable, especially when it comes to correction.

	**NOTE:** However, if block is false, the editor **MUST NOT**
	stop responding, because the mediator will not be able to use
	recog_end to tell it to resume responding to user input.  

	Also, the editor must provide a way for the user to re-enable
	input manually, in case the mediator crashes.  If it cannot do
	so, it should not stop responding, regardless of the value of
	block.

        **OUTPUTS**
        
        BOOL *can_talk* -- *true* iif editor allows user to speak into window
        with ID *window_id*
        
        .. [recog_end()] file:///./AppState.AppState.html#recog_end"""

        self.talk_msgr.send_mess('recog_begin', {'window_id': window_id, 
	    'block': block})
        response = self.talk_msgr.get_mess(expect=['recog_begin_resp'])
        return messaging.messarg2int(response[1]['value'])

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

        NOTE: This method may be never be invoked

        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 

        ..[recog_begin()] file:///./AppState.AppState.html#recog_begin"""
        
        self.talk_msgr.send_mess('recog_end')
        response = self.talk_msgr.get_mess(expect=['recog_end_resp'])

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
        self.talk_msgr.send_mess('mediator_closing')
# this message has no response, otherwise we might block waiting for it
# if the external editor had hung, crashed, or been disconnected

    def listen_one_transaction(self):
        """Completes a single editor-initiated transaction
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        print '-- AppStateMessaging.listen_one_transation: called'
        mess = self.listen_msgr.get_mess(expect=['update',
	    'editor_disconnecting'])
        mess_name = mess[0]
        if mess_name == 'update':
	    mess_cont = mess[1]
            upd_list = mess_cont['value']
            self.apply_updates(upd_list)
	elif mess_name == 'editor_disconnecting':
	    self.close_app_cbk()
	elif mess_name == 'broken_connection':
	    self.close_app_cbk(unexpected = 1)


    def updates_from_app(self, what = None, exclude=1):
        """Gets a list of updates from the external app.

        Does this through a messaging protocol.
        
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

	if what == None:
	    what = []
	self.talk_msgr.send_mess('updates')
        response = self.talk_msgr.get_mess(expect=['updates'])

        #
        # Parse response as a list of udate messages
        #
        return response[1]['value']

    def apply_upd_descr(self, upd_descr_list):
        
        """Applies a updates provided by a list of update descriptions.
        
        **INPUTS**
        
        [{STR: ANY}] *upd_descr_list* -- List of update descriptions
        

        **OUTPUTS**
        
        [ [AS_Update]  ] *none* -- 

        ..[AS_Update] file:///./AppState.AS_Update.html"""

        for a_descr in upd_descr_list:
            the_update = AppState.create_update(a_descr)
            the_update.apply(self)


    def app_active_buffer_name(self):
        
	"""Reads the file name of the active buffer, directly from the
	external application.

	**OUTPUTS**

	*STR* -- file name of app's active buffer"""

	self.talk_msgr.send_mess('active_buffer_name')
        response = self.talk_msgr.get_mess(expect=['active_buffer_name_resp'])
        return response[1]['value']                


    def multiple_buffers(self):
      	"""does editor support multiple open buffers?

	**INPUTS**

	*none*

	**OUTPUTS**
	
	*BOOL* -- true if editor supports having multiple buffers open 
	at the same time"""

	return self.multiple_buffer_support
        
    def _multiple_buffers_from_app(self):
      	"""does editor support multiple open buffers?

        Retrieve this information directly from the external editor.

	**INPUTS**

	*none*

	**OUTPUTS**
	
	*BOOL* -- true if editor supports having multiple buffers open 
	at the same time"""

	self.talk_msgr.send_mess('multiple_buffers')
        response = self.talk_msgr.get_mess(expect=['multiple_buffers_resp'])
        return response[1]['value']                
        
    def bidirectional_selection(self):
      	"""does editor support selections with cursor at left?

        Get this value directly from the external editor

	**INPUTS**

	*none*

	**OUTPUTS**
	
	*BOOL* -- true if editor allows setting the selection at the
	left end of the selection"""

	return self.bidirectional_selection_support

    def _bidirectional_selection_from_app(self):
      	"""does editor support selections with cursor at left?

        Get this value directly from the external editor

	**INPUTS**

	*none*

	**OUTPUTS**
	
	*BOOL* -- true if editor allows setting the selection at the
	left end of the selection"""

	self.talk_msgr.send_mess('bidirectional_selection')
        response = self.talk_msgr.get_mess(expect=['bidirectional_selection_resp'])
        return response[1]['value']                


    def tell_editor_to_open_file(self, file_name):
        """Tell the external editor to open a file.

        STR *file_name* -- The full path of the file to be opened.
        
        **OUTPUTS**
        
        STR *buff_name* -- Unique name of the buffer in which the file
        was opened.

        """

#        print '-- AppStateMessaging.tell_editor_to_open_file: name=%s' % name
        
        #
        # Tell external editor to open the file
        #
        self.talk_msgr.send_mess('open_file', {'file_name': file_name})
        response = self.talk_msgr.get_mess(expect=['open_file_resp'])
	buff_name = response[1]['buff_name']

	return buff_name

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
        #
        # Tell external editor to save the file
        #
        self.talk_msgr.send_mess('save_file', 
	    {'full_path': full_path,
	     'no_prompt': no_prompt
	    })
        response = self.talk_msgr.get_mess(expect=['save_file_resp'])
	buff_name = response[1]['buff_name']

	return buff_name
        
        
    def query_buffer_from_app(self, buff_name):
	"""query the application to see if a buffer by the name of buff_name 
	exists.

        **INPUTS**

	*STR* buff_name -- name of the buffer to check

        **OUTPUTS**

	*BOOL* -- does the buffer exist?
	"""
        self.talk_msgr.send_mess('confirm_buffer_exists', {'buff_name': buff_name})
        response = \
	    self.talk_msgr.get_mess(expect=['confirm_buffer_exists_resp'])
	buffer_exists = response[1]['value']
	return buffer_exists

    def open_buffers_from_app(self):
	"""retrieve a list of the names of open buffers from the
	application.

        **INPUTS**

	*none*

        **OUTPUTS**

	*[STR]* -- list of the names of open buffers
	"""
        self.talk_msgr.send_mess('list_open_buffers')
        response = \
	    self.talk_msgr.get_mess(expect=['list_open_buffers_resp'])
	open_buffers = response[1]['value']
	return open_buffers

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

        self.talk_msgr.send_mess('close_buffer', {'buff_name': buff_name, 'save': save})
        response = self.talk_msgr.get_mess(expect=['close_buffer_resp'])
	success = response[1]['value']
	return success



class AppStateInsertIndentMess(AppStateMessaging):
    
    """subclass of AppStateMessaging which uses
    SourceBuffInsertIndentMess in place of SourceBuffMessaging

    **NOTE:** This class is used only for test editors.  Real editors 
    supporting client-side indentation should use SourceBuffMessaging.  
    Real editors not supporting client-side indentation should use 
    server-side indentation (see SB_MessExtEdSim in tcp_server.py 
    for an example).

    Its purpose is to work with clients with an incomplete implementation 
    of client-side indentation which won't work with the generic 
    AppState.insert_indent, because indent is implemented as a no-op.
    

    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**
    
    *none*
    """

    
    def __init__(self, **attrs):
        self.deep_construct(AppStateInsertIndentMess, 
                            {},
                            attrs)

    def new_compatible_sb(self, buff_name):
        """Creates a new instance of [SourceBuff].

        Note: The class used to instantiate the [SourceBuff] needs to
        be compatible with the class of *self*. With a few exceptions
        (if any), each subclass of *AppState* will have to redefine
        *new_compatible_sb* in order to generate a [SourceBuff] of the
        appropriate class.
        
        **INPUTS**
                
        STR *buff_name* -- unique name of the source buffer.
        
        **OUTPUTS**
        
        *none* -- 

        ..[SourceBuff] file:///./SourceBuff.SourceBuff.html"""
        
        return SourceBuffMessaging.SourceBuffInsertIndentMess(app=self, 
	    buff_name=buff_name)
