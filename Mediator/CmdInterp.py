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
from debug import trace
from actions_C_Cpp import *
from actions_py import *
from AppState import AppState
from cont_gen import ContC, ContPy
from CSCmd import CSCmd
from Object import Object, OwnerObject
import SymDict
import sr_interface

from SpacingState import *

class LSAlias(Object):
    """
    Language-specific alias (or LSA), a word with one or more spoken 
    forms, which is translated into a written form according to the 
    language of the current buffer.
    
    Generally, all combinations of written and spoken forms for an LSA 
    are added to the vocabulary as words, so as to enable
    select-pseudocode.
    
    *STR* spoken_forms -- List of spoken form of the word.

    *{STR: STR}* meanings -- Dictionary of language specific
     meanings. Key is the language name and value is the written form
     of the LSA for that langugage. If language name is *None*, then
     it means that this LSA applies for all languages (I know, it
     doesn't make much sense syntactically).

    *INT* spacing -- spacing flags, from SpacingState (CURRENTLY
    IGNORED)
    """
    def __init__(self, spoken_forms, meanings, spacing = 0, **args):
        """
        **INPUTS**

        *STR* spoken_forms -- List of spoken form of the word.

        *{STR: STR}* meanings -- Dictionary of language specific
         meanings. Key is the language name and value is the written form
         of the LSA for that langugage. If language name is *None*, then
         it means that this LSA applies for all languages (I know, it
         doesn't make much sense syntactically).

        *INT* spacing -- spacing flags, from SpacingState (CURRENTLY
        IGNORED)
        """
        self.deep_construct(LSAlias,
                            {'spoken_forms': spoken_forms,
                             'meanings': {},
                             'spacing': spacing
                            },
                            args)

        for language, written_as in meanings.items():
            self.meanings[language] = written_as

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
            self.commands[name].spoken_forms = spoken_forms[:]
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
        except KeyError:
            return 0
        for spoken in spoken_forms:
            command.spoken_forms.append(spoken)
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
        except KeyError:
            return 0
        new_spoken = []
        for spoken in command.spoken_forms:
            if spoken not in spoken_forms:
                new_spoken.append(spoken)
        command.spoken_forms = new_spoken
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

    *{STR: CSCmd}* aliases -- map from unique names to
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
        self.deep_construct(CSCmdSet,
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
        trace('CmdInterp.add_lsa', '** invoked')
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



class CmdInterp(OwnerObject):
    """Interprets Context Sensitive Commands spoken into a given application.
    
    **INSTANCE ATTRIBUTES**

    *NewMediatorObject mediator* -- reference to the parent mediator
    which owns this CmdInterp instance

    {STR: [[(Context , FCT)]} *cmd_index={}* -- index of CSCs. Key
     is the spoken form of the command, value is a list of contextual
     meanings. A contextual meaning is a pair of a *context object*
     and an *action function* to be fired if the context applies.

    [SymDict] *known_symbols* -- dictionary of known symbols
    
    {STR: {STR: STR}} *language_specific_aliases = {}* -- Key is the name of
     a programming language (None means all languages). Value is a
     dictionary of written forms over spoken form keys 
     specific to a language.

    BOOL *disable_dlg_select_symbol_matches = None* -- If true, then
    do not prompt the user for confirmation of new symbols.
    
    BOOL *add_sr_entries_for_LSAs_and_CSCs* -- if *TRUE*, then add 
    SR entries for the LSAs and CSCs when they are added. If *FALSE*, 
    assume that these entries were already added by an previous instance
    of the mediator. This is mostly used for regression testing purposes
    where we create a new mediator in each test, and don't want to waste
    CPU time adding the same LSAs and CSCs over and over again.

    *{STR: {STR: STR}}* lsa_spacing = {} -- Key is the name of
     a programming language (None means all languages). Value is a
     dictionary of spacing flags over spoken form keys 
     specific to a language.
    
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

        #
        # These attributes can't be set at construction time
        #
#        self.decl_attrs({})

        #
        # But these can
        #
        self.deep_construct(CmdInterp,
                            {'mediator': mediator,
                             'cmd_index': {}, 
                             'known_symbols':
                             SymDict.SymDict(sym_file = sym_file), 
                             'language_specific_aliases': {},
                             'lsa_spacing': {},
                             'disable_dlg_select_symbol_matches': disable_dlg_select_symbol_matches,
                             'add_sr_entries_for_LSAs_and_CSCs': 1},
                            attrs)
        self.name_parent('mediator')

    def set_mediator(self, mediator):
        """sets the parent mediator which owns this CmdInterp instance

        **INPUTS**

        *NewMediatorObject mediator* -- reference to the parent mediator
        which owns this CmdInterp instance

        **OUTPUTS**

        *none*
        """
        self.mediator = mediator

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
        trace('CmdInterp.interpret_NL_cmd', 'cmd=%s' % cmd)

        if initial_buffer == None:
            app.bind_to_buffer(app.curr_buffer_name())
        else:
            app.bind_to_buffer(initial_buffer)

        untranslated_words = []
        
        #
        # Process the beginning of the command until there is nothing
        # left
        #
        while len(cmd) > 0:
             trace('CmdInterp.interpret_massaged', 'now, cmd=%s' % cmd)

             #
             # Identify leading CSC, LSA, symbol and ordinary word
             #
             chopped_CSC, CSC_consumes, cmd_without_CSC = \
                 self.chop_CSC(cmd, app)
             chopped_LSA, LSA_consumes, cmd_without_LSA = \
                 self.chop_LSA(cmd, app)
             chopped_symbol, symbol_consumes, cmd_without_symbol = \
                 self.chop_symbol(cmd, app)
             chopped_word, word_consumes, cmd_without_word = self.chop_word(cmd)             
             most_consumed = max((LSA_consumes, symbol_consumes, CSC_consumes, word_consumes))

             trace('CmdInterp.interpret_massaged', 
             'chopped_CSC=%s, CSC_consumes=%s, chopped_LSA=%s, LSA_consumes=%s, chopped_symbol=%s, symbol_consumes=%s, chopped_word=%s, word_consumes=%s' % (chopped_CSC, CSC_consumes, chopped_LSA, LSA_consumes, chopped_symbol, symbol_consumes, chopped_word, word_consumes))
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
             
             if CSC_consumes == most_consumed:
                 #
                 # CSC consumed the most words from the command.
                 # Try all the CSCs with this spoken form until find
                 # one that applies in current context
                 #
                 trace('CmdInterp.interpret_massaged', 'processing leading CSC=\'%s\'' % chopped_CSC)
                 CSCs = self.cmd_index[chopped_CSC]
                 trace('CmdInterp.interpret_massaged', '** CSCs=%s' % repr(CSCs))                 
                 csc_applies = 0
# DCF: why is self.cmd_index[a_spoken_form] a list of CSCs each with
# multiple meanings?  The meanings are a dictionary, so there is no way
# to specify their order, so allowing a list of forms allows you to
# prioritize between elements.  On the other hand, add_csc always
# appends to the list, so you always have to go from general to
# specific.  Furthermore, priority within elements is
# undefined.  This seems like a very bad design.
                 for aCSC in CSCs:
                     csc_applies = aCSC.applies(app)
                     trace('CmdInterp.interpret_massaged', '** aCSC=%s, csc_applies=%s' % (aCSC, csc_applies))
                     if (csc_applies):
# flush untranslated words before executing action
                         if untranslated_words:
                             self.match_untranslated_text(untranslated_words, 
                                 app)
                             untranslated_words = []
                         aCSC.interpret(app)
                         break
                 if csc_applies:
                     #
                     # Found a CSC that applies
                     # Chop the CSC from the command
                     #
                     cmd = cmd_without_CSC
                     head_was_translated = 1
                 else:
                     #
                     # As it turns out, none of the CSCs with this
                     # spoken form apply in current context
                     # So don't chop the CSC
                     #
                     chopped_CSC = None
                     CSC_consumes = 0
                     most_consumed = max((LSA_consumes, symbol_consumes, word_consumes))
             
             if not head_was_translated and LSA_consumes == most_consumed:
                 #
                 # LSA consumed the most words from command. Insert it.
                 #
                 trace('CmdInterp.interpret_massaged', 'processing leading LSA=\'%s\'' % chopped_LSA)
# flush untranslated words before inserting LSA
                 if untranslated_words:
                     self.match_untranslated_text(untranslated_words, app)
                     untranslated_words = []
                 actions_gen.ActionInsert(code_bef=chopped_LSA, code_after='').log_execute(app, None)
                 cmd = cmd_without_LSA
                 head_was_translated = 1


             if not head_was_translated and symbol_consumes == most_consumed:
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
                 trace('CmdInterp.interpret_massaged', 'processing leading symbol=\'%s\'' % chopped_symbol)
                 untranslated_words.append( chopped_symbol)
                 cmd = cmd_without_symbol
                 head_was_translated = 1
                                          
                    
             if not head_was_translated and word_consumes == most_consumed:
                 #
                 # Nothing special translated at begining of command.
                 # Just chop off the first word and insert it, marking
                 # it as untranslated text.
                 #                 
                 trace('CmdInterp.interpret_massaged', 'processing leading word=\'%s\'' % chopped_word)
                 untranslated_words.append( chopped_word)
                 cmd = cmd_without_word
                 head_was_translated = 1

             #
             # Finished translating head of command.
             #
             # Check if it marked the end of some untranslated text
             #
             if (len(cmd) == 0) and untranslated_words:
                 #
                 # A CSC or LSA was translated, or we reached end of the
                 # command, thus marking the end of a sequence of untranslated
                 # text. Try to match untranslated text to a known (or new)
                 # symbol.
                 #
                 trace('CmdInterp.interpret_massaged', 'found the end of some untranslated text')
                 self.match_untranslated_text(untranslated_words, app)
                 untranslated_words = []

             if untranslated_words:
                 untranslated_text = string.join(untranslated_words)
             else:
                 untranslated_text = None
             trace('CmdInterp.interpret_massaged', 'End of *while* iteration. untranslated_text=\'%s\', app.curr_buffer().cur_pos=%s' % (untranslated_text, app.curr_buffer().cur_pos()))

        # make sure to unbind the buffer before returning
        app.unbind_from_buffer()

        #
        # Notify external editor of the end of recognition
        #
        app.recog_end()


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
# redundant
#            written = sr_interface.clean_written_form(written, clean_for='vc')
            spoken = sr_interface.clean_spoken_form(spoken)
#            spoken = re.sub('\s+', ' ', spoken)
#            spoken = re.sub('\s+', ' ', spoken)
#            spoken = re.sub('(^\s+|\s+$)', '', spoken)
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

    def match_untranslated_text(self, untranslated_words, app):
        """Tries to match last sequence of untranslated text to a symbol.
        
        **INPUTS**
        
        *[STR]* -- list of untranslated words
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        untranslated_text = string.join(untranslated_words)

        trace('CmdInterp.match_untranslated_text', 'untranslated_text=\'%s\'' % (untranslated_text))
#        trace('CmdInterp.match_untranslated_text', 'symbols are: %s' % self.known_symbols.print_symbols())
#        print '-- CmdInterp.match_untranslated_text: untranslated_text=\'%s\'' % (untranslated_text);
#        print '-- CmdInterp.match_untranslated_text: symbols are: '; self.known_symbols.print_symbols()
        
        a_match = re.match('(\s*)([\s\S]*)\s*$', untranslated_text)
        text_no_spaces = a_match.group(2)
#          #
#          # Remove dots after single characters
#          # Not really necessary because the symbol matching ignores non
#          # alphanums?
#          #
#          text_no_spaces = re.sub('(^|\s)([a-zA-Z])\.', '\1\2', text_no_spaces)
        
        leading_spaces = a_match.group(1)

        trace('CmdInterp.match_untranslated_text', 'text_no_spaces=\'%s\', leading_spaces=\'%s\'' % (text_no_spaces, leading_spaces))
                
        #
        # Match untranslated text to new known symbol or a known symbol with
        # unresolved spoken forms.
        #
        # Don't bother the user if the untranslated text is just the written
        # form of a known symbol or if it's a number
        #
        reg = '[\d\s]+'
        num_match = re.match(reg, text_no_spaces)
        if not self.known_symbols.symbol_info.has_key(text_no_spaces) and \
           not num_match:
            symbol_matches = self.known_symbols.match_pseudo_symbol(untranslated_text)
            trace('CmdInterp.match_untranslated_text', 'symbol_matches=%s' % symbol_matches)
            if symbol_matches:
                self.dlg_select_symbol_match(untranslated_text, 
                    symbol_matches, app)
            else:
                actions_gen.ActionInsert(code_bef=untranslated_text, code_after='').log_execute(app, None)                
        else:
            untranslated_text = re.sub('\s', '', untranslated_text)        
            actions_gen.ActionInsert(code_bef=untranslated_text, code_after='').log_execute(app, None)                            
        

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
#        print '-- CmdInterp.dlg_select_symbol_match: self.disable_dlg_select_symbol_matches=%s' % self.disable_dlg_select_symbol_matches

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
            self.known_symbols.accept_symbol_match(chosen_match)            

            #
            # Insert matched symbol
            #
            actions_gen.ActionInsert(code_bef=chosen_match.native_symbol, code_after='').log_execute(app, None)            
#            app.insert_indent(chosen_match.native_symbol, '')
        else:
            actions_gen.ActionInsert(code_bef=untranslated_text, code_after='').log_execute(app, None)                        
#            app.insert_indent(untranslated_text, '')
        

    def chop_CSC(self, cmd, app):
        """Chops the start of a command if it starts with a CSC.
        
        **INPUTS**
        
        *[(STR, STR)]* cmd -- The command,  a list of
         tuples of (spoken_form, written_form), with the spoken form
         cleaned and the written form cleaned for VoiceCode.

        **OUTPUTS**

        Returns a tuple *(chopped_CSC, consumed, rest)* where:
        
        *STR* chopped_symbol -- The spoken form of the CSC that
        was chopped off. If *None*, it means *cmd* did
        not start with a known CSC.

        *INT* consumed* -- Number of words consumed by the CSC from
         the command

        *(STR, STR)* rest -- is what was left of *cmd* after the CSC
         was chopped off.        
        """
        
        trace('CmdInterp.chop_CSC', 'cmd=%s' % cmd)
#        print '-- CmdInterp.chop_CSC: cmd=%s' % cmd

        return self.chop_construct(cmd, CmdInterp.is_spoken_CSC, app)

    def chop_LSA(self, command, app):
        """Chops off the first word of a command if it is an LSA.
                
        **INPUTS**
        
        *[(STR, STR)]* cmd -- The command,  a list of
         tuples of (spoken_form, written_form), with the spoken form
         cleaned and the written form cleaned for VoiceCode.

        **OUTPUTS**
        
        Returns a tuple *(chopped_LSA, consumed, rest)* where:
        
        *STR* chopped_LSA -- The written form of the LSA that was
         chopped off. If *None*, it means *command* did not start with
         an LSA.

        *INT* consumed* -- Number of words consumed by the LSA from
         the command (always 1, but return it anyway because want to
         keep same signature as chop_CSC and chop_symbol)

        *(STR, STR)* rest -- is what was left of *cmd* after the LSA
         was chopped off.        
        """
        
        trace('CmdInterp.chop_LSA', 'command=%s' % command)
#        print '-- CmdInterp.chop_LSA: command=%s' % command
        return self.chop_construct(command, CmdInterp.is_spoken_LSA, app)

    def chop_symbol(self, command, app):
        """Chops off the beginning of a command if it is a known symbol.
        
        **INPUTS**
        
        *[(STR, STR)]* cmd -- The command,  a list of
         tuples of (spoken_form, written_form), with the spoken form
         cleaned and the written form cleaned for VoiceCode.

        **OUTPUTS**

        Returns a tuple *(chopped_symbol, consumed, rest)* where:
        
        *STR* chopped_symbol -- The written form of the known symbol that
        was chopped off. If *None*, it means *command* did
        not start with a known symbol.

        *INT* consumed* -- Number of words consumed by the symbol from
         the command

        *(STR, STR)* rest -- is what was left of *cmd* after the symbol
         was chopped off.        
        """

        trace('CmdInterp.chop_symbols', 'command=%s' % command)
#        if not app.translation_is_off:
        return self.chop_construct(command, CmdInterp.is_spoken_symbol, app)
#        else:
#            return None, 0, command
    
    def chop_word(self, command):
        """Removes a single word from a command.
        
        **INPUTS**
        
        *[(STR, STR)]* cmd -- The command,  a list of
         tuples of (spoken_form, written_form), with the spoken form
         cleaned and the written form cleaned for VoiceCode.

        **OUTPUTS**
        
        Returns a tuple *(chopped_word, consumed, rest)* where:

        *STR* chopped_word -- The spoken form of the first word

        *INT* consumed -- Number of words consumed (always 1, but
         return it anyway because want to keep same method signature
         as chop_CSC, chop_LSA and chop_symbol).

        *[(STR, STR)]* rest -- Rest of the command after the word was chopped
        
        """
        
        chopped_word = command[0][0]
        consumed = 1
        rest = command[1:]
        return chopped_word, consumed, rest
        
    def chop_construct(self, cmd, construct_check, app):
        """Look at NL command to see if it starts with a
        particular kind of construct (e.g. CSC, LSA, symbol)
        
        **INPUTS**
        
        *[STR]* cmd -- The words in the NL command (in their written\spoken
        form).

        *METHOD* construct_check(self, STR) returns STR -- Method used
         to check wether a string corresponds to the type of construct
         we are looking for. For LSA and symbol constructs, it returns
         the construct's written form. For CSCs, it returns its spoken
         form. If the string doesn't correspond to the proper construtct,
         it returns *None*.

         
        **OUTPUTS**
        
        *(chopped_construct, consumed, rest)*

        *STR* chopped_construct -- Spoken form of the construct
        chopped from the command

        *INT* consumed -- Number of words consumed from *cmd*

        *[STR]* rest -- The remaining of *cmd* after the construct has been
        chopped"""

        trace('CmdInterp.chop_construct', 'construct_check=%s' % repr(construct_check))
#        print '-- CmdInterp.chop_construct: construct_check=%s' % repr(construct_check)

        chopped_construct, consumed, rest = None, 0, cmd

        #
        # Create list of spoken forms of the words in command
        #
        words = []
        for a_word in cmd:
            a_word = a_word[0]
            words = words + [a_word]

        #
        # Starting with the whole command and dropping words from the end,
        # check if that corresponds to the spoken form of a known CSC.
        #
        upto = len(words)
        while upto:
            a_spoken_form = string.join(words[:upto], ' ')
# not completely redundant because the original spoken form might have
# contained initials (e.g. "M" or "M.") which would not have cleaned 
#            individually
            a_spoken_form = sr_interface.clean_spoken_form(a_spoken_form)
            trace('CmdInterp.chop_construct', 'upto=%s, a_spoken_form=%s' % (upto, a_spoken_form))
#            print '-- CmdInterp.chop_construct: upto=%s, a_spoken_form=%s' % (upto, a_spoken_form)

            chopped_construct = construct_check(self, a_spoken_form, app)
            trace('CmdInterp.chop_construct', 'after construct_check')
#            print '-- CmdInterp.chop_construct: after construct_check'
            if chopped_construct != None:
                #
                # This corresponds to the spoken form of a construct and it's
                # the longest one we'll ever find.
                #
                trace('CmdInterp.chop_construct', 'matches known construct \'%s\'' % a_spoken_form)
#                print '-- CmdInterp.chop_construct: matches known construct \'%s\'' % a_spoken_form
                rest = cmd[upto:]
                consumed = upto
                break
            upto = upto - 1

        trace('CmdInterp.chop_construct', 'returning chopped_construct=%s, consumed=%s, rest=%s' % (repr(chopped_construct), repr(consumed), repr(rest)))
#        print '-- CmdInterp.chop_construct: returning chopped_construct=%s, consumed=%s, rest=%s' % (repr(chopped_construct), repr(consumed), repr(rest))
        return chopped_construct, consumed, rest


    def is_spoken_CSC(self, spoken_form, app):
        """Checks if a string is the spoken form of a CSC.
        
        **INPUTS**
        
        *STR* spoken_form -- String to be checked
        

        **OUTPUTS**
        
        *BOOL* return value -- True iif *spoken_form* is the spoken form of a CSC.
        """
        trace('CmdInterp.is_spoken_CSC', 'spoken_form=%s' % spoken_form)
        chopped_CSC = None
        if self.cmd_index.has_key(spoken_form):
            chopped_CSC = spoken_form
        trace('CmdInterp.is_spoken_CSC', 
            'matched = %d' % (chopped_CSC is not None))
        return chopped_CSC



    def is_spoken_LSA(self, spoken_form, app):
        """Checks if a string is the spoken form of an LSA.
        
        **INPUTS**
        
        *none* -- 
        
        **OUTPUTS**

        *BOOL* return value -- True iif *spoken_form* is the spoken form of a LSA.
        """
        trace('CmdInterp.is_spoken_LSA', 'spoken_form = \'%s\'' % spoken_form)
#        print '-- CmdInterp.is_spoken_LSA: spoken_form = \'%s\'' % spoken_form

        written_LSA = None
        
        #
        # See if spoken_form is in the list of active LSAs
        #

        aliases = self.language_specific_aliases
        language = app.active_language()
        trace('CmdInterp.is_spoken_LSA', 'language=%s' % language)
#        print '-- CmdInterp.is_spoken_LSA: language=%s' % language
        
        if aliases.has_key(language):
            if aliases[language].has_key(spoken_form):
                written_LSA = aliases[language][spoken_form]
                trace('CmdInterp.is_spoken_LSA', 
                    'found language specific match')
# check common LSAs for all languages, if we haven't found a
# language-specific one
        if written_LSA == None and aliases.has_key(None):
            if aliases[None].has_key(spoken_form):
                written_LSA = aliases[None][spoken_form]
                trace('CmdInterp.is_spoken_LSA', 
                    'found language-independent match')

        trace('CmdInterp.is_spoken_LSA', 
            'written_LSA is "%s"' % repr(written_LSA))
        return written_LSA
        
    def is_spoken_symbol(self, spoken_form, app):
        """Checks if a string is the spoken form of a known symbol.
        
        **INPUTS**
        
        *none* -- 
        
        **OUTPUTS**

        *BOOL* return value -- True iif *spoken_form* is the spoken form of a
        known symbol.
        """

#        trace('CmdInterp.is_spoken_symbol', 'spoken_form=%s, self.known_symbols.spoken_form_info=%s' % (spoken_form, self.known_symbols.spoken_form_info))
#        print '-- CmdInterp.is_spoken_symbol: spoken_form=%s, self.known_symbols.spoken_form_info=%s' % (spoken_form, self.known_symbols.spoken_form_info)
        
        written_symbol = None
        if self.known_symbols.spoken_form_info.has_key(spoken_form):
            written_symbol = self.choose_best_symbol(spoken_form, self.known_symbols.spoken_form_info[spoken_form].symbols)

        trace('CmdInterp.is_spoken_symbol', 'returning written_symbol=\'%s\'' % written_symbol)
#        print '-- CmdInterp.is_spoken_symbol: returning written_symbol=\'%s\'' % written_symbol
        
        return written_symbol

    def choose_best_symbol(self, spoken_form, choices):
        """Chooses the best match for a spoken form of a symbol.

        For now, we just choose the first item in *choices*, but in
        the future, we might choose the one that appears closest to
        the cursor, or the one that used most recently, or the one
        that best matches the spoken form.
        
        **INPUTS**
        
        *STR* spoken_form -- spoken form of the symbol. 
        
        *ANY* choices -- undocumented 
        

        **OUTPUTS**
        
        *none* -- 
        """

        return choices[0]
    def index_csc(self, acmd):
        """Add a new csc to the command interpreter's command dictionary

        [CSCmd] *acmd* is the command to be indexed.

        .. [CSCmd] file:///./CSCmd.CSCmd.html"""

        debug.trace('CmdInterp.index_csc', 'acmd=%s, acmd.spoken_forms=%s, =%s' % (acmd, acmd.spoken_forms, acmd.meanings))
        for a_spoken_form in acmd.spoken_forms:
            #
            # Remove leading, trailing and double blanks from the spoken form
            #
            orig_spoken = string.strip(a_spoken_form)
            a_spoken_form = sr_interface.clean_spoken_form(a_spoken_form)

            #
            # Index the spoken form
            #
            if (self.cmd_index.has_key(a_spoken_form)):
                #
                # Already indexed. Just add to the list of CSCs for that
                # spoken form
                #
                cmds_this_spoken_form = self.cmd_index[a_spoken_form]
                cmds_this_spoken_form[len(cmds_this_spoken_form):] = [acmd]
# DCF: what's wrong with self.cmd_index[a_spoken_form].append(acmd)?
# also, why is self.cmd_index[a_spoken_form] a list of CSCs each with
# multiple meanings?  The meanings are a dictionary, so there is no way
# to specify their order, so allowing a list of forms allows you to
# prioritize between elements.  However, priority within elements is
# undefined.  This seems like a very bad design.
            else:
                #
                # First time indexed. Create a new list of CSCs for that
                # spoken form, and add it to the SR vocabulary.
                #
                self.cmd_index[a_spoken_form] = [acmd]
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
#                print '%s hard space %d' % (an_LSA.spoken_forms[0], an_LSA.spacing)
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
                    self.language_specific_aliases[language] = {}
                    self.lsa_spacing[language] = {}

                self.lsa_spacing[language][clean_spoken] = an_LSA.spacing 

                self.language_specific_aliases[language][clean_spoken] = hacked_written_as
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

    def add_lsa_set(self, set):
        """add LSAs from a set

        **INPUTS**

        *LSAliasSet set* -- the set of aliases to add

        **OUTPUTS**

        *none*
        """
        for alias in set.aliases.values():
            self.add_lsa(alias)

            
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
        if to_check.has_key(clean_spoken):
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

#        print '-- SymDict.parse_symbols: file_name=%s' % file_name
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
        self.known_symbols.print_abbreviations()

