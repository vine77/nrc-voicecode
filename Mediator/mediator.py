"""Usage: python mediator.py -hs

Main script for VoiceCode mediator.

OPTIONS
-------

-h   : print this help message.

-s   : run mediator in simulation mode


Console mode
------------

When used with '-s' option, the script runs in simulation mode. It
asks for commands and executes those using an editor simulator.

After each command, the content of the current buffer is printed. The
position of the cursor is indicated by a mark *<CURSOR>*.

Valid commands are:

openfile(STR fname)
   Opens file with path name *fname* in the editor simulator

say(STR utterance)
   Interprets string *utterance* as though it had been said by a user.

   When called in this way, the system will simulate a recognition
   event using NatLink's <EM>recognitionMimic</EM> function.

say(STR utterance, bypass_NatLink=1)
   Same as above, except that the interpretation process will bypass
   NatLink's <EM>recognitionMimic</EM> function.

goto(INT pos)
   Moves cursor to position *pos*

gotoline(INT linenum)
   Moves cursor to the beginning of line number *linenum*

showbuff()
   Prints the content of the current buffer

listen()
   Throws the mediator into a dictation loop. It will listen for
   dictation utterances and interpret and execute any part of the
   utterance that corresponds to a Context Sensitive Command.

   Once in 'listen' mode, you cannot type console commands until you
   have clicked the 'OK' button on the 'Natlink/ Python Subsystem'
   window.

quit()
   Quit the simulator.

   Note that if you don't quit using this command
   (e.g. <EM>Ctrl-C</EM>), your DOS window will hang up.   
"""

import util

import natlink
import os, sys
import util, vc_globals
from CSCmd import CSCmd
from config import add_csc


# for actions that span different languages
from cont_gen import ContC, ContPy
from actions_gen import *

# for C support
from actions_C_Cpp import *

# for Python support
from actions_py import *

#
# Configure the system
#
config_file = vc_globals.config + os.sep + 'vc_config.py'
try:
    execfile(config_file)
except Exception, err:
    print 'ERROR: in configuration file %s.\n' % config_file
    raise err

quit_flag = 0

def openfile(fname):
    """Open a file with name in current buffer.

    *STR fname* is the path of the file"""

    vc_globals.interp.app.open_file(fname)
    showbuff()

def say(utterance, bypass_NatLink=0):
    """Simulate an utterance *STR utterance*

    IF *BOOL bypass_NatLink* is true, the interpretation will be done withouth
    going through NatLink's recognitionMimic function.
    """

    if bypass_NatLink or os.environ.has_key('VCODE_NOSPEECH'):
        vc_globals.interp.interpret_NL_cmd(utterance)
    else:
        natlink.recognitionMimic(utterance)
    showbuff()

def goto(pos):
    """Goes to position *INT pos* of the current buffer"""

    vc_globals.interp.app.goto(pos)
    showbuff()

def gotoline(linenum):
    """Goes to line number *INT linenum* of current source buffer"""
    vc_globals.interp.app.goto_line(linenum)
    showbuff()

def showbuff():
    """Shows content of current source buffer"""
    vc_globals.interp.app.print_buff_content()

def move(steps):
    """Moves cursor by *INT steps* (can be negative)"""
    pos = vc_globals.interp.app.curr_buffer.cur_pos
    vc_globals.interp.app.goto(pos + steps)
    showbuff()


def setmic(state):
    if not os.environ.has_key('VCODE_NOSPEECH'):
        natlink.setMicState(state)


def listen():
    if not os.environ.has_key('VCODE_NOSPEECH'):
        natlink.setMicState('on')
        natlink.waitForSpeech(0)
        
def quit():
    global quit_flag
    quit_flag = 1
    if not vc_globals.interp.dictation_object == None and \
       not os.environ.has_key('VCODE_NOSPEECH'):
        vc_globals.interp.terminate()
        natlink.natDisconnect()

if (__name__ == '__main__'):

    opts, args = util.gopt(['h', None, 's', None])

    if opts['h']:
        print __doc__
    elif opts['s']:
        
        #
        # Start in console mode with editor simulator.
        # NOTE: We only activate NatLink if -b option was not set
        #
        if not os.environ.has_key('VCODE_NOSPEECH'):
            vc_globals.interp.activate(0)
            
        while (not quit_flag):
            sys.stdout.write('Command> ')
            cmd = sys.stdin.readline()
            try:
                exec(cmd)
            except Exception, err:
                print 'Error executing command.\n'
                print '   Error type: %s' % err
                print '   Error data: %s' % err.__dict__

quit()
        
