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

"""Usage: python gui_sim.py -hs

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

import CmdInterp, MediatorObject, sr_interface, util, vc_globals
import WaxEdit
import WaxEdSim
import AppStateWaxEdit
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
    global the_mediator, console_win_handle

    sim_commands.quit(clean_sr_voc=clean_sr_voc)
    if the_mediator:
        the_mediator.quit(clean_sr_voc=clean_sr_voc, 
	    save_speech_files=save_speech_files, disconnect=disconnect)

def init_simulator(app, symdict_pickle_fname=None, 
    disable_dlg_select_symbol_matches = None, window = 0, exclusive = 0,
    allResults = 0, editor_app = None):

#    print '-- mediator.init_simulator: disable_dlg_select_symbol_matches=%s' % disable_dlg_select_symbol_matches
    
    global the_mediator

    if editor_app:
	mic_change = editor_app.mic_change

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
            
            
        the_mediator = MediatorObject.MediatorObject(app = app, interp=CmdInterp.CmdInterp(), window = window, exclusive=exclusive, allResults=allResults)

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
    sim_commands.gui_sim = 1

    # define some useful local variables
    home = os.environ['VCODE_HOME']
    sim_commands.__dict__['home'] = home
    sim_commands.__dict__['testdata'] = \
        os.path.join(home, 'Data', 'TestData')

def execute_command(cmd):
#    print '-- mediator.execute_command: cmd=%s' % cmd
    try:
	exec cmd in sim_commands.__dict__, sim_commands.command_space
	#	  exec command in sim_commands and command_space
    except Exception, err:
	traceback.print_exc()
#    else:
#        if the_mediator.app.curr_buffer:
#            the_mediator.app.curr_buffer.print_buff()

        
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

    editor_app = WaxEdSim.WaxEdSim(command_space= sim_commands.__dict__)
    module_info = natlink.getCurrentModule()
    window = module_info[2]
    print module_info
    app = AppStateWaxEdit.AppStateWaxEdit(editor = editor_app)

    
    init_simulator(app = app, 
	symdict_pickle_fname = vc_globals.state + os.sep + 'symdict.pkl', 
	disable_dlg_select_symbol_matches = 1, window = window,
	editor_app = editor_app)
        
    #
    # For better error reporting, you can type some instructions here
    # instead of typing them at the console. The fact that the console
    # commands are eval'ed means the error reporting isn't great
    #
    # e.g. compile_symbols(['D:/Temp/blah.py'])
    #
    file_name = vc_globals.test_data + os.sep + 'large_buff.py'
    open_file(file_name)
    

    editor_app.run(app_control = app)
    print 'gui exited'
        
if (__name__ == '__main__'):
    
    opts, args = util.gopt(['h', None, 's', None, 'p', 50007, 't', None])
    
#    print '-- mediator.__main__: opts=%s' % opts
  
    sim_commands.__dict__['clean_sr_voc_flag']=0
    sim_commands.__dict__['save_speech_files_flag']=None
    sim_commands.__dict__['disconnect_flag']=1
  
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

    cleanup(sim_commands.clean_sr_voc_flag, 
	sim_commands.save_speech_files_flag, sim_commands.disconnect_flag)
