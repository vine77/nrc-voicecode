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
import debug

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
    
#    print '-- sr_interface.connect: mic_state=%s, sr_is_connected=%s' % (mic_state, sr_is_connected)
    
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

#    print '-- sr_interface.addedByVC: flag=%s' % str(flag)
    if flag == None:
        indicator = 0
    elif (add_words_as == 'user'):
        indicator = (flag % int(0x00000010))        
    else:
        indicator = (flag / int(0x40000000))
#    print '-- sr_interfacen.addedByVC: indicator=%s' % indicator
    return indicator

def getWordInfo(word, *rest):
    
#    print '-- sr_interface.getWordInfo: word=%s, rest=%s' % (word, rest)
    
    #
    # First, fix the written form of the word
    #
    spoken, written = spoken_written_form(word)
    word = vocabulary_entry(spoken, written, clean_written=1)
#    print '-- sr_interface.getWordInfo: reformatted word=%s' % word

    answer = None
    if speech_able():
        if len(rest) == 0:
            answer = natlink.getWordInfo(word)
        elif len(rest) == 1:
            answer = natlink.getWordInfo(word, rest[0])

#    print '-- sr_interface.getWordInfo: answer is %s' % answer
    return answer


def addWord(word, *rest):
    """Add a word to NatSpeak's vocabulary.

    We only add the word if it doesn't already exist in the vocabulary
    and if speech is enabled (i.e. environment variable
    $VCODE_NOSPEECH undefined).
    """
        
    global word_info_flag

#    print '-- sr_interface.addWord: adding \'%s\'' % word
    
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
#            print '-- sr_interface.addWord: this word is new to NatSpeak'
                   
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
#                print '-- sr_interface.addWord: adding redundant form with no spaces \'%s\'' % word_no_special_chars
                natlink.addWord(word_no_special_chars, flag)

def deleteWord(word, *rest):
    """Delete a word from NatSpeak's vocabulary.

    We only delete it if speech is enabled (i.e. environment variable
    $VCODE_NOSPEECH undefined).

    Also, we only remove it if the word was added to the vocabulary by
    VoiceCode, i.e. if the word info has 'added by Vocabulary Builder'
    flag set and if the word is a phrase (single words might actually
    have ben added by the real Vocabulary Builder)"""

#    print '-- sr_interface.deleteWord: word=%s, rest=%s' % (word, rest)
    if speech_able():
        flag = getWordInfo(word, 4)
        num_words = len(re.split('\s+', word))
#        print '-- sr_interface.deleteWord: word=%s, flag=%s, num_words=%s, word_info_flag=%s' % (word, flag, num_words, word_info_flag)        
        if addedByVC(flag) and num_words > 1:
#            print '-- sr_interface.deleteWord: actually deleting word %s' % word
            sr_user_needs_saving = 1
            return natlink.deleteWord(word)
        else:
#            print '-- sr_interface.deleteWord: word not added by VoiceCode %s' % word
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

#    print '-- sr_interface.clean_written_form: written_form=\'%s\', clean_for=%s' % (written_form, clean_for)
    cleansed_form = written_form
    if clean_for == 'sr': 
        cleansed_form = re.sub('\n', '{Enter}', cleansed_form)
        cleansed_form = re.sub('\s', '{Spacebar}', cleansed_form)
        cleansed_form = re.sub('\\\\', '{Backslash}', cleansed_form)
    elif clean_for == 'vc':
        cleansed_form = re.sub('\\{Enter\\}', '\n', cleansed_form)
        cleansed_form = re.sub('\\{Spacebar\\}', ' ', cleansed_form)
        cleansed_form = re.sub('\\{Backslash\\}', '\\\\', cleansed_form)        
#    print '-- sr_interface.clean_written_form: cleansed_form=\'%s\'' % cleansed_form
    return cleansed_form
    

def clean_spoken_form(spoken_form):
    """Cleans a spoken form.
    word.
    
    **INPUTS**
    
    *STR* spoken_form -- Spoken form to be cleansed
    
     **OUTPUTS**
    
    *STR* clean_form -- The cleansed form.
    """

#    print '-- sr_interface.clean_spoken_form: spoken_form=\'%s\'' % spoken_form

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

#    print '-- sr_interface.clean_spoken_form: returning clean_form=\'%s\'' % clean_form
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
#        print '-- sr_interface.spoken_written_form: entry \'%s\' is spoken/written form' % vocabulary_entry
        
        #
        # Note: need to check for things like {Enter} in written_form
        # ignore for now
        #
        written = a_match.group(1)
        spoken = a_match.group(2)
    else:
#        print '-- sr_interface.spoken_written_form: entry \'%s\' is just spoken ' % vocabulary_entry        
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

#    print '-- sr_interface.spoken_written_form: spoken=\'%s\', written=\'%s\'' % (spoken, written)

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

#    print '-- sr_interface.vocabulary_entry: spoken_form=\'%s\', written_form=%s, clean_written=%s' % (spoken_form, repr(written_form), clean_written)

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

#    print '-- sr_interface.vocabulary_entry: returning entry=\'%s\'' % entry
    return entry

class BufferState(Object):
    """stores information about the buffer before and after the 
    most recent dictation utterance

    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**
    """
    def __init__(self):
        pass

class LastDictationUtterance(Object):
    """stores information about the most recent dictation utterance

    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, **attrs):
	self.deep_construct(LastDictationUtterance,
	    {}, attrs)

    def spoken_forms(self):
	"""returns list of spoken forms from the utterance

	**INPUTS**

	*none*

	**OUTPUTS**

	*[STR]* -- list of spoken forms from the utterance
	"""
	words = self.words()
	l = []
	for a_word in words:
	    spoken, written = spoken_written_form(a_word)
	    l.append(spoken)
	return l

    def words(self):
	"""returns list of words (in written\spoken form) from the utterance

	**INPUTS**

	*none*

	**OUTPUTS**

	*[STR]* -- list of words (in written\spoken form) from the utterance
	
	"""
	debug.virtual('LastDictationUtterance.words')
      
    def set_words(self, words):
	"""changes the stored list of words (after correction) so that 
	subsequent correction boxes can display the corrected list.
	The results object is unaffected.

	**INPUTS**

	*[STR] words* -- corrected list of words (in written\spoken form, or 
	simply spoken form)

	*none*

	**OUTPUTS**
	"""
	debug.virtual('LastDictationUtterance.set_words')
      

class LastDictNatlink(LastDictationUtterance):
    """stores information about the most recent dictation utterance

    **INSTANCE ATTRIBUTES**

    *ResObj* results -- natlink ResObj results object
    *[STR]* last_words -- corresponding list of words

    **CLASS ATTRIBUTES**
    """
    def __init__(self, results = None, **attrs):
	"""initialize LastDictNatlink 

	**INPUTS**

	*ResObj* results -- a new natlink ResObj results object
	"""
	self.deep_construct(LastDictNatlink,
	    {'results': results, 'last_words':[]}, attrs)
	if results:
	    self.last_words = results.getWords(0)

    def save(self, results):
	"""stores the new results object, replacing the old one

	**INPUTS**

	*ResObj* results -- natlink ResObj results object

	"""
	self.results = results
	if results:
	    self.last_words = results.getWords(0)

    def words(self):
	"""returns list of words (in written\spoken form) from the utterance

	**INPUTS**

	*none*

	**OUTPUTS**

	*[STR]* -- list of words (in written\spoken form) from the utterance
	
	"""
	return self.last_words

    def set_words(self, words):
	"""changes the stored list of words (after correction) so that 
	subsequent correction boxes can display the corrected list.
	The results object is unaffected.

	**INPUTS**

	*[STR] words* -- corrected list of words (in written\spoken form, or 
	simply spoken form)

	*none*

	**OUTPUTS**
	"""
	self.last_words = words
      

class CommandDictGrammar(DictGramBase):
    """A grammar for mixing continuous dictation and commands.

    This is basically a [DictGramBase] dictation grammar that forwards
    the dictation result to a command interpreter that parses it and
    executes it.
    
    **INSTANCE ATTRIBUTES**
    
    [CmdInterp] *interpreter*-- Command interpreter used to and execute the
    recognised dictation utterances.

    *INT window* -- MSW window handle of the window which must be in the
    foreground for the grammar to be activated, or 0 to make the grammar
    global

    *LastDictNatlink last* -- stores the last recognized dictation utterance 

    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, interpreter=None, window = 0, **attrs):
#          self.deep_construct(CommandDictGrammar, \
#                              {'interpreter': interpreter}, \
#                              attrs, \
#                              {DictGramBase: 1})
        self.__dict__['interpreter'] = interpreter
        DictGramBase.__init__(self)
	self.window = window
        self.state = None
        self.isActive = 0
	self.last = LastDictNatlink()

    def deactivate(self):
	DictGramBase.deactivate(self)
	self.isActive = 0

    def activate(self, window = 0, exclusive = None):
	if self.isActive:
	    return
	DictGramBase.activate(self, window = window, exclusive = exclusive)
	self.isActive = 1

    def gotBegin(self, moduleInfo):
#        print '-- CommandDictGrammar.gotBegin: called'
#	print moduleInfo
	if self.window == 0:
	    pass
#	    self.activate()
	elif self.interpreter.on_app.active_field() == None:
	    if not self.isActive:
		self.activate(window = self.window)
	else:
	    self.deactivate()
        
    def gotResultsObject(self, recog_type, results):
	if recog_type == 'self':
	    self.last.save(results)
	    words = results.getWords(0)
	    self.interpreter.interpret_NL_cmd(words)
	    self.interpreter.on_app.curr_buffer.refresh_if_necessary()
        
#    def gotResults(self, words):
        #
        # Interpret the commands, then print buffer content
        #
#        print '-- CommandDictGrammar.gotResults: Heard mixed dictation and commands:%s' % repr(words)

#        self.interpreter.interpret_NL_cmd(words)
# this is needed for the EdSim mediator simulator.  We want EdSim to
# refresh at the end of interpretation of a whole utterance, not with 
# every change to the buffer.  Other editors will usually refresh
# instantly and automatically, so their AppState/SourceBuff
# implementations can simply ignore the refresh_if_necessary message.
#        self.interpreter.on_app.curr_buffer.refresh_if_necessary()
        

class CodeSelectGrammar(SelectGramBase):
    """A grammar for selecting part of the visible code.
    
    **INSTANCE ATTRIBUTES**
    
    [CmdInterp] *interpreter=None*-- Command interpreter used to and execute the
    recognised dictation utterances.

    *INT window* -- MSW window handle of the window which must be in the
    foreground for the grammar to be activated, or 0 to make the grammar
    global

    CLASS ATTRIBUTES**
    
    *none* -- 
    """

    def __init__(self, interpreter=None, window = 0):
        DictGramBase.__init__(self)
        self.interpreter = interpreter
	self.window = window
        self.isActive = 0

    def load_with_verbs(self):
       """Load the selection grammar using specific verbs
       """
       self.load(['go', 'go after next', 'go after previous', 'go before',
                  'go before next', 'go before previous', 'go next',
                  'go previous', 'after next', 'after previous', 'before',
                  'before next', 'before previous', 'correct',
                  'correct next', 'correct previous', 'next', 'previous',
                  'select', 'select next', 'select previous', 'after'])
#       self.load(['select', 'correct'])       
       
    def deactivate(self):
	SelectGramBase.deactivate(self)
	self.isActive = 0

    def activate(self, window = 0, exclusive = None):
	if self.isActive:
	    return
	SelectGramBase.activate(self, window = window, exclusive = exclusive)
	self.isActive = 1

    def gotBegin(self, moduleInfo):
#        print '-- CodeSelectGrammar.gotBegin: called'
#	print moduleInfo
	vis_start, vis_end = self.interpreter.on_app.curr_buffer.get_visible()
	self.vis_start = vis_start
#	print vis_start, vis_end
	visible = \
	    self.interpreter.on_app.curr_buffer.get_text(vis_start, vis_end)
	self.setSelectText(visible)
#	print visible[0:50]
	if self.window == 0:
#	    self.activate()
	    self.setSelectText(visible)
	elif self.interpreter.on_app.active_field() == None:
	    self.setSelectText(visible)
	    self.activate(self.window)
	else:
	    self.deactivate()
        

# NOT NEEDED ANYMORE. gotResultsObject HANDLES THE SELECTION.
#      def gotResults(self, words, startPos, endPos):
#          print '-- CodeSelectGrammar.gotResults: Heard Select command: <%s>, startPos=%s, endPos=%s, self.ranges=%s, self.__dict__=%s' % (string.join(words), startPos, endPos, self.ranges, self.__dict__)
#          #
#          # Note: we ignore startPos and endPos because they are somewhat
#          #       randomly chosen by NatSpeak. Instead, use the first entry
#          #       in self.ranges, which was set by our own gotResultsObject
#          #       callback
#          #
#          if len(self.ranges) > 0:
#              self.interpreter.on_app.set_selection(self.ranges[0])

    def gotResultsObject(self,recogType,resObj):
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
		    true_region = (region[0] + self.vis_start,
		      region[1] + self.vis_start)
                    self.ranges.append(true_region)
                    
        except natlink.OutOfRange:
            #
            # Note: We end up here when we finished collecting selection ranges
            #       with the top score
            #
            # Sort the ranges from earliest to latest, and select the one
            # which is closest to the cursor
            #
            self.ranges.sort()
            closest_range_index = self.interpreter.on_app.curr_buffer.closest_occurence_to_cursor(self.ranges, regexp=self.selection_spoken_form(resObj), direction=direction, where=where)           

            #
            # Mark selection and/or move cursor  to the appropriate end of
            # the selection.
            #
            if mark_selection:
                actions_gen.ActionSelect(range=self.ranges[closest_range_index], cursor_at=where).log_execute(self.interpreter.on_app, None)
#                self.interpreter.on_app.curr_buffer.set_selection(self.ranges[closest_range_index], cursor_at=where)
            else:
                if where > 0:
                    pos = self.ranges[closest_range_index][1]
                else:
                    pos = self.ranges[closest_range_index][0]
                self.interpreter.on_app.curr_buffer.goto(pos)

# this is needed for the EdSim mediator simulator.  We want EdSim to
# refresh at the end of interpretation of a whole utterance, not with 
# every change to the buffer.  Other editors will usually refresh
# instantly and automatically, so their AppState/SourceBuff
# implementations can simply ignore the refresh_if_necessary message.
            self.interpreter.on_app.curr_buffer.refresh_if_necessary()

            #
            # Log the selected occurence so that if the user repeats the
            # same Select Pseudocode operation we don't end up selecting
            # the same occurence again
            #
            self.interpreter.on_app.curr_buffer.log_search(regexp=self.selection_spoken_form(resObj), direction=direction, where=where, match=self.ranges[closest_range_index])

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

#        print '-- CodeSelectGrammar.selection_spoken_form: returning spoken_form=%s' % spoken_form
        
        return spoken_form