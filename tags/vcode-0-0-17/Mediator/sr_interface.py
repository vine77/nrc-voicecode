"""Interface to the Speech Recognition engine.
"""

import re
import natlink
from natlinkutils import *
import CmdInterp
#import nsformat

#
# Flag that remembers whether or not we have connected to NatSpeak
#
sr_is_connected = 0

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


def connect(mic_state=None):
    """Connects to the SR system.
    
    **INPUTS**
    
    *STR* mic_state -- *'on'* or *'off'*. State to put the mic in
    after connection. If *None*, then leave mic alone.
    
    
    **OUTPUTS**
    
    *none* -- 
    """
    global sr_is_connected, vc_user_name, vc_base_model, vc_base_topic
    
#    print '-- sr_interface.connect: mic_state=%s, sr_is_connected=%s' % (mic_state, sr_is_connected)
    
    if speech_able():
        if not sr_is_connected:
            natlink.natConnect()
            sr_is_connected = 1            
            openUser(vc_user_name, 0, vc_base_model, vc_base_topic)
        if mic_state:
            natlink.setMicState(mic_state)

def disconnect():
    """Dicsconnects from SR system.
    
    **INPUTS**
    
    *none* -- 
    
    
    **OUTPUTS**
    
    *none* -- 
    """
    global sr_is_connected

    if speech_able() and sr_is_connected:
        natlink.natDisconnect()
    sr_is_connected = 0        

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
#    written = re.sub('\\{Enter\\}', '\n', written)
#    written = re.sub('\\{Spacebar\\}', ' ', written)

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

class CommandDictGrammar(DictGramBase):
    """A grammar for mixing continuous dictation and commands.

    This is basically a [DictGramBase] dictation grammar that forwards
    the dictation result to a command interpreter that parses it and
    executes it.
    
    **INSTANCE ATTRIBUTES**
    
    [CmdInterp] *interpreter*-- Command interpreter used to and execute the
    recognised dictation utterances.

    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, interpreter=None, **attrs):
#          self.deep_construct(CommandDictGrammar, \
#                              {'interpreter': interpreter}, \
#                              attrs, \
#                              {DictGramBase: 1})
        self.__dict__['interpreter'] = interpreter
        DictGramBase.__init__(self)
        self.state = None
        self.isActive = 0

    def gotBegin(self, moduleInfo):
#        print '-- CommandDictGrammar.gotBegin: called'
        pass
        
    def gotResults(self, words):
        #
        # Interpret the commands, then print buffer content
        #
#        print '-- CommandDictGrammar.gotResults: Heard mixed dictation and commands:%s' % repr(words)

        self.interpreter.interpret_NL_cmd(words)
# this is needed for the EdSim mediator simulator.  We want EdSim to
# refresh at the end of interpretation of a whole utterance, not with 
# every change to the buffer.  Other editors will usually refresh
# instantly and automatically, so their AppState/SourceBuff
# implementations can simply ignore the refresh_if_necessary message.
        self.interpreter.on_app.curr_buffer.refresh_if_necessary()
        

class CodeSelectGrammar(SelectGramBase):
    """A grammar for selecting part of the visible code.
    
    **INSTANCE ATTRIBUTES**
    
    [CmdInterp] *interpreter=None*-- Command interpreter used to and execute the
    recognised dictation utterances.

    CLASS ATTRIBUTES**
    
    *none* -- 
    """

    def __init__(self, interpreter=None):
        DictGramBase.__init__(self)
        self.interpreter = interpreter
        self.isActive = 0

    def load_with_verbs(self):
       """Load the selection grammar using specific verbs
       """
       self.load(['go', 'go after next', 'go after previous', 'go before',
                  'go before next', 'go before previous', 'go next',
                  'go previous', 'after next', 'after previous', 'before',
                  'before next', 'before previous', 'correct',
                  'correct next', 'correct previous', 'next', 'previous',
                  'select', 'select next', 'select previous'])
#       self.load(['select', 'correct'])       
       

    def gotBegin(self, moduleInfo):
#        print '-- CodeSelectGrammar.gotBegin: called'
        self.setSelectText(self.interpreter.on_app.curr_buffer.contents())

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

#            print '--** CodeSelectGrammar.gotResultsObject: direction=%s, where=%s, mark_selection=%s' % (direction, where, mark_selection)                

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
                    self.ranges.append(region)
                    
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
                self.interpreter.on_app.curr_buffer.set_selection(self.ranges[closest_range_index], cursor_at=where)
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

        print '-- CodeSelectGrammar.selection_spoken_form: returning spoken_form=%s' % spoken_form
        
        return spoken_form
