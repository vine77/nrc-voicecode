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

"""Define a series of regression tests for VoiceCode

**NOTE:** This file must be run with execfile, not imported.  Also,
before the tests are actually run (with auto_test), you must create an
appropriate regression.PersistentMediator object with a reference to the 
namespace in which you perform(ed) the execfile, and ensure that 
this namespace contains a reference to this PersistentMediator 
object named 'testing'
"""

import os, sys
import actions_C_Cpp, actions_py, CmdInterp, CSCmd, cont_gen, EdSim
import mediator, MediatorObject, Object, SymDict, test_pseudo_python
import util, unit_testing, vc_globals
import AppMgr, RecogStartMgr, GramMgr, sr_grammars
import KnownTargetModule, NewMediatorObject, TargetWindow, WinIDClient

from actions_gen import *
from actions_C_Cpp import *
from actions_py import *
from cont_gen import *


small_buff_c = vc_globals.test_data + os.sep + 'small_buff.c'
small_buff_py = vc_globals.test_data + os.sep + 'small_buff.py'

#  auto_test.add_test('PyUnitTests', unit_testing.run_all_pyunit_tests,
#                     desc='run a series of unit tests through PyUnit')



##############################################################################
# Testing SymDict
##############################################################################

def compilation_test(interp, source):
    
    """Does a compilation test on file *source*        
    """
    print '*** Compiling symbols from file: %s ***' % util.within_VCode(source)
    interp.cleanup()
    interp.parse_symbols_from_file(source)
    print '\n\nParsed symbols are: '
    interp.print_symbols()
    print 'Unresolved abbreviations are:'
    unresolved = interp.peek_at_unresolved()
    sorted_unresolved = unresolved.keys()
    sorted_unresolved.sort()
    for an_abbreviation in sorted_unresolved:
        symbol_list = unresolved[an_abbreviation].keys()
        print '\'%s\': appears in %s' % (an_abbreviation, str(symbol_list))
        
    print '\n*** End of compilation test ***\n'


def accept_symbol_match_test(interp, source, symbol_matches):
    """Does a test on SymDict.accept_symbol_match.
    """
    print '\n\n*** Accept symbol match test. source=\'%s\' ***' \
        % util.within_VCode(source)
    interp.cleanup()            
    interp.parse_symbols_from_file(source)
    print 'Parsed symbols are: '
    interp.print_symbols()
    print '\n\nUnresolved abbreviations are:'
    unresolved = interp.peek_at_unresolved()
    sorted_unresolved = unresolved.keys()
    sorted_unresolved.sort()
    for an_abbreviation in sorted_unresolved:
        symbol_list = unresolved[an_abbreviation].keys()
        print '\'%s\': appears in %s' % (an_abbreviation, str(symbol_list))

    sys.stdout.write('\n\nAccepting: ')
    for a_match in symbol_matches:
       sys.stdout.write('\'%s\' -> \'%s\', ' % (a_match.pseudo_symbol, a_match.native_symbol))
       interp.accept_symbol_match(a_match)
    sys.stdout.write('\n')
           

    print '\n\nAfter accepting those symbols, known symbols are:\n'
    interp.print_symbols()
    print '\n\nUnresolved abbreviations are:'
    unresolved = interp.peek_at_unresolved()
    sorted_unresolved = unresolved.keys()
    sorted_unresolved.sort()
    for an_abbreviation in sorted_unresolved:
        symbol_list = unresolved[an_abbreviation].keys()
        print '\'%s\': appears in %s' % (an_abbreviation, str(symbol_list))

        
    print '\n*** End of accept symbol match test ***\n'
    
        
def symbol_match_test(interp, sources, pseudo_symbols):
        """Tests pseudo-symbol matching.
        
        **INPUTS**

        [MediatorObject] interp -- [MediatorObject] instance to
        use for the test.
        
        *[STR]* sources -- List of source files to be compiled before
         doing the matches.
        
        *[STR]* pseudo_symbols -- List of pseudo-symbols to be matched.
        

        **OUTPUTS**
        
        *none* -- 
        """

        strsources = []
        for source in sources:
            strsources.append(util.within_VCode(source))

        print '*** Pseudo symbol match test***\n   Source files are: %s\n   Symbols are: %s\n\n' % (strsources, pseudo_symbols)


        #
        # Compile symbols
        #
        interp.cleanup()        
        for a_source in sources:
            interp.parse_symbols_from_file(a_source)
#        print '\n Known symbols are: \n'
#        interp.known_symbols.print_symbols()

        #
        # Match the symbols
        #
        for a_symbol in pseudo_symbols:
            matches = interp.match_pseudo_symbol(a_symbol)
            sys.stdout.write('\'%s\' matches: [' % a_symbol) 
            if matches:
                for a_match in matches:
                    sys.stdout.write('%s, ' % a_match.native_symbol)
            else: sys.stdout.write('[]')
            sys.stdout.write(']\n')

        print '\n*** End of Pseudo Symbol Match test ***'

        
def test_SymDict():
    """Self test for SymDict"""

    temp_config = temp_factory.new_config()
    interp = temp_config.interpreter()
#    a_mediator = MediatorObject.MediatorObject(app = EdSim.EdSim(),
#        interp=CmdInterp.CmdInterp())
#    a_mediator.configure()
    
#  temporary check
#    print repr(vc_globals.test_data)
    compilation_test(interp, vc_globals.test_data + os.sep + 'small_buff.c')
    compilation_test(interp, vc_globals.test_data + os.sep + 'large_buff.py')
    pseudo_symbols = ['set attribute', 'expand variables', 'execute file', 'profile Constructor Large Object', 'profile construct large object', 'auto test']
    symbol_match_test(interp, [vc_globals.test_data + os.sep + 'large_buff.py'], pseudo_symbols)

    a_match = SymDict.SymbolMatch(pseudo_symbol='this symbol is unresolved', native_symbol='this_sym_is_unres', words=['this', 'symbol', 'is', 'unresolved'], word_matches=['this', 'sym', 'is', 'unres'])    
    accept_symbol_match_test(interp, vc_globals.test_data + os.sep + 'small_buff.c', [a_match])

#    a_mediator.quit(save_speech_files=0, disconnect=0)    
    temp_config.quit()    

auto_test.add_test('SymDict', test_SymDict, desc='self-test for SymDict.py')


##############################################################################
# Testing CmdInterp
##############################################################################

# test_mediator = None


def test_CmdInterp_mediator(temp_config):

# I don't think this is necessary (or correct -- we do want the mediator
# to go out of scope) but for regression testing purposes, I'm first
# leaving it in and then will remove it.
#    global test_mediator
#    test_mediator = a_mediator
    a_mediator = temp_config.mediator()
    app = temp_config.editor()
    interp = temp_config.interpreter()
    acmd = CSCmd.CSCmd(spoken_forms=['for', 'for loop'], meanings={ContC(): c_simple_for, ContPy(): py_simple_for})
    a_mediator.add_csc(acmd)
    acmd = CSCmd.CSCmd(spoken_forms=['loop body', 'goto body'], meanings={ContC(): c_goto_body, ContPy(): py_goto_body})
    a_mediator.add_csc(acmd)    
    app.open_file(vc_globals.test_data + os.sep + 'small_buff.c')
    app.goto(41)
    print '\n\n>>> Testing command interpreter\n\n'
    print '\n>>> Interpreting in a C buffer'    
    print '\n>>> Current buffer is:\n'
    app.print_buff()
    old_stdin = util.stdin_read_from_string('1\n')

    #
    # Test if spoken form of CSC is recognised as a single SR vocabulary entry
    # e.g. 'for loop' recognised as: ['for loop\for loop']
    #
    print '>>> Interpreting: %s' % ['for loop', 'loop body']
    interp.interpret_NL_cmd(['for loop', 'loop body'],
        app)

    #
    # Test if spoken form of CSC is recognised as multiple vocabulary entries
    # e.g. 'for loop' recognised as ['for', 'loop']
    print '>>> Interpreting: %s' % ['for', 'loop', 'loop', 'body']
    interp.interpret_NL_cmd(['for', 'loop', 'loop', 'body'],
        app)                                       
    sys.stdin = old_stdin
    print '\n>>> Buffer is now:'
    app.print_buff()
    

    app.open_file(vc_globals.test_data + os.sep + 'small_buff.py')
    app.goto(43)
    app.curr_buffer().language = 'python'
    print '\n>>> Interpreting in a Python buffer'    
    print '\n>>> Current buffer is:\n'
    app.print_buff()

    print '>>> Interpreting: %s' % ['for loop', 'loop body']
    interp.interpret_NL_cmd(['for loop', 'loop body'],
        app)
    print '\n>>> Buffer is now:'
    app.print_buff()

    temp_config.quit()    
        
def test_CmdInterp():
    
    #
    # Create a command interpreter connected to the editor simulator
    #
#    natlink.natConnect()    
    temp_config = temp_factory.new_config(skip_config = 1)
#     a_mediator = MediatorObject.MediatorObject(app = EdSim.EdSim(),
#         interp=CmdInterp.CmdInterp())
    test_CmdInterp_mediator(temp_config)
    

auto_test.add_test('CmdInterp', test_CmdInterp, desc='self-test for CmdInterp.py')


###############################################################################
# Testing EdSim
###############################################################################

def test_EdSim():
    """Self test for EdSim.py."""

    test_buff = posixpath.expandvars('$VCODE_HOME' + os.sep + 'Data' + os.sep + 'TestData' + os.sep + 'small_buff.c')
    sim = EdSim.EdSim()
    test_buff2 = posixpath.expandvars('$VCODE_HOME' + os.sep + 'Data' + os.sep + 'TestData' + os.sep + 'small_buff2.c')


    print ">>> Testing EdSim.py"
    print "\n\n>>> Opening a buffer"
    sim.open_file(test_buff)    
    sim.print_buff()

    print "\n\n>>> Moving to position 5"
    sim.goto(5)
    sim.print_buff()

    print "\n\n>>> Testing breadcrumbs"
    print "\n>>> Dropping one here"; sim.print_buff()
    sim.drop_breadcrumb()
    sim.goto(10)
    sim.drop_breadcrumb()
    print "\n>>> Dropping one here"; sim.print_buff()    
    print "\n>>> Popping 2 crumbs -> end up here:"
    sim.pop_breadcrumbs(num=2)
    sim.print_buff()
    print "\n>>> Dropping one here"; sim.print_buff()    
    sim.drop_breadcrumb()
    sim.goto(10)
    print "\n>>> Dropping one here"; sim.print_buff()    
    sim.drop_breadcrumb()
    sim.goto(20)
    sim.print_buff()
    sim.pop_breadcrumbs()
    print "\n>>> Popping 1 crumb -> end up here..."    
    sim.print_buff()

    print '\n\n>>> Testing code indentation. Inserting for loop.'
    sim.goto(42)
    sim.insert_indent('for (ii=0; ii <= maxValue; ii++)\n{\n', '\n}\n')
    sim.print_buff()
    sim.cleanup()


auto_test.add_test('EdSim', test_EdSim, desc='self-test for EdSim.py')


###############################################################################
# Testing Object.py
###############################################################################

class Person1(Object.Object):
    def __init__(self, name, citizenship=None, **args_super):
        self.deep_construct(Person1, {'name': name, 'citizenship': citizenship}, args_super)

class Employee1(Person1):
    def __init__(self, salary=None, **args_super):
        self.deep_construct(Employee1, {'salary': salary}, args_super)

class MyPerson(Person1):
    def __init__(self, marital_status=None, **args_super):
        self.deep_construct(MyPerson, {'marital_status': marital_status}, args_super, new_default={'citizenship': 'Canadian eh?'})

class Canadian(Person1):
    def __init__(self, **args_super):
        self.deep_construct(Canadian, {}, args_super, enforce_value={'citizenship': 'Canadian eh?'})

class Person2(Object.Object):
    def __init__(self, name=None, citizenship=None, init_file=None, **args_super):
        self.deep_construct(Person2, {'name': name, 'citizenship': citizenship}, args_super)
        sys.stdout.write('\nPerson2.__init__ received init_file=%s' % init_file)

class AnimatedCharacter:
    def __init__(self, animation_file, frames_per_sec=40):
        self.animation_file = animation_file
        self.frames_per_sec = frames_per_sec
              

class AnimatedPerson(Person1, AnimatedCharacter):
    def __init__(self, animation_file, frames_per_sec=40, **args_super):
        self.deep_construct(AnimatedPerson, {'animation_file': animation_file, 'frames_per_sec': frames_per_sec}, args_super, exclude_bases={AnimatedCharacter: 1})
        AnimatedCharacter.__init__(self, animation_file, frames_per_sec=frames_per_sec)

def try_attribute(obj, name, operation):
    """Test setting/getting attributes

    **INPUTS**

    *ANY* obj -- object on which we will get/set attributes 

    *STR* name -- name of attribute to get/set 

    *STR* operation -- *'get'* or *'set'*

    **OUTPUTS**

    *none* -- 
    """
    env_py_debug_object = None
    if os.environ.has_key('PY_DEBUG_OBJECT'): env_py_debug_object =  os.environ['PY_DEBUG_OBJECT']
    sys.stdout.write("\nTrying to %s the value of attribute '%s', $PY_DEBUG_OBJECT=%s\n   -> " % (operation, name, env_py_debug_object))
    if (operation == 'set'):
        code = "obj." + name + " = '999'"
    else:
        code = "x = obj." + name
    x = 0
    try:
        exec(code)
    except AttributeError, exc:
        sys.stdout.write("Caught AttributeError exception: '%s'" % [exc.__dict__])
    else:
        sys.stdout.write("Caught NO AttributeError exception. ")
        str = "obj.%s=%s, x=%s" % (name, obj.name, x)
        sys.stdout.write(str)
    sys.stdout.write("\n\n")
        

def test_Object():

    obj = Object.SmallObject()
    sys.stdout.write("Testing exceptions for get/set\n\n")
    try_attribute(obj, 'name', 'get')
    try_attribute(obj, 'name', 'set')
    try_attribute(obj, 'nonexistant', 'get')
    try_attribute(obj, 'nonexistant', 'set')

    result = Employee1(name='Alain', salary='not enough')    
    print "Testing inheritance of constructor arguments\n   Employee1(name='Alain', salary='not enough') -> %s\n" % result.__dict__

    print "\nRedefining default value of *citizenship*\n   MyPerson(name='Alain') -> result=%s" % result.__dict__

    result = MyPerson(name='Alain', citizenship='US citizen')
    print "\nOverriding redefined default value of *citizenship*\n   MyPerson(name='Alain', citizenship='US citizen') -> result=%s" % result.__dict__    

    result = Canadian(name='Alain')
    print "\nEnforcing 'Canadian eh?' as the value of *citizenship*\n   Canadian(name='Alain') -> result=%s" % result.__dict__    

    sys.stdout.write("\nTrying to change enforced value 'Canadian eh?' of *citizenship*\n   Canadian(citizenship='US') -> ")
    try:
        result = Canadian(citizenship='US')
        print 'Test failed. EnforcedConstrArg exception should have been raised but wasn\'t'
    except Object.EnforcedConstrArg, mess:
        print 'Test OK. EnforcedConstrArg was correctly raised: \'%s\'' % mess


    result = Person2(init_file='C:/temp.txt')
    print "\nClass with private *init_file* attribute*\n   Person2(init_file='C:/temp.txt') -> result=%s" % result.__dict__    

    result = AnimatedPerson(name='Alain', animation_file='C:/People/Alain.dat')
    print "\nSubclassing from non-standard class AnimatedCharacter.*\n   AnimatedPerson(name='Alain', animation_file='C:/People/Alain.dat') -> result=%s" % result.__dict__        


auto_test.add_test('Object', test_Object, desc='self-test for Object.py')

###############################################################################
# Testing sr_interface.connect() when VoiceCode user is not defined
###############################################################################

def test_no_sr_user():
    sr_interface.disconnect()
    old_vc_user_name= sr_interface.vc_user_name
    sr_interface.vc_user_name = 'dfafasdfrqowerglgferqeandgliaugfa'    
    print 'Trying to connect to SR system with inexistant user name'
    try:
        sr_interface.connect('off')
    except natlink.UnknownName:
        print 'natlink.UnknownName exception was sucessfully raised.'
    except Exception, err:
        print 'ERROR: wrong error was raised: err=%s, err.__dict__=%s' % (err, err.__dict__)
    else:
        print 'ERROR: natlink.UnknownName exception was NOT sucessfully raised.'
    sr_interface.vc_user_name = old_vc_user_name
    
#auto_test.add_test('no_sr_user', test_no_sr_user, desc='testing connect with inexistant SR user')

###############################################################################
# Testing mediator.py console
###############################################################################

def test_command(command):
    
    print '\n\n>>> Testing console command: %s\n' % command
    sys.stdout.flush()
    testing.execute_command(command)
    sys.stdout.flush()

def test_say(utterance, user_input=None):
    print '\n\n>>> Testing console command: say(%s, user_input=\'%s\')' % (utterance, user_input)
    sys.stdout.flush()
    commands.say(utterance, user_input)
    sys.stdout.flush()
    

def test_mediator_console():
    testing.init_simulator_regression()
    test_command("""clear_symbols()    """)
    test_command("""open_file('blah.c')""")
    file = vc_globals.test_data + os.sep + 'small_buff.c'
    commands.print_abbreviations()    
    test_command("""compile_symbols([r'""" + file + """'])""")
    test_say(['for', 'loop', 'horiz_pos\\horizontal position', 'loop', 'body'])

    test_command("""say(['select', 'horiz_pos\\horizontal position', '=\equals'])""")
    test_command("""quit(save_speech_files=0, disconnect=0)""")        



auto_test.add_test('mediator_console', test_mediator_console, desc='testing mediator console commands')


###############################################################################
# Testing Select Pseudocode console
###############################################################################


def test_select_pseudocode():

    
    testing.init_simulator_regression()
    test_command("""open_file('blah.py')""")
    test_say(['index', 'equals', '0', 'new statement'], user_input='1\\n')
    test_say(['index', 'equals', '1', 'new statement'], user_input='1\\n')    
    test_say(['index', 'equals', '0', 'new statement'], user_input='1\\n')
    test_say(['index', 'equals', '1', 'new statement'], user_input='1\\n')        
    test_say(['index', 'equals', '0', 'new statement'], user_input='1\\n')

#    util.request_console_be(active=1)
    
    #
    # Testing go commands
    #
    test_command("""goto_line(2)""")
    test_say(['go', 'index', '=\\equals', '0'])
    test_command("""goto_line(2)""")
    test_say(['go after next', 'index', '=\\equals', '0'])
    test_command("""goto_line(2)""")
    test_say(['go after previous', 'index', '=\\equals', '0'])
    test_command("""goto_line(2)""")
    test_say(['go before', 'index', '=\\equals', '0'])
    test_command("""goto_line(2)""")
    test_say(['go before next', 'index', '=\\equals', '0'])
    test_command("""goto_line(2)""")
    test_say(['go before previous', 'index', '=\\equals', '0'])
    test_command("""goto_line(2)""")
    test_say(['go next', 'index', '=\\equals', '0'])
    test_command("""goto_line(2)""")
    test_say(['go previous', 'index', '=\\equals', '0'])
    test_command("""goto_line(2)""")
    test_say(['after next', 'index', '=\\equals', '0'])
    test_command("""goto_line(2)""")
    test_say(['after previous', 'index', '=\\equals', '0'])
    test_command("""goto_line(2)""")
    test_say(['before', 'index', '=\\equals', '0'])
    test_command("""goto_line(2)""")
    test_say(['before next', 'index', '=\\equals', '0'])
    test_command("""goto_line(2)""")
    test_say(['before previous', 'index', '=\\equals', '0'])
    test_command("""goto_line(2)""")
    
    #
    # Testing correct commands
    #
# DCF: this is silly.  Until we implement correct xyz, these are
# equivalent to the corresponding select xyz commands, so there is no
# point in testing them.  Once we implement correct xyz,
# test_say(['correct',...]) will bring up the correction test, so the
# old "correct" results for this test won't be right anyway
#    test_say(['correct', 'index', '=\\equals', '0'])
#    test_command("""goto_line(2)""")
#    test_say(['correct next', 'index', '=\\equals', '0'])
#    test_command("""goto_line(2)""")
#    test_say(['correct previous', 'index', '=\\equals', '0'])

    #
    # Testing selectionn commands
    #
    test_command("""goto_line(2)""")
    test_say(['next', 'index', '=\\equals', '0'])
    test_command("""goto_line(2)""")
    test_say(['previous', 'index', '=\\equals', '0'])
    test_command("""goto_line(2)""")
    test_say(['select', 'index', '=\\equals', '0'])
    test_command("""goto_line(2)""")
    test_say(['select next', 'index', '=\\equals', '0'])
    test_command("""goto_line(2)""")
    test_say(['select previous', 'index', '=\\equals', '0'])

    #
    # Testing repeated go commands in both directions
    #
    test_command("""goto_line(1)""")
    test_say(['go next', 'index', '=\\equals', '0'])
    test_say(['go next', 'index', '=\\equals', '0'])
    test_command("""goto_line(6)""")
    test_say(['go previous', 'index', '=\\equals', '0'])
    test_say(['go previous', 'index', '=\\equals', '0'])
    

    #
    # Testing repeated correction in both directions
    #
# DCF: this is silly.  Until we implement correct xyz, these are
# equivalent to the corresponding select xyz commands, so there is no
# point in testing them.  Once we implement correct xyz,
# test_say(['correct',...]) will bring up the correction test, so the
# old "correct" results for this test won't be right anyway
#    test_command("""goto_line(1)""")
#    test_say(['correct next', 'index', '=\\equals', '0'])
#    test_say(['correct next', 'index', '=\\equals', '0'])
#    test_command("""goto_line(6)""")
#    test_say(['correct previous', 'index', '=\\equals', '0'])
#    test_say(['correct previous', 'index', '=\\equals', '0'])
    
    #
    # Testing repeated selection in both directions
    #
    test_command("""goto_line(1)""")
    test_say(['select next', 'index', '=\\equals', '0'])
    test_say(['select next', 'index', '=\\equals', '0'])
    test_command("""goto_line(6)""")
    test_say(['select previous', 'index', '=\\equals', '0'])
    test_say(['select previous', 'index', '=\\equals', '0'])

#    util.request_console_be(active=0)    
    
    test_command("""quit(save_speech_files=0, disconnect=0)""")        


auto_test.add_test('select_pseudocode', test_select_pseudocode, desc='testing select pseudocode commands')



##############################################################################
# Testing automatic addition of abbreviations
##############################################################################

def test_auto_add_abbrevs():
    testing.init_simulator_regression()
    
    test_command("""open_file('blah.c')""")
    print repr(vc_globals.test_data)
    file = vc_globals.test_data + os.sep + 'small_buff.c'    
    test_command("""compile_symbols([r'""" + file + """'])""")
    test_command("""print_abbreviations(1)""")    

    #
    # Match selection dialog should be invoked, and abbreviation
    # unres->unresolved should be added
    #
    test_say(['this', 'symbol', 'is', 'unresolved', ', \\comma'], user_input='1\\n')
    test_command("""print_abbreviations(1)""")
    test_command("""print_symbols()""")

    #
    # Match selection dialog should NOT be invoked 
    #
    test_say(['this_sym_is_unres_too\\this symbol is unresolved too', ', \\comma'])
    test_command("""print_symbols()""")    
    test_command("""print_abbreviations(1)""")

    #
    # Match selection dialog should be invoked, and abbreviation
    # f->file should NOT be added (too short)
    #
    test_say(['file', 'name', ', \\comma'], user_input='1\\n')
    test_command("""print_symbols()""")    
    test_command("""print_abbreviations(1)""")

    #
    # Case with abbreviations which are the first letter of every word
    # (API->"Application Programming Interface"). Should be added as
    # a single abbreviation instead of three separate ones (A->applicaiton,
    # P->programming, I->interface).
    #
    test_say(['application', 'programming', 'interface', 'function', ', \\comma'], user_input='1\\n')
    test_command("""print_abbreviations(1)""")
    test_command("""quit(save_speech_files=0, disconnect=0)""")        

auto_test.add_test('automatic_abbreviations', test_auto_add_abbrevs, desc='testing automatic creation of abbreviations')


##############################################################################
# Testing persistence between VoiceCode sessions
##############################################################################

def test_persistence():
        
    #
    # Create make mediator console use an empty file for SymDict persistence
    #
    fname = vc_globals.tmp + os.sep + 'tmp_symdict.pkl'
    try:
        os.remove(fname)
    except:
        # Never mind if file doesn't exist
        pass

    print '\n\n>>> Starting mediator with persistence'
    testing.init_simulator_regression(symdict_pickle_fname=fname)

    #
    # Compile symbols
    #
    test_command("""compile_symbols([r'""" + vc_globals.test_data + os.sep + """small_buff.c'])""")

    #
    # Restart the mediator, with saved SymDict. The symbols should still be
    # there
    #
    print '\n\n>>> Restarting mediator with persistence. Compiled symbols should still be in the dictionary.\n'
    test_command("""quit(save_speech_files=0, disconnect=0)""")
    testing.init_simulator_regression(symdict_pickle_fname=fname)
    test_command("""print_symbols()""")

    #
    # Restart the mediator without saved SymDict. The symbols should not be
    # there anymore.
    #
    print '\n\n>>> Restarting mediator WITHOUT persistence. There should be NO symbols in the dictionary.\n'
    test_command("""quit(save_speech_files=0, disconnect=0)""")
    testing.init_simulator_regression(symdict_pickle_fname=None)
    test_command("""print_symbols()""")
    test_command("""quit(save_speech_files=0, disconnect=0)""")        
    

auto_test.add_test('persistence', test_persistence, desc='testing persistence between VoiceCode sessions')    


##############################################################################
# Testing redundant translation of LSAs and symbols
##############################################################################

def test_redundant_translation():
    global small_buff_c
    
    testing.init_simulator_regression()    
    test_command("""open_file('blah.c')""")
    test_command("""compile_symbols([r'""" + small_buff_c + """'])""")
    test_say(['index', ' != \\not equal to', '0'], '0\n0\n')
    test_say(['index', 'not', 'equal', 'to', '0'], '0\n0\n')
    test_say(['move_horiz\\move horizontally'], '0\n0\n')
    test_say(['move', 'horizontally'], '0\n0\n')
    test_command("""quit(save_speech_files=0, disconnect=0)""")        

auto_test.add_test('redundant_translation', test_redundant_translation, desc='testing redundant translation of LSAs and symbols at SR and Mediator level')    


##############################################################################
# Testing dictation and navigation of punctuation
##############################################################################

def test_punctuation():
    testing.init_simulator_regression()
    commands.open_file('blah.py')

    commands.say(['variable', ' \\blank space', ' = \\equals', ' \\space bar', 'index', '*\\asterisk', '2', '**\\double asterisk', '8', '\n\\newline'], user_input='1\n2\n1\n1\n1\n1\n1\n', echo_utterance=1)

## causes recognitionMimic error in Natspeak 4
#    commands.say(['variable', ' = \\equals', 'variable', '/\\slash', '2', '+\\plus sign', '1', '-\\minus sign', 'index', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['variable', 'equals', 'variable', '/\\slash', '2', '+\\plus sign', '1', '-\\minus sign', 'index', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['variable', ' = \\equals', 'index', '%\\percent', '2', ' + \\plus', 'index', '%\\percent sign', '3', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['if', 'index', '&\\and percent', 'variable', 'then'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['if', 'index', '|\\pipe', 'variable', '|\\pipe sign', 'index', '|\\vertical bar', 'value', 'then'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['index', ' = \\equals', '0', ';\\semicolon', 'variable', ' = \\equals', '0', ';\\semi', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['index', '.\\dot', 'function', '()\\without arguments', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['variable', ' = \\equals', 'new', 'list', '0', '...\\ellipsis', '10', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['#\\pound', '!\\bang', 'python', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['#\\pound sign', '!\\exclamation mark', 'python', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['if', '~\\tilde', 'index', 'and', '~\\squiggle', 'variable', 'then'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['variable', '::\\double colon', 'index', '::\\colon colon', 'field', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['if', 'index', '<\\less sign', '0', ' and \\and', 'index', '>\\greater sign', '-\\minus sign', '1', 'then'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    

    commands.say(['index', '=\\equal sign', '0', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['function', '(\\open paren', '0', ')\\close paren', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['function', 'parens', '0', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['function', '()\\empty parens', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['list', '[\\open bracket', '0', ']\\close bracket', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['list', 'brackets', '0', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['list', '[]\\empty brackets', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    


## BUG: causes recognitionMimic error    
##    commands.say(['dictionary', '{\\open brace', '0', '}\\close brace', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['dictionary', 'braces', '0', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

## BUG: causes recognitionMimic error
##    commands.say(['dictionary', '{}\\empty braces', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['<\\open angled', 'head', '>\\close angled', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['angled brackets', 'head', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['<>\\empty angled', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    
    commands.say(['string', ' = \\equals', '\'\\open single quote', 'message', '\'\\close single quote', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
## causes recognitionMimic error in Natspeak 4
#    commands.say(['string', ' = \\equals', 'single', 'quotes', 'message', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['string', 'equals', 'single', 'quotes', 'message', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    
    commands.say(['\'\'\\empty single quotes', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['string', ' = \\equals', '\"\\open quote', 'message', '\"\\close quote', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
## causes recognitionMimic error in Natspeak 4
#    commands.say(['string', ' = \\equals', 'quotes', 'message', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['string', 'equals', 'quotes', 'message', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['""\\empty quotes', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['string', ' = \\equals', '`\\open back quote', 'message', '`\\close back quote', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['string', ' = \\equals', 'back', 'quotes', 'message', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['``\\empty back quotes', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    commands.say(['\\a\\back slash a.', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\a\\back slash alpha', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\b\\back slash b.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\b\\back slash bravo'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\c\\back slash c.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\c\\back slash charlie'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\d\\back slash d.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\d\\back slash delta'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\e\\back slash e.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\e\\back slash echo'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\f\\back slash f.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\f\\back slash foxtrot'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\g\\back slash g.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\g\\back slash golf'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\h\\back slash h.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\h\\back slash hotel'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\i\\back slash i.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\i\\back slash india'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\j\\back slash j.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\j\\back slash juliett'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\k\\back slash k.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\k\\back slash kilo'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\l\\back slash l.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\l\\back slash lima'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\m\\back slash m.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\m\\back slash mike'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\n\\back slash n.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\n\\back slash november'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\o\\back slash o.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\o\\back slash oscar'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\p\\back slash p.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\p\\back slash papa'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\q\\back slash q.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\q\\back slash quebec'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\r\\back slash r.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\r\\back slash romeo'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\s\\back slash s.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\s\\back slash sierra'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\t\\back slash t.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\t\\back slash tango'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\u\\back slash u.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\u\\back slash uniform'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\v\\back slash v.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\v\\back slash victor'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\w\\back slash w.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\w\\back slash whiskey'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\x\\back slash x.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\x\\back slash xray'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\y\\back slash y.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\y\\back slash yankee'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\z\\back slash z.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\z\\back slash zulu'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\A\\back slash cap a.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\A\\back slash cap alpha', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\B\\back slash cap b.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\B\\back slash cap bravo', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    #
#BUG:    commands.say(['quotes', '\\C\\back slash cap c.', '\\C\\back slash cap charlie', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\D\\back slash cap d.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\D\\back slash cap delta', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    

    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\E\\back slash cap e.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\E\\back slash cap echo', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\F\\back slash cap f.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\F\\back slash cap foxtrot', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\G\\back slash cap g.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\G\\back slash cap golf', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\H\\back slash cap h.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\H\\back slash cap hotel', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\I\\back slash cap i.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\I\\back slash cap india', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)


    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\J\\back slash cap j.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\J\\back slash cap juliett', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)


    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\K\\back slash cap k.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\K\\back slash cap kilo', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)


    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\L\\back slash cap l.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\L\\back slash cap lima', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)


    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\M\\back slash cap m.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\M\\back slash cap mike', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)


    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\N\\back slash cap n.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\N\\back slash cap november', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\O\\back slash cap o.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\O\\back slash cap oscar', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    
    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\P\\back slash cap p.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\P\\back slash cap papa', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\Q\\back slash cap q.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\Q\\back slash cap quebec', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)


    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\R\\back slash cap r.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\R\\back slash cap romeo', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)


    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\S\\back slash cap s.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\S\\back slash cap sierra', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)


    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\T\\back slash cap t.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\T\\back slash cap tango', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)


    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\U\\back slash cap u.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\U\\back slash cap uniform', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)


    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\V\\back slash cap v.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\V\\back slash cap victor', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\W\\back slash cap w.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\W\\back slash cap whiskey', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)


    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\X\\back slash cap x.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\X\\back slash cap xray', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)


    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\Y\\back slash cap y.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\Y\\back slash cap yankee', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)


    commands.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\Z\\back slash cap z.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['\\Z\\back slash cap zulu', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
  

    commands.say(['index', 'semi', 'variable', 'semi'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
  
    commands.say(['previous semi', 'previous semi'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)


    commands.say(['after semi'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['before previous semi'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['after semi'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['before semi'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['variable', ' = \\equals', 'brackets', '0', ',\\comma', '1', ',\\comma', '3'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['previous comma'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['after comma'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before previous comma'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before next comma'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['variable', '.\\dot', 'field', '.\\dot', 'value'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['previous dot', 'previous dot'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['after dot'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before previous dot'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before next dot'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['braces', 'variable', ': \\colon', '0', 'value', ': \\colon', '0'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['previous colon', 'previous colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['after colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before previous colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before next colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['variable', ' = \\equals', '2', '*\\asterisk', '3', '*\\asterisk', '4'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['previous asterisk', 'previous star'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['after star'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before previous asterisk'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before next star'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
## causes recognitionMimic error in Natspeak 4
#    commands.say(['variable', '= \\equals', '2', '/\\slash', '3', '/\\slash', '4'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['variable', 'equals', '2', '/\\slash', '3', '/\\slash', '4'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['previous slash', 'previous slash'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['after slash'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before previous slash'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before next slash'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['variable', ' = \\equals', '2', ' + \\plus', '3', ' + \\plus', '4'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['previous plus', 'previous plus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['after plus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before previous plus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before next plus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
## causes recognitionMimic error in Natspeak 4
#    commands.say(['variable', ' = \\equals', '2', ' - \\minus', '3', ' - \\minus', '4'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['variable', 'equals', '2', ' - \\minus', '3', ' - \\minus', '4'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['previous minus', 'previous minus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['after minus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before previous minus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before next minus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
## causes recognitionMimic error in Natspeak 4
#    commands.say(['variable', ' = \\equals', '2', ' % \\modulo', '3', ' % \\modulo', '4'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['variable', 'equals', '2', ' % \\modulo', '3', ' % \\modulo', '4'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['previous percent', 'previous percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['after percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before previous percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before next percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['0', '&\\and percent', '1', '&\\and percent', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['previous and percent', 'previous and percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['after and percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before previous and percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before next and percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['0', '|\\pipe', '1', '|\\pipe', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['previous pipe', 'previous pipe'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['after pipe'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before previous pipe'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before next pipe'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['0', '...\\ellipsis', '1', '...\\ellipsis', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['previous ellipsis', 'previous ellipsis'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['after ellipsis'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before previous ellipsis'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before next ellipsis'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['0', '!\\bang', '1', '!\\bang', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['previous bang', 'previous bang'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['after bang'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before previous bang'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before next bang'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['0', '?\\question mark', '1', '?\\question mark', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['previous question mark', 'previous question mark'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['after question mark'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before previous question mark'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before next question mark'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['0', '#\\pound', 'sign', '1', '#\\pound', 'sign', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['previous pound sign', 'previous pound sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['after pound sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before previous pound sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before next pound sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['0', '::\\double colon', '1', '::\\double colon', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['previous double colon', 'previous double colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['after double colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before previous double colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before next double colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['0', '~\\tilde', '1', '~\\tilde', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['previous tilde', 'previous tilde'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['after tilde'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before previous tilde'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before next tilde'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['0', '<\\less sign', '1', '<\\less sign', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['previous less sign', 'previous less sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['after less sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before previous less sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before next less sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['0', '>\\greater sign', '1', '>\\greater sign', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['previous greater sign', 'previous greater sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['after greater sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before previous greater sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before next greater sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['0', '=\\equal sign', '1', '=\\equal sign', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['previous equal sign', 'previous equal sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['after equal sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before previous equal sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['before next equal sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    commands.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    commands.say(['between parens', '1'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['before previous paren'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    commands.say(['after paren'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['before paren'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['previous paren'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    commands.say(['out of parens'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['before previous paren'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    commands.say(['back out of parens'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['between brackets', '1'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['before previous bracket'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    commands.say(['after bracket'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['before bracket'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['previous bracket'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['out of brackets'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['before previous bracket'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    commands.say(['back out of brackets'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['between braces', '1'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['before previous brace'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    commands.say(['after brace'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['before brace'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['previous brace'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    commands.say(['out of braces'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['before previous brace'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    commands.say(['back out of braces'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n', echo_utterance=1)


    commands.say(['between angled', '1'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['before previous angled'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    commands.say(['after angled'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['before angled'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['previous angled'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    commands.say(['out of angled'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['before previous angled'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    commands.say(['back out of angled'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['between single quotes', '1'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['before previous single quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    commands.say(['after single quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['before single quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['previous single quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    commands.say(['out of single quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['before previous single quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    commands.say(['back out of single quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['between quotes', '1'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['before previous quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    commands.say(['after quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['before quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['previous quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    commands.say(['out of quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['before previous quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    commands.say(['back out of quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n', echo_utterance=1)

    commands.say(['between back quotes', '1'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['before previous back quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    commands.say(['after back quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['before back quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['previous back quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    commands.say(['out of back quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['before previous back quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    commands.say(['back out of back quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    commands.say(['new statement'], user_input='2\n2\n2\n2\n', echo_utterance=1)

    commands.quit(save_speech_files=0, disconnect=0)    

auto_test.add_test('punctuation', test_punctuation, 'testing the various Python CSCs and LSAs')



##############################################################################
# Testing the various Python CSCs and LSAs
##############################################################################
def pseudo_python_wrapper():
    test_pseudo_python.test_dictate_from_scratch(testing)

auto_test.add_test('python', pseudo_python_wrapper, 'testing the various CSCs and LSAs for dictating Python from scratch')

def pseudo_python_editing_wrapper():    
    test_pseudo_python.test_editing(testing)
    
auto_test.add_test('python_editing', pseudo_python_editing_wrapper, 'testing the various CSCs and LSAs for editing Python')

##############################################################################
# Testing repetition of last commands
##############################################################################


def test_repeat_last():
    testing.init_simulator_regression()    
    file_name = vc_globals.test_data + os.sep + 'large_buff.py'
    test_command("""open_file(r'""" + file_name + """')""")
    test_command("""say(['after hyphen'])""")
    test_command("""say(['again'])""")
    test_command("""goto_line(1)""")
    test_command("""say(['after hyphen'])""")
    test_command("""say(['again 3 times'])""")
    test_command("""goto_line(1)""")
    test_command("""say(['after hyphen'])""")
    test_command("""say(['3 times'])""")
    
    

auto_test.add_test('repeat_last', test_repeat_last, 'testing repetition of last command')


##############################################################################
# Testing changing direction of previous command
##############################################################################


def test_change_direction():
    testing.init_simulator_regression()
    
    file_name = vc_globals.test_data + os.sep + 'large_buff.py'
    
    test_command("""open_file(r'""" + file_name + """')""")
    
    
    test_command("""say(['after hyphen'])""")
    test_command("""say(['again'])""")
    test_command("""say(['again'])""")
    test_command("""say(['previous one'])""")
    test_command("""say(['previous one'])""")
    test_command("""say(['next one'])""")
    
auto_test.add_test('change_direction', test_change_direction, 'testing changing direction of last command')

##############################################################################
# Testing LSA masking by NatSpeak words
##############################################################################


def test_misc_bugs():
    
    testing.init_simulator_regression()

    test_command("""open_file(r'blah.py')""")

    #
    # NatSpeak defined words like '<\\less-than' used to mask the VoiceCode
    # defined words like '<\\less than' (i.e. no hyphen). Since interpreter
    # didn't know of an LSA with spoken form 'less-than', it treated it as
    # part of a new symbol.
    #
    # This tests a fix which ignores non-alphanums in the spoken form of
    # words to be interpreted.
    #
    test_command("""say(['<\\less-than', '>\\greater-than', '=\\equal-sign'])""")
    
auto_test.add_test('misc_bugs', test_misc_bugs, 'Testing a series of miscellaneous bugs that might reoccur.')


##############################################################################
# Testing AppMgr dictionaries
##############################################################################

def manager_state(manager):
    print ''
    print 'state {'
    apps = manager.app_names()
    for app in apps:
        print 'application: ', app
        instances =  manager.app_instances(app)
        for instance in instances:
            sys.stdout.flush()
            print 'instance: ', instance
            a_name = manager.app_name(instance)
            if a_name != app:
                print 'Warning: app names %s and %s do not match' \
                    % (app, a_name)
            windows = manager.known_windows(instance)
#            print 'windows is ', repr(windows), type(windows), type([])
            for window in windows:
                print 'window %d' % (window)
                win_ins = manager.window_instances(window)
#                print repr(win_ins)
                if instance not in win_ins:
                    print 'Warning: instance %s not found in window list' \
                        % instance
                sys.stdout.flush()
    print 'known windows', manager.known_windows()
    print '} state'
    print ''

def instance_status(manager, instance):
    print ''
    if not manager.known_instance(instance):
        print "instance %s is unknown" % instance
        return
    print "instance %s" % instance
    module = manager.instance_module(instance)
    if module != None:
        print "running in module %s" % module
    else:
        print "(unknown module)"
    windows = manager.known_windows(instance)
    print "windows: ", windows
    for window in windows:
        print "window #%d:" % window
        if manager.recog_mgr.shared_window(window):
            print "shared"
        if manager.recog_mgr.single_display(window):
            print "single-window display"
        instances = manager.window_instances(window)
        print "all instances for window:"
        for app in instances:
            print app
    print ''

def set_window(current, window, app_name, app = None, alt_title = ""):
    current.set_info(window.ID(), window.module(), app, app_name, alt_title)

def start_recog(manager, current):
    win, title, module = current.window_info()
    manager.recog_mgr._recognition_starting(win, title, module)

def new_buffer_for_instance(instance, buffer, before = "", after = ""):
    print 'new buffer %s for instance %d' % (buffer, int(instance))
    instance.open_file(buffer)
    b = instance.find_buff(buffer)
    b.insert_indent(before, after)
    instance.print_buff_if_necessary()

def new_instance(manager, current, app, window = None, 
        alt_title = ""):
    print 'new instance of %s %d' % (app.app_name, app)
    check = 0
    if window != None:
         print 'with window %d' % (window)
         check = 1
         set_window(current, window, app.app_name, app, alt_title)
    i_name = manager.new_instance(app, check)
    a_name = manager.app_name(i_name)
    if a_name != app.app_name:
        print 'Warning: app names %s and %s do not match' \
            % (app.app_name, a_name)
    a = manager.instances[i_name]
    if a != app:
        print 'Warning: AppStates %d and %d do not match' \
            % (app, a)
    return i_name

def new_universal_instance(manager, current, app, exclusive = 1):
    print 'new universal instance of %s %d' % (app.app_name, app)
    i_name = manager.new_universal_instance(app, exclusive)
    a_name = manager.app_name(i_name)
    if a_name != app.app_name:
        print 'Warning: app names %s and %s do not match' \
            % (app.app_name, a_name)
    a = manager.instances[i_name]
    if a != app:
        print 'Warning: AppStates %d and %d do not match' \
            % (app, a)
    return i_name

class FakeWindow(Object.Object):
    def __init__(self, handle, module, **args):
        self.deep_construct(FakeWindow,
                            {'handle': handle,
                             'module_name': module
                            },
                            args)
    def __int__(self):
        return self.handle
    def ID(self):
        return self.handle
    def module(self):
        return self.module_name

class FakeAppState(EdSim.EdSim):
# uses EdSim to handle buffer related stuff, for rsm_algorithm test,
# but overrides shared_window, multiple_window, is_active, title_string,
# so that we can pretend to be a variety of different types of editor
    def __init__(self, value, buff = None, shared = 0, 
            multi = 1, active = 1, title_control = 1, 
            safe_active = 1, **attrs):
        self.deep_construct(FakeAppState, 
                            {'value': value,
                             'the_title_string': '',
                             'shared_windows': shared,
                             'multi': multi,
                             'title_control': title_control,
                             'active': active,
                             'safe_active': safe_active
                            }, attrs)
        if buff != None:
            self.open_file(buff)
    def __str__(self):
        return str(self.value)
    def __int__(self):
        return self.value
    def shared_window(self):
        return self.shared_windows
    def multiple_windows(self):
        return self.multi
#    def name(self):
#        return self.buff
    def suspend(self):
        self.active = 0
    def resume(self):
        self.active = 1
    def is_active(self):
        return self.active
    def is_active_is_safe(self):
        return self.safe_active
    def set_instance_string(self, instance_string):
        self.the_instance_string = instance_string
        return self.title_control
    def instance_string(self):
        if self.title_control:
            return self.the_instance_string 
        return None
    def title_escape_sequence(self, a, b):
        return self.title_control

def old_test_am_dictionaries():
    manager = AppMgr.AppMgr()

    Emacs = FakeAppState(1, app_name = 'emacs')
    another_Emacs = FakeAppState(2, app_name = 'emacs')
    yet_another_Emacs = FakeAppState(4, app_name = 'emacs')
    shell_Emacs = FakeAppState(5, app_name = 'emacs')
    shell_Emacs2 = FakeAppState(6, app_name = 'emacs')
    Vim = FakeAppState(3, app_name = 'Vim')
    i = new_instance(manager, Emacs)
    manager_state(manager)
    print 'new window 14'
    manager.new_window(i, 14)
    print 'new window 20'
    manager.new_window(i, 20)
    manager_state(manager)

    j = new_instance(manager, another_Emacs, 10)
    manager_state(manager)

    k = new_instance(manager, 'Vim', Vim)
    print 'delete window 20'
    manager.delete_window(i, 20)
    manager_state(manager)

    print 'delete instance ' + j
    manager.delete_instance(j)
    l = new_instance(manager, 'Emacs', yet_another_Emacs, 7)
    manager_state(manager)
    print 'delete instance ' + i
    manager.delete_instance(i)
    manager_state(manager)
    print 'delete instance ' + k
    manager.delete_instance(k)
    print 'delete instance ' + l
    manager.delete_instance(l)
    manager_state(manager)

    m = new_instance(manager, 'Emacs (Exceed)', shell_Emacs,
        window = 94)
    n = new_instance(manager, 'Emacs (Exceed)', shell_Emacs2,
        window = 94)
    manager_state(manager)
    manager.delete_window(m, 94)
    manager_state(manager)
    manager.delete_instance(m)
    manager_state(manager)
    manager.delete_instance(n)
    manager_state(manager)

def test_am_dictionaries():
    g_factory = sr_grammars.WinGramFactoryDummy(silent = 1)
    GM_factory = GramMgr.WinGramMgrFactory(g_factory)
    current = RecogStartMgr.CurrWindowDummy()
    recog_mgr = RecogStartMgr.RSMExtInfo(GM_factory = GM_factory, 
      win_info = current)
    manager = AppMgr.AppMgr(recog_mgr)
    windows = {}
    mod_Emacs = KnownTargetModule.DedicatedModule(module_name = 'EMACS',
        editor = 'emacs')
    mod_Vim = KnownTargetModule.DedicatedModule(module_name = 'VIM',
        editor = 'Vim')
    mod_telnet = KnownTargetModule.RemoteShell(module_name = 'TELNET',
        title_varies = 1)
    manager.add_module(mod_Emacs)
    manager.add_module(mod_Vim)
    manager.add_module(mod_telnet)
    manager.add_prefix('emacs', 'Yak')
    manager.add_prefix('Vim', 'Oldie')

    Emacs = FakeAppState(1, 'a_file.py', app_name = 'emacs')
    another_Emacs = FakeAppState(2, 'poodle.C', app_name = 'emacs')
    yet_another_Emacs = FakeAppState(4, 'foo.bar', app_name = 'emacs')
    shell_Emacs = FakeAppState(5, 'bug.c', app_name = 'emacs', shared = 1, multi = 0)
    shell_Emacs2 = FakeAppState(6, 'dog.q', app_name = 'emacs', shared = 1, multi = 0)
    Vim = FakeAppState(3, 'tests_def.py', app_name = 'Vim')
    i = new_instance(manager, current, Emacs)
    manager_state(manager)
    print 'new window 14'
    windows[14] = FakeWindow(14, 'EMACS')
    set_window(current, windows[14], Emacs.app_name, Emacs)
    manager.new_window(i)
    print 'new window 20'
    manager.app_instance(i).buff = 'dogs.C'
    windows[20] = FakeWindow(20, 'EMACS')
    set_window(current, windows[20], Emacs.app_name, Emacs)
    manager.new_window(i)
    manager_state(manager)

    windows[10] = FakeWindow(10, 'EMACS')
    j = new_instance(manager, current, another_Emacs, windows[10])
    manager_state(manager)

    k = new_instance(manager, current, Vim)
    print 'delete window 20'
    manager.delete_window(i, 20)
    manager_state(manager)

    print 'delete instance ' + j
    manager.delete_instance(j)
    windows[7] = FakeWindow(7, 'EMACS')
    l = new_instance(manager, current, yet_another_Emacs, windows[7])
    manager_state(manager)
    print 'delete instance ' + i
    manager.delete_instance(i)
    manager_state(manager)
    print 'delete instance ' + k
    manager.delete_instance(k)
    print 'delete instance ' + l
    manager.delete_instance(l)
    manager_state(manager)
    windows[94] = FakeWindow(94, 'TELNET')

    m = new_instance(manager, current, shell_Emacs,
        window = windows[94])
    shell_Emacs.suspend()
    n = new_instance(manager, current, shell_Emacs2,
        window = windows[94])
    manager_state(manager)
    manager.delete_window(m, 94)
    manager_state(manager)
    manager.delete_instance(m)
    manager_state(manager)
    manager.delete_instance(n)
    manager_state(manager)

def test_rsm_algorithm(trust = 0):
    g_factory = sr_grammars.WinGramFactoryDummy(silent = 0)
    GM_factory = GramMgr.WinGramMgrFactory(g_factory)
    current = RecogStartMgr.CurrWindowDummy()
    recog_mgr = RecogStartMgr.RSMExtInfo(GM_factory = GM_factory, 
        trust_current_window = trust, win_info = current)
    manager = AppMgr.AppMgr(recog_mgr)
    windows = {}
    mod_Emacs = KnownTargetModule.DedicatedModule(module_name = 'EMACS',
        editor = 'emacs')
    mod_Vim = KnownTargetModule.DedicatedModule(module_name = 'VIM',
        editor = 'Vim')
    mod_telnet = KnownTargetModule.RemoteShell(module_name = 'TELNET',
        title_varies = 1)
    mod_exceed = \
        KnownTargetModule.DualModeDisplayByTitle(title_regex = '^Exceed$',
        module_name = 'EXCEED')
    manager.add_module(mod_Emacs)
    manager.add_module(mod_Vim)
    manager.add_module(mod_telnet)
    manager.add_module(mod_exceed)
    manager.add_prefix('emacs', 'Yak')
    manager.add_prefix('Vim', 'Oldie')
    manager.add_prefix('WaxEdit', 'Floor')

    fish_h_before = "void move(float x, y);"
    fish_h_after = "\n"
    fish_before = """/* This is a small test buffer for C */

void move(float x, y)
"""
    fish_after = """{
  move_horiz(x);
  move_vert(y)
  horiz_pos = 0;
  this_sym_is_unres = 0;
  this_sym_is_unres_too = 0;
  this_sym_has_an_other_abbrev = 0;
  f_name;
  f_name2();
  API_function(1);
  API_function(2);
}
"""

    fowl_before = """import sys

def something(value):
    print """
    fowl_after = """value

if __name__ == '__main__':
    something('nice')
"""

    dog_before = """#!/usr/local/bin/perl5


#
# Environment variables for voiceGrip 
#
$voiceGripHome = $ENV{'VGTWO'};
$voiceGripOS = $ENV{'VGOS'};
if ($voiceGripOS eq 'win') {
    $dirSep = "\\";
    $curDirCom = 'cd';
} else {
    $dirSep = """
    dog_after = """'/';
    $curDirCom = 'pwd';
};
"""


    Emacs = FakeAppState(1, 'a_file.py', app_name = 'emacs')
    another_Emacs = FakeAppState(2, 'poodle.C', app_name = 'emacs')
#    yet_another_Emacs = FakeAppState(4, 'foo.bar', app_name = 'emacs')
    shell_Emacs = FakeAppState(5, 'bug.c', app_name = 'emacs', shared = 1, multi = 0,
        title_control = 0)
    shell_Emacs2 = FakeAppState(6, 'dog.q', app_name = 'emacs', shared = 1, multi = 0,
        title_control = 0)
#    Vim = FakeAppState(3, 'tests_def.py')
    text_Emacs = FakeAppState(7, 'nothing.py', app_name = 'emacs', shared = 1, multi = 0,
        title_control = 0)
    text_Emacs2 = FakeAppState(8, 'pickle.dll', app_name = 'emacs', shared = 1, multi = 0,
        title_control = 0)
    xEmacs = FakeAppState(9, '.cshrc', app_name = 'emacs', shared = 0, multi = 1)
    text_Vim = FakeAppState(10, '', app_name = 'Vim', shared = 1, multi = 0, safe_active = 0)
    internal = FakeAppState(12, 'large_buff.py', app_name = 'WaxEdit', multi = 0)

    windows[14] = FakeWindow(14, 'EMACS')
    print 'new instance in window 14'
    e1 = new_instance(manager, current, Emacs, windows[14])
    instance_status(manager, e1)
    windows[20] = FakeWindow(20, 'EMACS')
    windows[50] = FakeWindow(50, 'BROWSEUI')
    print 'new window 20'
    set_window(current, windows[20], Emacs.app_name, Emacs)
    new_buffer_for_instance(Emacs, "fish.C", before = fish_before, 
        after = fish_after)
    instance_status(manager, e1)
    print 'starting recognition in ', repr(current.window_info())
    start_recog(manager, current)
    instance_status(manager, e1)

    set_window(current, windows[50], None, alt_title = 'D:\Projects')
    print 'starting recognition in ', repr(current.window_info())
    start_recog(manager, current)
    instance_status(manager, e1)

    windows[5] = FakeWindow(5, 'TELNET')
    windows[8] = FakeWindow(8, 'TELNET')
    print 'new instance in telnet window 5'
    se1 = new_instance(manager, current, shell_Emacs, 
        windows[5])
    instance_status(manager, se1)
    manager_state(manager)
    print 'now specifying window'
    if manager.specify_window(se1):
        print 'success'
    else:
        print 'failed'
    instance_status(manager, se1)

    set_window(current, windows[8], None, alt_title = 'ttssh - acappella')
    print 'starting recognition in ', repr(current.window_info())
    start_recog(manager, current)
    instance_status(manager, se1)
    
    set_window(current, windows[5], shell_Emacs.app_name, shell_Emacs, 
        alt_title = 'ttssh - acappella')
    print 'starting recognition in ', repr(current.window_info())
    start_recog(manager, current)
    instance_status(manager, se1)

    print 'suspending ', se1
    shell_Emacs.suspend()
    set_window(current, windows[5], None, alt_title = 'ttssh - acappella')
    print 'starting recognition in ', repr(current.window_info())
    start_recog(manager, current)
    instance_status(manager, se1)

    se2 = new_instance(manager, current, shell_Emacs2) 
    instance_status(manager, se2)
    instance_status(manager, se1)
    print 'now specifying window'
    if manager.specify_window(se2):
        print 'success'
    else:
        print 'failed'
    instance_status(manager, se2)
    instance_status(manager, se1)
    print 'starting recognition in ', repr(current.window_info())
    start_recog(manager, current)
    instance_status(manager, se1)
    instance_status(manager, se2)
    print 'suspending ', se2
    shell_Emacs2.suspend()

    print 'starting recognition in ', repr(current.window_info())
    start_recog(manager, current)
    instance_status(manager, se1)
    instance_status(manager, se2)

    print 'resuming ', se1
    shell_Emacs.resume()
    print 'starting recognition in ', repr(current.window_info())
    start_recog(manager, current)
    instance_status(manager, se1)
    instance_status(manager, se2)

    windows[15] = FakeWindow(15, 'EXCEED')
    print 'new Vim instance in exceed window 15'
    tv1 = new_instance(manager, current, text_Vim, 
        windows[15], alt_title = 'xterm - acappella')
    new_buffer_for_instance(text_Vim, "dog.pl", before = dog_before, 
        after = dog_after)
    instance_status(manager, tv1)
    manager_state(manager)
    print 'starting recognition in ', repr(current.window_info())
    start_recog(manager, current)
    instance_status(manager, tv1)

    print 'suspending ', tv1
    text_Vim.suspend()
    set_window(current, windows[15], None, alt_title = 'xterm - acappella')

    print 'starting recognition in ', repr(current.window_info())
    start_recog(manager, current)
    instance_status(manager, tv1)

    print 'new emacs instance in exceed window 15'
    te1 = new_instance(manager, current, text_Emacs, 
        windows[15], alt_title = 'xterm - acappella')
    instance_status(manager, te1)

    print 'starting recognition in ', repr(current.window_info())
    start_recog(manager, current)
    instance_status(manager, te1)

    print 'now specifying window'
    if manager.specify_window(te1):
        print 'success'
    else:
        print 'failed'
    instance_status(manager, te1)

    print 'starting recognition in ', repr(current.window_info())
    start_recog(manager, current)
    instance_status(manager, te1)

    print 'suspending ', te1
    text_Emacs.suspend()
    print 'starting recognition in ', repr(current.window_info())
    start_recog(manager, current)
    instance_status(manager, te1)

    print 'resuming ', tv1
    text_Vim.resume()
    set_window(current, windows[15], text_Vim.app_name, text_Vim,
        alt_title = 'xterm - acappella')
    print 'starting recognition in ', repr(current.window_info())
    start_recog(manager, current)
    instance_status(manager, tv1)

    windows[25] = FakeWindow(25, 'EXCEED')
    print 'new emacs instance in exceed window 25'
    xe1 = new_instance(manager, current, xEmacs, 
        windows[25])
    instance_status(manager, xe1)
    print 'starting recognition in ', repr(current.window_info())
    start_recog(manager, current)
    instance_status(manager, xe1)

    print 'app reports new window (is current)'
    windows[26] = FakeWindow(26, 'EXCEED')
    set_window(current, windows[26], xEmacs.app_name, xEmacs)
    print 'current is', repr(current.window_info())
    manager.new_window(xe1)
    instance_status(manager, xe1)

    print 'starting recognition in ', repr(current.window_info())
    start_recog(manager, current)
    instance_status(manager, xe1)

    text_Vim.suspend()
    set_window(current, windows[15], None, alt_title = 'xterm - acappella')
    print 'app reports new window (is not current)'
    print 'current is', repr(current.window_info())
    manager.new_window(xe1)
    instance_status(manager, xe1)
    instance_status(manager, tv1)

    windows[27] = FakeWindow(27, 'EXCEED')

    print 'but now it is'
    set_window(current, windows[27], xEmacs.app_name, xEmacs)
    print 'current is', repr(current.window_info())
    print 'starting recognition in ', repr(current.window_info())
    start_recog(manager, current)
    instance_status(manager, xe1)

    windows[99] = FakeWindow(99, 'PYTHON')
    ii1 = new_universal_instance(manager, current, internal)
    print 'now it is on WaxEdit'
    set_window(current, windows[99], internal.app_name, internal)
    print 'starting recognition in ', repr(current.window_info())
    start_recog(manager, current)
    instance_status(manager, ii1)

    print 'but now it is'
    set_window(current, windows[27], xEmacs.app_name, xEmacs)
    print 'current is', repr(current.window_info())
    print 'starting recognition in ', repr(current.window_info())
    start_recog(manager, current)
    instance_status(manager, xe1)
    instance_status(manager, ii1)
    manager.delete_instance(ii1)

    print 'and now the WaxEdit is gone'
    print 'current is', repr(current.window_info())
    print 'starting recognition in ', repr(current.window_info())
    start_recog(manager, current)
    instance_status(manager, xe1)

def test_rsm_algorithm_no_trust():
    test_rsm_algorithm(trust = 0)

def test_rsm_algorithm_trust():
    test_rsm_algorithm(trust = 1)

auto_test.add_test('am_dictionaries', test_am_dictionaries, 
    'Testing AppMgr dictionary management.')

auto_test.add_test('rsm_algorithm', test_rsm_algorithm_no_trust, 
    'Testing RecogStartMgr algorithm.')

auto_test.add_test('rsm_algorithm_trust', test_rsm_algorithm_trust, 
    'Testing RecogStartMgr algorithm.')

##############################################################################
# Testing WinGramMgr with dummy grammars
##############################################################################

def activate_for(manager, buffer, window):
    print 'activating buffer %s for window %d' % (buffer, window)
    manager.app.change_buffer(buffer)
    manager.app.print_buff_if_necessary()
    manager.activate(buffer, window)

def new_buffer(manager, buffer, window = None, before = "", after = ""):
    print 'new buffer %s' % (buffer)
    if window != None:
         print 'with window %d' % (window)
    manager.app.open_file(buffer)
    b = manager.app.find_buff(buffer)
    b.insert_indent(before, after)
    manager.new_buffer(buffer, window)

def new_window(manager, window):
    print 'new window %d' % (window) 
    manager.new_window(window)

def delete_window(manager, window):
    print 'delete window %d' % (window) 
    manager.delete_window(window)

def buffer_closed(manager, buffer):
    print 'close buffer %s' % (buffer) 
    manager.buffer_closed(buffer)

def test_gram_manager_flags(global_grammars = 0, exclusive = 0):
    fish_h_before = "void move(float x, y);"
    fish_h_after = "\n"
    fish_before = """/* This is a small test buffer for C */

void move(float x, y)
"""
    fish_after = """{
  move_horiz(x);
  move_vert(y)
  horiz_pos = 0;
  this_sym_is_unres = 0;
  this_sym_is_unres_too = 0;
  this_sym_has_an_other_abbrev = 0;
  f_name;
  f_name2();
  API_function(1);
  API_function(2);
}
"""

    fowl_before = """import sys

def something(value):
    print """
    fowl_after = """value

if __name__ == '__main__':
    something('nice')
"""

    dog_before = """#!/usr/local/bin/perl5


#
# Environment variables for voiceGrip 
#
$voiceGripHome = $ENV{'VGTWO'};
$voiceGripOS = $ENV{'VGOS'};
if ($voiceGripOS eq 'win') {
    $dirSep = "\\";
    $curDirCom = 'cd';
} else {
    $dirSep = """
    dog_after = """'/';
    $curDirCom = 'pwd';
};
"""

    factory = sr_grammars.WinGramFactoryDummy()
    app = EdSim.EdSim(multiple = 1, instance_reporting = 1)
    manager = GramMgr.WinGramMgr(factory, app = app, 
        instance_name = None, recog_mgr = None,
        global_grammars = global_grammars, exclusive = exclusive)
    w = 5
    w2 = 7
    new_buffer(manager, 'fish.C', w, fish_before, fish_after)
    new_buffer(manager, 'fowl.py', w, fowl_before, fowl_after)
    activate_for(manager, 'fish.C', w)
    new_window(manager, w2)
    new_buffer(manager, 'dog.pl', w2, dog_before, dog_after)
    new_buffer(manager, 'fish.h', w2, fish_h_before, fish_h_after)
    activate_for(manager, 'dog.pl', w2)
    activate_for(manager, 'fish.h', w2)
    activate_for(manager, 'fowl.py', w)
    app.close_buffer('fowl.py', -1)
    buffer_closed(manager, 'fowl.py')
    print 'deactivate all for window %d' % (w)
    manager.deactivate_all(w)
    delete_window(manager, w2)
    app.close_buffer('dog.pl', -1)
    buffer_closed(manager,  'dog.pl')
    activate_for(manager,'fish.C', w)
    print 'deactivate all'
    manager.deactivate_all()
    print 'close all buffers'
    app.close_all_buffers(-1)
    print 'cleanup app'
    app.cleanup()
    print 'cleanup manager'
    manager.cleanup()
    print 'test ending - expect dels of manager, app'

def test_gram_manager():
    test_gram_manager_flags()
    
def test_gram_manager_all_set():
    test_gram_manager_flags(1, 1)


auto_test.add_test('dummy_grammars', test_gram_manager, 
   'Testing WinGramMgr grammar management with dummy grammars.')
auto_test.add_test('dummy_grammars_global', test_gram_manager_all_set, 
   'Testing WinGramMgr grammar management with global, exclusive dummy grammars.')

##############################################################################
# Testing EdSim allocation and cleanup 
##############################################################################

def test_EdSim_alloc_cleanup():
    #
    # Create a command interpreter connected to the editor simulator
    #

    print '\n*** testing cleanup with single buffer EdSim\n'
#    natlink.natConnect()    
    editor = EdSim.EdSim(instance_reporting = 1)
    temp_config = temp_factory.new_config(editor = editor, skip_config = 1)
    del editor
#     a_mediator = MediatorObject.MediatorObject(app =
#        EdSim.EdSim(instance_reporting = 1),
#         interp=CmdInterp.CmdInterp())
    test_CmdInterp_mediator(temp_config)

    print '\n*** testing cleanup with multi-buffer EdSim\n'
#    natlink.natConnect()    
    editor = EdSim.EdSim(multiple = 1, instance_reporting = 1)
    temp_config = temp_factory.new_config(editor = editor, skip_config = 1)
    del editor
#     a_mediator = MediatorObject.MediatorObject(app =
#        EdSim.EdSim(multiple = 1, instance_reporting = 1),
#         interp=CmdInterp.CmdInterp())
    test_CmdInterp_mediator(temp_config)
    

auto_test.add_test('EdSim_alloc_cleanup', test_EdSim_alloc_cleanup, 
    'Testing EdSim allocation and cleanup.')

##############################################################################
# Testing basic correction features of ResMgr
##############################################################################
def check_stored_utterances(instance_name, expected):
    sys.stdout.flush()
    the_mediator = testing.mediator()
    n = the_mediator.stored_utterances(instance_name)
    if n == expected:
        print '\n%d stored utterances, as expected\n' %n
    else:
        print '\nWARNING: %d stored utterances (expected %d)' % (n, expected)

    recent = the_mediator.recent_dictation(instance_name)
    if expected == 0:
        if recent == None:
            print '\nrecent dictation is empty, as expected\n'
        else:
            msg = \
                '\nWARNING: %d recently dictated utterances (expected None)' \
                % len(recent)
            print msg
    else:
        n = 0
#        print 'recent is %s' % repr(recent)
        if recent != None:
            n = len(recent)
        if n != expected:
            msg = \
                '\nWARNING: %d recently dictated utterances (expected %d)' \
                % (n, expected)
            print msg
        else:
            print '\n%d recently dictated utterances, as expected\n' \
                % n
    sys.stdout.flush()
   
def check_recent(instance_name, expected_utterances, expected_status):
    sys.stdout.flush()
    the_mediator = testing.mediator()
    n = the_mediator.stored_utterances(instance_name)
    recent = the_mediator.recent_dictation(instance_name)
    expected = len(expected_utterances)
    n_compare = expected
    if n != expected:
        msg = '\nWARNING: check_recent found %d stored utterances\n' % n
        msg = msg +  '(expected %d)' % expected
        print msg
        n_compare = min(n, expected)
    for i in range(1, n_compare+1):
        expect = expected_utterances[-i]
#        expect = string.split(expected_utterances[-i])
        received = recent[-i][0].spoken_forms()
        status = recent[-i][2]
        if expect != received:
            print "\nWARNING: utterance %d doesn't match:\n" % i
            print "expected:\n"
            print expect
            print "received:\n"
            print received
        if expected_status[-i] != status:
            msg = "\nWARNING: status of utterance "
            msg = msg + "%d was %d (expected %d)" \
                % (i, status, expected_status[-i])
            print msg
    if n < expected:
        print '\nadditional utterances were expected:'
        for i in range(n_compare + 1, expected):
            print string.split(expected_utterances[-i])
    elif n > expected:
        print '\nextra utterances were received:'
        for i in range(n_compare + 1, n):
            received = recent[-i][0].spoken_forms()
            print received
    sys.stdout.flush()

def check_scratch_recent(instance_name, n = 1, should_fail = 0):
    print 'scratching %d\n' %n
    sys.stdout.flush()

    the_mediator = testing.mediator()
    scratched = the_mediator.scratch_recent(instance_name, n = n)
    msg = 'scratch %d ' % n
    if scratched == n:
        msg = msg + 'succeeded '
        if should_fail:
            msg = 'WARNING: ' +  msg + 'unexpectedly' 
        else:
            msg = msg + 'as expected'
    else:
        msg = msg + 'failed '
        if should_fail:
            msg = msg + 'as expected'
        else:
            msg = 'WARNING: ' +  msg + 'unexpectedly' 
    print msg

    sys.stdout.flush()
    return scratched

def test_reinterpret(instance_name, changed, user_input = None):
    the_mediator = testing.mediator()
    done = None
    try:
        if user_input:
            #
            # Create temporary user input file
            #
            old_stdin = sys.stdin
            temp_file_name = vc_globals.tmp + os.sep + 'user_input.dat'
            temp_file = open(temp_file_name, 'w')
#        print 'temp file opened for writing'
            sys.stdout.flush()
            temp_file.write(user_input)
            temp_file.close()
            temp_file = open(temp_file_name, 'r')
#        print 'temp file opened for reading'
            sys.stdout.flush()
            sys.stdin = temp_file

        done = the_mediator.reinterpret_recent(instance_name, changed)

    finally:
        if user_input:
            sys.stdin = old_stdin
            temp_file.close()
    return done


        
def reinterpret(instance_name, utterances, errors, user_input = None, 
    should_fail = 0):
    sys.stdout.flush()
    the_mediator = testing.mediator()
    n = the_mediator.stored_utterances(instance_name)
    recent = the_mediator.recent_dictation(instance_name)
    n_recent = 0
    if recent != None:
        n_recent = len(recent)

    earliest = max(errors.keys())
    if n < earliest:
        print "\ncan't correct error %d utterances ago" % earliest
        print "because stored_utterances only goes back %d\n" % n
        sys.stdout.flush()
        return 0
    if n_recent < earliest:
        print "\ncan't correct error %d utterances ago" % earliest
        print "because recent_dictation only goes back %d\n" % n_recent
        sys.stdout.flush()
        return 0
    okay = 1
    for i in errors.keys():
        if not the_mediator.can_reinterpret(instance_name, i):
            print "\ncan't correct error %d utterances ago" % i
            print "because can_reinterpret returned false\n" 
            sys.stdout.flush()
            okay = 0
    if not okay:
        return 0

    print 'detecting changes'
    sys.stdout.flush()
    changed = []
    changed_numbers = []
    for i, change in errors.items():
        print 'utterance %d: change = %s' % (i, repr(change))
        sys.stdout.flush()
        utterance = recent[-i][0]
        number = recent[-i][1]
        spoken = utterance.spoken_forms()
        wrong = 0
        for j in range(len(spoken)):
            try:
                replacement = change[spoken[j]]
                print 'word %s being replaced with %s' % (spoken[j], replacement)
                sys.stdout.flush()
                spoken[j] = replacement
                wrong = 1
            except KeyError:
                pass
        if wrong:
            changed.append(i)
            changed_numbers.append(number)
# set_spoken doesn't cause adaption
            print 'utterance %d was changed ' % i
            sys.stdout.flush()
            utterance.set_spoken(spoken)
#            utterances[-i] = string.join(utterance.spoken_forms())
            utterances[-i] = utterance.spoken_forms()
            print 'utterance %d was corrected' % i
            sys.stdout.flush()
    done = None
    if changed_numbers:
        print 'about to reinterpret'
        sys.stdout.flush()
        done = test_reinterpret(instance_name, changed_numbers, user_input = user_input)

    if done == None:
        if should_fail:
            print '\nreinterpretation failed, as expected\n'
        else:
            print '\nWARNING: reinterpretation failed unexpectedly\n'
        sys.stdout.flush()
        return 0
    if testing.correction_available() == 'basic':
        if done == range(max(changed), 0, -1):
            print '\nall utterances from %d to the present'% max(changed)
            print 'were reinterpreted, as expected\n'
            sys.stdout.flush()
            return 1
        else:
            print '\WARNING: only utterances ', done, 'were reinterpreted'
            print '(expected %d to the present)\n' % max(changed)
            sys.stdout.flush()
            return 0
    else:
        okay = 1
        for i in changed:
            if i not in done:
                print '\nWARNING: utterance %d was not reinterpreted\n'
                okay = 0
        for i in done:
            if i not in changed:
                print '\nWARNING: utterance %d was unexpectedly reinterpreted\n'
                okay = 0
        sys.stdout.flush()
        return okay

def test_basic_correction():
    testing.init_simulator_regression()
    instance_name = testing.editor()
    if instance_name == None:
        msg = '\n***Using old Mediator object: '
        msg = msg + 'unable to test correction features***\n'
        print msg
        return
    correction_available = testing.correction_available()
    if instance_name == None:
        msg = '\n***No correction available: '
        msg = msg + 'unable to test correction features***\n'
        print msg
        return
    commands.open_file('blah.py')

    the_mediator = testing.mediator()
    print '\n***Testing initial state***\n'

    check_stored_utterances(instance_name, expected = 0)

    print '\n***Some simple dictation***\n'

    utterances = []
    utterances.append(string.split('class clown inherits from student'))
    input = ['0\n0\n']
    status = [1]

    utterances.append(string.split('class body'))
    input.append('')
    status.append(1)

    utterances.append(string.split('define method popularity method body'))
    input.append('0\n')
    status.append(1)


    utterances.append(string.split('return 8'))
    input.append('')
    status.append(1)

    for i in range(len(utterances)):
        test_say(utterances[i], user_input = input[i])

    print '\n***Testing state***\n'

    check_stored_utterances(instance_name, expected = len(utterances))
    check_recent(instance_name, utterances, status)

    print '\n***Testing scratch that***\n'

    scratched = check_scratch_recent(instance_name)
    if scratched:
        del utterances[-scratched:]
        del input[-scratched:]
        del status[-scratched:]

    check_stored_utterances(instance_name, expected = len(utterances))
    check_recent(instance_name, utterances, status)

#    return
# inserted temporarily to help debug emacs

    print "\n***Moving cursor manually***\n"
    commands.goto_line(1)

    print '\n***Testing scratch that following manual move***\n'

    scratched = check_scratch_recent(instance_name)
    if scratched:
        del utterances[-scratched:]
        del input[-scratched:]
        del status[-scratched:]

    check_stored_utterances(instance_name, expected = len(utterances))
    check_recent(instance_name, utterances, status)

    utterances.append(string.split('define method grades method body return B.'))
    input.append('0\n2\n')
    status.append(1)

    test_say(utterances[-1], user_input = input[-1])

    check_stored_utterances(instance_name, expected = len(utterances))
    check_recent(instance_name, utterances, status)

    test_say(['select', 'clown'])
    editor = the_mediator.editors.app_instance(instance_name)
    buffer = editor.curr_buffer()

    print '\n***Manually changing text\n'

    buffer.insert('president')
    commands.show_buff()


    status = len(status)*[0]

    print '\n***Testing scratch that following manual change***\n'

    scratched = check_scratch_recent(instance_name, should_fail = 1)
    if scratched:
        del utterances[-scratched:]
        del input[-scratched:]
        del status[-scratched:]

    the_mediator.reset_results_mgr()
    editor = the_mediator.editors.app_instance(instance_name)
    editor.init_for_test(save=-1)

    commands.open_file('blahblah.py')


    utterances = []
    utterances.append(string.split('class cloud inherits from student'))
    input = ['0\n0\n']
    status = [1]

    utterances.append(string.split('class body'))
    input.append('')
    status.append(1)

    utterances.append(string.split('fine method popularity method body'))
    input.append('0\n')
    status.append(1)

    utterances.append(string.split('return 8'))
    input.append('')
    status.append(1)

    for i in range(len(utterances)):
        test_say(utterances[i], user_input = input[i])

    print '\n***Testing state***\n'

    check_stored_utterances(instance_name, expected = len(utterances))
    check_recent(instance_name, utterances, status)

    print '\n***Testing correction of recent utterance***\n'

    errors = {}
    errors[len(utterances)-2] = {'fine': 'define'}
    reinterpret(instance_name, utterances, errors, user_input = '0\n')


    print '\n***Testing state***\n'

    check_stored_utterances(instance_name, expected = len(utterances))
    check_recent(instance_name, utterances, status)

    print '\n***Testing correction of another recent utterance***\n'


    errors = {}
    errors[len(utterances)] = {'cloud': 'clown'}
    reinterpret(instance_name, utterances, errors, user_input = '0\n'*3)
  
    print '\n***Testing state***\n'

    check_stored_utterances(instance_name, expected = len(utterances))
    check_recent(instance_name, utterances, status)

    new_utterances = []
    new_utterances.append(string.split('new line'))
    new_input = ['']
    new_status = [1]

    new_utterances.append(['back indent'])
    new_input.append('')
    new_status.append(1)

    new_utterances.append(string.split('excess equals 0'))
    new_input.append('0\n')
    new_status.append(1)

    for i in range(len(new_utterances)):
        test_say(new_utterances[i], user_input = new_input[i])

    editor = the_mediator.editors.app_instance(instance_name)
    buffer = editor.curr_buffer()

    utterances.extend(new_utterances)
    input.extend(new_input)
    status.extend(new_status)

    print '\n***Manually changing text\n'

    pos = buffer.cur_pos()
    buffer.delete(range = (pos-4, pos))
    commands.show_buff()
    status = len(status)*[0]

    print '\n***Testing state***\n'

    check_stored_utterances(instance_name, expected = len(utterances))
    check_recent(instance_name, utterances, status)

    print '\n***Testing failed correction of a recent utterance***\n'

    errors = {}
    errors[0] = {'excess' : 'success'}
    reinterpret(instance_name, utterances, errors, should_fail = 1,
        user_input = '0\n'*10)

    print '\n***Fixing error manually***\n'

    pos = buffer.cur_pos()
    buffer.delete(range = (pos-6, pos))
    commands.show_buff()
    status = len(status)*[0]

    print '\n***Testing state***\n'

    check_stored_utterances(instance_name, expected = len(utterances))
    check_recent(instance_name, utterances, status)

    new_utterances = []
    new_utterances.append(string.split('excess equals 1 new line'))
    new_input = ['0\n']
    new_status = [1]

    new_utterances.append(['back indent'])
    new_input.append('')
    new_status.append(1)

    new_utterances.append(string.split('results at index 0 jump out equals 0'))
    new_input.append('0\n')
    new_status.append(1)


    for i in range(len(new_utterances)):
#        if new_utterances[i] == 'back indent':
#            test_say([new_utterances[i]], user_input = new_input[i])
#        else:
#            split = string.split(new_utterances[i])
#            test_say(split, user_input = new_input[i])
        test_say(new_utterances[i], user_input = new_input[i])

    utterances.extend(new_utterances)
    input.extend(new_input)
    status.extend(new_status)

    print '\n***Testing state***\n'

    check_stored_utterances(instance_name, expected = len(utterances))
    check_recent(instance_name, utterances, status)

    print '\n***Testing scratch that***\n'

    scratched = check_scratch_recent(instance_name)
    if scratched:
        del utterances[-scratched:]
        del input[-scratched:]
        del status[-scratched:]

    print '\n***Testing state***\n'

    check_stored_utterances(instance_name, expected = len(utterances))
    check_recent(instance_name, utterances, status)

    print '\n***Testing correction after scratch that***\n'

    errors = {}
    errors[2] = {'excess': 'access'}
    reinterpret(instance_name, utterances, errors, user_input = '0\n')
  
    print '\n***Testing state***\n'

    check_stored_utterances(instance_name, expected = len(utterances))
    check_recent(instance_name, utterances, status)


# Temporarily disable this failing test so I can continue working on Emacs client
# without interference
#

auto_test.add_test('basic_correction', test_basic_correction, 
    'Testing basic correction infrastructure with ResMgr.')

##############################################################################
# Testing set_text 
##############################################################################
def test_set_text():
    testing.init_simulator_regression()
    the_mediator = testing.mediator()
    instance_name = testing.editor()
    if instance_name: 
        editor = the_mediator.editors.app_instance(instance_name)
    else:
        editor = the_mediator.app
    commands.open_file(vc_globals.test_data + os.sep + 'small_buff.py')
    buffer = editor.curr_buffer()
    buffer.set_text('nothing left')
    editor.print_buff_if_necessary()
    buffer.set_text('almost ', start = 0, end = 0)
    editor.print_buff_if_necessary()
    buffer.set_text('body', start = 9, end = 14)
    editor.print_buff_if_necessary()


auto_test.add_test('set_text', test_set_text, 
    'Testing set_text.')
    
##############################################################################
# Insertion deletion commands
##############################################################################

def test_insert_delete_commands():
   testing.init_simulator_regression()
   commands.open_file('blah.py')
   test_say(['this', 'is', 'a', 'very', 'long', 'variable', 'name', 'but', 'never', 'mind'], user_input="1\n1\n1\n1\n1\n1\n1\n1\n1\n")
   test_say(['back space'])
   test_say(['2 times'])
   test_say(['back space 2'])   
   test_say(['back space 3'])
   test_say(['back space 4'])
   test_say(['back space 5'])
   mediator = testing.mediator()
   instance_name = testing.editor()
   if instance_name:
       editor = mediator.editor_instance(instance_name)
   else:
       editor = mediator.app
   editor.set_text('some additional text')
   test_say(['select', 'additional'])
   test_say(['back space'])
   editor.set_text('some additional text')
   test_say(['select', 'additional'])
   test_say(['back space 2'])

auto_test.add_test('insert_delete', test_insert_delete_commands, 'Testing insertion and deletion commands')


##############################################################################
# Testing interaction between user inputs and speech
##############################################################################

def test_mixed_kbd_and_voice_editing():
    testing.init_simulator_regression()
    commands = testing.namespace()['commands']    
    instance_name = testing.editor()
    if instance_name: 
        app = the_mediator.editors.app_instance(instance_name)
    else:
        app = the_mediator.app    

    test_cursor_moved_by_kbd(app, commands)
    test_selection_set_by_kbd(app, commands)
    test_search_for_typed_text(app, commands)
    test_select_typed_text_by_voice(app, commands)
   
def test_cursor_moved_by_kbd(app, commands):
   commands.open_file(edit_this_buff_py)
   app.curr_buffer().move_cursor_by_kbd('Right', 10)
   commands.say(['hello'], user_input="0\n")

def test_selection_set_by_kbd(app, commands):
   commands.open_file(edit_this_buff_py)
   app.curr_buffer().set_selection_by_kbd(1, 10)
   commands.say(['hello'], user_input="0\n")
   
def test_search_for_typed_text(app, commands):
   commands.open_file(edit_this_buff_py)
   commands.goto_line(2)
   app.curr_buffer().type_text(',')
   app.curr_buffer().move_cursor_by_kbd('Left', 2)
   commands.say(['next', 'comma'])
   
def test_select_typed_text_by_voice(app, commands):
   commands.open_file(edit_this_buff_py)
   commands.goto_line(2)
   app.curr_buffer().type_text('hello')   
   commands.say(['select', 'hello'])

#auto_test.add_test('mixed_mode_editing', test_mixed_kbd_and_voice_editing, 'Testing mixed mode (kbd + voice) editing')

##############################################################################
# Voice Commands for compiling symbols
##############################################################################

def test_compile_symbols():
   testing.init_simulator_regression()
   commands.open_file(small_buff_py)
   commands.clear_symbols()
   print "Before compiling symbols, symbols are:\n"
   commands.print_symbols()
   commands.say(['compile symbols'])
   print "After compiling symbols, symbols are:\n"
   commands.print_symbols()
   
auto_test.add_test('compile_symbols', test_compile_symbols, 'Testing voice command for compiling symbols')
    
    
##############################################################################
# Use this to create temporary tests
##############################################################################

def test_large_messages():
    testing.init_simulator_regression()
    commands.open_file('tmp.py')
    commands.app.set_text(generate_string_of_approx_length(1024))
    commands.app.print_buff()
    
    
def generate_string_of_approx_length(str_len):
   the_string = ""
   line_len = 1
   len_to_now = 0
   while len_to_now < str_len:
      the_string = "%s%s" % (the_string, line_len)
      len_to_now = len_to_now + 1
      line_len = line_len + 1
      if line_len >= 9:
         line_len = 1
         the_string = "%s\n" % the_string
         len_to_now = len_to_now + 1
   return the_string
      


auto_test.add_test('large_messages', test_large_messages, desc='Send a message that has more than 1024 character (length of a message chunk)')


    
    
##############################################################################
# Use this to create temporary tests
##############################################################################

def test_temporary():
   edit_file = vc_globals.test_data + os.sep + 'edit_this_buff.py'
   testing.init_simulator_regression()
   commands = testing.namespace()['commands']
   commands.open_file(edit_file)

#   commands.goto_line(4)
#   commands.say(['class', 'body'])

# here, it seems class body    
   commands.goto_line(20)
   commands.say(['class', 'dummy', 'class', 'body'], user_input="1\n")
   commands.say(['define', 'method', 'new', 'method', 'method', 'body', 'pass'], user_input="1\n")

    
auto_test.add_test('temp', test_temporary, desc='temporary test')


