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
# (C)2000, National Research Council of Canada
#
##############################################################################

"""Interface to the Speech Recognition engine.
"""

import re
import natlink
from natlinkutils import *
import actions_gen, CmdInterp
from Object import Object
from debug import trace

import SpokenUtterance

#import nsformat

#
# Flag that remembers whether or not we have connected to NatSpeak
#
sr_is_connected = 0

#
# microphone state change callback (None for no callback
#
#    *FCT* mic_change_callback -- 
#      mic_change_callback(*STR* mic_state)
#    (optional) function to be called when the microphone state changes.

sr_mic_change_callback = None

#
# Flag that remembers whether or not the VoiceCode SR user was modified since
# last saved
#
sr_user_needs_saving = 0

#
# Name, base model and base topic to use for VoiceCode
#
vc_user_name = 'VoiceCode'
vc_base_model = 'BestMatch Model'
vc_base_topic = 'US General English - BestMatch Plus'


#
# Flag used to add a word to NatSpeak
# 0x40000000 -> added by VoiceCode (i.e. alias Vocabulary Builder)
# 0x00000001 -> added by user
#
#
# Words added by VoiceCode to NatSpeak's vocabulary can be added either
# as 'user' or as 'vocabulary builder'.
#
# If added as 'user', then the a-priori probabibility of the words is very
# high which may improve accuracy for coding, but decrease accuracy for
# regular dictation. Also, words added by VoiceCode are indistinguishable from
# words added by the user.
#
# If added as 'vocabulary builder', a-priori probability of the words is
# low, which decreases accuracy for programming, but doesn't affect accuracy
# of regular dictation. However, this makes the symbols distinguishable from
# user added symbols (but not distinguishable from vocabulary builder added
# symbol, but that doesn't matter because we only remove multi word vocabulary
# entries, and vocabulary builder entries are all single words.
#
add_words_as = 'user'
if add_words_as == 'user':
    word_info_flag = 0x00000001
else:
    word_info_flag = 0x40000000

#
# The following functions are just wrappers on top of natlink ones.
# They check for value of environment variable *VCODE_NOSPEECH* before
# calling the corresponding natlink functions
#

def speech_able():
    return not os.environ.has_key('VCODE_NOSPEECH')


def set_mic(mic_state):
    """turns microphone on or off (connecting first, if necessary).

    *STR* mic_state -- *'on'* or *'off'*. State to put the mic in
    after connection.
    """
    if speech_able():
        if not sr_is_connected:
	    connect()
	natlink.setMicState(mic_state)

def connect(mic_state=None, mic_change_callback = None):
    """Connects to the SR system.
    
    **INPUTS**
    
    *STR* mic_state -- *'on'* or *'off'*. State to put the mic in
    after connection. If *None*, then leave mic alone.
    
    *FCT* mic_change_callback -- 
      mic_change_callback(*STR* mic_state)
    (optional) function to be called when the microphone state changes.
    
    **OUTPUTS**
    
    *none* -- 
    """
    global sr_is_connected, vc_user_name, vc_base_model, vc_base_topic
    global sr_mic_change_callback
    
#    trace('sr_interface.connect', 'mic_state=%s, sr_is_connected=%s' % (mic_state, sr_is_connected))
    
    if speech_able():
        if not sr_is_connected:
# 1 means use threads -- needed for GUI apps
            natlink.natConnect(1)
            sr_is_connected = 1            
            openUser(vc_user_name, 0, vc_base_model, vc_base_topic)
        if mic_state:
            natlink.setMicState(mic_state)
	if mic_change_callback:
	    sr_mic_change_callback = mic_change_callback
	    natlink.setChangeCallback(change_callback)


def disconnect():
    """Dicsconnects from SR system.
    
    **INPUTS**
    
    *none* -- 
    
    
    **OUTPUTS**
    
    *none* -- 
    """
    global sr_is_connected, sr_mic_change_callback

    if speech_able() and sr_is_connected:
	if sr_mic_change_callback:
	    natlink.setChangeCallback(None)
	    sr_mic_change_callback = None
        natlink.natDisconnect()
    sr_is_connected = 0        


def change_callback(*args):
    if args[0] == 'mic' and sr_mic_change_callback:
	sr_mic_change_callback(args[1])


def openUser(user_name, create_if_not_exist=0, create_using_model=None, create_using_topic=None):

    """Open a user, maybe create it if it doesn't exist.
        
    **INPUTS**
        
    *STR* user_name -- Name of the user to be opened.

    *BOOL* create_if_not_exist -- If *true* then the user will be
     created if it doesn't exist.
        
    *STR* create_using_model=None -- User model to use for creation of
     the user (if *create_if_not_exist* is *true*).

    *STR* create_using_topic=None -- Topic to use for creation of
     the user (if *create_if_not_exist* is *true*)
        

    **OUTPUTS**
        
    *none* -- 
    """
    
    try:
        natlink.openUser(user_name)
    except natlink.UnknownName, exc:
        if create_if_not_exist:
            natlink.createUser(user_name, create_using_model, create_using_topic)
        else:
            #
            # Reraise the exception so it can be caught further up the call chain
            #
            raise exc

def saveUser():
    """Saves the current user"""
    natlink.saveUser()
    sr_user_needs_saving = 0

def addedByVC(flag):   
    """Returns *true* iif word information *flag* indicates that word
    was added by VoiceCode"""

#    trace('sr_interface.addedByVC', 'flag=%s' % str(flag))
    if flag == None:
        indicator = 0
    elif (add_words_as == 'user'):
        indicator = (flag % int(0x00000010))        
    else:
        indicator = (flag / int(0x40000000))
#    trace('sr_interfacen.addedByVC', 'indicator=%s' % indicator)
    return indicator

def getWordInfo(word, *rest):
    
#    trace('sr_interface.getWordInfo', 'word=%s, rest=%s' % (word, rest))
    
    #
    # First, fix the written form of the word
    #
    spoken, written = spoken_written_form(word)
    word = vocabulary_entry(spoken, written, clean_written=1)
#    trace('sr_interface.getWordInfo', 'reformatted word=%s' % word)

    answer = None
    if speech_able():
        if len(rest) == 0:
            answer = natlink.getWordInfo(word)
        elif len(rest) == 1:
            answer = natlink.getWordInfo(word, rest[0])

#    trace('sr_interface.getWordInfo', 'answer is %s' % answer)
    return answer


def addWord(word, *rest):
    """Add a word to NatSpeak's vocabulary.

    We only add the word if it doesn't already exist in the vocabulary
    and if speech is enabled (i.e. environment variable
    $VCODE_NOSPEECH undefined).
    """
        
    global word_info_flag

#    trace('sr_interface.addWord', 'adding \'%s\'' % word)
    
    #
    # First, fix the written form of the word
    #
    spoken, written = spoken_written_form(word)
    word = vocabulary_entry(spoken, written, clean_written=1)


    if speech_able():
        #
        # Make sure we are connected to SR system
        #
        connect()
                
        if getWordInfo(word) == None:
#            trace('sr_interface.addWord', 'this word is new to NatSpeak')
                   
            if len(rest) == 0:
                flag = word_info_flag
            elif len(rest) == 1:
                flag = rest[0]
            else:
                return None
                
            natlink.addWord(word, flag)
            sr_user_needs_saving = 1

            #
            # Note: Need to add redundant entry without special
            # characters (e.g. {Spacebar}}) in the written form,
            # because Select XYZ will not work if XYZ has some spaces
            # in its written form. This means that there will be two
            # vocabulary entries in the vocabulary. The entry without
            # spaces will always be used by Select XYZ, but
            # unfortunately, the dictation grammar may chose the one
            # without spaces over the one with spaces. Hopefully,
            # user correction will address that
            #
            word_no_special_chars = re.sub('{Spacebar}', '', word)
            if word_no_special_chars != word:
#                trace('sr_interface.addWord', 'adding redundant form with no spaces \'%s\'' % word_no_special_chars)
                natlink.addWord(word_no_special_chars, flag)

def deleteWord(word, *rest):
    """Delete a word from NatSpeak's vocabulary.

    We only delete it if speech is enabled (i.e. environment variable
    $VCODE_NOSPEECH undefined).

    Also, we only remove it if the word was added to the vocabulary by
    VoiceCode, i.e. if the word info has 'added by Vocabulary Builder'
    flag set and if the word is a phrase (single words might actually
    have ben added by the real Vocabulary Builder)"""

#    trace('sr_interface.deleteWord', 'word=%s, rest=%s' % (word, rest))
    if speech_able():
        flag = getWordInfo(word, 4)
        num_words = len(re.split('\s+', word))
        if addedByVC(flag) and num_words > 1:
#            trace('sr_interface.deleteWord', 'actually deleting word %s' % word)
            sr_user_needs_saving = 1
            return natlink.deleteWord(word)
        else:
#            trace('sr_interface.deleteWord', 'word not added by VoiceCode %s' % word)
            return None

def clean_written_form(written_form, clean_for=None):
    """Substitutes special charactes like newline and space in written form
    of a word.

    **INPUTS**

    *STR written_form* -- Written form to be cleaned.

    *STR clean_for* -- If 'sr', substitute the character to the form
     expected by the SR (e.g. ' ' -> {Spacebar}). If 'vc', substitute
     to the form expected by VoiceCode (e.g. '{Spacebar}' -> ' '). If
     neither of those, leave the form alone.

    **OUTPUT**

    *STR cleansed_form* -- The clean written form
    """

#    trace('sr_interface.clean_written_form', 'written_form=\'%s\', clean_for=%s' % (written_form, clean_for))
    cleansed_form = written_form
    if clean_for == 'sr': 
        cleansed_form = re.sub('\n', '{Enter}', cleansed_form)
        cleansed_form = re.sub('\s', '{Spacebar}', cleansed_form)
        cleansed_form = re.sub('\\\\', '{Backslash}', cleansed_form)
    elif clean_for == 'vc':
        cleansed_form = re.sub('\\{Enter\\}', '\n', cleansed_form)
        cleansed_form = re.sub('\\{Spacebar\\}', ' ', cleansed_form)
        cleansed_form = re.sub('\\{Backslash\\}', '\\\\', cleansed_form)        
#    trace('sr_interface.clean_written_form', 'cleansed_form=\'%s\'' % cleansed_form)
    return cleansed_form
    

def clean_spoken_form(spoken_form):
    """Cleans a spoken form.
    word.
    
    **INPUTS**
    
    *STR* spoken_form -- Spoken form to be cleansed
    
     **OUTPUTS**
    
    *STR* clean_form -- The cleansed form.
    """

#    trace('sr_interface.clean_spoken_form', 'spoken_form=\'%s\'' % spoken_form)

    clean_form = spoken_form

    # AD
    # Note: if spoken form is 'X.' where X is some capital letter, then leave
    # spoken form alone. Otherwise
    #   say(['O.'])
    # ends up calling
    #   recognitionMimic(['O.\\o'])
    #
    if not re.match('[A-Z].$', clean_form):

        #
        # Lower case
        #
        clean_form = string.lower(clean_form)

        #
        # Replace non alphanumericals by spaces.
        # 
        clean_form = re.sub('[^a-z0-9]+', ' ', clean_form)    
         
        #
        # Remove leading, trailing and multiple blanks
        #
        clean_form = re.sub('\s+', ' ', clean_form)
        clean_form = re.sub('^\s+', '', clean_form)
        clean_form = re.sub('\s+$', '', clean_form)

#    trace('sr_interface.clean_spoken_form', 'returning clean_form=\'%s\'' % clean_form)
    return clean_form


def spoken_written_form(vocabulary_entry):
    """Returns the written and spoken forms of a NatSpeak vocabulary entry
    
    **INPUTS**
    
    *STR* vocabulary_entry -- the vocabulary entry in either
    written or written\\spoken form.
    
    **OUTPUTS**
    
    *STR* (spoken, written) -- written and spoken forms of the vocabulary entry.
    """
    a_match = re.match('^([\s\S]*)\\\\([^\\\\]*)$', vocabulary_entry)
    if a_match:
#        trace('sr_interface.spoken_written_form', 'entry \'%s\' is spoken/written form' % vocabulary_entry)
        
        #
        # Note: need to check for things like {Enter} in written_form
        # ignore for now
        #
        written = a_match.group(1)
        spoken = a_match.group(2)
    else:
#        trace('sr_interface.spoken_written_form', 'entry \'%s\' is just spoken ' % vocabulary_entry        )
        written = vocabulary_entry
        spoken = vocabulary_entry

    #
    # Substitute special characters in written form (e.g. ' ', '\n') to the
    # form that the SR expects (e.g. {Spacebar}, {Enter})
    #
    written = clean_written_form(written, clean_for='vc')

    #
    # Clean spoken form
    #
    spoken = clean_spoken_form(spoken)

#    trace('sr_interface.spoken_written_form', 'spoken=\'%s\', written=\'%s\'' % (spoken, written))

    return (spoken, written)
    

def vocabulary_entry(spoken_form, written_form, clean_written=1):
    """Creates a vocabulary entry with given spoken and written forms.

    **INPUTS**

    *STR* spoken_form -- the spoken form 

    *STR* *written_form -- the written form (default to *spoken_form*)
    
    *BOOL* clean_written -- If true, substitute special characters in
     written form (e.g. '\n' -> '{Enter}')

    **OUTPUTS**

    *entry* -- the entry to be added to the SR vocabulary
    """

#    trace('sr_interface.vocabulary_entry', 'spoken_form=\'%s\', written_form=%s, clean_written=%s' % (spoken_form, repr(written_form), clean_written))

    spoken_form = clean_spoken_form(spoken_form)
    entry = spoken_form
    if spoken_form != written_form:
        #
        # Substitute special characters in written form (e.g. {Spacebar},
        # {Enter}) to the form used in VoiceCode (e.g. ' ', '\n')
        #
        if clean_written:
            written_form = clean_written_form(written_form, clean_for='sr')

        if len(written_form) > 0:
            entry = written_form + '\\' + entry

#    trace('sr_interface.vocabulary_entry', 'returning entry=\'%s\'' % entry)
    return entry

class SpokenUtteranceNL(SpokenUtterance.SpokenUtterance):
    """implementation of SpokenUtterance using natlink ResObj.
    Defines an interface for manipulating the speech
    information associated with a single user utterance

    **INSTANCE ATTRIBUTES**

    *ResObj* results -- natlink results object representing speech
    information
    *[(STR, STR)]* word_list -- list of spoken, written forms,
    either originally recognized or corrected with set_words
    *[STR]* spoken_only -- list of spoken forms,
    either originally recognized or corrected with set_words
    *[[(STR, STR))]* choices -- list of alternative choices retrieved
    from ResObj (ResObj may have more choices than this - see
    alternatives method)
    *INT* choices_available -- number of alternative choices available
    or -1 if unknown    

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, results, **attrs):
	"""creates a SpokenUtteranceNL from a results object

	**INPUTS**

	*ResObj* results -- natlink results object representing speech
	information

	**OUTPUTS**

	*none*
	"""
	# local variables needed for initialization in deep_construct
	raw_words = results.getWords(0)
	word_list = map(spoken_written_form, raw_words)
	spoken_only = map(lambda x: x[0], word_list)
      
	self.deep_construct(SpokenUtteranceNL,
	    {'results' : results, 
	    'word_list': word_list,
	    'spoken_only': spoken_only,
	    'choices_available': -1,
	    'choices': []}, 
	    attrs)

    def spoken_forms(self):
	"""returns list of spoken forms from the utterance

	**INPUTS**

	*none*

	**OUTPUTS**

	*[STR]* -- list of spoken forms from the utterance
	"""
	return self.spoken_only

    def words(self):
	"""returns list of words (as (spoken, written) 2-tuples) 
	from the utterance.

	**INPUTS**

	*none*

	**OUTPUTS**

	*[(STR, STR)]* -- list of words (as (spoken, written) 2-tuples) 
	
	"""
	return self.word_list

    def entry(self, spoken, written = None):
	"""returns a vocabulary entry in the form used by
	NaturallySpeaking/natlink.  If the written form is omitted, then it is
	assumed to be identical to the spoken form.

	**INPUTS**

	*STR* spoken -- spoken form
	*STR* written -- written form (if different)

	**OUTPUTS**

	*STR* -- vocabulary entry in written\spoken form as used by
	NaturallySpeaking
	"""
	if  written == None:
	    written = spoken
	return vocabulary_entry(spoken, written) 

    def entry_tuple(self, word):
	"""returns a vocabulary entry in the form used by
	NaturallySpeaking/natlink.  

	**INPUTS**

	*(STR, STR)* word -- word (as (spoken, written) 2-tuples) 

	**OUTPUTS**

	*STR* -- vocabulary entry in written\spoken form as used by
	NaturallySpeaking
	"""
	return vocabulary_entry(word[0], word[1])

    def same_written(self, spoken_forms):
	"""converts a list of spoken forms to a list of (spoken, written) 
	2-tuples.

	**INPUTS**

	*[STR]* spoken_forms -- list of spoken forms 
	(written forms will be assumed to be identical)
	
	**OUTPUTS**

	*[(STR, STR)]* -- list of words (as (spoken, written) 2-tuples) 
	"""
	return map(lambda s: (s, s), spoken_forms)

    def entries_spoken( self, spoken_forms):
	"""converts a list of spoken forms to a list of vocabulary entries
	in the form used by NaturallySpeaking/natlink.

	**INPUTS**

	*[STR]* spoken_forms -- list of spoken forms 
	(written forms will be assumed to be identical)

	**OUTPUTS**

	*[STR]* -- list of vocabulary entries in written\spoken form as used by
	NaturallySpeaking

	"""
	return map(self.entry, spoken_forms)

    def spoken_written_form(self, entry):
	"""converts a vocabulary entry in the form used by 
	NaturallySpeaking/natlink to a 2-tuple of spoken, written.

	**INPUTS**

	*STR* -- vocabulary entry in written\spoken form as used by
	NaturallySpeaking

	**OUTPUTS**

	*(STR, STR)* word -- word (as (spoken, written) 2-tuples) 

	*[STR]* spoken_forms -- list of spoken forms 
	(written forms will be assumed to be identical)

	"""
	return spoken_written_form(entry)

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
	list = entries(words)
	success = 0
	try:
	    success = self.results.correction(list)
	except natlink.InvalidWord:
# if the ResObj raises an InvalidWord exception, do not set the 
#	 word list
	    return 0
	set_words(words)
	return success

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
	words = self.same_written(spoken_forms)
	return self.adapt(words)

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
	self.word_list = words
	self.spoken_only = map(lambda x: x[0], word_list)

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
	words = self.same_written(spoken_forms)
	self.set_words(words)

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
	return 0
# ResObj may have wave data, but we don't have code to play it back yet

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
	return 0
# ResObj may have wave data, but we don't have code to play it back yet
      
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
	return 1
      
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
	return self.choices_available

    def _get_alternative(self, choice):
	"""private method for getting a single alternative and converting it to
	list of 2-tuples.
	**INPUTS**

	*INT* choice -- number of the choice to request

	**OUTPUTS**

	*[(STR, STR)]* -- list of words (as (spoken, written) 
	2-tuples) corresponding to that alternative, or None if choice
	was unavailable
	"""
	try:
	    list = self.results.getWords(choice)
	except natlink.OutOfRange:
	    return None
	return map(self.spoken_written_form, list)

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
	if n <= len(self.choices):
	    return self.choices[0:n-1]
	if self.choices_available >= 0:
	    return self.choices
# if number of choices available is known, then we already have all
# available choices, so just return what we have.
# otherwise, try to get more choices
	for choice in range(len(self.choices), n):
	    words = self._get_alternative(choice)
	    if words == None:
# no more available, so now we know how many are available
		self.choices_available = choice
		break
	    self.choices.append(words)
# return what we have.
	return self.choices

class CommandDictGrammar(DictGramBase):
    """A grammar for mixing continuous dictation and commands.

    This is basically a [DictGramBase] dictation grammar that forwards
    the dictation result to a command interpreter that parses it and
    executes it.
    
    **INSTANCE ATTRIBUTES**

    [AppState] *app* -- interface to the editor application
    
    [CmdInterp] *interpreter*-- Command interpreter used to and execute the
    recognised dictation utterances.

    *INT window = 0* -- MSW window handle of the window which must be in the
    foreground for the grammar to be activated, or 0 to make the grammar
    global

    *0-1 exclusive = 0* -- Indicates whether the grammar is activated as an
    exclusive (1) or non-exclusive grammar (0)

    *0-1 allResults = 0* -- Indicates if the grammar should be loaded so as
    to get all results (even those intercepted by other grammars)

    *SpokenUtterance last* -- stores the last recognized dictation utterance

    BOOL *dictation_allowed* -- *true* iif editor allows dictation in
    current buffer.

    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, app = None, interpreter=None, window = 0, exclusive = 0,
                 allResults = 0, **attrs):
        self.__dict__['app'] = app
        self.__dict__['interpreter'] = interpreter
        DictGramBase.__init__(self)
	self.window = window
        self.exclusive = exclusive
        self.allResults = allResults
        self.state = None
        self.isActive = 0
	self.last = None
        self.dictation_allowed = None

    def cleanup(self):
        del self.app
	del self.interpreter

    def deactivate(self):
#        trace('sr_interface.CommandDictGramm.deactivate', 'called')
	DictGramBase.deactivate(self)
	self.isActive = 0

    def activate(self):
	if self.isActive:
#            trace('sr_interface.CommandDictGramm.activate', 'already active')
	    return
#        trace('sr_interface.CommandDictGramm.activate', 'activating grammar')
	DictGramBase.activate(self, window = self.window, exclusive = self.exclusive)
	self.isActive = 1

    def gotBegin(self, moduleInfo):
        trace('sr_interface.CommandDictGrammar.gotBegin', 
              'invoked: self.window=%s, self.isActive=%s, self.exclusive=%s, self.allResults=%s, self.app.active_field()=%s, moduleInfo=%s' % (self.window, self.isActive, self.exclusive, self.allResults, self.app.active_field(), moduleInfo))

        #
        # Tell the external editor which window was active when utterance
        # started (Emacs for one needs to know that for some reason I don't
        # clearly understand).
        #
        # Check if Editor currently allows user to dictate in that window.
        #
        self.dictation_allowed = self.app.recog_begin(moduleInfo[2])
        
	if self.window == 0:
	    pass
            trace('sr_interface.CommandDictGrammar.gotBegin', 'this is a global grammar. Just pass')
	elif (self.app.active_field() == None and
              self.dictation_allowed):
            trace('sr_interface.CommandDictGrammar.gotBegin', 'I think this is supposed to be called only when editor window is active.')
	    if not self.isActive:
                trace('sr_interface.CommandDictGrammar.gotBegin', 'grammar not active. Activating it.'                )
		self.activate()
	else:
            trace('sr_interface.CommandDictGrammar.gotBegin', 'Local grammar but the editor doesn\'t have focus. Deactivate the grammar')
	    self.deactivate()

        
    def gotResultsObject(self, recogType, results):
        trace('sr_interface.CommandDictGramm.gotResultsObject', 'recogType=%s' % recogType)
        trace('sr_interface.CommandDictGramm.gotResultsObject', 'self.app=%s, self.dictation_allowed=%s' % (self.app, self.dictation_allowed))

        if self.dictation_allowed:        
            #
            # In regression testing mode (self.allResults = 1), we process all
            # all utterances even if they were intercepted by an other dictation
            # grammar.
            #
            # This allows user to work in other applications (by keyboard only)
            # while regression test is running
            #

            if recogType == 'other':
                #
                # First check if this result was generated by a selection grammar
                # (in which case, ignore it).
                #
                try:
                    trace('sr_interface.CommandDictGramm.gotResultsObject', 'checking if select grammar result')
                    results.getSelectInfo(self.gramObj, 0)
                    # If no exception is generated, then results was generated
                    # by a selection grammar. So skip it.
                    trace('sr_interface.CommandDictGramm.gotResultsObject', 'this result generated by a selection grammar. Skipping it')
                    return
                except natlink.BadGrammar:
                    trace('sr_interface.CommandDictGramm.gotResultsObject', 'this result NOT generated by a selection grammar. Processing it')
                    # If exception is generated, then results was NOT generated
                    # by a selection grammar. So keep processing it.
                    pass

            if recogType == 'self' or (recogType == 'other' and self.allResults):
                self.last = SpokenUtteranceNL(results)
                words = results.getWords(0)
                self.interpreter.interpret_NL_cmd(words, self.app)
                self.app.curr_buffer().print_buff_if_necessary()

#        trace('sr_interface.CommandDictGramm.gotResults', 'exited')
        

class CodeSelectGrammar(SelectGramBase):
    """A grammar for selecting part of the visible code.
    
    **INSTANCE ATTRIBUTES**

    [AppState] *app* -- interface to the editor application
    
    *INT window* -- MSW window handle of the window which must be in the
    foreground for the grammar to be activated, or 0 to make the grammar
    global

    *0-1 exclusive=0* -- Indicates whether the grammar should be activated as
    an exclusive (1) or non-exclusive (1) grammar

    *0-1 allResults = 0* -- Indicates if the grammar should be loaded so as
    to get all results (even those intercepted by other grammars)    
    
    CLASS ATTRIBUTES**
    
    *none* -- 
    """

    def __init__(self, app = None, window = 0, exclusive = 0,
                 allResults = 0):
        DictGramBase.__init__(self)
	self.app = app
	self.window = window
        self.exclusive = exclusive
        self.allResults = allResults
        self.isActive = 0

    def cleanup(self):
        del self.app

    def load_with_verbs(self):
       """Load the selection grammar using specific verbs
       """
       self.load(['go', 'go after next', 'go after previous', 'go before',
                  'go before next', 'go before previous', 'go next',
                  'go previous', 'after next', 'after previous', 'before',
                  'before next', 'before previous', 'correct',
                  'correct next', 'correct previous', 'next', 'previous',
                  'select', 'select next', 'select previous', 'after'], allResults=self.allResults)
       
    def deactivate(self):
	SelectGramBase.deactivate(self)
	self.isActive = 0

    def activate(self):
	if self.isActive:
	    return
	SelectGramBase.activate(self, window = self.window, exclusive = self.exclusive)
	self.isActive = 1

    def gotBegin(self, moduleInfo):
        trace('sr_interface.CodeSelectGrammar.gotBegin',
              'called,self.app=%s, self.app.curr_buffer()=%s' % (self.app, self.app.curr_buffer()))

	vis_start, vis_end = self.app.get_visible()
	self.vis_start = vis_start
	visible = \
	    self.app.curr_buffer().get_text(vis_start, vis_end)
        trace('sr_interface.CodeSelectGrammar.gotBegin',
              '** vis_start=%s, vis_end=%s, visible="%s"' %
              (vis_start, vis_end, visible))
#        trace('sr_interface.CodeSelectGrammar.gotBegin',
#              '** self.app.get_text()="%s", self.app.curr_buffer()._get_text_from_app()="%s"' %
#              (self.app.get_text(), self.app.curr_buffer()._get_text_from_app()))
        
        
	self.setSelectText(visible)
	if self.window == 0:
	    self.activate()
	    self.setSelectText(visible)
	elif self.app.active_field() == None:
	    self.setSelectText(visible)
	    self.activate()
	else:
	    self.deactivate()
        

    def gotResultsObject(self,recogType,resObj):
        trace('sr_interface.CodeSelectGrammar.gotResultsObject',
              'called, recogType=\'%s\'' % recogType)

        #
        # In regression testing mode (self.allResults = 1), we process all
        # all select utterances even if they were intercepted by an other
        # selection grammar.
        #
        # This allows user to work in other applications (by keyboard only)
        # while regression test is running
        #
        
        if recogType == 'other':
            #
            # *resObj* was generated by an other grammar. Make sure
            # it was generated by a selection grammar
            #
            try:
                resObj.getSelectInfo(self.gramObj, 0)
            except natlink.BadGrammar:
                return
        
        if recogType == 'self' or (recogType == 'other' and self.allResults):
            trace('sr_interface.CodeSelectGrammar.gotResultsObject',
                  '** collecting the possible regions')
            
            # If there are multiple matches in the text we need to scan through
            # the list of choices to find every entry which has the highest.
            self.ranges = []        
            try:
                bestScore = resObj.getWordInfo(0)[0][2]
                verb = resObj.getWordInfo(0)[0][0]

                #
                # Analyse the verb used by the user in the Select utterance
                #
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
                # Collect selection ranges with highest score
                #
                for i in range(100):
                    trace('sr_interface.CodeSelectGrammar.gotResultsObject',
                          '** i=%s' % i)
                    
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
                        # first ones. Raise OutOfRange exception to exit the
                        # loop (sorry about that ;-)
                        #
                        raise natlink.OutOfRange
                    else:
                        #
                        # This region has the same score as the first ones. Add it
                        # to the candidate selection ranges.
                        #
                        region = resObj.getSelectInfo(self.gramObj, i)

#                        trace('sr_interface.CodeSelectGrammar.gotResultsObject', 'region=%s, self.vis_start=%s' % (repr(region), self.vis_start))
                        
                        true_region = (region[0] + self.vis_start,
                          region[1] + self.vis_start)
                        self.ranges.append(true_region)

            except natlink.OutOfRange:
                trace('sr_interface.CodeSelectGrammar.gotResultsObject',
                      '** got the last region, self.ranges=%s' % self.ranges)
                
                #
                # Note: We end up here when we finished collecting selection ranges
                #       with the top score
                #
                # Sort the ranges from earliest to latest, and select the one
                # which is closest to the cursor
                #
                self.ranges.sort()
                trace('sr_interface.CodeSelectGrammar.gotResultsObject',
                      '** invoking closest_occurence_to_cursor')
                
                closest_range_index = self.app.curr_buffer().closest_occurence_to_cursor(self.ranges, regexp=self.selection_spoken_form(resObj), direction=direction, where=where)

                trace('sr_interface.CodeSelectGrammar.gotResultsObject',
                      '** DONE with closest_occurence_to_cursor')

                #
                # Mark selection and/or move cursor  to the appropriate end of
                # the selection.
                #
                trace('sr_interface.CodeSelectGrammar.gotResultsObject',
                      '** mark_selection=%s' % mark_selection)
                
                if mark_selection:
                    trace('sr_interface.CodeSelectGrammar.gotResultsObject',
                          '** invoking ActionSelect(...).log_execute(...)')
                    
                    actions_gen.ActionSelect(range=self.ranges[closest_range_index], cursor_at=where).log_execute(self.app, None)
                    trace('sr_interface.CodeSelectGrammar.gotResultsObject',
                          '** DONE invoking ActionSelect(...).log_execute(...)')
                    
                else:
                    if where > 0:
                        pos = self.ranges[closest_range_index][1]
                    else:
                        pos = self.ranges[closest_range_index][0]
                    trace('sr_interface.CodeSelectGrammar.gotResultsObject',
                          '** going to pos=%s' % pos)
                        
                    self.app.curr_buffer().goto(pos)
                    trace('sr_interface.CodeSelectGrammar.gotResultsObject',
                          '** DONE going to pos=%s' % pos)
                    

# this is needed for the EdSim mediator simulator.  We want EdSim to
# refresh at the end of interpretation of a whole utterance, not with 
# every change to the buffer.  Other editors will usually refresh
# instantly and automatically, so their AppState/SourceBuff
# implementations can simply ignore the print_buff_if_necessary message.

                trace('sr_interface.CodeSelectGrammar.gotResultsObject',
                      '** invoking print_buff_if_necessary')

                self.app.curr_buffer().print_buff_if_necessary()
                
                trace('sr_interface.CodeSelectGrammar.gotResultsObject',
                      '** DONE invoking print_buff_if_necessary')


                #
                # Log the selected occurence so that if the user repeats the
                # same Select Pseudocode operation we don't end up selecting
                # the same occurence again
                #
                trace('sr_interface.CodeSelectGrammar.gotResultsObject',
                      '** invoking log_search')
                
                self.app.curr_buffer().log_search(regexp=self.selection_spoken_form(resObj), direction=direction, where=where, match=self.ranges[closest_range_index])

                trace('sr_interface.CodeSelectGrammar.gotResultsObject',
                      '** DONE invoking log_search')

        trace('sr_interface.CodeSelectGrammar.gotResultsObject', 'exited')


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
            a_spoken_word, dummy = spoken_written_form(a_word_info[0])
            if spoken_form != '':
                spoken_form = spoken_form + ' '
            spoken_form = spoken_form + a_spoken_word

#        trace('sr_interface.CodeSelectGrammar.selection_spoken_form', 'returning spoken_form=%s' % spoken_form)
        
        return spoken_form
