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

"""Classes for dealing with programming symbols and their spoken forms.
"""


from Object import Object
import sb_services, SourceBuff
from LangDef import LangDef
import auto_test, CmdInterp, PickledObject, sr_interface, vc_globals
import util
from debug import trace
import debug

import copy, cPickle, exceptions, os, re, string, sys
import stat
import time
import os.path
import shelve

import traceback

language_definitions={}

current_version = 1

#
# Minimum length for an abbreviation (short abbreviations tend to introduce
# too many false spoken forms, which bloats the SR's vocabulary)
#
min_abbreviation_len = 2

#
# Set *vocabulary_symbols_written_form* to 1 if you want VoiceCode to create a
# written form/spoken form entry in the SR vocabulary for every symbol it
# compiles.
# If set to 0, SR will create a spoken form entry only and the VoiceCode
# command interpreter will translate that spoken form to a written form
#
vocabulary_symbols_with_written_form = 1


#############################################################################
# Symbol formatting functions
#
# List of formatting functions for generating new native symbols from
# pseudo_symbols.
#
# Each formatting function must return a valid SymbolMatch object.
#
#############################################################################

symbol_formats = []

def fmt_lower_under(pseudo_symbol, words):
    """Format symbol as xxx_yyy_zzz.
    
    **INPUTS**

    *STR pseudo_symbol* -- Pseudo symbol to be formatted as a native symbol
    
    *[STR]* words -- Words in *pseudo_symbol* (to avoid redundant splitting)
    
    **OUTPUTS**
    
    *none* -- 
    """
    
    native_symbol = string.join(words, '_')
    native_symbol_match = SymbolMatch(pseudo_symbol=pseudo_symbol, native_symbol = native_symbol, words=words, word_matches=words, fmt_rank=1)
    
    return native_symbol_match
    
symbol_formats = symbol_formats + [fmt_lower_under]

def fmt_cap(pseudo_symbol, words):
    """Format symbol as XxxYxxZzz.
    
    **INPUTS**

    *STR pseudo_symbol* -- Pseudo symbol to be formatted as a native symbol
    
    *[STR]* words -- Words in *pseudo_symbol* (to avoid redundant splitting)
    
    **OUTPUTS**
    
    *none* -- 
    """

    native_symbol = ''
    for a_word in words:
        native_symbol = native_symbol + string.capitalize(a_word)
    return SymbolMatch(pseudo_symbol=pseudo_symbol, native_symbol = native_symbol, words=words, word_matches=words, fmt_rank=2)
    
symbol_formats = symbol_formats + [fmt_cap]


def fmt_lower_cap(pseudo_symbol, words):
    """Format symbol as xxxYyyZzz.
    
    **INPUTS**

    *STR pseudo_symbol* -- Pseudo symbol to be formatted as a native symbol
    
    *[STR]* words -- Words in *pseudo_symbol* (to avoid redundant splitting)
    
    **OUTPUTS**
    
    *none* -- 
    """

    native_symbol = string.lower(words[0])    
    if len(words) > 1:
        for a_word in words[1:]:
            native_symbol = native_symbol + string.capitalize(a_word)
    return SymbolMatch(pseudo_symbol=pseudo_symbol, native_symbol = native_symbol, words=words, word_matches=words, fmt_rank=3)
    
symbol_formats = symbol_formats + [fmt_lower_cap]


def fmt_upper_under(pseudo_symbol, words):
    """Format symbol as XXX_YYY_ZZZ
    
    **INPUTS**

    *STR pseudo_symbol* -- Pseudo symbol to be formatted as a native symbol
    
    *[STR]* words -- Words in *pseudo_symbol* (to avoid redundant splitting)
    
    **OUTPUTS**
    
    *none* -- 
    """

    for ii in range(len(words)):
        words[ii] = string.upper(words[ii])
    native_symbol = string.join(words, '_')
    return SymbolMatch(pseudo_symbol=pseudo_symbol, native_symbol = native_symbol, words=words, word_matches=words, fmt_rank=4)
    
symbol_formats = symbol_formats + [fmt_upper_under]
    
    

def fmt_join(pseudo_symbol, words):
    """Format symbol as xxxyyyzzz
    
    **INPUTS**

    *STR pseudo_symbol* -- Pseudo symbol to be formatted as a native symbol
    
    *[STR]* words -- Words in *pseudo_symbol* (to avoid redundant splitting)
    
    **OUTPUTS**
    
    *none* -- 
    """

    lower_words = []
    for a_word in words: lower_words = lower_words + [string.lower(a_word)]
    native_symbol = string.join(lower_words, '')
    return SymbolMatch(pseudo_symbol=pseudo_symbol, native_symbol = native_symbol, words=words, word_matches=words, fmt_rank=5)
    
symbol_formats = symbol_formats + [fmt_join]


def fmt_upper_join(pseudo_symbol, words):
    """Format symbol as XXXYYYZZZ
    
    **INPUTS**

    *STR pseudo_symbol* -- Pseudo symbol to be formatted as a native symbol
    
    *[STR]* words -- Words in *pseudo_symbol* (to avoid redundant splitting)
    
    **OUTPUTS**
    
    *none* -- 
    """

    for ii in range(len(words)):
        words[ii] = string.upper(words[ii])
    native_symbol = string.join(words, '')
    return SymbolMatch(pseudo_symbol=pseudo_symbol, native_symbol = native_symbol, words=words, word_matches=words, fmt_rank=6)
    
symbol_formats = symbol_formats + [fmt_upper_join]


#############################################################################
# End of symbol formatting functions
#############################################################################

def pluralize(word):
    """Finds the plural form of a word
        
    **INPUTS**
        
    *STR* word -- the word to be pluralized 
        

    **OUTPUTS**
        
    *STR plural* -- plural of *word*
    """        
    #
    # For now, just append an 's'
    #
    return word + 's'



class SymbolInfo(Object):
    """Stores information about a parsed symbol.
    
    **INSTANCE ATTRIBUTES**
    
    *[STR] spoken_forms=[]* -- list of spoken forms for that symbol.

    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, spoken_forms=[], **attrs):
        self.deep_construct(SymbolInfo, \
                            {'spoken_forms': spoken_forms}, \
                            attrs, \
                            {})
class SpokenFormInfo(Object):
    """Stores information about a spoken form for a parsed symbol.
    
    **INSTANCE ATTRIBUTES**
                        
    *[STR] symbols=[]* -- list of symbols (written forms) that have
    this spoken form.
    
    CLASS ATTRIBUTES**
            
    *none* -- 
    """
            
    def __init__(self, symbols=[], **attrs):
        self.deep_construct(SpokenFormInfo, \
                            {'symbols': symbols}, \
                            attrs, \
                            {})

class SymbolMatch(Object):
    
    """Encapsulates information about a match between a pseudo-symbol
    and a native symbol.
            
    **INSTANCE ATTRIBUTES**
            
    *STR pseudo_symbol=None* -- The pseudo symbol (e.g. "a new symbol")
    
    *STR native_symbol=None* -- The matched native symbol (e.g. aNewSym)

    *STR words=None* --  The words in *pseudo_symbol*

    *BOOL is_new=0* -- If true, then the symbol is a new one

    *NUM fmt_rank=10* -- For new symbol, this gives the match's rank in
     the list of possible forms for the new symbol
    
    *{STR: STR} word_matches=None* -- Keys are words of
     *pseudo_symbol* and vallues are the matching segment in
     *native_symbol*.

    CLASS ATTRIBUTES**
            
    *none* -- 
    """
    
    def __init__(self, pseudo_symbol=None, native_symbol=None, words=None, word_matches=None, is_new=0, fmt_rank=10, **args_super):
        self.deep_construct(SymbolMatch, \
                            {'pseudo_symbol': pseudo_symbol, \
                             'native_symbol': native_symbol, \
                             'words': words, \
                            'word_matches': word_matches, \
                             'is_new': is_new, \
                             'fmt_rank': fmt_rank}, \
                            args_super, \
                            {})



    def score(self):
        """Returns a score for the match.
        
        **INPUTS**
        
        *none* -- 
        
        **OUTPUTS**
        
        *INT score* -- The score takes into account things like:
        - the likelyhood of the abbreviations (presumably) used in *native_symbol* (not implemented yet)
        - the length of *native_symbol*
        """
                         
        if self.is_new:
            #
            # For matches to new symbols, score depends on the rank of the
            # format used to create the symbol
            #
            # Note use of float to force float division (as opposed to integer
            # div)
            #
            score = float(1)/self.fmt_rank
        else:
            #
            # For matches to existing symbols, just base score on lenght of
            # the native symbol for now
            #
            score = len(self.native_symbol)

        return score

    

    def compare_scores(self, other_match):
        """Compares the score of a match to that of an other match.

        Note that since the first argument is *self*, this method can
        be passedas a comparison method to *LIST.sort* method.
        
        **INPUTS**
        
        *[SymbolMatch]* other_match -- The other match to compare *self* to.
        

        **OUTPUTS**
        
        *INT* compare_flag -- -1 -> *self* has lower score
                               0 -> *self* has same score
                               1 -> *self* has higher score
        """

        self_score = self.score()
        other_score = other_match.score()
        if self_score < other_score:
            compare_flag = -1
        elif self_score > other_score:
            compare_flag = 1
        else:
            compare_flag = 0

        return compare_flag



class SymDict(Object):
    """Known symbols dictionary.

    This class stores information about symbols defined in source files
    that the user is working on.

    It has methods for parsing symbols and adding pronounceable
    phrases for those symbols to the Speech Recognition system's vocabulary.

    Also has methods for matching a pseudo symbol to a native symbol
    (e.g. "a new symbol" -> aNewSym)

    **INSTANCE ATTRIBUTES**

    *{STR:* [SymbolInfo] *)}* symbol_info={} -- Dictionary of known
     symbols. Key is the native written form of the symbol and the
     value is the information about that symbol.

    *{STR:* [SpokenFormInfo] *}* spoken_form_info={} -- Dictionary of
     resolved spoken forms for known symbols. The key is a resolved
     spoken form and the value is the list of written native symbols
     with that spoken form.

    *{STR: [STR]}* abbreviations -- Dictionary of preferred
     abbreviations for words.  The key is the word, and the value is a
     prioritized list of abbreviations

    *{STR: [STR]}* alt_abbreviations -- Dictionary of alternative
     abbreviations to be used as additional suggestions in the sing
     symbol reformatting dialog, but not as the first choice in initial
     dictation of new symbols.  The key is the word, and the value is a
     prioritized list of abbreviations.  The inverse of this mapping is 
     also used to generate expansions for abbreviations in symbols 
     scanned from existing code.  In fact, that is the primary purpose
     of the alternative abbreviations, but they are stored in the
     inverse form because the order of abbreviations for a given word is
     significant in the reformatting dialog, whereas the order of
     expansions for a given abbreviations is not.

    *{STR: [STR]}* expansions={} -- Dictionary of
     expansions of abbreviations. The key is the abbreviation and 
     the value is a list of possible expansions. It contains both 
     resolved and unresolved abbreviations.  This dictionary is
     generated by inverting abbreviations and alt_abbreviations.

    *{STR: {STR: 1}}* unresolved_abbreviations={} -- Dictionary of
     unresolved abbreviations. These are abbreviations that have
     appeared in at least one compiled symbol, yet are neither a word
     in the speech vocabulary or a known abbreviation. Values are
     dictionnaries that list the symbols containing the unresolved
     abbreviation.

    *STR* _cached_symbols_as_one_string='' -- Caches the last value
     returned by method [symbols_as_one_string]. A value of *None*
     indicates that the string needs to be regenerated by
     [symbols_as_one_string].

    *[STR] standard_symbol_sources* -- List of files in which standard
    symbols for different languages are defined.

    *[STR] abbrev_sources* -- List of files in which
    abbreviations and expansions for symbol terms are defined.

    *STR* sym_file = None -- Name of the file used to store those SymDict 
    attributes which should be persistent.  If *None*
    it means the object should never be saved to/read from file.

    *BOOL* from_file -- true if the symbol dictionary was successfully
    loaded from a file

    *INT* file_time -- if from_file is true, contains the time of last 
    modification of the symbol dictionary file (in seconds since the
    epoch, as returned by os.stat)

    [SB_ServiceLang] *lang_name_srv* -- Service used by SymDict to
    determine a buffer's programming language.

   
    CLASS ATTRIBUTES**

    *{STR: * [LangDef] *}* language_definitions={} -- Key is the name
     of a language and the value is a language definition object which
     defines rules for parsing symbols in that language.
        
    .. [LangDef] file:///./LangDef.LangDef.html
    .. [SymbolInfo] file:///./SymDict.SymbolInfo.html
    .. [SpokenFormInfo] file:///./SymDict.SpokenFormInfo.html
    .. [symbols_as_one_string] file:///./SymDict.SymDict.html#symbols_as_one_string"""

    def __init__(self, sym_file = None, 
                 **attrs):

        # These attributes can't be set at construction time
        self.decl_attrs({'_cached_symbols_as_one_string': '',
                         'spoken_form_info': {},
                         'symbol_info': {},
                         'abbreviations': {},
                         'alt_abbreviations': {},
                         'expansions': {},
                         'standard_symbol_sources': [],
                         'abbrev_sources': [],
                         'unresolved_abbreviations': {},
                         'lang_name_srv': sb_services.SB_ServiceLang(buff=None)})
        
        # These attributes CAN be set at construction time
        self.deep_construct(SymDict,
                            {'sym_file': sym_file,
                             'from_file': 0,
                             'file_time': None},
                            attrs)
        self.from_file = self.init_from_file()

#        print '-- SymDict.__init__: returning self.__dict__=%s' % self.__dict__


    def save(self, file = None):
        """save persistent attributes to a file

        **INPUTS**

        *STR file* -- name of the file, or None to use the sym_file name
        given at construction.  Normally, this argument should be
        omitted.  It is included only for regression testing of the
        persistence features of SymDict

        **OUTPUTS**

        *none*
        """
        if file is None:
            file = self.sym_file
        if file is None:
            return
        try:
            db = shelve.open(file, "n")
        except:
            msg = 'WARNING: error creating SymDict state file %s\n' % file
            sys.stderr.write(msg)
            return
            
        try:
            db['version'] = current_version
            db['symbol_info'] = self.symbol_info
# at the moment, spoken_form_info is redundant with symbol_info, except for 
# ordering, but I'm not sure that will always be true, or what to do 
# about ordering, so for now let's just store both
            db['spoken_form_info'] = self.spoken_form_info
            db['abbreviations'] = self.abbreviations
            db['alt_abbreviations'] = self.alt_abbreviations
            db['unresolved_abbreviations'] = self.unresolved_abbreviations
        except:
            msg = 'WARNING: error writing to SymDict state file %s\n' % file
            sys.stderr.write(msg)
            traceback.print_exc()
            db.close()
            os.remove(file)
            return

        db.close()

    def _add_corresponding_expansion(self, abbreviation, expansion):
        """private method to add expansions for an abbreviation corresponding 
        to the mapping a word to its abbreviation.  

        *NOTE:* This method should only be called by add_abbreviation,
        prepend_abbreviations, etc., because otherwise the expansion
        will be lost when the user exits VoiceCode

        **INPUTS**
        
        *STR* abbreviation -- the new abbreviations

        *STR* expansion -- the word which is an expansion of the
        abbreviation
        
        **OUTPUTS**

        *none*
        """
        if self.expansions.has_key(abbreviation):
            if expansion not in self.expansions[abbreviation]:
                self.expansions[abbreviation].append(expansion)
        else:
            self.expansions[abbreviation] = [expansion]
        if self.unresolved_abbreviations.has_key(abbreviation):
            trace('SymDict._add_corresponding_expansion', 
                    '%s was previously unresolved' % abbreviation)
            for a_symbol in self.unresolved_abbreviations[abbreviation].keys():
                trace('SymDict._add_corresponding_expansion', 
                    'updating forms for %s' % a_symbol)
                self.update_spoken_forms(a_symbol)
            del self.unresolved_abbreviations[abbreviation]

    def prepend_abbreviations(self, word, abbreviations):
        """prepends one or more abbreviations to the list of abbreviations 
        for a word, or moves them to the front of the list, if they is 
        already in the list.  Also creates corresponding entries
        in the list of expansions for each abbreviation.

        *NOTE:* this method should only be called if the user has
        explicitly requested import of a user abbreviation file with
        instructions that it should override existing preferences, or by
        the reformatting dialog in accordance with the user's choice

        **INPUTS**

        *STR* word -- the word to be abbreviated
        
        *[STR]* abbreviations -- list of new abbreviations
        
        **OUTPUTS**

        *none*
        """
        #
        # Make sure the word is the SR vocabulary
        #
        clean_word = sr_interface.clean_spoken_form(word)
        sr_interface.addWord(clean_word)
        if not self.abbreviations.has_key(word):
            self.abbreviations[word] = abbreviations
        else:
            for abbreviation in abbreviations:
                try:
                    self.abbreviations[word].remove(abbreviation)
                except ValueError:
                    pass
            self.abbreviations[word] = abbreviations + self.abbreviations[word]
        for abbreviation in abbreviations:
            self._add_corresponding_expansion(abbreviation, word)
       
    def add_abbreviation(self, word, abbreviation):
        """Appends an abbreviation to the list of abbreviations for a word, 
        unless it is already present, and creates a corresponding entry
        in the list of expansions for the abbreviation
        
        **INPUTS**

        *STR* word -- the word to be abbreviated
        
        *STR* abbreviation -- the abbreviation 
        
        **OUTPUTS**
        
        *none* -- 
        """
        clean_word = sr_interface.clean_spoken_form(word)
        sr_interface.addWord(clean_word)
        if not self.abbreviations.has_key(word):
            self.abbreviations[word] = [abbreviation]
        else:
            try:
                self.abbreviations[word].index(abbreviation)
            except ValueError:
                self.abbreviations[word].append(abbreviation)
        self._add_corresponding_expansion(abbreviation, word)

    def add_abbreviations(self, word, abbreviations):
        """Appends an abbreviation to the list of abbreviations for a word, 
        unless it is already present, and creates a corresponding entry
        in the list of expansions for the abbreviation
        
        **INPUTS**

        *STR* word -- the word to be abbreviated
        
        *[STR]* abbreviations -- list of abbreviations to add
        
        **OUTPUTS**
        
        *none* -- 
        """
        clean_word = sr_interface.clean_spoken_form(word)
        sr_interface.addWord(clean_word)
        if not self.abbreviations.has_key(word):
            self.abbreviations[word] = abbreviations
        else:
            for abbreviation in abbreviations:
                try:
                    self.abbreviations[word].index(abbreviation)
                except ValueError:
                    self.abbreviations[word].append(abbreviation)
        for abbreviation in abbreviations:
            self._add_corresponding_expansion(abbreviation, word)

    def add_alt_abbreviations(self, word, abbreviations):
        """Appends an abbreviation to the list of alternative abbreviations 
        for a word, unless it is already present, and creates a 
        corresponding entry in the list of expansions for the abbreviation
        
        **INPUTS**

        *STR* word -- the word to be abbreviated
        
        *[STR]* abbreviations -- list of abbreviations to add
        
        **OUTPUTS**
        
        *none* -- 
        """
        clean_word = sr_interface.clean_spoken_form(word)
        sr_interface.addWord(clean_word)
        if not self.alt_abbreviations.has_key(word):
            self.alt_abbreviations[word] = abbreviations
        else:
            for abbreviation in abbreviations:
                try:
                    self.alt_abbreviations[word].index(abbreviation)
                except ValueError:
                    self.alt_abbreviations[word].append(abbreviation)
        for abbreviation in abbreviations:
            self._add_corresponding_expansion(abbreviation, word)

    def symbols_as_one_string(self):
        """Returns a string that lists all the native known symbols.

        This string is used for matching pseudo-symbols to known
        native symbols, because it's much faster than looping through
        keys of *symbol_info*.

        To avoid regenerating this string everytime, the last value
        returned is cached in [self._cached_symbols_as_one_string]
        
        **INPUTS**
        
        *none* -- 
        
        **OUTPUTS**
        
        *none* --

        .. [self._cached_symbols_as_one_string] file:///./SymDict.SymDict.html
        """
        
        if self._cached_symbols_as_one_string == None:
            #
            # Cached value has become stale. Regenerate it.
            #
            self._cached_symbols_as_one_string = ''
            symbol_list = self.symbol_info.keys()
            symbol_list.sort()            
            for a_symbol in symbol_list:
                #
                # Note: symbols must be separated by two spaces because
                #       re.findall only returns non-overlapping matches.
                #       But since the regexp used for symbol matching requires
                #       that there be a space before and after the symbol,
                #       if two matching symbols were consecutive in
                #       _cached_symbols_as_one_string, and were separated by
                #       a single space, only the first symbol would be matched
                #
                self._cached_symbols_as_one_string = self._cached_symbols_as_one_string + ' ' + a_symbol + ' '

#        self.save()

        return self._cached_symbols_as_one_string

    def print_symbols(self, symbols = None):
        """Print the content of the symbols dictionary.
        
        **INPUTS**

        *[STR] symbols* -- list of symbols to print, or None to print
        the whole dictionary
        
        **OUTPUTS**
        
        *none* -- 
        """
        if symbols:
            the_symbols = symbols
        else:
            the_symbols = self.symbol_info.keys()
            the_symbols.sort()        
        for a_symbol in the_symbols:
            try:
                a_symbol_info = self.symbol_info[a_symbol]
                forms = copy.copy(a_symbol_info.spoken_forms)
                forms.sort()
                print '%s: %s' % (a_symbol, str(forms))
            except KeyError:
                print '%s: undefined' % a_symbol

        if symbols is None:
            print '_cached_symbols_as_one_string is:\n   %s' % self._cached_symbols_as_one_string

    def print_abbreviations(self, show_unresolved=0):
        """Prints the known and unresolved abbreviations."""

        print 'List of abbreviations\n'
        sorted_abbreviations = self.expansions.keys()
        sorted_abbreviations.sort()
        for an_abbreviation in sorted_abbreviations:
            sorted_expansions = copy.copy(self.expansions[an_abbreviation])
            sorted_expansions.sort()
            print '\'%s\' expands to %s' % (an_abbreviation, sorted_expansions)

        if show_unresolved:
            print '\n\nList of unresolved abbreviations\n'
            sorted_unresolved = self.unresolved_abbreviations.keys()
            sorted_unresolved.sort(lambda x, y: len(x) > len(y) or (len(x) == len(y) and x < y))
            for an_abbreviation in sorted_unresolved:
                symbol_list = self.unresolved_abbreviations[an_abbreviation].keys()
                symbol_list.sort()
                print '\'%s\': appears in %s' % (an_abbreviation, str(symbol_list))


    def peek_at_unresolved(self):
        """returns a reference to the dictionary of unresolved abbreviations
        and the symbols containing those abbreviations.

        **NOTE:** This method is intended only for diagnostic testing
        purpose.  The caller must not modify the dictionary returned

        **INPUTS**

        *none*

        **OUTPUTS**

        *{STR: {STR: 1}}* unresolved_abbreviations={} -- Dictionary of
        unresolved abbreviations. These are abbreviations that have
        appeared in at least one compiled symbol, yet are neither a word
        in the speech vocabulary or a known abbreviation. Values are
        dictionnaries that list the symbols containing the unresolved
        abbreviation.
        """
        return self.unresolved_abbreviations

    def changed_since_sym_file(self, path):
        """indicates whether the file with the given path has changed
        since the last change to the persistent symbol dictionary file
        from which this SymDict was restored. 

        **INPUTS**

        *STR path* -- the path to the file to check

        **OUTPUTS**

        *BOOL* -- true if the file has changed more recently than the
        persistent symbol dictionary file, or if this SymDict instance
        was not initialized from a persisten symbol dictionary
        """
        if self.from_file and util.last_mod(path) <= self.file_time:
            return 0
        return 1

    def abbrev_config(self):
        """Parse standard symbols for the various programming languages.
        
        **INPUTS**
        
        *none* 
        
        **OUTPUTS**
        
        *none* 
        """
        existing = []
        for file in self.abbrev_sources:
            if os.path.exists(file):
                existing.append(file)

        if self.from_file:
            files = []
            for file in existing:
                if self.changed_since_sym_file(file):
                    files.append(file)
        else:
            files = existing

        if not files:
            return
        names = {}
        names['add_abbreviation'] = self.add_abbreviation
        names['add_abbreviations'] = self.add_abbreviations
        names['add_alt_abbreviations'] = self.add_alt_abbreviations
        for file in files:
            try:
                execfile(file, names)
            except:
                traceback.print_exc(file = sys.stderr)
    
    def finish_config(self):
        """Finish performing those parts of the SymDict
        configuration which can't take place until after the VoiceCode
        configuration files have been executed
        
        **INPUTS**

        *none*
        
        **OUTPUTS**
        
        *none*
        """
        self.abbrev_config()
        self.maybe_parse_standard_symbols()
# mark this user so we don't have to scan the symbol files every time
        sr_interface.mark_user()

    def maybe_parse_standard_symbols(self):
        """Parse standard symbols for the various programming languages,
        but only if this is a fresh VoiceCode user, or if the files 
        have changed more recently than the persistent symbol dictionary
        file

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        existing = []
        for file in self.standard_symbol_sources:
            if os.path.exists(file):
                existing.append(file)

#        print 'existing files:', existing
#        print 'from_file = ', self.from_file
#        print 'marked = ', sr_interface.is_user_marked()
        if self.from_file and sr_interface.is_user_marked():
            files = []
            for file in existing:
                if self.changed_since_sym_file(file):
                    files.append(file)
#            print 'changed files:', files
        else:
            files = existing
#            print 'all existing files:', files

        if files:
            self.parse_symbols_from_files(files)

    def parse_standard_symbols(self):
        """Parse standard symbols for the various programming languages.
        
        **INPUTS**
        
        *none* 
        
        **OUTPUTS**
        
        *none* 
        """
        self.parse_symbols_from_files(self.standard_symbol_sources)
    
    def parse_symbols_from_files(self, file_list, add_sr_entries=1):
        """Parse symbols from a series of source files

        **INPUTS**

        *[STR] file_list -- List of files to be compiled

        *BOOL* add_sr_entries = 1 -- If true, add symbols to the SR vocabulary

        **OUTPUT**

        *none* --
        """

#        print '-- SymDict.parse_symbols_from_files: file_list=%s' % file_list
#        debug.print_call_stack()
        for a_file in file_list:
            print 'Compiling symbols for file \'%s\'' \
                % util.within_VCode(a_file)
            self.parse_symbols_from_file(a_file, add_sr_entries=add_sr_entries)
            
        #
        # Save dictionary to file
        #
        self.save()

#        print '-- SymDict.parse_symbols_from_files: symbols are:'; self.print_symbols()                    

    def parse_symbols_from_file(self, file_name, add_sr_entries=1):
        """Parse symbols from a source file.

        *STR* file_name -- The path of the file.

        *BOOL* add_sr_entries = 1 -- If true, add symbols to the SR vocabulary
        
        Parsed symbols are stored in the *symbol_info* and
        *spoken_forms2symbol* attributes.
        """

#        print '-- SymDict.parse_symbols: file_name=%s' % file_name
        try:
            source_file = open(file_name, 'r')
        except Exception:
            #
            # If the file doesn't exist, we just do nothing
            #
            print 'WARNING: source file \'%s\' doesn\'t exist.' % file_name
        else:
            source = source_file.read()
            
#            print '-- SymDict.parse_symbols: \n*** START OF SOURCE ***\n%s\n*** END OF SOURCE ***' % source

            language_name = self.get_language_by_filename(file_name)
#            print '-- SymDict.parse_symbols: language_name=%s' % language_name
            self.parse_symbols(source, language_name, 
                add_sr_entries = add_sr_entries)
                
    def parse_symbols(self, contents, language_name, add_sr_entries=1):
        """Parse symbols from a string representing the contents of a 
        source file.

        *STR* contents -- the contents of the source file

        *STR* language_name -- the name of the language of the source
        file

        *BOOL* add_sr_entries = 1 -- If true, add symbols to the SR vocabulary
        
        Parsed symbols are stored in the *symbol_info* and
        *spoken_forms2symbol* attributes.
        """

#            print '-- SymDict.parse_symbols: \n*** START OF SOURCE ***\n%s\n*** END OF SOURCE ***' % source

        language_definition = self.get_language_definition(language_name)
#            print '-- SymDict.parse_symbols: language_definition.name=%s' % language_definition.name
        stripped_contents = self.strip_source(contents, language_definition)

            #
            # Parse symbols from the first chunk
            #
        while stripped_contents != '':
            a_match = re.search('(' + \
                language_definition.regexp_symbol + ')', stripped_contents)
            if a_match:
                self.add_symbol(a_match.group(1), 
                    add_sr_entries=add_sr_entries)
                stripped_contents = stripped_contents[a_match.end()+1:]
            else:
                stripped_contents = ''
                
    def strip_source(self, source, language_definition):
        """Removes all parts of a source file that don't contain symbols.

        This includes comments and quoted strings.
        
        **INPUTS**
        
        *STR* source -- the source

        *BOOL* add_sr_entries = 1 -- If true, add symbols to the SR vocabulary.

        [LangDef] language_definition -- the definition of the
        language that *source* is written in.
        

        **OUTPUTS**
        
        *STR* stripped_source -- source stripped of all non-symbols chunks

        .. [LangDef] file:///./LangDef.LangDef.html"""

#        print '-- SymDict.strip_source: source=\n%s\n*** End of source' % source
        stripped_source = ''
        while source != '':
            #
            # Identify earliest chunk of code that doesn't contain any symbols
            #
            non_symbol_start = None
            non_symbol_end = None
            for a_regexp in language_definition.regexps_no_symbols:
#                print '-- SymDict.strip_source: trying to strip regexp: %s ' % a_regexp
                a_match = re.search(a_regexp, source)
                if a_match:
#                    print '-- SymDict.strip_source: we have a match for that regexp'
                    if non_symbol_start == None or a_match.start() < non_symbol_start:
                        non_symbol_start = a_match.start()
                        non_symbol_end = a_match.end()
#                        print '-- SymDict.strip_source: updated non_symbol_start=%s, non_symbol_end=%s' % (non_symbol_start, non_symbol_end)                        

            #
            # Rip that part of the code out
            #
            if non_symbol_start != None:
#                print '-- SymDict.strip_source: stripping following text\n%s\n*** End of stripped text' % source[non_symbol_start:non_symbol_end]                
                stripped_source = stripped_source + source[0:non_symbol_start]
                source = source[non_symbol_end:]
            else:
                stripped_source = stripped_source + source
                source = ''
                
        return stripped_source
                                

    def standard_symbols_in(self, file_list):
        """Specify source files defining standard symbols"""
        for a_file in file_list:
            if not a_file in self.standard_symbol_sources:
                self.standard_symbol_sources.append(a_file)

    def abbreviations_in(self, file_list):
        """Specify source files defining expansions and abbreviations"""
        for a_file in file_list:
            if not a_file in self.abbrev_sources:
                self.abbrev_sources.append(a_file)

    def add_symbol(self, symbol, user_supplied_spoken_forms=[], \
                   add_sr_entries=1):
        """Add a symbol to the dictionary

        **INPUTS**
        
        *STR* symbol -- Symbol to add

        *BOOL* add_sr_entries = 1 -- If true, adds symbol to the SR vocabulary.

        *[STR] user_supplied_spoken_forms* -- Spoken forms for the
         symbol which were supplied explicitly by the user. These
         forms are added even if they are not generated automaticly by
         [update_spoken_forms]. This is useful in cases where the user
         has explicitly supplied spoken forms for a symbol that contains very
         short abbreviations (i.e. abbreviations that are rejected by
         [add_abbreviation]). In such cases, the spoken form wouldn't
         automaticaly be generated by [updated_spoken_forms] and must
         therefore be added explictely by add_symbol.
        
        **OUTPUTS**
        
        *none* -- 

        .. [update_spoken_forms] file:///./SymDict.SymDict.html#update_spoken_forms
        .. [add_abbreviation] file:///./SymDict.SymDict.html#add_abbreviation"""
        
#        print '-- SymDict.add_symbol: symbol=%s' % symbol
            
        if not self.symbol_info.has_key(symbol):
            
            trace('SymDict.add_symbol', 'new symbol=%s' % symbol)
#            print '-- SymDict.add_symbol: this is a new symbol'

            #
            # Add the symbol to the string used for symbol matching
            #
            new_string_entry = ' %s ' % symbol
            if self._cached_symbols_as_one_string == None:
                self._cached_symbols_as_one_string = new_string_entry
            else:
                self._cached_symbols_as_one_string = self._cached_symbols_as_one_string + new_string_entry

            #
            # Add an entry to the symbol dictionary
            #
            self.symbol_info[symbol] = SymbolInfo()
                
            #
            # Update the symbol's spoken forms.
            #
            self.update_spoken_forms(symbol, add_sr_entries=add_sr_entries)

            #
            # Add user supplied spoken forms
            #
            for a_spoken_form in user_supplied_spoken_forms:
                if not a_spoken_form in self.symbol_info[symbol].spoken_forms:
                    self.symbol_info[symbol].spoken_forms = self.symbol_info[symbol].spoken_forms + [a_spoken_form]

            trace('SymDict.add_symbol', 'new symbol spoken forms = %s' %
                self.symbol_info[symbol].spoken_forms)
            

    def update_spoken_forms(self, symbol, add_sr_entries=1):
        """Updates the spoken forms of a native symbol.

        **INPUTS**
        
        *STR* symbol -- Native symbol for which we want to update the
         spoken forms.

         *BOOL* add_sr_entries = 1 -- If true, add written\spoken
          symbols to the SR vocabulary.

        **OUTPUTS**
        
        *none* -- 
        """

        global vocabulary_symbols_with_written_form

        trace('SymDict.update_spoken_forms', 'symbol="%s"' % symbol)
        
        #
        # Get the symbol's spoken forms
        #

        forms_this_symbol = self.get_spoken_forms(symbol)
        trace('SymDict.update_spoken_forms', 'spoken forms originally are:"%s"\nforms_this_symbol=%s' % (self.symbol_info[symbol].spoken_forms, forms_this_symbol))
        self.symbol_info[symbol].spoken_forms = forms_this_symbol
           
        #
        # Store information about the symbol and its spoken forms
        #
        for a_form in forms_this_symbol:
            if self.spoken_form_info.has_key(a_form):
                self.spoken_form_info[a_form].symbols = self.spoken_form_info[a_form].symbols + [symbol]
            else:
                self.spoken_form_info[a_form] = SpokenFormInfo(symbols=[symbol])
            #
            # Add spoken form to NatSpeak's vocab if not already there.
            #
            # Note: If the spoken form is a single word, we don't
            #       add it because it might be an unresolved
            #       abbreviation.
            #
            #       This abbreviation would not be removed upon exit
            #       of VoiceCode because it's undistinguishable from
            #       words that have been added by the real NatSpeak
            #       Vocabulary Builder.
            #
            #       So the next time we start VoiceCode and compile a
            #       symbol that contains that abbreviation, the
            #       abbreviation would not be logged as unresolved
            #       (because it would correspond to an in-vocabulary
            #       word)
            #
            if len(re.split('\s+', a_form)) > 1:
                if vocabulary_symbols_with_written_form:
                    #
                    # Add the vocabulary entry as a written\\spoken
                    # form
                    #
                    entry = sr_interface.vocabulary_entry(a_form, symbol)
                else:
                    #
                    # Add just the spoken form entry
                    #
                    entry = sr_interface.vocabulary_entry(a_form)
                    
                if add_sr_entries: sr_interface.addWord(entry)        

    def get_spoken_forms(self, symbol):
        """Returns a list of possible spoken forms for a symbol.
        
        **INPUTS**
        
        *STR* symbol -- the symbol in question 
        

        **OUTPUTS**
        
        *[STR]* -- returns a list of spoken forms
        """

#        print '-- SymDict.get_spoken_forms: symbol=%s, abbreviations:' % symbol; self.print_abbreviations()

        
        #
        # First, split the symbol into words or abbreviations
        #
        mod_symbol = symbol
               # Replace non alphanums by space
        mod_symbol = re.sub('[^a-zA-Z0-9]+', ' ', mod_symbol)
#        print '-- SymDict.get_spoken: after 1st sub, mod_symbol=\'%s\'' % mod_symbol
               # Split before and after string of numbers
        mod_symbol = re.sub('([0-9]+)', ' \\1 ', mod_symbol)

               # Split when there is a change of case. Must distinguish between
               # the following cases:
               #    'XXXyyy'   -> 'XX Xyyy'
               #    'xxxYYY'   -> 'xxx YYY'               
        mod_symbol = re.sub('([A-Z]+?)([A-Z][a-z]+)', '\\1 \\2', mod_symbol)
#        print '-- SymDict.get_spoken: after 1st sub, mod_symbol=\'%s\'' % mod_symbol                
        mod_symbol = re.sub('([a-z]+)([A-Z]+)', '\\1 \\2', mod_symbol)
#        print '-- SymDict.get_spoken: after 2nd sub, mod_symbol=\'%s\'' % mod_symbol        
               # Remove leading/trailing spaces
        mod_symbol = re.sub('(^\s+|\s+$)', '', mod_symbol)
#        print '-- SymDict.get_spoken: after 3rd sub, mod_symbol=\'%s\'' % mod_symbol
        mod_symbol = string.lower(mod_symbol)
        words = re.split('\s+', mod_symbol)
        

#        print '-- SymDict.get_spoken: mod_symbol=\'%s\', words=%s' % (mod_symbol, str(words))
        #
        # Replace each abbreviated word by its possible expansion
        #
        possibilities = []
        for a_word in words:
            possibilities = possibilities + [self.expand_word(a_word, symbol)]
#        print '-- SymDict.get_spoken_forms: possibilities=%s' % possibilities

        #
        # Generate all possible spoken forms for that symbol
        #
        the_spoken_forms = self.expand_possible_forms([''], possibilities)
#        print '-- SymDict.get_spoken_forms: the_spoken_forms=%s' % the_spoken_forms        
        return the_spoken_forms



    def expand_word(self, word, symbol):
        """Expands a word from a symbol to its possible spoken forms.

        If *word* is an in-vocabulary word simply returns *[word]*

        If it's a known abbreviation returns the list of possible expansions
        for that abbreviation or the list of their plural forms.

        If it's the plural of a known abbreviation, returns the plural
        form of the abbreviation's expansions.

        Otherwise, it tries to split *word* into substrings that are
        in-vocabulary words or known abbreviations (*NOT IMPLEMENTED
        AT THE MOMENT).

        If that doesn't work either logs *word* in
        *self.unresolved_abbreviations* and log *symbol* as one of the symbol
        where it occured.
        
        **INPUTS**
        
        *STR* abbreviation -- Abbreviation to be expanded 
        
        *STR* symbol -- Symbol in which the word appeared
        
        **OUTPUTS**
        
        *[STR] expansions * -- list of possible expansions of the word.
        """
        
#        print '-- SymDict.expand_word: expanding word: \'%s\'' % word

        #
        # Check if word might be a pluralised word
        #
        word_length = len(word)
        if word_length and word[word_length-1] == 's':
            single_form = word[0:word_length-1]
        else:
            single_form = word
        
        expansions = [word]
        if self.expansions.has_key(word):
            #
            # word is a known abbreviation. Add expansions.
            #
            expansions = expansions + self.expansions[word]            
        elif self.expansions.has_key(single_form):
            #
            # word is the plural of an abbreviation
            #
            expansions = map(lambda an_expansion: pluralize(an_expansion), self.expansions[single_form])
        else:
            #
            # Word is not a known abbreviation nor plural of a known
            # abbreviation
            # Check if this is an unresolved abbreviation
            # (note: flag=4 means case unsensitive)
            #
            if sr_interface.getWordInfo(word, 4) == None:
#                print '-- SymDict.expand_word: word is not a known abbreviation. Adding it to unresolved abbreviations'                
                if self.unresolved_abbreviations.has_key(word):
                    self.unresolved_abbreviations[word][symbol] = 1
                else:
                    self.unresolved_abbreviations[word] = {symbol: 1}

#        print '-- SymDict.expand_word: returning expansions=%s' % expansions
        return expansions 



    def expand_possible_forms(self, partial_forms, further_extensions):
        """Returns a list of possible spoken forms for a symbol.
        
        **INPUTS**
        
        *[STR]* partial_forms -- a list of partially completed spoken
         forms. 

        *[[STR]]* further_extensions -- a list of possibilities for
         further extending the spoken forms in *partal_forms*.
        

        **OUTPUTS**
        
        *[STR]* -- List of all possible spoken forms for the symbol.
        
        """
#        print '-- SymDict.expand_possible_forms: partial_forms=%s, further_extensions=%s' % (partial_forms, further_extensions)
        if len(further_extensions) == 0:
            return partial_forms
        else:            
            #
            # There are more possible extensions
            #
            # Extend each partial expansion by one level, then call
            # expand_possible_forms recursively
            #
            next_extensions = further_extensions[0]
            if len(further_extensions) > 1:
                further_extensions = further_extensions[1:]
            else:
                further_extensions = []

#            print '-- SymDict.expand_possible_forms: next_extensions=%s' % next_extensions
            extended_partial_forms = []            
            for a_partial_form in partial_forms:
                for an_extension in next_extensions:
#                    print '-- SymDict.expand_possible_forms: a_partial_form=%s, an_extension=%s' % (a_partial_form, an_extension)
                    if a_partial_form == '':
                        an_extended_partial_form = an_extension
                    else:
                        an_extended_partial_form = a_partial_form + ' ' + an_extension
                    extended_partial_forms = extended_partial_forms + [an_extended_partial_form]

#            print '-- SymDict.expand_possible_forms: further_extensions=%s' % further_extensions
            expanded_forms = self.expand_possible_forms(extended_partial_forms , further_extensions)
                    
            return expanded_forms
            
    def get_language_by_filename(self, file_name):
        """Gets the name of the language associated with a source file.
        
        **INPUTS**
        
        *STR* file_name -- name of the file 
        

        **OUTPUTS**
        
        *STR* -- name of the language.  Returns *None* if there doesn'
        t exist a proper language definition, or if can't tell what 
        language the source file is written in.

        """

        language_name = self.lang_name_srv.file_language_name(file_name)
        return language_name

            
    def get_language_definition_by_filename(self, file_name):
        """Gets the definition of the language associated with a source file.
        
        **INPUTS**
        
        *STR* file_name -- name of the file 
        

        **OUTPUTS**
        
        [LangDef] -- definition of the language *file_name* is written
        in. Returns *None* if there doesn't exist a proper language
        definition, or if can't tell what language the source file is
        written in.

        ..[LangDef] file:///./LangDef.LangDef.html"""

        global language_definitions
        definition = None
        
        language_name = self.get_language_by_filename(file_name)
        return self.get_language_definition(language_name)

    def get_language_definition(self, language_name):
        """Gets the definition of the language associated with a source file.
        
        **INPUTS**
        
        *STR* file_name -- name of the file 
        

        **OUTPUTS**
        
        [LangDef] -- definition of the language *file_name* is written
        in. Returns *None* if there doesn't exist a proper language
        definition, or if can't tell what language the source file is
        written in.

        ..[LangDef] file:///./LangDef.LangDef.html"""

        global language_definitions
        definition = None
        
#        print '-- SymDict.get_language_definition: language_definitions=%s, language_name=%s' % (language_definitions, language_name)
        if language_definitions.has_key(language_name):
            definition = language_definitions[language_name]
        return definition



    def match_pseudo_symbol(self, pseudo_symbol):        
        """Returns a prioritized list of all known native symbols that
        match a given pseudo symbol.
        
        **INPUTS**
        
        *STR* pseudo_symbol -- The pseudo symbol to be matched. 
        

        **OUTPUTS**
        
        *[* [SymbolMatch] *]* -- Prioritized list of symbol matches.

        
        .. [SymbolMatch] file:///./SymDict.SymbolMatch.html"""

#        print '-- SymDict.match_pseudo_symbol: pseudo_symbol=\'%s\'' % pseudo_symbol

        #
        # Find all known native symbols that match *pseudo_symbol*
        #
        all_symbols = self.symbols_as_one_string()

        #
        # Remove leading/trailing blanks
        #
        pseudo_symbol = re.sub('(^\s+|\s+$)', '', pseudo_symbol)
#        words = re.split('\s+', pseudo_symbol)
        words = re.split('[^a-zA-Z0-9]+', pseudo_symbol)

        #
        # Remove empty words in case pseudo_symbol starts or ends with
        # non-alphanums
        #
        if len(words) > 0 and words[0] == '':
            words = words[1:]
        if len(words) > 0 and words[len(words)-1] == '':
            words = words[:len(words)-1]

            
#        print '-- SymDict.match_pseudo_symbols: words=%s' % words        
        regexp = self.reg_pseudo_to_native_symbol(words)

#        print '-- SymDict.match_pseudo_symbol: regexp=%s, all_symbols=\'%s\'' % (regexp.__dict__, all_symbols)
        
        raw_matches = regexp.findall(all_symbols)

#        print '-- SymDict.match_pseudo_symbol: raw_matches = %s' % raw_matches

        #
        # Create a list of matches to known symbols
        #
        matches = []
        for a_match in raw_matches:
            matches = matches + [SymbolMatch(pseudo_symbol=pseudo_symbol, native_symbol=a_match[0], words=words, word_matches=a_match[1:])]


        #
        # Add list of possible new symbols
        #
        matches = matches + self.format_as_symbol(pseudo_symbol, words)

        #
        # Sort the list of matches according to their scores
        #
        matches.sort(SymbolMatch.compare_scores)
        matches.reverse()

        #
        # Remove duplicate entries (in some cases, different formatting
        # functions for new symbol may yield same result)
        #
        ii = 0
        previous_matches = {}
        while ii < len(matches):
            a_match = matches[ii].native_symbol
            if previous_matches.has_key(a_match):
                if ii + 1 < len(matches):
                    matches = matches[:ii] + matches[ii+1:]
                else:
                    matches = matches[:ii]
            else:
                ii = ii + 1
            previous_matches[a_match] = 1
        return matches


    

    def format_as_symbol(self, pseudo_symbol, words):
        
        """Returns a list of alternative ways to format a pseudo
        symbol as a new native symbol.
        
        **INPUTS**
        
        *STR* pseudo_symbol -- Pseudo symbol to be formatted

        *[STR] words -- Words in *pseudo_symbol* (to avoid redundant splitting        

        **OUTPUTS**
        
        *none* -- 
        """

        global symbol_formats

        collapsed_words, dummy = self.collapse_consec_single_chars(words)
                            
        #
        # Format list of words into a symbol
        #
        possible_forms = []
        for a_format in symbol_formats:

            #
            # Make a copy of the words so that formating functions can't
            # modify the original in place
            #
            tmp_words = []
            for a_word in collapsed_words: tmp_words = tmp_words + [a_word]
            a_match = a_format(pseudo_symbol, tmp_words)

            #
            # Make sure the match is labeled as new (in case the formatting
            # function forgot to do so)
            #
            a_match.is_new = 1
            possible_forms = possible_forms + [a_match]

        return possible_forms

    def reg_pseudo_to_native_symbol(self, words):
        
        """Returns a compiled regular expression that matches all possible
        native forms of a pseudo symbol.
        
        **INPUTS**
        
        *[STR]* words -- Words in the pseudo symbol to be matched.
        

        **OUTPUTS**
        
        *regexp* -- The regular expression. This regexp requires that
        the first character of every word in *words* be
        matched. Non alphanumeric characters are allowed between
        words. Matches for each word in *words* are put into
        groups.        
        """

#        print '-- SymDict.reg_pseudo_to_native_symbol: words=%s' % words
        trace('SymDict.reg_pseudo_to_native_symbol', 
            'words = %s' % repr(words))

        #
        # Generate string for the regexp.
        #
        # The regexp requires the first character of every word to be present.
        # Separator characters (not alphanums nor spaces) are allowed before
        # and after words.
        # 
        # For example for pseudo symbol "a new symbol", the regexp string
        # would be:
        #
        # ' [^a-zA-Z0-9\s]*((a)[^a-zA-Z0-9\s]*(ne{0,1}w{0,1})[^a-zA-Z0-9\s]*(sy{0,1}m{0,1}b{0,1}o{0,1}l{0,1}))[^a-zA-Z0-9\s]* '
        #
        # When matched, the first group corresponds to the whole symbol and
        # the remaining groups correspond to the segment of the native symbol
        # matched by each of the words in the pseudo symbol
        #

        reg_non_alphanums = '[^a-zA-Z0-9\s]*'
        regexp_string = ' (' + reg_non_alphanums
        for a_word in words:
            trace('SymDict.reg_pseudo_to_native_symbol',
                'a_word=%s' % a_word)
            if len(a_word) > 0:
                regexp_string = regexp_string + '(' + a_word[0]
                for a_remaining_char in a_word[1:]:
                    regexp_string = regexp_string + a_remaining_char + '{0,1}'
                regexp_string = regexp_string + ')' + reg_non_alphanums
        regexp_string = regexp_string +  ') '


        trace('SymDict.reg_pseudo_to_native_symbol', 
            'regexp_string="%s"' % regexp_string)
        
        #
        # Compile regexp with flags=IGNORECASE (i.e. case insensitive match)
        #
        regexp = re.compile(regexp_string, re.IGNORECASE)
        
        return regexp



    def accept_symbol_match(self, the_match):
        """Accepts a match between a pseudo symbol and its native form.

        Adds the new written\spoken symbol to the SR vocabulary and
        adds new abbreviations which are used in the match.

        Also, adds written\spoken symbols for symbols that contain
        those new abbreviations and whose spoken form can now be
        resolved because of those new abbreviations.
        
        **INPUTS**
        
        [SymbolMatch] the_match -- The match to be accepted
        

        **OUTPUTS**
        
        *none* --

        .. [SymbolMatch] file:///./SymDict.SymbolMatch.html"""

        trace('SymDict.accept_symbol_match', 
            'the_match.__dict__=%s' % (the_match.__dict__))
#        print '-- SymDict.accept_symbol_match: the_match.words=%s, the_match.word_matches=%s' % (the_match.words, the_match.word_matches)        
        
        #
        # Collapse consecutive single character abbreviations into a
        # single abbreviation
        # e.g. words=['context', 'sensitive']
        #      word_matches=['c', 's']
        #      then add abbreviation cs->'context sensitive' instead of
        #      two abbrevs c->'context' and 's'->'sensitive'
        #
        # Note: need to convert word_matches from a tuple to a list
        #       because can't use a tuple as an argument for +
        #
        the_match.word_matches = list(the_match.word_matches)
        the_match.word_matches, the_match.words = self.collapse_consec_single_chars(the_match.word_matches, the_match.words)                
                
        #
        # Convert word_matches back to tuple for consistency
        #
        the_match.word_matches = tuple(the_match.word_matches)
        
        #
        # Add newly resolved abbreviations
        #
        for ii in range(len(the_match.words)):
            abbrev = the_match.word_matches[ii]
            word = the_match.words[ii]
            if abbrev != word:
                if len(abbrev) >= min_abbreviation_len:
                    self.add_abbreviation(word, abbrev)
                else:
                    print 'WARNING: abbreviation \'%s\' not added (length < %s)' % (abbrev, min_abbreviation_len)            

        #
        # Add the word to the symbol dictionary its spoken forms if its
        # already there
        #
        self.add_symbol(the_match.native_symbol, user_supplied_spoken_forms=the_match.pseudo_symbol)

        #
        # Resave the dictionary to disk
        #
#        self.save()

#        print '-- SymDict.accept_symbol_match: upon exit, known symbols are now:'; self.print_symbols()
            



    def cleanup_dictionary(self, clean_sr_voc=0, clean_symdict=1, resave=1):
        """Cleans up the symbol dictionary.
        
        **INPUTS**
        
        *BOOL* clean_sr_voc=0 -- If true, then remove symbols from SR
        vocabulary

        *BOOL* clean_symdict=1 -- If true, then removes symbols from
         the symbol dictionary.

        *BOOL resave = 1* -- If true, symbol dictionary is
        resaved to disk after cleanup.        

        **OUTPUTS**
        
        *none* -- 
        """
        
#        print '-- SymDict.cleanup: called, self.standard_symbol_sources=%s' % self.standard_symbol_sources

        global vocabulary_symbols_with_written_form


        self._cached_symbols_as_one_string = ''

        #
        # Delete vocabulary entries for symbols
        #
        if clean_sr_voc:
            for (a_form, a_form_info) in self.spoken_form_info.items():
        
                #
                # This spoken form was added specifically by VoiceCode.
                # Remove it.
                #
#                print '-- SymDict.cleanup: removing word %s' % a_form
                if not vocabulary_symbols_with_written_form:
                    #
                    # Just remove the spoken form
                    #
                    sr_interface.deleteWord(a_form)
                else:
                    #
                    # Remove every spoken\written entry in the vocabulary
                    #
                    for a_written_form in self.spoken_form_info[a_form].symbols:
                        entry = sr_interface.vocabulary_entry(a_form, a_written_form)
                        sr_interface.deleteWord(entry)

        #
        # Possibly clean up the symbol dictionary itself
        #
        if clean_symdict:
#            print '-- SymDict.cleanup: abbreviations are:'; self.print_abbreviations(show_unresolved=1)
            self.spoken_form_info = {}
            self.symbol_info = {}
            for an_unresolved in self.unresolved_abbreviations.keys():
#                print '-- SymDict.cleanup: removing unresolved abbreviation %s' % an_unresolved
                if self.expansions.has_key(an_unresolved):
                    del self.expansions[an_unresolved]
            self.unresolved_abbreviations = {}

        #
        # Recompile sources of standard symbols.
        # Add symbols to the SR vocabulary only if the SR vocabulary has been
        # cleansed of symbols. This is because addition of thouasands of
        # symbols to the SR vocabulary is slow.
        #
        if clean_sr_voc:
            add_sr_entries = 1
        else:
            add_sr_entries = 0
        if clean_sr_voc or clean_symdict:
            self.parse_symbols_from_files(self.standard_symbol_sources, add_sr_entries=add_sr_entries)

        #
        # Resave dictionary to disk
        #
        if resave: self.save()
            


    def init_from_file(self):
        """Initialises the symbol dictionary from a persistent version
        stored on file.

        The file is *self.sym_file*. If *None*, don't reinitialise.
        
        **INPUTS**
        
        *none* -- 
        
        **OUTPUTS**
        
        *BOOL* -- true if we successfully retrieved the state from the
        file
        """

        if self.sym_file is None:
            return 0
        if not os.path.exists(self.sym_file):
            return 0
        try:
            db = shelve.open(self.sym_file, "r")
        except:
            msg = 'WARNING: Failed to open symbol dictionary file %s\n' \
                % self.sym_file
            sys.stderr.write(msg)
            return 0
        try:
            version = db['version']
        except KeyError:
            version = 1
        if version != current_version:
            msg = 'unknown version %d of the symbol dictionary file %s' % \
                (version, self.sym_file)
            raise RuntimeError(msg)
        try:
            values = {}
            fields = ['symbol_info', 'spoken_form_info', 'abbreviations',
                'alt_abbreviations', 'unresolved_abbreviations']
            for field in fields:
                values[field] = db[field]
        except:
            msg = 'WARNING: error reading %s from symbol dictionary file %s\n' \
                % (field, self.sym_file)
            traceback.print_exc()
            sys.stderr.write(msg)
            db.close()
            return 0

        db.close()
        version
        self.symbol_info = values['symbol_info']
        self.spoken_form_info = values['spoken_form_info']
        self.abbreviations = values['abbreviations'] 
        self.alt_abbreviations = values['alt_abbreviations'] 
        self.unresolved_abbreviations = values['unresolved_abbreviations'] 

        self.file_time = util.last_mod(self.sym_file)

# re-create expansions from abbreviations
        self.regenerate_expansions()

        #
        # Make sure symbols have been added to SR's vocabulary
        #
        for written_as, symbol_info in self.symbol_info.items():
            for spoken_as in symbol_info.spoken_forms:
                entry = sr_interface.vocabulary_entry(spoken_as, written_as)
                sr_interface.addWord(entry)
        return 1

    def regenerate_expansions(self):
        """re-creates the dictionary of expansions from the dictionaries
        of abbreviations and alternate abbreviations

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        self.expansions = {}
        for word, abbreviations in self.abbreviations.items():
            for abbreviation in abbreviations:
                self._add_corresponding_expansion(abbreviation, word)
        for word, abbreviations in self.alt_abbreviations.items():
            for abbreviation in abbreviations:
                self._add_corresponding_expansion(abbreviation, word)

    def collapse_consec_single_chars(self, words, auxilliary_words=None):
        """Takes a list of words and collapse consecutive single-char words into single words
        
        **INPUTS**
        
        *[STR]* words -- List of words

        *[STR]* auxilliary_words = None -- List of words of the same
         length as *words*. Each word in list *words* corresponds to a
         word in list *auxilliary_words* and they are collapsed in
         sync. If None, set to be the same as *words*        

        **OUTPUTS**

        Returns tuple (collapsed_words, collapsed_auxilliary_words)
        
        *[STR]* collapsed_words -- List with consecutive single-char words collapsed.

        *[STR]* collapsed_auxilliary_words -- List with consecutive
         single-char words collapsed as per what was done to
         *collapsed_words*.
        
        """

        if auxilliary_words == None:
            auxilliary_words = copy.copy(words)
        
        #
        # Collapse consecutive words which are single characters into a single
        # word
        #
        collapsed_words = []
        collapsed_auxilliary_words = []
        re_single_char = '([a-zA-Z])\.{0,1}$'
        ii = 0
        while ii < len(words):
            new_word = words[ii]
            new_auxilliary_word = auxilliary_words[ii]
            a_match = re.match(re_single_char, new_word)
            if a_match:
                #
                # This word marks the start of a sequence of single character
                # words. new_word collects those characters.
                #
                new_word = a_match.group(1)
                ii = ii + 1                
                previous_was_char = 1
                while ii < len(words) and previous_was_char:
                    next_word = words[ii]
                    next_auxilliary_word = auxilliary_words[ii]
                    a_match = re.match(re_single_char, next_word)
                    if a_match:
                        ii = ii + 1
                        new_word = new_word + next_word
                        new_auxilliary_word = new_auxilliary_word + ' ' + next_auxilliary_word
                    else:
                        previous_was_char = 0
            else:
                ii = ii + 1
            collapsed_words = collapsed_words + [string.lower(new_word)]
            collapsed_auxilliary_words = collapsed_auxilliary_words + [new_auxilliary_word]
            
        return collapsed_words, collapsed_auxilliary_words

###############################################################################
# Configuration functions. These are not methods
###############################################################################

def define_language(name, definition):
    """Defines the syntax of a programming language.

    **INPUTS**

    *STR* name -- name of the programming language

    [LangDef] definition -- language definition 


    **OUTPUTS**

    *none* -- 

    .. [LangDef] file:///./LangDef.LangDef.html"""

    global language_definitions
    definition.name = name
    language_definitions[name] = definition


