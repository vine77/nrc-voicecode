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
from debug import trace

        
class AppStateEmacs(AppStateMessaging.AppStateMessaging):
    """Interface to the Emacs editor.
    """

    def __init__(self, **attrs):
        self.deep_construct(AppStateEmacs, 
                            {'breadcrumbs_srv': as_services.AS_ServiceBreadcrumbs(app=self)},
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
        
        
    #
    # Note: If and when we support Emacs in single shell mode (with process
    #       suspension), we will have to modify the methods below to use
    #       the AppStateMessaging version. Emacs will then have to respon
    #       to those messages. It will respond to them differently depending
    #       on whether it is operating in single shell window or multi window
    #       environment, and whether it is in a suspended state or not.
    #
    
    
    def _multiple_windows_from_app(self):
        return 0
    
    def _shared_window_from_app(self):
        return 0

    def _is_active_from_app(self):
        return 1
        
    # Eventually, delete this method and make Emacs respond to the
    # "suspendable" message with 0 if 'window-system is "w32" and
    # 1 otherwise
    def suspendable(self):
        return 0

    # For now, assume that Emacs will not be able to notify of suspension.
    # Later on, see if there are hooks in Emacs allowing such notification.
    def suspend_notification(self):
        return 0
        
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

        
        
        
