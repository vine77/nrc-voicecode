
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
# (C)2002, National Research Council of Canada
#
##############################################################################

"""classes supporting inter-thread communication
"""

from thread_communication import *
from wxPython.wx import *

class GenericEventWX(wxPyEvent):
    def __init__(self, evt_type):
        wxPyEvent.__init__(self)
        self.SetEventType(evt_type)

class SocketDataEventWX(GenericEventWX):
    def __init__(self, evt_type, socket_ID):
        GenericEventWX.__init__(self, evt_type)
        self.socket_ID = socket_ID

class InterThreadEventWX(InterThreadEvent):
    """implementation of InterThreadEvent using the wxPython custom
    events module.

    **INSTANCE ATTRIBUTES**

    *wxEvtHandler evt_handler* -- wxWindow or wxEvtHandler to which to
    post the event.

    *WXTYPE evt_type* -- type/ID of the wxWindow event

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, evt_handler, evt_type, **args):
        """
	**INPUTS**

	*wxEvtHandler evt_handler* -- wxWindow or wxEvtHandler to which to
	post the event.
	"""
        self.deep_construct(InterThreadEventWX,
                            {'evt_handler': evt_handler,
                             'evt_type': evt_type},
                            args)
    def notify(self):
        """send the message, and return asynchronously

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
        event = GenericEventWX(self.evt_type)
        wxPostEvent(self.evt_handler, event)

class SocketHasDataWX(SocketHasDataEvent):
    """implementation of SocketHasDataEvent using wxPython events.
    
    **INSTANCE ATTRIBUTES**

    *wxEvtHandler evt_handler* -- wxWindow or wxEvtHandler to which to
    post the event.

    *WXTYPE evt_type* -- type/ID of the wxWindow event

    *STR socket_ID* -- the unique ID of the socket

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, evt_handler, evt_type, socket_ID, **args):
        """
	**INPUTS**

	*wxEvtHandler evt_handler* -- wxWindow or wxEvtHandler to which to
	post the event.

	*WXTYPE evt_type* -- type/ID of the wxWindow event

	*STR socket_ID* -- the unique ID of the socket
	"""
        self.deep_construct(SocketHasDataWX,
                            {'evt_handler': evt_handler,
                             'evt_type': evt_type,
                             'socket_ID': socket_ID},
                            args)
    def notify(self):
        """send the message, and return asynchronously

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
        event = SocketDataEvent(self.evt_type, self.socket_ID)
        wxPostEvent(self.evt_handler, event)


