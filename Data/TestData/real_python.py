"""Usage: python mediator.py -hs

Main script for VoiceCode mediator.

OPTIONS
-------

-h  : print this help message.

-s  : run mediator in simulation mode

-p  : port number for communication with external programming environment


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

   Note that this command will not work with Select XYZ
   utterances. For those, you must use the say_select command
   described below.

say(STR utterance, bypass_NatLink=1)
   Same as above, except that the interpretation process will bypass
   NatLink's <EM>recognitionMimic</EM> function.

say_select([STR] utterrance)
   Simulates a Select XYZ utterance.

   Elements of list *utterance* are the individual NatSpeak vocabulary
   entries that make the utterance. For vocabulary entries of the form
   written\spoken form, you must specify both the written and spoken
   form of the entry.

   e.g. say_select(['Select', '!=\\not equal to'])

goto(INT pos)
   Moves cursor to position *pos*

goto_line(INT linenum)
   Moves cursor to the beginning of line number *linenum*

select(INT start, end)
   Selects from position *start* to position *end* in current buffer

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

import natlink
import os, re, string, sys
import CmdInterp, EdSim, MediatorObject, sr_interface, util, vc_globals
from CSCmd import CSCmd

# for actions that span different languages
from cont_gen import ContC, ContPy
from actions_gen import *

# for C support
from actions_C_Cpp import *

# for Python support
from actions_py import *

the_mediator = MediatorObject.MediatorObject()
quit_flag = 0

def open_file(fname):
    """Open a file with name in current buffer.

    *STR fname* is the path of the file"""

    global the_mediator
    the_mediator.interp.on_app.open_file(fname)
    the_mediator.interp.known_symbols.parse_symbols(fname)
    show_buff()

def compile_symbols(file_list):
    global the_mediator
    for a_file in file_list:
        print 'Compiling symbols for file \'%s\'' % a_file
        the_mediator.interp.known_symbols.parse_symbols(a_file)
    print '>>> Known symbols are: '; the_mediator.interp.known_symbols.print_symbols()

    
def say(utterance, user_input=None, bypass_NatLink=0):
    """Simulate an utterance *STR utterance*

    Note that this command will not work with *Select XYZ* utterances.
    For those, you must use the [say_select] command.
    
    *STR utterance* -- The utterance. Contrarily to [say_select]
     command, this is a string as opposed to a list of words. Also,
     only the spoken form of words or phrases is entered in that
     string.

    *STR user_input* -- A string that will be sent to the mediator console's
     standard input. Use in automated regression testing, if the *say*
     command requires user additional user input (e.g. confirmation of
     a symbol match).
    
    *BOOL bypass_NatLink* -- if true, the interpretation will be done
    withouth going through NatLink's recognitionMimic function.
        
    .. [say_select] file:///./mediator.html#say_select"""
    
    global the_mediator

    if user_input:
        #
        # Create temporary user input file
        #
        old_stdin = sys.stdin
        temp_file_name = vc_globals.tmp + os.sep + 'user_input.dat'
        temp_file = open(temp_file_name, 'w')
        temp_file.write(user_input)
        temp_file.close()
        temp_file = open(temp_file_name, 'r')
        sys.stdin = temp_file
        
        
    if bypass_NatLink or os.environ.has_key('VCODE_NOSPEECH'):
        the_mediator.interp.interpret_NL_cmd(utterance)
        show_buff()        
    else:
        words = re.split('\s+', utterance)
#        print '-- mediator.say: words=%s' % repr(words)
        natlink.recognitionMimic(words)

    #
    # Redirect stdin back to what it was
    #
    if user_input:
        sys.stdin = old_stdin
        temp_file.close()

def say_select(utterance):
    """Simulate a *Select XYZ* utterance


    Elements of list *utterance* are the individual NatSpeak vocabulary
    entries that make the utterance. For vocabulary entries of the form
    written\spoken form, you must specify both the written and spoken
    form of the entry.
    
    e.g. say_select(['Select', '!=\\not equal to'])    
    """
    
    global the_mediator
    utterance[0] = string.capitalize(utterance[0])
#    print '-- mediator.say_select: utterance = %s' % repr(utterance)
    natlink.recognitionMimic(utterance)


def goto(pos):
    """Goes to position *INT pos* of the current buffer"""
    global the_mediator
    the_mediator.interp.on_app.goto(pos)
    show_buff()

def goto_line(linenum):
    """Goes to line number *INT linenum* of current source buffer"""
    global the_mediator    
    the_mediator.interp.on_app.goto_line(linenum)
    show_buff()

def select(start, end):
    """Selects from position *start* to position *end* in current buffer"""
    global the_mediator    
    the_mediator.interp.on_app.select(start, end)
    
def show_buff():
    """Shows content of current source buffer"""
    global the_mediator    
    the_mediator.interp.on_app.print_buff_content()

def move(steps):
    """Moves cursor by *INT steps* (can be negative)"""
    global the_mediator        
    pos = the_mediator.interp.on_app.curr_buffer.cur_pos
    the_mediator.interp.on_app.goto(pos + steps)
    show_buff()


def setmic(state):
    if not os.environ.has_key('VCODE_NOSPEECH'):
        natlink.setMicState(state)


def listen():
    if not os.environ.has_key('VCODE_NOSPEECH'):
        natlink.setMicState('on')
        natlink.waitForSpeech(0)
        natlink.setMicState('off')

def unresolved_abbreviations():
    global the_mediator        
    print 'List of unresolved abbreviations\n'
    sorted_unresolved = the_mediator.interp.known_symbols.unresolved_abbreviations.keys()
    sorted_unresolved.sort(lambda x, y: len(x) > len(y) or (len(x) == len(y) and x < y))
    for an_abbreviation in sorted_unresolved:
        symbol_list = the_mediator.interp.known_symbols.unresolved_abbreviations[an_abbreviation].keys()
        print '\'%s\': appears in %s' % (an_abbreviation, str(symbol_list))


def clear_symbols():
    #
    # Remove symbols from the Speech Recognition vocabulary
    #
    global the_mediator        
    the_mediator.interp.known_symbols.vocabulary_cleanup()
    
def quit():
    global quit_flag, the_mediator
    quit_flag = 1
    
    if sr_interface.speech_able():
#        print '-- mediator.quit: the_mediator=%s' % the_mediator.__dict__
        the_mediator.mixed_grammar.unload()
        the_mediator.code_select_grammar.unload()
        natlink.natDisconnect()

def init_simulator():
    global the_mediator

    if sr_interface.speech_able:
        natlink.natConnect()
        natlink.setMicState('off')

    the_mediator = MediatorObject.MediatorObject(interp=CmdInterp.CmdInterp(on_app=EdSim.EdSim()))
    the_mediator.configure()
    if sr_interface.speech_able:
#         natlink.natConnect()
#         natlink.setMicState('off')
        the_mediator.mixed_grammar.load()
        the_mediator.mixed_grammar.activate()
        the_mediator.code_select_grammar.load( ['Select', 'Correct'] )
        the_mediator.code_select_grammar.activate()

def execute_command(cmd):
    try:
        exec(cmd)
    except Exception, err:
        print 'Error executing command.\n'
        print '   Error type: %s' % err
        print '   Error data: %s' % err.__dict__

        
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

    init_simulator()
    
    #
    # For better error reporting, you can type some instructions here
    # instead of typing them at the console. The fact that the console
    # commands are eval'ed means the error reporting isn't great
    #
    # e.g. compile_symbols(['D:/Temp/blah.py'])
    #
    clear_symbols()    
    open_file('D:/blah.c')
    compile_symbols(['D:/VoiceCode/VCode.vg3_trans/Data/TestData/small_buff.c'])
    say('prefix horizontal position')
#    say('horizontal position equals this symbol is unresolved with arguments this symbol is unresolved too at index this symbol has an other abbreviation')
#      say_select(['Select', """horiz_pos\horizontal position"""])
#    quit()


    while (not quit_flag):
        sys.stdout.write('Command> ')
        cmd = sys.stdin.readline()
        execute_command(cmd)                
        
if (__name__ == '__main__'):
    
    if sr_interface.speech_able():
        natlink.natConnect()
#        print '-- main: checked mic state'

    opts, args = util.gopt(['h', None, 's', None, 'p', 50007])
#    print '-- mediator.__main__: opts=%s' % opts
    
    if opts['h']:
        print __doc__
    elif opts['s']:
        #
        # Run mediator using an editor simulator
        #
        simulator_mode(opts)        

    quit()
        
