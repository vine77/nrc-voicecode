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

    print '-- VoiceDictation.addedByVC: flag=%s' % str(flag)
    if flag == None:
        indicator = 0
    elif (add_words_as == 'user'):
        indicator = (flag % int(0x00000010))        
    else:
        indicator = (flag / int(0x40000000))
    print '-- VoiceDictation.addedByVC: indicator=%s' % indicator
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

    if speech_able():
        if getWordInfo(word) == None:
#            print '-- VoiceDictation.addWord: this word is new to NatSpeak'
                   
            if len(rest) == 0:
                natlink.addWord(word, word_info_flag)
            elif len(rest) == 1:
                natlink.addWord(word, rest[0])
            else:
                return None



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
#        print '-- VoiceDictation.deleteWord: word=%s, flag=%s, num_words=%s, word_info_flag=%s' % (word, flag, num_words, word_info_flag)        
        if addedByVC(flag) and num_words > 1:
#            print '-- VoiceDictation.deleteWord: actually deleting word %s' % word
            return natlink.deleteWord(word)
        else:
#            print '-- VoiceDictation.deleteWord: word not added by VoiceCode %s' % word
            return None



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
        print '-- CommandDictGrammar.gotBegin: called'
        
    def gotResults(self, words):
        #
        # Interpret the commands, then print buffer content
        #
        print 'Heard mixed dictation and commands:%s' % repr(words)

        #
        # Substitute written form of words
        #
        for index in range(0, len(words)):
            a_word = words[index]
            print '-- CommandDictGrammar.gotResults: checking for special written form in %s' % a_word            
            a_match = re.match('^([^\\\\]*)\\\\([\s\S]*)$', a_word)
            if a_match:
                print '-- CommandDictGrammar.gotResults: %s has a special written form' % a_word            
                written_form = a_match.group(1)

                # Note: need to check for things like {enter} in written_form
                # ignore for now
                words[index] = written_form
                
        self.interpreter.interpret_NL_cmd(string.join(words))
        self.interpreter.app.print_buff_content()
        

class CodeSelectGrammar(SelectGramBase):

    def __init__(self, app=None):
        DictGramBase.__init__(self)
        self.app = app
        self.isActive = 0

    def gotBegin(self, moduleInfo):
        print '-- CodeSelectGrammar.gotBegin: called'
        self.setSelectText(self.app.curr_buffer.content)

    def gotResults(self, words, startPos, endPos):
        print 'Heard Select command: <%s>, startPos=%s, endPos=%s' % (string.join(words), startPos, endPos)
        self.app.select_region(startPos, endPos)
        self.app.print_buff_content()

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
                    print '-- CodeSelectGrammar.gotResultsObject: processingregion: %s' % repr(region)                    
                    distance = self.app.curr_buffer.distance_to_selection(region[0], region[1])
                    if closest == None or distance < closest:
                        self.ranges = [self.app.curr_buffer.content[region[0]:region[1]]]
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
    
