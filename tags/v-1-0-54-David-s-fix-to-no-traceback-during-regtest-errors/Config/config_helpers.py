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

"""helper functions which generate LSAs and CSCs"""

import string
import re
from SpacingState import *
from CSCmd import CSCmd
from CmdInterp import LSAlias, CSCmdSet, LSAliasSet
from cont_gen import *
from actions_gen import *
from Object import Object
import sr_interface
import debug


# US English military spelling

alpha_bravo = {}
alpha_bravo["a"] = "alpha"
alpha_bravo["b"] = "bravo"
alpha_bravo["c"] = "charlie"
alpha_bravo["d"] = "delta"
alpha_bravo["e"] = "echo"
alpha_bravo["f"] = "foxtrot"
alpha_bravo["g"] = "golf"
alpha_bravo["h"] = "hotel"
alpha_bravo["i"] = "india"
alpha_bravo["j"] = "juliett"
alpha_bravo["k"] = "kilo"
alpha_bravo["l"] = "lima"
alpha_bravo["m"] = "mike"
alpha_bravo["n"] = "november"
alpha_bravo["o"] = "oscar"
alpha_bravo["p"] = "papa"
alpha_bravo["q"] = "quebec"
alpha_bravo["r"] = "romeo"
alpha_bravo["s"] = "sierra"
alpha_bravo["t"] = "tango"
alpha_bravo["u"] = "uniform"
alpha_bravo["v"] = "victor"
alpha_bravo["w"] = "whiskey"
alpha_bravo["x"] = "xray"
alpha_bravo["y"] = "yankee"
alpha_bravo["z"] = "zulu"

def add_escaped_characters(commands, back_slash = 'back slash', 
    alphabet = 'abcdefghijklmnopqrstuvwxyz',
    name_map = alpha_bravo, cap = "cap", context = None):
    """define CSCs for characters escaped with backslashes

    **INPUTS**

    *CSCmdSet commands* -- set to which to add the context-sensitive
    commands

    *STR* back_slash -- spoken form for the backslash

    *STR* alphabet -- set of letters for which to define escaped
    characters

    *{STR: STR}* -- map from letters to an alternate spoken form (e.g.
    the military alphabet), or None to omit

    *STR* cap -- spoken form indicating that the letter should be
    capitalized, or None to omit capitalized forms

    *Context* context -- the context in which the CSCs should apply, or
    None for ContAny()
    """
    if context is None:
        context = ContAny()
    for letter in alphabet:
        ending = ["%s." % string.upper(letter)]
        if name_map:
            try:
                named = "%s" % name_map[letter]
            except KeyError:
                pass
            else:
                ending.append(named)
        spoken = map(lambda s, prefix = back_slash: "%s %s" % (prefix, s),
                     ending)
        acmd = CSCmd(spoken_forms = spoken, 
            meanings = {context: ActionInsert('\\%s' % letter, '',
                spacing = no_space_before | no_space_after)},
                docstring = 'escaped character')
        commands.add_csc(acmd)
        if cap:
            cap_spoken = map(lambda s, prefix = ("%s %s" % (back_slash, cap)): \
               "%s %s" % (prefix, s), ending)
            acmd = CSCmd(spoken_forms = cap_spoken, meanings = \
                {context: ActionInsert('\\%s' % string.upper(letter), '',
                    spacing = no_space_before | no_space_after)},
                    docstring = 'cap escaped character')
            commands.add_csc(acmd)


def add_backspacing(commands, max_count = 5, primary = 'back space', 
    alternate = 'delete backwards', context = None):
    """add CSCs for repeatable backspacing commands.

    Note: NaturallySpeaking (at least version 6) has a backspace command
    and a backspace 2 to 20 command.  Since they are defined as command
    grammars, they will take precedence over our "back space" dictation
    commands (except if you say the latter immediately before/after
    something else)

    **INPUTS**

    *CSCmdSet commands* -- set to which to add the context-sensitive
    commands

    *INT* max_count -- generate commands for backspace and backspace 2
    through max_count

    *STR* primary -- primary spoken form

    *STR* alternate -- alternate spoken form, or None to omit

    *Context* context -- the context in which the CSCs should apply, or
    None for ContAny()
    """
    if context is None:
        context = ContAny()
    for i in range(1, max_count + 1):
        count_string = "%s" % i
        spoken = ["%s %s" % (primary, count_string)]
        if alternate:
            spoken.append("%s %s" % (alternate, count_string))
        if i == 1:
            spoken = [primary]
            if alternate:
                spoken.append(alternate)
        command = CSCmd(spoken_forms = spoken, 
            meanings = {context: ActionBackspace(n_times = i)},
            docstring = "Backspace %d characters" % i)
        commands.add_csc(command)

def add_repeats(commands, max_count = 10, context = None, again = None, 
    time = 'time', times = 'times'):
    """add CSCs for repeating commands.

    **INPUTS**

    *CSCmdSet commands* -- set to which to add the context-sensitive
    commands

    *INT* max_count -- generate commands for repeating 1 through
    max_count times

    *Context* context -- the context in which the CSCs should apply, or
    None for ContLastActionWas([ActionRepeatable])

    *[STR]* again -- list of prefix strings for again/repeat n times, or
    None for ['again', 'repeat']

    *STR* time -- singular string for 1 time

    *STR* times -- plural string for n times
    """
    if context is None:
        context = ContLastActionWas([ActionRepeatable])
    if again is None:
        again = ['again', 'repeat']
    for i in range(1, max_count + 1):
        count_string = "%s" % i
        initial_count = []
        if i == 1:
            initial_count = ["%d %s" % (i, time)]
        initial_count.append("%d %s" % (i, times))
        commands.add_csc(CSCmd(spoken_forms = initial_count, 
            meanings = {context: ActionRepeatLastCmd(n_times = i,
            check_already_repeated = 1)},
            docstring = "Perform last command %s" % initial_count[0]))
        more = []
        for prefix in again:
            for form in initial_count:
                more.append("%s %s" % (prefix, form))
        commands.add_csc(CSCmd(spoken_forms = more, 
            meanings = {context: ActionRepeatLastCmd(n_times = i)},
            docstring = "Repeat last command %s" % initial_count[0]))


class PunctuationSet(Object):
    """abstract class for sets of punctuation for which to generate
    language-specific aliases for dictation and context-sensitive
    commands for navigation

    **INSTANCE ATTRIBUTES**

    *STR name* -- name of the LSAliasSet to use when adding LSAs.  The
    suffix " navigation" will be added to generat the name of the CSCmdSet
    when adding punctuation navigation 
    
    *STR language* -- language of the punctuation LSAs

    *Context context* -- context for punctuation navigation commands

    *STR next_word, prev_word, after_word, before_word* -- words with 
    which to prefix navigate-by-punctuation commands generated from 
    the punctuation set
    """
    def __init__(self, name, language = None, context = None, **args):
        """
        NOTE: These parameters can also be set later

        **INPUTS**

        *STR name* -- name of the LSAliasSet to use when adding LSAs.  The
        suffix " navigation" will be added to generate the name of the CSCmdSet
        when adding punctuation navigation 

        *STR language* -- language of the punctuation LSAs, or None to
        add language-independent aliases

        *Context context* -- context for punctuation navigation
        commands, or None for ContAny.
        """
        self.deep_construct(PunctuationSet,
                            {'name': name,
                             'language': language,
                             'context': context,
                             'next_word': None,
                             'prev_word': None,
                             'after_word': None,
                             'before_word': None},
                            args)
        self.set_direction_words()
        self.set_side_words()

    def set_direction_words(self, prev_word = 'previous', next_word = 'next'):
        """set the values of direction words used in
        navigation-by-punctuation

        **INPUTS**

        *STR prev_word, next_word* -- prefixes for moving to 
        previous/next punctuation mark

        **OUTPUTS**

        *none*
        """
        self.next_word = next_word
        self.prev_word = prev_word

    def set_side_words(self, before_word = 'before', after_word = 'after'):
        """set the values of words indicating where the cursor should be
        placed in navigation-by-punctuation

        **INPUTS**

        *STR before_word, after_word* -- prefixes for 
        moving before/after the punctuation mark

        **OUTPUTS**

        *none*
        """
        self.before_word = before_word
        self.after_word = after_word

    def set_name(self, name):
        """change the name to be used when adding LSAs and CSCs as a set

        **INPUTS**

        *STR name* -- name of the LSAliasSet to use when adding LSAs.  The
        suffix " navigation" will be added to generat the name of the CSCmdSet
        when adding punctuation navigation 

        **OUTPUTS**

        *none*
        """
        self.name = name

    def set_language(self, language):
        """set the target language

        **INPUTS**

        *STR language* -- language of the punctuation LSAs, or None to
        add language-independent aliases

        **OUTPUTS**

        *none*
        """
        self.language = language

    def set_context(self, context):
        """set the target language

        **INPUTS**

        *Context context* -- context for punctuation navigation
        commands, or None for ContAny.

        **OUTPUTS**

        *none*
        """
        self.context = context

    def _add_lsa(self, aliases, written, spoken_forms, spacing):
        """private method to add an LSA for dictation of this 
        punctuation symbol
        
        **INPUTS**

        *LSAliasSet aliases* -- set to which to add the language-specific
        aliases 
        
        *STR written* -- the written form of the symbol

        *[STR] spoken_forms* -- the spoken forms

        *INT spacing* -- the spacing flags (see SpacingState.py)
        """
        aliases.add_lsa(LSAlias(spoken_forms, 
                        {self.language: written}, spacing))

    def _add_navigation(self, commands, expression, spoken_forms):
        """private method to add CSCs for navigation by this 
        punctuation symbol
        
        **INPUTS**

        *CSCmdSet commands* -- set to which to add the context-sensitive
        commands

        *STR expression* -- a regular expression matching the symbol

        *[STR] spoken_forms* -- the spoken forms
        """
        context = self.context
        if context is None:
            context = ContAny()
        debug.trace('PunctuationSet._add_navigation', 'context=%s, expression="%s"' % (context, expression))
        for spoken in spoken_forms:
            command = CSCmd(spoken_forms = \
               ['%s %s' % (self.next_word, spoken),
                '%s %s' % (self.after_word, spoken),
                '%s %s %s' % (self.after_word, self.next_word, spoken)],
               meanings = {context: ActionSearchBidirectionalRepeat(regexp =
               expression + 
                   r'\s{0,1}')},
               docstring='go after next %s' % spoken)
            debug.trace('PunctuationSet._add_navigation', 'command.meanings=%s, command.spoken_forms=%s' % (command.meanings, repr(command.spoken_forms)))
            commands.add_csc(command)
            command = CSCmd(spoken_forms = \
               ['%s %s %s' % (self.before_word, self.next_word, spoken), 
                '%s %s' % (self.before_word, spoken)],
               meanings = {context: ActionSearchBidirectionalRepeat(regexp = r'\s{0,1}' +
                   expression, where = -1)},
               docstring='go before next %s' % spoken)
            commands.add_csc(command)
            command = CSCmd(spoken_forms = \
               ['%s %s' % (self.prev_word, spoken), 
                '%s %s %s' % (self.after_word, self.prev_word, spoken)],
               meanings = {context: ActionSearchBidirectionalRepeat(regexp =
               expression + 
                   r'\s{0,1}', direction = -1)},
               docstring='go after previous %s' % spoken)
            commands.add_csc(command)
            command = CSCmd(spoken_forms = \
               ['%s %s %s' % (self.before_word, self.prev_word, spoken)],
               meanings = {context: ActionSearchBidirectionalRepeat(regexp = r'\s{0,1}' +
                   expression, where = -1, direction = -1)},
               docstring='go before previous %s' % spoken)
            commands.add_csc(command)
        debug.trace('PunctuationSet._add_navigation', 'exited')


class SinglePunctuation(PunctuationSet):
    """set of individual (i.e. not paired) punctuation symbols used to
    define punctuation navigation commands and LSAs

    **INSTANCE ATTRIBUTES**

    *[STR]* written_forms -- list of written forms

    *[[STR]]* spoken_forms -- list of corresponding (lists of) spoken forms 

    *[INT]* spacing -- corresponding spacing flags
    """
    def __init__(self, **args):
        self.deep_construct(SinglePunctuation,
                            {'written_forms': [],
                             'spoken_forms': [],
                             'spacing': []},
                            args)

    def add(self, written_form, spoken_forms, spacing = 0):
        """add a punctuation symbol

        **INPUTS**

        *STR* written_form -- written form

        *[STR]* spoken_forms -- list of corresponding spoken forms 

        *INT spacing* -- the spacing flags (see SpacingState.py)

        **OUTPUTS**

        *none*
        """
        self.written_forms.append(written_form)
        self.spoken_forms.append(spoken_forms)
        self.spacing.append(spacing)
    
    def create(self, interp, force = 0, dictation_only = 0):
        """add LSAs for dictation of punctuation symbols and CSCs for
        punctuation navigation
        
        **INPUTS**
        
        *CmdInterp interp* -- command interpreter (or NewMediatorObject,
        which will forward to the interpreter) to which to add the LSAs
        and CSCs

        *BOOL force* -- if true, create aliases even when another alias
        with the same spoken form exists (normally, for standard forms,
        we do not do this).

        *BOOL dictation_only* -- if true, add only LSAs for dictation 
        of punctuation symbols, but not punctuation navigation commands
        """
        debug.trace('SinglePunctuation.create', 'self.name="%s"' % self.name)
        if not interp:
            return
        aliases = LSAliasSet(self.name, description = 'dictating punctuation')
        commands = CSCmdSet(self.name + " navigation", 
            description = 'navigation by punctuation')
        for i in range(len(self.written_forms)):
            if force:
                add_spoken_forms = self.spoken_forms[i]
            else:
                add_spoken_forms = []
                for spoken in self.spoken_forms[i]:
# only add the word if we don't already have an LSA with the same spoken
# form, and if the word exists in the vocabulary.  The latter prevents us 
# from accidentally adding back punctuation which the user has deleted from
# the vocabulary, or adding NaturallySpeaking US English spoken forms 
# for punctuation to the vocabulary of a different edition or different
# speech engine
                    if interp.has_lsa(spoken, language = self.language):
                        debug.trace('SinglePunctuation.create',
                            'single form "%s" already exists in language %s' % (spoken, self.language))
                        continue
                    entry = sr_interface.vocabulary_entry(spoken,
                        self.written_forms[i])
                    if sr_interface.word_exists(entry):
                        add_spoken_forms.append(spoken)
                    else:
                        debug.trace('SinglePunctuation.create',
                            "word '%s' doesn't exist" % entry)
            if add_spoken_forms:
                self._add_lsa(aliases, self.written_forms[i], 
                    add_spoken_forms, self.spacing[i])
                if not dictation_only:
                    self._add_single_navigation(commands, i, add_spoken_forms)
        interp.add_lsa_set(aliases)
        interp.add_csc_set(commands)

    def _add_single_navigation(self, commands, i, spoken_forms):
        """private method to add CSCs for navigation by this 
        punctuation symbol
        
        **INPUTS**

        *CSCmdSet commands* -- set to which to add the context-sensitive
        commands

        *INT i* -- index into list of written forms

        *[STR] spoken_forms* -- the spoken forms
        """
        debug.trace('SinglePunctuation._add_single_navigation', 'spoken_forms=%s' % repr(spoken_forms))
        escaped = re.escape(self.written_forms[i])
        self._add_navigation(commands, expression = escaped,
            spoken_forms = spoken_forms) 

class PairedPunctuation(PunctuationSet):
    """partially concrete class used to define punctuation navigation 
    commands and LSAs for punctuation symbols which come in matching pairs. 

    **INSTANCE ATTRIBUTES**

    *[STR] empty_prefixes* -- list of prefixes to singular form(s) for 
    dictating an empty pair of symbols

    *[STR] singular_pair* -- list of format strings (containing %s for
    which the singular form of the symbol name will be substituted)
    to create spoken forms for dictating a pair of symbols 
    and placing the cursor in the middle.

    *[STR] plural_pair* -- list of format strings (containing %s for
    which the plural form of the symbol name will be substituted)
    to create spoken forms for dictating a pair of symbols 
    and placing the cursor in the middle.

    *STR out_of* -- prefix for commands to jump forward out of a pair of
    symbols

    *STR back* -- prefix to out_of for commands to jump back out of a pair of
    symbols
    """
    def __init__(self, singular_pair = None, plural_pair = None, **args):
        """
        **INPUTS**
        """
        self.deep_construct(PairedPunctuation,
                            {'singular_pair': singular_pair,
                             'plural_pair': plural_pair,
                             'out_of': None,
                             'back': None,
                             'empty_prefixes': None},
                            args)
        self.set_empty_prefixes()
        self.set_jump_out_words()

    def set_pair_forms(self, singular_pair = None, plural_pair = None):
        """set the format strings for spoken forms for dictating pairs 
        of symbols.

        **INPUTS**

        *[STR] singular_pair* -- list of format strings (containing %s for
        which the singular form of the symbol name will be substituted)
        to create spoken forms for dictating a pair of symbols 
        and placing the cursor in the middle.

        *[STR] plural_pair* -- list of format strings (containing %s for
        which the plural form of the symbol name will be substituted)
        to create spoken forms for dictating a pair of symbols 

        **OUTPUTS**

        *none*
        """
        self.singular_pair = singular_pair
        self.plural_pair = plural_pair

    def set_jump_out_words(self, out_of = 'out of', back = 'back'):
        """set the values of words used in commands to jump out of a
        pair of symbols

        **INPUTS**

        *STR out_of* -- prefix for commands to jump forward out of a 
        pair of symbols

        *STR back* -- prefix to out_of for commands to jump back out 
        of a pair of symbols
        **OUTPUTS**

        *none*
        """
        self.out_of = out_of
        self.back = back

    def set_empty_prefixes(self, empty_prefixes = None):
        """set the prefixes for the left/open and right/close spoken forms

        **INPUTS**

        *[STR] empty_prefixes* -- list of prefixes to singular form(s) for 
        dictating an empty pair of symbols

        **OUTPUTS**

        *none*
        """
        if empty_prefixes is None:
            empty_prefixes = ['empty']
        self.empty_prefixes = empty_prefixes

    def _add_empty(self, aliases, written, plural, spacing):
        """private method to add LSAs for dictation of empty pairs 
        of symbols
        
        **INPUTS**

        *LSAliasSet aliases* -- set to which to add the language-specific
        aliases 

        *STR written* -- the written form of the empty pair
        
        *[STR] plural* -- list of plural spoken forms for the symbol

        *INT spacing* -- the spacing flags (see SpacingState.py)
        """
        if self.empty_prefixes:
            empty_forms = []
            for spoken in plural:
                for empty in self.empty_prefixes:
                    empty_forms.append("%s %s" % (empty, spoken))
            if empty_forms:
                aliases.add_lsa(LSAlias(empty_forms, {self.language: written},
                        spacing))

    def _add_between(self, commands, action, singular, plural):
        """private method to add CSCs for dictating a pair of symbols 
        and placing the cursor in the middle.
        
        **INPUTS**

        *CSCmdSet commands* -- set to which to add the context-sensitive
        commands

        *ActionInsert action* -- action which adds the pair of
        symbols around the cursor

        *[STR] singular* -- list of singular spoken forms for the symbol
        
        *[STR] plural* -- list of plural spoken forms for the symbol
        """
        context = self.context
        if context is None:
            context = ContAny()
        forms = []
        if self.singular_pair:
            for spoken in singular:
                for form in self.singular_pair:
                    forms.append(form % spoken)
        if self.plural_pair:
            for spoken in plural:
                for form in self.plural_pair:
                    forms.append(form % spoken)
        doc = 'pair of %s' % plural[0]
        commands.add_csc(CSCmd(spoken_forms = forms, 
                               meanings = {context: action},
                               docstring = doc))

    def _add_jump_out(self, commands, open_written, close_written, plural):
        """private method to add CSCs for jumping out of a pair of
        symbols.
        
        **INPUTS**

        *CSCmdSet commands* -- set to which to add the context-sensitive
        commands

        *STR open_written* -- written form for the opening symbol of the pair

        *STR close_written* -- written form for the closing symbol of the pair

        *[STR] plural* -- list of plural spoken forms for the symbol
        """
        context = self.context
        if context is None:
            context = ContAny()
        open_escaped = re.escape(open_written)
        close_escaped = re.escape(close_written)
        if self.out_of:
            doc = 'jump forward out of innermost pair of %s' \
                % plural[0]
            spoken_forms = []
            for spoken in plural:
                spoken_forms.append("%s %s" % (self.out_of, spoken))
            command = CSCmd(spoken_forms,
               meanings = {context: ActionSearchBidirectionalRepeat(regexp = close_escaped + 
                   r'\s{0,1}')},
               docstring=doc)
            commands.add_csc(command)
            if self.back:
                back_spoken_forms = []
                doc = 'jump backward out of innermost pair of %s' \
                    % plural[0]
                for spoken_form in spoken_forms:
                    back_spoken_forms.append(self.back + " " + spoken_form)
                command = CSCmd(back_spoken_forms,
                   meanings = {context: ActionSearchBidirectionalRepeat(regexp = \
                           r'\s{0,1}' + open_escaped, 
                           direction = -1, where = -1)},
                   docstring=doc)
                commands.add_csc(command)


class LeftRightPunctuation(PairedPunctuation):
    """punctuation symbols which come in matching pairs with different
    written forms for left/open vs. right/close 
    used to define punctuation navigation commands and LSAs

    **INSTANCE ATTRIBUTES**

    *[STR]* open_written_forms, close_written_forms -- opening and closing
    written forms for the pair

    *[[STR]]* singular_spoken_forms -- corresponding (lists of) spoken forms 
    for single symbols (omitting open/left/close/right)

    *[[STR]]* plural_spoken_forms -- corresponding (lists of) spoken forms 
    for plural symbols

    *[STR] left_prefixes* -- prefixes for left/open member of the pair

    *[STR] right_prefixes* -- prefixes for right/close member of the pair
    """
    def __init__(self, **args):
        self.deep_construct(LeftRightPunctuation,
                            {'open_written_forms': [],
                             'close_written_forms': [],
                             'singular_spoken_forms': [],
                             'plural_spoken_forms': [],
                             'left_prefixes': None,
                             'right_prefixes': None},
                            args)
        self.set_prefixes()

    def set_prefixes(self, left_prefixes = None, right_prefixes = None):
        """set the prefixes for the left/open and right/close spoken forms

        **INPUTS**

        *[STR] left_prefixes* -- prefixes for left/open member of the pair, 
        or None for ['left-', 'open-']

        *[STR] right_prefixes* -- prefixes for right/close member of the pair,
        or None for ['right-', 'close-']

        **OUTPUTS**

        *none*
        """
        if left_prefixes is None:
            left_prefixes = ['left-', 'open-']
        if right_prefixes is None:
            right_prefixes = ['right-', 'close-']
        self.left_prefixes = left_prefixes
        self.right_prefixes = right_prefixes

    def add(self, open_written_form, close_written_form, 
        singular_spoken_forms, plural_spoken_forms = None):
        """
        add a pair of punctuation symbols

        **INPUTS**

        *STR* open_written_form, close_written_form -- opening and closing
        written forms for the pair

        *[STR]* singular_spoken_forms -- spoken forms for single symbols
        (omitting open/left/close/right)

        *[STR]* plural_spoken_forms -- spoken forms for plural symbols

        **OUTPUTS**

        *none*
        """
        self.open_written_forms.append(open_written_form)
        self.close_written_forms.append(close_written_form)
        self.singular_spoken_forms.append(singular_spoken_forms)
        self.plural_spoken_forms.append(plural_spoken_forms)

    def create(self, interp, force = 0, dictation_only = 0):
        """add LSAs for dictation of punctuation symbols and CSCs for
        punctuation navigation
        
        **INPUTS**
        
        *CmdInterp interp* -- command interpreter (or NewMediatorObject,
        which will forward to the interpreter) to which to add the LSAs
        and CSCs

        *BOOL force* -- if true, create aliases even when another alias
        with the same spoken form exists (normally, for standard forms,
        we do not do this).

        *BOOL dictation_only* -- if true, add only LSAs for dictation 
        of punctuation symbols, but not punctuation navigation commands
        """
        if not interp:
            return
        aliases = LSAliasSet(self.name, 
            description = 'dictating left- and right- punctuation')
        between = CSCmdSet("between " + self.name,
            description = 'dictating punctuation in matching pairs')
        navigation = CSCmdSet(self.name + " navigation", 
            description = 'navigation by punctuation')
        for i in range(len(self.open_written_forms)):
            open_spoken_forms = []
            close_spoken_forms = []
            for spoken in self.singular_spoken_forms[i]:
                for left in self.left_prefixes:
                    left_comp = "%s%s" % (left, spoken)
                    if force:
                        open_spoken_forms.append(left_comp)
                    else:
# only add the word if we don't already have an LSA with the same spoken
# form, and if the word exists in the vocabulary.  The latter prevents us 
# from accidentally adding back punctuation which the user has deleted from
# the vocabulary, or adding NaturallySpeaking US English spoken forms 
# for punctuation to the vocabulary of a different edition or different
# speech engine
                        if interp.has_lsa(left_comp, language = self.language):
                            debug.trace('LeftRightPunctuation.create',
                                'left form "%s" already exists in language %s' % (left_comp, self.language))
                            continue
                        entry = sr_interface.vocabulary_entry(left_comp,
                            self.open_written_forms[i])
                        if sr_interface.word_exists(entry):
                            open_spoken_forms.append(left_comp)
                        else:
                            debug.trace('LeftWritePunctuation.create',
                                "word '%s' doesn't exist" % entry)
                for right in self.right_prefixes:
                    right_comp = "%s%s" % (right, spoken)
                    if force:
                        close_spoken_forms.append(right_comp)
                    else:
                        if interp.has_lsa(right_comp, 
                            language = self.language):
                            debug.trace('LeftRightPunctuation.create',
                                'right form "%s" already exists in language %s' % (right_comp, self.language))
                            continue
                        entry = sr_interface.vocabulary_entry(right_comp,
                            self.close_written_forms[i])
                        if sr_interface.word_exists(entry):
                            close_spoken_forms.append(right_comp)
                        else:
                            debug.trace('LeftWritePunctuation.create',
                                "word '%s' doesn't exist" % entry)
            if open_spoken_forms or close_spoken_forms:
                self._add_single(aliases, i, 
                    open_spoken_forms, close_spoken_forms)
                written = self.open_written_forms[i] + \
                    self.close_written_forms[i]
                plural = self.plural_spoken_forms[i]
                if plural:
                    self._add_empty(aliases, written,
                        plural, 
                        spacing = joins_identifier)
                    action = ActionInsert(code_bef = \
                        self.open_written_forms[i],
                        code_after = self.close_written_forms[i],
                        spacing = like_open_paren)
                    self._add_between(between, action,
                        self.singular_spoken_forms[i],
                        self.plural_spoken_forms[i])
                if not dictation_only:
                    self._add_single_navigation(navigation, i,
                        open_spoken_forms, close_spoken_forms)
                    self._add_either_navigation(navigation, i)
                    if plural:
                        self._add_jump_out(navigation,
                            self.open_written_forms[i],
                            self.close_written_forms[i],
                            self.plural_spoken_forms[i])
        interp.add_lsa_set(aliases)
        interp.add_csc_set(between)
        interp.add_csc_set(navigation)

    def _add_single(self, aliases, i, open_spoken_forms, 
        close_spoken_forms):
        """private method to add LSAs for dictation of left and right 
        elements of the pair of symbols
        
        **INPUTS**

        *LSAliasSet aliases* -- set to which to add the language-specific
        aliases 
        
        *INT i* -- index into list of written forms

        *[STR] open_spoken_forms* -- the spoken forms for the left/open
        symbol

        *[STR] close_spoken_forms* -- the spoken forms for the
        right/close symbol
        """
        aliases.add_lsa(LSAlias(open_spoken_forms, 
                        {self.language: self.open_written_forms[i]}, 
                        spacing = like_open_paren))
        aliases.add_lsa(LSAlias(close_spoken_forms, 
                        {self.language: self.close_written_forms[i]}, 
                        spacing = like_close_paren))

    def _add_single_navigation(self, commands, i, open_spoken_forms,
        close_spoken_forms):
        """private method to add CSCs for navigation by the left and
        right forms of this punctuation symbol
        
        **INPUTS**

        *CSCmdSet commands* -- set to which to add the context-sensitive
        commands

        *INT i* -- index into list of written forms

        *[STR] open_spoken_forms* -- the spoken forms for the left
        element of the pair

        *[STR] close_spoken_forms* -- the spoken forms for the right
        element of the pair
        """
        left_escaped = re.escape(self.open_written_forms[i])
        self._add_navigation(commands, expression = left_escaped,
            spoken_forms = open_spoken_forms) 
        right_escaped = re.escape(self.close_written_forms[i])
        self._add_navigation(commands, expression = right_escaped,
            spoken_forms = close_spoken_forms) 

    def _add_either_navigation(self, commands, i):
        """private method to add CSCs for navigation by either left or
        right forms of this punctuation symbol
        
        **INPUTS**

        *CSCmdSet commands* -- set to which to add the context-sensitive
        commands

        *INT i* -- index into list of written forms
        """
        left_escaped = re.escape(self.open_written_forms[i])
        right_escaped = re.escape(self.close_written_forms[i])
        expression = "[%s%s]" % (left_escaped, right_escaped)
        self._add_navigation(commands, expression,
            self.singular_spoken_forms[i]) 

class PairedQuotes(PairedPunctuation):
    """paired quotes with identical written forms for left/open vs. 
    right/close, used to define punctuation navigation commands and LSAs

    **INSTANCE ATTRIBUTES**

    *[STR]* written_forms -- written forms for each type of quote

    *[[STR]]* singular_spoken_forms -- corresponding (lists of) spoken forms 
    for single symbols (omitting open-/begin-/close-/end-)

    *[[STR]]* plural_spoken_forms -- corresponding spoken forms for 
    plural symbols

    *[BOOL]* no_empty -- corresponding flags indicating whether to omit 
    empty quotes form

    *[STR] open_prefixes* -- prefixes for open-/begin- member of the pair

    *[STR] close_prefixes* -- prefixes for close-/end- member of the pair
    """
    def __init__(self, **args):
        self.deep_construct(PairedQuotes,
                            {'written_forms': [],
                             'singular_spoken_forms': [],
                             'plural_spoken_forms': [],
                             'no_empty': [],
                             'open_prefixes': None,
                             'close_prefixes': None},
                            args)
        self.set_prefixes()

    def set_prefixes(self, open_prefixes = None, close_prefixes = None):
        """set the prefixes for the open/begin and close/end spoken forms

        **INPUTS**

        *[STR] open_prefixes* -- prefixes for open/begin member of the pair, 
        or None for ['open-', 'begin-']

        *[STR] close_prefixes* -- prefixes for close/end member of the pair,
        or None for ['close-', 'end-']

        **OUTPUTS**

        *none*
        """
        if open_prefixes is None:
            open_prefixes = ['open-', 'begin-']
        if close_prefixes is None:
            close_prefixes = ['close-', 'end-']
        self.open_prefixes = open_prefixes
        self.close_prefixes = close_prefixes

    def add(self, written_form, singular_spoken_forms, 
            plural_spoken_forms, no_empty = 0):
        """add a type of quotes

        **INPUTS**

        *STR* written_form -- written form

        *[STR]* spoken_forms -- list of corresponding spoken forms 

        **OUTPUTS**

        *none*
        """
        self.written_forms.append(written_form)
        self.singular_spoken_forms.append(singular_spoken_forms)
        self.plural_spoken_forms.append(plural_spoken_forms)
        self.no_empty.append(no_empty)

    def create(self, interp, force = 0, dictation_only = 0):
        """add LSAs for dictation of punctuation symbols and CSCs for
        punctuation navigation
        
        **INPUTS**
        
        *CmdInterp interp* -- command interpreter (or NewMediatorObject,
        which will forward to the interpreter) to which to add the LSAs
        and CSCs

        *BOOL force* -- if true, create aliases even when another alias
        with the same spoken form exists (normally, for standard forms,
        we do not do this).

        *BOOL dictation_only* -- if true, add only LSAs for dictation 
        of punctuation symbols, but not punctuation navigation commands
        """
        if not interp:
            return
        aliases = LSAliasSet(self.name, 
            description = 'dictating open- and close- quotes')
        between = CSCmdSet("between " + self.name,
            description = 'dictating punctuation in matching pairs')
        navigation = CSCmdSet(self.name + " navigation", 
            description = 'navigation by punctuation')
        for i in range(len(self.written_forms)):
            open_spoken_forms = []
            close_spoken_forms = []
            for spoken in self.singular_spoken_forms[i]:
                for open_prefix in self.open_prefixes:
                    open_comp = "%s%s" % (open_prefix, spoken)
                    if force:
                        open_spoken_forms.append(open_comp)
                    else:
# only add the word if we don't already have an LSA with the same spoken
# form, and if the word exists in the vocabulary.  The latter prevents us 
# from accidentally adding back punctuation which the user has deleted from
# the vocabulary, or adding NaturallySpeaking US English spoken forms 
# for punctuation to the vocabulary of a different edition or different
# speech engine
                        if interp.has_lsa(open_comp, language =
                            self.language):
                            debug.trace('PairedQuotes.create',
                                'open form "%s" already exists in language %s' % (open_comp, self.language))
                            continue
                        entry = sr_interface.vocabulary_entry(open_comp,
                            self.written_forms[i])
                        if sr_interface.word_exists(entry):
                            open_spoken_forms.append(open_comp)
                        else:
                            debug.trace('PairedQuotes.create',
                                "word '%s' doesn't exist" % entry)
                for close_prefix in self.close_prefixes:
                    close_comp = "%s%s" % (close_prefix, spoken)
                    if force:
                        close_spoken_forms.append(close_comp)
                    else:
                        if interp.has_lsa(close_comp, language =
                            self.language):
                            debug.trace('PairedQuotes.create',
                                'close form "%s" already exists in language %s' % (open_comp, self.language))
                            continue
                        entry = sr_interface.vocabulary_entry(close_comp,
                            self.written_forms[i])
                        if sr_interface.word_exists(entry):
                            close_spoken_forms.append(close_comp)
                        else:
                            debug.trace('PairedQuotes.create',
                                "word '%s' doesn't exist" % entry)
            if open_spoken_forms or close_spoken_forms:
                self._add_single(aliases, i, 
                    open_spoken_forms, close_spoken_forms)
                plural = self.plural_spoken_forms[i]
                if plural:
                    if not self.no_empty[i]:
                        written = self.written_forms[i] * 2
                        self._add_empty(aliases, written,
                            plural, 
                            spacing = normal_spacing)
                    action = ActionInsert(code_bef = \
                        self.written_forms[i],
                        code_after = self.written_forms[i],
                        spacing = like_open_quote)
                    self._add_between(between, action,
                        self.singular_spoken_forms[i],
                        self.plural_spoken_forms[i])
                if not dictation_only:
                    expression = re.escape(self.written_forms[i])
                    self._add_navigation(navigation, expression,
                        self.singular_spoken_forms[i])
                    if plural:
                        self._add_jump_out(navigation,
                            self.written_forms[i],
                            self.written_forms[i],
                            self.plural_spoken_forms[i])
        interp.add_lsa_set(aliases)
        interp.add_csc_set(between)
        interp.add_csc_set(navigation)


    def _add_single(self, aliases, i, open_spoken_forms, 
        close_spoken_forms):
        """private method to add LSAs for dictation of open and close
        quotes
        
        **INPUTS**

        *LSAliasSet aliases* -- set to which to add the language-specific
        aliases 
        
        *INT i* -- index into list of written forms

        *[STR] open_spoken_forms* -- the spoken forms for the left/open
        symbol

        *[STR] close_spoken_forms* -- the spoken forms for the
        right/close symbol
        """
        aliases.add_lsa(LSAlias(open_spoken_forms, 
                        {self.language: self.written_forms[i]}, 
                        spacing = like_open_quote))
        aliases.add_lsa(LSAlias(close_spoken_forms, 
                        {self.language: self.written_forms[i]}, 
                        spacing = like_close_quote))
