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

clear_abbreviations()
   Removes all defined abbreviations from VoiceCode's symbol dictionary

say(STR utterance, bypass_NatLink=1, user_input=None)
   Interprets string *utterance* as though it had been said by a user.

   Note that this command will not work with *Select XYZ* utterances.
   For those, you must use the *say_select* command.
    
   *utterance* can be either:
   
       - a string with the written form of what should be recognised by the
         SR system
         e.g.: say('index not equal to 0')
         
       - a list of list of words in their written\spoken form (or just
         written if it doesn't have a spoken form different from its
         written form).
         e.g.: say(['index', ' != \\not equal to', '0'])
   

    In general, it's better to specify *utterance* as a list of
    written\spoken words because it allows to simulate exactly what
    the SR does (e.g. what if the SR recognises an LSA as a sequence
    of words instead of its written\spoken form?)

    Argument *user_input* is a string that will be sent to the
    mediator console's standard input. Use in automated regression
    testing, if the *say* command requires user additional user input
    (e.g. confirmation of a symbol match).
     
    If argument *bypass_NatLink* is true, the interpretation will be done
    withouth going through NatLink's recognitionMimic function.

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
   
print_abbreviations(show_unresolved=1)
   Prints out a list of the abbreviations in symbols that were parsed
   so far. If *show_unresolved=1*, also lists unresolved abbreviations
   and the symbols they appear in (an unresolved abbreviation is an
   abbreviation that appeared in a symbol and is neither a speech
   vocabulary word nor a known abbreviation).

print_symbols()
   Prints the list of symbols in the known symbols dictionary

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

quit_flag = 0
the_mediator = None

def open_file(fname):
    """Open a file with name in current buffer.

    *STR fname* is the path of the file"""

    global the_mediator
    the_mediator.interp.on_app.open_file(fname)
    the_mediator.interp.known_symbols.parse_symbols(fname)
    show_buff()

def compile_symbols(file_list):
    global the_mediator
    
    the_mediator.interp.known_symbols.parse_symbols_from_files(file_list)
    print '>>> Known symbols are: '; the_mediator.interp.known_symbols.print_symbols()

    #
    # Save the symbols dictionary to file
    #
    the_mediator.interp.known_symbols.pickle()

    
def say(utterance, user_input=None, bypass_NatLink=0):
    """Simulate an utterance *STR utterance*

    Note that this command will not work with *Select XYZ* utterances.
    For those, you must use the [say_select] command.
    
    *STR utterance* -- The utterance. This can be a string with the
     written form of what should be recognised by the SR system. If
     it's a list, it should be a list of words in their written\spoken
     form (or just written if it doesn't have a spoken form different
     from its written form).

    In general, it's better to specify *utterance* as a list of
    written\spoken words because it allows to simulate exactly what
    the SR does (e.g. what if the SR recognises an LSA as a sequence
    of words instead of its written\spoken form?)

    *STR user_input* -- A string that will be sent to the mediator console's
     standard input. Use in automated regression testing, if the *say*
     command requires user additional user input (e.g. confirmation of
     a symbol match).
    
    *BOOL bypass_NatLink* -- if true, the interpretation will be done
    withouth going through NatLink's recognitionMimic function.

    Examples: say('x not equal to') -> 'x != '
              say(['x', ' != \\not equal to'] -> 'x != '
        
    .. [say_select] file:///./mediator.html#say_select"""
    
    global the_mediator

#    print '-- mediator.say: utterance=%s' % utterance    

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
        if util.islist(utterance) or util.istuple(utterance):
            words = []
            #
            # Clean up the written form in case use didn't type
            # special characters in the form that the SR expects
            # (e.g. '\n' instead of '{Enter}'
            #
            for a_word in utterance:
                spoken, written = sr_interface.spoken_written_form(a_word)
                if spoken != written:
                    written = sr_interface.clean_written_form(written, clean_for='sr')
                    words = words + [sr_interface.vocabulary_entry(spoken, written)]
                else:
                    words = words + [written]
        else:        
            words = re.split('\s+', utterance)

#        print '-- mediator.say: words=%s' % words
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

def print_symbols():
    global the_mediator
    the_mediator.interp.known_symbols.print_symbols()

def print_abbreviations(show_unresolved=1):
    global the_mediator
    the_mediator.interp.known_symbols.print_abbreviations(show_unresolved) 

def clear_symbols():
    #
    # Remove symbols from the Speech Recognition vocabulary
    #
    global the_mediator        
    the_mediator.interp.known_symbols.vocabulary_cleanup()

def clear_abbreviations():
    #
    # Remove abbreviations from the symbol dictionary
    #
    global the_mediator        
    the_mediator.interp.known_symbols.abbreviations_cleanup()

    
def quit():
    global quit_flag, the_mediator
    quit_flag = 1

    #
    # Cleanup the vocabulary to remove symbols from NatSpeak's vocabulary,
    # but don't save SymDict to file (we want the symbols and abbreviations to
    # still be there when we come back.
    #
    the_mediator.interp.known_symbols.vocabulary_cleanup(resave=0)
    if sr_interface.speech_able():
        the_mediator.mixed_grammar.unload()
        the_mediator.code_select_grammar.unload()
        natlink.natDisconnect()

def init_simulator(symdict_pickle_fname=None):
    global the_mediator

    if sr_interface.speech_able:
        natlink.natConnect()
        natlink.setMicState('off')

        if symdict_pickle_fname == None and the_mediator != None:
            #
            # Remove symbols from NatSpeak's dictionary 
            #
            the_mediator.interp.known_symbols.vocabulary_cleanup(resave=0)        

#        print '-- mediator.init_simulator: before creating MediatorObject'    
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


    if sr_interface.speech_able:
#         natlink.natConnect()
#         natlink.setMicState('off')
        the_mediator.mixed_grammar.load()
        the_mediator.mixed_grammar.activate(0)
        the_mediator.code_select_grammar.load( ['Select', 'Correct'] )
        the_mediator.code_select_grammar.activate()

#    print '-- mediator.init_mediator: at end, abbrevitions are:'; the_mediator.interp.known_symbols.print_abbreviations()

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

    init_simulator(symdict_pickle_fname = vc_globals.state + os.sep + 'symdict.pkl')
    
    #
    # For better error reporting, you can type some instructions here
    # instead of typing them at the console. The fact that the console
    # commands are eval'ed means the error reporting isn't great
    #
    # e.g. compile_symbols(['D:/Temp/blah.py'])
    #
    clear_symbols()        
    compile_symbols(['D:/VoiceCode/VCode.vg3_trans/Data/TestData/small_buff.c'])
    open_file('D:/blah.c')
#     print_abbreviations()
#      say('for loop index', user_input='1\n')
#    say('this symbol is unresolved comma')
#    quit()


    while (not quit_flag):
        sys.stdout.write('Command> ')
        cmd = sys.stdin.readline()
        execute_command(cmd)                
        
if (__name__ == '__main__'):
    
    if sr_interface.speech_able():
        natlink.natConnect()

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
        
