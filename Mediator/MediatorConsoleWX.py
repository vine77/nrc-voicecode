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

import sys
import Object, vc_globals
import MediatorConsole
import string
from wxPython.wx import *


# unfortunately, I haven't found any non-MS specific way of manipulating
# the foreground window, nor have I found a way to do it from Python 
# without the win32gui module from the win32all extensions package

import win32gui

"""implementation of the MediatorConsole interface for a wxPython GUI mediator
(e.g. wxMediator)

**MODULE VARIABLES**


"""

class WasForegroundWindowMSW(MediatorConsole.WasForegroundWindow):
    """win32 implementation of WasForegroundWindow interface for 
    storing the current foreground window and restoring it to 
    the foreground later
    """
    def __init__(self, **args):
        """create an object which stores the current foreground
        window"""
        self.deep_construct(WasForegroundWindowMSW, {'handle': None}, args)
        self.handle = win32gui.GetForegroundWindow()

    def restore_to_foreground(self):
        """restores the window to the foreground"""
        win32gui.SetForegroundWindow(self.handle)


class MediatorConsoleWX(MediatorConsole.MediatorConsole):
    """
    **INSTANCE ATTRIBUTES**

    *wxFrame main_frame* -- the main frame window of the console, which
    will be the parent for most modal dialogs

    **CLASS ATTRIBUTES**
    
    *none* 
    """
    def __init__(self, main_frame, **attrs):
        self.deep_construct(MediatorConsoleWX,
                            {'main_frame': main_frame
                            },
                            attrs)

    def store_foreground_window(self):
        """detect the current foreground window, and store it in a
        WasForegroundWindow object, so that the window can later
        be restored to the foreground

        **INPUTS**

        *none*

        **OUTPUTS**

        *WasForegroundWindow* -- the object which can be used to restore
        the window to the foreground
        """
        return WasForegroundWindowMSW()

    def raise_active_window(self):
        """makes the active window (within the current process) the
        foreground one (for the system)

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        active_handle = win32gui.GetActiveWindow()
        win32gui.SetForegroundWindow(active_handle)

    def raise_wxWindow(self, window):
        """makes the given wxWindoactive window the
        foreground one (for the system)

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        win32gui.SetForegroundWindow(window.GetHandle())

    def correct_utterance(self, editor_name, utterance, 
        can_reinterpret, should_adapt = 1):
        """display a correction box for correction a complete, recent
        utterance, accept user corrections, allow the user to
        approve or cancel, and adapt the speech engine.

        **INPUTS**

        *STR editor_name* -- name of the editor instance

        *SpokenUtterance utterance* -- the utterance itself

        *BOOL can_reinterpret* -- flag indicating whether the utterance
        could be reinterpreted upon correction, allowing the correction
        box to give some visual feedback to the user to indictate this.
        Whether the utterance can actually be reinterpreted may change
        between the call to this method and its return, so there is no
        guarantee that reinterpretation will take place.

        *BOOL should_adapt* -- flag indicating whether correct_utterance
        should adapt the speech engine according to user corrections (if
        the user approves), or if the caller will handle that later.

        **OUTPUTS**

        *BOOL* -- true if the user made changes and approved them
        """
        original = utterance.words()
        validator = CorrectionValidatorSpoken(utterance = utterance)
        editor_window = self.store_foreground_window()
        box = CorrectionBoxWX(self, self.main_frame, utterance, validator, 
            can_reinterpret)
#        app = wxGetApp()
#        evt = wxActivateEvent(0, true)
#        app.ProcessEvent(evt)
        answer = box.ShowModal()
        box.cleanup()
#        print answer, utterance.spoken_forms()
#        win32gui.SetForegroundWindow(current_handle)
        editor_window.restore_to_foreground()
        if answer == wxID_OK:
            if should_adapt:
                utterance.adapt_spoken(utterance.spoken_forms())
            return 1
        else:
            utterance.set_words(original)
            return 0

class CorrectionBoxWX(wxDialog, Object.OwnerObject):
    """dialog box for correcting misrecognized dictation results

    **INSTANCE ATTRIBUTES**

    *SpokenUtterance utterance* -- the utterance being corrected
    
    *BOOL first* -- flag indicating whether this is the first time the
    window has been activated.

    *MediatorConsoleWX console* -- the MediatorConsole object which owns
    the correction box

    """
    def __init__(self, console, parent, utterance, validator, 
            can_reinterpret, pos = None, **args):
        """
        **INPUTS**

        *MediatorConsoleWX console* -- the MediatorConsole object which owns
        the correction box

        *wxFrame parent* -- the parent frame

        *(INT, INT)* -- position of the box in pixels
    
        *SpokenUtterance utterance* -- the utterance itself

        *CorrectionValidator validator* -- a validator used to transfer
        misrecognized text to the results text field, and corrected text
        back from that field

        *BOOL can_reinterpret* -- flag indicating whether the utterance
        could be reinterpreted upon correction, allowing the correction
        box to give some visual feedback to the user to indictate this.
        Whether the utterance can actually be reinterpreted may change
        between the call to this method and its return, so there is no
        guarantee that reinterpretation will take place.
        """
        self.deep_construct(CorrectionBoxWX,
                            {
                             'console': console,
                             'utterance': utterance,
                             'first': 1
                            }, args,
                            exclude_bases = {wxDialog:1})
        self.name_parent('console')
        use_pos = pos
        if pos is None:
            use_pos = wxDefaultPosition
        wxDialog.__init__(self, parent, wxNewId(), "Correction", use_pos,
            (600, 400))
        if pos is None:
            self.Center()
        s = wxBoxSizer(wxVERTICAL)
        intro = wxStaticText(self, wxNewId(), 
            "&Correct the text (use spoken forms)",
            wxDefaultPosition, wxDefaultSize)
        init_value = string.join(self.utterance.spoken_forms())
        self.text = wxTextCtrl(self, wxNewId(), init_value, wxDefaultPosition,
            wxDefaultSize, validator = validator)
        s.Add(self.text, 0, wxEXPAND | wxALL)
        middle_sizer = wxFlexGridSizer(3, 2, 5, 5)
# three rows, two columns, 5 pixels between rows and columns
        number_sizer = wxBoxSizer(wxVERTICAL)
        ID_CHOICES = wxNewId()
        n = 9
        alternatives = self.utterance.alternatives(n)
        spoken_alternatives = []
        for alternative in alternatives:
            spoken_alternatives.append(map(lambda x: x[0], alternative))
        self.choices = map(string.join, spoken_alternatives)
        ID_NUMBERS = wxNewId()
        for i in range(1, 10):
            st = wxStaticText(self, ID_NUMBERS + i, "%d" % i,
                wxDefaultPosition, wxDefaultSize, wxALIGN_RIGHT)
            number_sizer.Add(st, 0)
        self.choice_list = wxListBox(self, ID_CHOICES, wxDefaultPosition,
             wxDefaultSize, self.choices, wxLB_SINGLE)
        EVT_LISTBOX(self, ID_CHOICES, self.on_chosen)
        yes = wxBitmap("bitmaps/plus.bmp")
        no = wxBitmap("bitmaps/minus.bmp")
        if can_reinterpret: 
            which = yes
        else:
            which = no
        maybe = wxStaticBitmap(self, wxNewId(), which,
            wxDefaultPosition, wxDefaultSize)
        middle_sizer.AddMany([maybe,
                              (intro, 0, wxEXPAND),
                              (0, 0), #spacer
                              (self.text, 0, wxEXPAND),
                              (number_sizer, 0, wxEXPAND),
                              (self.choice_list, 0, wxEXPAND)])
        middle_sizer.AddGrowableRow(2)
        middle_sizer.AddGrowableCol(1)
        if self.choices:
            self.choice_list.SetSelection(1, 0)
        s.Add(middle_sizer, 1, wxEXPAND | wxALL)
        button_sizer = wxBoxSizer(wxHORIZONTAL)
        ok_button = wxButton(self, wxID_OK, "OK", wxDefaultPosition, 
            wxDefaultSize)
        cancel_button = wxButton(self, wxID_CANCEL, "Cancel", 
            wxDefaultPosition, wxDefaultSize)
        self.playback_button = wxButton(self, wxNewId(), "Playback", 
            wxDefaultPosition, wxDefaultSize)
        if not utterance.playback_available():
            self.playback_button.Enable(0)

        button_sizer.Add(ok_button, 0, wxALL)
        button_sizer.Add(cancel_button, 0, wxALL)
        button_sizer.Add(self.playback_button, 0, wxALL)
        EVT_BUTTON(self, self.playback_button.GetId(), self.on_playback)
        s.Add(button_sizer, 0, wxEXPAND | wxALL, 10)
        ok_button.SetDefault()
#        win32gui.SetForegroundWindow(self.main_frame.handle)
        EVT_ACTIVATE(self, self.on_activate)
        EVT_CHAR(self.text, self.on_char_text)
        self.Raise()
        self.text.SetFocus()
        self.SetAutoLayout(true)
        self.SetSizer(s)
        self.Layout()

    def on_playback(self, event):
        ok = self.utterance.playback()
        if not ok:
            self.playback_button.Disable()

    def on_char_text(self, event):
        k = event.GetKeyCode()
        if k == WXK_UP:
            direction = -1
        elif k == WXK_DOWN:
            direction = 1
        else:
            event.Skip()
            return
        n = self.choice_list.GetSelection()
        n = n + direction
        if n < 0 or n >= len(self.choices):
            return 
        self.choice_list.SetSelection(n)
        self.select_choice(self.choices[n])

    def select_choice(self, text):
        """method which modifies the text field when the selected item
        in the list box changes

        **INPUTS**

        *STR text* -- text of the selected item 

        **OUTPUTS**

        *none*
        """
        self.text.SetValue(text)
        self.text.SetInsertionPointEnd()
        self.text.SetSelection(0, self.text.GetLastPosition())
        self.text.SetFocus()

    def on_chosen(self, event):
        self.select_choice(event.GetString())
        event.Skip()

    def on_activate(self, event):
        if self.first:
            if event.GetActive():
                self.first = 0
#                self.console.raise_active_window()
                self.console.raise_wxWindow(self)
                if self.choices:
                    self.choice_list.SetSelection(1, 0)



class CorrectionValidator(wxPyValidator, Object.Object):
    """abstract base class for classes used to transfer (mis-)recognized text 
    to the correction box, and retreive corrected text from the 
    correction box when the ok button is pressed"""
    def __init__(self, utterance, **args):
        """
        **INPUTS**

        *SpokenUtterance utterance* -- the utterance to which the
        correction will be made
        """
        self.deep_construct(CorrectionValidator,
                            {
                             'utterance': utterance
                            }, args, exclude_bases = {wxPyValidator:1})
        wxPyValidator.__init__(self)

    def args_for_clone(self, dict):
        """adds keyword arguments needed to clone this class to a
        dictionary

        **NOTE:** subclasses which override this method must call their 
        parent class's args_for_clone method.
        
        **INPUTS**

        *{STR:ANY} dict* -- dictionary of keyword arguments

        **OUTPUTS**

        *none*

        **NOTE:** while this method has no outputs, it must modify the
        input dictionary by adding to it any constructor arguments needed to 
        clone the object.  
        """
        dict['utterance'] = self.utterance

    def Clone(self):
        """copies the validator.
        
        subclass must override this to create a
        copy of the appropriate subclass

        **INPUTS**

        *none*

        **OUTPUTS**

        *same as self* -- a copy of the validator (not a reference to
        self)
        """
        debug.virtual('CorrectionValidator.Clone')

    def Validate(self, win):
        """validate the contents of the text field

        **INPUTS**

        *wxWindow win* -- wxTextCtrl representing the corrected text

        **OUTPUTS**

        *BOOL* -- true if the field contents are valid
        """
        return true

    def initial_value(self):
        """retrieve the initial value for the (mis-)recognized text
        from the  utterance

        **INPUTS**

        *none*

        **OUTPUTS**

        *STR* -- the recognized text as a string
        """
        debug.virtual('CorrectionValidator.initial_value')

    def convert_corrected(self, corrected):
        """accepts the converts the corrected text as a string 
        and corrects the utterance (but does not adapt)

        **INPUTS**

        *STR corrected* -- the corrected text

        **OUTPUTS**

        *BOOL* -- true if the corrected text was successfully converted 
        (otherwise, the dialog box won't close)
        """
        debug.virtual('CorrectionValidator.convert_corrected')

    def TransferToWindow(self):
        """Transfer data from validator to window.

        **INPUTS**

        *none*

        **OUTPUTS**

        *BOOL* -- true if data was successfully transfered to the text
        control
        """
        win = self.GetWindow()
        win.SetValue(self.initial_value())
#        parent = win.GetParent()
#        parent.Raise()
#        print parent.parent.handle
#        for i in range(5):
#            w = win32gui.GetWindow(parent.parent.handle, 0)
#            print w
#            print win32gui.GetWindowText(w)
#        hf = win32gui.GetForegroundWindow()
#        ha = win32gui.GetActiveWindow()
#        print 'foreground, active = ', hf, ha
#        print 'dialog shown: ', parent.IsShown()
#        win32gui.SetForegroundWindow(ha)
        return true


    def TransferFromWindow(self):
        """Transfer data from window to validator.

        **INPUTS**

        *none*

        **OUTPUTS**

        *BOOL* -- true if data was successfully transfered from the text
        control
        """
        win = self.GetWindow()
        parent = win.GetParent()
#        parent.parent = None
        return self.convert_corrected(win.GetValue())

class CorrectionValidatorSpoken(CorrectionValidator):
    """simplest possible implementaion of CorrectionValidator,
    assuming that the corrected text is a space-delimited list of spoken
    forms.
    """
    def __init__(self, **args):
        self.deep_construct(CorrectionValidatorSpoken,
                            {
                            }, args)

    def args_for_clone(self, dict):
        """adds keyword arguments needed to clone this class to a
        dictionary

        **NOTE:** subclasses which override this method must call their 
        parent class's args_for_clone method.
        
        **INPUTS**

        *{STR:ANY} dict* -- dictionary of keyword arguments

        **OUTPUTS**

        *none*

        **NOTE:** while this method has no outputs, it must modify the
        input dictionary by adding to it any constructor arguments needed to 
        clone the object.  
        """
        CorrectionValidator.args_for_clone(self, dict)

    def Clone(self):
        """copies the validator.
        
        subclass must override this to create a
        copy of the appropriate subclass

        **INPUTS**

        *none*

        **OUTPUTS**

        *same as self* -- a copy of the validator (not a reference to
        self)
        """
        dict = {}
        self.args_for_clone(dict)
        return apply(CorrectionValidatorSpoken, [], dict)

    def initial_value(self):
        """retrieve the initial value for the (mis-)recognized text
        from the  utterance

        **INPUTS**

        *none*

        **OUTPUTS**

        *STR* -- the recognized text as a string
        """
        return string.join(self.utterance.spoken_forms())

    def convert_corrected(self, corrected):
        """accepts the converts the corrected text as a string 
        and corrects the utterance (but does not adapt)

        **INPUTS**

        *STR corrected* -- the corrected text

        **OUTPUTS**

        *BOOL* -- true if the corrected text was successfully converted 
        (otherwise, the dialog box won't close)
        """
        self.utterance.set_spoken(string.split(corrected))

# defaults for vim - otherwise ignore
# vim:sw=4
