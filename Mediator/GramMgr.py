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
from Object import Object, OwnerObject

class GramMgr(OwnerObject):
    """abstract class defining basic grammar management interface.

    **INSTANCE ATTRIBUTES**

    *AppState* app -- the application to which the buffers belong
    
    *RecogStartMgr recog_mgr* -- the RecogStartMgr which owns this
    grammar manager

    **CLASS ATTRIBUTES**
    
    *none*
    """

    def __init__(self, recog_mgr, app, **args):
        """constructor
	
	**INPUTS**

	*RecogStartMgr recog_mgr* -- the RecogStartMgr which owns this
	grammar manager
	
	*AppState* app -- the application to which the buffers belong
	"""
        self.deep_construct(GramMgr,
                            {'recog_mgr': recog_mgr, 'app': app},
                            args)
        self.name_parent('recog_mgr')

    def interpreter(self):
        """return a reference to the mediator's current CmdInterp object

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
        return self.recog_mgr.interpreter()
    
    def remove_other_references(self):
        """additional cleanup to ensure that this object's references to
	its owned objects are the last remaining references

	**NOTE:** subclasses must call their parent class's 
	remove_other_references method, after performing their own duties.
	Also, a class inheriting from two OwnerObject classes MUST
	define remove_other_references and call both subclasses'
	versions

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
# subclasses must call their parent class's remove_other_references
# method, after performing their own duties
        self.deactivate_all()

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
    
    def using_global(self):
        """checks whether GramMgr creates global grammars, rather than 
	window-specific ones

	**INPUTS**

	*none*

	**OUTPUTS**

	*BOOL* -- true if the GramMgr produces global grammars
	"""
        debug.virtual('GramMgr.using_global')

    
class GramMgrFactory(Object):
    """factory which produces GramMgr objects for new application
    instances

    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, **args):
        """abstract class, no arguments
	"""
        self.deep_construct(GramMgrFactory, {}, args)

    def new_manager(self, editor, recog_mgr):
        """creates a new GramMgr

	**INPUTS**

	*AppState* editor -- AppState object for which to manage
	grammars

	*RecogStartMgr recog_mgr* -- the RecogStartMgr which owns this
	grammar manager

	**OUTPUTS**

	*none*
	"""
        debug.virtual('GramMgrFactory.new_manager')

    def new_global_manager(self, editor, recog_mgr, exclusive = 1):
        """creates a new GramMgr using global grammars (regardless of
	the value of self.global_grammars)

	**INPUTS**

	*AppState* editor -- AppState object for which to manage
	grammars

	*RecogStartMgr recog_mgr* -- the RecogStartMgr which owns this
	grammar manager

	**OUTPUTS**

	*none*
	"""
        debug.virtual('GramMgrFactory.new_global_manager')


class GramMgrDictContext(GramMgr):
    """implements finding of dictation context

    **INSTANCE ATTRIBUTES**

    *none*
    
    **CLASS ATTRIBUTES**
    
    *none*
    """
    def find_context(self, buffer):
        """Find context for dictation grammar

	**INPUTS**

	*STR buffer* -- name of the current buffer

	**OUTPUTS**

	(STR, STR) -- (two-word) context before and after the current
	selection
	"""
#  find dictation context
        current = self.app.cur_pos(buff_name = buffer)
        selection = self.app.get_selection(buff_name = buffer)
#        print current
        self.app.drop_breadcrumb(buffname = buffer)
        self.app.drop_breadcrumb(buffname = buffer)
#        self.app.search_for(r'\S+\s+\S+', direction = -1, 
#            num = 1, where = -1, buff_name = buffer, unlogged = 1)
# don't log the search -- otherwise we mess up commands to repeat
# previous user-initiated searches and punctuation navigation
        self.app.search_for(r'\s+\S', direction = -1, 
            num = 2, where = -1, buff_name = buffer, unlogged = 1)
#        self.app.search_for(r'\s+\S+', direction = -1, 
#            num = 2, where = -1, buff_name = buffer, unlogged = 1)
        start = self.app.cur_pos(buff_name = buffer)
#        print start
        before = self.app.get_text(start, current, buff_name = buffer)
#        print before
        self.app.pop_breadcrumbs()
        self.app.search_for(r'\S+\s+', direction = 1, 
            num = 2, where = 1, buff_name = buffer, unlogged = 1)
        end = self.app.cur_pos(buff_name = buffer)
#        print end
        after = self.app.get_text(current, end, buff_name = buffer)
        self.app.pop_breadcrumbs()
        self.app.set_selection(selection, buff_name = buffer)
        return before, after


class WinGramMgr(GramMgrDictContext):
    """implementation of GramMgr using window-specific grammars from
    a WinGramFactory.

    **INSTANCE ATTRIBUTES**

    *{INT : {STR : WinDictGram}}* dict_grammars -- map from window handles to
    map from buffer names to dictation grammars

    *{INT : SelectWinGram}* sel_grammars -- map from window handles to
    to selection grammars

    *WinGramFactory* factory -- factory which supplies WinGramMgr
    with new window-specific dictation and selection grammars.

    **CLASS ATTRIBUTES**
    
    *none*
    """

    def __init__(self, factory, global_grammars = 0, exclusive =
        0, **args):
        """
	
	**INPUTS**
	
	*WinGramFactory* factory -- factory which will supply WinGramMgr
	with new window-specific dictation and selection grammars.

	*BOOL* global_grammars -- use global grammars, instead of
	window-specific ones (only for testing purposes)

	*BOOL* exclusive -- use exclusive grammars which prevent 
	non-exclusive grammars from getting results (only for testing purposes)

	"""
        self.deep_construct(WinGramMgr,
                            {'factory': factory, 
                            'global_grammars': global_grammars,
                            'exclusive': exclusive,
                            'dict_grammars' : {},
                            'sel_grammars' : {}},
                            args)
        self.add_owned('dict_grammars')
        self.add_owned('sel_grammars')

    
    def remove_other_references(self):
        """additional cleanup to ensure that this object's references to
	its owned objects are the last remaining references

	**NOTE:** subclasses must call their parent class's 
	remove_other_references method, after performing their own duties.
	Also, a class inheriting from two OwnerObject classes MUST
	define remove_other_references and call both subclasses'
	versions

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
# subclasses must call their parent class's remove_other_references
# method, after performing their own duties
        self.deactivate_all()


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
        if not self.dict_grammars.has_key(window):
            self.new_window(window)
# this also creates a new dictation grammar and selection grammar
        if not self.dict_grammars[window].has_key(buffer):
            self.new_buffer(buffer, window)
        for buff_name in self.dict_grammars[window].keys():
            if buff_name != buffer:
                self.dict_grammars[window][buff_name].deactivate()
# if the dictation grammars are actually global, we need to deactivate 
# all the rest, even if they are stored under other windows in dict_grammars
        if self.global_grammars:
            for a_window in self.dict_grammars.keys():
                if a_window != window:
                    for buff_name in self.dict_grammars[a_window].keys():
                        self.dict_grammars[a_window][buff_name].deactivate()

#  set visible range and buffer for selection grammar
        self.sel_grammars[window].activate(buffer)
# if the selection grammars are actually global, we need to deactivate 
# all the rest, even if they are stored under other windows in sel_grammars
        if self.global_grammars:
            for a_window in self.sel_grammars.keys():
                if a_window != window:
                    self.sel_grammars[a_window].deactivate()

#  set dictation context
        before, after = self.find_context(buffer)
        self.dict_grammars[window][buffer].set_context(before, after)

        self.dict_grammars[window][buffer].activate()
    
    def _deactivate_all_window(self, window):
        """de-activate all buffer-specific grammars which would be
	active in window

	**INPUTS**

	*INT* window --
	identifier of current window.  Only grammars associated with 
	that window will be explicitly de-activated.  
	
	**OUTPUTS**

	*none*
	"""
        if self.dict_grammars.has_key(window):
            self.sel_grammars[window].deactivate()
            for a_buffer in self.dict_grammars[window].values():
                a_buffer.deactivate()

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
        if window == None or self.global_grammars:
            for a_window in self.dict_grammars.keys():
                self._deactivate_all_window(a_window)
        else:
            self._deactivate_all_window(window)

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
                self.new_window(window, buffer)
            if not self.dict_grammars[window].has_key(buffer):
                a_window = window
                if self.global_grammars:
                    a_window = None
                debug.trace('WinGramMgr.new_buffer', 
                    'window, a_window: %s, %s' % (str(window), str(a_window)))
                self.dict_grammars[window][buffer] = \
                    self.factory.make_dictation(self, self.app, 
                    buffer, window = a_window, 
                    exclusive = self.exclusive)

    def new_window(self, window, buffer = None):
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
        if not self.sel_grammars.has_key(window):
            a_window = window
            if self.global_grammars:
                a_window = None
            debug.trace('WinGramMgr.new_window', 
                'window, a_window: %s, %s' % (str(window), str(a_window)))
            self.sel_grammars[window] = self.factory.make_selection(self.app,
                a_window, exclusive = self.exclusive)

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
        if self.sel_grammars.has_key(window):
            self._deactivate_all_window(window)
            del self.sel_grammars[window]
        if self.dict_grammars.has_key(window):
            for a_buffer in self.dict_grammars[window].keys():
                self.dict_grammars[window][a_buffer].cleanup()
                del self.dict_grammars[window][a_buffer]
            del self.dict_grammars[window]

    def buffer_closed(self, buffer):
        """clean up and destroy all grammars for a buffer which 
	has been closed.

	**INPUTS**

	*STR* buffer -- name of buffer

	**OUTPUTS**

	*none*
	"""
        for a_window in self.dict_grammars.keys():
            buffers = self.dict_grammars[a_window]
            if buffers.has_key(buffer):
                buffers[buffer].cleanup()
                del buffers[buffer]

    def using_global(self):
        """checks whether GramMgr creates global grammars, rather than 
	window-specific ones

	**INPUTS**

	*none*

	**OUTPUTS**

	*BOOL* -- true if the global_grammars flag has been set to
	produce global grammars
	"""
        return self.global_grammars

class WinGramMgrFactory(GramMgrFactory):
    """implements GramMgrFactory for WinGramMgr

    **INSTANCE ATTRIBUTES**

    *WinGramFactory* gram_factory -- factory which will supply each
    WinGramMgr with new window-specific dictation and selection grammars.

    *BOOL* global_grammars -- use global grammars, instead of
    window-specific ones (only for testing purposes)

    *BOOL* exclusive -- use exclusive grammars which prevent 
    non-exclusive grammars from getting results (only for testing purposes)

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, gram_factory, global_grammars = 0,
        exclusive = 0, **args):
        """create a GramMgrFactory which creates WinGramMgr objects for
	new editors

	**INPUTS**

	*WinGramFactory* gram_factory -- factory which will supply each
	WinGramMgr with new window-specific dictation and selection grammars.

	*BOOL* global_grammars -- use global grammars, instead of
	window-specific ones (only for testing purposes)

	*BOOL* exclusive -- use exclusive grammars which prevent 
	non-exclusive grammars from getting results (only for testing purposes)

	"""
        self.deep_construct(WinGramMgrFactory, 
                            {'gram_factory': gram_factory,
                             'global_grammars': global_grammars,
                             'exclusive': exclusive
                            }, args)

    def using_global(self):
        """checks whether the GramMgr objects created by the factory use
	global grammars, rather than window-specific ones

	**INPUTS**

	*none*

	**OUTPUTS**

	*BOOL* -- true if the factory has been set to produce GramMgr
	objects with the global_grammars flag set
	"""
        return self.global_grammars

    def new_manager(self, editor, recog_mgr):
        """creates a new GramMgr

	**INPUTS**

	*AppState* editor -- AppState object for which to manage
	grammars
    
	*RecogStartMgr recog_mgr* -- the RecogStartMgr which owns this
	grammar manager

	**OUTPUTS**

	*none*
	"""
        debug.trace('WinGramMgrFactory.new_manager', 
            'new manager: global = ' + str(self.global_grammars))
        return WinGramMgr(app = editor, recog_mgr = recog_mgr,
            factory = self.gram_factory,
            global_grammars = self.global_grammars, exclusive = self.exclusive)

    def new_global_manager(self, editor, recog_mgr, exclusive = 1):
        """creates a new GramMgr using global grammars (regardless of
	the value of self.global_grammars)

	**INPUTS**

	*AppState* editor -- AppState object for which to manage
	grammars
    
	*RecogStartMgr recog_mgr* -- the RecogStartMgr which owns this
	grammar manager

	**OUTPUTS**

	*none*
	"""
        debug.trace('WinGramMgrFactory.new_global_manager', 
            'new global manager')
        return WinGramMgr(app = editor, recog_mgr = recog_mgr,
            factory = self.gram_factory,
            global_grammars = 1, exclusive = exclusive)

# defaults for vim - otherwise ignore
# vim:sw=4

