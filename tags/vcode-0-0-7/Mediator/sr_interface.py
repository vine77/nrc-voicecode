"""Interface to the Speech Recognition engine.
"""

import re
import natlink
from natlinkutils import *
import CmdInterp
#import nsformat

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

def addedByVC(flag):   
    """Returns *true* iif word information *flag* indicates that word
    was added by VoiceCode"""

#    print '-- sr_interfacen.addedByVC: flag=%s' % str(flag)
    if flag == None:
        indicator = 0
    elif (add_words_as == 'user'):
        indicator = (flag % int(0x00000010))        
    else:
        indicator = (flag / int(0x40000000))
#    print '-- sr_interfacen.addedByVC: indicator=%s' % indicator
    return indicator

def getWordInfo(word, *rest):    
    if speech_able():
        if len(rest) == 0:
            return natlink.getWordInfo(word)
        elif len(rest) == 1:
            return natlink.getWordInfo(word, rest[0])
    else:
        return None


def addWord(word, *rest):
    """Add a word to NatSpeak's vocabulary.

    We only add the word if it doesn't already exist in the vocabulary
    and if speech is enabled (i.e. environment variable
    $VCODE_NOSPEECH undefined).
    """
        
    global word_info_flag

#    print '-- sr_interface.addWord: adding \'%s\'' % word
    if speech_able():
        if getWordInfo(word) == None:
#            print '-- sr_interfacen.addWord: this word is new to NatSpeak'
                   
            if len(rest) == 0:
                flag = word_info_flag
            elif len(rest) == 1:
                flag = rest[0]
            else:
                return None
                
            natlink.addWord(word, flag)

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
    
    if speech_able():
        flag = getWordInfo(word, 4)
        num_words = len(re.split('\s+', word))
#        print '-- sr_interfacen.deleteWord: word=%s, flag=%s, num_words=%s, word_info_flag=%s' % (word, flag, num_words, word_info_flag)        
        if addedByVC(flag) and num_words > 1:
#            print '-- sr_interfacen.deleteWord: actually deleting word %s' % word
            return natlink.deleteWord(word)
        else:
#            print '-- sr_interfacen.deleteWord: word not added by VoiceCode %s' % word
            return None




def spoken_written_form(vocabulary_entry):
    """Returns the written and spoken forms of a NatSpeak vocabulary entry
    
    **INPUTS**
    
    *STR* vocabulary_entry -- the vocabulary entry in either
    written or written\\spoken form.
    
    **OUTPUTS**
    
    *STR* (spoken, written) -- written and spoken forms of the vocabulary entry.
    """
    a_match = re.match('^([^\\\\]*)\\\\([\s\S]*)$', vocabulary_entry)
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
    # Substitute {Spacebar}->' ', {Enter} -> '\n'
    #
    written = re.sub('\\{Enter\\}', '\n', written)
    written = re.sub('\\{Spacebar\\}', ' ', written)

    return (spoken, written)
    

def vocabulary_entry(spoken_form, written_form):
    """Creates a vocabulary entry with given spoken and written forms.

    **INPUTS**

    *STR* spoken_form -- the spoken form 

    *STR* \*written_form -- the written form (default to *spoken_form*)


    **OUTPUTS**

    *entry* -- the entry to be added to the SR vocabulary
    """

#    print '-- sr_interface.vocabulary_entry: spoken_form=\'%s\', written_form=%s' % (spoken_form, repr(written_form))

    #
    # Substitute blanks in written form
    #
    written_form = re.sub('\n', '{Enter}', written_form)
    written_form = re.sub('\s', '{Spacebar}', written_form)
    if len(written_form) > 0:
        entry = written_form + '\\' + spoken_form
    else:
        entry = spoken_form
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
        self.interpreter.load_language_specific_aliases()        
        
    def gotResults(self, words):
        #
        # Interpret the commands, then print buffer content
        #
#        print '-- CommandDictGrammar.gotResults: Heard mixed dictation and commands:%s' % repr(words)

        #
        # Substitute written form of words
        #
        for index in range(0, len(words)):
            spoken, words[index] = spoken_written_form(words[index])
                
        self.interpreter.interpret_NL_cmd(string.join(words))
        self.interpreter.on_app.print_buff_content()
        

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

    def gotBegin(self, moduleInfo):
#        print '-- CodeSelectGrammar.gotBegin: called'
        self.interpreter.load_language_specific_aliases()
#        print '-- CodeSelectGrammar.gotBegin: calling self.setSelectText with bufer content:\n*** Start of buffer content ***\n%s\n*** End of buffer content ***' % self.interpreter.on_app.curr_buffer.content
        self.setSelectText(self.interpreter.on_app.curr_buffer.content)

    def gotResults(self, words, startPos, endPos):
#        print '-- CodeSelectGrammar.gotResults: Heard Select command: <%s>, startPos=%s, endPos=%s' % (string.join(words), startPos, endPos)
        self.interpreter.on_app.select(startPos, endPos)

    def gotResultsObject(self,recogType,resObj):
        # If there are multiple matches in the text we need to scan through
        # the list of choices to find every entry which has the highest.
        
        self.ranges = []
        closest = None
        try:
            bestScore = resObj.getWordInfo(0)[0][2]
            for i in range(100):
                wordInfo = resObj.getWordInfo(i)
                if wordInfo[0][2] != bestScore:
                    return
                else:
                    region = resObj.getSelectInfo(self.gramObj, i)
#                    print '-- CodeSelectGrammar.gotResultsObject: processingregion: %s' % repr(region)                    
                    distance = self.interpreter.on_app.curr_buffer.distance_to_selection(region[0], region[1])
                    if closest == None or distance < closest:
                        self.ranges = [self.interpreter.on_app.curr_buffer.content[region[0]:region[1]]]
        except natlink.OutOfRange:
            return


def run():
    try:
        natlink.natConnect()
        natlink.setMicState('on')
        myGrammar = CommandDictGrammar()
        natlink.waitForSpeech()
    finally:        
        natlink.setMicState('off')
        myGrammar.unload()
        natlink.natDisconnect()

if __name__=='__main__':
    run()
    
