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

from Object import Object
import debug

class SymbolResult(Object):
    """
    class representing a portion of an utterance translated as a
    new or existing symbol
    """
    def __init__(self, native_symbol, spoken_phrase, exact_matches,
                 as_inserted, buff_name,
                 builder_preferences, possible_matches = None,
                 forbidden = None,
                 new_symbol = 0, in_utter_interp = None, **args):
        """
        ** INPUTS **

        *STR native_symbol* -- the written form of the symbol

        *[STR] spoken_phrase* -- the list of spoken words which were
        translated into this symbol

        *STR buff_name* -- the name of the buffer in which the symbol
        was dictated

        *TextBlock as_inserted* -- the text as inserted  (possibly
        including leading or trailing spaces) and the range in the
        buffer this text occupied just after insertion
        
        *[STR] builder_preferences* -- list of names of
        registered SymBuilder objects, prioritized according to the
        state of the interpreter at the time the symbol was
        interpreted.

        *[STR] exact_matches* -- a prioritized list of exact matches
        to known symbols

        *BOOL new_symbol* -- true if the symbol was a new symbol,
        false if it matched an existing symbol
        
        *[(INT, STR)] possible_matches* -- list of (confidence score,
        written_form) tuples for possible (but not exact) matches to 
        the spoken form of this symbol.
        
        *[(INT, STR)] forbidden* -- list of (confidence score,
        written_form) tuples for forbidden inexact matches (but
        which may be displayed as alternatives in the exact symbols
        tab of the re-formatting dialog)
        
        *UtteranceInterpretation in_utter_interp = None* -- Utterance 
        interpretation in which that symbol was heard.
        
        *BOOL was_reformatted=false* -- indicates wheter or not that symbol result
        was reformatted by the user through a symbol reformatting dialog.
    
        *[STR] alternate_forms=[]* -- list of alternate formats for the symbol.
        These could be homophonic symbols, or different ways of formatting
        the same symbol.
        """
       
        self.deep_construct(SymbolResult,
                            {
                             'symbol': native_symbol,
                             'phrase': spoken_phrase,
                             'buff_name': buff_name, 
                             'text': as_inserted,
                             'builders': builder_preferences,
                             'exact': exact_matches,
                             'possible': possible_matches,
                             'forbidden': forbidden,
                             'was_new': new_symbol,
                             'in_utter_interp': in_utter_interp,
                             'was_reformatted': 0,
                             'alternate_forms': []
                            }, args)
       
                            
    def native_symbol(self):
        return self.symbol
    def buffer(self):
        return self.buff_name
    def final_range(self):
        return self.location
    def spoken_phrase(self):
        return self.phrase
    def builder_preferences(self):
        return self.builders

    def new_symbol(self):
        """
        Indicates whether the symbol was a newly generated symbol, or
        was a match to a previously known symbol
        """
        return self.was_new
        
    def exact_matches(self):
        """
        Returns a prioritized list of exact matches to known
        symbols

        **INPUTS**

        *none*

        **OUTPUTS**

        *[STR]* -- written forms of known symbols which are an exact
        match to the spoken form of this symbol
        """
        return self.exact
        
    def possible_matches(self):
        """
        Returns a prioritized list of possible (but not exact) matches
        to known symbols

        **INPUTS**

        *none*

        **OUTPUTS**

        *[(INT, STR)]* -- the confidence score and written forms of 
        possible matches, or None if none have been generated yet
        """
        return self.possible
    
    def forbidden_matches(self):
        """
        Returns a prioritized list of possible (but not exact) matches
        to known symbols

        **INPUTS**

        *none*

        **OUTPUTS**

        *[(INT, STR)]* -- the confidence score and written forms of 
        forbidden matches, or None if none have been generated yet
        """
        return self.forbidden
        
    def cleanup(self):
        self.in_utter_interp = None
