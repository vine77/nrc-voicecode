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

import AppStateMessaging, SourceBuffEmacs

	
class AppStateEmacs(AppStateMessaging.AppStateMessaging):
    """Interface to the Emacs editor.
    """

    def __init__(self, **attrs):
        
        self.deep_construct(AppStateEmacs, 
                            {},
                            attrs, new_default = {'app_name': 'emacs'})

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
#        
    def updates_from_app(self, what = None, exclude=1):        
        return []

    def config_from_external(self):
        pass
