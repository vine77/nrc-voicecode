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

"""implementation of sr_grammars classes using natlink
"""

from Object import Object
import sr_interface
from sr_grammars import *
import natlink
import debug
from natlinkutils import *

import CmdInterp, AppState

class DictWinGramNL(DictWinGram, DictGramBase):
    """natlink implementation of DictWinGram for window-specific 
    dictation grammar interfaces

    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, **attrs):
        self.deep_construct(DictWinGramNL,
            {}, attrs, exclude_bases = {DictGramBase:1})
        DictGramBase.__init__(self)
        self.load()

    def activate(self):
        """activates the grammar for recognition
	tied to the current window.

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
        if not self.is_active():
            window = self.window
            if window == None:
                window = 0
            DictGramBase.activate(self, window = window, 
                exclusive = self.exclusive)
            self.active = 1

    def remove_other_references(self):
        DictGramBase.unload(self)
        DictWinGram.remove_other_references(self)

    def deactivate(self):
        """disable recognition from this grammar

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
        if self.is_active():
            DictGramBase.deactivate(self)
            self.active = 0

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
        self.setContext(before, after)

    def gotResultsObject(self, recogType, results):
            if recogType == 'self':
#                self.last = SpokenUtteranceNL(results)
# not sure if yet if this is where we should store the utterance
                words = results.getWords(0)
                interp = self.interpreter()
                interp.interpret_NL_cmd(words, self.app)
                # DCF - comment out temporarily to see if this is the
                # source of the problem with dictating over selected
                # text
#                interp.interpret_NL_cmd(words, self.app,
#                    initial_buffer = self.buff_name)
                self.app.print_buff_if_necessary(buff_name
                    = self.buff_name)

class SelectWinGramNL(SelectWinGram, SelectGramBase):
    """natlink implementation of SelectWinGram for window-specific 
    selection grammar interfaces

    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, **attrs):
        self.deep_construct(SelectWinGramNL,
            {}, attrs, exclude_bases = {SelectGramBase:1})
        SelectGramBase.__init__(self)
        self.load(selectWords = self.select_words, throughWord =
            self.through_word)

    def _set_visible(self, visible):
        """internal call to set the currently visible range.

	**INPUTS**

	*STR* visible -- visible text range 

	**OUTPUTS**

	*none*
	"""
        SelectGramBase.setSelectText(self, visible)

    def activate(self, buff_name):
        """activates the grammar for recognition tied to the current window,
	and checks with buffer for the currently visible range.

	**INPUTS**

	*STR* buff_name -- name of currently active buffer

	**OUTPUTS**

	*none*
	"""
        self.buff_name = buff_name
        self.find_visible()

        if not self.is_active():
            window = self.window
            if window == None:
                window = 0
            SelectGramBase.activate(self, window = window, 
                exclusive = self.exclusive)
            self.active = 1


    def deactivate(self):
        """disable recognition from this grammar

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
        if self.is_active():
            DictGramBase.deactivate(self)
            self.active = 0

    def cleanup(self):
        SelectGramBase.unload(self)
        SelectWinGram.cleanup(self)
    
    def buffer_name(self):
        """returns name of buffer corresponding to this selection grammar.

	**INPUTS**

	*none*
    
	**OUTPUTS**

	*STR* -- name of buffer currently used by this selection grammar.
	"""

        return self.buff_name
    
    def gotResultsObject(self,recogType,resObj):
        if recogType == 'self':
            # If there are multiple matches in the text we need to scan through
            # the list of choices to find every entry which has the highest.
            
            ranges = []        
            try:
                bestScore = resObj.getWordInfo(0)[0][2]
                verb = resObj.getWordInfo(0)[0][0]

                #
                # Collect selection ranges with highest score
                #
                for i in range(100):
                    #
                    # The candidate regions are sorted from best to worst scores.
                    # Loop through candidate regions until we reach one whose
                    # score is not the same as the first score (or until a
                    # natlink.outOfRange exception is raised to signal the end
                    # of the list of candidate regions).
                    #
                    wordInfo = resObj.getWordInfo(i)
                    if wordInfo[0][2] != bestScore:
                        #
                        # All remaining regions don't have as good a score as the
                        # first ones.
                        break
                    else:
                        #
                        # This region has the same score as the first ones. Add it
                        # to the candidate selection ranges.
                        #
                        region = resObj.getSelectInfo(self.gramObj, i)

                        
                        true_region = (region[0] + self.vis_start,
                          region[1] + self.vis_start)
                        ranges.append(true_region)

            except natlink.OutOfRange:
                pass

            spoken = self.selection_spoken_form(resObj)
            self.find_closest(verb, spoken, ranges)

    def selection_spoken_form(self, resObj):

        """Returns the spoken form of the selected part of a *Select
        Pseudocode* utterance.
        
        **INPUTS**
        
        *ResObj* resObj -- The *ResObj* returned by the *Select* grammar.
        

        **OUTPUTS**
        
        *spoken_form* -- The spoken form of the selected code.
        """
                
        spoken_form = ''
        #
        # Ignore first word because it is the verb
        #
        for a_word_info in resObj.getWordInfo(0)[1:]:
            a_spoken_word, dummy = sr_interface.spoken_written_form(a_word_info[0])
            if spoken_form != '':
                spoken_form = spoken_form + ' '
            spoken_form = spoken_form + a_spoken_word

#        print '-- CodeSelectGrammar.selection_spoken_form: returning spoken_form=%s' % spoken_form
        
        return spoken_form

class WinGramFactoryNL(WinGramFactory):
    """natlink implementation of factory which returns 
    window-specific grammars

    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, **attrs):
        """
	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
        self.deep_construct(WinGramFactoryNL,
            {}, attrs)

    def make_dictation(self, manager, app, buff_name, window = None,
        exclusive = 0):
        """create a new dictation grammar

	**INPUTS**

	*WinGramMgr* manager -- the grammar manager which will own the
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
        return DictWinGramNL(manager = manager, app = app, 
            buff_name = buff_name, window = window, exclusive = exclusive) 
    
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

	*BOOL* exclusive -- is grammar exclusive?  (prevents other
	non-exclusive grammars from getting results)

	**OUTPUTS**

	*SelectWinGram* -- new selection grammar
	"""
        return SelectWinGramNL(app = app, buff_name = buff_name, select_words =
            self.select_words, through_word = self.through_word, 
            window = window, exclusive = exclusive) 
    
