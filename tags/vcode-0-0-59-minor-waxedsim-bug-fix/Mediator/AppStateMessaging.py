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

import AppStateCached


	
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

    
    def __init__(self, id, listen_msgr, talk_msgr, **attrs):
        self.init_attrs({})
        self.deep_construct(AppState, 
                            {'id': id,
                            'listen_msgr': listen_msgr,
                             'talk_msgr': talk_msgr},
                            attrs)

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
        return response[1]['returns']


    def curr_buffer_name_from_app(self):
	"""queries the application for the file name of the current buffer

	**OUTPUTS**

	*STR* -- file name of current buffer"""

	self.talk_msgr.send_mess('curr_buffer_name_from_app')
        response = self.talk_msgr.get_mess(expect=['curr_buffer_name_from_app_resp'])
        return response[1]['returns']        


    def apply_upd_descr(self, upd_descr_list):
        
        """Applies a updates provided by a list of update descriptions.
        
        **INPUTS**
        
        [{STR: ANY}] *upd_descr_list* -- List of update descriptions
        

        **OUTPUTS**
        
        [ [AS_Update]  ] *none* -- 

        ..[AS_Update] file:///./AppState.AS_Update.html"""
        
        for a_descr in upd_descr_list:
            the_update = AppState.updates_factory(a_descr))
            the_update.apply(self)
