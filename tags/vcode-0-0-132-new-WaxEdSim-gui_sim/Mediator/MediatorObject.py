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
#import traceback
import actions_gen, AppState, CmdInterp, cont_gen, CSCmd, Object, re, sr_interface, SymDict, vc_globals

import debug
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
            
        
def do_nothing(*positional, **keywords):
    pass

class AppCbkFilter(Object.OwnerObject, AppState.AppCbkHandler):
    """object which filters callbacks from a MediatorObject's AppState

    **INSTANCE ATTRIBUTES**

    *MediatorObject mediator* -- reference to the parent MediatorObject

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, the_mediator, **args):
	self.deep_construct(AppCbkFilter,
	                    {
			     'mediator': the_mediator
			    }, args)
	self.name_parent('mediator')

    def close_app_cbk(self, instance, unexpected = 0):
	"""callback from AppState which indicates that the application has 
	closed or disconnected from the mediator

	**INPUTS**

	*STR* instance -- name of the application instance to be removed
      
 	*BOOL unexpected* -- 1 if the editor broke the connection
	without first sending an editor_disconnecting message
   
	**OUTPUTS**

	*none*
	"""
# for now at least, this does the same thing as delete_instance
	self.mediator.close_app_cbk(instance, unexpected = unexpected)

    def close_buffer_cbk(self, instance, buff_name):
	"""callback from AppState which notifies us that the application
	has closed a buffer

	**INPUTS**

	*STR* instance -- name of the application instance 

	*STR* buff_name -- name of the buffer which was closed

	**OUTPUTS**

	*none*
	"""
# ignored by MediatorObject
	pass

    def open_buffer_cbk(self, instance, buff_name):
	"""callback from AppState which notifies us that the application
	has opened a buffer

	**INPUTS**

	*STR* instance -- name of the application instance 

	*STR* buff_name -- name of the buffer which was closed

	**OUTPUTS**

	*none*
	"""
# ignored by MediatorObject
	pass

    def curr_buff_name_cbk(self, instance, buff_name):
	"""callback from AppState which notifies us that the current
	buffer has changed

	**INPUTS**

	*STR* instance -- name of the application instance 

	*STR* buff_name -- name of the buffer which was closed

	**OUTPUTS**

	*none*
	"""
# ignored by MediatorObject
	pass

    def rename_buffer_cbk(self, instance, old_buff_name, new_buff_name):
	"""callback from AppState which notifies us that the application
	has renamed a buffer

	**INPUTS**

	*STR* instance -- name of the application instance 

	**OUTPUTS**

	*STR* old_buff_name -- old name of the buffer 

	*STR* new_buff_name -- new name of the buffer 

	*none*
	"""
# ignored by MediatorObject
	pass


    def new_window(self, instance):
	"""called when the editor notifies us of a new window for the 
	specified instance

	**INPUTS**

	*STR* instance -- name of the application instance

	**OUTPUTS**

	*BOOL* -- true if window is added
	"""
# ignored by MediatorObject
	pass
    


class MediatorObject(Object.Object):
    """Main object for the mediator.

    Typically, there will be one such object for every application
    that is being controlled through a VoiceCode mediator.
    
    **INSTANCE ATTRIBUTES**

    *ServerMainThread owner* -- server which owns this mediator, or
    None.  Note: if owner is set, the id field MUST be provided.

    STR *id* -- The unique identifier assigned by the server to
    this MediatorObject

    [AppState] *app* -- interface to editor 

    *BOOL owns_app* -- does the MediatorObject own the editor app?  If
    so, it should call app.cleanup() and then delete it when it quits.
    Normally, this should be true, except if the mediator is created for
    regression testing purposes with an editor which is reused by the
    next test.

    *AppCbkFilter cbk_filter* -- object which filters callbacks from
    AppState and passes only close_app_cbk to us.

    [CmdInterp] *interp=CmdInterp.CmdInterp()* -- Command interpreter used to
    translate pseudo-code to native code.
    
    [CommandDictGrammar] *mixed_grammar = None* -- Speech Recognition grammar
    that recognises continuous dictation and forwards the results to the
    *interp* command interpreter.

    [CodeSelectGrammar] code_select_grammar = None -- Grammar for
    selecting a part of the visible code.

    *INT window=0*  -- MSW window handle of the top-level window in which
    to activate the grammars, or 0 to make them global.

    *0-1 exclusive=0* -- Indicates whether the mediator should use
    grammars that are exclusive (1) or non-exclusive (1)

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
    
    def __init__(self, app = None, interp=None,
		 window = 0, owns_app = 1, exclusive=0,
                 allResults = 0, owner = None, id = None, **attrs):
#        print '-- MediatorObject.__init__: called, window=%s' % window
        sr_interface.connect('off')        
        self.deep_construct(MediatorObject,
                            {'app': app,
			     'owns_app': owns_app,
			     'interp': interp,
                             'mixed_grammar': None,
                             'code_select_grammar': None,
			     'window': window,
			     'owner': owner,
			     'id': id,
			     'cbk_filter': AppCbkFilter(self)},
                            attrs,
                            {})
        if self.interp == None:
	    interp = CmdInterp.CmdInterp()
        self.mixed_grammar = \
	    sr_interface.CommandDictGrammar(app = self.app,
		interpreter=self.interp, 
	        window = window, exclusive = exclusive,
                allResults = allResults)
        self.code_select_grammar = \
	    sr_interface.CodeSelectGrammar(app = self.app,
		window = window, exclusive = exclusive,
                allResults = allResults)
        if self.owns_app and self.app:
	    self.app.set_manager(self.cbk_filter)
	    self.app.set_name('dummy')
#	print 'Mediator constructor: allResults = %d\n' % allResults
#	print traceback.extract_stack()

    def define_config_functions(self, names, exclude = []):
        """Adds the appropriate configuration functions to the  given
	namespace, to allow the configuration file to access the
	appropriate mediator methods.  These functions are generally
	bound methods.
        
        **INPUTS**

	*{STR: ANY}* names -- the dictionary or namespace to which to
	add the functions

	*[STR] exclude* -- list of mediator object attribute objects 
	to ignore during reconfiguration.  Currently, the only recognized 
	attributes are ['editors', 'interp'].  MediatorObject may
	exclude some attribute objects not supported by this version, 
	even if they are not specified.
        
        **OUTPUTS**
        
        *none* 
        """        
	names['add_module'] = do_nothing
	names['add_prefix'] = do_nothing
	names['trust_current_window'] = do_nothing
	if 'interp' in exclude:
	    names['add_csc'] = do_nothing
	    names['add_lsa'] = do_nothing
	    names['add_abbreviation'] = do_nothing
	    names['standard_symbols_in'] = do_nothing
	    names['print_abbreviations'] = do_nothing
	else:
	    names['add_csc'] = self.add_csc
	    names['add_lsa'] = self.add_lsa
	    names['add_abbreviation'] = self.add_abbreviation
	    names['standard_symbols_in'] = self.standard_symbols_in
	    names['print_abbreviations'] = self.print_abbreviations


    def configure(self, config_file=vc_globals.default_config_file):
        """Configures a mediator object based on a configuration file.
        
        **INPUTS**
        
        *STR* config_file = vc_globals.default_config_file -- Full path of the config


        **OUTPUTS**
        
        *none* -- 
        """        

                
#	print 'Mediator configure:\n'
#	print traceback.extract_stack()
        if sr_interface.speech_able():
            self.mixed_grammar.load(allResults=self.mixed_grammar.allResults)
	    if self.window == 0:
		self.mixed_grammar.activate()
            self.code_select_grammar.load_with_verbs()
	    if self.window == 0:
		self.code_select_grammar.activate()                
                        
	config_dict = {}
	self.define_config_functions(config_dict)
        try:
            execfile(config_file, config_dict)
        except Exception, err:
            print 'ERROR: in configuration file %s.\n' % config_file
            raise err

        #
        # Compile standard symbols for the different languages
        #
        self.interp.parse_standard_symbols(add_sr_entries=self.interp.known_symbols.sr_symbols_cleansed)
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
        self.interp.cleanup(clean_sr_voc=clean_sr_voc)
    
        if sr_interface.speech_able():
            if self.mixed_grammar:
                self.mixed_grammar.unload()
            if self.code_select_grammar:
                self.code_select_grammar.unload()

            disconnect_from_sr(disconnect, save_speech_files)

	if self.mixed_grammar:
	    self.mixed_grammar.cleanup()
	    self.mixed_grammar = None
	if self.code_select_grammar:
	    self.code_select_grammar.cleanup()
	    self.code_select_grammar = None
	if self.owns_app and self.app:
	    self.app.cleanup()
	    self.app = None
	if self.cbk_filter:
	    self.cbk_filter.cleanup()
	    self.cbk_filter = None
	del self.owner
                
    def close_app_cbk(self, instance_name, unexpected = 0):
	"""method called by our AppState to tell us that it is closing, or
	disconnecting from the mediator.  This method is included
	only to allow an external editor to disconnect when we are
	running tcp_server with this old MediatorObject implementation.
	MediatorObject responds to this message only by informing its,
	if any.

	**INPUTS**

	*STR* instance_name -- name of the instance.  This parameter is
	included only for compatibility with the usual call from
	AppState to the AppMgr.  This implementation of MediatorObject
	has only one editor instance, so it ignores this parameter
      
 	*BOOL unexpected* -- 1 if the editor broke the connection
	without first sending an editor_disconnecting message

	**OUTPUTS**

	*none*
	"""
	debug.trace('MediatorObject.close_app_cbk', 
	    'Mediator Object received close app callback')
	if self.owner and self.id:
	    debug.trace('MediatorObject.close_app_cbk', 
		'sending delete instance callback to owner')
	    self.owner.delete_instance_cbk(self.id, 
		unexpected = unexpected)

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

	self.interp.standard_symbols_in(file_list)
    
    def print_abbreviations(self):
	self.interp.print_abbreviations()
    
###############################################################################
# Configuration functions. These are not methods
###############################################################################

        
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


