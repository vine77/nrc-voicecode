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

#    print '-- sr_interface.disconnect: called, sr_is_connected=%s' % sr_is_connected
    if speech_able() and sr_is_connected:
#        print '-- sr_interface.disconnect: calling natlink.natDisconnect()'
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
    
#    print '-- sr_interface.openUser: user_name=%s, create_if_not_exist=%s, create_using_model=%s, create_using_topic=%s' % (user_name, create_if_not_exist, create_using_model, create_using_topic)
    try:
        natlink.openUser(user_name)
#        print '-- sr_interface.openUser: natlink.openUser succeeded'
    except natlink.UnknownName, exc:
#        print '-- sr_interface.openUser: natlink.openUser failed'
        if create_if_not_exist:
#            print '-- sr_interface.openUser: creating new user, user_name=%s, create_using_model=%s, create_using_topic=%s' % (user_name, create_using_model, create_using_topic)
            natlink.createUser(user_name, create_using_model, create_using_topic)
        else:
            #
            # Reraise the exception so it can be caught further up the call chain
            #
            raise exc

def saveUser():
    """Saves the current user"""
#    print '-- sr_interface.saveUser: saving user'
    natlink.saveUser()
#    print '-- sr_interface.saveUser: user saved'    
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

    def gotBegin(self, moduleInfo):
#        print '-- CodeSelectGrammar.gotBegin: called'
#        print '-- CodeSelectGrammar.gotBegin: calling self.setSelectText with bufer content:\n*** Start of buffer content ***\n%s\n*** End of buffer content ***' % self.interpreter.on_app.curr_buffer.contents()
        self.setSelectText(self.interpreter.on_app.curr_buffer.contents())

    def gotResults(self, words, startPos, endPos):
#        print '-- CodeSelectGrammar.gotResults: Heard Select command: <%s>, startPos=%s, endPos=%s' % (string.join(words), startPos, endPos)
        self.interpreter.on_app.set_selection((startPos, endPos))

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
                        self.ranges = [self.interpreter.on_app.curr_buffer.contents()[region[0]:region[1]]]
        except natlink.OutOfRange:
            return


    

##############################################################################
#
# -- Alain
# The code below is inserted only so I don't forget about a potentially useful
# hack.
#
#:-( :-( :-( :-( :-( :-( :-( :-( :-( :-( :-( :-( :-( :-( :-( :-( :-( :-( :-( 
# SILLY ME! This is useless because the DictObj never receives speech data
# to associate to the words it receives through recognitionMimic, so it's
# useless for correction purposes. Oh well, keep it there until I'm sure
# it's really useless
#:-( :-( :-( :-( :-( :-( :-( :-( :-( :-( :-( :-( :-( :-( :-( :-( :-( :-( :-( 
#
# David Fox wants to use a DictObj (i.e. VDct based) grammar to keep track of
# what was said for error correction purposes.
#
# The problem is that DictObj only returns a string that is the concatenation
# of written form of words. But the interpreter NEEDS to receive a list of
# words in written\spoken form (because just the concatenation of written
# forms is too ambiguous).
#
# Such a list of words could however be supplied by a DictGramBase object
#
# The solution is to have both types of grammars active at the same type.
# I tried this, and both grammars hear the beginning of the utterance but
# only the DictObj grammar gets the final results. I tried to make the DictObj
# non-exclusive, but that class doesn't support setExclusive method
#
# So, the hack is to not make the DictObj active to start with. When the
# DictGramBase object gets results, it forwards them to the interprter,
# and then forwards them to the DictObj by activating it and doing a
# recognitionMimic. When the DictObj's text change callback is activated,
# it simply disactivates the DictObj, thus returning control back to the
# DictGramBase object
#
# One potential problem with that is that the VoiceDictation object only returns
# control to the InterpreterGrammar when it hears something that results in
# changes to its internal buffer. So if the words do not result in changes to the
# internall buffer (e.g. a word with no written form), then the InterpreterGrammar
# won't get results until the VoiceDictation object gets an other result which does cause a text change.
#
# From a user's point of view, it's not a big deal. It won't happen too often and
# it just means that a few words or commands may be missed. However, for error
# correction, it may completely screw up the matching between what the
# VoiceDictation thinks was typed and what the command interpreter actually typed
# (based on what it received from the InterpreterGrammar).
#
# The code below (based on Joel Gould's windict.py) illustrates how all of
# this can be done.
#
# To try it, copy and paste it to a .py file and run that file as a script.
#
##############################################################################

#  #
#  # Python Macro Language for Dragon NaturallySpeaking
#  #   (c) Copyright 1999 by Joel Gould
#  #   Portions (c) Copyright 1999 by Dragon Systems, Inc.
#  #
#  # my_windict2.py
#  #
#  # This is a sample Python program which demonstrates how to use the
#  # NatLink dictation object in a Python program.  The user interface for
#  # this programn is based on the PythonWin (win32) extensions.
#  #
#  # The basic idea is as follows.
#  #
#  # Dragon NaturallySpeaking handles dictation by having a dictation object
#  # which contains a copy oft he user document.  In this way, NatSpeak knows
#  # what text is on the screen so it can get the spacing write.  It also
#  # knows the text on the screen for the Select and Correct commands.
#  #
#  # When writing an application which supports dictation (and voice editing),
#  # the application must keep the contents of the NatSpeak dictation object in
#  # sync with the text on the screen.
#  #
#  # In this sample application, we illustrate doing this for a rich edit
#  # control.  There will be a rich edit contorl on the screen and we keep its
#  # contents synchronized with a NatSpeak dictation object.  Thus, our simple
#  # edit control will allow our window to behave like NatSpeak's own editor
#  # window (althoug hnot every feature is exposed).
#  #
#  # For correctness, you only have to intercept the "begin" callback which
#  # happens just before recognition starts.  At that point you have to make
#  # sure that the internal dictation object has a complete copy of the state
#  # of the edit control -- text, selection and visible range.  Then when
#  # recognition occurs, the dictation object will return information about
#  # what change happened --- text deleted, text added and selection moved.
#  #
#  # To optimize for better performance and to prevent the lose of recorded
#  # speech, it helps if the code doe snot wait until the tsart of recognition,
#  # but instead updates the dictation object after every change of the edit
#  # control.
#  #
#  # The best implementation only tells the dictation object aboiut the change
#  # (for example a character was typed), but in this code I update the
#  # dictation object with the entire contents of the edit control on every
#  # keystroke.
#  #

#  import sys
#  import string

#  # Pythonwin imports
#  from pywin.mfc import dialog
#  import win32ui
#  import win32api
#  import win32con
#  import win32gui

#  # Speech imports
#  import natlink
#  from natlinkutils import *

#  #---------------------------------------------------------------------------
#  # This code describes the dialog box.  I cheated when I created the dialog.
#  # I created the dialog box using Visual C++ so that I could use a graphical
#  # layout tool.  Then I copied the resource file information here.  The
#  # format of the text in the template was determined by looking at the
#  # pythonwin sample applications.
#  #

#  IDC_EDIT = 1000
#  IDC_MICBUTTON = 1001

#  def MakeDlgTemplate():
#      style = win32con.DS_MODALFRAME|win32con.WS_POPUP|win32con.WS_VISIBLE|win32con.WS_CAPTION|win32con.WS_SYSMENU
#      child = win32con.WS_CHILD|win32con.WS_VISIBLE
#      templ = [
#          ["Correction Test Window",(0, 0, 320, 197),style,None,(8,"MS Sans Serif")],
#          ["RICHEDIT","",IDC_EDIT,(7,7,306,167),child|win32con.ES_MULTILINE|win32con.ES_AUTOVSCROLL|win32con.ES_WANTRETURN|win32con.WS_BORDER|win32con.WS_VSCROLL|win32con.WS_TABSTOP],
#          [128,"Turn &Mic On",IDC_MICBUTTON,(244,176,65,14),child],
#      ]
#      return templ

#  #---------------------------------------------------------------------------
#  # Command grammar
#  #
#  # I have included a very simple command grammar sonsisting of one command
#  # "delete that" as an example.  The command grammar can be easily extended.

#  class CommandGrammar(GrammarBase):

#      # First we list our grammar as a long string.  The grammar is in SAPI
#      # format, where we define a series of rules as expressions built from
#      # other rules, words and lists.  Rules which can be activated are flagged
#      # with the keyword "exported".

#      gramSpec = """
#          <DeleteThat> exported = delete that;
#      """

#      # Call this function to load the grammar, activate it and install
#      # install callback functions
    
#      def initialize(self,dlg):
#          self.dlg = dlg
#          self.load(self.gramSpec)
#          self.setExclusive(0)
#          self.activateAll(dlg.GetSafeHwnd())
    
#      # Call this function to cleanup.  We have to reset the callback
#      # functions or the object will not be freed.

#      def terminate(self):
#          self.dlg = None
#          self.unload()

#      # This routine is called from GrammarBase when words are recognized from
#      # the rule 'DeleteThat'.  We pass the recognition information directly
#      # to the dialog box code.
        
#      def gotResults_DeleteThat(self,words,fullResults):
#          self.dlg.onCommand_DeleteThat(words)

#  #---------------------------------------------------------------------------
#  # VoiceDictation client
#  #
#  # This class provides a way of encapsulating the voice dictation (DictObj)
#  # of NatLink.  We can not derive a class from DictObj because DictObj is an
#  # exporeted C class, not a Python class.  But we can create a class which
#  # references a DictObj instance and makes it lkook like the class was
#  # inherited from DictObj.        

#  class VoiceDictation:

#      def __init__(self):
#          self.dictObj = None

#      # Initialization.  Create a DictObj instance and activate it for the
#      # dialog box window.  All callbacks from the DictObj instance will go
#      # directly to the dialog box.

#      def initialize(self,dlg):
#          self.dlg = dlg
#          self.dictObj = natlink.DictObj()
#          self.dictObj.setBeginCallback(dlg.onTextBegin)

#          #
#          # Note: assumed that dlg.onTextChange will automatically disactivate
#          # the VoiceDictation at the end, thus allowing InterpreterGrammar
#          # to get results again.
#          #
#          # This means that if the VoiceDictation object hears something that
#          # never results in a change to the buffer, it will never return
#          # "control" back to the InterpreterGrammar.
#          #
#          # Don't know if that can happen, other than if some other command
#          # (not dictation) grammar gets the recognition results instead of
#          # the VoiceDictation grammar.
#          #
#          # Note that this may not be such a big deal because as soon as
#          # VoiceDictation hears SOMETHING that causes text to be changed,
#          # control will revert back to the InterpreterGrammar.
#          # So the worse that can happen is that the interpreter will
#          # miss a few utterances and the user can simply reutter them.
#          #
#          self.dictObj.setChangeCallback(dlg.onTextChange)
        
#  # This doesn't work because VoiceDictation doesn't support setExclusive()
#  #        self.setExclusive(0)

#  # Don't activate the VoiceDictation grammar. InterpreterGrammar will do that
#  # before doing a recognitionMimic on what it receives
#  #        self.dictObj.activate(dlg.GetSafeHwnd())

#      # Call this function to cleanup.  We have to reset the callback
#      # functions or the object will not be freed.
        
#      def terminate(self):
#          self.dictObj.deactivate()
#          self.dictObj.setBeginCallback(None)
#          self.dictObj.setChangeCallback(None)
#          self.dictObj = None

#      # This makes it possible to access the member functions of the DictObj
#      # directly as member functions of this class.
        
#      def __getattr__(self,attr):
#          try:
#              if attr != '__dict__':
#                  dictObj = self.__dict__['dictObj']
#                  if dictObj is not None:
#                      return getattr(dictObj,attr)
#          except KeyError:
#              pass
#          raise AttributeError, attr

#  class InterpreterGrammar(DictGramBase):
#      """This grammar would hear everything that the VoiceDictation grammar
#      hears, but it would send it to the interpreter
#      """
    
#      def __init__(self):
#          DictGramBase.__init__(self)
#          self.state = None
#          self.isActive = 0

#      def initialize(self,dlg):
#          self.dlg = dlg
#          self.voiceDictObj = None
#          self.load()
#          self.setExclusive(0)
#          self.activate(dlg.GetSafeHwnd())
        
#      def gotBegin(self, moduleInfo):
#          print '-- InterpreterGrammar.gotBegin: called'
        
#      def gotResults(self, words):
#          #
#          # Interpret the commands, then print buffer content
#          #
#          print '-- InterpreterGrammar.gotResults: Heard mixed dictation and commands:%s. This would be sent to the interpreter.' % repr(words)
#          print '-- InterpreterGrammar.gotResults: Now, forwarding those words to VoiceDictation through recognitionMimic'
#          self.voiceDictObj.activate(self.dlg.GetSafeHwnd())
#          recognitionMimic(words)
        

    

#  #---------------------------------------------------------------------------
#  # Dialog box

#  class TestDialog(dialog.Dialog):

#      # Dialog initialization.  Tell the rich text control to send us change
#      # messages, install callbacks for buttons and initialize the command and
#      # dictation objects.
#      def OnInitDialog(self):
#          rc = dialog.Dialog.OnInitDialog(self)
#          self.HookCommand(self.onMicButton,IDC_MICBUTTON)
#          self.HookCommand(self.onNotify,IDC_EDIT)
#          self.edit = self.GetDlgItem(IDC_EDIT)
#          self.edit.SetEventMask(win32con.ENM_CHANGE)
        
#          self.grammar = CommandGrammar()
#          self.grammar.initialize(self)
        
#          self.dictObj = VoiceDictation()
#          self.dictObj.initialize(self)

#          self.interpGrammar = InterpreterGrammar()
#          self.interpGrammar.initialize(self)

#          #
#          # Make interpGrammar aware of dictObj so it can forward
#          # what it recognises to it.
#          #
#          self.interpGrammar.voiceDictObj = self.dictObj
        

#      # When the dialog is closed, make sure we delete the grammar and
#      # dictation objects so the callbacks are reset
        
#      def OnDestroy(self,msg):
#          self.grammar.terminate()
#          self.grammar = None
#          self.dictObj.terminate()
#          self.dictObj = None

#      # This subroutine transfers the contents and state of the edit control
#      # into the dictation object.  We currently don't bother to indicate
#      # exactly what changed.  The dictation object will compare the text we
#      # write with the contents of its buffer and only make the necessary
#      # changes (as long as on one contigious region has changed).
        
#      def updateState(self):
#          text = self.edit.GetWindowText()
#          selStart,selEnd = self.edit.GetSel()
#          visStart,visEnd = self.getVisibleRegion()

#          self.dictObj.setLock(1)
#          self.dictObj.setText(text,0,0x7FFFFFFF)
#          self.dictObj.setTextSel(selStart,selEnd)
#          self.dictObj.setVisibleText(visStart,visEnd)
#          self.dictObj.setLock(0)

#      # Utility subroutine which calculates the visible region of the edit
#      # control and returns the start and end of the current visible region.
        
#      def getVisibleRegion(self):
#          top,bottom,left,right = self.edit.GetClientRect()
#          firstLine = self.edit.GetFirstVisibleLine()
#          visStart = self.edit.LineIndex(firstLine)

#          lineCount = self.edit.GetLineCount()
#          lastLine = lineCount
#          for line in range(firstLine+1,lineCount):
#              charInLine = self.edit.LineIndex(line)
#              left,top = self.edit.GetCharPos(charInLine)
#              if top >= bottom:
#                  break
#              lastLine = line

#          visEnd = self.edit.LineIndex(lastLine+1)
#          if visEnd == -1:
#              visEnd = len(self.edit.GetWindowText())
#          return visStart,visEnd
        
#      # Special code for the microphone button.  We turn the microphone on or
#      # off depending on its current state.

#      def onMicButton(self,nID,code):
#          micState = natlink.getMicState()
#          if micState == 'on' or micState == 'sleeping':
#              self.SetDlgItemText(IDC_MICBUTTON,'Turn &Mic On')
#              natlink.setMicState('off')
#          else:
#              self.SetDlgItemText(IDC_MICBUTTON,'Turn &Mic Off')
#              natlink.setMicState('on')
#          self.edit.SetFocus()

#      # When something changes in the edit control (usually because the user
#      # is typing), update the dictation object.

#      def onNotify(self,controlId,code):
#          if code == win32con.EN_CHANGE:
#              self.updateState()

#      # This routine is invoked when we hear "delete that".  We simply play a
#      # delete key.  A more sophisticated algorithm is possible, but I am
#      # lazy.

#      def onCommand_DeleteThat(self,words):
#          natlink.playString('{Del}')

#      # We get this callback just before recognition starts. This is our
#      # chance to update the dictation object just in case we missed a change
#      # made to the edit control.

#      def onTextBegin(self,moduleInfo):
#          self.updateState()

#      # We get this callback when something in the dictation object changes
#      # like text is added or something is selected by voice.  We then update
#      # the edit control to match the dictation object.

#      def onTextChange(self,delStart,delEnd,newText,selStart,selEnd):
#          print '-- onTextChange: called'
#          self.dictObj.setLock(1)
#          self.edit.SetSel(delStart,delEnd)
#          self.edit.ReplaceSel(newText)
#          self.edit.SetSel(selStart,selEnd)
#          self.dictObj.setLock(0)

#          #
#          # At the end, we disactivate the VoiceDictation grammar in order to
#          # allow the InterpreterGrammar to get results again.
#          #
#          print '-- onTextChange: disactivating the VoiceDictation grammar'
#          self.dictObj.deactivate()

#  #---------------------------------------------------------------------------
#  # This is the main routine.  Here we connect to the speech subsystem,
#  # create the dialog box and when the dialog is closed, disconnect from
#  # the speech subsystem.
#  #
#  # If an exception occurs, make sure we disconnect from NatSpeak before
#  # reporting the exception.

#  def run():
#      try:
#          natlink.natConnect(1)
#          a_dialog = TestDialog(MakeDlgTemplate()).DoModal()
#          natlink.natDisconnect()
#      except:
#          natlink.natDisconnect()
#          raise

#  if __name__=='__main__':
#      run()
