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

"""Defines abstract interface for the mediator GUI console and all other
GUI windows and dialog boxes

**MODULE VARIABLES**


"""

class MediatorConsole(Object.OwnerObject):
    """
    **INSTANCE ATTRIBUTES**

    *NewMediatorObject mediator* -- the mediator which owns this console

    *WinGramFactory gram_factory* -- the grammar factory used to add
    speech grammars to dialog boxes

    *INT main_frame_handle* -- the window-system specific ID for the
    main frame of the mediator application

    *WinSystem win_sys -- WinSystem interface to
    window-system specific functions
    **CLASS ATTRIBUTES**
    
    *none* 
    """
    def __init__(self, main_frame_handle, win_sys, **attrs):
        """
        **INPUTS**

        *INT main_frame_handle* -- the window-system specific ID for the
        main frame of the mediator application

        *WinSystem win_sys -- WinSystem interface to
        window-system specific functions
        """
        self.deep_construct(MediatorConsole,
                            {
                             'main_frame_handle': main_frame_handle,
                             'win_sys': win_sys,
                             'mediator': None,
                             'gram_factory': None
                            },
                            attrs)
        self.name_parent('mediator')
        self.win_sys.set_main_frame_handle(main_frame_handle)

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
        return self.win_sys.store_foreground_window()

    def set_mediator(self, mediator):
        """assigns a parent mediator to the console

        **INPUTS**

        *NewMediatorObject mediator* -- the parent mediator which will
        own the console

        **OUTPUTS**

        *none*
        """
        self.mediator = mediator

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
        return 0

    def heard_utterance(self, instance, words, gram_type = None):
        """callback from mediator to provide feedback to the user 
        that an utterance was heard

        **INPUTS**

        *STR instance* -- name of the instance whose grammar
        recognized the utterance

        *[(STR, STR)]* words -- list of spoken, written forms 
        representing the recognition results

        *STR gram_type* -- type of grammar 
        ('dictation', 'selection', or 'correction')

        **OUTPUTS**

        *none*
        """
        pass

    def set_gram_factory(self, gram_factory):
        """assigns a parent mediator to the console

        **INPUTS**

        *WinGramFactory gram_factory* -- the grammar factory used to add
        speech grammars to dialog boxes

        **OUTPUTS**

        *none*
        """
        self.gram_factory = gram_factory

    def correct_utterance(self, editor_name, utterance, 
        can_reinterpret, should_adapt = 1):
        """display a correction box for correction of a complete, recent
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
        debug.virtual('MediatorConsole.correct_utterance')

    def correct_recent(self, editor_name, utterances):
        """display a correct recent dialog box for to allow the user to 
        select a recent utterance to correct

        **INPUTS**

        *STR editor_name* -- name of the editor instance

        *[(SpokenUtterance, BOOL)] utterances* -- the n most recent dictation 
        utterances (or all available if < n), sorted most recent last, 
        with corresponding flags indicating if the utterance can be 
        undone and re-interpreted, or None if no utterances are stored.

        **OUTPUTS**

        *BOOL* -- true if the user made changes and approved them
        """
        debug.virtual('MediatorConsole.correct_utterance')

    def raise_active_window(self):
        """makes the active window (within the current process) the
        foreground one (for the system)

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        debug.virtual('MediatorConsole.raise_active_window')

    def already_modal(self):
        """does the console already have a modal dialog running?

        **INPUTS**

        *none*

        **OUTPUTS**
        
        *BOOL* -- true if a modal dialog is active
        """
        debug.virtual('MediatorConsole.already_modal')

    def dismiss_modal(self):
        """dismisses any modal dialog boxes which the console has
        running

        **INPUTS**

        *none*

        **OUTPUTS**
        
        *BOOL* -- true if the modal dialog box was sucessfully dismissed
        (or if there wasn't one to start with)
        """
        debug.virtual('MediatorConsole.dismiss_modal')

# defaults for vim - otherwise ignore
# vim:sw=4
