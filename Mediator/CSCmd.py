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
# (C) 2000, National Research Council of Canada
#
##############################################################################

import sys

from Object import Object
from debug import trace


class CSCmd(Object):
    """Class for Context Sensitive Commands (CSCs).

    A CSC is a phrase which, when uttered into an application, may
    fire a particular action.
    
    A CSC may fire different actions depending on the context of the
    application where it was typed.
        
    **INSTANCE ATTRIBUTES**
        
    *STR spoken_forms=[]* -- list of alternatives ways that this
     command can be spoken out. 
    
    *meanings=*{* [Context] *: * [Action] *}* -- Dictionary of
    possible contextual meanings for this command. Key is a context
    and value is an action object to be fired if that context applies.

    CLASS ATTRIBUTES**
        
    *none* --

    .. [Context] file:///./Context.Context.html
    .. [Action] file:///./Action.Action.html"""
        
    def __init__(self, spoken_forms=[], meanings={}, docstring=None, **attrs):
        self.deep_construct(CSCmd,
                            {'spoken_forms': spoken_forms,\
                             'meanings': meanings},
                            attrs)

    def applies(self, app, preceding_symbol = 0):
        """test whether any of its contexts applies, and returns

        **INPUTS**

        [AppState] app is the application into which the command was spoken.

        BOOL *preceding_symbol* indicates if a symbol would be inserted
        at the current cursor position before the action corresponding
        to this context was executed.  

        **OUTPUTS**

        *meaning* -- meaning if a Context applies, return the (context,
        action) pair, otherwise None

        """
        
        #
        # Try each of the contextual meanings in turn until find one that
        # applies
        #
#        print '-- CSCmd.interpret: self.meanings=%s' % self.meanings
        for ameaning in self.meanings.items():
            cont, action = ameaning
            trace('CSCmd.interpret', 'cont=%s, cont.applies=%s, ameaning=%s, action=%s' % 
                                     (cont, cont.applies, ameaning, str(action)))
            if (cont == None or cont.applies(app, preceding_symbol)):
                trace('CSCmd.applies', 'this context applies')
                return ameaning

        return None


        if ameaning:
            cont, action = ameaning
            trace('CSCmd.interpret', 'ameaning=%s, cont=%s, action=%s' % 
                                     (ameaning, cont, action))
            action.log_execute(app, cont)
            applied = 1

        return applied

    def doc(self):
        """Returns the documentation for that CSC.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        return self.docstring
