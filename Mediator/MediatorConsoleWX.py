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
import shutil
import Object, vc_globals
import MediatorConsole
import string
from wxPython.wx import *
from thread_communication_WX import *
import exceptions
import os
import threading

class DummyCapture:
    def __init__(self):
        pass

global possible_capture
possible_capture = DummyCapture
try:
    import wxCapture
#    global possible_capture 
    possible_capture = wxCapture.ScreenShotCapture
except exceptions.ImportError:
    pass



# unfortunately, I haven't found any non-MS specific way of manipulating
# the foreground window, nor have I found a way to do it from Python 
# without the win32gui module from the win32all extensions package

import win32gui
import pywintypes

"""implementation of the MediatorConsole interface for a wxPython GUI mediator
(e.g. wxMediator)

**MODULE VARIABLES**


"""

def EVT_MINE(evt_handler, evt_type, func):
    evt_handler.Connect(-1, -1, evt_type, func)

def NO_EVT_MINE(evt_handler, evt_type, func):
    evt_handler.Disconnect(-1, -1, evt_type, func)

# create a unique event types
wxEVT_DISMISS_MODAL = wxNewEventType()

wxID_DISMISS_MODAL = wxNewId()

wxID_CORRECT_NEXT = wxNewId()
wxID_CORRECT_PREV = wxNewId()
wxID_CORRECT_MORE = wxNewId()
wxID_DISCARD_CORRECTION = wxNewId()

class DismissModalFlagTimerWX(MediatorConsole.DismissModalEvent):
    """implementation of DismissModalEvent using a Python Event flag.  
    The dialog must check this flag periodically

    **INSTANCE ATTRIBUTES**

    *threading.Event bye* -- threading.Event object whose state will be
    set to true if the dialog box should cancel.  

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, bye, **args):
        self.deep_construct(DismissModalFlagTimerWX,
                            {'bye': bye},
                            args)

    def dismiss(self):
        """send the message, and return synchronously

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        self.bye.set()
        wxWakeUpIdle()



class MediatorConsoleWX(MediatorConsole.MediatorConsole):
    """
    **INSTANCE ATTRIBUTES**

    *wxFrame main_frame* -- the main frame window of the console, which
    will be the parent for most modal dialogs

    *(INT, INT) corr_box_pos* -- most recent position of the correction
    box

    *(INT, INT) corr_recent_pos* -- most recent position of the correct
    recent box

    **CLASS ATTRIBUTES**
    
    *none* 
    """
    def __init__(self, main_frame, **attrs):
        self.deep_construct(MediatorConsoleWX,
                            {'main_frame': main_frame,
                             'corr_box_pos': None,
                             'corr_recent_pos': None
                            },
                            attrs, 
                            enforce_value = {'main_frame_handle':
                            main_frame.GetHandle()})

    def user_message(self, message, instance = None):
        """displays a user message (usually on a MediatorConsole status 
        line, but Natspeak-style tooltips might also be a possibility)

        **INPUTS**

        *STR message* -- the message

        *STR instance_name* -- the editor from which the message
        originated, or None if it is not associated with a specific
        editor.

        **OUTPUTS**

        *BOOL* -- true if the MediatorConsole implementation has a means
        of displaying user messages 
        """
        self.main_frame.set_status_text(message)
        return 1

    def message_box(self, message):
        """displays an error or warning message in a message box

        **INPUTS**

        *STR message* -- the message

        **OUTPUTS**

        *none*
        """
        box = wxMessageDialog(self.main_frame, message, "Error", wxOK,
            wxDefaultPosition)
        box.ShowModal()
        box.Destroy()

    def starting_tests(self):
        """method used by NewMediatorObject to notify us that it is
        about to start regression testing

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        self.main_frame.starting_tests()

    def finished_tests(self):
        """method used by NewMediatorObject to notify us that it is
        done with regression testing

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        self.main_frame.finished_tests()


# Hopefully, raise_active_window and raise_wxWindow are made obsolete by
# WinSystemMSW, since the former doesn't work consistently, and the latter
# doesn't seem to work at all under Windows NT (and presumably 2000/XP
# as well)
# However, I'll leave them in until WinSystemMSW has been tested.

    def raise_active_window(self):
        """makes the active window (within the current process) the
        foreground one (for the system)

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        active_handle = win32gui.GetActiveWindow()
        for i in range(2):
            try:
                win32gui.SetForegroundWindow(active_handle)
            except pywintypes.error:
                sys.stderr.write('error restoring window to foreground\n')
            else:
                break

# Hopefully, raise_active_window and raise_wxWindow are made obsolete by
# WinSystemMSW, since the former doesn't work consistently, and the latter
# doesn't seem to work at all under Windows NT (and presumably 2000/XP
# as well)
# However, I'll leave them in until WinSystemMSW has been tested.

    def raise_wxWindow(self, window):
        """makes the given wxWindow the foreground one (for the system)

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        for i in range(2):
            try:
                win32gui.SetForegroundWindow(window.GetHandle())
            except pywintypes.error:
                sys.stderr.write('error restoring window to foreground\n')
            else:
                break

    def show_modal_dialog(self, dialog):
        """shows a dismissable modal dialog box, and handles the push/pop modal 
        bookkeeping
        
        **INPUTS**
        
        *Dismissable, OwnerObject dialog* -- the dialog to show
        
        **OUTPUTS**
        
        *INT* -- the return code from ShowModal 
        """
        bye = dialog.dismiss_event()
        self.push_modal(bye)
        answer = dialog.ShowModal()
        self.pop_modal()
        return answer

    def copy_user_config(self, target, directory):
        """prompt the user for the sample user configuration file to
        copy to the target path, and copy the file

        **INPUTS**

        *STR target* -- the path of the default user configuration file

        *STR directory* -- the initial directory in which to look for a
        sample configuration file to copy

        **OUTPUTS**

        *BOOL* -- true if a file was selected and copied to the target
        path
        """
        message = """The user_config.py file does not exist.  
              One must be created before the mediator can be started.
              Select one of the sample user configuration files to use
              as an initial user file (which can then be customized)."""
        caption = "Missing user configuration file"
        wxMessageBox(message, caption, wxOK, self.main_frame)
        message = "Choose a sample user configuration file"
        wild = "Python scripts (*.py)|*.py"
        dlg = wxFileDialog(self.main_frame, message, directory, "",
            wild, wxOPEN | wxHIDE_READONLY)
        answer = dlg.ShowModal()
        if answer != wxID_OK:
            dlg.Destroy()
            return 0
        path = dlg.GetPath()
        shutil.copy(path, target)
        dlg.Destroy()
        return 1

    def show_correction_box(self, editor_name, utterance, 
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
        box = CorrectionBoxWX(self, self.main_frame, utterance, validator, 
            can_reinterpret, self.gram_factory, pos = self.corr_box_pos)
#        app = wxGetApp()
#        evt = wxActivateEvent(0, true)
#        app.ProcessEvent(evt)
        answer = self.show_modal_dialog(box)
        self.corr_box_pos = box.GetPositionTuple()
        box.cleanup()
        box.Destroy()
        if answer == wxID_OK:
            if should_adapt:
                utterance.adapt_spoken(utterance.spoken_forms())
            return 1
        else:
            utterance.set_words(original)
            return 0

    def show_recent_utterances(self, editor_name, utterances):
        """display a correct recent dialog box for to allow the user to 
        select a recent utterance to correct

        **INPUTS**

        *STR editor_name* -- name of the editor instance

        *[(SpokenUtterance, INT, BOOL)] utterances* -- the n most recent 
        dictation utterances (or all available if < n), sorted most recent 
        last, each with a corresponding utterance number and a flag 
        indicating if the utterance can be undone and re-interpreted.

        **OUTPUTS**

        *[INT]* -- the utterance numbers of 
        those utterances which were corrected by the user, or None if
        none were corrected
        """
        originals = map(lambda u: u[0].words(), utterances)
        box = CorrectRecentWX(self, self.main_frame, utterances, 
            self.gram_factory, pos = self.corr_recent_pos)
        answer = self.show_modal_dialog(box)
        self.corr_recent_pos = box.GetPositionTuple()
        changed = box.changed()  
        box.cleanup()
        box.Destroy()
        if answer == wxID_OK:
#            print 'answer was OK'
            return changed
        else:
#            print 'answer was cancel'
            return None


class ByeByeMixIn(MediatorConsole.Dismissable, Object.OwnerObject):
    """mix-in for a dialog box with an idle handler which checks a 
    threading.Event object to see if it should simulate being dismissed.

    **INSTANCE ATTRIBUTES**

    *threading.Event bye* -- threading.Event object whose state will be
    set to true if the dialog box should cancel.  The mix-in
    has a timer event which checks the state of the Event object
    and calls on_dismiss if the Event's state
    becomes true.  The dialog box should then call EndModal with return
    value wxID_DISMISS_MODAL.
    """
    def __init__(self, **args):
        """
        """
        ID_DISMISS_FLAG_TIMER = wxNewId()
        self.deep_construct(ByeByeMixIn,
                            {
                             'bye': threading.Event(),
                             'timer': wxTimer(self, ID_DISMISS_FLAG_TIMER)
                            }, args)
        EVT_TIMER(self, ID_DISMISS_FLAG_TIMER, self.check_dismiss_flag)
        self.timer.Start(50)
# this doesn't work because of a bug in wxPython (modal dialog boxes 
# which were started from a custom event handler are created from within
# an idle event, so no other idle events get processed until 
# the modal dialog box closes), so we'll need
# another solution
#        EVT_IDLE(wxGetApp(), self.check_dismiss_flag)
#        EVT_IDLE(self, self.check_dismiss_flag)

    def remove_other_references(self):
#        print 'disconnecting event?'
        self.timer.Stop()
        self.timer = None
# this doesn't work because of a bug in wxPython (modal dialog boxes 
# which were started from a custom event handler are created from within
# an idle event, so no other idle events get processed until 
# the modal dialog box closes), so we'll need
# another solution
#        wxGetApp().Disconnect(-1, -1, wxEVT_IDLE)
#        print self.Disconnect(-1, -1, wxEVT_IDLE)

    def dismiss_event(self):
        """returns a DismissModalEvent which can be used to dismiss the
        dialog

        **INPUTS**

        *none*

        **OUTPUTS**

        *DismissModalEvent* -- the event
        """
        return DismissModalFlagTimerWX(self.bye)

# this doesn't work because of a bug in wxPython (modal dialog boxes 
# which were started from a custom event handler are created from within
# an idle event, so no other idle events get processed until 
# the modal dialog box closes), so we'll need
# another solution
    def check_dismiss_flag_idle(self, event):
#        print 'idle'
        if self.bye.isSet():
#           print 'set'
            self.on_dismiss()
            return
        event.RequestMore()
#        print 'not set'

    def check_dismiss_flag(self, event):
        if self.bye.isSet():
            self.on_dismiss()
            return

    def on_dismiss(self):
        debug.virtual('ByeByeMixIn.on_dismiss')

class CorrectionBoxWX(wxDialog, ByeByeMixIn, possible_capture, Object.OwnerObject):
    """dialog box for correcting misrecognized dictation results

    **INSTANCE ATTRIBUTES**

    *SpokenUtterance utterance* -- the utterance being corrected
    
    *BOOL first* -- flag indicating whether this is the first time the
    window has been activated.

    *MediatorConsoleWX console* -- the MediatorConsole object which owns
    the correction box

    *ChoiceGram choose_n_gram* -- ChoiceGram supporting "Choose n"

    *ChoiceGram select_n_gram* -- ChoiceGram supporting "SelectOrEdit n"

    *NaturalSpelling spelling_gram* -- NaturalSpelling grammar

    *SimpleSelection selection_gram* -- SimpleSelection grammar for 
    select-and-say in the corrected text control

    *[STR] choices* -- list of alternatives
    """
    def __init__(self, console, parent, utterance, validator, 
            can_reinterpret, gram_factory, pos = None, **args):
        """
        **INPUTS**

        *MediatorConsoleWX console* -- the MediatorConsole object which owns
        the correction box

        *wxWindow parent* -- the parent wxWindow

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

        *WinGramFactory gram_factory* -- the grammar factory used to add
        speech grammars to the dialog box

        *(INT, INT) pos* -- position of the box in pixels
    
        """
        use_pos = pos
        if pos is None:
            use_pos = wxDefaultPosition
        wxDialog.__init__(self, parent, wxNewId(), "Correction", use_pos,
            (600, 400), style = wxDEFAULT_DIALOG_STYLE | wxRESIZE_BORDER)
        possible_capture.__init__(self)
        self.deep_construct(CorrectionBoxWX,
                            {
                             'console': console,
                             'utterance': utterance,
                             'first': 1,
                             'choices': None,
                             'choose_n_gram': None,
                             'select_n_gram': None,
                             'selection_gram': None
                            }, args, 
                            exclude_bases = {possible_capture: 1, wxDialog: 1}
                           )
        self.name_parent('console')
        self.add_owned('choose_n_gram')
        self.add_owned('select_n_gram')
        self.add_owned('spelling_gram')
        self.add_owned('selection_gram')
        if gram_factory:
            self.choose_n_gram = \
                gram_factory.make_choices(choice_words = ['Choose'])
            self.select_n_gram = \
                gram_factory.make_choices(choice_words = ['Select', 'Edit'])
            self.spelling_gram = \
                gram_factory.make_natural_spelling(spelling_cbk = \
                self.on_spelling)
            self.selection_gram = \
                gram_factory.make_simple_selection(get_visible_cbk = \
                self.get_text, get_selection_cbk = self.get_selection,
                select_cbk = self.on_select_text)
        if pos is None:
            self.CenterOnScreen()
        s = wxBoxSizer(wxVERTICAL)
        intro = wxStaticText(self, wxNewId(), 
            "&Correct the text (use spoken forms)",
            wxDefaultPosition, wxDefaultSize)
        init_value = string.join(self.utterance.spoken_forms())
        init_value = ""
# due to a bug in wxWindows, setting the initial value of a text control
# with default size may cause some of the text to be cut off.
#
# instead, we now set the initial value from the validator
        self.text = wxTextCtrl(self, wxNewId(), init_value, wxDefaultPosition,
            wxDefaultSize, style = wxTE_NOHIDESEL, validator = validator)
#        s.Add(self.text, 0, wxEXPAND | wxALL)
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
            number_sizer.Add(st, 0, wxALIGN_RIGHT | wxALIGN_BOTTOM)
        self.choice_list = wxListBox(self, ID_CHOICES, wxDefaultPosition,
             wxDefaultSize, self.choices, wxLB_SINGLE)
        EVT_LISTBOX(self.choice_list, ID_CHOICES, self.on_selected)
        EVT_LISTBOX_DCLICK(self.choice_list, ID_CHOICES, self.on_double)
        bitpath = os.path.join(vc_globals.home, 'Mediator', 'bitmaps')
        yes = wxBitmap(os.path.join(bitpath, 'plus.bmp'), wxBITMAP_TYPE_BMP)
        no = wxBitmap(os.path.join(bitpath, 'minus.bmp'), wxBITMAP_TYPE_BMP)
        if can_reinterpret: 
            which = yes
        else:
            which = no
        maybe = wxStaticBitmap(self, wxNewId(), which,
            wxDefaultPosition, wxDefaultSize)
        middle_sizer.AddMany([(maybe, 0, wxALIGN_CENTER),
                              (intro, 0, wxEXPAND),
                              (0, 0), #spacer
                              (self.text, 0, wxEXPAND | wxALIGN_TOP, 3),
                              (number_sizer, 0, wxEXPAND | wxALIGN_RIGHT),
                              (self.choice_list, 0, wxEXPAND)])
        middle_sizer.AddGrowableRow(2)
        middle_sizer.AddGrowableCol(1)
# not sure why this was needed in the first place - it doesn't seem to
# be now -- DCF
#        if self.choices:
#            self.choice_list.SetSelection(0, 0)
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
        ok_button.SetDefault()
# optionally, add additional buttons
        extra_buttons = self.more_buttons()
        if extra_buttons:
            s.Add(extra_buttons, 0, wxEXPAND | wxALL, 10)
        s.Add(button_sizer, 0, wxEXPAND | wxALL, 10)
#        print 'ids', ok_button.GetId(), wxID_OK
#        win32gui.SetForegroundWindow(self.main_frame.handle)
        EVT_ACTIVATE(self, self.on_activate)
        EVT_CHAR(self.text, self.on_char_text)
        EVT_SET_FOCUS(self.text, self.on_focus_text)
        EVT_KILL_FOCUS(self.text, self.on_kill_focus_text)
        self.Raise()
        self.text.SetFocus()
#        print 'before autolayout: text size is ', self.text.GetSize()
        self.SetAutoLayout(true)
        self.SetSizer(s)
        self.Layout()
#        print 'before fit: text size is ', self.text.GetSize()
        s.Fit(self)
#        print 'after fit: text size is ', self.text.GetSize()
#        EVT_MINE(self, wxEVT_DISMISS_MODAL, self.on_dismiss(self))

    def more_buttons(self, button_sizer = None):
        """optionally, add additional buttons

        **INPUTS**

        *wxBoxSizer button_sizer* -- the box sizer for the button row.
        If None and if more_buttons wants to add buttons, it should
        create a new horizontal wxBoxSizer.
      

        **OUTPUTS**

        *wxBoxSizer* -- a reference to the same button sizer,
        containing the added buttons, or None if none was passed to 
        more_buttons and no more buttons were added
        """
        return button_sizer

    def on_dismiss(self):
        self.EndModal(wxID_DISMISS_MODAL)

    def on_playback(self, event):
        ok = self.utterance.playback()
        if not ok:
            self.playback_button.Enable(0)
        self.text.SetFocus()

    def get_text(self):
        return self.text.GetValue()

    def get_selection(self):
        return self.text.GetSelection()

    def on_select_text(self, range):
        if range is not None:
            self.text.SetSelection(range[0], range[1])

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

    def on_focus_text(self, event):
        if self.spelling_gram:
            self.spelling_gram.activate(self.GetHandle())

    def on_kill_focus_text(self, event):
        if self.spelling_gram:
            self.spelling_gram.deactivate()

    def on_spelling(self, letters):
        """callback called by natural spelling grammar

        **INPUTS**

        *STR* letters -- string of recognized letters

        **OUTPUTS**

        *none*
        """
#        print 'spelled "%s"' % letters
        self.text.WriteText(letters)

    def on_select(self, n):
        """callback called by Select/Edit n grammar to indicate which
        choice was selected

        **INPUTS**

        *INT n* -- the index of the choice selected

        **OUTPUTS**

        *none*
        """
        if n <= self.choice_list.GetCount():
            self.choice_list.SetSelection(n - 1)
            self.select_choice(self.choices[n-1])

    def on_choose(self, n):
        """callback called by Select/Edit n grammar to indicate which
        choice was selected

        **INPUTS**

        *INT n* -- the index of the choice selected

        **OUTPUTS**

        *none*
        """
        if n <= self.choice_list.GetCount():
            self.choice_list.SetSelection(n - 1)
            self.select_choice(self.choices[n-1])
            self.simulate_OK()

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
#        print 'text changing: text size is ', self.text.GetSize()

    def on_selected(self, event):
        self.select_choice(event.GetString())
        event.Skip()

    def simulate_OK(self):
        """method which simulates the user having pressed the Ok button

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        button_event = wxCommandEvent(wxEVT_COMMAND_BUTTON_CLICKED, wxID_OK)
        self.ProcessEvent(button_event)
# DCF: For some reason, wxPostEvent doesn't work right if the correction
# box was created from within my custom event handler (though it does if
# it was created from within an EVT_BUTTON handler)
#        wxPostEvent(self, button_event)

    def on_double(self, event):
        self.select_choice(event.GetString())
        self.simulate_OK()

    def on_activate(self, event):
        if self.first:
            if event.GetActive():
                if self.choose_n_gram:
                    self.choose_n_gram.activate(9, self.GetHandle(), 
                        self.on_choose)
                    self.select_n_gram.activate(9, self.GetHandle(), 
                        self.on_select)
                if self.selection_gram:
                    self.selection_gram.activate(window = self.GetHandle())
                self.first = 0
# doesn't work consistently
#                self.console.raise_active_window()
# doesn't work on Win NT
#                self.console.raise_wxWindow(self)
                self.console.win_sys.raise_main_frame()
#                if self.choices:
#                    self.choice_list.SetSelection(0, 0)


class CorrectNextPrevWX(CorrectionBoxWX):
    """subclass of CorrectionBoxWX which adds the option of correcting 
    the next or previous utterance

    **INSTANCE ATTRIBUTES**

    *BOOL first_utterance* -- indicates if this utterance is the first 
    stored utterance, in which case the option to correct the previous 
    utterance should be disabled.

    *BOOL last_utterance* -- indicates if this utterance is the most 
    recent utterance, in which case the option to correct the next 
    utterance should be disabled.
    """
    def __init__(self, first_utterance = 0, last_utterance = 0, **args):
        self.decl_attrs({'first_utterance': first_utterance,
                              'last_utterance': last_utterance})
        self.deep_construct(CorrectNextPrevWX, {}, args)

    def more_buttons(self, button_sizer = None):
        """optionally, add additional buttons

        **INPUTS**

        *wxBoxSizer button_sizer* -- the box sizer for the button row.
        If None and if more_buttons wants to add buttons, it should
        create a new horizontal wxBoxSizer.
      

        **OUTPUTS**

        *wxBoxSizer* -- a reference to the same button sizer,
        containing the added buttons, or None if none was passed to 
        more_buttons and no more buttons were added
        """
        button_sizer = CorrectionBoxWX.more_buttons(self, button_sizer)
        correct_previous = wxButton(self, wxNewId(), "Previous Phrase", 
            wxDefaultPosition, wxDefaultSize)
        correct_next = wxButton(self, wxNewId(), "Next Phrase", 
            wxDefaultPosition, wxDefaultSize)
        if self.first_utterance:
            correct_previous.Enable(0)
        if self.last_utterance:
            correct_next.Enable(0)
        if button_sizer is None:
            button_sizer = wxBoxSizer(wxHORIZONTAL)
        button_sizer.Add(correct_previous, 0, wxALL)
        button_sizer.Add(correct_next, 0, wxALL)
        EVT_BUTTON(self, correct_previous.GetId(), 
            self.on_correct_previous)
        EVT_BUTTON(self, correct_next.GetId(), 
            self.on_correct_next)
        return button_sizer

    def on_correct_previous(self, event):
        if self.Validate() and self.TransferDataFromWindow():
            self.EndModal(wxID_CORRECT_PREV)
    def on_correct_next(self, event):
        if self.Validate() and self.TransferDataFromWindow():
            self.EndModal(wxID_CORRECT_NEXT)

class CorrectFromRecentWX(CorrectNextPrevWX):
    """subclass of CorrectNextPrevWX which adds the option of returning to
    the correct recent dialog box for additional corrections, or after
    discarding changes 
    """
    def __init__(self, **args):
        self.deep_construct(CorrectFromRecentWX, {}, args)

    def more_buttons(self, button_sizer = None):
        """optionally, add additional buttons

        **INPUTS**

        *wxBoxSizer button_sizer* -- the box sizer for the button row.
        If None and if more_buttons wants to add buttons, it should
        create a new horizontal wxBoxSizer.
      

        **OUTPUTS**

        *wxBoxSizer* -- a reference to the same button sizer,
        containing the added buttons, or None if none was passed to 
        more_buttons and no more buttons were added
        """
        button_sizer = CorrectNextPrevWX.more_buttons(self, button_sizer)
        more_correction = wxButton(self, wxNewId(), "More Correction", 
            wxDefaultPosition, wxDefaultSize)
        discard_changes = wxButton(self, wxNewId(), "Discard Changes", 
            wxDefaultPosition, wxDefaultSize)
        EVT_BUTTON(self, more_correction.GetId(), 
            self.on_more_correction)
        EVT_BUTTON(self, discard_changes.GetId(), 
            self.on_discard_changes)
        if button_sizer is None:
            button_sizer = wxBoxSizer(wxHORIZONTAL)
        button_sizer.Add(more_correction, 0, wxALL)
        button_sizer.Add(discard_changes, 0, wxALL)
        return button_sizer

    def on_more_correction(self, event):
        if self.Validate() and self.TransferDataFromWindow():
            self.EndModal(wxID_CORRECT_MORE)

    def on_discard_changes(self, event):
        self.EndModal(wxID_DISCARD_CORRECTION)



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
        text = self.initial_value()
        win.SetValue(text)
        win.SetInsertionPointEnd()
        win.SetSelection(0, len(text))
#        print text
#        print win.GetValue()
#        print win.GetSelection()
#        print win.GetSize()
#        win.Refresh()
#        print win.GetSize()
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
#        print 'transferring from window'
        valid = self.convert_corrected(win.GetValue())
#        print 'valid = %d' % valid
        return valid

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
        return 1

class CorrectRecentWX(wxDialog, ByeByeMixIn, possible_capture, Object.OwnerObject):
    """dialog box which lists recently dictated utterances, allowing the user 
    to select one for correction of misrecognized results or for symbol 
    reformatting

    **INSTANCE ATTRIBUTES**

    *[(SpokenUtterance, INT, BOOL)] utterances* -- the n most recent 
    dictation utterances (or all available if < n), sorted most recent 
    last, each with a corresponding utterance number and a flag 
    indicating if the utterance can be undone and re-interpreted.

    *BOOL first* -- flag indicating whether this is the first time the
    window has been activated.

    *MediatorConsoleWX console* -- the MediatorConsole object which owns
    the correction box

    *WinGramFactory gram_factory* -- the grammar factory used to add
    speech grammars to the dialog box

    *ChoiceGram correct_n_gram* -- ChoiceGram supporting "Correct n"
    """
    def __init__(self, console, parent, utterances, 
            gram_factory, pos = None, **args):
        """
        **INPUTS**

        *MediatorConsoleWX console* -- the MediatorConsole object which owns
        the correction box

        *wxWindow parent* -- the parent wxWindow

        *[(SpokenUtterance, INT, BOOL)] utterances* -- the n most recent 
        dictation utterances (or all available if < n), sorted most 
        recent last, with corresponding flags indicating if the utterance 
        can be undone and re-interpreted

        *{INT: BOOL} corrected* -- set of utterances which have been
        corrected, counted from most recent = 1

        *WinGramFactory gram_factory* -- the grammar factory used to add
        speech grammars to the dialog box

        *(INT, INT) pos* -- position of the box in pixels
        """
        use_pos = pos
        if pos is None:
            use_pos = wxDefaultPosition
        wxDialog.__init__(self, parent, wxNewId(), "Correct Recent", use_pos,
            (600, 400),
            style = wxDEFAULT_DIALOG_STYLE | wxRESIZE_BORDER)
        possible_capture.__init__(self)
        self.deep_construct(CorrectRecentWX,
                            {
                             'console': console,
                             'utterances': utterances,
                             'gram_factory': gram_factory,
                             'first': 1,
                             'nth_event': CorrectNthEventWX(self),
                             'corrected': {},
                             'correct_n_gram': None,
                            }, args, 
                            exclude_bases = {possible_capture:1, wxDialog: 1}
                           )
        self.name_parent('console')
        self.add_owned('correct_n_gram')
        if gram_factory:
            if wxMAJOR_VERSION > 2 or \
                (wxMAJOR_VERSION == 2 and 
                     (wxMINOR_VERSION > 3 or 
                          (wxMINOR_VERSION == 3 and wxRELEASE_NUMBER >= 4)
                     )
                ):
                self.correct_n_gram = \
                    gram_factory.make_choices(choice_words = ['Correct'])
        if pos is None:
            self.CenterOnScreen()

        s = wxBoxSizer(wxVERTICAL)
        intro = wxStaticText(self, wxNewId(), 
            "&Choose a phrase to correct",
            wxDefaultPosition, wxDefaultSize)
        s.Add(intro, 0, wxEXPAND | wxALL)
        recent = wxListCtrl(self, wxNewId(), wxDefaultPosition,
            wxDefaultSize, 
            style = wxLC_REPORT | wxLC_HRULES | wxLC_SINGLE_SEL)
        recent.InsertColumn(0, "#")
        recent.InsertColumn(1, "Spoken phrase")
        phrases = map(lambda x: string.join(x[0].spoken_forms()),
            utterances)
        can_reinterpret = map(lambda x: x[2], utterances)
        index = range(len(phrases), 0, -1)
        bitpath = os.path.join(vc_globals.home, 'Mediator', 'bitmaps')
        yes = wxBitmap(os.path.join(bitpath, 'small_plus.bmp'), wxBITMAP_TYPE_BMP)
        no = wxBitmap(os.path.join(bitpath, 'small_minus.bmp'), wxBITMAP_TYPE_BMP)
        self.images = wxImageList(16, 16)
        index_no = self.images.Add(no)
        index_yes = self.images.Add(yes)
# I'm guessing that LC_REPORT uses small images
        recent.SetImageList(self.images, wxIMAGE_LIST_SMALL)
        for i in range(len(phrases)):
            if can_reinterpret[i]: 
                which = index_yes
            else:
                which = index_no
            recent.InsertImageStringItem(i, str(index[i]), which)
            recent.SetStringItem(i, 1, phrases[i])
        recent.SetColumnWidth(0, wxLIST_AUTOSIZE)
        recent.SetColumnWidth(1, wxLIST_AUTOSIZE)

        recent.ScrollList(0, len(phrases))
        self.recent = recent
        self.phrases = phrases
        s.Add(recent, 1, wxEXPAND | wxALL)
        okb = wxButton(self, wxID_OK, "OK", wxDefaultPosition, wxDefaultSize)
        cancelb = wxButton(self, wxID_CANCEL, "Cancel", wxDefaultPosition, wxDefaultSize)
#        EVT_BUTTON(self, okb.GetId(), self.on_ok)
        b_sizer = wxBoxSizer(wxHORIZONTAL)
        b_sizer.Add(okb, 0, 0)
        b_sizer.Add(cancelb, 0, 0)
        s.Add(b_sizer, 0, wxEXPAND | wxALL)
#        okb.SetDefault()
# note: neither of these handlers gets called if a child control 
# has the focus.
# I thought they would be called if the focused control didn't have a
# handler
        EVT_ACTIVATE(self, self.on_activate)
        EVT_CHAR(self, self.on_char)
#        EVT_KEY_DOWN(self, self.on_key_down)

#        EVT_KEY_DOWN(self.recent, self.on_recent_char)
#        EVT_CHAR(self.recent, self.on_recent_char)

        EVT_LIST_ITEM_ACTIVATED(self.recent, self.recent.GetId(), self.on_choose)
        self.SetAutoLayout(true)
        self.SetSizer(s)
        self.Layout()
        actual = s.GetSize()
        minimum = s.GetMinSize()
        list_size = self.recent.GetSize()
        list_client_size = self.recent.GetClientSize()
        h = list_client_size.GetHeight()
        w = list_client_size.GetWidth()
        s.SetItemMinSize(self.recent, w, h)
        s.SetMinSize(wxSize(0, actual.GetHeight()))
        q = s.GetMinSize()
        s.Fit(self)
        s.SetMinSize(wxSize(q.GetWidth(), 0))
        self.resize_last_column()
        last = len(self.phrases)-1
        self.recent.EnsureVisible(last)
        self.recent.SetItemState(last, wxLIST_STATE_SELECTED, wxLIST_STATE_SELECTED)
        self.recent.SetItemState(last, wxLIST_STATE_FOCUSED, wxLIST_STATE_FOCUSED)
        self.hook_events()
    def hook_events(self):
        """hook events up to our handlers

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        EVT_MINE(self, wxEVT_CORRECT_NTH_RECENT, self.on_nth_by_voice)

    def resize_last_column(self):
        list_client_size = self.recent.GetClientSize()
        n_cols = self.recent.GetColumnCount()
        rest = 0
        for col in range(n_cols -1):
            rest = rest + self.recent.GetColumnWidth(col)
        self.recent.SetColumnWidth(n_cols - 1, list_client_size.width - rest)

    def focus_recent(self):
        self.recent.SetFocus()

    def on_choose(self, event):
        i = event.GetIndex()
        print 'on_choose, %d' %i
        self.chose_from_list(i)

    def correct_nth(self, n):
        """display a correction box for correction a complete, recent
        utterance, accept user corrections, and allow the user to
        approve or cancel.

        **INPUTS**

        *INT n* -- correct nth most recent utterance

        **OUTPUTS**

        *STR* -- string indicating the outcome of the correction dialog:
        allowed values are 'ok', 'cancel', 'next', 'previous', 'more',
        'discard'
        """
        u = self.utterances[-n]
        utterance = u[0]
        can_reinterpret = u[2]
        validator = CorrectionValidatorSpoken(utterance = utterance)
        box = CorrectFromRecentWX(console = self.console, parent = self, 
            utterance = utterance, validator = validator, 
            can_reinterpret = can_reinterpret, gram_factory = self.gram_factory,
            pos = self.console.corr_box_pos,
            last_utterance = (n == 1), 
            first_utterance = (n == len(self.utterances)))
        answer = self.console.show_modal_dialog(box)
        self.console.corr_box_pos = box.GetPositionTuple()
        box.cleanup()
        box.Destroy()
        if answer == wxID_OK:
            return 'ok'
        elif answer == wxID_CANCEL:
            return 'cancel'
        elif answer == wxID_CORRECT_NEXT:
            return 'next'
        elif answer == wxID_CORRECT_PREV:
            return 'previous'
        elif answer == wxID_CORRECT_MORE:
            return 'more'
        elif answer == wxID_DISCARD_CORRECTION:
            return 'discard'
# shouldn't happen, but ...
        return None

    def chose_from_list(self, i):
        n = len(self.phrases) - i
        original_words = self.utterances[-n][0].words()
        answer = self.correct_nth(n)
        if answer == 'cancel':
            self.EndModal(wxID_CANCEL)
            return
        if answer == 'discard':
            self.utterances[-n][0].set_words(original_words)
            self.focus_recent()
            return
        self.corrected[n] = 1
        self.phrases[i] = string.join(self.utterances[i][0].spoken_forms())
        self.recent.SetStringItem(i, 1, self.phrases[i])
        self.resize_last_column()
        if answer == 'next':
            self.chose_from_list(i + 1)
        elif answer == 'previous':
            self.chose_from_list(i - 1)
        elif answer == 'ok':
            if self.Validate() and self.TransferDataFromWindow():
                self.EndModal(wxID_OK)
        self.focus_recent()
        return
#        str = 'You chose item %d: "%s"' % (n, self.phrases[-n])
#        m = wxMessageDialog(self, str, style = wxOK)
#        m.ShowModal()
#        m.Destroy()

#    def on_ok(self, event):
#        print 'hit ok'
#        event.Skip()

    def on_char(self, event):
        k = event.GetKeyCode()
        if k == WXK_PRIOR:
            top = self.recent.GetTopItem()
            page = self.recent.GetCountPerPage()
            new_top = top-page
            if new_top < 0:
                new_top = 0
            self.recent.EnsureVisible(new_top)
        elif k == WXK_NEXT:
            top = self.recent.GetTopItem()
            page = self.recent.GetCountPerPage()
            last = self.recent.GetItemCount()
            new_bottom = top+ 2*page
            if new_bottom >= last:
                new_bottom = last -1
            self.recent.EnsureVisible(new_bottom)
        else:
            event.Skip()
            return

    def on_activate(self, event):
        if self.first:
#            print 'first'
            if event.GetActive():
                if self.correct_n_gram:
                    self.correct_n_gram.activate(len(self.phrases), 
                        self.GetHandle(), self.chose_by_voice)
                self.first = 0
                self.console.raise_wxWindow(self)
                self.focus_recent()

    def chose_by_voice(self, n):
        i = len(self.phrases) - n
# send an event to notify self to bring up correct n asynchronously
        self.nth_event.notify(i)

    def on_nth_by_voice(self, event):
# bring up correct n synchronously
        self.chose_from_list(event.recent_chosen)

    def changed(self):
        """reports which utterances have been corrected

        **INPUTS**

        *none*
        
        **OUTPUTS**

        *[INT]* -- the indices of those utterances which have been 
        corrected by the user, counted from most recent = 1, or 
        None if none were corrected
        """
        return self.corrected.keys()



# defaults for vim - otherwise ignore
# vim:sw=4
