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

import Object
import debug

class InterThreadEvent(Object.Object):
    """abstract interface for sending a dataless message between threads.
    Particular implementations may use win32 events or wxPython custom
    events.

    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, **args):
        """abstract base class so no arguments
	"""
        self.deep_construct(InterThreadEvent,
                            {},
                            args)
    def notify(self):
        """send the message, and return asynchronously

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
        debug.virtual('InterThreadEvent.notify')

class SocketHasDataEvent(Object.Object):
    """abstract interface for sending a message from to the main thread 
    indicating that a particular socket has data waiting to be read.

    The concrete subclass will have a reference to the particular
    socket.
    
    Particular implementations may use win32 events or wxPython custom
    events.

    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, **args):
        """abstract base class so no arguments
	"""
        self.deep_construct(SocketHasDataEvent,
                            {},
                            args)
    def notify(self):
        """send the message, and return asynchronously

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
        debug.virtual('SocketHasDataEvent.notify')

