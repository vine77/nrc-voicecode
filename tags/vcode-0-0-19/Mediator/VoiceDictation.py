#
# Python Macro Language for Dragon NaturallySpeaking
#   (c) Copyright 1999 by Joel Gould
#   Portions (c) Copyright 1999 by Dragon Systems, Inc.
#
# windict.py
#
# This is a sample Python program which demonstrates how to use the
# NatLink dictation object in a Python program.  The user interface for
# this programn is based on the PythonWin (win32) extensions.
#
# The basic idea is as follows.
#
# Dragon NaturallySpeaking handles dictation by having a dictation object
# which contains a copy oft he user document.  In this way, NatSpeak knows
# what text is on the screen so it can get the spacing write.  It also
# knows the text on the screen for the Select and Correct commands.
#
# When writing an application which supports dictation (and voice editing),
# the application must keep the contents of the NatSpeak dictation object in
# sync with the text on the screen.
#
# In this sample application, we illustrate doing this for a rich edit
# control.  There will be a rich edit contorl on the screen and we keep its
# contents synchronized with a NatSpeak dictation object.  Thus, our simple
# edit control will allow our window to behave like NatSpeak's own editor
# window (althoug hnot every feature is exposed).
#
# For correctness, you only have to intercept the "begin" callback which
# happens just before recognition starts.  At that point you have to make
# sure that the internal dictation object has a complete copy of the state
# of the edit control -- text, selection and visible range.  Then when
# recognition occurs, the dictation object will return information about
# what change happened --- text deleted, text added and selection moved.
#
# To optimize for better performance and to prevent the lose of recorded
# speech, it helps if the code doe snot wait until the tsart of recognition,
# but instead updates the dictation object after every change of the edit
# control.
#
# The best implementation only tells the dictation object aboiut the change
# (for example a character was typed), but in this code I update the
# dictation object with the entire contents of the edit control on every
# keystroke.
#


import re
import natlink, vc_globals
from natlinkutils import *
from Object import Object

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

# The following functions are just wrappers on top of natlink ones.
# They check for value of environment variable *VCODE_NOSPEECH* before
# calling the corresponding natlink functions

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

    We add the word with flag of 0x40000000 which means 'added by
    Vocabulary  Builder'. This has the effect of decreasing the 
    a-priori probability of those words (so as to not affect  performance of  
    the vocabulary for regular dictation). It also  allows us to
    distinguish between words added by  VoiceCode and those added by the
    user which makes  it possible to clean up the vocabulary 
    VoiceDictation.addWord(a_form)"""
    
#VoiceDictation.addWord: word=%s' % word
    
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


#---------------------------------------------------------------------------
# VoiceDictation client
#
# This class provides a way of encapsulating the voice dictation (DictObj)
# of NatLink.  We can not derive a class from DictObj because DictObj is an
# exporeted C class, not a Python class.  But we can create a class which
# references a DictObj instance and makes it lkook like the class was
# inherited from DictObj.        

class VoiceDictation(Object):


    def __init__(self, dictation_object=None, **attrs):
        self.deep_construct(VoiceDictation, {'dictation_object': dictation_object}, attrs)

    # Initialization.  Create a DictObj instance and activate it for the
    # dialog box window.  All callbacks from the DictObj instance will go
    # directly to the dialog box.

    def initialize(self, window_handle, begin_cbk, change_cbk):
        if not os.environ.has_key('VCODE_NOSPEECH'):
            natlink.natConnect(1)
            self.dictation_object = natlink.DictObj()
            self.dictation_object.setBeginCallback(begin_cbk)
            self.dictation_object.setChangeCallback(change_cbk)
            self.dictation_object.activate(window_handle)

    # Call this function to cleanup.  We have to reset the callback
    # functions or the object will not be freed.
        
    def terminate(self):
        if not os.environ.has_key('VCODE_NOSPEECH'):
            self.dictation_object.deactivate()
            self.dictation_object.setBeginCallback(None)
            self.dictation_object.setChangeCallback(None)
            self.dictation_object = None

    # This makes it possible to access the member functions of the DictObj
    # directly as member functions of this class.
        
    def __getattr__(self,attr):
        try:
            if attr != '__dict__':
                dictation_object = self.__dict__['dictation_object']
                if dictation_object is not None:
                    return getattr(dictation_object,attr)
        except KeyError:
            pass
        raise AttributeError, attr

