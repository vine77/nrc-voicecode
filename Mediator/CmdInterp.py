
import os, re, string, sys

import auto_test, natlink, vc_globals
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

    [SymDict] known_symbols -- dictionary of known symbols
    
    *STR cached_regexp=''* -- Regular expresion that matches the
     spoken form of any of the CSCs.

    *BOOL cached_regexp_is_dirty* -- *true* iif *self.cached_regexp* needs
     to be regenerated based on the values in *self.cmd_index*

    *{STR: [STR]}* language_specific_aliases = {} -- Key is the name of
     a programming language (None means all languages). Value is a
     list of written form\spoken form words specific to a
     language. These words are loaded automatically when we are in a
     source buffer of that language and removed when we change to a
     buffer in a different language.

    *STR* last_loaded_language = None -- Name of the previous language
     for which the language specific words were loaded.

    *FILE symdict_pickle_file = None* -- File used to for
     reading/writing the symbol dictionary. If *None*, then don't
     read/write the symbol dictionary from/to file.

    *INT* _untranslated_text_start = None -- Start position of the
     current string of untranslated text inserted in current buffer.

    *INT* _untranslated_text_end = None -- End position of the
     current string of untranslated text inserted in current buffer.
     
    
    CLASS ATTRIBUTES**

    *none* --
        
    .. [AppState] file:///./AppState.AppState.html
    .. [Context] file:///./Context.Context.html
    .. [SymDict] file:///./SymDict.SymDict.html"""
    
    def __init__(self, on_app=None, symdict_pickle_file=None, **attrs):

        #
        # These attributes can't be set at construction time
        #
        self.decl_attrs({'_untranslated_text_start': None, '_untranslated_text_end': None})

        #
        # But these can
        #
        self.deep_construct(CmdInterp,
                            {'on_app': on_app, 'cmd_index': {}, \
                             'known_symbols': SymDict.SymDict(), \
                             'cached_regexp': '',\
                             'cached_regexp_is_dirty': 1,\
                             'language_specific_aliases': {},\
                             'last_loaded_language': None, \
                             'symdict_pickle_file': symdict_pickle_file},\
                            attrs)

#      def refresh_dict_buff(self, moduleInfo):
#          """Refresh the dictation object's internal buffer."""

#          print '-- CmdInterp.refresh_dict_buff: called'
#          buff = self.on_app.curr_buffer
#          text = buff.content
#          sel_start = buff.selection_start
#          sel_end = buff.selection_end
#          vis_start = buff.visible_start
#          vis_end = buff.visible_end
        
#          self.dictation_object.setLock(1)
#          self.dictation_object.setText(text,0,0x7FFFFFFF)
#  #        self.dictation_object.setTextSel(sel_start,sel_end)
#  #        self.dictation_object.setVisibleText(vis_start,vis_end)

#          #
#          # For some reason, need to repeatadly call setLock(0) until it raises
#          # a natlink.WrongState exception. If don't do that, refresh_editor_buff
#          # doesn't get called for all but the first utterance (although
#          # refresh_dict_buff gets called everytime)
#          #
#          while (1):
#              try:
#                  self.dictation_object.setLock(0)
#              except natlink.WrongState:
#                  break

#      def refresh_editor_buff(self,del_start,del_end,newText,sel_start,sel_end):
#          """Refresh the editor's internal buffer after a recognition

#          *INT del_start, del_end* are the start and end position of text
#           that was deleted

#           *STR newText* is the text that was recognised by the dictation object.

#           *INT sel_start, sel_end* are the start and end position of the selection after the recognition"""

#          print '-- CmdInterp.refresh_editor_buff: del_start=%s,del_end=%s,newText=%s,sel_start=%s,sel_end=%s' % (del_start,del_end,newText,sel_start,sel_end)

#          self.dictation_object.setLock(1)
        
#  ##        self.edit.SetSel(del_start,del_end)
#  ##        self.edit.SetSel(sel_start,sel_end)

#          #
#          # Instead of inserting the text as is, interpret it as a pseudo
#          # code command
#          #
#          self.interpret_NL_cmd(newText)
#          self.on_app.print_buff_content()
        

    def all_cmds_regexp(self):
        """Returns a regexp that matches the spoken form of all voice commands"""

        if self.cached_regexp_is_dirty:
            #
            # Need to regenerate the regexp
            #
            self.cached_regexp = ''

            #
            # Sort spoken forms in decreasing order of length so that
            # longer expressions will be used in priority
            #            
            all_spoken_forms = self.cmd_index.keys()

            def cmp(x, y):
                if (len(x) < len(y)): return 1
                else: return -1
            all_spoken_forms.sort(cmp)

#            print '-- CmdInterp.all_cmds_regexp: sorted all_spoken_forms=%s' % str(all_spoken_forms)
            
            for a_spoken_form in all_spoken_forms:
                #
                # Allow arbitrary number of spaces between words
                #
                a_spoken_form = re.sub('\s+', '\\s+', a_spoken_form)

                spoken_regexp = self.spoken_form_regexp(a_spoken_form)
                
                if (self.cached_regexp == ''):
                    self.cached_regexp = spoken_regexp
                else:
                    self.cached_regexp = self.cached_regexp + '|' + spoken_regexp

            # CSC must be followed by a delimiter
            self.cached_regexp = '^(\s*)(' + self.cached_regexp + ')(\s*?)([^a-zA-Z0-9_]|$)'
        return self.cached_regexp


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

    def interpret_NL_cmd(self, cmd):
        
        """Interprets a natural language command and executes
        corresponding instructions.

        *STR cmd* is the spoken form of the command.
        """
        
#        print '-- CmdInterp.interpret_NL_cmd: cmd=%s' % cmd
#        print '-- CmdInterp.interpret_NL_cmd: self.all_cmds_regexp()=%s' % self.all_cmds_regexp()

        self._untranslated_text_start = None
        self._untranslated_text_end = None
        
        regexp = self.all_cmds_regexp()

        #
        # Process the beginning of the command until there is nothing
        # left
        #
        while (not cmd == ''):
#             print '-- CmdInterp.interpret_NL_cmd: now, cmd=%s' % cmd
#            print '-- CmdInterp.interpret_NL_cmd: cur_pos=%s' % self.on_app.curr_buffer.cur_pos
#             self.on_app.print_buff_content()

             #
             # Check for a CSC at the beginning of the command, and compute
             # length of string it consumes
             #
             csc_consumes = 0
             csc_match = re.match(regexp, cmd)
             if csc_match:
                 csc_consumes = csc_match.end(2) - csc_match.start(2) + 1
                 if re.match('\s', csc_match.group(3)):
                     #
                     # Delimiter was a space. Remove it
                     #
                     cmd_without_csc = cmd[csc_match.end():]
                 else:
                     #
                     # Delimiter was not a space. Leave it in command.
                     #
                     cmd_without_csc = cmd[csc_match.end(2):]

             #
             # Check if command starts with a known symbol, and compute
             # length of string it consumes
             #
             (a_symbol, cmd_without_symbol) = self.chop_symbol(cmd)
             symbol_consumes = len(cmd) - len(cmd_without_symbol)

#             print '-- CmdInterp.interpret_NL_cmd: csc_consumes=%s, symbol_consumes=%s' % (csc_consumes, symbol_consumes)

             #
             # Translate either CSC or known symbol, depending on which
             # of the two consumes the longest part of the NL command
             #
             if csc_consumes and csc_consumes >= symbol_consumes:
                 #
                 # The CSC consumes more than the symbol, so translate it.
                 # Try every possible contexts until one applies
                 #                
                 orig_spoken_form = csc_match.group(2)
#                 print '-- CmdInterp.interpret_NL_cmd: matched spoken form \'%s\'' % orig_spoken_form                                
                 indexed_spoken_form = orig_spoken_form
                 re.sub('\s+', ' ', indexed_spoken_form)
                 CSCs = self.cmd_index[string.lower(indexed_spoken_form)]
                 csc_applied = 0                 
                 for aCSC in CSCs:
                     csc_applied = aCSC.interpret(self.on_app)
                     if (csc_applied):
                         break
                 if csc_applied:
                     # Found applicable context for the CSC
#                     print '-- CmdInterp.interpret_NL_cmd: csc_applied CSC \'%s\'' % indexed_spoken_form
                     cmd = cmd_without_csc
                 else:
                     #
                     # Found no applicable contexts so CSC couldn't consume
                     # anything after all
                     #
                     csc_consumes = 0
                         
             if symbol_consumes and symbol_consumes >= csc_consumes:
                #
                # Command doesn't start with CSC, or CSC consumes less than
                # the symbol.
                #
                # So, insert the symbol
                #
                # Note: known symbols are inserted as untranslated
                #       text because often, the user will create new symbols
                #       by prefixing/postfixing existing ones. For example,
                #       if you define a subclass of a known class SomeClass
                #       you may name the new class SomeprefixSomeClass or
                #       SomeClassSomepostfix.
                #
#                print '-- CmdInterp.interpret_NL_cmd: inserted symbol %s' % a_symbol                                
                self.insert_untranslated_text(a_symbol)
                cmd = cmd_without_symbol
                
             if not csc_consumes and not symbol_consumes:
                #
                # Command starts with neither CSC or symbol.
                # Just remove a word from the beginning of the
                # command and insert it into the application's buffer
                #
#                print '-- CmdInterp.interpret_NL_cmd: inserted first word as is'
                amatch = re.match('(^\s*[^\s]*)', cmd)
                leading_word = amatch.group(1)
                self.insert_untranslated_text(leading_word)
                cmd = cmd[amatch.end():]

             if (csc_consumes or cmd == '') and \
                self._untranslated_text_start != None:
                #
                # A CSC was translated, or we reached end of the
                # command, thus marking the end of a sequence of untranslated
                # text. Try to match it to a known (or new) symbol.
                #
                self.match_untranslated_text()

#             print '-- CmdInterp.interpret_NL_cmd: End of while. self._untranslated_text_start=%s, self._untranslated_text_end=%s, self.on_app.curr_buffer.cur_pos=%s' % (self._untranslated_text_start, self._untranslated_text_end, self.on_app.curr_buffer.cur_pos)
                                
    def insert_untranslated_text(self, text):
        
        """Inserts some text in current buffer, and marks it as untranslated
        text.

        The next time a CSC is encountered, the interpreter will try
        to match that text (and all untranslated text that immediatly
        precedes/follows it) to a new symbol, or a known symbol with
        unresolved spoken forms.
        
        **INPUTS**
        
        *ST* text -- The text to be inserted
        

        **OUTPUTS**
        
        *none* -- 
        """

        self.on_app.insert_indent(text, '')

        if self._untranslated_text_start == None:
            #
            # This was the beginning of a sequence of
            # untranslated text. Remember its start
            # position.
            #
            # NOTE: We set start past any blanks that may
            # have been inserted for indentation
            #
            self._untranslated_text_start = self.on_app.curr_buffer.cur_pos - len(text)            
        
        #
        # Remember end of the current sequence of untranslated
        # text.
        #
        self._untranslated_text_end = self.on_app.curr_buffer.cur_pos

#        self.on_app.print_buff_content()
#        print '-- CmdInterp.insert_untranslated_text: self._untranslated_text_start=%s, self._untranslated_text_end=%s, untranslated region=\'%s\'' % (self._untranslated_text_start, self._untranslated_text_end, self.on_app.curr_buffer.content[self._untranslated_text_start:self._untranslated_text_end])
        

    def match_untranslated_text(self):
        """Tries to match last sequence of untranslated text to a symbol.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

#        print '-- CmdInterp.match_untranslated_text: self._untranslated_text_start=%s, self._untranslated_text_end=%s, untranslated region=\'%s\'' % (self._untranslated_text_start, self._untranslated_text_end, self.on_app.curr_buffer.content[self._untranslated_text_start:self._untranslated_text_end])
#        self.on_app.print_buff_content()
        
        untranslated_text = self.on_app.curr_buffer.content[self._untranslated_text_start:self._untranslated_text_end]

        a_match = re.match('(\s*)([\s\S]*)\s*$', untranslated_text)
        text_no_spaces = a_match.group(2)
        leading_spaces = a_match.group(1)

#        print '-- CmdInterp.match_untranslated_text: text_no_spaces=\'%s\', leading_spaces=\'%s\'' % (text_no_spaces, leading_spaces)

#          #
#          # Remove leading blanks in untranslated region.
#          #
#          old_pos = self.on_app.curr_buffer.cur_pos
#          old_pos = old_pos - len(leading_spaces)
#          self._untranslated_text_end = self._untranslated_text_end - len(leading_spaces)
#          self.on_app.delete(start=self._untranslated_text_start, end=self._untranslated_text_start + len(leading_spaces))
#          self.on_app.move_to(old_pos)
                
        #
        # Don't bother the user if the untranslated text is just a known symbol
        #
        if not self.known_symbols.symbol_info.has_key(text_no_spaces):
#        print '-- CmdInterp.match_untranslated_text: trying to match untranslated text to a symbol. untranslated_text=\'%s\', self._untranslated_text_start=%s, self._untranslated_text_end=%s' % (untranslated_text, self._untranslated_text_start, self._untranslated_text_end)
            symbol_matches = self.known_symbols.match_pseudo_symbol(untranslated_text)
            if symbol_matches:
                self.dlg_select_symbol_match(symbol_matches)

        #
        # There is no more untranslated region
        #
        self._untranslated_text_start = None
        self._untranslated_text_end = None
        

    def dlg_select_symbol_match(self, symbol_matches):
        """Asks the user to select a match for pseudo symbol.
        
        **INPUTS**
        
        *[SymbolMatch]* symbol_matches -- List of possible matches.
        

        **OUTPUTS**
        
        *none* -- 

        .. [SymbolMatch] file:///./SymDict.SymbolMatch.html"""

        untranslated_text = self.on_app.curr_buffer.content[self._untranslated_text_start:self._untranslated_text_end]

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
#                print '-- CmdInterp.dlg_select_symbol_match: a_match.score()=%s, a_match.__dict__=%s' % (a_match.score(), a_match.__dict__)
            sys.stdout.write('\n> ')
            answer = sys.stdin.readline()
            answer_match = re.match('\s*([\d])+\s*', answer)
            if answer_match:
                choice_index = int(answer_match.group(1)) - 1
                if choice_index < len(symbol_matches) and choice_index >= -1:

                    good_answer = 1
            if not good_answer:
                print 'Invalid answer \'%s\'' % answer

        #
        # Accept the match
        #
        if choice_index >= 0:
            #
            # A match was chosen. Accept it and type it instead of the
            # untranslated text.
            #
            chosen_match = symbol_matches[choice_index]
            self.known_symbols.accept_symbol_match(chosen_match)

            #
            # Insert matched symbol, then go back to where we were
            #
            old_pos = self.on_app.curr_buffer.cur_pos
            self.on_app.insert_indent(chosen_match.native_symbol, '', start=self._untranslated_text_start, end=self._untranslated_text_end)
            new_pos = old_pos + len(chosen_match.native_symbol) - (self._untranslated_text_end - self._untranslated_text_start)
            self.on_app.move_to(new_pos)
            
        
        #
        # Now, there is no more untranslated text.
        #
        self._untranslated_text_start = None
        self._untranslated_text_end = None
            

    def chop_symbol(self, command):
        """Chops off the beginning of a string if it matches a known symbol.

        If more than one symbols are possible, returns the symbol that
        consumes the greateest number of words from command.
        
        **INPUTS**
        
        *STR* command -- the string from which we want to chop off a symbol.
        

        **OUTPUTS**

        Returns a pair *(best_symbol, rest)* where:
        
        *STR* best_symbol -- is the symbol that was chopped off (in native
         format). If *None*, it means *command* did not start with a
         symbol.

        *STR* rest -- is what was left of *command* after the symbol
         was chopped off.
        
        """

#        print '-- CmdInterp.chop_symbols: command=%s' % command

        (best_symbol, rest) = (None, command)

        #
        # Split the command into words
        #
        command = re.sub('(\W+)', ' \\1 ', command)
        command = re.sub('(^\s+|\s+$)', '', command)
        words = re.split('\s+', command)                
        upto = len(words)

        #
        # Starting with the whole command and dropping words from the end,
        # check if that corresponds to a known symbol.
        #
        while upto:
            a_spoken_form = string.join(words[0:upto], ' ')
            a_spoken_form = string.lower(a_spoken_form)
#            print '-- CmdInterp.chop_symbols: upto=%s, a_spoken_form=%s' % (upto, a_spoken_form)
            if self.known_symbols.spoken_form_info.has_key(a_spoken_form):
                # This corresponds to the spoken form of a symbol
#                print '-- CmdInterp.chop_symbols: matches a known symbol'
                best_symbol = self.choose_best_symbol(a_spoken_form, self.known_symbols.spoken_form_info[a_spoken_form].symbols)
                words = words[upto:]
                rest = string.join(words, ' ')
                break
            upto = upto - 1
        return (best_symbol, rest)
        
        


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
            re.sub('\s+', ' ', a_spoken_form)
            re.sub('^\s+', '', a_spoken_form)
            re.sub('\s+$', '', a_spoken_form)
            a_spoken_form = string.lower(a_spoken_form)

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
            else:
                #
                # First time indexed. Create a new list of CSCs for that
                # spoken form, and add it to the SR vocabulary.
                #
                self.cmd_index[a_spoken_form] = [acmd]
                if not os.environ.has_key('VCODE_NOSPEECH') and add_voc_entry:
                    sr_interface.addWord(a_spoken_form)



    def load_language_specific_aliases(self):
        
        """Loads words specific to the language of the current buffer,
        if needed.

        Also, unloads words specific to previously loaded language if needed.
        
        **INPUTS**
        
        *none*

        **OUTPUTS**
        
        *none* -- 
        """

        language = self.on_app.curr_buffer.language
        last_language = self.last_loaded_language
#        print '-- CmdInterp.load_language_specific_aliases: called, language=%s, last_language=%s' % (language, last_language)
#        print '-- CmdInterp.load_language_specific_aliases: self.language_specific_aliases[%s]=%s' % (language, self.language_specific_aliases[language])
        if language != last_language:
            #
            # Remove words from previous language
            #
            if self.language_specific_aliases.has_key(last_language):
                for a_word in self.language_specific_aliases[last_language]:
                    sr_interface.deleteWord(a_word)
            
            #
            # Add words for new language
            #
            if self.language_specific_aliases.has_key(language):
                for a_word in self.language_specific_aliases[language]:
                    sr_interface.addWord(a_word)

            self.last_loaded_language = language
            
#        print '-- CmdInterp.load_language_specific_aliases: finished'
