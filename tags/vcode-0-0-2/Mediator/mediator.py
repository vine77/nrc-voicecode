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

open_file(STR fname)
   Opens file with path name *fname* in the editor
   simulator. It also compiles a list of symbols for that file.

compile_symbols([STR] file_list)
   Compiles symbols for all source files in list *file_list*.

clear_symbols()
   Removes all spoken forms of symbols added by VoiceCode to NatSpeak's 
   vocabulary. Spoken forms which consist of a single word are however left
   there.

say(STR utterance)
   Interprets string *utterance* as though it had been said by a user.

   When called in this way, the system will simulate a recognition
   event using NatLink's <EM>recognitionMimic</EM> function.

say(STR utterance, bypass_NatLink=1)
   Same as above, except that the interpretation process will bypass
   NatLink's <EM>recognitionMimic</EM> function.

goto(INT pos)
   Moves cursor to position *pos*

goto_line(INT linenum)
   Moves cursor to the beginning of line number *linenum*

show_buff()
   Prints the content of the current buffer

listen()
   Throws the mediator into a dictation loop. It will listen for
   dictation utterances and interpret and execute any part of the
   utterance that corresponds to a Context Sensitive Command.

   Once in 'listen' mode, you cannot type console commands until you
   have clicked the 'OK' button on the 'Natlink/ Python Subsystem'
   window.

unresolved_abbreviations()
   Prints out a list of the unresolved abbreviations in symbols that were
   parsed so far. An unresolved abbreviation is an abbreviation that appeared
   in a symbol and is neither a speech vocabulary word nor a known
   abbreviation.

   The unresolved abbreviations are printed in increasing order of length, 
   to make it easier to spot the ones that are actually abbreviations (they
   will tend to be short and appear at the beginning).

quit()
   Quit the simulator.

   Note that if you don't quit using this command
   (e.g. *Ctrl-C*), your DOS window will hang up.   
"""

import util

import natlink
import os, sys
import util, vc_globals
from CSCmd import CSCmd
import config


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

def open_file(fname):
    """Open a file with name in current buffer.

    *STR fname* is the path of the file"""

    config.interp.app.open_file(fname)
    print '-- mediator: config.interp.known_symbols=%s' % config.interp.known_symbols
    config.interp.known_symbols.parse_symbols(fname)
    show_buff()

def compile_symbols(file_list):
    for a_file in file_list:
        print 'Compiling symbols for file \'%s\'' % a_file
        config.interp.known_symbols.parse_symbols(a_file)
    print '>>> Known symbols are: '; config.interp.known_symbols.print_symbols()
    
def say(utterance, bypass_NatLink=0):
    """Simulate an utterance *STR utterance*

    IF *BOOL bypass_NatLink* is true, the interpretation will be done withouth
    going through NatLink's recognitionMimic function.
    """

    if bypass_NatLink or os.environ.has_key('VCODE_NOSPEECH'):
        config.interp.interpret_NL_cmd(utterance)
    else:
        natlink.recognitionMimic(utterance)
    show_buff()

def goto(pos):
    """Goes to position *INT pos* of the current buffer"""

    config.interp.app.goto(pos)
    show_buff()

def goto_line(linenum):
    """Goes to line number *INT linenum* of current source buffer"""
    config.interp.app.goto_line(linenum)
    show_buff()

def show_buff():
    """Shows content of current source buffer"""
    config.interp.app.print_buff_content()

def move(steps):
    """Moves cursor by *INT steps* (can be negative)"""
    pos = config.interp.app.curr_buffer.cur_pos
    config.interp.app.goto(pos + steps)
    show_buff()


def setmic(state):
    if not os.environ.has_key('VCODE_NOSPEECH'):
        natlink.setMicState(state)


def listen():
    if not os.environ.has_key('VCODE_NOSPEECH'):
        natlink.setMicState('on')
        natlink.waitForSpeech(0)

def unresolved_abbreviations():
    print 'List of unresolved abbreviations\n'
    sorted_unresolved = config.interp.known_symbols.unresolved_abbreviations.keys()
    sorted_unresolved.sort(lambda x, y: len(x) > len(y) or (len(x) == len(y) and x < y))
    for an_abbreviation in sorted_unresolved:
        symbol_list = config.interp.known_symbols.unresolved_abbreviations[an_abbreviation].keys()
        print '\'%s\': appears in %s' % (an_abbreviation, str(symbol_list))


def clear_symbols():
    #
    # Remove symbols from the Speech Recognition vocabulary
    #
    config.interp.known_symbols.vocabulary_cleanup()
    
def quit():
    global quit_flag
    quit_flag = 1
    
    if not config.interp.dictation_object == None and \
       not os.environ.has_key('VCODE_NOSPEECH'):
        config.interp.terminate()
        natlink.natDisconnect()


if (__name__ == '__main__'):

    opts, args = util.gopt(['h', None, 's', None])

#
# For better error reporting, you can type some instructions here instead
# of typing them at the console.
# The fact that the console commands are eval'ed means the error reporting
# isn't great
#
#    compile_symbols(['D:/Temp/blah.py'])
#    compile_symbols(['Actions_C.py', 'AppState.py', 'CSCmd.py', 'CmdInterp.py', 'Context.py', 'EdSim.py', 'LangDef.py', 'Object.py', 'SelfHandlingExc.py', 'SourceBuff.py', 'SymDict.py', 'VoiceDictation.py', 'actions_C_Cpp.py', 'actions_gen.py', 'actions_py.py', 'config.py', 'cont_gen.py', 'debug.py', 'mediator.py', 'safe_setattr.py', 'util.py', 'vc_globals.py'])
#    compile_symbols(['D:/VoiceCode/VCode/Data/TestData/large_buff.py'])
#    open_file('D:/blah.py')
#    say('for a base in')
#    unresolved_abbreviations()
#    clear_symbols()
#    say('horizontal position = 0', bypass_NatLink=1)
#      say('witharguments', bypass_NatLink=1)
#    unresolved_abbreviations()
#    clear_symbols()
#    quit()

    if opts['h']:
        print __doc__
    elif opts['s']:
        
        #
        # Start in console mode with editor simulator.
        # NOTE: We only activate NatLink if -b option was not set
        #
        if not os.environ.has_key('VCODE_NOSPEECH'):
            config.interp.activate(0)
            
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
        
