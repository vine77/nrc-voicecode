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

"""Usage: python gui_sim.py -h
            or
	  python gui_sim.py [-s | -t]

Main script for VoiceCode mediator.

OPTIONS
-------

-h  : print this help message.

-s  : run mediator in simulation mode

-t  : run mediator in timed (profiled) simulation mode


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
import mediator

# we need the module object, so we must import the whole module
import sim_commands

# but test suite assumes that the commands are defined here, so we need
# this too.
# test suite doesn't run from gui_sim, so we don't need this here
# from sim_commands import *


sys.path = sys.path + [vc_globals.config, vc_globals.admin]

import CmdInterp, MediatorObject, sr_interface, util, vc_globals
import AppStateGenEdit
import WaxEdSim
from CSCmd import CSCmd

# for actions that span different languages
from cont_gen import ContC, ContPy
from actions_gen import *

# for C support
from actions_C_Cpp import *

# for Python support
from actions_py import *

the_mediator = None


def cleanup(the_mediator, clean_sr_voc=0, save_speech_files = None, 
    disconnect = 1):

#    sim_commands.quit(clean_sr_voc=clean_sr_voc)
#    if sim_commands.the_mediator:
#        sim_commands.the_mediator.quit(clean_sr_voc=clean_sr_voc, 
#	    save_speech_files=save_speech_files, disconnect=disconnect)
    the_mediator.quit(clean_sr_voc=clean_sr_voc, 
	save_speech_files=save_speech_files, disconnect=disconnect)

def simulator_mode(options):
    """Start mediator in console mode.

    Useful for debugging purposes when using the mediator separately from
    an external editor.

    **INPUTS**

    *[STR: ANY] options* -- Dictionary of options for the script.

    **OUTPUTS**

    *none* -- 
    """


#    sim_commands.setmic('off')
    sr_interface.set_mic('off')

    names = {}
# stuff from mediator.init_simulator (must be defined here now that we are using
# mediator.new_simulator
    home = os.environ['VCODE_HOME']
    names['home'] = home
    names['testdata'] = os.path.join(home, 'Data', 'TestData')

# need this early, before SimCmdsObj has a chance to add it
#    names['getmic'] = sim_commands.getmic
    names['getmic'] = sr_interface.get_mic

    editor_app = WaxEdSim.WaxEdSim(command_space= names)
    module_info = natlink.getCurrentModule()
    window = module_info[2]
    print module_info
    app = editor_app.editor
    editor_app.got_window()

    the_mediator = mediator.new_simulator(on_app = app, owns_app = 0,
	symdict_pickle_fname = vc_globals.state + os.sep + 'symdict.pkl', 
#	symdict_pickle_fname = None,
	disable_dlg_select_symbol_matches = 1, window = window,
	mic_change = editor_app.mic_change)
        

# get actual namespace used by panel (which is a copy of the names we
# passed to WaxEdSim)
    actual_names = editor_app.access_command_space()

    commands = sim_commands.SimCmdsObj(app, the_mediator.interp, actual_names)
# add bound methods of the commands SimCmdsObj instance, corresponding
# to the functions in the sim_commands module, to this 
# namespace 
#    print actual_names
    commands.bind_methods(actual_names)
#    print actual_names



    #
    # For better error reporting, you can type some instructions here
    # instead of typing them at the console. The fact that the console
    # commands are eval'ed means the error reporting isn't great
    #
    # e.g. compile_symbols(['D:/Temp/blah.py'])
    #
    file_name = vc_globals.test_data + os.sep + 'large_buff.py'
    commands.open_file(file_name)
    

    editor_app.run()

    print 'gui exited'
    cleanup(the_mediator, commands.clean_sr_voc, 
	commands.save_speech_files, commands.disconnect_flag)
        
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
    else:
#    elif opts['s']:
        #
        # Run mediator using an editor simulator
        #
        simulator_mode(opts)
