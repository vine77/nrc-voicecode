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

#
# Handle of the DOS window in which mediator is running
#
sr_interface.connect()
console_win_handle = natlink.getCurrentModule()[2]

def cleanup(clean_sr_voc=0):
    global the_mediator, console_win_handle

    sim_commands.quit(clean_sr_voc=clean_sr_voc)


def init_simulator(symdict_pickle_fname=None,
                   disable_dlg_select_symbol_matches = None,
                   window=None, exclusive=0, allResults=0,
                   reuse_mediator=0, on_app=None):

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
    active. If *window=0*, then mediator is not associated with a
    particular window and it will always listen for utterances.
    
    BOOL *exclusive=0* -- See [MediatorObject.exclusive] for details.
    
    BOOL *allResults=0* -- See [MediatorObject.allResults] for details.

    [AppState] *on_app=None* -- [AppState] instance to use for the
    mediator. If *None*, then use a new [EdSim] instance.

    BOOL *reuse_mediator* -- If *true*, then reuse the existing
    mediator (if any), instead of creating one from scratch (useful
    when regression testing using an external editor instead of EdSim).

    [AppState] *on_app* -- Attach this [AppState] to the meditor
    instead of generating a new one from scratch (useful when
    regression testing using an external editor instead of EdSim).

    
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
    
    if window == None:
        window = console_win_handle

    try:
        sr_interface.connect('off')
    except natlink.UnknownName:
        print 'SR user \'%s\' not defined. \nDefine it and restart VoiceCode' % sr_interface.vc_user_name
        cleanup()        
        
    if sr_interface.speech_able:
        if symdict_pickle_fname == None and the_mediator != None:
            #
            # Remove symbols from NatSpeak's dictionary 
            #
            pass
            the_mediator.interp.known_symbols.cleanup(resave=0)

        #
        # It could be that the_mediator has previously been initiated (e.g. if
        # we are running multiple regression tests). If so, must unload the
        # SR grammars otherwise they will continue to exist and to recognise
        # utterances.
        #
        if the_mediator:
            the_mediator.quit(save_speech_files=0, disconnect=0)            
        
        the_mediator = MediatorObject.MediatorObject(interp=CmdInterp.CmdInterp(on_app=on_app), window=window, exclusive=exclusive, allResults=allResults)

        #
        # Read the symbol dictionary from file
        #
        the_mediator.interp.known_symbols.pickle_fname = symdict_pickle_fname
        the_mediator.interp.known_symbols.init_from_file()

        #
        # Configure the mediator
        #
        the_mediator.configure()

    #
    # Possibly disable the symbol selection dialog
    #
    the_mediator.interp.disable_dlg_select_symbol_matches = disable_dlg_select_symbol_matches

    # define global variables accessible to the simulator commands
    # through the sim_commands module namespace

    sim_commands.the_mediator = the_mediator

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
        on_app = the_mediator.interp.on_app
    
    init_simulator(on_app=on_app, symdict_pickle_fname=symdict_pickle_fname,
                   window=0, exclusive=1, allResults=0, reuse_mediator=1,
                   disable_dlg_select_symbol_matches=disable_dlg_select_symbol_matches)

    #
    # Make sure to reinitialise the external editor.
    #
    the_mediator.interp.on_app.init_for_test()
    

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

    setmic('off')
    init_simulator(symdict_pickle_fname = vc_globals.state + os.sep + 'symdict.pkl', disable_dlg_select_symbol_matches = 1)
    
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
        
if (__name__ == '__main__'):
    
    opts, args = util.gopt(['h', None, 's', None, 'p', 50007, 't', None, 'e', None])
    
#    print '-- mediator.__main__: opts=%s' % opts
    
    if opts['h']:
        print __doc__
	print sim_commands.__doc__

    elif opts['t']:
        #
        # Run mediator using an editor simulator, in profiling mode
        #
        profile.run("""
simulator_mode(opts)""")
    elif opts['s']:
        #
        # Run mediator using an editor simulator
        #
        simulator_mode(opts)

    cleanup()
        
