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
# (C)2000, David C. Fox
#
##############################################################################

"""abstract class defining interface for an object which receives 
recognition-starting (or onBegin/gotBegin) callbacks, figures out which
application and buffer are active, and tells the GramMgr to activate the
appropriate grammars.
"""

import debug
import RecogStartMgr
import natlink
from natlinkutils import *

class RecogStartGram(GrammarBase):
    """a dummy grammar used only to capture recognition-starting events,
    without interfering with the global setBeginCallback from
    natlinkmain which loads natlink python macros (and reloads modified
    ones)
    """

    gramSpec = """
        <start> exported = {emptyList};
    """

    def initialize(self, callback = None):
	self.callback = callback
        self.load(self.gramSpec)
#        self.activateAll()

    def gotBegin(self, module_info):
	if self.callback != None:
	    self.callback(module_info)

class RecogStartMgrNL(RecogStartMgr.RSMBasic):
    """abstract class defining interface for an object which receives 
    recognition-starting (or onBegin/gotBegin) callbacks, figures out which
    application and buffer are active, and tells the GramMgr to activate the
    appropriate grammars.

    **INSTANCE ATTRIBUTES**

    *RecogStartGram* start_gram -- dummy grammar used to capture the
    recognition-starting event without interfering with user-defined
    natlink macros

    *none*

    **CLASS ATTRIBUTES**
    
    *none*
    """

    def __init__(self, **args):
        self.deep_construct(RecogStartMgr,
                            {'start_gram': RecogStartGram(),
			    },
                            args)
	start_gram.initialize(self.starting)
	
    def remove_other_references(self):
	self.deactivate()
	self.start_gram.unload()
	del self.start_gram
	RSMBasic.cleanup(self)

    def parse_module_info(self, module_info):
	"""rearrange natlink's module_info in our format
	
	**INPUTS**

	*(STR, STR, INT)* -- the module name, window title, and window
	handle

	**OUTPUTS**

	*(INT, STR, STR)* -- the window id, title, and module name
	"""
	module_path, title, handle = module_info
	module = os.path.basename(module_path)
	module = os.path.splitext(module)[0]
	return handle, title, module

    def window_info(self):
	"""find the window id, title, and module of the current window

	**INPUTS**

	*none*

	**OUTPUTS**

	*(INT, STR, STR)* -- the window id, title, and module name
	"""
	return parse_module_info(natlink.getCurrentModule())

    def starting(self, module_info):
	self._recognition_starting(self.parse_module_info(module_info))


# defaults for vim - otherwise ignore
# vim:sw=4

