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
# (C) 2002, National Research Council of Canada
#
##############################################################################

"""Interface to the Emacs editor."""

import as_services, AppStateMessaging, SourceBuffEmacs

import sr_interface

# used for keybd_event
import win32api
import win32con

from debug import trace

        
class AppStateEmacs(AppStateMessaging.AppStateMessaging):
    """Interface to the Emacs editor.

    **INSTANCE ATTRIBUTES**

    *AS_ServiceBreadcrumbs breadcrumbs_srv* -- service handling
    breadcrumb-related functions

    *BOOL use_ignored_key* -- flag indicating whether we should send the
    new ignored key message before recog_begin
    """

    def __init__(self, use_ignored_key = 0, **attrs):
        self.deep_construct(AppStateEmacs, 
                            {'breadcrumbs_srv': 
                              as_services.AS_ServiceBreadcrumbs(app=self),
                             'use_ignored_key': use_ignored_key},
#                            {'breadcrumbs_srv': None},
                            attrs, new_default = {'app_name': 'emacs'})
#        self.breadcrumbs_srv = as_services.AS_ServiceBreadcrumbs(app=self)                            
        self.add_owned('breadcrumbs_srv')                            

    def _multiple_buffers_from_app(self):
        return 1

    def _bidirectional_selection_from_app(self):
        return 1

    def new_compatible_sb(self, buff_name):
        """Creates a new instance of [SourceBuffEmacs] which is compatible
        with [AppStateEmacs].
        
        **INPUTS**
                
        STR *buff_name* -- ID of the source buffer.
        
        **OUTPUTS**
        
        *none* -- 

        ..[SourceBuffEmacs] file:///./SourceBuffEmacs.SourceBuffEmacs.html
        ..[AppStateEmacs] file:///./AppStateEmacs.AppStateEmacs.html"""
        
        return SourceBuffEmacs.SourceBuffEmacs(app=self, buff_name=buff_name)
        
#
# No need to ask Emacs for updates, because it will notify VCode of changes
# as they happen.
# DCF: not true - still need to get updates on current position and selection
#        
#    def updates_from_app(self, what = None, exclude=1):        
#        return []

    def config_from_external(self):
        pass
        

    def recog_begin(self, window_id, block = 0):
        """Invoked at the beginning of a recognition event.

        The editor then returns telling VoiceCode whether or not the user
        is allowed to speak into window *window_id*.

        **INPUTS**
        
        INT *window_id* -- The ID of the window that was active when
        the recognition began.                

	*BOOL block* -- true if the speech engine can detect recog_end
	events reliably.  If so, and if the editor is capable of doing so, 
        the editor may (at its discretion) also stop responding to user
        input until method [recog_end()] is invoked.  This is to
        prevent a bunch of problems that can arise if the user types
        while VoiceCode is still processing an utterance. In such
        cases, the results of the utterance interpretation can be
        unpredictable, especially when it comes to correction.

	**NOTE:** However, if block is false, the editor **MUST NOT**
	stop responding, because the mediator will not be able to use
	recog_end to tell it to resume responding to user input.  

	Also, the editor must provide a way for the user to re-enable
	input manually, in case the mediator crashes.  If it cannot do
	so, it should not stop responding, regardless of the value of
	block.

        **OUTPUTS**
        
        BOOL *can_talk* -- *true* iif editor allows user to speak into window
        with ID *window_id*
        
        .. [recog_end()] file:///./AppState.AppState.html#recog_end"""

        if self.multiple_windows() and self.use_ignored_key:
            self.talk_msgr.send_mess('emacs_prepare_for_ignored_key')
            response = self.talk_msgr.get_mess(expect = \
                ['emacs_prepare_for_ignored_key_resp'])

            win32api.keybd_event(win32con.VK_F9, 0x43, 0, 0)
            win32api.keybd_event(win32con.VK_F9, 0x43, win32con.KEYEVENTF_KEYUP, 0)
# can't call this from within a gotBegin callback, so we have to
# simulate this using windows.  Should probably use SendInput, but
# that's not wrapped by the win32 Python extensions, so let's try this
# for now
#            sr_interface.send_keys('{F9}')

        return AppStateMessaging.AppStateMessaging.recog_begin(self, window_id, block = block)

        
    #
    # Note: If and when we support Emacs in single shell mode (with process
    #       suspension), we will have to modify the methods below to use
    #       the AppStateMessaging version. Emacs will then have to respon
    #       to those messages. It will respond to them differently depending
    #       on whether it is operating in single shell window or multi window
    #       environment, and whether it is in a suspended state or not.
    #
    
    
# Multiple windows mode is basically working now, so we don't need to
# override this any more
#    def _multiple_windows_from_app(self):
#        return 0
    
# DCF: emacs now handles this message, so we can use the default version
# from AppStateMessaging
#    def _shared_window_from_app(self):
#        return 0

# DCF: bit of a cheat, but since suspend_notification is true, this will
# only be called once, when AppStateMessaging is initialized.  Emacs
# should be active when it first connects (otherwise, how did it
# connect), and if it isn't, a lot of other calls would 
# hang
    def _is_active_from_app(self):
        return 1
        
# Eventually, delete this method and make Emacs respond to the
# "suspendable" message with 0 if 'window-system is "w32" and
# 1 otherwise
#
# DCF: emacs now handles this message, so we can use the default version
# from AppStateMessaging
#    def suspendable(self):
#        return 0

# For now, assume that Emacs will not be able to notify of suspension.
# Later on, see if there are hooks in Emacs allowing such notification.
#
# DCF: emacs now handles this message, so we can use the default version
# from AppStateMessaging
#    def suspend_notification(self):
#        return 0
        
    def shared_window(self):
        return 0
        
    def title_escape_sequence(self, before = "", after = ""):
        """gives the editor a (module-dependent) hint about the escape
	sequence which can be used to set the module's window title, if
	any.  If the editor has its own mechanism for setting the window
	title, it should simply ignore this method.  

	**INPUTS**

	*STR* before -- the escape sequence to be sent before the string
	to place in the window title, or the empty string if there is no
	escape sequence

	*STR* after -- the escape sequence which terminates the window
	title value

	**OUTPUTS**

        *BOOL* -- true if the editor, given the title escape sequence, 
        can and will include the instance string in its window title 
        for all windows containing editor buffers.
	"""
# for right now at least, Emacs doesn't handle this message, so we
# should just return the same value set by the earlier call to
# set_instance_string
        return self.can_show_instance_string

    def drop_breadcrumb(self, buffname=None, pos=None):
        self.breadcrumbs_srv.drop_breadcrumb(buffname, pos)


    def pop_breadcrumbs(self, num=1, gothere=1):
        self.breadcrumbs_srv.pop_breadcrumbs(num, gothere)

        
        
        
