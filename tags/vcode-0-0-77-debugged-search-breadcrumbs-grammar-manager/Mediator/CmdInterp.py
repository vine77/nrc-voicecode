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
from actions_C_Cpp import *
from actions_py import *
from AppState import AppState
from cont_gen import ContC, ContPy
from CSCmd import CSCmd
from EdSim import EdSim
from Object import Object
import EdSim, SymDict
import sr_interface


class CmdInterp(Object):
    """Interprets Context Sensitive Commands spoken into a given application.
    
    **INSTANCE ATTRIBUTES**

    [AppState] *on_app=None* -- application for which we are
    interpreting the commands
    
    *{STR: [[* (Context] *, FCT)]} cmd_index={}* -- index of CSCs. Key
     is the spoken form of the command, value is a list of contextual
     meanings. A contextual meaning is a pair of a *context object*
     and an *action function* to be fired if the context applies.

    *[SymDict] known_symbols* -- dictionary of known symbols
    
    *{STR: {STR: STR}}* language_specific_aliases = {} -- Key is the name of
     a programming language (None means all languages). Value is a
     dictionary of written forms over spoken form keys 
     specific to a language.

    *FILE symdict_pickle_file = None* -- File used to for
     reading/writing the symbol dictionary. If *None*, then don't
     read/write the symbol dictionary from/to file.

    *BOOL disable_dlg_select_symbol_matches = None* -- If true, then
    do not prompt the user for confirmation of new symbols.

    
    CLASS ATTRIBUTES**

    *none* --
        
    .. [AppState] file:///./AppState.AppState.html
    .. [Context] file:///./Context.Context.html
    .. [SymDict] file:///./SymDict.SymDict.html"""
    
    def __init__(self, on_app=None, symdict_pickle_file=None,
                 disable_dlg_select_symbol_matches = None, **attrs):

        #
        # These attributes can't be set at construction time
        #
#        self.decl_attrs({})

        #
        # But these can
        #
        self.deep_construct(CmdInterp,
                            {'on_app': on_app, 'cmd_index': {}, 
                             'known_symbols': SymDict.SymDict(), 
                             'language_specific_aliases': {},
                             'symdict_pickle_file': symdict_pickle_file,
                             'disable_dlg_select_symbol_matches': disable_dlg_select_symbol_matches},
                            attrs)


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

    def interpret_NL_cmd(self, cmd, initial_buffer = None):
        
        """Interprets a natural language command and executes
        corresponding instructions.

        *[STR] cmd* -- The command. It is a list of written\spoken words.
        
        *[STR] initial_buffer* -- The name of the target buffer at the 
	start of the utterance.  Some CSCs may change the target buffer of 
	subsequent parts of the command.  If None, then the current buffer 
	will be used.
        
        """
        
#        print '-- CmdInterp.interpret_NL_cmd: cmd=%s' % cmd
        
	if initial_buffer == None:
	    self.on_app.bind_to_buffer(self.on_app.curr_buffer_name())
	else:
	    self.on_app.bind_to_buffer(initial_buffer)

	untranslated_words = []

        cmd = self.massage_command(cmd)
        
        #
        # Process the beginning of the command until there is nothing
        # left
        #
        while len(cmd) > 0:
#             print '-- CmdInterp.interpret_NL_cmd: now, cmd=%s' % cmd

             #
             # Identify leading CSC, LSA, symbol and ordinary word
             #
             chopped_CSC, CSC_consumes, cmd_without_CSC = self.chop_CSC(cmd)
             chopped_LSA, LSA_consumes, cmd_without_LSA = self.chop_LSA(cmd)
             chopped_symbol, symbol_consumes, cmd_without_symbol = self.chop_symbol(cmd)
             chopped_word, word_consumes, cmd_without_word = self.chop_word(cmd)             
             most_consumed = max((LSA_consumes, symbol_consumes, CSC_consumes, word_consumes))

#             print '-- CmdInterp.interpret_NL_cmd: chopped_CSC=%s, CSC_consumes=%s, chopped_LSA=%s, LSA_consumes=%s, chopped_symbol=%s, symbol_consumes=%s, chopped_word=%s, word_consumes=%s' % (chopped_CSC, CSC_consumes, chopped_LSA, LSA_consumes, chopped_symbol, symbol_consumes, chopped_word, word_consumes)
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
#                 print '-- CmdInterp.interpret_NL_cmd: processing leading CSC=\'%s\'' % chopped_CSC
                 CSCs = self.cmd_index[chopped_CSC]
                 csc_applies = 0
                 for aCSC in CSCs:
                     csc_applies = aCSC.applies(self.on_app)
                     if (csc_applies):
# flush untranslated words before executing action
		         if untranslated_words:
			     self.match_untranslated_text(untranslated_words)
			     untranslated_words = []
			 aCSC.interpret(self.on_app)
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
#                 print '-- CmdInterp.interpret_NL_cmd: processing leading LSA=\'%s\'' % chopped_LSA
# flush untranslated words before inserting LSA
		 if untranslated_words:
		     self.match_untranslated_text(untranslated_words)
		     untranslated_words = []
                 actions_gen.ActionInsert(code_bef=chopped_LSA, code_after='').log_execute(self.on_app, None)
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
#                 print '-- CmdInterp.interpret_NL_cmd: processing leading symbol=\'%s\'' % chopped_symbol                     
		 untranslated_words.append( chopped_symbol)
                 cmd = cmd_without_symbol
                 head_was_translated = 1
                                          
                    
             if not head_was_translated and word_consumes == most_consumed:
                 #
                 # Nothing special translated at begining of command.
                 # Just chop off the first word and insert it, marking
                 # it as untranslated text.
                 #                 
#                 print '-- CmdInterp.interpret_NL_cmd: processing leading word=\'%s\'' % chopped_word                                                  
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
#                 print '-- CmdInterp.interpret_NL_cmd: found the end of some untranslated text'
                 self.match_untranslated_text(untranslated_words)
	 	 untranslated_words = []

             if untranslated_words:
                 untranslated_text = string.join(untranslated_words)
             else:
                 untranslated_text = None
#             print '-- CmdInterp.interpret_NL_cmd: End of *while* iteration. untranslated_text=\'%s\', self.on_app.curr_buffer().cur_pos=%s' % (untranslated_text, self.on_app.curr_buffer().cur_pos())

        # make sure to unbind the buffer before returning
	self.on_app.unbind_from_buffer()

        #
        # Notify external editor of the end of recognition
        #
        self.on_app.recog_end()


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
        
        *[STR] mod_command* -- The massaged command
        """
        
        mod_command = []
        for a_word in command:
            spoken, written = sr_interface.spoken_written_form(a_word)
            written = sr_interface.clean_written_form(written, clean_for='vc')
            spoken = re.sub('\s+', ' ', spoken)
            spoken = re.sub('(^\s+|\s+$)', '', spoken)
            mod_command = mod_command + [sr_interface.vocabulary_entry(spoken, written, clean_written=0)]
        return mod_command

    def match_untranslated_text(self, untranslated_words):
        """Tries to match last sequence of untranslated text to a symbol.
        
        **INPUTS**
        
        *[STR]* -- list of untranslated words
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        untranslated_text = string.join(untranslated_words)

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

#        print '-- CmdInterp.match_untranslated_text: text_no_spaces=\'%s\', leading_spaces=\'%s\'' % (text_no_spaces, leading_spaces)
                
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
#            print '-- CmdInterp.match_untranslated_text: symbol_matches=%s' % symbol_matches
            if symbol_matches:
                self.dlg_select_symbol_match(untranslated_text, symbol_matches)
	    else:
                actions_gen.ActionInsert(code_bef=untranslated_text, code_after='').log_execute(self.on_app, None)                
#		self.on_app.insert_indent(untranslated_text, '')
	else:
            actions_gen.ActionInsert(code_bef=untranslated_text, code_after='').log_execute(self.on_app, None)                            
#	    self.on_app.insert_indent(untranslated_text, '')
        

    def dlg_select_symbol_match(self, untranslated_text, symbol_matches):
        """Asks the user to select a match for pseudo symbol.
        
        **INPUTS**

	*STR* untranslated_text -- untranslated form of the text which
	matched
        
        *[SymbolMatch]* symbol_matches -- List of possible matches.
        

        **OUTPUTS**
        
        *none* -- 

        .. [SymbolMatch] file:///./SymDict.SymbolMatch.html"""
        

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
#                print '-- CmdInterp.dlg_select_symbol_match: answer=%s, answer_match=%s, answer_match.groups()=%s' % (answer, answer_match, answer_match.groups())
                if answer_match:
                    choice_index = int(answer_match.group(1)) - 1
                    if choice_index < len(symbol_matches) and choice_index >= -1:
                        good_answer = 1
                if not good_answer:
                    print 'Invalid answer \'%s\'' % answer
                    
        #
        # Accept the match
        #
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
            actions_gen.ActionInsert(code_bef=chosen_match.native_symbol, code_after='').log_execute(self.on_app, None)            
#            self.on_app.insert_indent(chosen_match.native_symbol, '')
	else:
            actions_gen.ActionInsert(code_bef=untranslated_text, code_after='').log_execute(self.on_app, None)                        
#	    self.on_app.insert_indent(untranslated_text, '')
	
            

    def chop_CSC(self, cmd):
        """Chops the start of a command if it starts with a CSC.
        
        **INPUTS**
        
        *[STR]* cmd -- The command. It is a list of written\spoken words.

        **OUTPUTS**

        Returns a tuple *(chopped_CSC, consumed, rest)* where:
        
        *STR* chopped_symbol -- The written form of the CSC that
        was chopped off. If *None*, it means *cmd* did
        not start with a known CSC.

        *INT* consumed* -- Number of words consumed by the CSC from
         the command

        *[STR]* rest -- is what was left of *cmd* after the CSC
         was chopped off.        
        """
        
#        print '-- CmdInterp.chop_CSC: cmd=%s' % cmd

        return self.chop_construct(cmd, CmdInterp.is_spoken_CSC)

    def chop_LSA(self, command):
        """Chops off the first word of a command if it is an LSA.
                
        **INPUTS**
        
        *[STR]* command -- The command. It is a list of words in
         written\spoken form.        

        **OUTPUTS**
        
        Returns a tuple *(chopped_LSA, consumed, rest)* where:
        
        *STR* chopped_LSA -- The written form of the LSA that was
         chopped off. If *None*, it means *command* did not start with
         an LSA.

        *INT* consumed* -- Number of words consumed by the LSA from
         the command (always 1, but return it anyway because want to
         keep same signature as chop_CSC and chop_symbol)

        *[STR]* rest -- is what was left of *command* after the LSA
         was chopped off.
        """
        
#        print '-- CmdInterp.chop_LSA: command=%s' % command
        return self.chop_construct(command, CmdInterp.is_spoken_LSA)

    def chop_symbol(self, command):
        """Chops off the beginning of a command if it is a known symbol.
        
        **INPUTS**
        
        *[STR]* command -- The command. It is a list of written\spoken words.

        **OUTPUTS**

        Returns a tuple *(chopped_symbol, consumed, rest)* where:
        
        *STR* chopped_symbol -- The written form of the known symbol that
        was chopped off. If *None*, it means *command* did
        not start with a known symbol.

        *INT* consumed* -- Number of words consumed by the symbol from
         the command

        *[STR]* rest -- is what was left of *command* after the symbol
         was chopped off.        
        """

#        print '-- CmdInterp.chop_symbols: command=%s' % command
#        if not self.on_app.translation_is_off:
        return self.chop_construct(command, CmdInterp.is_spoken_symbol)
#        else:
#            return None, 0, command
    
    def chop_word(self, command):
        """Removes a single word from a command.
        
        **INPUTS**
        
        *[STR]* command -- The command. It is a list of written\spoken words.
        

        **OUTPUTS**
        
        Returns a tuple *(chopped_word, consumed, rest)* where:

        *STR* chopped_word -- The spoken form of the first word

        *INT* consumed -- Number of words consumed (always 1, but
         return it anyway because want to keep same method signature
         as chop_CSC, chop_LSA and chop_symbol).

        *[STR]* rest -- Rest of the command after the word was chopped
        
        """
        
        chopped_word, dummy = sr_interface.spoken_written_form(command[0])
        consumed = 1
        rest = command[1:]
        return chopped_word, consumed, rest
        


    def chop_construct(self, cmd, construct_check):
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

#        print '-- CmdInterp.chop_construct: construct_check=%s' % repr(construct_check)

        chopped_construct, consumed, rest = None, 0, cmd

        #
        # Create list of spoken forms of the words in command
        #
        words = []
        for a_word in cmd:
            a_word, dummy = sr_interface.spoken_written_form(a_word)
            words = words + [a_word]

        #
        # Starting with the whole command and dropping words from the end,
        # check if that corresponds to the spoken form of a known CSC.
        #
        upto = len(words)
        while upto:
            a_spoken_form = string.join(words[:upto], ' ')
            a_spoken_form = sr_interface.clean_spoken_form(a_spoken_form)
#            print '-- CmdInterp.chop_construct: upto=%s, a_spoken_form=%s' % (upto, a_spoken_form)

            chopped_construct = construct_check(self, a_spoken_form)
#            print '-- CmdInterp.chop_construct: after construct_check'
            if chopped_construct != None:
                #
                # This corresponds to the spoken form of a construct and it's
                # the longest one we'll ever find.
                #
#                print '-- CmdInterp.chop_construct: matches known construct \'%s\'' % a_spoken_form
                rest = cmd[upto:]
                consumed = upto
                break
            upto = upto - 1

#        print '-- CmdInterp.chop_construct: returning chopped_construct=%s, consumed=%s, rest=%s' % (repr(chopped_construct), repr(consumed), repr(rest))
        return chopped_construct, consumed, rest
        


    def is_spoken_CSC(self, spoken_form):
        """Checks if a string is the spoken form of a CSC.
        
        **INPUTS**
        
        *STR* spoken_form -- String to be checked
        

        **OUTPUTS**
        
        *BOOL* return value -- True iif *spoken_form* is the spoken form of a CSC.
        """
#        print '-- CmdInterp.is_spoken_CSC: spoken_form=%s' % spoken_form
#        print '--** CmdInterp.is_spoken_CSC:self.cmd_index        
        chopped_CSC = None
        if self.cmd_index.has_key(spoken_form):
            chopped_CSC = spoken_form
        return chopped_CSC



    def is_spoken_LSA(self, spoken_form):
        """Checks if a string is the spoken form of an LSA.
        
        **INPUTS**
        
        *none* -- 
        
        **OUTPUTS**

        *BOOL* return value -- True iif *spoken_form* is the spoken form of a LSA.
        """
#        print '-- CmdInterp.is_spoken_LSA: spoken_form = \'%s\'' % spoken_form

        written_LSA = None
        
        #
        # See if spoken_form is in the list of active LSAs
        #

	aliases = self.language_specific_aliases
	language = self.on_app.active_language()
#        print '-- CmdInterp.is_spoken_LSA: language=%s' % language
        
        if aliases.has_key(language):
	    if aliases[language].has_key(spoken_form):
		written_LSA = aliases[language][spoken_form]
# check common LSAs for all languages, if we haven't found a
# language-specific one
	if written_LSA == None and aliases.has_key(None):
	    if aliases[None].has_key(spoken_form):
		written_LSA = aliases[None][spoken_form]

        return written_LSA
        
    def is_spoken_symbol(self, spoken_form):
        """Checks if a string is the spoken form of a known symbol.
        
        **INPUTS**
        
        *none* -- 
        
        **OUTPUTS**

        *BOOL* return value -- True iif *spoken_form* is the spoken form of a
        known symbol.
        """

#        print '-- CmdInterp.is_spoken_symbol: spoken_form=%s, self.known_symbols.spoken_form_info=%s' % (spoken_form, self.known_symbols.spoken_form_info)
        
        written_symbol = None
        if self.known_symbols.spoken_form_info.has_key(spoken_form):
            written_symbol = self.choose_best_symbol(spoken_form, self.known_symbols.spoken_form_info[spoken_form].symbols)

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

    def index_csc(self, acmd, add_voc_entry=1):
        """Add a new csc to the command interpreter's command dictionary

        [CSCmd] *acmd* is the command to be indexed.

        *BOOL add_voc_entry = 1* -- if true, add a SR vocabulary entry
         for the CSC's spoken forms

        .. [CSCmd] file:///./CSCmd.CSCmd.html"""

        global regexp_is_dirty

        regexp_is_dirty = 1

        for a_spoken_form in acmd.spoken_forms:
            #
            # Remove leading, trailing and double blanks from the spoken form
            #
            a_spoken_form = sr_interface.clean_spoken_form(a_spoken_form)

            #
            # Index the spoken form
            #
            if (self.cmd_index.has_key(a_spoken_form)):
                #
                # Already indexed. Just add to the list of CSCs for that
                # spoken form
                #
#                print '-- CmdInterp.index_csc: spoken form \'%s\'already indexed. Not adding to SR vocabulary' % a_spoken_form
                cmds_this_spoken_form = self.cmd_index[a_spoken_form]
                cmds_this_spoken_form[len(cmds_this_spoken_form):] = [acmd]
            else:
                #
                # First time indexed. Create a new list of CSCs for that
                # spoken form, and add it to the SR vocabulary.
                #
#                print '-- CmdInterp.index_csc: spoken form \'%s\' indexed for first time. Adding to SR vocabulary' % a_spoken_form
                self.cmd_index[a_spoken_form] = [acmd]
                if not os.environ.has_key('VCODE_NOSPEECH') and add_voc_entry:
                    sr_interface.addWord(a_spoken_form)

    def add_csc(self, acmd, add_voc_entry=1):
	"""Add a new Context Sensitive Command. (synonym for index_csc)

	[CSCmd] *acmd* is the command to add.

	*BOOL add_voc_entry = 1* -- if true, add a SR vocabulary entry
	for the CSC's spoken forms
	

	.. [CSCmd] file:///./CSCmd.CSCmd.html"""

	self.index_csc(acmd, add_voc_entry)


    def add_lsa(self, spoken_forms, meanings):
	"""Add a language specific word.

	These words get added and removed dynamically from the SR
	vocabulary, depending on the language of the active buffer.

	A redundant CSC is also added to allow translation of the LSA at
	the level of the Mediator, in cases where NatSpeak prefers to
	recognise the LSA as dictated text instead of a spoken/written
	word (this often happens if the spoken form looks to much like
	dictated text, e.g. "is not equal to").
	
	**INPUTS**
	
	*STR* spoken_forms -- List of spoken form of the word.

	*{STR: STR}* meanings -- Dictionary of language specific
	 meanings. Key is the language name and value is the written form
	 of the LSA for that langugage. If language name is *None*, then
	 it means that this LSA applies for all languages (I know, it
	 doesn't make much sense syntactically).
	
	**OUTPUTS**
	
	*none* -- 
	"""
	
#    print '-- MediatorObject.add_lsa: spoken_forms=%s' % spoken_forms
	

	for a_meaning in meanings.items():
	    language, written_as = a_meaning
	    for spoken_as in spoken_forms:
		clean_spoken = sr_interface.clean_spoken_form(spoken_as)
		entry = sr_interface.vocabulary_entry(spoken_as, written_as)
		vc_entry = sr_interface.vocabulary_entry(spoken_as, written_as, clean_written=0)
		
		if not self.language_specific_aliases.has_key(language):
		    self.language_specific_aliases[language] = {}

		self.language_specific_aliases[language][clean_spoken] = written_as

		#
		# Add LSA to the SR vocabulary
		#
		sr_interface.addWord(entry)
	    
    def add_abbreviation(self, abbreviation, expansions, user_added = 1):
	"""Add an abbreviation to VoiceCode's abbreviations dictionary.

	**INPUTS**

	*STR* abbreviation -- the abbreviation 

	*[STR]* expansions -- list of possible expansions


	**OUTPUTS**

	*none* -- 
	"""
	self.known_symbols.add_abbreviation(abbreviation, expansions)


    def standard_symbols_in(self, file_list):
	"""Compile symbols defined in a series of source files"""

#    print '-- MediatorObject.standard_symbols_in: file_list=%s' % repr(file_list)

	for a_file in file_list:
	    if not a_file in self.known_symbols.standard_symbol_sources:
		self.known_symbols.standard_symbol_sources = self.known_symbols.standard_symbol_sources + [a_file]

    def print_abbreviations(self):
	self.known_symbols.print_abbreviations()
