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
import tcp_server
import AppMgr, RecogStartMgr, GramMgr
import MediatorConsole

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

class NewMediatorObject(Object.OwnerObject):
    """Main object for the mediator.

    Note: there will be one such object, even if multiple editor
    instances are being controlled through a VoiceCode mediator.
    
    **INSTANCE ATTRIBUTES**

    [AppMgr] *editors* -- class which manages editor instances and whe
    their corresponding AppState interfaces.

    *BOOL owns_editors* -- does the MediatorObject own the application 
    manager?  If so, it should call editors.cleanup() and then delete it 
    when it quits.  Normally, this should be true, except if the mediator 
    is created for regression testing purposes with an editor which is 
    reused by the next test.

    [CmdInterp] *interp=CmdInterp.CmdInterp()* -- Command interpreter used to
    translate pseudo-code to native code.

    [ServerMainThread] *server* -- Server to listen for connections
    from new editors, or None if the mediator should operate only with
    an internal test editor

    [MediatorConsole] *console* -- GUI console for viewing mediator
    status, allowing the user to close the mediator when it is running
    as a server, and for invoking the correction dialog boxes.  May be
    None if the mediator is not running in GUI mode

    *STR test_suite* -- suite of tests to run (see auto_test.py), or
    None

    *BOOL global_grammars* -- should this instance use global grammars for 
    regression testing (ignored if test_suite is None)

    *BOOL exclusive* -- should this instance use exclusive grammars for 
    regression testing (ignored if test_suite is None)

    *BOOL test_next* -- flag to indicate that the mediator should run
    regression tests using the next editor to connect

    *STR config_file* -- file which was used to configure the mediator,
    and which will be the default to use if reconfigure is called
    (usually only by init_simulator_regression during regression tests)

    **CLASS ATTRIBUTES**
    
    *none* --

    ..[AppMgr] file:///./AppMgr.AppMgr.html
    ..[CmdInterp] file:///./CmdInterp.CmdInterp.html
    ..[ServerSingleThread] file:///./ServerSingleThread.tcp_server.html
    """
    
    def __init__(self, interp = None,
      		 editors = None,
		 owns_editors = 1, 
		 server = None,
		 console = None,
		 test_suite = 0, global_grammars = 0, exclusive = 0, 
                 **attrs):
        sr_interface.connect('off')        
        self.deep_construct(NewMediatorObject,
                            {'editors': editors,
			     'owns_editors': owns_editors,
			     'server': server,
			     'console': console,
			     'interp': interp,
			     'test_suite': test_suite,
			     'global_grammars': global_grammars,
			     'exclusive': exclusive,
			     'test_next': 0,
			     'config_file': None
			    },
                            attrs,
                            {})
	if self.interp == None:
	    self.new_interpreter()

    def new_interpreter(self):
	"""create a new interpreter

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	if self.interp:
	    self.interp.cleanup(clean_sr_voc=1)
	self.interp = CmdInterp.CmdInterp()

    def configure(self, config_file = None):
        """Configures a mediator object based on a configuration file.
	Must be called before (and only before) run.
        
        **INPUTS**
        
        *STR* config_file -- Full path of the config file.  Defaults to
        vc_globals.default_config_file 

        **OUTPUTS**
        
        *none* -- 
        """        

#	print 'Mediator configure:\n'
#	print traceback.extract_stack()
	self._configure_from_file(config_file = config_file)

    def _configure_from_file(self, exclude = [], config_file = None):
	"""private method used by configure and reconfigure to perform
	 actual configuration.

        **INPUTS**
        
	*[STR] exclude* -- list of mediator object attributes objects 
	to ignore during reconfiguration.  Currently, the only recognized 
	attributes are ['editors', 'interp'].
	
        *STR* config_file* -- Full path of the config file.  Defaults to
	the vc_globals.default_config_file 

        **OUTPUTS**
        
        *none*
        """        

	config_dict = {}
	if not 'editors' in exclude:
	    self.before_app_mgr_config(config_dict)
	if not 'interp' in exclude:
	    self.before_interp_config(config_dict)
        try:
            execfile(config_file, config_dict)
        except Exception, err:
            print 'ERROR: in configuration file %s.\n' % config_file
            raise err

# if successful, store file name so the reconfigure method can reuse it
	self.config_file = config_file

        #
        # Compile standard symbols for the different languages
        #
	if not 'interp' in exclude:
	    self.interp.parse_standard_symbols(add_sr_entries = 
		self.interp.known_symbols.sr_symbols_cleansed)
# what does this mean?  
	    self.interp.known_symbols.sr_symbols_cleansed = 0

    def before_app_mgr_config(self, config_dict, ignore = 0):
	"""called by configure to add the functions pertaining to
	AppMgr configuration to the configuration dictionary.  If
	ignore is true, this method will instead add dummy versions of those
	functions which will do nothing.

	**INPUTS**

	*{STR: ANY} config_dict* -- dictionary to which to add
	interpreter configuration functions.  This dictionary will be
	used as the namespace for executing the configuration file.

	*BOOL ignore* -- if true, add dummy versions of the interpreter
	configuration functions, so that calls to these functions from
	the configuration file will be ignored.  Normally, reset should
	be false if ignore is true
	"""
	if self.ignore:
	    config_dict['add_module'] = do_nothing
	else:
	    config_dict['add_module'] = self.add_module

    def before_interp_config(self, config_dict, reset = 1, ignore = 0):
	"""called by configure to reset or replace the current interpreter 
	(unless reset is false), and add the functions pertaining to
	interpreter configuration to the configuration dictionary.  If
	ignore is true, this method will add dummy versions of those
	functions which will do nothing.

	**INPUTS**

	*{STR: ANY} config_dict* -- dictionary to which to add
	interpreter configuration functions.  This dictionary will be
	used as the namespace for executing the configuration file.

	*BOOL reset* -- if true, reset the current interpreter, or
	replace it with a fresh one

	*BOOL ignore* -- if true, add dummy versions of the interpreter
	configuration functions, so that calls to these functions from
	the configuration file will be ignored.  Normally, reset should
	be false if ignore is true
	"""
	if reset:
	    self.new_interpreter()
	if self.ignore:
	    config_dict['add_csc'] = do_nothing
	    config_dict['add_lsa'] = do_nothing
	    config_dict['add_abbreviation'] = do_nothing
	    config_dict['standard_symbols_in'] = do_nothing
	    config_dict['print_abbreviations'] = do_nothing
	else:
	    config_dict['add_csc'] = self.add_csc
	    config_dict['add_lsa'] = self.add_lsa
	    config_dict['add_abbreviation'] = self.add_abbreviation
	    config_dict['standard_symbols_in'] = self.standard_symbols_in
	    config_dict['print_abbreviations'] = self.print_abbreviations

    def reconfigure(self, exclude = ['editors'], config_file=None):
        """reconfigure an existing mediator object.  Unlike configure,
	reconfigure may be called while the mediator object is already
	running.  By default, reconfigure will use the same file used by
	configure, or the vc_globals.default_config_file if configure
	did not record the filename.
	
        **INPUTS**
        
	*[STR] exclude* -- list of mediator object attributes objects 
	to ignore during reconfiguration.  Currently, the only recognized 
	attributes are ['editors', 'interp'].
	
        *STR* config_file* -- Full path of the config file.  If None,
	then use the same one used previously by configure, or
	the vc_globals.default_config_file if configure
	did not record the filename.

        **OUTPUTS**
        
        *none* -- 
        """        
	file = config_file
	if not file:
	    file = self.config_file
	self._configure_from_file(exclude = exclude, config_file = file)


    def run(self):
	"""starts the mediator

	**NOTE:** make sure to configure the mediator before calling run

	**NOTE:** the behavior of this method varies drastically
	depending on the server attribute:
	
        (1) If there is no server, but there is a GUI console, this
	method will return so that the GUI can start its message loop.
	
        (2) If there is no server and no GUI console, this
	method will run the EdSim (internal) editor simulator, which 
	prompts for commands indefinitely.

        (3) If there is a server, this method will call its run method.  
	If the server has an internal message loop, that method will not 
	return until the server has quit, so neither will this method.  
	If the server has no internal message loop, then this method
	will return so that the GUI start its message loop.

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	if self.server == None:
	    if self.console != None:
		return
	    self.run_simulator()
	    return
	if self.test_suite != None:
	    self.test_next = 1
	self.server.run()

    def run_simulator(self):
	"""runs the editor simulator (EdSim).  This method is used only
	if there is neither a server for external editors nor a GUI
	console.

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	if self.test_suite:
#	    run tests
	    pass
	else:
#	    run simulator in interactive mode
	    pass

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
            disconnect_from_sr(disconnect, save_speech_files)

	if self.owns_editors and self.editors:
	    self.editors.cleanup()
	    del self.app
                
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

    def add_module(self, module):
	"""add a new KnownTargetModule to the AppMgr/RecogStartMgr

	**INPUTS**

	*KnownTargetModule* module -- the new module

	**OUTPUTS**

	*BOOL* -- true unless a module of the same name already exists
	"""
	return self.editors.add_module(module)

    def window_info(self):
	"""find the window id, title, and module of the current window

	**INPUTS**

	*none*

	**OUTPUTS**

	*(INT, STR, STR)* -- the window id, title, and module name
	"""
	return self.editors.window_info()

    
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


# defaults for vim - otherwise ignore
# vim:sw=4
