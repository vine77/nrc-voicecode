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

def cleanup(clean_sr_voc=0):
    global the_mediator

    sim_commands.quit(clean_sr_voc=clean_sr_voc)

def setmic(state):
    if sr_interface.speech_able():
        sr_interface.connect()
        natlink.setMicState(state)

def init_simulator(symdict_pickle_fname=None):
    global the_mediator

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
            the_mediator.interp.known_symbols.cleanup(resave=0)

        #
        # It could be that the_mediator has previously been initiated (e.g. if
        # we are running multiple regression tests). If so, must unload the
        # SR grammars otherwise they will continue to exist and to recognise
        # utterances.
        #
        if the_mediator:
            the_mediator.quit(save_speech_files=0, disconnect=0)            
            
            
        the_mediator = MediatorObject.MediatorObject(interp=CmdInterp.CmdInterp(on_app=EdSim.EdSim()))

        #
        # Read the symbol dictionary from file
        #
        the_mediator.interp.known_symbols.pickle_fname = symdict_pickle_fname
        the_mediator.interp.known_symbols.init_from_file()

        #
        # Configure the mediator
        #
        the_mediator.configure()

    # define global variables accessible to the simulator commands
    # through the sim_commands module namespace

    sim_commands.the_mediator = the_mediator

    # define some useful local variables
    home = os.environ['VCODE_HOME']
    sim_commands.command_space['home'] = home
    sim_commands.command_space['testdata'] = \
        os.path.join(home, 'Data', 'TestData')

def execute_command(cmd):
#    print '-- mediator.execute_command: cmd=%s' % cmd
    try:
	exec cmd in sim_commands.__dict__, sim_commands.command_space
	#	  exec command in sim_commands and command_space
    except Exception, err:
	traceback.print_exc()
#    else:
#        if the_mediator.interp.on_app.curr_buffer:
#            the_mediator.interp.on_app.curr_buffer.print_buff()

        
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
    init_simulator(symdict_pickle_fname = vc_globals.state + os.sep + 'symdict.pkl')
    
    #
    # For better error reporting, you can type some instructions here
    # instead of typing them at the console. The fact that the console
    # commands are eval'ed means the error reporting isn't great
    #
    # e.g. compile_symbols(['D:/Temp/blah.py'])
    #
#    compile_symbols(['D:/VoiceCode/VCode.testing/Data/TestDatat/native_python.py'])
#    open_file('D:/blah.py')


    while (not sim_commands.quit_flag):
        sys.stdout.write('Command> ')
        cmd = sys.stdin.readline()
        execute_command(cmd)                
        
if (__name__ == '__main__'):
    
    opts, args = util.gopt(['h', None, 's', None, 'p', 50007, 't', None])
    
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
        