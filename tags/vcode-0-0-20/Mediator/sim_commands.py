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

"""mediator simulator commands

Valid commands are:

help()
   display (this) list of commands

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
         
       - a list of words in their written\spoken form (or just
         written if it doesn't have a spoken form different from its
         written form).
         e.g.: say(['index', ' != \\not equal to', '0'])
   

    In general, it's better to specify *utterance* as a list of
    written\spoken words because it allows to simulate exactly what
    the SR does (e.g. what if the SR recognises an LSA as a sequence
    of words instead of its written\spoken form?)

    Note that if the utterance is a *Select XYZ* utterance, the first item
    in list *utterances* should be the whole verb used in the select statement.

    Example: say(['select previous', 'index', ' != \\not equal to', '0'])
             NOT
             say(['select', 'previous', 'index', ' != \\not equal to', '0'])
    
    Argument *user_input* is a string that will be sent to the
    mediator console's standard input. Use in automated regression
    testing, if the *say* command requires user additional user input
    (e.g. confirmation of a symbol match).
     
    If argument *bypass_NatLink* is true, the interpretation will be done
    withouth going through NatLink's recognitionMimic function.

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

make_position_visible(INT pos)
   Scroll so that pos is visible
   
print_abbreviations(show_unresolved=1)
   Prints out a list of the abbreviations in symbols that were parsed
   so far. If *show_unresolved=1*, also lists unresolved abbreviations
   and the symbols they appear in (an unresolved abbreviation is an
   abbreviation that appeared in a symbol and is neither a speech
   vocabulary word nor a known abbreviation).

print_error(STR message):
   Prints an error to stderr

print_symbols()
   Prints the list of symbols in the known symbols dictionary

provoke()
   causes an error deliberately

quit()
   Quit the simulator.

   Note that if you don't quit using this command
   (e.g. *Ctrl-C*), your DOS window will hang up.   
"""

import natlink
import os, profile, re, string, sys
import traceback
import vc_globals

sys.path = sys.path + [vc_globals.config, vc_globals.admin]

import CmdInterp, EdSim, MediatorObject, sr_interface, util, vc_globals
from CSCmd import CSCmd

# I'm not sure which of these contexts and actions are necessary for 
# sim_commands, as opposed to the rest of mediator.py, so I've just left them

# for actions that span different languages
from cont_gen import ContC, ContPy
from actions_gen import *

# for C support
from actions_C_Cpp import *

# for Python support
from actions_py import *

quit_flag = 0
the_mediator = None

# local name space for user command-line commands
command_space = {}

def help():
    print __doc__

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

    
def say(utterance, user_input=None, bypass_NatLink=0, echo_utterance=0):
    """Simulate an utterance *STR utterance*

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

    *BOOL echo_utterance=0* -- If true, echo the utterance on STDOUT.

    Examples: say('x not equal to') -> 'x != '
              say(['x', ' != \\not equal to'] -> 'x != '
    """
    
    global the_mediator

#    print '-- sim_commands.say: utterance=%s' % utterance

    if echo_utterance:
        print 'Saying: %s' % utterance

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
            # Clean up the written form in case user didn't type
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

def make_position_visible(pos):
    global the_mediator    
    the_mediator.interp.on_app.make_position_visible(pos)
    show_buff()

def select(start, end):
    """Selects from position *start* to position *end* in current buffer"""
    global the_mediator    
    the_mediator.interp.on_app.set_selection((start, end))
    show_buff()
    
def show_buff():
    """Shows content of current source buffer"""
    global the_mediator    
    the_mediator.interp.on_app.curr_buffer.print_buff()

def move(steps):
    """Moves cursor by *INT steps* (can be negative)"""
    global the_mediator        
    the_mediator.interp.on_app.move_relative(steps)
    show_buff()



def listen():
    if not os.environ.has_key('VCODE_NOSPEECH'):
        natlink.setMicState('on')
        natlink.waitForSpeech(0)
        natlink.setMicState('off')

def print_error(message):
    sys.stderr.write(message)

def provoke():
    print slidjf

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

    the_mediator.interp.known_symbols.cleanup()

def clear_abbreviations():
    #
    # Remove abbreviations from the symbol dictionary
    #
    global the_mediator        
    the_mediator.interp.known_symbols.abbreviations_cleanup()

def quit(clean_sr_voc=0, save_speech_files=None, disconnect=1):
    global quit_flag, the_mediator

    if the_mediator:
        the_mediator.quit(clean_sr_voc=clean_sr_voc, save_speech_files=save_speech_files, disconnect=disconnect)
        
    quit_flag = 1            

def setmic(state):
    if sr_interface.speech_able():
        sr_interface.connect()
        natlink.setMicState(state)