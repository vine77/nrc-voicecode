import os, re, string

import auto_test, config, natlink, vc_globals
from actions_C_Cpp import *
from actions_py import *
from AppState import AppState
from cont_gen import ContC, ContPy
from CSCmd import CSCmd
from EdSim import EdSim
from Object import Object
import SymDict
import sr_interface
#import VoiceDictation

class CmdInterp(Object):
    """Interprets Context Sensitive Commands spoken into a given application.
    
    **INSTANCE ATTRIBUTES**

    [AppState] *app=AppState()* -- application for which we are
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

    *{STR: [STR]}* language_specific_words = {} -- Key is the name of
     a programming language. Value is a list of written form\spoken
     form words specific to a language. These words are loaded
     automatically when we are in a source buffer of that language and
     removed when we change to a buffer in a different language.

    *STR* prev_loaded_language = None -- Name of the previous language
     for which the language specific words were loaded.
   
    
    CLASS ATTRIBUTES**

    *none* --
        
    .. [AppState] file:///./AppState.AppState.html
    .. [Context] file:///./Context.Context.html
    .. [SymDict] file:///./SymDict.SymDict.html"""
    
    def __init__(self, app=AppState(), **attrs):
        self.deep_construct(CmdInterp,
                            {'app': app, 'cmd_index': {}, \
                             'known_symbols': SymDict.SymDict(), \
                             'cached_regexp': '',\
                             'cached_regexp_is_dirty': 1,\
                             'language_specific_words': {},\
                             'prev_loaded_language': None},\
                            attrs)

#      def refresh_dict_buff(self, moduleInfo):
#          """Refresh the dictation object's internal buffer."""

#          print '-- CmdInterp.refresh_dict_buff: called'
#          buff = self.app.curr_buffer
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
#          self.app.print_buff_content()
        

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

        *STR cmd* is the spoken form of the command."""
        
        #
        # Interpret the begining of the command until nothing left to
        # interpret.
        #
        
#        print '-- CmdInterp.interpret_NL_cmd: self.all_cmds_regexp()=%s' % self.all_cmds_regexp()
        regexp = '^(\s*)(' + self.all_cmds_regexp() + ')(\s*)'
        while (not cmd == ''):
            #
            # Check for a CSC at the beginning of the command, and compute
            # length of string it consumes
            #
            csc_consumes = 0
            csc_match = re.match(regexp, cmd)
            if (csc_match):
                csc_consumes = csc_match.end(2) - csc_match.start(2) + 1

            #
            # Check if command starts with a known symbol, and compute length
            # of string it consumes
            #
            (a_symbol, cmd_without_symbol) = self.chop_symbol(cmd)
            symbol_consumes = len(cmd) - len(cmd_without_symbol)

#            print '-- CmdInterp.interpret_NL_cmd: csc_consumes=%s, symbol_consumes=%s' % (csc_consumes, symbol_consumes)
            #
            # Translate either CSC or known symbol, depending on which of the
            # two consumes the longest part of the NL command
            #
            if csc_consumes and csc_consumes >= symbol_consumes:
                #
                # The CSC consumes more than the symbol, so translate it.
                # Try every possible contexts until one applies
                #                
                cmd_without_csc = cmd[csc_match.end():]
                orig_spoken_form = csc_match.group(2)
#                print '-- CmdInterp.interpret_NL_cmd: matched spoken form \'%s\'' % orig_spoken_form                                
                indexed_spoken_form = orig_spoken_form
                re.sub('\s+', ' ', indexed_spoken_form)
                CSCs = self.cmd_index[string.lower(indexed_spoken_form)]
                applied = 0
                for aCSC in CSCs:
                    applied = aCSC.interpret(self.app)
                    if (applied):
                        break
                if applied:
#                    print '-- CmdInterp.interpret_NL_cmd: applied CSC \'%s\'' % indexed_spoken_form
                    cmd = cmd_without_csc
                else:
                    #
                    # None of the contexts applied.
                    #
                    if symbol_consumes:
                        #
                        # Insert the symbol after all
                        #
#                        print '-- CmdInterp.interpret_NL_cmd: inserted symbol %s' % symbol
                        self.app.insert(symbol)
                        cmd = cmd_without_symbol
                    else:
                        #
                        # Just remove a word from the beginning of the
                        # command and insert it into the application's buffer
                        #
#                        print '-- CmdInterp.interpret_NL_cmd: inserted first word as is'
                        amatch = re.match('(^\s*[^\s]*)', cmd)
                        self.app.insert_indent(amatch.group(1), '')
                        cmd = cmd[amatch.end():]
                        cmd = cmd_without_csc
                
            elif symbol_consumes:
                #
                # Command doesn't start with CSC, or CSC consumes less than
                # the symbol.
                #
                # So, insert the symbol
                #
#                print '-- CmdInterp.interpret_NL_cmd: inserted symbol %s' % a_symbol                
                self.app.insert_indent(a_symbol, '')
                cmd = cmd_without_symbol

            else:
                #
                # Command starts with neither CSC or symbol.
                # Just remove a word from the beginning of the
                # command and insert it into the application's buffer
                #
#                print '-- CmdInterp.interpret_NL_cmd: inserted first word as is'                
                amatch = re.match('(^\s*[^\s]*)', cmd)
                self.app.insert_indent(amatch.group(1), '')
                cmd = cmd[amatch.end():]


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

    def index_csc(self, acmd):
        """Add a new csc to the command interpreter's command dictionary

        [CSCmd] *acmd* is the command to be indexed.

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
                if not os.environ.has_key('VCODE_NOSPEECH'):
#                    VoiceDictation.addWord(a_spoken_form)
                    sr_interface.addWord(a_spoken_form)

def self_test():    
    #
    # Create a command interpreter connected to the editor simulator
    #
    config.interp = CmdInterp(app=EdSim())
    acmd = CSCmd(spoken_forms=['for', 'for loop'], meanings=[[ContC(), c_simple_for], [ContPy(), py_simple_for]])
    config.add_csc(acmd)
    acmd = CSCmd(spoken_forms=['loop body', 'goto body'], meanings=[[ContC(), c_goto_body], [ContPy(), py_goto_body]])
    config.add_csc(acmd)

    
    config.interp.app.open_file(vc_globals.test_data + os.sep + 'small_buff.c')
    config.interp.app.goto(41)
    print '\n\n>>> Testing command interpreter\n\n'
    print '\n>>> Interpreting \'for loop index loop body\' in a C buffer'    
    print '\n>>> Current buffer is:\n'
    config.interp.app.print_buff_content()
    config.interp.interpret_NL_cmd('for loop index loop body')
    print '\n>>> Buffer is now:'
    config.interp.app.print_buff_content()
    

    config.interp.app.open_file(vc_globals.test_data + os.sep + 'small_buff.py')
    config.interp.app.goto(43)
    config.interp.app.curr_buffer.language = 'python'
    print '\n>>> Interpreting \'for loop index loop body\' in a Python buffer'    
    print '\n>>> Current buffer is:\n'
    config.interp.app.print_buff_content()
    config.interp.interpret_NL_cmd('for loop index loop body')
    print '\n>>> Buffer is now:'
    config.interp.app.print_buff_content()


#
# Initialise config.interp here instead of in vc_globals.py.
# This is because CmdInterp.py imports vc_globals.py. But when vc_globals.py
# is imported from CmdInterp.py, the class CmdInterp is not yet defined.
# Therefore we couldn't access CmdInterp.CmdInterp() from within vc_globals.py
# at that point.
#
# This is a silly problem with Python really...
#
#
# Actually, now we have put the interp object in config.py, cause circular
# reference problems kept creeping up.
# config.interp = CmdInterp(app=EdSim())


#
# Add a regression test for this module
#
auto_test.add_test('CmdInterp', self_test, 'self-test for CmdInterp.py')


if (__name__ == '__main__'):
    self_test()
