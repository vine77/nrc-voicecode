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
import string
import debug
#import traceback
import actions_gen, AppState, CmdInterp, cont_gen, CSCmd, Object, re, sr_interface, SymDict, vc_globals
import tcp_server
import AppMgr, RecogStartMgr, GramMgr
import MediatorConsole
import sr_grammars
import RecogStartMgrNL
import ResMgr
import sr_grammarsNL
import auto_test
import regression
import cPickle

"""Defines main class for the mediator.

**MODULE VARIABLES**


..[MediatorObject] file:///./MediatorObject.MediatorObject.html"""




def disconnect_from_sr(disconnect, save_speech_files):
    """Save SR user and disconnect from SR.
    **INPUTS**
        
    *BOOL* disconnect -- true iif should disconnect from SR 
        
    *BOOL* save_speech_files -- true iif should save user. If *None*, prompt user.

        
    **OUTPUTS**
        
    *none* -- 
    """

#    print '-- MediatorObject.disconnect_from_sr: disconnect=%s, save_speech_files=%s' % (disconnect, save_speech_files)
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

    [CmdInterp] *interp=CmdInterp.CmdInterp()* -- Command interpreter used to
    translate pseudo-code to native code.

    *BOOL symbol_match_dlg* -- use a CmdInterp with symbol match 
    dialog/prompt.  Normally disabled except during regression
    testing, and even then, the persistent mediator object should
    be created symbol_match_dlg = 0, because if
    symbol_match_dlg_regression is set, the mediator object will 
    automatically enable the dialog when regression testing starts 
    and disable it afterwards.  

    *BOOL symbol_match_dlg_regression* -- use a CmdInterp with symbol match 
    dialog/prompt during regression testing, with both persistent
    and temporary mediator objects.

    [ServerNewMediator] *server* -- Server to listen for connections
    from new editors, or None if the mediator should operate only with
    an internal test editor

    *{STR: BOOL} external_editors* -- set of instance names
    of all external editors connected to the mediator via the server

    [MediatorConsole] *the_console* -- GUI console for viewing mediator
    status, allowing the user to close the mediator when it is running
    as a server, and for invoking the correction dialog boxes.  May be
    None if the mediator is not running in GUI mode

    *CLASS* wave_playback -- class constructor for a concrete
    subclass of WavePlayback, or None if no playback is available

    *CorrectUtteranceEvent correct_evt* -- doorbell used to send an
    event to bring up the correction box asynchronously.

    *CorrectRecentEvent correct_recent_evt* -- doorbell used to send an
    event to bring up the correct recent box asynchronously.

    *{STR:ANY} test_args* -- list of test names to run

    *{STR:ANY} test_space* -- if the mediator is started in regression 
    testing mode, test_space is the namespace in which regression tests 
    have been defined and will run.  Otherwise, it should be None.

    *STR pickled_interp* -- CmdInterp as originally configured,
    pickled to speed up regression testing

    *BOOL global_grammars* -- should this instance use global grammars for 
    regression testing (ignored if test_space is None)

    *BOOL exclusive* -- should this instance use exclusive grammars for 
    regression testing (ignored if test_space is None or global_grammars
    is false)

    *STR profile_prefix* -- prefix for filename for output of profiler,
    or None if not profiling (ignored if test_space is None) 

    *BOOL bypass_sr_recog* -- when testing, bypass natlink for 
    dictation utterances (ignored if test_space is None) 

    *BOOL test_next* -- flag to indicate that the mediator should run
    regression tests using the next editor to connect

    *BOOL testing* -- flag indicating that the mediator is currently
    running regression tests.

    *STR config_file* -- file which was used to configure the mediator.
    This file will also be the default to use if reconfigure is called
    (usually only by init_simulator_regression during regression tests)

    *STR user_config_file* -- user-specific file which was used to 
    configure the mediator.
    This file will also be the default to use if reconfigure is called
    (usually only by init_simulator_regression during regression tests)

    **CLASS ATTRIBUTES**
    
    *none* --

    ..[AppMgr] file:///./AppMgr.AppMgr.html
    ..[CmdInterp] file:///./CmdInterp.CmdInterp.html
    ..[ServerNewMediator] file:///./ServerNewMediator.tcp_server.html
    """
    
    def __init__(self, interp = None,
                 server = None,
                 console = None,
                 wave_playback = None,
                 correct_evt = None,
                 correct_recent_evt = None,
                 test_args = None,
                 test_space = None, global_grammars = 0, exclusive = 0, 
                 profile_prefix = None,
                 bypass_sr_recog = 0,
                 symdict_pickle_fname = None,
                 symbol_match_dlg_regression = 1,
                 symbol_match_dlg = 0,
                 **attrs):
        """creates the NewMediatorObject

        **NOTE:** the caller must also call configure before calling
        other methods, or starting the server.
    
        **INPUTS**

        *CmdInterp interp* -- the command interpreter, or None to have
        NewMediatorObject create one

        *BOOL symbol_match_dlg* -- use a CmdInterp with symbol match 
        dialog/prompt.  Normally disabled except during regression
        testing, and even then, the persistent mediator object should
        be created symbol_match_dlg = 0, because if
        symbol_match_dlg_regression is set, the mediator object will 
        automatically the dialog when regression testing starts 
        and disable it afterwards.  

        *BOOL symbol_match_dlg_regression* -- use a CmdInterp with symbol match 
        dialog/prompt during regression testing, with both persistent
        and temporary mediator objects.

        *ServerNewMediator server* -- the TCP server which will listen 
        for new connections from external editors, or None if we are running
        only with internal editors.  The caller must create the server,
        but NewMediatorObject will always own it.  The application which
        creates NewMediatorObject must start the server but only after
        NewMediatorObject has been configured, and should then delete
        its reference to the server.

        *MediatorConsole console* -- GUI console for viewing mediator
        status, allowing the user to close the mediator when it is running
        as a server, and for invoking the correction dialog boxes.  Since
        console is an interface to an underlying GUI, NewMediatorObject
        does not own it, and will not clean up either it or the
        underlying GUI.  May be None if the mediator is not running in 
        GUI mode.

        *CLASS* wave_playback -- class constructor for a concrete
        subclass of WavePlayback, or None if no playback is available

        *CorrectUtteranceEvent correct_evt* -- doorbell used to send an
        event to bring up the correction box asynchronously.

        *{STR:ANY} test_space* -- if the mediator is started in regression 
        testing mode, test_space is the namespace in which regression tests 
        have been defined and will run.  Otherwise, it should be None.

        *BOOL global_grammars* -- should this instance use global grammars for 
        regression testing (ignored if test_space is None)

        *BOOL exclusive* -- should this instance use exclusive grammars for 
        regression testing (ignored if test_space is None or
        global_grammars is false)

        *STR profile_prefix* -- prefix for filename for output of profiler,
        or None if not profiling (ignored if test_space is None) 

        *BOOL bypass_sr_recog* -- when testing, bypass natlink for 
        dictation utterances (ignored if test_space is None) 

        STR *symdict_pickle_fname=None* -- Name of the file containing the
        persistent version of the symbols dictionnary.
        """

        sr_interface.connect('off')        
        self.deep_construct(NewMediatorObject,
                            {'editors': None,
                             'server': server,
                             'external_editors': {},
                             'the_console': console,
                             'wave_playback': wave_playback,
                             'correct_evt': correct_evt,
                             'correct_recent_evt': correct_recent_evt,
                             'interp': interp,
                             'test_args': test_args,
                             'test_space': test_space,
                             'global_grammars': global_grammars,
                             'symdict_pickle_fname': symdict_pickle_fname,
                             'symbol_match_dlg_regression': \
                                  symbol_match_dlg_regression,
                             'symbol_match_dlg': symbol_match_dlg,
                             'exclusive': exclusive,
                             'profile_prefix': profile_prefix,
                             'bypass_sr_recog': bypass_sr_recog,
                             'test_next': 0,
                             'testing': 0, 
                             'pickled_interp': None,
                             'config_file': None,
                             'user_config_file': None
                            },
                            attrs,
                            {})
        self.add_owned('server')
        self.add_owned('editors')
        self.add_owned('the_console')
        self.add_owned('interp')
        if self.the_console:
            self.the_console.set_mediator(self)
        if self.test_args != None and self.test_space != None:
            self.test_next = 1
        if self.interp == None:
            self.new_interpreter(symdict_pickle_fname = symdict_pickle_fname,
                symbol_match_dlg = symbol_match_dlg)
        else:
            self.interp.set_mediator(self)

        if self.editors == None:
            self.new_app_mgr()
        if server:
            server.set_mediator(self)

    def new_app_mgr(self):
        """create a new AppMgr if one was not supplied to  the
        constructor
        
        **INPUTS**

        *none*

        **OUTPUTS**

        *BOOL* -- true if a new AppMgr was sucessfully created
        """
        if self.editors != None:
            return 1 # we've already got one!
        correct_words = []
        if self.the_console:
            correct_words = ["Correct"]
        grammar_factory = \
            sr_grammarsNL.WinGramFactoryNL(correct_words = correct_words, 
                recent_words = ['Recent'], wave_playback = self.wave_playback)
# suppress Correct That if there is no console
# allow Correct Recent, because it has at least a stub implementation
        if self.the_console:
            self.the_console.set_gram_factory(grammar_factory)
        GM_factory = GramMgr.WinGramMgrFactory(grammar_factory, 
            global_grammars = 0, correction = 'basic')
#        res_mgr_factory = \
#            ResMgr.ResMgrStdFactory()
        res_mgr_factory = \
            ResMgr.ResMgrBasicFactory(correct_evt = self.correct_evt,
            correct_recent_evt = self.correct_recent_evt)
        recog_mgr = RecogStartMgrNL.RecogStartMgrNL(GM_factory = GM_factory,
            res_mgr_factory = res_mgr_factory)
        self.editors = AppMgr.AppMgr(recog_mgr, mediator = self)
        return 1
    
    def new_interpreter(self, symdict_pickle_fname = None,
        symbol_match_dlg = 0, no_circle = 0):
        """create a new interpreter

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        if self.interp:
            self.interp.cleanup()
        m = self
        if no_circle:
            m = None
        self.interp = \
            CmdInterp.CmdInterp(symdict_pickle_file = symdict_pickle_fname, 
                disable_dlg_select_symbol_matches = not symbol_match_dlg, 
                mediator = m)

    def console(self):
        """returns a reference to the MediatorConsole which provides the
        GUI correction interfaces.

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        return self.the_console
   
    def interpreter(self):
        """return a reference to the mediator's current CmdInterp object

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        return self.interp
   
    def configure(self, config_file = None, user_config_file = None, exclude_interp = 0):
        """Configures a mediator object based on a configuration file.
        Must be called before (and only before) run.
        
        **INPUTS**
        
        *STR* config_file -- Full path of the config file.  Defaults to
        vc_globals.default_config_file 

        *STR* user_config_file -- Full path of the user config file.  
        Defaults to vc_globals.default_user_config_file 

        *BOOL* exclude_interp -- if true, don't re-configure the
        interpreter

        **OUTPUTS**
        
        *none* -- 
        """        

#        print 'Mediator configure:\n'
#        print traceback.extract_stack()
        exclude = None
        if exclude_interp:
            exclude = ['interp']
        self._configure_from_file(config_file = config_file,
            user_config_file = user_config_file,
            symdict_pickle_fname = self.symdict_pickle_fname, 
            exclude = exclude)
        if self.test_next:
# remove the reference to ourselves before pickling
            self.interp.set_mediator(None)
# pickled interpreter is used only for regression testing, so 
# use symbol_match_dlg setting appropriate for regression testing
            old_setting = self.interp.disable_dlg_select_symbol_matches
            self.interp.disable_dlg_select_symbol_matches = not self.symbol_match_dlg_regression
            self.pickled_interp = cPickle.dumps(self.interp)
            self.interp.set_mediator(self)
            self.interp.disable_dlg_select_symbol_matches = old_setting

    def define_config_functions(self, names, exclude = None,
            reset = 0,
            symdict_pickle_fname = None, symbol_match_dlg = None, 
            add_sr_entries_for_LSAs_and_CSCs = 1):
        """Adds the appropriate configuration functions to the  given
        namespace, to allow the configuration file to access the
        appropriate mediator methods.  These functions are generally
        bound methods.
        
        **INPUTS**

        *{STR: ANY}* names -- the dictionary or namespace to which to
        add the functions

        *[STR] exclude* -- list of mediator object attributes objects 
        to ignore during reconfiguration.  Currently, the only recognized 
        attributes are ['editors', 'interp'].
        
        *BOOL reset* -- if true, reset the current interpreter, or
        replace it with a fresh one

        STR *symdict_pickle_fname=None* -- Name of the file containing the
        persistent version of the symbols dictionnary.

        *BOOL symbol_match_dlg* -- use a CmdInterp with symbol match 
        dialog/prompt.  Normally disabled except during regression
        testing.  If None, use current setting.

        **OUTPUTS**
        
        *none* 
        """        
        if exclude == None:
            exclude = []
        self.before_app_mgr_config(names, ignore = 'editors' in exclude)
        sym_dlg = self.symbol_match_dlg
        if symbol_match_dlg != None:
           sym_dlg = symbol_match_dlg
        self.before_interp_config(names, ignore = 'interp' in exclude,
            reset = reset and ('interp' not in exclude),
            symdict_pickle_fname = symdict_pickle_fname,
            symbol_match_dlg = sym_dlg, 
            add_sr_entries_for_LSAs_and_CSCs = add_sr_entries_for_LSAs_and_CSCs)


    def _configure_from_file(self, exclude = None, config_file = None,
        user_config_file = None,
        reset = 0,
        symdict_pickle_fname = None, symbol_match_dlg = None,
        add_sr_entries_for_LSAs_and_CSCs = 1,
        use_pickled_interp = 0):
        """private method used by configure and reconfigure to perform
         actual configuration.

        **INPUTS**
        
        *[STR] exclude* -- list of mediator object attributes objects 
        to ignore during reconfiguration.  Currently, the only recognized 
        attributes are ['editors', 'interp'].
        
        *STR* config_file* -- Full path of the config file.  Defaults to
        the vc_globals.default_config_file 

        *STR* user_config_file -- Full path of the user config file.  
        Defaults to vc_globals.default_user_config_file 

        *BOOL reset* -- if true, reset the current interpreter, or
        replace it with a fresh one

        STR *symdict_pickle_fname=None* -- Name of the file containing the
        persistent version of the symbols dictionnary.

        *BOOL symbol_match_dlg* -- use a CmdInterp with symbol match 
        dialog/prompt.  Normally disabled except during regression
        testing.  If None, use current setting.

        *BOOL use_pickled_interp* -- if true, reset the interpreter by
        unpickling it from the copy pickled on initialization (if one is
        available)

        **OUTPUTS**
        
        *none*
        """        
        if exclude == None:
            exclude = []
        config_dict = {}
        sym_dlg = self.symbol_match_dlg
        if symbol_match_dlg != None:
           sym_dlg = symbol_match_dlg
        if not 'interp' in exclude:
            if use_pickled_interp and self.pickled_interp:
                self.interp.cleanup(clean_sr_voc = 0, clean_symdict = 0, 
                    resave = 0)
                self.interp = cPickle.loads(self.pickled_interp)
                self.interp.set_mediator(self)
                exclude.append('interp')
# if we've unpickled the interpreter, we don't need to re-configure it
        self.define_config_functions(config_dict, exclude,
            reset = reset,
            symdict_pickle_fname = symdict_pickle_fname,
            symbol_match_dlg = sym_dlg,
            add_sr_entries_for_LSAs_and_CSCs = add_sr_entries_for_LSAs_and_CSCs)
        file = config_file
        if not file:
            file = vc_globals.default_config_file
        execfile(file, config_dict)
# doing execfile directly actually provides better error reporting (the
# traceback is actually reported from the proper line, even when it is
# in another module imported from the config file).  (Probably the same
# effect could be achieved if we put a try block in the config file
# itself)
#        try:
#            execfile(file, config_dict)
#        except Exception, err:
#            print 'ERROR: in configuration file %s.\n' % file
#            raise err
        user_file = user_config_file
        if not user_file:
            if self.test_next:
                user_file = vc_globals.regression_user_config_file
            else:
                user_file = vc_globals.default_user_config_file
        execfile(user_file, config_dict)

# if successful, store file name so the reconfigure method can reuse it
        self.config_file = config_file
        self.user_config_file = user_config_file

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

        *BOOL ignore* -- if true, add dummy versions of the application
        manager configuration functions, so that calls to these functions from
        the configuration file will be ignored.  
        """
        if ignore:
            config_dict['add_module'] = do_nothing
            config_dict['trust_current_window'] = do_nothing
            config_dict['add_prefix'] = do_nothing
        else:
            config_dict['add_module'] = self.add_module
            config_dict['trust_current_window'] = self.trust_current_window
            config_dict['add_prefix'] = self.add_app_prefix

    def before_interp_config(self, config_dict, reset = 0, ignore = 0,
        symdict_pickle_fname = None, symbol_match_dlg = None, 
        add_sr_entries_for_LSAs_and_CSCs = 1):
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

        STR *symdict_pickle_fname=None* -- Name of the file containing the
        persistent version of the symbols dictionnary.

        *BOOL symbol_match_dlg* -- use a CmdInterp with symbol match 
        dialog/prompt.  Normally disabled except during regression
        testing.  If None, use current setting.
        """
        if reset:
            sym_dlg = self.symbol_match_dlg
            if symbol_match_dlg != None:
               sym_dlg = symbol_match_dlg
            self.new_interpreter(symdict_pickle_fname = symdict_pickle_fname,
                symbol_match_dlg = sym_dlg)
            self.interp.add_sr_entries_for_LSAs_and_CSCs = \
                add_sr_entries_for_LSAs_and_CSCs
        if ignore:
            config_dict['interpreter'] = None
            config_dict['add_csc'] = do_nothing
            config_dict['add_csc_set'] = do_nothing
            config_dict['add_lsa'] = do_nothing
            config_dict['add_lsa_set'] = do_nothing
            config_dict['add_abbreviation'] = do_nothing
            config_dict['standard_symbols_in'] = do_nothing
            config_dict['print_abbreviations'] = do_nothing
        else:
            config_dict['interpreter'] = self
            config_dict['add_csc'] = self.add_csc
            config_dict['add_csc_set'] = self.add_csc_set
            config_dict['add_lsa'] = self.add_lsa
            config_dict['add_lsa_set'] = self.add_lsa_set
            config_dict['has_lsa'] = self.has_lsa
            config_dict['add_abbreviation'] = self.add_abbreviation
            config_dict['standard_symbols_in'] = self.standard_symbols_in
            config_dict['print_abbreviations'] = self.print_abbreviations

    def reset(self, config_file = None, user_config_file = None, 
        symdict_pickle_fname = None,
        symbol_match_dlg = None, add_sr_entries_for_LSAs_and_CSCs=1,
        use_pickled_interp = 1):
        """reset the mediator object to continue regression testing with
        a fresh interpreter

        **INPUTS**

        *STR* config_file* -- Full path of the config file.  If None,
        then use the same one used previously by configure, or
        the vc_globals.default_config_file if configure
        did not record the filename.

        *STR* user_config_file* -- Full path of the user config file.  If None,
        then use the same one used previously by configure, or
        the vc_globals.default_user_config_file if configure
        did not record the filename.

        *BOOL symbol_match_dlg* -- use a CmdInterp with symbol match 
        dialog/prompt.  Normally disabled except during regression
        testing.  If None, use current setting.
        
        *BOOL add_sr_entries_for_LSAs_and_CSCs=1* -- see [CmdInterp] attribute 
        by the same name.

        *BOOL use_pickled_interp* -- if true, reset the interpreter by
        unpickling it from the copy pickled on initialization
        
        ..[CmdInterp] file:///./CmdInterp.CmdInterp.html"""
        
#        self.interp.add_sr_entries_for_LSAs_and_CSCs = add_sr_entries_for_LSAs_and_CSCs
        old_add_entries = self.interp.add_sr_entries_for_LSAs_and_CSCs
        sym_dlg = self.symbol_match_dlg
        if symbol_match_dlg != None:
           sym_dlg = symbol_match_dlg
        self.reconfigure(exclude = ['editors'],
            config_file = config_file, 
            user_config_file = user_config_file, reset = 1, 
            symdict_pickle_fname = symdict_pickle_fname,
            symbol_match_dlg = sym_dlg, 
            add_sr_entries_for_LSAs_and_CSCs = add_sr_entries_for_LSAs_and_CSCs,
            use_pickled_interp = use_pickled_interp)
        self.reset_results_mgr()
        self.interp.add_sr_entries_for_LSAs_and_CSCs = old_add_entries

    def reconfigure(self, exclude = None, config_file=None,
        user_config_file = None,
        reset = 0,
        symdict_pickle_fname = None, symbol_match_dlg = None,
        add_sr_entries_for_LSAs_and_CSCs = 1,
        use_pickled_interp = 1):
        """reconfigure an existing mediator object.  Unlike configure,
        reconfigure may be called while the mediator object is already
        running.  By default, reconfigure will use the same files used by
        configure, or the vc_globals.default_config_file  and
        vc_globals.default_user_config_file if configure
        did not record the filenames.
        
        **INPUTS**
        
        *[STR] exclude* -- list of mediator object attributes objects 
        to ignore during reconfiguration.  Currently, the only recognized 
        attributes are ['editors', 'interp'].
        
        *STR* config_file* -- Full path of the config file.  If None,
        then use the same one used previously by configure, or
        the vc_globals.default_config_file if configure
        did not record the filename.

        *STR* user_config_file* -- Full path of the user config file.  If None,
        then use the same one used previously by configure, or
        the vc_globals.default_user_config_file if configure
        did not record the filename.

        *BOOL reset* -- if true, reset the current interpreter, or
        replace it with a fresh one

        STR *symdict_pickle_fname=None* -- Name of the file containing the
        persistent version of the symbols dictionnary.

        *BOOL symbol_match_dlg* -- use a CmdInterp with symbol match 
        dialog/prompt.  Normally disabled except during regression
        testing.  If None, use current setting.

        *BOOL use_pickled_interp* -- if true, reset the interpreter by
        unpickling it from the copy pickled on initialization

        **OUTPUTS**
        
        *none* -- 
        """        
        file = config_file
        if not file:
            file = self.config_file
        user_file = user_config_file
        if not user_file:
            user_file = self.user_config_file
        sym_dlg = self.symbol_match_dlg
        if symbol_match_dlg != None:
           sym_dlg = symbol_match_dlg
        self._configure_from_file(exclude = exclude, config_file = file,
            user_config_file = user_config_file,
            reset = reset,
            symdict_pickle_fname = symdict_pickle_fname,
            symbol_match_dlg = sym_dlg, 
            add_sr_entries_for_LSAs_and_CSCs = add_sr_entries_for_LSAs_and_CSCs,
            use_pickled_interp = use_pickled_interp)

    def remove_other_references(self):
        """additional cleanup to ensure that this object's references to
        its owned objects are the last remaining references

        **NOTE:** subclasses must call their parent class's 
        remove_other_references method, after performing their own duties.
        Also, a class inheriting from two OwnerObject classes MUST
        define remove_other_references and call both subclasses'
        versions

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
# subclasses must call their parent class's remove_other_references
# method, after performing their own duties
#        print 'removing'

# This isn't necessary from an OwnerObject point of view (CmdInterp has
# no circular references).  If you want to clean up the interpreter, you
# should call NMO.quit

#        self.interp.cleanup()

# for now, don't disconnect from sr_interface -- let the creator do that

        self.correct_evt = None
# correct_evt may have a reference to a method of the application which
# owns NewMediatorObject
        Object.OwnerObject.remove_other_references(self)

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
# DCF: contrary to this comment, this *will* save the symbol dictionary, 
# at least according to current defaults for CmdInterp.cleanup
        #
#        print 'quitting'
        debug.trace('NewMediatorObject.quit', 'quit called')
        self.interp.cleanup(clean_sr_voc=clean_sr_voc)
    
        if self.server:
            self.server.mediator_closing()

        if self.editors:
            self.editors.cleanup()
            self.editors = None

        disconnect_from_sr(disconnect, save_speech_files)

#        self.cleanup()
                
    def delete_editor_cbk(self, app_name, instance_name, unexpected = 0):
        """callback from the application manager indicating that
        an editor closed or disconnected from the mediator

        **INPUTS**

        *STR app_name* -- name of the editor 

        *STR instance_name* -- name of the application instance

        *BOOL unexpected* -- for external editors, was the editor
        connection broken unexpectedly, or did the editor notify the
        mediator that it was going to close/disconnect?

        **OUTPUTS**

        *none*
        """
# for now, all editor instance-specific data is stored under AppMgr,
# except for external editors, for which we have the instance name in 
# external_editors and the server has a reference to the
# AppStateMessaging interface.
#
# once we add correction, we may have other instance-specific objects 
# which we will need to clean up.
        try:
            del self.external_editors[instance_name]
        except KeyError:
            pass
        else: 
            s = '%s instance %s disconnected' % (app_name, instance_name)
            if unexpected:
                s = s + ' unexpectedly'
# don't use instance argument because instance we've disconnected
            self.user_message(s)
            self.server.delete_instance_cbk(instance_name, 
                unexpected = unexpected)

# Note: if we have no server, we should quit when the last internal
# editor exits.  However, the application which creates
# NewMediatorObject will be running the internal editor, so it should
# know when it exits and should call our cleanup method

    def _new_test_editor(self, app, server = 1, check_window = 1, 
            window_info = None):
        """private method to a new editor application instance and run
        regression tests.  This method should only be called by
        NewMediatorObject.new_editor.

        **INPUTS**

        *AppState* app --  AppState interface corresponding to the new
        instance

        *BOOL* server -- true if this editor instance is connected to the 
        mediator via the server.

        *BOOL* check_window -- should we check to see if the
        current window belongs to this instance?  Normally ignored
        unless self.global_grammars is false, or the application manager
        is unable to create a universal instance

        *(INT, STR, STR) window_info*  -- window id, title, and module of 
        the current window as detected by the TCP server when it
        originally processed the new editor connection, or None to let
        RSM.new_instance check now.  Normally ignored unless
        check_window is true and either self.global_grammars is false
        or the application manager is unable to create a 
        universal instance.

        **OUTPUTS**

        *BOOL* -- true if the regression tests were run
        """
        instance_name = None
        if self.global_grammars:
            instance_name = self.editors.new_universal_instance(app, 
                exclusive = self.exclusive)
            print 'universal instance named "%s"' % instance_name
        if not instance_name:
            instance_name = self.editors.new_instance(app, 
                check_window = check_window, window_info = window_info)
            print 'ordinary instance named "%s"' % instance_name
        if not instance_name:
            return 0
        app = self.editors.app_instance(instance_name)
# give the user an initial chance to save existing buffers before
# closing them
        app.init_for_test(save = 0)
        app.print_buff_when_changed = 1
        self.test_space['testing'] = \
            regression.PersistentConfigNewMediator(mediator = self,
            editor_name = instance_name, names = self.test_space,
            symbol_match_dlg = self.symbol_match_dlg_regression,
            bypass_sr_recog = self.bypass_sr_recog,
            correction = 'basic')
        self.interp.enable_symbol_match_dlg(self.symbol_match_dlg_regression)
        self.test_space['temp_factory'] = \
             regression.TempConfigNewMediatorFactory(symbol_match_dlg = \
             self.symbol_match_dlg_regression, 
             pickled_interp = self.pickled_interp)
        self.testing = 1
        auto_test.run(self.test_args, profile_prefix = self.profile_prefix)
        self.testing = 0
        app.mediator_closing()
        self.interp.enable_symbol_match_dlg(self.symbol_match_dlg)
        self.editors.delete_instance(instance_name)
        return 1

    def new_editor(self, app, server = 1, check_window = 1, 
            window_info = None, test_editor = 0):
        """add a new editor application instance

        **INPUTS**

        *AppState* app --  AppState interface corresponding to the new
        instance

        *BOOL* server -- true if this editor instance is connected to the 
        mediator via the server.

        *BOOL* check_window -- should we check to see if the
        current window belongs to this instance?

        *(INT, STR, STR) window_info*  -- window id, title, and module of 
        the current window as detected by the TCP server when it
        originally processed the new editor connection, or None to let
        RSM.new_instance check now.  Ignored unless check_window is
        true.

        BOOL *test_editor* -- flag indicating whether or not the editor
        is expecting to be used for regression testing


        **OUTPUTS**

        *STR* -- name of the application instance.  Necessary
        if you want to add windows to the application in the future.
        """
        if test_editor:
            if self.test_space != None and self.test_next:
                self._new_test_editor(app, server = server, 
                    check_window = check_window, window_info = window_info)
                return None
        instance_name = self.editors.new_instance(app, 
            check_window = check_window, window_info = window_info)
# don't use instance argument to user_message here, because the editor
# should display its own message on connection
        self.user_message('%s instance %s connected' %
            (self.editors.app_name(instance_name), instance_name))
        if server:
            if self.server == None:
                msg = 'WARNING: new_editor called with server = 1, but mediator has no server\n'
                sys.stderr.write(msg)
            else:
                self.external_editors[instance_name] = 1
        return instance_name

    def editor_instance(self, instance_name):
        """return a reference to the AppState object corresponding to a
        particular instance. **Note:** Use only temporarily.  Storing 
        this reference is unsafe, and may lead to mediator crashes on 
        calls to its methods, and to failure to free resources.

        **INPUTS**

        *STR* instance -- name of the application instance 

        **OUTPUTS**

        *AppState* -- temporary reference to the corresponding AppState
        object
        """
        return self.editors.app_instance(instance_name)

    def add_csc(self, acmd):
        """Add a new Context Sensitive Command.

        [CSCmd] *acmd* is the command to add.      

        .. [CSCmd] file:///./CSCmd.CSCmd.html"""

        self.interp.add_csc(acmd)

    def add_csc_set(self, set):
        """add CSCs from a set

        **INPUTS**

        *CSCmdSet set* -- the set of commands to add

        **OUTPUTS**

        *none*
        """
        self.interp.add_csc_set(set)

    def has_lsa(self, spoken_form, language = None):
        """check if there is already an LSA defined with this spoken
        form

        **INPUTS**

        *STR spoken_form* -- spoken form to check

        *STR language* -- name of the language in which to check

        **OUTPUTS**

        *BOOL* -- true if such an LSA exists
        """
        return self.interp.has_lsa(spoken_form, language)

    def add_lsa(self, an_LSA):
        """Add a language specific word.

        **INPUTS**
        
        *LSAlias an_LSA* -- language-specific alias (see CmdInterp)
        
        **OUTPUTS**
        
        *none* -- 
        """
        
        self.interp.add_lsa(an_LSA)

    def add_lsa_set(self, set):
        """add LSAs from a set

        **INPUTS**

        *LSAliasSet set* -- the set of aliases to add

        **OUTPUTS**

        *none*
        """
        self.interp.add_lsa_set(set)

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

    def trust_current_window(self, trust = 1):
        """specifies whether the RecogStartMgr should trust that the current
        window corresponds to the editor when the editor first connects to
        VoiceCode, or when it notifies VoiceCode of a new window.

        **INPUTS**

        *BOOL* trust_current_window -- 1 if RSM should trust that the current
        window corresponds to the editor when the editor first connects to
        VoiceCode, or when it notifies VoiceCode of a new window.

        **OUTPUTS**

        *none*
        """
        self.editors.trust_current(trust)

    def add_app_prefix(self, app_name, title_prefix):
        """specifies a title prefix to use for a given editor application.

        **INPUTS**

        *STR* app_name -- name of the editor application

        *STR* title_prefix  -- a unique string for each application, 
        used as the prefix of the title string (which is in turn 
        included as a substring of the window title, if the editor 
        can do so).  The prefix should be entirely alphabetic and
        contain no spaces or punctuation.

        **OUTPUTS**

        *BOOL* -- false if app_name was already known, or prefix wasn't
        unique
        """
        return self.editors.add_prefix(app_name, title_prefix)

    def reset_results_mgr(self, instance_name = None):
        """resets the ResMgr objects for a given editor, erasing any 
        stored utterance and corresponding editor state information.  
        Normally called only as part of resetting the mediator for 
        a new regression test

        **INPUTS**

        *STR instance_name* -- the editor whose data should be reset, or
        None to reset ResMgr data for all editors

        **OUTPUTS**

        *none*
        """
        self.editors.reset_results_mgr(instance_name = instance_name)

    def stored_utterances(self, instance_name):
        """queries the ResMgr to see how many dictated utterances have 
        been stored for the specified editor

        **INPUTS**

        *STR instance_name* -- the editor 

        **OUTPUTS**

        *INT* -- number of utterances which can be retrieved with
        recent_dictation
        """
        return self.editors.stored_utterances(instance_name)

    def recent_dictation(self, instance_name, n = None):
        """returns a list of the most recent SpokenUtterance objects for
        the specified editor

        **Note:** additional dictation into the editor will increment
        the indices of specific utterances, so the mediator must not
        allow dictation into the editor between the call to 
        recent_dictation to get the utterances and the call to 
        reinterpret_recent.

        **INPUTS**

        *STR instance_name* -- the editor 

        *INT n* -- the number of utterances to return, or None to return 
        all available utterances.

        **OUTPUTS**

        *[(SpokenUtterance, INT, BOOL)]* -- the n most recent dictation 
        utterances (or all available if < n), sorted most recent last, 
        each with a corresponding identifying number and a flag indicating 
        if the utterance can be undone and re-interpreted, 
        or None if no utterances are stored.

        The utterance number is unique, within a given editor instance.

        Note:  These utterances should not be stored permanently, nor
        should they be modified except as part of the correction
        process.  Also, the status of whether a given utterance can be
        re-interpreted may change if the user makes other changes to the 
        """
        return self.editors.recent_dictation(instance_name, n = n)

    def scratch_recent(self, instance_name, n = 1):
        """undo the effect of the most recent n utterances into the
        specified editor, if possible.

        **INPUTS**

        *STR instance_name* -- the editor 

        *INT n* -- number of utterances to undo

        **OUTPUTS**

        *INT* -- number of utterances actually undone
        """
        debug.trace('NewMediatorObject.scratch_recent', 'instance_name=%s, n=%s' % (instance_name, n))
        return self.editors.scratch_recent(instance_name, n = n)

    def reinterpret_recent(self, instance_name, changed):
        """undo the effect of one or more recent utterances, if
        possible, and reinterpret these utterances (and possibly any
        intervening utterances), making the appropriate changes to the
        editor buffers.

        **Note:** this method does not perform adaption of the changed
        utterances.  The caller should do that itself.

        **INPUTS**

        *[INT] changed* -- the utterance numbers of 
        those utterances which were corrected by the user

        **NOTE:** particular implementations of ResMgr may reinterpret 
        all utterances subsequent to the oldest changed utterance

        **OUTPUTS**

        *[INT]* -- the indices onto the stack of recent utterances 
        actually reinterpreted (including intervening ones), sorted 
        with the oldest first, or None if no utterances could be 
        reinterpreted
        """
        return self.editors.reinterpret_recent(instance_name, changed)
   
    def can_reinterpret(self, instance_name, n):
        """can we safely reinterpret the nth most recent utterance
        into the specified editor

        **INPUTS**

        *STR instance_name* -- the editor 

        *INT n* -- the depth in the editor state stack of the utterance
        to be reinterpreted

        **OUTPUTS**

        *BOOL* -- true if we can safely reinterpret that utterance
        """
        return self.editors.can_reinterpret(instance_name, n = n)

    def correct_utterance(self, instance_name, utterance_number):
        """initiate user correction of the utterance with a given
        utterance number into the given instance

        NOTE: this is a synchronous method which starts a modal
        correction box, and will not return until the user has 
        dismissed the correction box.  Generally, it should be called
        only in response to a CorrectUtterance event, rather than
        in direct response to a spoken correction command.

        **INPUTS**

        *STR instance_name* -- name of the application instance

        *INT utterance_number* -- the number assigned to the utterance by
        interpret_dictation

        **OUTPUTS**

        *none*
        """
        self.editors.correct_utterance(instance_name, utterance_number)

    def correct_recent(self, instance_name):
        """initiate user selection of a recent utterance to correct

        NOTE: this is a synchronous method which starts a modal
        correction box, and will not return until the user has 
        dismissed the correct recent dialog box.  Generally, it should 
        be called only in response to a CorrectRecent event, rather than
        in direct response to a spoken correction command.

        **INPUTS**

        *STR instance_name* -- name of the application instance

        **OUTPUTS**

        *none*
        """
        self.editors.correct_recent(instance_name)
    
    def user_message(self, message, instance = None):
        """displays a user message via the appropriate channel
        (e.g. stdout, or a MediatorConsole status line, or an 
        editor-specific status line if supported.

        **INPUTS**

        *STR message* -- the message

        *STR instance_name* -- the editor from which the message
        originated, or None if it is not associated with a specific
        editor.

        **OUTPUTS**

        *none*
        """
        if self.the_console:
            sent = self.the_console.user_message(message, 
                instance = instance)
            if sent and not self.testing:
                return
        print message

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
