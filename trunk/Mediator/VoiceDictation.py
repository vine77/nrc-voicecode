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

#  import re, sys
#  import string

#  # Pythonwin imports
#  from pywin.mfc import dialog
#  import win32ui
#  import win32api
#  import win32con
#  import win32gui

# Speech imports
import natlink, vc_globals
from natlinkutils import *
from Object import Object




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

