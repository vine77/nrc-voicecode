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

""" interfaces which represent the speech information from spoken
utterances, including recognition results, alternatives, adaption,
and playback
"""

from Object import Object
import debug

class SpokenUtterance(Object):
    """defines an abstract interface for manipulating the speech
    information associated with a single user utterance

    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, **attrs):
        self.deep_construct(SpokenUtterance,
            {}, attrs)

    def spoken_forms(self):
        """returns list of spoken forms from the utterance

	**INPUTS**

	*none*

	**OUTPUTS**

	*[STR]* -- list of spoken forms from the utterance
	"""
        debug.virtual('SpokenUtterance.spoken_forms')

    def words(self):
        """returns list of words (as (spoken, written) 2-tuples) 
	from the utterance.

	**INPUTS**

	*none*

	**OUTPUTS**

	*[(STR, STR)]* -- list of words (as (spoken, written) 2-tuples) 
	
	"""
        debug.virtual('SpokenUtterance.words')
      
    def adapt(self, words):
        """changes the stored list of words so that 
	subsequent correction boxes can display the corrected list, and
	informs the speech engine of the corrected list of words, so
	it can adapt.

	**INPUTS**

	*[(STR, STR)]* -- corrected list of words 
	(as (spoken, written) 2-tuples) 

	**OUTPUTS**

	*BOOL* -- true if the adaption was accepted
	"""
        debug.virtual('SpokenUtterance.adapt')

    def adapt_spoken(self, spoken_forms):
        """changes the stored list of words so that 
	subsequent correction boxes can display the corrected list, and
	informs the speech engine of the corrected list of words, so
	it can adapt.


	**INPUTS**

	*[STR]* spoken_forms -- corrected list of spoken forms 
	(written forms will be assumed to be identical)

	**OUTPUTS**

	*BOOL* -- true if the adaption was accepted
	"""
        debug.virtual('SpokenUtterance.adapt_spoken')

    def set_words(self, words):
        """changes the stored list of words (after correction) so that 
	subsequent correction boxes can display the corrected list.
	The results object is unaffected.

	**INPUTS**

	*[(STR, STR)]* -- corrected list of words 
	(as (spoken, written) 2-tuples) 

	**OUTPUTS**

	*none*

	"""
        debug.virtual('SpokenUtterance.set_words')

    def set_spoken(self, spoken_forms):
        """changes the stored list of words (after correction) so that 
	subsequent correction boxes can display the corrected list.
	The results object is unaffected.

	**INPUTS**

	*[STR]* spoken_forms -- corrected list of spoken forms 
	(written forms will be assumed to be identical)

	**OUTPUTS**

	*none*

	"""
        debug.virtual('SpokenUtterance.set_spoken')

    def playback_available(self):
        """indicates whether playback of the utterance is available.

	**INPUTS**

	*none*

	**OUTPUTS**

	*BOOL* -- true if playback is available, false if it is not
	(because utterance wasn't actually spoken, or speech data has 
	been lost, or because the implementation doesn't support
	playback)
	"""
        debug.virtual('SpokenUtterance.playback_available')
      

    def playback(self):
        """plays back recorded utterance.

	Playback is synchronous.  It will handle turning the microphone
	off and back on again (if necessary)

	**INPUTS**

	*none*

	**OUTPUTS**

	*BOOL* -- true unless playback was unavailable, or 
	there was an error in playback (e.g.  another program had 
	control of the audio device)
	"""
        debug.virtual('SpokenUtterance.playback')
      
    def can_be_adapted(self):
        """indicates whether the utterance can be corrected for adaption
	of the speech engine.  Utterances for which there was no speech
	information or for which the speech information has been lost or
	discarded may not be adaptable.

	**INPUTS**

	*none*

	**OUTPUTS**

	*BOOL* -- true if the speech information is available for adaption.
	"""
        debug.virtual('SpokenUtterance.can_be_adapted')
      
    def alternatives_available(self):
        """returns number of recognition alternatives available 
	(for the whole utterance), or -1 if the number
	is unknown.

	**INPUTS**

	*none*

	**OUTPUTS**

	*INT* -- number of recognition alternatives available (including
	the original), or -1 if the number is unknown (NaturallySpeaking
	doesn't indicate the total number, but simply lets you keep
	asking for the next one until it runs out.
	"""
        debug.virtual('SpokenUtterance.alternatives_available')

    def alternatives(self, n):
        """returns the best recognition alternatives available 
	(for the whole utterance) including the original.  
	Will not return more than n alternatives, but may return fewer
	(if the speech engine has not provided that many).

	Note: the first alternative in the list will not be identical
	to the output of words(), if the phrase has previously been
	corrected with set_words.

	**INPUTS**

	*INT* n -- number of alternatives requested

	**OUTPUTS**

	*[[(STR, STR)]]* -- list of list of words (as (spoken, written) 
	2-tuples) 
	
	"""
        debug.virtual('SpokenUtterance.words')
      
