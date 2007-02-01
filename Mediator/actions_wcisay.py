#############################################################################
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
# placing apart, for prevention of circular imports
from WhatCanISay import WhatCanISay
from actions_gen import Action

class ActionWhatCanISay(Action):
    """give what can I say info...
    
    **INSTANCE ATTRIBUTES**
        
    *none*
        
    CLASS ATTRIBUTES**
        
    *none* -- 
    
    Moves to instance of class WhatCanISay, written mainly by Quintijn Hoogenbooms
    This instance makes a current language aware overview of LSAs (and later) CSCs.
    The info is presented in HTML format and opened with webbrowser in the default browser.
    
    """

    def __init__(self, buff_name=None, **args_super):
        self.deep_construct(ActionWhatCanISay, \
                            {}, \
                                args_super, \
                            {})
                            
    def doc(self):
        return 'Give actual command info.';

    def execute(self, app, cont, state = None):
        """See [Action.execute] for details.
        
        .. [Action.execute] file:///./Action.Action.html#execute"""
        
        manager = app.current_manager()
        if manager:
            wciSay = WhatCanISay()
            wciSay.load_commands_from_interpreter(manager.interpreter(), app.language_name())
            wciSay.create_cmds()
            wciSay.show_cmds()


