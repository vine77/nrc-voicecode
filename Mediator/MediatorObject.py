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

import sys
import actions_gen, AppState, CmdInterp, cont_gen, CSCmd, Object, re, sr_interface, SymDict, vc_globals

"""Defines main class for the mediator.

**MODULE VARIABLES**


..[MediatorObject] file:///./MediatorObject.MediatorObject.html"""

# to_configure = None

# no longer used: [MediatorObject] *to_configure* -- When configuring a mediator object, we temporarily assign it to this global variable so that it be accessible from the various configuration function.


def disconnect_from_sr(disconnect, save_speech_files):
    """Save SR user and disconnect from SR.
    **INPUTS**
        
    *BOOL* disconnect -- true iif should disconnect from SR 
        
    *BOOL* save_speech_files -- true iif should save user. If *None*, prompt user.

        
    **OUTPUTS**
        
    *none* -- 
    """

#    print '-- MediatorObject.disconnect_from_sr: disconnect=%s, save_speech_files=%s' % (disconnect, save_speech_files)
    if sr_interface.speech_able():
        #
        # Ask the user if he wants to save speech files
        #
        while save_speech_files == None:
            sys.stdout.write('Would you like to save your speech files (y/n)?\n> ')
            answer = sys.stdin.readline()
            answer = answer[:len(answer)-1]
       
            if answer == 'y':
                save_speech_files = 1
            elif answer == 'n':
                save_speech_files = 0
           
            if save_speech_files == None:
                print "\nPlease answer 'y' or 'n'."

        if save_speech_files and sr_interface.sr_user_needs_saving:
            print 'Saving speech files. This may take a moment ...'
            sr_interface.saveUser()
            print 'Speech files saved.'

        if disconnect: sr_interface.disconnect()
            
        


class MediatorObject(Object.Object):
    """Main object for the mediator.

    Typically, there will be one such object for every application
    that is being controlled through a VoiceCode mediator.
    
    **INSTANCE ATTRIBUTES**

    [CmdInterp] *interp=CmdInterp.CmdInterp()* -- Command interpreter used to
    translate pseudo-code to native code.
    
    [CommandDictGrammar] *mixed_grammar = None* -- Speech Recognition grammar
    that recognises continuous dictation and forwards the results to the
    *interp* command interpreter.

    [CodeSelectGrammar] code_select_grammar = None -- Grammar for
    selecting a part of the visible code.

    *INT window=0*  -- MSW window handle of the top-level window in which
    to activate the grammars, or 0 to make them global.

    *0-1 exclusive=0* -- Indicates whether the mediator should use grammars that
    are exclusive (1) or non-exclusive (1)

    *0-1 allResults=0* -- Indicates whether or not the grammars used by the
    mediator should receive all recognition results (even those intercepted by
    other grammars). Typically set to 0, except when running regression test
    (in which case, VoiceCode must receive all recognition results, even if
    user is working in an other window).
        
    CLASS ATTRIBUTES**
    
    *none* --

    ..[AppState] file:///./AppState.AppState.html
    ..[CmdInterp] file:///./CmdInterp.CmdInterp.html
    ..[CommandDictGrammar] file:///./sr_interface.CommandDictGrammar.html
    ..[CodeSelectGrammar] file:///./sr_interface.CodeSelectGrammar.html"""
    
    def __init__(self, interp=CmdInterp.CmdInterp(), window = 0, exclusive=0,
                 allResults = 0, **attrs):
#        print '-- MediatorObject.__init__: called, window=%s' % window
        sr_interface.connect('off')        
        self.deep_construct(MediatorObject,
                            {'interp': interp,
                             'mixed_grammar': None,
                             'code_select_grammar': None,
			     'window': window},
                            attrs,
                            {})
        self.mixed_grammar = \
	    sr_interface.CommandDictGrammar(interpreter=self.interp, 
	        window = window, exclusive = exclusive,
                allResults = allResults)
        self.code_select_grammar = \
	    sr_interface.CodeSelectGrammar(interpreter=self.interp,
		window = window, exclusive = exclusive,
                allResults = allResults)


    def configure(self, config_file=vc_globals.default_config_file):
        """Configures a mediator object based on a configuration file.
        
        **INPUTS**
        
        *STR* config_file = vc_globals.default_config_file -- Full path of the config


        **OUTPUTS**
        
        *none* -- 
        """        
#        global to_configure

#        print '-- MediatorObject.configure: config_file=%s' % config_file
        
#        to_configure = self
        
        if sr_interface.speech_able():
#            print '-- MediatorObject.configure: loading grammars'
            self.mixed_grammar.load(allResults=self.mixed_grammar.allResults)
	    if self.window == 0:
#                print '-- MediatorObject.configure: activating self.mixed_grammar'
		self.mixed_grammar.activate()
            self.code_select_grammar.load_with_verbs()
	    if self.window == 0:
		self.code_select_grammar.activate()                
                        
	config_dict = {}
	config_dict['add_csc'] = self.add_csc
	config_dict['add_lsa'] = self.add_lsa
	config_dict['add_abbreviation'] = self.add_abbreviation
	config_dict['standard_symbols_in'] = self.standard_symbols_in
	config_dict['print_abbreviations'] = self.print_abbreviations
        try:
            execfile(config_file, config_dict)
        except Exception, err:
            print 'ERROR: in configuration file %s.\n' % config_file
            raise err

        #
        # Compile standard symbols for the different languages
        #
        self.interp.known_symbols.parse_standard_symbols(add_sr_entries=self.interp.known_symbols.sr_symbols_cleansed)
        self.interp.known_symbols.sr_symbols_cleansed = 0

#        to_configure = None

    def quit(self, clean_sr_voc=0, save_speech_files=None, disconnect=1):
        """Quit the mediator object

        **INPUTS**
        
        *BOOL* clean_sr_voc=0 -- If true, remove all SR entries for known
        symbols.

        *BOOL* save_speech_files = None -- Indicates whether or not
        speech files should be saved. If *None*, then ask the user.

        *BOOL* disconnect = 1 -- Indicates whether or not to disconnect from
        the SR system.

        **OUTPUTS**
        
        *none* --
        """            
        #
        # Cleanup the vocabulary to remove symbols from NatSpeak's vocabulary,
        # but don't save SymDict to file (we want the symbols and
        # abbreviations to still be there when we come back.
        #
        self.interp.known_symbols.cleanup(clean_sr_voc=clean_sr_voc)
    
        if sr_interface.speech_able():
            if self.mixed_grammar:
                self.mixed_grammar.unload()
            if self.code_select_grammar:
                self.code_select_grammar.unload()

            disconnect_from_sr(disconnect, save_speech_files)
                
    def add_csc(self, acmd, add_voc_entry=1):
	"""Add a new Context Sensitive Command.

	[CSCmd] *acmd* is the command to add.

	*BOOL add_voc_entry = 1* -- if true, add a SR vocabulary entry
	for the CSC's spoken forms
	

	.. [CSCmd] file:///./CSCmd.CSCmd.html"""

	self.interp.add_csc(acmd, add_voc_entry)


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
	
        self.interp.add_lsa(spoken_forms, meanings)

    def add_abbreviation(self, abbreviation, expansions):
	"""Add an abbreviation to VoiceCode's abbreviations dictionary.

	**INPUTS**

	*STR* abbreviation -- the abbreviation 

	*[STR]* expansions -- list of possible expansions


	**OUTPUTS**

	*none* -- 
	"""
	self.interp.add_abbreviation(abbreviation, expansions, user_added=1)


    def standard_symbols_in(self, file_list):
	"""Compile symbols defined in a series of source files"""

#    print '-- MediatorObject.standard_symbols_in: file_list=%s' % repr(file_list)
	self.interp.standard_symbols_in(file_list)
    
    def print_abbreviations(self):
	self.interp.print_abbreviations()
    
###############################################################################
# Configuration functions. These are not methods
###############################################################################

#def add_csc(acmd, add_voc_entry=1):
#    """Add a new Context Sensitive Command.
#
#    [CSCmd] *acmd* is the command to add.
#
#    *BOOL add_voc_entry = 1* -- if true, add a SR vocabulary entry
#    for the CSC's spoken forms
#    
#
#    .. [CSCmd] file:///./CSCmd.CSCmd.html"""
#
#    global to_configure
#    to_configure.interp.index_csc(acmd, add_voc_entry)
#
#
#def add_lsa(spoken_forms, meanings):
#    """Add a language specific word.
#
#    These words get added and removed dynamically from the SR
#    vocabulary, depending on the language of the active buffer.
#
#    A redundant CSC is also added to allow translation of the LSA at
#    the level of the Mediator, in cases where NatSpeak prefers to
#    recognise the LSA as dictated text instead of a spoken/written
#    word (this often happens if the spoken form looks to much like
#    dictated text, e.g. "is not equal to").
#    
#    **INPUTS**
#    
#    *STR* spoken_forms -- List of spoken form of the word.
#
#    *{STR: STR}* meanings -- Dictionary of language specific
#     meanings. Key is the language name and value is the written form
#     of the LSA for that langugage. If language name is *None*, then
#     it means that this LSA applies for all languages (I know, it
#     doesn't make much sense syntactically).
#    
#    **OUTPUTS**
#    
#    *none* -- 
#    """
#    
#    global to_configure
#
##    print '-- MediatorObject.add_lsa: spoken_forms=%s' % spoken_forms
#    
#
#    language_specific_aliases = to_configure.interp.language_specific_aliases
#    for a_meaning in meanings.items():
#        language, written_as = a_meaning
#        for spoken_as in spoken_forms:
#	    clean_spoken = sr_interface.clean_spoken_form(spoken_as)
#            entry = sr_interface.vocabulary_entry(spoken_as, written_as)
#            vc_entry = sr_interface.vocabulary_entry(spoken_as, written_as, clean_written=0)
#            
#            if not language_specific_aliases.has_key(language):
#                language_specific_aliases[language] = {}
#
#	    language_specific_aliases[language][clean_spoken] = written_as
#
#            #
#            # Add LSA to the SR vocabulary
#            #
#            sr_interface.addWord(entry)
        
def associate_language(extension, language):
    """Add an association between a file extension and a programming
    language.

    **INPUTS**

    *STR* extension -- file names that end with this extension
    will be asociated with language *languate*

    *STR* language -- name of the programming language        

    **OUTPUTS**

    *none* -- 
    """
    SourceBuff.file_language[extension] = language


#def add_abbreviation(abbreviation, expansions):
#    """Add an abbreviation to VoiceCode's abbreviations dictionary.
#
#    **INPUTS**
#
#    *STR* abbreviation -- the abbreviation 
#
#    *[STR]* expansions -- list of possible expansions
#
#
#    **OUTPUTS**
#
#    *none* -- 
#    """
#    global to_configure
#    to_configure.interp.known_symbols.add_abbreviation(abbreviation, expansions, user_added=1)
#

#def standard_symbols_in(file_list):
#    """Compile symbols defined in a series of source files"""
#
##    print '-- MediatorObject.standard_symbols_in: file_list=%s' % repr(file_list)
#    global to_configure
#
#    for a_file in file_list:
#        if not a_file in to_configure.interp.known_symbols.standard_symbol_sources:
#            to_configure.interp.known_symbols.standard_symbol_sources = to_configure.interp.known_symbols.standard_symbol_sources + [a_file]
#    

def define_language(name, definition):
    """Defines the syntax of a programming language.

    **INPUTS**

    *STR* name -- name of the programming language

    [LangDef] definition -- language definition 


    **OUTPUTS**

    *none* -- 

    .. [LangDef] file:///./LangDef.LangDef.html"""

    definition.name = name
    SymDict.language_definitions[name] = definition


#def print_abbreviations():
#    global to_configure
#    to_configure.interp.known_symbols.print_abbreviations()
