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

import AppState, AppStateCached, SourceBuffMessaging


	
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
        self.init_attrs({})        
        self.deep_construct(AppStateMessaging, 
                            {'id': id,
                             'listen_msgr': listen_msgr,
                             'talk_msgr': talk_msgr},
                            attrs)
        self.init_cache()


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
        
        return SourceBuffMessaging.SourceBuffMessaging(app=self, fname=fname)


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
        
        self.talk_msgr.send_mess('stop_responding')
        response = self.talk_msgr.get_mess(expect=['stop_responding_resp'])


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

        self.talk_msgr.send_mess('start_responding')
        response = self.talk_msgr.get_mess(expect=['start_responding_resp'])


    def listen_one_transaction(self):
        """Completes a single editor-initiated transaction
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        print '-- AppStateMessaging.listen_one_transation: called'
        mess = self.listen_msgr.get_mess(expect=['update'])
        mess_name = mess[0]
        mess_cont = mess[1]
        if mess_name == 'update':
            upd_list = mess_cont['value']
            self.apply_updates(upd_list)


    def updates_from_app(self, what=[], exclude=1):
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
            the_update = AppState.updates_factory(a_descr)
            the_update.apply(self)


    def _app_active_buffer_name_from_app(self):
        
	"""Reads the file name of the active buffer, directly from the
	external application.

	**OUTPUTS**

	*STR* -- file name of app's active buffer"""

	self.talk_msgr.send_mess('active_buffer_name')
        response = self.talk_msgr.get_mess(expect=['active_buffer_name_resp'])
        return response[1]['value']                


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
