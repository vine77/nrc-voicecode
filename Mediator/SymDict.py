"""Classes for dealing with programming symbols and their spoken forms.
"""


from Object import Object
from SourceBuff import SourceBuff
from LangDef import LangDef
import auto_test, sr_interface, vc_globals
import os, re, string
import CmdInterp, EdSim


language_definitions={}

#
# Set *vocabulary_symbols_written_form* to 1 if you want VoiceCode to create a
# written form/spoken form entry in the SR vocabulary for every symbol it
# compiles.
# If set to 0, SR will create a spoken form entry only and the VoiceCode
# command interpreter will translate that spoken form to a written form
#
vocabulary_symbols_with_written_form = 1


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
    
    *{STR: STR} word_matches=None* -- Keys are words of
     *pseudo_symbol* and vallues are the matching segment in
     *native_symbol*.

    CLASS ATTRIBUTES**
            
    *none* -- 
    """
    
    def __init__(self, pseudo_symbol=None, native_symbol=None, word_matches=None, **args_super):
        self.deep_construct(SymbolMatch, \
                            {'pseudo_symbol': pseudo_symbol, \
                             'native_symbol': native_symbol, \
                             'word_matches': word_matches}, \
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

    *{STR: [STR]}* abbreviations={} -- Dictionary of
     abbreviations. The key is the abbreviation and the value is a
     list of poosible expansions. It contains both resolved and
     unresolved abbreviations.

    *{STR: {STR: 1}}* unresolved_abbreviations={} -- Dictionary of
     unresolved abbreviations. These are abbreviations that have
     appeared in at least one compiled symbol, yet are neither a word
     in the speech vocabulary or a known abbreviation. Values are
     dictionnaries that list the symbols containing the unresolved
     abbreviation.

    *STR* _cached_symbols_as_one_string=None -- Caches the last value
     returned by method [symbols_as_one_string]. A value of *None*
     indicates that the string needs to be regenerated by
     [symbols_as_one_string].

   
    CLASS ATTRIBUTES**

    *{STR: * [LangDef] *}* language_definitions={} -- Key is the name
     of a language and the value is a language definition object which
     defines rules for parsing symbols in that language.
        
    .. [LangDef] file:///./LangDef.LangDef.html
    .. [SymbolInfo] file:///./SymDict.SymbolInfo.html
    .. [SpokenFormInfo] file:///./SymDict.SpokenFormInfo.html
    .. [symbols_as_one_string] file:///./SymDict.SymDict.html#symbols_as_one_string"""

    def __init__(self, symbol_info={}, spoken_form_info={},
                 abbreviations={}, **attrs):

        # These attributes can't be set at construction time
        self.decl_attrs({'_cached_symbols_as_one_string': None})

        # These attributes CAN be set at construction time
        self.deep_construct(SymDict,
                            {'spoken_form_info': spoken_form_info, \
                             'symbol_info': symbol_info, \
                             'abbreviations': abbreviations, \
                             'unresolved_abbreviations': {}}, \
                            attrs)


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
            
        return self._cached_symbols_as_one_string

    def print_symbols(self):
        """Print the content of the symbols dictionary.
        
        **INPUTS**
        
        *none* -- 
        
        
        **OUTPUTS**
        
        *none* -- 
        """
        sorted_symbols = self.symbol_info.keys()
        sorted_symbols.sort()        
        for a_symbol in sorted_symbols:
            a_symbol_info = self.symbol_info[a_symbol]
            print '%s: %s' % (a_symbol, str(a_symbol_info.spoken_forms))

        print '_cached_symbols_as_one_string is:\n   %s' % self._cached_symbols_as_one_string

    def parse_symbols(self, file_name):
        """Parse symbols from a source file.

        *STR file_name* is the path of the file.

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

            language_definition = self.get_language_definition(file_name)
            source = self.strip_source(source, language_definition)

            #
            # Parse symbols from the first chunk
            #
            while source != '':
                a_match = re.search('(' + language_definition.regexp_symbol + ')', source)
                if a_match:
                    self.add_symbol(a_match.group(1))
                    source = source[a_match.end()+1:]
                else:
                    source = ''
                


    def strip_source(self, source, language_definition):
        """Removes all parts of a source file that don't contain symbols.

        This includes comments and quoted strings.
        
        **INPUTS**
        
        *STR* source -- the source

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
                                

    def add_symbol(self, symbol):
        """Add a symbol to the dictionary

        **INPUTS**
        
        *STR* symbol -- Symbol to add 
        
        **OUTPUTS**
        
        *none* -- 
        """

        global vocabulary_symbols_with_written_form
        
#        print '-- SymDict.add_symbol: symbol=%s' % symbol
        
        if not self.symbol_info.has_key(symbol):
            
#            print '-- SymDict.add_symbol: this is a new symbol'
            
            #
            # Get the symbol's spoken forms
            #
            forms_this_symbol = self.get_spoken_forms(symbol)
#            print '-- SymDict.add_symbol: forms_this_symbol=%s' % forms_this_symbol
            self.symbol_info[symbol] = SymbolInfo(spoken_forms=forms_this_symbol)
            #
            # Store information about the symbol and its spoken forms
            #
            for a_form in forms_this_symbol:
#                print '-- SymDict.add_symbol: a_form=%s' % a_form            
                if self.spoken_form_info.has_key(a_form):
                    self.spoken_form_info[a_form].symbols = self.spoken_form_info[a_form].symbols + [symbol]
                else:
#                    print '-- SymDict.add_symbol: this is a new spoken form'
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
#                    print '-- SymDict.add_symbol: adding symbol spoken=\'%s\', written=\'%s\'' % (a_form, symbol)
                    if len(re.split('\s+', a_form)) > 1:
                        if vocabulary_symbols_with_written_form:
                            #
                            # Add the vocabulary entry as a written\\spoken
                            # form
                            #
#                            print '-- SymDict.add_symbol: adding it as a written/spoken form'
                            entry = sr_interface.vocabulary_entry(a_form, symbol)
                        else:
                            #
                            # Add just the spoken form entry
                            #
#                            print '-- SymDict.add_symbol: adding it as a written form only'
                            entry = sr_interface.vocabulary_entry(a_form)
                            
                        sr_interface.addWord(entry)        

    def get_spoken_forms(self, symbol):
        """Returns a list of possible spoken forms for a symbol.
        
        **INPUTS**
        
        *STR* symbol -- the symbol in question 
        

        **OUTPUTS**
        
        *[STR]* -- returns a list of spoken forms
        """

#        print '-- SymDict.get_spoken_forms: symbol=%s' % symbol
        
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
        if word[word_length-1] == 's':
            single_form = word[0:word_length-1]
        else:
            single_form = word
        
        expansions = [word]
        if self.abbreviations.has_key(word):
            #
            # word is a known abbreviation. Add expansions.
            #
            expansions = expansions + self.abbreviations[word]
        elif self.abbreviations.has_key(single_form):
            #
            # word is the plural of an abbreviation
            #
            expansions = map(lambda an_expansion: pluralize(an_expansion), self.abbreviations[single_form])
        else:
            #
            # Word is not a known abbreviation nor plural of a known
            # abbreviation
            # Check if this is an unresolved abbreviation
            # (note: flag=4 means case unsensitive)
            #
            if sr_interface.getWordInfo(word, 4) == None:
                if self.unresolved_abbreviations.has_key(word):
                    self.unresolved_abbreviations[word][symbol] = 1
                else:
                    self.unresolved_abbreviations[word] = {symbol: 1}
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

            expanded_forms = self.expand_possible_forms(extended_partial_forms ,further_extensions)
                    
            return expanded_forms
            
            
    def get_language_definition(self, file_name):
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
        language_name = SourceBuff().language_name(file_name)
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

        #
        # Find all known native symbols that match *pseudo_symbol*
        #
        all_symbols = self.symbols_as_one_string()
        regexp = self.reg_pseudo_to_native_symbol(pseudo_symbol)

#        print '-- SymDict.match_pseudo_symbol: regexp=%s, all_symbols=\'%s\'' % (regexp.__dict__, all_symbols)
        
        raw_matches = regexp.findall(all_symbols)

#        print '-- SymDict.match_pseudo_symbol: raw_matches = %s' % raw_matches

        #
        # Create a list of matches
        #
        matches = []
        for a_match in raw_matches:
            matches = matches + [SymbolMatch(pseudo_symbol=pseudo_symbol, native_symbol=a_match[0], word_matches=a_match[1:])]

        #
        # Sort the list of matches according to their scores
        #
        matches.sort(SymbolMatch.compare_scores)
        return matches
  

    def reg_pseudo_to_native_symbol(self, pseudo_symbol):
        
        """Returns a compiled regular expression that matches all possible
        native forms of a pseudo symbol.
        
        **INPUTS**
        
        *STR* pseudo_symbol -- The pseudo symbol to be matched.
        

        **OUTPUTS**
        
        *regexp* -- The regular expression. This regexp requires that
        the first character of every word in *pseudo_symbol* be
        matched. Non alphanumeric characters are allowed between
        words. Matches for each word in *pseudo_symbol* are put into
        groups.        
        """

#        print '-- SymDict.reg_pseudo_to_native_symbol: pseudo_symbol=%s' % pseudo_symbol

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
        words = re.split('\s+', pseudo_symbol)
        regexp_string = ' (' + reg_non_alphanums
        for a_word in words:
            regexp_string = regexp_string + '(' + a_word[0]
            for a_remaining_char in a_word[1:]:
                regexp_string = regexp_string + a_remaining_char + '{0,1}'
            regexp_string = regexp_string + ')' + reg_non_alphanums
        regexp_string = regexp_string +  ') '


#        print '-- SymDict.reg_pseudo_to_native_symbol: regexp_string=\'%s\'' % regexp_string
        
        #
        # Compile regexp with flags=1 (i.e. case insensitive match)
        #
        regexp = re.compile(regexp_string, 1)
        
        return regexp



    def vocabulary_cleanup(self):
        """Removes symbols from the speech recognition vocabulary
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        global vocabulary_symbols_with_written_form
        
        for (a_form, a_form_info) in self.spoken_form_info.items():
        
              #
              # This spoken form was added specifically by VoiceCode.
              # Remove it.
              #
#              print '-- SymDict.vocabulary_cleanup: removing word %s' % a_form
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
                  
        self.spoken_form_info = {}
        self.symbol_info = {}
            

        



