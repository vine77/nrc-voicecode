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

"""abstract interfaces for dictation and selection grammars
"""

from Object import Object
import debug

import CmdInterp, AppState

class WinGram(Object):
    """abstract base class for window-specific grammar interfaces

    **INSTANCE ATTRIBUTES**

    *BOOL* active -- is grammar active?

    *BOOL* exclusive -- is grammar exclusive?  (prevents other
    non-exclusive grammars from getting results)

    *BOOL* all_results -- does grammar intercept all results, even for
    other grammars?

    *INT* window -- window handle (unique identifier) for
    window-specific grammars (even if active, will only receive results
    when the corresponding window has the focus).

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, window = None, exclusive = 0, all_results = 0, **attrs):
	self.deep_construct(WinGram,
	    {'window' : window, 'exclusive' : exclusive, 
	    'all_results': all_results,
	    'active' : 0}, attrs)

    def activate(self, window = None, exclusive = 0, all_results = 0):
	"""activates the grammar for recognition
	tied to the current window.

	**INPUTS**

	*INT* window -- make grammar window-specific.  Specify None 
	to make the grammar global

	*BOOL* exclusive -- make grammar exclusive?  (prevents other
	non-exclusive grammars from getting results.  Use with caution)

	*BOOL* all_results -- make grammar intercept all results, even for
	other grammars

	**OUTPUTS**

	*none*
	"""
	debug.virtual('WinGram.activate')
    
    def deactivate(self):
	"""disable recognition from this grammar

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	debug.virtual('WinGram.deactivate')

    def window(self):
	"""window to which the grammar is specific (or None for 
	a global grammar)

	**INPUTS**

	*none*
    
	**OUTPUTS**

	*INT* -- window handle (None indicates global)
	"""
	return self.window

    def is_exclusive(self):
	"""is the grammar exclusive?

	**INPUTS**

	*none*
    
	**OUTPUTS**

	*BOOL* -- exclusive?
	"""
	return self.exclusive

    def is_greedy(self):
	"""does the grammar capture all results?

	**INPUTS**

	*none*
    
	**OUTPUTS**

	*BOOL* -- captures all results?
	"""
	return self.all_results

    def reactivate(self):
	"""reactivate recognition using the same window (or globally).

	**INPUTS**

	*none*
    
	**OUTPUTS**

	*none*
	"""
	debug.virtual('WinGram.reactivate')

    def is_active(self):
	"""indicates whether the grammar is active for recognition 

	**INPUTS**

	*none*

	**OUTPUTS**

	*BOOL* -- returns true iff the grammar is active
	"""
	return self.active

    def is_global(self):
	"""tells whether the grammar is global

	**INPUTS**

	*none*

	**OUTPUTS**

	*BOOL* -- is grammar set for global (window-independent)
	recognition.
	"""
	return self.window == None

class DictWinGram(WinGram):
    """abstract base class for window-specific dictation grammar interfaces

    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, **attrs):
	self.deep_construct(DictWinGram,
	    {}, attrs)

    def set_context(self, before = "", after = ""):
	"""set the context to improve dictation accuracy

	**INPUTS**

	*STR* before -- one or more words said immediately before the
	next utterance, or found in the text immediately before the
	utterance

	*STR* after -- one or more words found in the text
	immediately after the utterance def activate(self, window =
	None, exclusive = 0)

	**OUTPUTS**

	*none*
	"""
	debug.virtual('DictWinGram.set_context')


class SelectWinGram(WinGram):
    """abstract base class for dictation grammar interfaces

    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, buff_name = None, **attrs):
	"""
	**INPUTS**
	
	*STR* buff_name - name of buffer to which to tie this 
	selection grammar (can also be set by activate)
	"""
	self.deep_construct(SelectWinGram,
	    {'buff_name' : buff_name}, attrs)

    def activate(self, buff_name, window = None, exclusive = 0, 
	all_results = 0):
	"""activates the grammar for recognition tied to the current window,
	and checks with buffer for the currently visible range.

	**INPUTS**

	*STR* buff_name -- name of currently active buffer

	*INT* window -- make grammar window-specific.  Specify None 
	to make the grammar global

	*BOOL* exclusive -- make grammar exclusive?  (prevents other
	non-exclusive grammars from getting results.  Use with caution)

	*BOOL* all_results -- make grammar intercept all results, even for
	other grammars

	**OUTPUTS**

	*none*
	"""
	debug.virtual('SelectWinGram.activate')
    
    def buff_name(self):
        """returns name of buffer corresponding to this selection grammar.

	**INPUTS**

	*none*
    
	**OUTPUTS**

	*STR* -- name of buffer currently used by this selection grammar.
	"""

	return self.buff_name


    def reactivate(self):
	"""reactivate recognition using the same buffer name and
	same window (or globally).

	**INPUTS**

	*none*
    
	**OUTPUTS**

	*none*
	"""
	debug.virtual('SelectWinGram.reactivate')


class WinGramFactory(Object):
    """abstract base class for a factory which returns 
    window-specific grammars

    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, **attrs):
	"""no arguments: abstract base class
	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	self.deep_construct(WinGramFactory,
	    {}, attrs)

    def make_dictation(self, app, buff_name, window = None):
	"""create a new dictation grammar

	**INPUTS**

	*AppState* app -- application to which to forward results

	*STR* buff_name -- name of the buffer corresponding to this
	grammar.  Buff_name will be passed to
	CmdInterp.interpret_NL_cmd as the initial buffer.

	*INT* window -- make grammar specific to a particular window

	**OUTPUTS**

	*DictWinGram* -- new dictation grammar
	"""
	debug.virtual('WinGramFactory.make_dictation')
    
    def make_selection(self, app, window = None, buff_name = None):
	"""create a new selection grammar

	**INPUTS**

	*AppState* app -- application corresponding to the selection
	grammar, which is queried with buff_name for the currently
	visible range, and is notified of selection changes

	*STR* buff_name -- name of the buffer corresponding to this
	grammar.  Can also be set later in the activate call to the
	grammar.

	**OUTPUTS**

	*SelectWinGram* -- new selection grammar
	"""
	debug.virtual('WinGramFactory.make_selection')
    
class DictWinGramDummy(DictWinGram):
    """dummy implementation of window-specific dictation grammar 

    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, **attrs):
	self.deep_construct(DictWinGramDummy,
	    {}, attrs)
	self.identify_grammar()
	print "init"

    def __del__(self):
	self.identify_grammar()
	print "del"

    def identify_grammar(self):
        """print information identifying the grammar by buffer and
	window

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	print "DictWinGramDummy for window %d" % (self.window)

    def set_context(self, before = "", after = ""):
	"""set the context to improve dictation accuracy

	**INPUTS**

	*STR* before -- one or more words said immediately before the
	next utterance, or found in the text immediately before the
	utterance

	*STR* after -- one or more words found in the text
	immediately after the utterance def activate(self, window =
	None, exclusive = 0)

	**OUTPUTS**

	*none*
	"""
	self.identify_grammar()
	print "setting context: before = [%s], after = [%s]" % (before,
	    after)

    def activate(self, window = None, exclusive = 0, all_results = 0):
	"""activates the grammar for recognition
	tied to the current window.

	**INPUTS**

	*INT* window -- make grammar window-specific.  Specify None 
	to make the grammar global

	*BOOL* exclusive -- make grammar exclusive?  (prevents other
	non-exclusive grammars from getting results.  Use with caution)

	*BOOL* all_results -- make grammar intercept all results, even for
	other grammars

	**OUTPUTS**

	*none*
	"""
	self.window = window
	self.exclusive = exclusive
	self.all_results = all_results
	self.identify_grammar()
	print "activating: ",
	if window == None:
	    print "global ",
	else:
	    print "%d " % (window),
	if exclusive:
	    print "exclusive "
	if all_results:
	    print "all_results"
	print ""
	self.active = 1
    
    def deactivate(self):
	"""disable recognition from this grammar

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	self.identify_grammar()
	self.active = 0
	print "deactivating"

    def reactivate(self):
	"""reactivate recognition using the same buffer name and
	same window (or globally).

	**INPUTS**

	*none*
    
	**OUTPUTS**

	*none*
	"""
	self.identify_grammar()
	self.active = 1
	print "reactivating"

class SelectWinGramDummy(SelectWinGram):
    """dummy implementation of window-specific selection grammar 

    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, **attrs):
	"""
	**INPUTS**

	*none*
	"""
	self.deep_construct(SelectWinGramDummy,
	    {}, attrs)
	self.identify_grammar()
	print "init"

    def __del__(self):
	self.identify_grammar()
	print "del"

    def identify_grammar(self):
        """print information identifying the grammar by buffer and
	window

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	print "SelectWinGramDummy for buffer %s, window %d" % \
	    (self.buff_name, self.window)

    def activate(self, buff_name, window = None, exclusive = 0, 
	all_results = 0):
	"""activates the grammar for recognition tied to the current window,
	and checks with buffer for the currently visible range.

	**INPUTS**

	*STR* buff_name -- name of currently active buffer

	*INT* window -- make grammar window-specific.  Specify None 
	to make the grammar global

	*BOOL* exclusive -- make grammar exclusive?  (prevents other
	non-exclusive grammars from getting results.  Use with caution)

	*BOOL* all_results -- make grammar intercept all results, even for
	other grammars

	**OUTPUTS**

	*none*
	"""
	self.buff_name = buff_name
	self.window = window
	self.exclusive = exclusive
	self.all_results = all_results
	self.identify_grammar()
	self.active = 1
	print "activating: ",
	if window == None:
	    print "global ",
	else:
	    print "%d " % (window),
	if exclusive:
	    print "exclusive "
	if all_results:
	    print "all_results"
	print ""
    
    def reactivate(self):
	"""reactivate recognition using the same buffer name and
	same window (or globally).

	**INPUTS**

	*none*
    
	**OUTPUTS**

	*none*
	"""
	self.identify_grammar()
	self.active = 1
	print "reactivating"

    def deactivate(self):
	"""disable recognition from this grammar

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	self.identify_grammar()
	self.active = 0
	print "deactivating"

class WinGramFactoryDummy(Object):
    """implementation fo WinGramFactory with dummy grammars for
    regression testing.

    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, **attrs):
	"""no arguments: abstract base class
	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	self.deep_construct(WinGramFactoryDummy,
	    {}, attrs)

    def make_dictation(self, app, buff_name, window = None):
	"""create a new dictation grammar

	**INPUTS**

	*AppState* app -- application to which to forward results

	*STR* buff_name -- name of the buffer corresponding to this
	grammar.  Buff_name will be passed to
	CmdInterp.interpret_NL_cmd as the initial buffer.

	*INT* window -- make grammar specific to a particular window

	**OUTPUTS**

	*DictWinGram* -- new dictation grammar
	"""
	return DictWinGramDummy(window = window)
    
    def make_selection(self, app, window = None, buff_name = None):
	"""create a new selection grammar

	**INPUTS**

	*AppState* app -- application corresponding to the selection
	grammar, which is queried with buff_name for the currently
	visible range, and is notified of selection changes

	*STR* buff_name -- name of the buffer corresponding to this
	grammar.  Can also be set later in the activate call to the
	grammar.

	**OUTPUTS**

	*SelectWinGram* -- new selection grammar
	"""
	return SelectWinGramDummy(window = window, buff_name = buff_name)
    