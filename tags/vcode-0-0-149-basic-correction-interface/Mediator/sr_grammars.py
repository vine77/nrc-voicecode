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

from Object import Object, OwnerObject
import debug
import re
import actions_gen

import CmdInterp, AppState

class WinGram(Object):
    """abstract base class for window-specific grammar interfaces

    **INSTANCE ATTRIBUTES**

    *BOOL* active -- is grammar active?

    *BOOL* exclusive -- is grammar exclusive?  (prevents other
    non-exclusive grammars from getting results)

    *INT* window -- window handle (unique identifier) for
    window-specific grammars (even if active, will only receive results
    when the corresponding window has the focus).

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, window = None, exclusive = 0, **attrs):
        self.deep_construct(WinGram,
            {'window' : window, 'exclusive' : exclusive, 
            'active' : 0}, attrs)

    def activate(self):
        """activates the grammar for recognition
	tied to the current window.

	**INPUTS**

	*none*

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

class DictWinGram(WinGram, OwnerObject):
    """abstract base class for window-specific dictation grammar interfaces

    **INSTANCE ATTRIBUTES**

    *WinGramMgr* manager -- the grammar manager which owns this grammar

    *AppState* app -- application which is the target of the grammar

    *STR* buff_name -- name of the buffer corresponding to this
    grammar.  Buff_name will be passed to
    CmdInterp.interpret_NL_cmd as the initial buffer.

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, manager, app, buff_name = None, **attrs):
        self.deep_construct(DictWinGram,
            {'manager': manager, 'app': app,'buff_name': buff_name}, attrs)
        self.name_parent('manager')

    def interpreter(self):
        """return a reference to the mediator's current CmdInterp object

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
        return self.manager.interpreter()

    def rename_buffer_cbk(self, new_buff_name):
        """callback from GramMgr which notifies us that the application
	has renamed buffer corresponding to this dictation grammar

	**INPUTS**

	*STR* new_buff_name -- new name of the buffer 

	*none*
	"""
        self.buff_name = new_buff_name

    def set_context(self, before = "", after = ""):
        """set the context to improve dictation accuracy

	**INPUTS**

	*STR* before -- one or more words said immediately before the
	next utterance, or found in the text immediately before the
	utterance

	*STR* after -- one or more words found in the text
	immediately after the utterance 

	**OUTPUTS**

	*none*
	"""
        debug.virtual('DictWinGram.set_context')

    def on_results(self, results):
        """interpret the results of recognition.  This method must be
        called by the concrete subclass of DictWinGram.

        **INPUTS**

        *SpokenUtterance results* -- the SpokenUtterance object
        representing the recognition results

        **OUTPUTS**

        *none*
        """
        self.manager.interpret_dictation(results, \
            initial_buffer = self.buff_name)
# old implementation - now taken care of by the ResMgr
#        interp = self.interpreter()
#        interp.interpret_NL_cmd(words, self.app,
#            initial_buffer = self.buff_name)
#        self.app.print_buff_if_necessary(buff_name = self.buff_name)




class SelectWinGram(WinGram):
    """abstract base class for selection grammar interfaces

    **INSTANCE ATTRIBUTES**

    *AppState* app -- application to which results will be sent
    
    *STR* buff_name -- name of buffer to which to tie this 
    selection grammar (can also be set by activate)

    *[STR]* select_words -- words (or phrases) which introduces a
    selection utterance

    *STR* through_word -- word which separates the beginning and end of
    a range to be selected.

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, app, buff_name = None, select_words = ['select'],
        through_word = 'through', **attrs):
        """
	**INPUTS**

	*AppState* app -- application to which results will be sent
	
	*STR* buff_name -- name of buffer to which to tie this 
	selection grammar (can also be set by activate)
	"""
        self.deep_construct(SelectWinGram,
            {'app': app,'buff_name' : buff_name, 
            'select_words' : select_words, 'through_word' : through_word}, 
            attrs)

    def cleanup(self):
        """SelectWinGram has a reference to an AppState instance, but no
	circular references, so strictly speaking it is only necessary
	for the grammar manager to delete its reference to the grammar.
	However, a dummy cleanup method allows us to avoid the need for
	a custom cleanup method for GramMgr.
	"""
# not necessary, but can't hurt
        self.app = None

    def _set_visible(self, visible):
        """internal call to set the currently visible range.

	**INPUTS**

	*STR* visible -- visible text range 

	**OUTPUTS**

	*none*
	"""
        debug.virtual('SelectWinGram._set_visible')

    def find_visible(self):
        """find the currently visible range for self.buff_name
	and checks with buffer for the currently visible range.

	**INPUTS**

	*STR* buff_name -- name of currently active buffer

	**OUTPUTS**

	*none*
	"""
        buff_name = self.buff_name
        vis_start, vis_end = self.app.get_visible(buff_name = buff_name)
        self.vis_start = vis_start
        visible = \
            self.app.get_text(vis_start, vis_end, buff_name = buff_name)
        self._set_visible(visible)

    def activate(self, buff_name):
        """activates the grammar for recognition tied to the current window,
	and checks with buffer for the currently visible range.

	**INPUTS**

	*STR* buff_name -- name of currently active buffer

	**OUTPUTS**

	*none*
	"""
        debug.virtual('SelectWinGram.activate')


    def buffer_name(self):
        """returns name of buffer corresponding to this selection grammar.

	**INPUTS**

	*none*
    
	**OUTPUTS**

	*STR* -- name of buffer currently used by this selection grammar.
	"""

        return self.buff_name
    
    def find_closest(self, verb, spoken_form, ranges):
        """Sort the ranges from earliest to latest, and select the one
        which is closest to the cursor in the proper direction

        **INPUTS**

        *STR* verb -- verb used by the selection

        *STR* spoken_form -- The spoken form of the selected code.

        *[(INT, INT)] -- list of ranges of offsets into buffer with the
        best recognition score
        """
        
        #
        # Analyse the verb used by the user in the Select utterance
        #
        debug.trace('SelectWinGram.find_closest', 'invoked')
        direction = None
        if re.search('previous', verb, 1):
            direction = -1
        if re.search('next', verb, 1):                
            direction = 1

        mark_selection = 1
        if re.search('go', verb, 1) or re.search('before', verb, 1) or \
           re.search('after', verb, 1):
            mark_selection = 0

        where = 1
        if re.search('before', verb, 1):
            where = -1
        if re.search('after', verb, 1):
            where = 1



        #
        ranges.sort()
        closest_range_index = \
            self.app.closest_occurence_to_cursor(ranges, 
                regexp=spoken_form, 
                direction=direction, where=where, 
                buff_name = self.buff_name)
        if closest_range_index == None:
            return

        #
        # Mark selection and/or move cursor  to the appropriate end of
        # the selection.
        #
        if mark_selection:
            a = actions_gen.ActionSelect(range = \
                ranges[closest_range_index],
                buff_name = self.buff_name,
                cursor_at=where)
            a.log_execute(self.app, None)
        else:
            if where > 0:
                pos = ranges[closest_range_index][1]
            else:
                pos = ranges[closest_range_index][0]
            self.app.goto(pos, buff_name = self.buff_name)

# this is needed for the EdSim mediator simulator.  We want EdSim to
# refresh at the end of interpretation of a whole utterance, not with 
# every change to the buffer.  Other editors will usually refresh
# instantly and automatically, so their AppState/SourceBuff
# implementations can simply ignore the print_buff_if_necessary message.

        self.app.print_buff_if_necessary(buff_name = self.buff_name)

        #
        # Log the selected occurence so that if the user repeats the
        # same Select Pseudocode operation we don't end up selecting
        # the same occurence again
        #
        self.app.log_search(regexp=spoken_form, 
            direction=direction, where=where, 
            match=ranges[closest_range_index],
            buff_name = self.buff_name)


class BasicCorrectionWinGram(WinGram, OwnerObject):
    """abstract base class for window-specific grammar for basic
    correction (Scratch That/n, Correct That, Correct Recent)

    **INSTANCE ATTRIBUTES**

    *WinGramMgr* manager -- the grammar manager which owns this grammar

    *[STR]* scratch_words -- list of synonyms for Scratch in "Scratch
    That" and "Scratch n"

    *[STR]* correct_words -- list of synonyms for Correct in "Correct
    That" and "Correct Recent" 

    *[STR]* recent_words -- list of synonyms for Recent in "Correct Recent"

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, manager, scratch_words = None, correct_words = None,
        recent_words = None, **attrs):
        """
        **INPUTS**

        *WinGramMgr* manager -- the grammar manager which owns this grammar

        *[STR]* scratch_words -- list of synonyms for Scratch in "Scratch
        That" and "Scratch n", or None for the default of 'Scratch'

        *[STR]* correct_words -- list of synonyms for Correct in "Correct
        That" and "Correct Recent"  or None for the default of 'Correct'

        *[STR]* recent_words -- list of synonyms for 
        Recent in "Correct Recent" or None for the dfault of 'Recent
        """
        self.deep_construct(BasicCorrectionWinGram,
            {'manager': manager, 
             'scratch_words': scratch_words,
             'correct_words': correct_words,
             'recent_words': recent_words
            }, attrs)
        if scratch_words is None:
            self.scratch_words = ['Scratch']
        if correct_words is None:
            self.correct_words = ['Correct']
        if recent_words is None:
            self.recent_words = ['Recent']
        self.name_parent('manager')

    def scratch_recent(self, n = 1):
        """method which subclass must call when the grammar 
        recognizes Scratch That/Scratch n, to undo the effect of the 
        most recent n utterances, if possible.

        **INPUTS**

        *INT n* -- number of utterances to undo

        **OUTPUTS**
        
        *INT* -- number of utterances successfully undone
        """
        debug.trace('BasicCorrectionWinGram.scratch_recent', 
            'trying to scratch %d' %n)
        n_done = self.manager.scratch_recent(n)
        debug.trace('BasicCorrectionWinGram.scratch_recent', 
            'actually scratched %d' %n_done)
        return n_done


    def on_correct_last(self):
        """method which subclass must call when the grammar 
        recognizes Correct That with nothing selected

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        self.manager.correct_last()

    def on_correct_recent(self):
        """method which subclass must call when the grammar 
        recognizes Correct Recent 

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        self.manager.correct_recent(self)


class WinGramFactory(Object):
    """abstract base class for a factory which returns 
    window-specific grammars

    **INSTANCE ATTRIBUTES**

    *[STR]* select_words -- list of words which can precede the
    phrase from the visible text in selection grammars

    *STR* through_word -- word for selecting a range with the 
    selection grammars

    *[STR]* scratch_words -- list of synonyms for Scratch in "Scratch
    That" and "Scratch n" in basic correction grammars

    *[STR]* correct_words -- list of synonyms for Correct in "Correct
    That" and "Correct Recent"  in basic correction grammars

    *[STR]* recent_words -- *[STR]* correct_words -- list of synonyms for 
    Recent in "Correct Recent" in basic correction grammars

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, select_words = ['go', 'go after next', 
        'go after previous', 'go before',
        'go before next', 'go before previous', 'go next',
        'go previous', 'after next', 'after previous', 'before',
        'before next', 'before previous', 
#        'correct', 'correct next', 'correct previous', 
        'next', 'previous',
        'select', 'select next', 'select previous', 'after'], 
        through_word = 'through',
        scratch_words = None,
        correct_words = None,
        recent_words = None,
        **attrs):
        """
	**INPUTS**

	*[STR]* select_words -- list of words which can precede the
	phrase from the visible text in selection grammars

	*STR* through_word -- word for selecting a range with the 
	selection grammars

        *[STR]* scratch_words -- list of synonyms for Scratch in "Scratch
        That" and "Scratch n", or None for the default of 'Scratch'

        *[STR]* correct_words -- list of synonyms for Correct in "Correct
        That" and "Correct Recent"  or None for the default of 'Correct'

        *[STR]* recent_words -- list of synonyms for 
        Recent in "Correct Recent" or None for the dfault of 'Recent

	**OUTPUTS**

	*none*
	"""
        self.deep_construct(WinGramFactory,
            {'select_words' : select_words, 
             'through_word' : through_word,
             'scratch_words': scratch_words,
             'correct_words': correct_words,
             'recent_words': recent_words}, 
            attrs)

    def make_dictation(self, manager, app, buff_name, window = None,
        exclusive = 0):
        """create a new dictation grammar

	**INPUTS**

	*WinGramMgr* manager -- the grammar manager which will own the new
	grammar

	*AppState* app -- application which is the target of the grammar

	*STR* buff_name -- name of the buffer corresponding to this
	grammar.  Buff_name will be passed to
	CmdInterp.interpret_NL_cmd as the initial buffer.

	*INT* window -- make grammar specific to a particular window

	*BOOL* exclusive -- is grammar exclusive?  (prevents other
	non-exclusive grammars from getting results)
	
	**OUTPUTS**

	*DictWinGram* -- new dictation grammar
	"""
        debug.virtual('WinGramFactory.make_dictation')
    
    def make_selection(self, app, window = None, buff_name = None,
        exclusive = 0):
        """create a new selection grammar

	**INPUTS**

	*AppState* app -- application corresponding to the selection
	grammar, which is queried with buff_name for the currently
	visible range, and is notified of selection changes

	*STR* buff_name -- name of the buffer corresponding to this
	grammar.  Can also be set later in the activate call to the
	grammar.

	*INT* window -- make grammar specific to a particular window

	*BOOL* exclusive -- is grammar exclusive?  (prevents other
	non-exclusive grammars from getting results)

	**OUTPUTS**

	*SelectWinGram* -- new selection grammar
	"""
        debug.virtual('WinGramFactory.make_selection')

    def make_correction(self, manager, window = None, exclusive = 0):
        """create a new basic correction grammar

	**INPUTS**

        *WinGramMgr* manager -- the grammar manager which owns this grammar

	*INT* window -- make grammar specific to a particular window

	*BOOL* exclusive -- is grammar exclusive?  (prevents other
	non-exclusive grammars from getting results)

	**OUTPUTS**

	*BasicCorrectionWinGram* -- new basic correction grammar
	"""
        debug.virtual('WinGramFactory.make_correction')
    
    
class DictWinGramDummy(DictWinGram):
    """dummy implementation of window-specific dictation grammar 

    **INSTANCE ATTRIBUTES**

    *BOOL* silent -- don't print diagnostics

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, silent = 0, **attrs):
        self.deep_construct(DictWinGramDummy,
            {'silent': silent}, attrs)
        if not self.silent:
            self.identify_grammar()
            print "init"

    def __del__(self):
        if not self.silent:
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
        if self.window == None:
            winname = "global"
        else:
            winname = "window %d" % self.window
        print "DictWinGramDummy for buffer = %s, %s" % \
            (repr(self.buff_name), winname)

    def set_context(self, before = "", after = ""):
        """set the context to improve dictation accuracy

	**INPUTS**

	*STR* before -- one or more words said immediately before the
	next utterance, or found in the text immediately before the
	utterance

	*STR* after -- one or more words found in the text
	immediately after the utterance 

	**OUTPUTS**

	*none*
	"""
        if not self.silent:
            self.identify_grammar()
            print "setting context: before = [%s], after = [%s]" % (before,
                after)

    def activate(self):
        """activates the grammar for recognition
	tied to the current window.

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
        if not self.silent:
            self.identify_grammar()
            print "activating: ",
            if self.window == None:
                print "global ",
            else:
                print "%d " % (self.window),
            if self.exclusive:
                print "exclusive "
            print ""
        self.active = 1
    
    def deactivate(self):
        """disable recognition from this grammar

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
        if not self.silent:
            self.identify_grammar()
            print "deactivating"
        self.active = 0

class SelectWinGramDummy(SelectWinGram):
    """dummy implementation of window-specific selection grammar 

    **INSTANCE ATTRIBUTES**

    *BOOL* silent -- don't print diagnostics

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, silent = 0, **attrs):
        """
	**INPUTS**

	*none*
	"""
        self.deep_construct(SelectWinGramDummy,
            {'silent': silent}, attrs)
        if not self.silent:
            self.identify_grammar()
            print "init"

    def __del__(self):
        if not self.silent:
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
        if self.window == None:
            winname = "global"
        else:
            winname = "window %d" % self.window
        print "SelectWinGramDummy for buffer %s, %s" % \
            (repr(self.buff_name), winname)

    def activate(self, buff_name):
        """activates the grammar for recognition tied to the current window,
	and checks with buffer for the currently visible range.

	**INPUTS**

	*STR* buff_name -- name of currently active buffer

	**OUTPUTS**

	*none*
	"""
        self.buff_name = buff_name
        self.active = 1
        if not self.silent:
            self.identify_grammar()
            print "activating: ",
            if self.window == None:
                print "global ",
            else:
                print "%d " % (self.window),
            if self.exclusive:
                print "exclusive "
            print ""
    
    def deactivate(self):
        """disable recognition from this grammar

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
        if not self.silent:
            self.identify_grammar()
            print "deactivating"
        self.active = 0

class BasicCorrectionWinGramDummy(BasicCorrectionWinGram):
    """dummy implementation of window-specific basic correction grammar 

    **INSTANCE ATTRIBUTES**

    *BOOL* silent -- don't print diagnostics

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, silent = 0, **attrs):
        self.deep_construct(BasicCorrectionWinGramDummy,
            {'silent': silent}, attrs)
        if not self.silent:
            self.identify_grammar()
            print "init"

    def __del__(self):
        if not self.silent:
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
        if self.window == None:
            winname = "global"
        else:
            winname = "window %d" % self.window
        print "BasicCorrectionWinGramDummy for window = %s" % winname

    def activate(self):
        """activates the grammar for recognition
	tied to the current window.

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
        if not self.silent:
            self.identify_grammar()
            print "activating: ",
            if self.window == None:
                print "global ",
            else:
                print "%d " % (self.window),
            if self.exclusive:
                print "exclusive "
            print ""
        self.active = 1
    
    def deactivate(self):
        """disable recognition from this grammar

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
        if not self.silent:
            self.identify_grammar()
            print "deactivating"
        self.active = 0


class WinGramFactoryDummy(Object):
    """implementation fo WinGramFactory with dummy grammars for
    regression testing.

    **INSTANCE ATTRIBUTES**

    *BOOL* silent -- don't print diagnostics

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, silent = 0, **attrs):
        """
	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
        self.deep_construct(WinGramFactoryDummy,
            {}, attrs)

    def make_dictation(self, manager, app, buff_name, window = None,
        exclusive = 0):
        """create a new dictation grammar

	**INPUTS**

	*WinGramMgr* manager -- the grammar manager which will own the new
	grammar

	*AppState* app -- application to which to forward results

	*STR* buff_name -- name of the buffer corresponding to this
	grammar.  Buff_name will be passed to
	CmdInterp.interpret_NL_cmd as the initial buffer.

	*INT* window -- make grammar specific to a particular window

	*BOOL* exclusive -- is grammar exclusive?  (prevents other
	non-exclusive grammars from getting results)

	**OUTPUTS**

	*DictWinGram* -- new dictation grammar
	"""
        return DictWinGramDummy(manager = manager, app = app, 
            buff_name = buff_name, window = window, exclusive =
            exclusive)
    
    def make_selection(self, app, window = None, buff_name = None,
        exclusive = 0):
        """create a new selection grammar

	**INPUTS**

	*AppState* app -- application corresponding to the selection
	grammar, which is queried with buff_name for the currently
	visible range, and is notified of selection changes

	*STR* buff_name -- name of the buffer corresponding to this
	grammar.  Can also be set later in the activate call to the
	grammar.

	*BOOL* exclusive -- is grammar exclusive?  (prevents other
	non-exclusive grammars from getting results)

	**OUTPUTS**

	*SelectWinGram* -- new selection grammar
	"""
        return SelectWinGramDummy(app = app, buff_name = buff_name, 
            window = window, exclusive = exclusive)

    def make_correction(self, manager, window = None, exclusive = 0):
        """create a new basic correction grammar

	**INPUTS**

        *WinGramMgr* manager -- the grammar manager which owns this grammar

	*INT* window -- make grammar specific to a particular window

	*BOOL* exclusive -- is grammar exclusive?  (prevents other
	non-exclusive grammars from getting results)

	**OUTPUTS**

	*BasicCorrectionWinGram* -- new basic correction grammar
	"""
        return BasicCorrectionWinGramDummy(window = window, 
            exclusive = exclusive)
    
    
