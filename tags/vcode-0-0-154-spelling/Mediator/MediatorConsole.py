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
class WasForegroundWindow(Object.Object):
    """abstract base class defining an interface for storing the current
    foreground window and restoring it to the foreground later

    """
    def __init__(self, **args):
        """create an object which stores the current foreground
        window"""
        self.deep_construct(WasForegroundWindow, {}, args)

    def restore_to_foreground(self):
        """restores the window to the foreground"""
        debug.virtual('WasForegroundWindow.restore_to_foreground')


class MediatorConsole(Object.OwnerObject):
    """
    **INSTANCE ATTRIBUTES**

    *NewMediatorObject mediator* -- the mediator which owns this console

    *WinGramFactory gram_factory* -- the grammar factory used to add
    speech grammars to dialog boxes


    **CLASS ATTRIBUTES**
    
    *none* 
    """
    def __init__(self, **attrs):
        self.deep_construct(MediatorConsole,
                            {
                             'mediator': None,
                             'gram_factory': None
                            },
                            attrs)
        self.name_parent('mediator')

    def set_mediator(self, mediator):
        """assigns a parent mediator to the console

        **INPUTS**

        *NewMediatorObject mediator* -- the parent mediator which will
        own the console

        **OUTPUTS**

        *none*
        """
        self.mediator = mediator

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
        debug.virtual('MediatorConsole.correct_utterance')

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
        debug.virtual('MediatorConsole.store_foreground_window')

    def raise_active_window(self):
        """makes the active window (within the current process) the
        foreground one (for the system)

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        debug.virtual('MediatorConsole.raise_active_window')

# defaults for vim - otherwise ignore
# vim:sw=4
