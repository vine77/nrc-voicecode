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

import os, re, string, sys

import actions_gen, auto_test, vc_globals
from debug import trace, config_warning
from actions_C_Cpp import *
from actions_py import *
from AppState import AppState
from cont_gen import ContC, ContPy
from CSCmd import CSCmd, DuplicateContextKeys
from Object import Object, OwnerObject
import SymDict
import symbol_formatting
import sr_interface
import WordTrie

from SpacingState import *

class DeferInterp(Object):
    """
    abstract base class which allows the interpreter main loop to 
    distinguish phrase translations which should be interpreted 
    immediately from those whose interpretation should be deferred 
    to the new symbol loop
    """
    def __init__(self, **args):
        self.deep_construct(DeferInterp, {}, args)

    def interp_now(self,  preceding_symbol = 0):
        """tells the interpreter main loop whether to interpret this 
        object now or whether to append it to the untranslated list
        which will build up the components of a new symbol

        **INPUTS**

        BOOL *preceding_symbol* indicates if there is already
        untranslated text (LSAs generating digits should be interpreted
        immediately if there is no pending text, because digits cannot
        start a symbol name)

        **OUTPUTS**

        *BOOL* -- if true, the object should be interpreted now
        """
        debug.virtual('DeferInterp.interp_now')

class LSAlias(Object):
    """
    Language-specific alias (or LSA), a word with one or more spoken 
    forms, which is translated into a written form according to the 
    language of the current buffer.
    
    Generally, all combinations of written and spoken forms for an LSA 
    are added to the vocabulary as words, so as to enable
    select-pseudocode.

    **INSTANCE ATTRIBUTES**
    
    *STR* spoken_forms -- List of spoken form of the word.

    *{STR: STR}* meanings -- Dictionary of language specific
     meanings. Key is the language name and value is the written form
     of the LSA for that langugage. If language name is *None*, then
     it means that this LSA applies for all languages (I know, it
     doesn't make much sense syntactically).

    *INT* spacing -- spacing flags, from SpacingState (Note: only a
    handful of these spacing flags are currently used)

    *STR* new_symbol -- flag indicating whether the LSAlias can form
    part of a new symbol.  Recognized values are None if the alias
    is always interpreted on its own (and flushes any pending
    untranslated phrase), 'start' if it can start a new symbol (e.g.
    underscore, letter-alpha), or 'within' if it can appear within a
    symbol but cannot start one (e.g. digits)
    """
    def __init__(self, spoken_forms, meanings, spacing = 0, 
        new_symbol = None, **args):
        """
        **INPUTS**

        *STR* spoken_forms -- List of spoken form of the word.

        *{STR: STR}* meanings -- Dictionary of language specific
         meanings. Key is the language name and value is the written form
         of the LSA for that langugage. If language name is *None*, then
         it means that this LSA applies for all languages (I know, it
         doesn't make much sense syntactically).

        *INT* spacing -- spacing flags, from SpacingState (CURRENTLY
        IGNORED BUT MUST BE SPECIFIED PROPERLY TO INSURE FUTURE
        COMPATABILITY)

        *STR* new_symbol -- flag indicating whether the LSAlias can form
        part of a new symbol.  Recognized values are None if the alias
        is always interpreted on its own (and flushes any pending
        untranslated phrase), 'start' if it can start a new symbol (e.g.
        underscore, letter-alpha), or 'within' if it can appear within a
        symbol but cannot start one (e.g. digits)
        """
        self.deep_construct(LSAlias,
                            {'spoken_forms': spoken_forms,
                             'meanings': {},
                             'spacing': spacing,
                             'new_symbol': new_symbol
                            },
                            args)

        for language, written_as in meanings.items():
            self.meanings[language] = written_as

class AliasMeaning(DeferInterp, symbol_formatting.SymElement):
    """underlying object used by CmdInterp to store the data associated 
    with an LSAlias meaning

    **INSTANCE ATTRIBUTES**

    *STR* written_form -- the written form of the LSA 

    *INT* spacing -- spacing flags, from SpacingState (CURRENTLY
    IGNORED BUT MUST BE SPECIFIED PROPERLY TO INSURE FUTURE
    COMPATABILITY)

    *STR* new_symbol -- flag indicating whether the LSAlias can form
    part of a new symbol.  Recognized values are None if the alias
    is always interpreted on its own (and flushes any pending
    untranslated phrase), 'start' if it can start a new symbol (e.g.
    underscore, letter-alpha), or 'within' if it can appear within a
    symbol but cannot start one (e.g. digits)
    """
    def __init__(self, written_form, spacing = 0, new_symbol = None,
        **args):
        self.deep_construct(AliasMeaning,
                            {
                             'written_form': written_form,
                             'spacing_flag': spacing,
                             'new_symbol': new_symbol
                            },
                            args)
    def written(self):
        """returns the written form of the alias

        **INPUTS**

        *none*

        **OUTPUTS**
        
        *STR* -- the written form
        """
        return self.written_form

    def spacing(self):
        """returns the spacing flag for the alias

        **INPUTS**

        *none*

        **OUTPUTS**
        
        *STR* -- the spacing flag
        """
        return self.spacing_flag

    def interp_now(self,  preceding_symbol = 0):
        """tells the interpreter main loop whether to interpret this 
        object now or whether to append it to the untranslated list
        which will build up the components of a new symbol

        **INPUTS**

        BOOL *preceding_symbol* indicates if there is already
        untranslated text (LSAs generating digits should be interpreted
        immediately if there is no pending text, because digits cannot
        start a symbol name)

        **OUTPUTS**

        *BOOL* -- if true, the object should be interpreted now
        """
        if self.new_symbol is None:
            return 1
        if self.new_symbol == 'within' and not preceding_symbol:
            return 1
        return 0

    def make_element(self, spoken):
        """create an AliasElement corresponding to this alias

        **INPUTS**

        *STR spoken* -- the spoken form used to dictate this alias

        **OUTPUTS**

        *AliasElement*
        """
        return AliasElement(self.written(), spoken)
            
class AliasElement(symbol_formatting.SymElement):
    """LSAlias meaning as an element of a symbol
    """

    def __init__(self, written, spoken, **args):
        self.deep_construct(AliasElement,
                            {
                             'written': written,
                             'spoken': spoken
                            },
                            args)

    def add_to(self, builder):
        """Add alias's written form to the symbol builder

        **INPUTS**

        *SymBuilder builder*

        **OUTPUTS**

        *none*
        """
        match = re.match(r'([a-zA-Z])\.{0,1}$', self.written)
        if match:
            letter = match.group(1)
            spoken = "%s." % string.upper(letter) 
            builder.add_letter(string.lower(letter), spoken)
        else:
            builder.add_word(self.written, self.spoken)


class CapitalizationWord(Object):
    """A word with no written form, but which affects capitalization of
    following word(s) in the symbol
    
    **INSTANCE ATTRIBUTES**
    
    *STR* spoken_forms -- List of spoken form of the word.

    *CapsModifier modifier* -- underlying capitalization data
    """
    def __init__(self, spoken_forms, caps, one_word = 1, **args):
        """
        **INPUTS**

        *STR caps* -- the new capitalization state: 'no-caps', 'normal', 
        'cap', or 'all-caps'

        *BOOL one_word* -- if true, modify capitalization for the next
        word.  If false, modify for all following words until a
        subsequent CapitalizationWord with one_word = 0.  (A subsequent
        CapitalizationWord one_word = 1 will take precedence temporarily)
        """
        self.deep_construct(CapitalizationWord,
                            {
                             'spoken_forms': spoken_forms,
                             'modifier': CapsModifier(caps, one_word),
                            },
                            args)

class CapsModifier(DeferInterp):
    """underlying object used by CmdInterp to store the data associated 
    with a CapitalizationWord
    """
    def __init__(self, caps, one_word = 1, **args):
        self.deep_construct(CapsModifier, 
                            {
                             'caps': caps, 
                             'one_word': one_word
                            }, args)

    def interp_now(self,  preceding_symbol = 0):
        """tells the interpreter main loop whether to interpret this 
        object now or whether to append it to the untranslated list
        which will build up the components of a new symbol

        **INPUTS**

        BOOL *preceding_symbol* indicates if there is already
        untranslated text (LSAs generating digits should be interpreted
        immediately if there is no pending text, because digits cannot
        start a symbol name)

        **OUTPUTS**

        *BOOL* -- if true, the object should be interpreted now
        """
# manual capitalization is ALWAYS part of new symbol, so it is never
# interpreted immediately (and it couldn't be interpreted safely, 
# since it doesn't implement the rest of the methods of AliasMeaning)
        return 0

    def written(self):
# dummy method to allow CapsModifier to pretend to be an LSAlias
        return ""
    
    def make_element(self, spoken):
        """create a CapsModifierElement corresponding to this modifier
        
        **INPUTS**

        *STR spoken* -- the spoken form used to dictate this modifier

        **OUTPUTS**

        *CapsModifierElement*
        """
        return CapsModifierElement(self.caps, self.one_word)

class CapsModifierElement(symbol_formatting.SymElement):
    """SymElement corresponding to a word which changes capitalization of
    the following word(s)
    """
    def __init__(self, caps, one_word = 1, **args):
        self.deep_construct(CapsModifierElement, 
                            {
                             'caps': caps, 
                             'one_word': one_word
                            }, args)


    def add_to(self, builder):
        """Add element to the symbol builder

        **INPUTS**

        *SymBuilder builder*

        **OUTPUTS**

        *none*
        """
        builder.change_caps(self.caps, one_word = self.one_word)

class CSCmdSet(Object):
    """a collection of context-sensitive commands which may be deleted,
    renamed, or giving synonyms prior to adding them to the command
    interpreter.

    **INSTANCE ATTRIBUTES**

    *STR* name -- name of the command set (to be used for automatic 
    generation of documentation)

    *STR* description -- description of the command set (to be used 
    for automatic generation of documentation)

    *{STR: CSCmd}* commands -- map from unique command names to
    context-sensitive commands
    """
    def __init__(self, name, description = None, **args):
        """
        **INPUTS**

        *STR* name -- name of the command set (to be used for automatic 
        generation of documentation)

        *STR* description -- description of the command set (to be used 
        for automatic generation of documentation)
        """
        self.deep_construct(CSCmdSet,
                            {'name': name, 'description': description,
                             'commands': {}}, args)
    def add_csc(self, command, name = None):
        """add a context-sensitive command to the set

        **INPUTS**

        *CSCmd command* -- the command

        *STR name* -- a unique name for the command, or None to use the
        first item in the spoken form list

        **OUTPUTS**

        *none*
        """
        if name is None:
            name = command.spoken_forms[0]
        self.commands[name] = command

    def replace_spoken(self, name, spoken_forms):
        """replace the spoken forms of a command with the given name

        **INPUTS**

        *STR name* -- unique name of the command given when it was added

        *[STR] spoken_forms* -- the new spoken forms

        **OUTPUTS**

        *BOOL* -- true if a command by that name existed
        """
        try:
            command = self.commands[name]
            command.replace_spoken(spoken_forms)
        except KeyError:
            return 0
        return 1

    def add_spoken(self, name, spoken_forms):
        """add the given spoken forms to a command with the given name

        **INPUTS**

        *STR name* -- unique name of the command given when it was added

        *[STR] spoken_forms* -- the spoken forms to add

        **OUTPUTS**

        *BOOL* -- true if a command by that name existed
        """
        try:
            command = self.commands[name]
            command.add_spoken(spoken_forms)
        except KeyError:
            return 0
        return 1


    def remove_spoken(self, name, spoken_forms):
        """remove the given spoken forms of a command with the given name

        **INPUTS**

        *STR name* -- unique name of the command given when it was added

        *[STR] spoken_forms* -- the spoken forms to remove

        **OUTPUTS**

        *BOOL* -- true if a command by that name existed
        """
        try:
            command = self.commands[name]
            command.remove_spoken(spoken_forms)
        except KeyError:
            return 0
        return 1


    def remove_command(self, name):
        """remove a command with the given name

        **INPUTS**

        *STR name* -- unique name of the command given when it was added

        **OUTPUTS**

        *BOOL* -- true if a command by that name existed
        """
        try:
            del self.commands[name]
        except KeyError:
            return 0
        return 1

class LSAliasSet(Object):
    """a collection of language-specific aliases which may be deleted,
    renamed, or giving synonyms prior to adding them to the command
    interpreter.

    **INSTANCE ATTRIBUTES**

    *STR* name -- name of the alias set (to be used for automatic 
    generation of documentation)

    *STR* description -- description of the alias set (to be used 
    for automatic generation of documentation)

    *{STR: LSAlias}* aliases -- map from unique names to
    language-specific aliases
    """
    def __init__(self, name, description = None, **args):
        """
        **INPUTS**

        *STR* name -- name of the alias set (to be used for automatic 
        generation of documentation)

        *STR* description -- description of the alias set (to be used 
        for automatic generation of documentation)
        """
        self.deep_construct(LSAliasSet,
                            {'name': name, 'description': description,
                             'aliases': {}}, args)

    def add_lsa(self, alias, name = None):
        """add a language-specific alias to the set

        **INPUTS**

        *LSAlias alias* -- the alias

        *STR name* -- a unique name for the alias, or None to use the
        first item in the spoken form list

        **OUTPUTS**

        *none*
        """
        if name is None:
            name = alias.spoken_forms[0]
        self.aliases[name] = alias

    def replace_spoken(self, name, spoken_forms):
        """replace the spoken forms of an alias with the given name

        **INPUTS**

        *STR name* -- unique name of the alias given when it was added

        *[STR] spoken_forms* -- the new spoken forms

        **OUTPUTS**

        *BOOL* -- true if a command by that name existed
        """
        try:
            self.aliases[name].spoken_forms = spoken_forms[:]
        except KeyError:
            return 0
        return 1

    def add_spoken(self, name, spoken_forms):
        """add the given spoken forms to a command with the given name

        **INPUTS**

        *STR name* -- unique name of the command given when it was added

        *[STR] spoken_forms* -- the spoken forms to add

        **OUTPUTS**

        *BOOL* -- true if an alias by that name existed
        """
        try:
            alias = self.aliases[name]
        except KeyError:
            return 0
        for spoken in spoken_forms:
            alias.spoken_forms.append(spoken)
        return 1

    def remove_spoken(self, name, spoken_forms):
        """remove the given spoken forms of an alias with the given name

        **INPUTS**

        *STR name* -- unique name of the alias given when it was added

        *[STR] spoken_forms* -- the spoken forms to remove

        **OUTPUTS**

        *BOOL* -- true if an alias by that name existed
        """
        try:
            alias = self.aliases[name]
        except KeyError:
            return 0
        new_spoken = []
        for spoken in alias.spoken_forms:
            if spoken not in spoken_forms:
                new_spoken.append(spoken)
        alias.spoken_forms = new_spoken
        return 1


    def remove_alias(self, name):
        """remove an alias with the given name

        **INPUTS**

        *STR name* -- unique name of the alias given when it was added

        **OUTPUTS**

        *BOOL* -- true if an alias by that name existed
        """
        try:
            del self.aliases[name]
        except KeyError:
            return 0
        return 1

class CapitalizationWordSet(Object):
    """a collection of CapitalizationWord objects which may be deleted,
    renamed, or giving synonyms prior to adding them to the command
    interpreter.

    **INSTANCE ATTRIBUTES**

    *STR* name -- name of the set (to be used for automatic 
    generation of documentation)

    *STR* description -- description of the set (to be used 
    for automatic generation of documentation)

    *{STR: CapitalizationWord}* words -- map from unique names to
    CapitalizationWord objects
    """
    def __init__(self, name, description = None, **args):
        """
        **INPUTS**

        *STR* name -- name of the set (to be used for automatic 
        generation of documentation)

        *STR* description -- description of the set (to be used 
        for automatic generation of documentation)
        """
        self.deep_construct(CapitalizationWordSet,
                            {'name': name, 'description': description,
                             'words': {}}, args)

    def add_capitalization_word(self, word, name = None):
        """add a CapitalizationWord to the set

        **INPUTS**

        *CapitalizationWord word* -- the word

        *STR name* -- a unique name for the word, or None to use the
        first item in the spoken form list

        **OUTPUTS**

        *none*
        """
        if name is None:
            name = word.spoken_forms[0]
        self.words[name] = word

    def replace_spoken(self, name, spoken_forms):
        """replace the spoken forms of a word with the given name

        **INPUTS**

        *STR name* -- unique name of the alias given when it was added

        *[STR] spoken_forms* -- the new spoken forms

        **OUTPUTS**

        *BOOL* -- true if a command by that name existed
        """
        try:
            self.words[name].spoken_forms = spoken_forms[:]
        except KeyError:
            return 0
        return 1

    def add_spoken(self, name, spoken_forms):
        """add the given spoken forms to a command with the given name

        **INPUTS**

        *STR name* -- unique name of the command given when it was added

        *[STR] spoken_forms* -- the spoken forms to add

        **OUTPUTS**

        *BOOL* -- true if a word by that name existed
        """
        try:
            word = self.words[name]
        except KeyError:
            return 0
        for spoken in spoken_forms:
            word.spoken_forms.append(spoken)
        return 1

    def remove_spoken(self, name, spoken_forms):
        """remove the given spoken forms of a word with the given name

        **INPUTS**

        *STR name* -- unique name of the word given when it was added

        *[STR] spoken_forms* -- the spoken forms to remove

        **OUTPUTS**

        *BOOL* -- true if a word by that name existed
        """
        try:
            word = self.words[name]
        except KeyError:
            return 0
        new_spoken = []
        for spoken in word.spoken_forms:
            if spoken not in spoken_forms:
                new_spoken.append(spoken)
        word.spoken_forms = new_spoken
        return 1

    def remove_word(self, name):
        """remove a word with the given name

        **INPUTS**

        *STR name* -- unique name of the word given when it was added

        **OUTPUTS**

        *BOOL* -- true if a word by that name existed
        """
        try:
            del self.words[name]
        except KeyError:
            return 0
        return 1

class SymWord(symbol_formatting.SymElement):
    """a word as an element of a symbol 

    **INSTANCE ATTRIBUTES**

    *STR word* -- the word (possibly abbreviated)

    *STR original* -- original, unabbreviated version (if word is an
    abbreviation/substitution) or None if word is not abbreviated
    """
    def __init__(self, word, original = None, **args):
        self.deep_construct(SymWord,
                            {
                             'word': word,
                             'original': original
                            },
                            args)

    def add_to(self, builder):
        """Add alias's written form to the symbol builder

        **INPUTS**

        *SymBuilder builder*

        **OUTPUTS**

        *none*
        """
        match = re.match(r'([a-zA-Z])\.{0,1}$', self.word)
        if match:
            letter = match.group(1)
            spoken = "%s." % string.upper(letter) 
            builder.add_letter(string.lower(letter), spoken)
        else:
            builder.add_word(self.word, self.original)

class NoSeparator(symbol_formatting.SymElement):
    """a symbol element which suppresses any separator before the next
    word in the symbol
    """
    def __init__(self, **args):
        self.deep_construct(NoSeparator, {}, args)

    def add_to(self, builder):
        """suppress any separator before the next word in the symbol

        **INPUTS**

        *SymBuilder builder*

        **OUTPUTS**

        *none*
        """
        builder.suppress_separator()

class NoAbbreviation(symbol_formatting.SymElement):
    """a symbol element which suppresses abbreviation of the next
    word in the symbol
    """
    def __init__(self, **args):
        self.deep_construct(NoAbbreviation, {}, args)

    def add_to(self, builder):
        """suppress any abbreviation of the next word in the symbol

        **INPUTS**

        *SymBuilder builder*

        **OUTPUTS**

        *none*
        """
        builder.suppress_abbreviation()

class InterpState(OwnerObject):
    """interface by which CSC actions can modify aspects of the
    interpreter state to affect subsequent commands or the
    interpretation process itself.
    
    examples:
    - Hungarian Notation et al modifies the formatting style of the next
      symbol
    - No-Space will modify the spacing state (once the spacing engine is
      implemented)

    InterpState just provides methods which return other interface
    objects.  The purpose of this architecture is to 
    organize related interpreter state methods, while avoiding the need
    to change the signature of the execute method whenever a new set of
    methods are added

    Note: InterpState retains ownership of all returned objects
    """
    def __init__(self, sym_style, **args):
        """
        **INPUTS**

        *SymStyling sym_style* -- object providing the symbol styling 
        interface
        """
        self.deep_construct(InterpState, 
                            {
                             'sym_style': sym_style
                            },
                            args)
        self.add_owned('sym_style')

    def styling_state(self):
        """Returns a reference to an object providing the symbol styling 
        interface

        Note: InterpState retains ownership of the SymStyling object
        """
        return self.sym_style

class SymStyling(OwnerObject):
    """interface to the symbol styling methods of CmdInterp

    """
    def __init__(self, builder_factory, **args):
        self.deep_construct(SymStyling, 
            {'builder_factory': builder_factory}, args)

    def expect(self, identifier):
        """method used to tell the SymBuilderFactory to expect a
        particular type of identifier

        **INPUTS**

        *STR identifier* -- name of the identifier type, or None for a
        generic identifier

        **OUTPUTS**

        *BOOL* -- true if the identifier is known
        """
        return self.builder_factory.expect(identifier)

    def prefer(self, builder):
        """method used to tell the SymBuilderFactory that a CSC has
        given an explicit preference for particular SymBuilder to be
        used for the next symbol

        **INPUTS**

        *STR identifier* -- name of the identifier type, or None for a
        generic identifier

        **OUTPUTS**

        *BOOL* -- true if the identifier is known
        """
        return self.builder_factory.prefer(builder)

    def clear(self):
        """clear expectations and preferences for the next identifier

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        return self.builder_factory.clear()
    
class CmdInterp(OwnerObject):
    """Interprets Context Sensitive Commands spoken into a given application.
    
    **INSTANCE ATTRIBUTES**

    *NewMediatorObject mediator* -- reference to the parent mediator
    which owns this CmdInterp instance

    WordTrie *commands* -- WordTrie mapping spoken form phrases to 
    CSCmdDict objects which contain the data on mappings from Context to
    Action

    [SymDict] *known_symbols* -- dictionary of known symbols
    
    {STR: WordTrie} *language_specific_aliases = {}* -- Key is the name of
     a programming language (None means all languages). Value is a
     WordTrie of AliasMeaning objects over spoken form phrases

    *SymBuilderFactory builder_factory* -- factory for creating new
    SymBuilder objects

    *InterpState state_interface* -- interface passed to
    Action.log_execute, allowing it to affect the interpreter state for
    subsequent commands

    *SymStyling styling_state* -- interface which allows actions 
    affect the formatting style of the next symbol

    BOOL *disable_dlg_select_symbol_matches = None* -- If true, then
    do not prompt the user for confirmation of new symbols.
    
    BOOL *add_sr_entries_for_LSAs_and_CSCs* -- if *TRUE*, then add 
    SR entries for the LSAs and CSCs when they are added. If *FALSE*, 
    assume that these entries were already added by an previous instance
    of the mediator. This is mostly used for regression testing purposes
    where we create a new mediator in each test, and don't want to waste
    CPU time adding the same LSAs and CSCs over and over again.

    CLASS ATTRIBUTES**

    *none* --
        
    .. [AppState] file:///./AppState.AppState.html
    .. [Context] file:///./Context.Context.html
    .. [SymDict] file:///./SymDict.SymDict.html"""
    
    def __init__(self, sym_file = None,
                 disable_dlg_select_symbol_matches = None, mediator =
                 None, **attrs):
        
        """
        **INPUTS**

        *STR sym_file = None* -- File used for
        reading/writing the symbol dictionary. If *None*, then don't
        read/write the symbol dictionary from/to file.

        *BOOL disable_dlg_select_symbol_matches = None* -- If true, then
        do not prompt the user for confirmation of new symbols.

        *NewMediatorObject mediator* -- reference to the parent mediator
        which owns this CmdInterp instance
        """

        self.deep_construct(CmdInterp,
                            {'mediator': mediator,
                             'commands': WordTrie.WordTrie(), 
                             'known_symbols': None,
                             'language_specific_aliases': \
                                 {None: WordTrie.WordTrie()},
                             'builder_factory':
                                 symbol_formatting.SymBuilderFactory(),
                             'state_interface': None,
                             'disable_dlg_select_symbol_matches': disable_dlg_select_symbol_matches,
                             'add_sr_entries_for_LSAs_and_CSCs': 1},
                            attrs)
        self.name_parent('mediator')
        self.add_owned('known_symbols')
        self.add_owned('state_interface')
        self.known_symbols = SymDict.SymDict(sym_file = sym_file, interp = self)
        self.styling_state = SymStyling(self.builder_factory)
        self.state_interface = InterpState(self.styling_state)

    def set_mediator(self, mediator):
        """sets the parent mediator which owns this CmdInterp instance

        **INPUTS**

        *NewMediatorObject mediator* -- reference to the parent mediator
        which owns this CmdInterp instance

        **OUTPUTS**

        *none*
        """
        self.mediator = mediator

    def input_error(self, message, fatal = 0):
        """sends a message to NewMediatorObject indicating that a
        serious error occurred while trying to read SymDict information 
        from the persistent dictionary file.  If a GUI is available, the
        message should be displayed in a dialog box before the rest of
        the GUI and server starts.  Otherwise, the message should be
        sent to stderr

        **INPUTS**

        *STR message* -- the message to display

        *BOOL fatal* -- if true, the error is fatal and the mediator
        should clean up and exit the user has confirmed seeing it

        **OUTPUTS**

        *none*
        """
        if self.mediator:
            self.mediator.input_error(message, fatal = fatal)

    def user_message(self, message, instance = None):
        """sends a user message up the chain to the NewMediatorObject to
        be displayed

        **INPUTS**

        *STR message* -- the message

        *STR instance_name* -- the editor from which the message
        originated, or None if it is not associated with a specific
        editor.

        **OUTPUTS**

        *none*
        """
        if self.mediator:
            self.mediator.user_message(message, instance = instance)

    def spoken_form_regexp(self, spoken_form):
        """Returns a regexp that matches a spoken form of a command.

        *STR spoken_form* is the spoken form. The returned regexp will match
        it even if the case of the first letter of each word do not match."""

        words = re.split('\s+', spoken_form)
        regexp = ''
        for aword in words:
            first = aword[0]
            rest = aword[1:]
            regexp_this_word = '[' + string.lower(first) + string.upper(first) + ']' + rest
            if not regexp == '':
                regexp = regexp + '\s*'
            regexp = regexp + regexp_this_word
        return regexp

    def interpret_massaged(self, cmd, app, initial_buffer = None):
        """Interprets a natural language command and executes
        corresponding instructions.

        *[(STR, STR)]* cmd -- The command,  a list of
         tuples of (spoken_form, written_form), with the spoken form
         cleaned and the written form cleaned for VoiceCode.

        *AppState app* -- the AppState interface to the editor
        
        *[STR] initial_buffer* -- The name of the target buffer at the 
        start of the utterance.  Some CSCs may change the target buffer of 
        subsequent parts of the command.  If None, then the current buffer 
        will be used.
        
        """
        trace('CmdInterp.interpret_massaged', 'command=%s' % cmd)
        spoken_list = map(lambda word: word[0], cmd)
#        spoken_list = map(lambda word: process_initials(word[0]), cmd)
        trace('CmdInterp.interpret_massaged', 'spoken=%s' % spoken_list)
        self.interpret_spoken(spoken_list, app, initial_buffer = initial_buffer)

    def interpret_spoken(self, spoken_list, app, initial_buffer = None):
        """Interprets a natural language command and executes
        corresponding instructions.

        *[STR]* spoken_list -- The list of spoken forms in the command

        *AppState app* -- the AppState interface to the editor
        
        *[STR] initial_buffer* -- The name of the target buffer at the 
        start of the utterance.  Some CSCs may change the target buffer of 
        subsequent parts of the command.  If None, then the current buffer 
        will be used.
        
        """
        trace('CmdInterp.interpret_spoken', 'spoken_list = %s' % spoken_list)

        spoken = string.join(spoken_list)
        phrase = string.split(spoken)
        self.interpret_phrase(phrase, app, initial_buffer = initial_buffer)

    def interpret_phrase(self, phrase, app, initial_buffer = None):
        """Interprets a natural language command and executes
        corresponding instructions.

        *[STR]* phrase -- The list of spoken words in the command, without
        regard to the original boundaries between words as interpreted
        by the speech engine

        *AppState app* -- the AppState interface to the editor
        
        *[STR] initial_buffer* -- The name of the target buffer at the 
        start of the utterance.  Some CSCs may change the target buffer of 
        subsequent parts of the command.  If None, then the current buffer 
        will be used.
        
        """
        trace('CmdInterp.interpret_phrase', 'phrase = %s' % phrase)

        processed_phrase = map(lambda word: process_initials(word), phrase)

        if initial_buffer == None:
            app.bind_to_buffer(app.curr_buffer_name())
        else:
            app.bind_to_buffer(initial_buffer)

        untranslated_words = []

# eventually, we will want to allow expectations and possibly explicit
# formatting commands to persist across utterances if the buffer and
# cursor position have not changed.  However, that requires a system for
# detecting these changes, which doesn't exist yet, so for now we just
# reset the state when we start interpreting a new utterance
        self.styling_state.clear()
        builder = None

# flag indicating whether untranslated words consists of an exact match
# of the spoken form to an existing symbol
        exact_symbol = 0

        new_symbol = 0
        
        #
        # Process the beginning of the command until there is nothing
        # left
        #

        while len(phrase) > 0:
            trace('CmdInterp.interpret_phrase', 
                'now, phrase = %s' % phrase)
            trace('CmdInterp.interpret_phrase', 
                'processed phrase = %s' % processed_phrase)

            #
            # Identify leading CSC, LSA, symbol and ordinary word
            #
            possible_CSCs = self.chop_CSC_phrase(processed_phrase, app)

            aliases = self.language_specific_aliases
            language = app.active_language()
            chopped_LSA = ""
            LSA_consumes = 0
            if aliases.has_key(language):
                chopped_LSA, LSA_consumes = \
                    self.chop_LSA_phrase(processed_phrase, aliases[language])
            chopped_generic_LSA, generic_LSA_consumes = \
                self.chop_LSA_phrase(processed_phrase, aliases[None])

            if LSA_consumes < generic_LSA_consumes:
                chopped_LSA = chopped_generic_LSA
                LSA_consumes = generic_LSA_consumes

            chopped_symbol, symbol_consumes = \
                self.chop_symbol_phrase(processed_phrase)

            chopped_word = phrase[0]
            word_consumes = 1

            most_definite = max((LSA_consumes, symbol_consumes, word_consumes))

            trace('CmdInterp.interpret_phrase', 
            'possible_CSCs=%s, chopped_LSA=%s, LSA_consumes=%s, chopped_symbol=%s, symbol_consumes=%s, chopped_word=%s, word_consumes=%s' % (possible_CSCs, chopped_LSA, LSA_consumes, chopped_symbol, symbol_consumes, chopped_word, word_consumes))
            trace('CmdInterp.interpret_phrase', 
                'most_definite = %d' % most_definite)
            head_was_translated = 0

            #
            # Translate CSC, LSA, symbol or ordinary word at head of command.
            #
            # If more than one translations are possible, choose the one
            # that consumes the most words from the command.
            #
            # In case of ties, use this order of priority: CSC, LSA, symbol,
            # ordinary words. This order goes from most specific to least
            # specific, i.e.
            #
            # - CSCs usually apply in very restricted contexts only
            # - LSAs usually apply for a specific language only
            # - Symbols are restricted to sequences of words that are the
            #   spoken form of a known symbol
            # - ordinary words can be anything
            #
            csc_applies = 0

            CSC_consumes = self.apply_CSC(app, possible_CSCs, processed_phrase, 
                most_definite, builder, untranslated_words, 
                exact_symbol, new_symbol)
            if CSC_consumes:
                phrase = phrase[CSC_consumes:]
                processed_phrase = processed_phrase[CSC_consumes:]
                head_was_translated = 1
                untranslated_words = []
                builder = None
                exact_symbol = 0
                new_symbol = 0

            if not head_was_translated and LSA_consumes == most_definite:
                #
                # LSA consumed the most words from command. Insert it.
                #
                trace('CmdInterp.interpret_phrase', 'processing leading LSA=\'%s\'' % chopped_LSA)
                preceding_symbol = 0
                if builder and not builder.empty():
                    preceding_symbol = 1
                if not chopped_LSA.interp_now(preceding_symbol):
                    if chopped_LSA.written():
                        untranslated_words.append(chopped_LSA.written())
                    else:
                        new_symbol = 1
                    spoken_form = processed_phrase[:LSA_consumes]
                    element = \
                        chopped_LSA.make_element(string.join(spoken_form))
                    if not builder:
                        builder = self.new_builder(app)
                    element.add_to(builder)
                else:
# flush untranslated words before inserting LSA
                    if builder:
                        self.match_untranslated_text(builder, 
                            untranslated_words, app, exact_symbol,
                            new_symbol)
                        untranslated_words = []
                        builder = None
                        exact_symbol = 0
                        new_symbol = 0
                    actions_gen.ActionInsert(code_bef=chopped_LSA.written(), 
                        code_after='').log_execute(app, None, self.state_interface)
                phrase = phrase[LSA_consumes:]
                processed_phrase = processed_phrase[LSA_consumes:]
                head_was_translated = 1


            if not head_was_translated and symbol_consumes == most_definite:
                #
                # Symbol consumed the most words from command. Insert it.
                #
                # Note: known symbols are inserted as untranslated
                #       text because often, the user will create new
                #       symbols by prefixing/postfixing existing ones.
                #       For example, if you define a subclass of a known
                #       class SomeClass you may name the new class
                #       SomeprefixSomeClass or SomeClassSomepostfix.
                #
                trace('CmdInterp.interpret_phrase', 'processing leading symbol=\'%s\'' % chopped_symbol)
                if untranslated_words:
                    exact_symbol = 0
                else:
                    exact_symbol = 1
                untranslated_words.append(chopped_symbol)
                if not builder:
                    builder = self.new_builder(app)
                spoken_list = string.split(chopped_symbol)
                trace('CmdInterp.interpret_phrase', 
                    'symbol breaks into %s' % repr(spoken_list))
                for word in spoken_list:
                    word_element = self.make_word_element(word)
                    word_element.add_to(builder)

                phrase = phrase[symbol_consumes:]
                processed_phrase = processed_phrase[symbol_consumes:]
                head_was_translated = 1
                                         
                   
            if not head_was_translated and word_consumes == most_definite:
                #
                # Nothing special translated at begining of command.
                # Just chop off the first word and insert it, marking
                # it as untranslated text.
                #                 
                trace('CmdInterp.interpret_phrase', 'processing leading word=\'%s\'' % chopped_word)
                untranslated_words.append(process_initials(chopped_word))
                exact_symbol = 0
                if not builder:
                    builder = self.new_builder(app)
                word_element = self.make_word_element(chopped_word)
                word_element.add_to(builder)

                phrase = phrase[word_consumes:]
                processed_phrase = processed_phrase[word_consumes:]
                head_was_translated = 1

            #
            # Finished translating head of command.
            #
            # Check if it marked the end of some untranslated text
            #
            if (len(phrase) == 0) and untranslated_words:
                #
                # A CSC or LSA was translated, or we reached end of the
                # command, thus marking the end of a sequence of untranslated
                # text. Try to match untranslated text to a known (or new)
                # symbol.
                #
                trace('CmdInterp.interpret_phrase', 'found the end of some untranslated text')
                self.match_untranslated_text(builder, 
                    untranslated_words, app, exact_symbol, new_symbol)
                builder = None
                untranslated_words = []
                exact_symbol = 0
                new_symbol = 0

            if untranslated_words:
                untranslated_text = string.join(untranslated_words)
            else:
                untranslated_text = None
            trace('CmdInterp.interpret_phrase', 'End of *while* iteration. untranslated_text=\'%s\', app.curr_buffer().cur_pos=%s' % (untranslated_text, app.curr_buffer().cur_pos()))

        # make sure to unbind the buffer before returning
        app.unbind_from_buffer()

        #
        # Notify external editor of the end of recognition
        #
        app.recog_end()

    def apply_CSC(self, app, possible_CSCs, spoken_list,
        most_definite, builder, untranslated_words, exact_symbol,
        new_symbol):
        """check which CSCs apply and execute the greediest one

        **INPUTS**

        *AppState app* -- the target application

        *[STR] spoken_list* -- list of spoken words

        *[(CSCmdDict, INT)] possible_CSCs* -- the possible CSCmds which
        might apply, together with the number of words they consume, in
        order of descending greediness

        *INT most_definite* -- the most words which would be consumed by
        those constructs which definitely apply (i.e. LSAs in the
        current language and known symbols)

        *SymBuilder builder* -- symbol builder for any
        untranslated words

        *[STR] untranslated_words -- list of untranslated words which
        would need to be flushed before the CSC

        *BOOL exact_symbol* -- true if the untranslated words are an
        exact match to a known symbol

        *BOOL new_symbol* -- true if the untranslated words include
        manual formatting and therefore should not be loosely matched to
        an existing symbol

        **OUTPUTS**

        *INT* -- the number of words actually consumed (0 if no CSC
        consuming more than most_definite applies)
        """
        preceding_symbol = 0
        if untranslated_words:
            preceding_symbol = 1
        for match in possible_CSCs:
            meanings, CSC_consumes = match
            trace('CmdInterp.apply_CSC', 
                'possible CSC %s, consumes %d' % \
                (meanings, CSC_consumes))
            if CSC_consumes < most_definite:
# LSA or symbol consumes more than the rest of the CSCs, so defer to
# them
                return 0
            applicable = meanings.applies(app, preceding_symbol)
            if not applicable:
                continue
            context, action = applicable[0]
            trace('CmdInterp.apply_CSC', 
                'len(applicable) = %d' % len(applicable))
            if len(applicable) > 1:
                msg = 'Configuration Warning: phrase %s\n' \
                    % spoken_list[:CSC_consumes]
                msg = msg + \
                    'has more than one applicable context with the same'
                msg = msg + '\nscope %s:\n' % context.scope()
                for context, action in applicable:
                    msg = msg + 'context: %s, action: %s\n' \
                        % (context, action)
                msg = msg + 'Applying the first context'
                config_warning(msg)
            csc_applies = 1
# flush untranslated words before executing action
            if untranslated_words:
                self.match_untranslated_text(builder, 
                    untranslated_words, app, exact_symbol, new_symbol)
# Eventually, we may want some of the styling state to persist across
# some CSCs.  However, it is not clear how to achieve that, so for now, 
# we just reset the state before executing the action
            self.styling_state.clear()
            action.log_execute(app, context, self.state_interface)
            return CSC_consumes
        return 0


    def interpret_NL_cmd(self, cmd, app, initial_buffer = None):
        
        """Interprets a natural language command and executes
        corresponding instructions.

        *[STR] cmd* -- The command. It is a list of written\spoken words.

        *AppState app* -- the AppState interface to the editor
        
        *[STR] initial_buffer* -- The name of the target buffer at the 
        start of the utterance.  Some CSCs may change the target buffer of 
        subsequent parts of the command.  If None, then the current buffer 
        will be used.
        
        """
        trace('CmdInterp.interpret_NL_cmd', 'pre-massaged cmd=%s' % cmd)
        cmd = self.massage_command(cmd)
        trace('CmdInterp.interpret_NL_cmd', 'post-massaged cmd=%s' % cmd)
        self.interpret_massaged(cmd, app, initial_buffer = initial_buffer)

    def interpret_cmd_tuples(self, cmd, app, initial_buffer = None):
        """Interprets a natural language command and executes
        corresponding instructions.

        **INPUTS**

        *[(STR, STR)]* cmd -- The command to be massaged. It's a list of
         tuples of (spoken_form, written_form), with the written form
         already cleaned for VoiceCode.
        
        *AppState app* -- the AppState interface to the editor
        
        *[STR] initial_buffer* -- The name of the target buffer at the 
        start of the utterance.  Some CSCs may change the target buffer of 
        subsequent parts of the command.  If None, then the current buffer 
        will be used.

        **OUTPUTS**

        *none*
        """
        cmd = self.massage_command_tuples(cmd)
        self.interpret_massaged(cmd, app, initial_buffer = initial_buffer)

    def massage_command_tuples(self, command_tuples):
        """Massages a command to prepare it for interpretation.

        Makes sure to substitute special characters (e.g. {Spacebar})
        in the written form of words in the command. Also, makes sure
        that the spoken forms are all lowercase, and contain no
        multiple, leading or trailing blanks.
        
        **INPUTS**
        
        *[(STR, STR)]* cmd -- The command to be massaged. It's a list of
         tuples of (spoken_form, written_form), with the written form
         already cleaned for VoiceCode.
        
        **OUTPUTS**
        
        *[(STR, STR)]* -- The massaged command
        """
        mod_command = []
        trace('CmdInterp.massage_command_tuples', 
            'pre-massaged cmd=%s' % command_tuples)
        for a_word in command_tuples:
            spoken, written = a_word
            spoken = sr_interface.clean_spoken_form(spoken)
            mod_command.append((spoken, written))
        return mod_command

    def massage_command(self, command):
        """Massages a command to prepare it for interpretation.

        Makes sure to substitute special characters (e.g. {Spacebar})
        in the written form of words in the command. Also, makes sure
        that the spoken forms are all lowercase, and contain no
        multiple, leading or trailing blanks.
        
        **INPUTS**
        
        *[STR]* command -- The command to be massaged. It's a list of
         written\spoken words.
        
        **OUTPUTS**
        
        *[(STR, STR)]* -- The massaged command
        """
        command_tuples = []
        for a_word in command:
            spoken, written = sr_interface.spoken_written_form(a_word,
                clean_spoken = 0)
            command_tuples.append((spoken, written))
        return self.massage_command_tuples(command_tuples)

    def match_untranslated_text(self, builder, 
        untranslated_words, app, exact_symbol = 0, new_symbol = 0):
        """Tries to match last sequence of untranslated text to a symbol.
        
        **INPUTS**
        
        *[STR]* untranslated_words -- list of untranslated words

        *AppState* app -- editor into which the command was spoken

        *SymBuilder builder* -- symbol builder for any
        untranslated words

        *[STR] untranslated_words -- list of untranslated words which
        would need to be flushed before the CSC

        *BOOL* exact_symbol -- true if the untranslated text was an
        exact match for the spoken form of a symbol

        **OUTPUTS**
        
        *none* -- 
        """
        
        untranslated_text = string.join(untranslated_words)
        trace('CmdInterp.match_untranslated_text', 'untranslated_text=\'%s\'' % (untranslated_text))

        if exact_symbol and not new_symbol:
            spoken_form = untranslated_text
            trace('CmdInterp.match_untranslated_text', 
                'exact symbol spoken "%s"' % (spoken_form))
            phrase = string.split(spoken_form)
            complete_match = self.known_symbols.complete_match(phrase)
            if complete_match:
                written_symbol = self.choose_best_symbol(spoken_form, 
                    complete_match)
                trace('CmdInterp.match_untranslated_text', 
                    'exact symbol written "%s"' % (untranslated_text))
                actions_gen.ActionInsert(code_bef=written_symbol,
                    code_after='').log_execute(app, None, self.state_interface)
                return
            else:
                msg = "CmdInterp says there was an exact match to a known\n"
                msg = msg + "symbol, but SymDict is not finding any"
                msg = msg + "complete match:\n"
                msg = msg + "match_phrase gives %s\n" \
                    % self.known_symbols.match_phrase(phrase)
                sys.stderr.write(msg)
        # Match untranslated text to new known symbol or a known symbol with
        # unresolved spoken forms.
        #
        # Don't bother the user if the untranslated text is just the written
        # form of a known symbol or if it's a number
        #
        reg = '[\d\s]+'
        num_match = re.match(reg, untranslated_text)
        if num_match:
            untranslated_text = re.sub('\s', '', untranslated_text)        
            actions_gen.ActionInsert(code_bef=untranslated_text,
            code_after='').log_execute(app, None, self.state_interface)                            
            return

        symbol_matches = None
        trace('CmdInterp.match_untranslated_text', 'new_symbol=%s' % new_symbol)
        if not new_symbol:
            symbol_matches = self.known_symbols.match_pseudo_symbol(untranslated_text)
            trace('CmdInterp.match_untranslated_text', 'symbol_matches=%s' % symbol_matches)
        if symbol_matches:
            actions_gen.ActionInsert(code_bef=symbol_matches[0].native_symbol,
                code_after='').log_execute(app, None, self.state_interface)
#            self.dlg_select_symbol_match(untranslated_text, 
#                symbol_matches, app)
        else:
            symbol = builder.finish()
            actions_gen.ActionInsert(code_bef=symbol,
                code_after='').log_execute(app, None, self.state_interface)
            self.known_symbols.add_symbol(symbol, [builder.spoken_form()])
        

    def new_builder(self, app):
        """create a new SymBuilder object to generate new
        symbols

        **INPUTS**

        *AppState app* -- the AppState interface to the editor

        **OUTPUTS**

        *SymBuilder* -- the new symbol builder
        """
        buff = app.curr_buffer()
        return self.builder_factory.new_builder(buff)

    def add_identifier(self, identifier, parent = None):
        """defines a new identifier type for the SymBuilderFactory

        *STR identifier* -- name of the new identifier type (must NOT be
        a known identifier type, or a RuntimeError will be raised)

        *STR parent* -- name of the parent (must be a known identifier
        type, or None, or a RuntimeError will be raised)

        **OUTPUTS**
        """
        self.builder_factory.add_identifier(identifier, parent = parent)
 
    def set_builder_preferences(self, builders, identifier = None, 
        language = None):
        """establishes the preferred order for symbol formatting styles
        for a given language and identifier type

        **INPUTS**

        *[STR] builders* -- prioritized list of names of registered SymBuilder
        objects. If one of the builders is unknown, set_preferences raises 
        a RuntimeError.

        *STR identifier* -- name of the identifier to which these
        preference apply, or None to set general preferences for all
        identifiers without their own preferences.  If the identifier type 
        is unknown, set_preferences raises a RuntimeError.

        *STR language* -- name of the language to which these
        preference apply, or None to set general preferences for all
        languages
        """
        self.builder_factory.set_preferences(builders, identifier =
            identifier, language = language)

    def make_word_element(self, word):
        """creates a SymWord symbol element corresponding to a word

        **INPUTS**

        *STR word* -- the original, unabbreviated form of the word

        **OUTPUTS**

        *SymWord* -- the new symbol element
        """
        trace('CmdInterp.make_word_element', 'word = %s' % repr(word))
        abbreviations = self.known_symbols.preferred_abbreviations(word)
        trace('CmdInterp.make_word_element', 'abbreviations = %s' % repr(abbreviations))
        return SymWord(abbreviations[0], original = word)

    def enable_symbol_match_dlg(self, enable = 1):
        """enables or disables the symbol match dialog

        **INPUTS**

        *BOOL* enable -- 1 to enable the dialog, 0 to disable it

        **OUTPUTS**

        *BOOL* -- previous status of the dialog
        """
        current = not self.disable_dlg_select_symbol_matches
        self.disable_dlg_select_symbol_matches = not enable
        return current

    def dlg_select_symbol_match(self, untranslated_text, symbol_matches, app):
        """Asks the user to select a match for pseudo symbol.
        
        **INPUTS**

        *STR* untranslated_text -- untranslated form of the text which
        matched
        
        *[SymbolMatch]* symbol_matches -- List of possible matches.
        

        **OUTPUTS**
        
        *none* -- 

        .. [SymbolMatch] file:///./SymDict.SymbolMatch.html"""
        

        trace('CmdInterp.dlg_select_symbol_match', 'self.disable_dlg_select_symbol_matches=%s' % self.disable_dlg_select_symbol_matches)

        if self.disable_dlg_select_symbol_matches:
            choice_index = 0
        else:
            good_answer = 0
            while not good_answer:
                print 'Associate \'%s\' with symbol (Enter selection):\n' % untranslated_text
                print '  \'0\': no association'
                ii = 1
                for a_match in symbol_matches:
                    sys.stdout.write('  \'%s\': %s' % (ii, a_match.native_symbol))
                    if a_match.is_new:
                        sys.stdout.write(' (*new*)')
                    sys.stdout.write('\n')
                    ii = ii + 1
                sys.stdout.write('\n> ')
                answer = sys.stdin.readline()
                answer_match = re.match('\s*([\d])+\s*', answer)
                if not answer_match:
                    trace('CmdInterp.dlg_select_symbol_match', 'no match')
                else:
                    trace('CmdInterp.dlg_select_symbol_match', 'answer=%s, answer_match=%s, answer_match.groups()=%s' % (answer, answer_match, answer_match.groups()))
                    choice_index = int(answer_match.group(1)) - 1
                    if choice_index < len(symbol_matches) and choice_index >= -1:
                        good_answer = 1
                if not good_answer:
                    print 'Invalid answer \'%s\'' % answer
                    
        #
        # Accept the match
        #
        trace('CmdInterp.dlg_select_symbol_match', 'choice_index=%s' % choice_index)
#        print '-- CmdInterp.dlg_select_symbol_match: choice_index=%s' % choice_index
        if choice_index >= 0:
            #
            # A match was chosen. Accept it and type it instead of the
            # untranslated text.
            #
            chosen_match = symbol_matches[choice_index]
# do this only on correction.  We'll have to add something to add
# symbols tentatively when they've been dictated but not
# corrected, but in that case, we should never add abbreviations (which
# accept_symbol_match does)
#            self.known_symbols.accept_symbol_match(chosen_match)            

            #
            # Insert matched symbol
            #
            actions_gen.ActionInsert(code_bef=chosen_match.native_symbol,
            code_after='').log_execute(app, None, self.state_interface)            
            if choice_index != 0:
                trace('CmdInterp.dlg_select_symbol_match.mismatch', 
                'selected alternative match %d: %s' % \
                (choice_index, chosen_match.native_symbol))
        else:
            actions_gen.ActionInsert(code_bef=untranslated_text,
            code_after='').log_execute(app, None, self.state_interface)                        
            if untranslated_text != symbol_matches[0].native_symbol:
                trace('CmdInterp.dlg_select_symbol_match.mismatch', 
                'untranslated text %s != first match %s' % \
                (untranslated_text, symbol_matches[0].native_symbol))
        
    def chop_CSC_phrase(self, phrase, app):
        """Chops the start of a command if it starts with a CSC.
        
        **INPUTS**
        
        *[STR]* phrase -- The list of spoken words in the command, without
        regard to the original boundaries between words as interpreted
        by the speech engine

        **OUTPUTS**

        Returns a list of tuples, each of the form 
        *(meanings, consumed)*, where:
        
        *CSCmdDict meanings* -- the meanings corresponding to the spoken
        form chopped off.

        *INT* consumed* -- Number of words consumed by the CSC from
         the command

        The list is sorted in order of descending numbers of words
        consumed
        """
        matches = self.commands.all_matches(phrase)
        trace('CmdInterp.chop_CSC_phrase',
            '%d matches' % len(matches))
        match_consumed = []
        for match in matches:
            cmd_dict, rest_spoken = match
            consumed = len(phrase) - len(rest_spoken)
            trace('CmdInterp.chop_CSC_phrase',
                'words = %d, phrase = %s' % (consumed,
                phrase[:consumed]))
            match_consumed.append((cmd_dict, consumed))

        return match_consumed
                    
    def chop_LSA_phrase(self, phrase, aliases):
        """Chops off the beginning of a command if it is an LSA.
        
        **INPUTS**
        
        *[STR]* phrase -- The list of spoken words in the command, without
        regard to the original boundaries between words as interpreted
        by the speech engine

        *WordTrie* aliases -- the set of aliases to use for the match

        **OUTPUTS**

        Returns a tuple *(chopped_LSA, consumed)* where:
        
        *AliasMeaning* chopped_LSA -- The AliasMeaning object
        corresponding to the LSA that was chopped off.  If *None*, it 
        means *command* did not start with an LSA.

        *INT* consumed* -- Number of words consumed by the LSA from
         the command
        """
        # See if spoken_form is in the list of active LSAs
        #

        match = aliases.match_phrase(phrase)
        if match[0] is None:
            return None, 0
        meaning, rest_spoken = match
        consumed = len(phrase) - len(rest_spoken)
        return meaning, consumed
    
    def chop_symbol_phrase(self, phrase):
        """Chops off the beginning of a command if it is a known symbol.
        
        **INPUTS**
        
        *[STR]* phrase -- The list of spoken words in the command, without
        regard to the original boundaries between words as interpreted
        by the speech engine

        **OUTPUTS**

        Returns a tuple *(chopped_symbol, consumed)* where:
        
        *STR chopped_symbol* -- spoken form of the known symbol, or None 
        if no symbol matches the spoken form. If *None*, it means 
        *command* did not start with a known symbol.

        *INT* consumed* -- Number of words consumed by the symbol from
         the command
        """
        match = self.known_symbols.match_phrase(phrase)
#        print match
        if match[0] is None:
            return None, 0
        symbols, rest_spoken = match
        consumed = len(phrase) - len(rest_spoken)
        consumed_words = phrase[:consumed]
        return string.join(consumed_words), consumed
                
    def whole_words(self, spoken_list, consumed_words):
        """Checks whether a list of words chopped off the spoken
        list consists of a whole number of words as returned by the
        speech engine
        
        **INPUTS**
        
        *[STR]* spoken_list -- The list of spoken forms in the command

        *[STR]* consumed_words -- The list of words which would be
        consumed 

        **OUTPUTS**

        (*BOOL*, *INT*) -- if the consumed_words consist of a whole
        number N of words from spoken_list, returns a tuple of (1, N).
        Otherwise, returns (0, M) where M is the index of the last
        partial word from spoken_list consumed by consumed_words
        """
        spoken = string.join(spoken_list)
        consumed_phrase = string.join(consumed_words)
        chars_consumed = len(consumed_phrase)
        consumed = 0
        total = -1
#        print 'len(spoken) = %d' % chars_consumed
        for i in range(len(spoken_list)):
#            print total, spoken_list[:i]
            total = total + len(spoken_list[i]) + 1
            if total == chars_consumed:
                consumed = i + 1
                return 1, consumed
            if total > chars_consumed:
                return 0, i
        raise RuntimeError('total length of command less than length consumed!')
        
    def choose_best_symbol(self, spoken_form, choices):
        """Chooses the best match for a spoken form of a symbol.

        For now, we just choose the first item in *choices*, but in
        the future, we might choose the one that appears closest to
        the cursor, or the one that used most recently, or the one
        that best matches the spoken form.
        
        **INPUTS**
        
        *STR* spoken_form -- spoken form of the symbol. 
        
        *[STR]* choices -- list of written forms of symbols having this
        spoken form

        **OUTPUTS**
        
        *none* -- 
        """

        return choices[0]

    def index_csc(self, acmd):
        """Add a new csc to the command interpreter's command dictionary

        [CSCmd] *acmd* is the command to be indexed.

        .. [CSCmd] file:///./CSCmd.CSCmd.html"""

#        debug.trace('CmdInterp.index_csc', 'acmd=%s, acmd.spoken_forms=%s, =%s' % (acmd, acmd.spoken_forms, acmd.meanings))
        debug.trace('CmdInterp.index_csc', 'spoken_forms=%s' % acmd.spoken_forms)
        cmd_dict = acmd.get_meanings()

        for a_spoken_form in acmd.spoken_forms:
            #
            # Remove leading, trailing and double blanks from the spoken form
            #
            orig_spoken = string.strip(a_spoken_form)
            a_spoken_form = sr_interface.clean_spoken_form(a_spoken_form)

            #
            # Index the spoken form
            #
            phrase = string.split(a_spoken_form)
            meanings = self.commands.complete_match(phrase)
            trace('CmdInterp.index_csc', 'adding phrase %s' % phrase)
            if meanings:
                try:
                    meanings.merge(cmd_dict)
                except DuplicateContextKeys, e:
                    msg = 'Warning: when adding CSC spoken form %s,\n' % phrase
                    msg = msg + e.msg
                    config_warning(msg)

# since meanings is an object reference, we don't need to call
# add_phrase to modify the value corresponding to the
# phrase
            else:
                #
                # First time indexed. Create a new list of CSCs for that
                # spoken form, and add it to the SR vocabulary.
                #
                self.commands.add_phrase(phrase, cmd_dict)
                if (self.add_sr_entries_for_LSAs_and_CSCs):
                    sr_interface.addWord(orig_spoken)
# we had some problems in regression testing because the individual
# words in a spoken form were unknown, so now we add the individual
# words in a multiple-word spoken form

# This allows for redundant translation, avoiding
# the problems in regression testing.  However,
# this presumably makes Natspeak recognition of the CSC/LSA worse, 
# so we may want to come up with an alternate solution in the future
                    
                    all_words = string.split(orig_spoken)
                    if (len(all_words) > 1 and 
                        self.add_sr_entries_for_LSAs_and_CSCs):
                        for word in all_words:
                            word = sr_interface.clean_spoken_form(word)
                            sr_interface.addWord(word)

#            print self.commands.all_matches(phrase)

    def add_csc(self, acmd):
        """Add a new Context Sensitive Command. (synonym for index_csc)

        [CSCmd] *acmd* is the command to add.

        .. [CSCmd] file:///./CSCmd.CSCmd.html"""

        self.index_csc(acmd)

    def add_csc_set(self, set):
        """add CSCs from a set

        **INPUTS**

        *CSCmdSet set* -- the set of commands to add

        **OUTPUTS**

        *none*
        """
        debug.trace('CmdInterp.add_csc_set', 
            'adding CSCs from set %s' % set.name)
        for cmd in set.commands.values():
#            print cmd.spoken_forms
            self.add_csc(cmd)

    def add_lsa(self, an_LSA):
        """Add a language specific word.

        **INPUTS**
        
        *LSAlias an_LSA* -- the new language-specific alias
        
        **OUTPUTS**
        
        *none* -- 
        """

        for language, written_as in an_LSA.meanings.items():
# DCF temporary spacing hack until we put in the real system
            hacked_written_as = written_as
            if an_LSA.spacing & hard_space:
                hacked_written_as = written_as + ' '
            elif an_LSA.spacing & hard_new_line:
                hacked_written_as = written_as + '\n'
            elif an_LSA.spacing & hard_paragraph:
                hacked_written_as = written_as + '\n\n'
            elif an_LSA.spacing & hard_tab:
                hacked_written_as = written_as + '\t'
            elif an_LSA.spacing == like_comma:
                hacked_written_as = written_as + ' '
#                print '%s like comma %d' % (an_LSA.spoken_forms[0], an_LSA.spacing)
            written_as = string.strip(written_as)
# now that we're using hacked_written_as for the LSA entry, there is
# no point in keeping leading and trailing spaces in the written form
# (and besides, they're going to go away as soon as the real spacing
# system is set up)
            for spoken_as in an_LSA.spoken_forms:
                clean_spoken = sr_interface.clean_spoken_form(spoken_as)
                entry = sr_interface.vocabulary_entry(spoken_as, written_as)
                vc_entry = sr_interface.vocabulary_entry(spoken_as, written_as, clean_written=0)
#                if clean_spoken == 'ellipsis':
#                    print "ellipsis spacing %d, written-as '%s'" \
#                        % (an_LSA.spacing, written_as)
                
                if not self.language_specific_aliases.has_key(language):
                    self.language_specific_aliases[language] = \
                        WordTrie.WordTrie()

                meaning = AliasMeaning(hacked_written_as, 
                    spacing = an_LSA.spacing, 
                    new_symbol = an_LSA.new_symbol)
                phrase = string.split(clean_spoken)
                self.language_specific_aliases[language].add_phrase(phrase, 
                    meaning)
                trace('CmdInterp.add_lsa', 'language = %s' % language)
                trace('CmdInterp.add_lsa', 
                    'spoken, written = "%s", "%s"' % (clean_spoken,
                    written_as))


                #
                # Add LSA to the SR vocabulary
                #
                if self.add_sr_entries_for_LSAs_and_CSCs:
                    trace('CmdInterp.add_lsa', 
                        'adding entry "%s"' % entry)
#                    print 'clean_spoken, written, entry: "%s", "%s", "%s"' \
#                        % (clean_spoken, hacked_written_as, entry)
                    sr_interface.addWord(entry)
# we had some problems in regression testing because the individual
# words in a spoken form were unknown, so now we add the individual
# words in a multiple-word spoken form

# This allows for redundant translation, avoiding
# the problems in regression testing.  However,
# this presumably makes Natspeak recognition of the CSC/LSA worse, 
# so we may want to come up with an alternate solution in the future

                all_words = string.split(spoken_as)
                if (len(all_words) > 1 and
                    self.add_sr_entries_for_LSAs_and_CSCs):
                    for word in all_words:
                        word = sr_interface.clean_spoken_form(word)
                        sr_interface.addWord(word)

    def add_capitalization_word(self, word):
        """Add a language specific word.

        **INPUTS**
        
        *CapitalizationWord word* -- the new word
        
        **OUTPUTS**
        
        *none* -- 
        """
        if not self.language_specific_aliases.has_key(None):
            self.language_specific_aliases[None] = \
                WordTrie.WordTrie()

        for spoken_as in word.spoken_forms:
            clean_spoken = sr_interface.clean_spoken_form(spoken_as)
            vc_entry = sr_interface.vocabulary_entry(spoken_as, "", clean_written=0)
            phrase = string.split(clean_spoken)
            self.language_specific_aliases[None].add_phrase(phrase, 
                word.modifier)

            #
            # Add LSA to the SR vocabulary
            #
            if self.add_sr_entries_for_LSAs_and_CSCs:
                trace('CmdInterp.add_capitalization_word', 
                    'adding entry "%s"' % vc_entry)
#                    print 'clean_spoken, written, entry: "%s", "%s", "%s"' \
#                        % (clean_spoken, hacked_written_as, entry)
                sr_interface.addWord(vc_entry)

    def add_lsa_set(self, set):
        """add LSAs from a set

        **INPUTS**

        *LSAliasSet set* -- the set of aliases to add

        **OUTPUTS**

        *none*
        """
        for alias in set.aliases.values():
            self.add_lsa(alias)

    def add_capitalization_word_set(self, set):
        """add CapitalizationWords from a set

        **INPUTS**

        *CapitalizationWordSet set* -- the set of words to add

        **OUTPUTS**

        *none*
        """
        for word in set.words.values():
            self.add_capitalization_word(word)

    def has_lsa(self, spoken_form, language = None):
        """check if there is already an LSA defined with this spoken
        form

        **INPUTS**

        *STR spoken_form* -- spoken form to check

        *STR language* -- name of the language in which to check

        **OUTPUTS**

        *BOOL* -- true if such an LSA exists
        """
        try:
            to_check = self.language_specific_aliases[language]
        except KeyError:
            return 0
        clean_spoken = sr_interface.clean_spoken_form(spoken_form)
        phrase = string.split(clean_spoken)
        if to_check.complete_match(phrase):
            return 1
        return 0

    def add_abbreviation(self, abbreviation, expansions, user_added = 1):
        """Add an abbreviation to VoiceCode's abbreviations dictionary.

        **INPUTS**

        *STR* abbreviation -- the abbreviation 

        *[STR]* expansions -- list of possible expansions


        **OUTPUTS**

        *none* -- 
        """
        self.known_symbols.add_abbreviation(abbreviation, expansions,
            user_added = user_added)

    def clear_standard_symbols_file_list(self):
        """Clears the list of files defining standard symbols"""
        self.known_symbols.clear_standard_symbols_file_list()

    def standard_symbols_in(self, file_list):
        """Specify source files defining standard symbols"""
        self.known_symbols.standard_symbols_in(file_list)

    def abbreviations_in(self, file_list):
        """Specify source files defining expansions and abbreviations"""
        self.known_symbols.abbreviations_in(file_list)

    def peek_at_unresolved(self):
        """returns a reference to the dictionary of unresolved 
        abbreviations maintained by the SymDict, and the symbols 
        containing those abbreviations.

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
        return self.known_symbols.peek_at_unresolved()

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
        return self.known_symbols.accept_symbol_match(the_match)

    def match_pseudo_symbol(self, pseudo_symbol):        
        """Returns a prioritized list of all known native symbols that
        match a given pseudo symbol.
        
        **INPUTS**
        
        *STR* pseudo_symbol -- The pseudo symbol to be matched. 
        

        **OUTPUTS**
        
        *[* [SymbolMatch] *]* -- Prioritized list of symbol matches.

        
        .. [SymbolMatch] file:///./SymDict.SymbolMatch.html"""
        return self.known_symbols.match_pseudo_symbol(pseudo_symbol)

    def save_dictionary(self, file = None):
        """saves the symbol dictionary state

        **INPUTS**

        *STR file* -- name of the file in which to save the dictionary
        (usually None to use the same file sym_file specified when
        CmdInterp was initialized)

        **OUTPUTS**

        *none*
        """
        self.known_symbols.save(file = file)

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
        self.known_symbols.cleanup_dictionary(clean_sr_voc=clean_sr_voc, 
            clean_symdict=clean_symdict, resave=resave)

    def abbreviations_cleanup(self):
        """Removes all known abbreviations from the symbols dictionary.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        self.known_symbols.abbreviations_cleanup()

    def finish_config(self):
        """Finish performing those parts of the CmdInterp/SymDict
        configuration which can't take place until after the VoiceCode
        configuration files have been executed
        
        **INPUTS**

        *none*
        
        **OUTPUTS**
        
        *none*
        """
# for now, only SymDict requires this
        self.known_symbols.finish_config()
    
    def parse_standard_symbols(self):
        """Parse standard symbols for the various programming languages.
        
        **INPUTS**

        *none*
        
        **OUTPUTS**
        
        *none*
        """
        self.known_symbols.parse_standard_symbols()
    
    def parse_symbols_from_files(self, file_list, add_sr_entries=1):
        """Parse symbols from a series of source files

        **INPUTS**

        *[STR] file_list -- List of files to be compiled

        *BOOL* add_sr_entries = 1 -- If true, add symbols to the SR vocabulary

        **OUTPUT**

        *none* --
        """

        self.known_symbols.parse_symbols_from_files(file_list, 
            add_sr_entries = add_sr_entries)


    def parse_symbols_from_file(self, file_name, add_sr_entries=1):
        """Parse symbols from a single source file.

        *STR* file_name -- The path of the file.

        *BOOL* add_sr_entries = 1 -- If true, add symbols to the SR vocabulary
        """

        self.known_symbols.parse_symbols_from_file(file_name, 
            add_sr_entries = add_sr_entries)
                
    def parse_symbols(self, contents, language_name, add_sr_entries=1):
        """Parse symbols from a string representing the contents of a 
        source file.

        *STR* contents -- the contents of the source file

        *STR* language_name -- the name of the language of the source
        file

        *BOOL* add_sr_entries = 1 -- If true, add symbols to the SR vocabulary
        """
        self.known_symbols.parse_symbols(contents, language_name,
            add_sr_entries = add_sr_entries)

    def print_symbols(self, symbols = None):
        """Print the content of the symbols dictionary.
        
        **INPUTS**
        
        *[STR] symbols* -- list of symbols to print, or None to print
        the whole dictionary
        
        **OUTPUTS**
        
        *none* -- 
        """
        self.known_symbols.print_symbols(symbols = symbols)

    def print_abbreviations(self, show_unresolved=0):
        """Prints the known and unresolved abbreviations."""
        self.known_symbols.print_abbreviations(show_unresolved)

# functions, not methods

def process_initials(spoken):
    """strips the period from initials

    **INPUTS**

    *STR spoken* -- spoken form

    **OUTPUTS**

    *STR* -- spoken form, but with 'A.' -> 'a', etc.
    """
    if re.match('[A-Z]\.$', spoken):
        return string.lower(spoken[0])
    return spoken

# defaults for vim - otherwise ignore
# vim:sw=4
