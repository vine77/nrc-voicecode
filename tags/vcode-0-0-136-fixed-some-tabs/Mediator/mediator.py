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

"""Usage: python mediator.py -hs

Main script for VoiceCode mediator.

OPTIONS
-------

-h  : print this help message.

-s  : run mediator in simulation mode

-t  : run mediator in timed (profiled) simulation mode

-p  : port number for communication with external programming environment


Console mode
------------

When used with '-s' option, the script runs in simulation mode. It
asks for commands and executes those using an editor simulator.

After each command, the content of the current buffer is printed. The
position of the cursor is indicated by a mark *<CURSOR>*.

For valid commands, see sim_commands.py

To quit, use:

quit()
   Quit the simulator.

   Note that if you don't quit using this command
   (e.g. *Ctrl-C*), your DOS window will hang up.   
"""

import natlink
import os, profile, re, string, sys
import traceback
import vc_globals

# we need the module object, so we must import the whole module
import sim_commands

# but test suite assumes that the commands are defined here, so we need
# this too.
from sim_commands import *

sys.path = sys.path + [vc_globals.config, vc_globals.admin]

import CmdInterp, EdSim, MediatorObject, sr_interface, util, vc_globals
from CSCmd import CSCmd

# for actions that span different languages
from cont_gen import ContC, ContPy
from actions_gen import *

# for C support
from actions_C_Cpp import *

# for Python support
from actions_py import *

the_mediator = None


def cleanup(clean_sr_voc=0, save_speech_files = None, disconnect = 1):
    global the_mediator

    sim_commands.quit(clean_sr_voc=clean_sr_voc)
    print the_mediator
    if the_mediator:
        the_mediator.quit(clean_sr_voc=clean_sr_voc, 
	    save_speech_files=save_speech_files, disconnect=disconnect)

def new_cleanup(the_mediator, clean_sr_voc=0, save_speech_files = None, 
	disconnect = 1):
    the_mediator.quit(clean_sr_voc=clean_sr_voc, 
	save_speech_files=save_speech_files, disconnect=disconnect)

def new_simulator(symdict_pickle_fname=None,
		   disable_dlg_select_symbol_matches = None,
		   window = 0, exclusive = 0,
		   allResults = 0,
		   on_app = None, owns_app = 1,
		   mic_change = None,
		   owner = None, id = None
		  ):

    """
    Creates, configures, and returns a local [MediatorObject] instance 

    **NOTE:** Unlike init_simulator, this function cannot be used to quit,
    re-create and reconfigure an existing mediator

    **INPUTS**

    STR *symdict_pickle_fname=None* -- Name of the file containing the
    persistent version of the symbols dictionnary.
    
    BOOL *disable_dlg_select_symbol_matches = None* -- If *true*,
    disable the dialog for confirming new symbol matches with the
    user.
    
    STR *window=None* -- Window handle of application associated with
    the mediator. The mediator listens only when this window is
    active. If *window=None*, then mediator is not associated with a
    particular window and it will always listen for utterances.
    
    BOOL *exclusive=0* -- See [MediatorObject.exclusive] for details.
    
    BOOL *allResults=0* -- See [MediatorObject.allResults] for details.

    [AppState] *on_app=None* -- [AppState] instance to use for the
    mediator. If *None*, then use a new [EdSim] instance.

    [AppState] *on_app* -- Attach this [AppState] to the meditor
    instead of generating a new one from scratch (useful when
    regression testing using an external editor instead of EdSim).

    *BOOL owns_app* -- create mediator with owns_app flag (see
    MediatorObject)

    *FCT* mic_change_callback -- mic_change_callback(*STR* mic_state)
    (optional) function to be called when the microphone state changes.

    *ServerMainThread owner* -- server which owns this mediator, or
    None.  Note: if owner is set, the id field MUST be provided.

    STR *id* -- The unique identifier assigned by the server to
    this MediatorObject
    
    **OUTPUT**

    *none*

    ..[AppState] file:///./AppState.AppState.html
    ..[EdSim] file:///./EdSim.EdSim.html
    ..[MediatorObject] file:///./MediatorObject.MediatorObject.html
    ..[MediatorObject.allResults] file:///./MediatorObject.MediatorObject.html
    ..[MediatorObject.exclusive] file:///./MediatorObject.MediatorObject.html
    """

    if on_app == None:
        on_app = EdSim.EdSim()
    
    try:
	sr_interface.connect('off', mic_change_callback = mic_change)
    except natlink.UnknownName:
        print 'SR user \'%s\' not defined. \nDefine it and restart VoiceCode' % sr_interface.vc_user_name
	sr_interface.disconnect()
	return None
#        cleanup()        
        
    if sr_interface.speech_able:
#   new_simulator doesn't have a pre-existing mediator (it is not used
#   for re-initialization, so init_simulator_regression cannot call
#   new_simulator the way it calls init_simulator)
#        if symdict_pickle_fname == None and the_mediator != None:
            #
            # Remove symbols from NatSpeak's dictionary 
            #
#            the_mediator.interp.cleanup(resave=0)

#   new_simulator doesn't have a pre-existing mediator (it is not used
#   for re-initialization, so init_simulator_regression cannot call
#   new_simulator the way it calls init_simulator)
#        if the_mediator:
#            the_mediator.quit(save_speech_files=0, disconnect=0)            
        
	interp = \
	    CmdInterp.CmdInterp(symdict_pickle_filename = symdict_pickle_fname, 
		disable_dlg_select_symbol_matches = \
		    disable_dlg_select_symbol_matches)
        the_mediator = MediatorObject.MediatorObject(app = on_app,
	    interp = interp,
	    window = window, 
	    owns_app = owns_app,
	    exclusive = exclusive, 
	    allResults = allResults, 
	    owner = owner,
	    id = id)

        #
        # Read the symbol dictionary from file
        #
# DCF: this is now done automatically by passing the pickle filename to
# the CmdInterp constructor
#        the_mediator.interp.known_symbols.pickle_fname = symdict_pickle_fname
#        the_mediator.interp.known_symbols.init_from_file()

        #
        # Configure the mediator
        #
        the_mediator.configure()
	return the_mediator

    return None


    #
    # Possibly disable the symbol selection dialog
    #
# DCF: this is now done by passing the argument to the CmdInterp
# constructor
#    the_mediator.interp.disable_dlg_select_symbol_matches = disable_dlg_select_symbol_matches

    # define global variables accessible to the simulator commands
    # through the sim_commands module namespace

#    sim_commands.the_mediator = the_mediator
#    print sim_commands.the_mediator

    # define some useful local variables
# if you want this stuff, you'll have to do it elsewhere
#    home = os.environ['VCODE_HOME']
#    sim_commands.command_space['home'] = home
#    sim_commands.command_space['testdata'] = \
#        os.path.join(home, 'Data', 'TestData')


def init_simulator(symdict_pickle_fname=None,
		   disable_dlg_select_symbol_matches = None,
		   window = 0, exclusive = 0,
		   allResults = 0,
		   on_app = None, owns_app = 1,
		   mic_change = None,
		   owner = None, id = None
		  ):

    """
    Creates a global [MediatorObject] instance *the_mediator*, and configures it.

    **INPUTS**

    STR *symdict_pickle_fname=None* -- Name of the file containing the
    persistent version of the symbols dictionnary.
    
    BOOL *disable_dlg_select_symbol_matches = None* -- If *true*,
    disable the dialog for confirming new symbol matches with the
    user.
    
    STR *window=None* -- Window handle of application associated with
    the mediator. The mediator listens only when this window is
    active. If *window=None*, then mediator is not associated with a
    particular window and it will always listen for utterances.
    
    BOOL *exclusive=0* -- See [MediatorObject.exclusive] for details.
    
    BOOL *allResults=0* -- See [MediatorObject.allResults] for details.

    [AppState] *on_app=None* -- [AppState] instance to use for the
    mediator. If *None*, then use a new [EdSim] instance.

    [AppState] *on_app* -- Attach this [AppState] to the meditor
    instead of generating a new one from scratch (useful when
    regression testing using an external editor instead of EdSim).

    *BOOL owns_app* -- create mediator with owns_app flag (see
    MediatorObject)

    *FCT* mic_change_callback -- mic_change_callback(*STR* mic_state)
    (optional) function to be called when the microphone state changes.

    *ServerMainThread owner* -- server which owns this mediator, or
    None.  Note: if owner is set, the id field MUST be provided.

    STR *id* -- The unique identifier assigned by the server to
    this MediatorObject
    
    **OUTPUT**

    *none*

    ..[AppState] file:///./AppState.AppState.html
    ..[EdSim] file:///./EdSim.EdSim.html
    ..[MediatorObject] file:///./MediatorObject.MediatorObject.html
    ..[MediatorObject.allResults] file:///./MediatorObject.MediatorObject.html
    ..[MediatorObject.exclusive] file:///./MediatorObject.MediatorObject.html
    """

#    print '-- mediator.init_simulator: window=%s, exclusive=%s, allResults=%s, reuse_mediator=%s' % (window, exclusive, allResults, reuse_mediator)
    
    global the_mediator

    if on_app == None:
        on_app = EdSim.EdSim()
    
    try:
	sr_interface.connect('off', mic_change_callback = mic_change)
    except natlink.UnknownName:
        print 'SR user \'%s\' not defined. \nDefine it and restart VoiceCode' % sr_interface.vc_user_name
        cleanup()        
        
    if sr_interface.speech_able:
        if symdict_pickle_fname == None and the_mediator != None:
            #
            # Remove symbols from NatSpeak's dictionary 
            #
            the_mediator.interp.cleanup(resave=0)

        #
        # It could be that the_mediator has previously been initiated (e.g. if
        # we are running multiple regression tests). If so, must unload the
        # SR grammars otherwise they will continue to exist and to recognise
        # utterances.
        #
        if the_mediator:
            the_mediator.quit(save_speech_files=0, disconnect=0)            
        
	interp = \
	    CmdInterp.CmdInterp(symdict_pickle_filename = symdict_pickle_fname, 
		disable_dlg_select_symbol_matches = \
		    disable_dlg_select_symbol_matches)
        the_mediator = MediatorObject.MediatorObject(app = on_app,
	    interp = interp,
	    window = window, 
	    owns_app = owns_app,
	    exclusive = exclusive, 
	    allResults = allResults, 
	    owner = owner,
	    id = id)

        #
        # Read the symbol dictionary from file
        #
# DCF: this is now done automatically by passing the pickle filename to
# the CmdInterp constructor
#        the_mediator.interp.known_symbols.pickle_fname = symdict_pickle_fname
#        the_mediator.interp.known_symbols.init_from_file()

        #
        # Configure the mediator
        #
        the_mediator.configure()

    #
    # Possibly disable the symbol selection dialog
    #
# DCF: this is now done by passing the argument to the CmdInterp
# constructor
#    the_mediator.interp.disable_dlg_select_symbol_matches = disable_dlg_select_symbol_matches

    # define global variables accessible to the simulator commands
    # through the sim_commands module namespace

    sim_commands.the_mediator = the_mediator
#    print sim_commands.the_mediator

    # define some useful local variables
    home = os.environ['VCODE_HOME']
    sim_commands.command_space['home'] = home
    sim_commands.command_space['testdata'] = \
        os.path.join(home, 'Data', 'TestData')

def init_simulator_regression(symdict_pickle_fname=None, disable_dlg_select_symbol_matches = None, on_app=None):
    
    """Initialises the simulator using a global exclusive grammar so that
    the user can continue to work in other applications using the keyboard
    while the regression test is running.

    Also, if there already exists a mediator, we reuse its [AppState], in
    case this was an [AppState] connected to an external editor (don't want to
    have the external editor reconnect after each test).

    **INPUTS**

    [AppState] *on_app* -- [AppState] to use for the regression
    tests. If *None* and there already exists a simulator, reuse the
    [AppState] from that simulator.
    
    ..[AppState] file:///./AppState.AppState.html"""

#    print '-- mediator.init_simulator_regression: on_app=%s' % on_app


    
    if the_mediator and on_app == None:
        on_app = the_mediator.app
    #
    # Make sure to reinitialise the external editor.
    #
    if on_app:
        on_app.init_for_test()


    
    init_simulator(on_app=on_app, symdict_pickle_fname=symdict_pickle_fname,
                   window=0, owns_app = 0, exclusive=1, allResults=0, 
                   disable_dlg_select_symbol_matches=disable_dlg_select_symbol_matches)
		   

    the_mediator.app.print_buff_when_changed = 1
    

def execute_command(cmd):
#    print '-- mediator.execute_command: cmd=%s' % cmd
    try:
	exec cmd in sim_commands.__dict__, sim_commands.command_space
	#	  exec command in sim_commands and command_space
    except Exception, err:
        traceback.print_exc()

        
def simulator_mode(options):
    """Start mediator in console mode.

    Useful for debugging purposes when using the mediator separately from
    an external editor.

    **INPUTS**

    *[STR: ANY] options* -- Dictionary of options for the script.


    **OUTPUTS**

    *none* -- 
    """

    global the_mediator

#
# Handle of the DOS window in which mediator is running
#
# print natlink.getCurrentModule()

    sr_interface.set_mic('off')

    console_win_handle = natlink.getCurrentModule()[2]

    init_simulator(window = console_win_handle, symdict_pickle_fname = vc_globals.state + os.sep + 'symdict.pkl', disable_dlg_select_symbol_matches = 1)
    
    #
    # For better error reporting, you can type some instructions here
    # instead of typing them at the console. The fact that the console
    # commands are eval'ed means the error reporting isn't great
    #
    # e.g. compile_symbols(['D:/Temp/blah.py'])
    #
    
    if options['e']:
	sys.stderr = sys.stdout
    try:
	while (not sim_commands.quit_flag):
	    sys.stdout.write('Command> ')
	    cmd = sys.stdin.readline()
	    execute_command(cmd)                
    finally:
	if options['e']:
	    sys.stderr = sys.__stderr__

def new_execute_command(cmd, names):
#    print '-- mediator.execute_command: cmd=%s' % cmd
    try:
	exec cmd in names
	#	  exec command in sim_commands and command_space
    except Exception, err:
        traceback.print_exc()

def new_simulator_mode(options):
    """Start mediator in console mode.

    Useful for debugging purposes when using the mediator separately from
    an external editor.

    **INPUTS**

    *[STR: ANY] options* -- Dictionary of options for the script.


    **OUTPUTS**

    *none* -- 
    """

#
# Handle of the DOS window in which mediator is running
#
# print natlink.getCurrentModule()

    sr_interface.set_mic('off')

    console_win_handle = natlink.getCurrentModule()[2]

    names = {}
    names['quit_flag'] = 0
# stuff from mediator.init_simulator (must be defined here now that we are using
# mediator.new_simulator
    home = os.environ['VCODE_HOME']
    names['home'] = home
    names['testdata'] = os.path.join(home, 'Data', 'TestData')

    the_mediator = new_simulator(window = console_win_handle,
	symdict_pickle_fname = vc_globals.state + os.sep + 'symdict.pkl', 
	disable_dlg_select_symbol_matches = 1) 

    commands = sim_commands.SimCmdsObj(the_mediator.app, 
	the_mediator.interp, names)
# add bound methods of the commands SimCmdsObj instance, corresponding
# to the functions in the sim_commands module, to this 
# namespace 
#    print actual_names
    commands.bind_methods(names)
#    print actual_names



    if options['e']:
	sys.stderr = sys.stdout
    try:
	while (not names['quit_flag']):
	    sys.stdout.write('Command> ')
	    cmd = sys.stdin.readline()
	    new_execute_command(cmd, names)                
    finally:
	new_cleanup(the_mediator, commands.clean_sr_voc, 
	    commands.save_speech_files, commands.disconnect_flag)
	if options['e']:
	    sys.stderr = sys.__stderr__

def run(options):
    """run simulator from within a Python shell
    
    **INPUTS**

    *[STR: ANY] options* -- Dictionary of options for the script.


    **OUTPUTS**

    *none* -- 
    """
# default parameters for cleanup
    sim_commands.__dict__['clean_sr_voc_flag']=0
    sim_commands.__dict__['save_speech_files_flag']=None
    sim_commands.__dict__['disconnect_flag']=1
 
    if opts['h']:
        print __doc__
	print sim_commands.__doc__
	return

    if opts['t']:
        #
        # Run mediator using an editor simulator, in profiling mode
        #
        profile.run("""
new_simulator_mode(opts)""")
    elif opts['s']:
        #
        # Run mediator using an editor simulator
        #
        new_simulator_mode(opts)
#        simulator_mode(opts)

#    cleanup(sim_commands.clean_sr_voc_flag, 
#	sim_commands.save_speech_files_flag, sim_commands.disconnect_flag)
        
if (__name__ == '__main__'):
    
    opts, args = util.gopt(['h', None, 's', None, 'p', 50007, 't', None, 'e', None])
    
#    print '-- mediator.__main__: opts=%s' % opts

    run(opts)
