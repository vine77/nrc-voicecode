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

"""abstract class defining interface for an object managing buffer-specific 
grammars (dictation and selection grammars)
"""

import debug
import string
from Object import Object

class GramMgr(Object):
    """abstract class defining basic grammar management interface.

    **INSTANCE ATTRIBUTES**

    *AppState* app -- the application to which the buffers belong
    
    **CLASS ATTRIBUTES**
    
    *none*
    """

    def __init__(self, app, **args):
	"""
	
	**INPUTS**
	
	*AppState* app -- the application to which the buffers belong
	"""
        self.deep_construct(GramMgr,
                            {'app': app},
                            args)

    def __del__(self):
	"""destructor: any subclass must call this destructor explicitly
	before returning

	**INPUTS**
	
	*none*

	**OUTPUTS**

	*none*
	"""
	self.deactivate_all()
	Object.__del__(self)

    def activate(self, buffer, window):
	"""activate grammars for a buffer displayed in a particular
	window, and deactivate all other buffer/window-specific grammars

	**INPUTS**

	*STR* buffer -- name of buffer

	*INT* window -- 
	number identifying the current window  displaying
	the buffer.  In Microsoft Windows, this will be the window
	handle

	**OUTPUTS**

	*none*
	"""
	debug.virtual('GramMgr.activate')
    
    def deactivate_all(self, window = None):
	"""de-activate all buffer-specific grammars which would be
	active in window, or all grammars if window is omitted.

	**INPUTS**

	*INT* window --
	identifier of current window.  If grammars are window-specific,
	then only grammars associated with that window need be
	explicitly de-activated.  If window is omitted, de-activate all
	grammars.
	
	**OUTPUTS**

	*none*
	"""
	debug.virtual('GramMgr.deactivate_all')

    def new_buffer(self, buffer, window = None):
	"""add grammars for new buffer/window

	**INPUTS**

	*STR* buffer -- name of buffer

	*INT* window -- 
	number identifying the current window  displaying
	the buffer.  In Microsoft Windows, this will be the window
	handle.

	Note: if grammars are window-specific, and window is omitted, 
	then new_buffer may not be created until activate is called.

	**OUTPUTS**

	*none*
	"""
	debug.virtual('GramMgr.new_buffer')

    def new_window(self, window):
	"""add a new window

	**INPUTS**

	*INT* window -- 
	number identifying the current window  displaying
	the buffer.  In Microsoft Windows, this will be the window
	handle.

	**OUTPUTS**

	*none*
	"""
	debug.virtual('GramMgr.new_window')


    def delete_window(self, window):
	"""clean up and destroy all grammars for a window which 
	has been deleted.

	**INPUTS**

	*INT* window -- 
	number identifying the current window  displaying
	the buffer.  In Microsoft Windows, this will be the window
	handle

	**OUTPUTS**

	*none*
	"""

	debug.virtual('GramMgr.delete_window')

    def buffer_closed(self, buffer):
	"""clean up and destroy all grammars for a buffer which 
	has been closed.

	**INPUTS**

	*STR* buffer -- name of buffer

	**OUTPUTS**

	*none*
	"""
	debug.virtual('GramMgr.buffer_closed')
    

class WinGramMgr(Object):
    """implementation of GramMgr using window-specific grammars from
    a WinGramFactory.

    **INSTANCE ATTRIBUTES**

    *{INT : {STR : WinDictGram}}* dict_grammars -- map from window handles to
    map from buffer names to dictation grammars

    *WinGramFactory* factory -- factory which supplies WinGramMgr
    with new window-specific dictation and selection grammars.

    **CLASS ATTRIBUTES**
    
    *none*
    """

    def __init__(self, factory, **args):
	"""
	
	**INPUTS**
	
	*WinGramFactory* factory -- factory which will supply WinGramMgr
	with new window-specific dictation and selection grammars.
	"""
        self.deep_construct(WinGramMgr,
                            {'factory': factory, 'dict_grammars' : {}},
                            args)

    def __del__(self):
	"""destructor: any subclass must call this destructor explicitly
	before returning

	**INPUTS**
	
	*none*

	**OUTPUTS**

	*none*
	"""
	GramMgr.__del__(self)

    def activate(self, buffer, window):
	"""activate grammars for a buffer displayed in a particular
	window, and deactivate all other buffer/window-specific grammars

	**INPUTS**

	*STR* buffer -- name of buffer

	*INT* window -- 
	number identifying the current window  displaying
	the buffer.  In Microsoft Windows, this will be the window
	handle

	**OUTPUTS**

	*none*
	"""
	debug.virtual('GramMgr.activate')
	if not self.dict_grammars.has_key(window):
	    self.new_window(window)
	if not self.dict_grammars[window].has_key(buffer):
	    self.new_buffer(buffer, window)
	for buff_name in self.dict_grammars[window].keys():
	    if buff_name != buffer: 
	        self.dict_grammars[window][buff_name].deactivate()
	self.dict_grammars[window][buffer].activate(window)
    
    def deactivate_all(self, window = None):
	"""de-activate all buffer-specific grammars which would be
	active in window, or all grammars if window is omitted.

	**INPUTS**

	*INT* window --
	identifier of current window.  If grammars are window-specific,
	then only grammars associated with that window need be
	explicitly de-activated.  If window is omitted, de-activate all
	grammars.
	
	**OUTPUTS**

	*none*
	"""
	if window == None:
	    for a_window in self.dict_grammars.keys():
		self.deactivate_all(a_window)
	elif self.dict_grammars.has_key(window):
	    for a_buffer in self.dict_grammars[window].values():
		a_buffer.deactivate()

    def new_buffer(self, buffer, window = None):
	"""add grammars for new buffer/window

	**INPUTS**

	*STR* buffer -- name of buffer

	*INT* window -- 
	number identifying the current window  displaying
	the buffer.  In Microsoft Windows, this will be the window
	handle.

	Note: if window is omitted, 
	then new_buffer may not be created until activate is called.

	**OUTPUTS**

	*none*
	"""
	if window != None:
	    if not self.dict_grammars.has_key(window):
		self.new_window(window)
	    if not self.dict_grammars[window].has_key(buffer):
		self.dict_grammars[window][buffer] = \
		    self.factory.make_dictation(self.app, buffer, window)

    def new_window(self, window):
	"""add a new window

	**INPUTS**

	*INT* window -- 
	number identifying the current window  displaying
	the buffer.  In Microsoft Windows, this will be the window
	handle.

	**OUTPUTS**

	*none*
	"""
	if not self.dict_grammars.has_key(window):
	    self.dict_grammars[window] = {}

    def delete_window(self, window):
	"""clean up and destroy all grammars for a window which 
	has been deleted.

	**INPUTS**

	*INT* window -- 
	number identifying the current window  displaying
	the buffer.  In Microsoft Windows, this will be the window
	handle

	**OUTPUTS**

	*none*
	"""
	if self.dict_grammars.has_key(window):
	    del self.dict_grammars[window]

    def buffer_closed(self, buffer):
	"""clean up and destroy all grammars for a buffer which 
	has been closed.

	**INPUTS**

	*STR* buffer -- name of buffer

	**OUTPUTS**

	*none*
	"""
	for a_window, buffers in self.dict_grammars:
	    if buffers.has_key(buffer):
		del buffers[buffer]
