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

"""Define a series of regression tests for VoiceCode"""

import os, sys
import mediator, CmdInterp, EdSim, MediatorObject, Object, SymDict, test_pseudo_python


small_buff_c = vc_globals.test_data + os.sep + 'small_buff.c'    

##############################################################################
# Testing SymDict
##############################################################################

def compilation_test(a_mediator, source):
    
    """Does a compilation test on file *source*        
    """
    print '*** Compiling symbols from file: %s ***' % source
    a_mediator.interp.known_symbols.cleanup()
    a_mediator.interp.known_symbols.parse_symbols(source)
    print '\n\nParsed symbols are: '
    a_mediator.interp.known_symbols.print_symbols()
    print 'Unresolved abbreviations are:'
    sorted_unresolved = a_mediator.interp.known_symbols.unresolved_abbreviations.keys()
    sorted_unresolved.sort()
    for an_abbreviation in sorted_unresolved:
        symbol_list = a_mediator.interp.known_symbols.unresolved_abbreviations[an_abbreviation].keys()
        print '\'%s\': appears in %s' % (an_abbreviation, str(symbol_list))
        
    print '\n*** End of compilation test ***\n'


def accept_symbol_match_test(a_mediator, source, symbol_matches):
    """Does a test on SymDict.accept_symbol_match.
    """
    print '\n\n*** Accept symbol match test. source=\'%s\' ***' % source
    a_mediator.interp.known_symbols.cleanup()            
    a_mediator.interp.known_symbols.parse_symbols(source)
    print 'Parsed symbols are: '
    a_mediator.interp.known_symbols.print_symbols()
    print '\n\nUnresolved abbreviations are:'
    sorted_unresolved = a_mediator.interp.known_symbols.unresolved_abbreviations.keys()
    sorted_unresolved.sort()
    for an_abbreviation in sorted_unresolved:
        symbol_list = a_mediator.interp.known_symbols.unresolved_abbreviations[an_abbreviation].keys()
        print '\'%s\': appears in %s' % (an_abbreviation, str(symbol_list))

    sys.stdout.write('\n\nAccepting: ')
    for a_match in symbol_matches:
       sys.stdout.write('\'%s\' -> \'%s\', ' % (a_match.pseudo_symbol, a_match.native_symbol))
       a_mediator.interp.known_symbols.accept_symbol_match(a_match)
    sys.stdout.write('\n')
           

    print '\n\nAfter accepting those symbols, known symbols are:\n'
    a_mediator.interp.known_symbols.print_symbols()
    print '\n\nUnresolved abbreviations are:'
    sorted_unresolved = a_mediator.interp.known_symbols.unresolved_abbreviations.keys()
    sorted_unresolved.sort()
    for an_abbreviation in sorted_unresolved:
        symbol_list = a_mediator.interp.known_symbols.unresolved_abbreviations[an_abbreviation].keys()
        print '\'%s\': appears in %s' % (an_abbreviation, str(symbol_list))

        
    print '\n*** End of accept symbol match test ***\n'
    
        
def symbol_match_test(a_mediator, sources, pseudo_symbols):
        """Tests pseudo-symbol matching.
        
        **INPUTS**

        [MediatorObject] a_mediator -- [MediatorObject] instance to
        use for the test.
        
        *[STR]* sources -- List of source files to be compiled before
         doing the matches.
        
        *[STR]* pseudo_symbols -- List of pseudo-symbols to be matched.
        

        **OUTPUTS**
        
        *none* -- 
        """

        print '*** Pseudo symbol match test***\n   Source files are: %s\n   Symbols are: %s\n\n' % (sources, pseudo_symbols)

        #
        # Compile symbols
        #
        a_mediator.interp.known_symbols.cleanup()        
        for a_source in sources:
            a_mediator.interp.known_symbols.parse_symbols(a_source)
#        print '\n Known symbols are: \n'
#        a_mediator.interp.known_symbols.print_symbols()

        #
        # Match the symbols
        #
        for a_symbol in pseudo_symbols:
            matches = a_mediator.interp.known_symbols.match_pseudo_symbol(a_symbol)
            sys.stdout.write('\'%s\' matches: [' % a_symbol) 
            if matches:
                for a_match in matches:
                    sys.stdout.write('%s, ' % a_match.native_symbol)
            else: sys.stdout.write('[]')
            sys.stdout.write(']\n')

        print '\n*** End of Pseudo Symbol Match test ***'

        
def test_SymDict():
    """Self test for SymDict"""

    a_mediator = MediatorObject.MediatorObject(interp=CmdInterp.CmdInterp(on_app=EdSim.EdSim()))
    a_mediator.configure()
    
    compilation_test(a_mediator, vc_globals.test_data + os.sep + 'small_buff.c')
    compilation_test(a_mediator, vc_globals.test_data + os.sep + 'large_buff.py')
    pseudo_symbols = ['set attribute', 'expand variables', 'execute file', 'profile Constructor Large Object', 'profile construct large object', 'auto test']
    symbol_match_test(a_mediator, [vc_globals.test_data + os.sep + 'large_buff.py'], pseudo_symbols)

    a_match = SymDict.SymbolMatch(pseudo_symbol='this symbol is unresolved', native_symbol='this_sym_is_unres', words=['this', 'symbol', 'is', 'unresolved'], word_matches=['this', 'sym', 'is', 'unres'])    
    accept_symbol_match_test(a_mediator, vc_globals.test_data + os.sep + 'small_buff.c', [a_match])

    a_mediator.quit(save_speech_files=0, disconnect=0)    

auto_test.add_test('SymDict', test_SymDict, desc='self-test for SymDict.py')


##############################################################################
# Testing CmdInterp
##############################################################################


def test_CmdInterp():    
    #
    # Create a command interpreter connected to the editor simulator
    #
    natlink.natConnect()
    a_mediator = MediatorObject.MediatorObject(interp=CmdInterp.CmdInterp(on_app=EdSim.EdSim()))
    MediatorObject.to_configure = a_mediator
    acmd = CSCmd(spoken_forms=['for', 'for loop'], meanings={ContC(): c_simple_for, ContPy(): py_simple_for})
    MediatorObject.add_csc(acmd)
    acmd = CSCmd(spoken_forms=['loop body', 'goto body'], meanings={ContC(): c_goto_body, ContPy(): py_goto_body})
    MediatorObject.add_csc(acmd)

    
    a_mediator.interp.on_app.open_file(vc_globals.test_data + os.sep + 'small_buff.c')
    a_mediator.interp.on_app.goto(41)
    print '\n\n>>> Testing command interpreter\n\n'
    print '\n>>> Interpreting in a C buffer'    
    print '\n>>> Current buffer is:\n'
    a_mediator.interp.on_app.print_buff()
    old_stdin = util.stdin_read_from_string('1\n')

    #
    # Test if spoken form of CSC is recognised as a single SR vocabulary entry
    # e.g. 'for loop' recognised as: ['for loop\for loop']
    #
    print '>>> Interpreting: %s' % ['for loop', 'loop body']
    a_mediator.interp.interpret_NL_cmd(['for loop', 'loop body'])

    #
    # Test if spoken form of CSC is recognised as multiple vocabulary entries
    # e.g. 'for loop' recognised as ['for', 'loop']
    print '>>> Interpreting: %s' % ['for', 'loop', 'loop', 'body']
    a_mediator.interp.interpret_NL_cmd(['for', 'loop', 'loop', 'body'])                                       
    sys.stdin = old_stdin
    print '\n>>> Buffer is now:'
    a_mediator.interp.on_app.print_buff()
    

    a_mediator.interp.on_app.open_file(vc_globals.test_data + os.sep + 'small_buff.py')
    a_mediator.interp.on_app.goto(43)
    a_mediator.interp.on_app.curr_buffer().language = 'python'
    print '\n>>> Interpreting in a Python buffer'    
    print '\n>>> Current buffer is:\n'
    a_mediator.interp.on_app.print_buff()

    print '>>> Interpreting: %s' % ['for loop', 'loop body']
    a_mediator.interp.interpret_NL_cmd(['for loop', 'loop body'])
    print '\n>>> Buffer is now:'
    a_mediator.interp.on_app.print_buff()

    a_mediator.quit(save_speech_files=0, disconnect=0)    
        

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

    #
    # This raises an exception because we don't give a value for
    # compulsory argument name, which is inherited from Person.__init__
    #
    sys.stdout.write("Omitting an inherited compulsory argument\n   Employee1(salary='not enough') -> ")
    try:
        result = Employee1(salary='not enough')
        print 'Test failed! An exception should have been raised, but wasn\'t\n'
    except Object.BadConstrCall, mess:
        print 'Test OK. Correct exception was raised: \'%s\'' % mess

    result = MyPerson(name='Alain')
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
    
auto_test.add_test('no_sr_user', test_no_sr_user, desc='testing connect with inexistant SR user')

###############################################################################
# Testing mediator.py console
###############################################################################

def test_command(command):
    print '\n\n>>> Testing console command: %s\n' % command
    mediator.execute_command(command)

def test_say(utterance, user_input=None):
    print '\n\n>>> Testing console command: say(%s, user_input=\'%s\')' % (utterance, user_input)
    mediator.say(utterance, user_input)

def test_mediator_console():    
    mediator.init_simulator()
    test_command("""clear_symbols()    """)
    test_command("""open_file('D:/blah.c')""")
    file = vc_globals.test_data + os.sep + 'small_buff.c'
    mediator.print_abbreviations()    
    test_command("""compile_symbols(['""" + file + """'])""")
    test_say(['for', 'loop', 'horiz_pos\\horizontal position', 'loop', 'body'])
    test_command("""say(['select', 'horiz_pos\\horizontal position', '=\equals'])""")
    test_command("""quit(save_speech_files=0, disconnect=0)""")        


auto_test.add_test('mediator_console', test_mediator_console, desc='testing mediator console commands')


###############################################################################
# Testing Select Pseudocode console
###############################################################################


def test_select_pseudocode():
    mediator.init_simulator()
    test_command("""open_file('D:/blah.py')""")
    test_say(['index', 'equals', '0', 'new statement'], user_input='1\\n')
    test_say(['index', 'equals', '1', 'new statement'], user_input='1\\n')    
    test_say(['index', 'equals', '0', 'new statement'], user_input='1\\n')
    test_say(['index', 'equals', '1', 'new statement'], user_input='1\\n')        
    test_say(['index', 'equals', '0', 'new statement'], user_input='1\\n')

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
    test_say(['correct', 'index', '=\\equals', '0'])
    test_command("""goto_line(2)""")
    test_say(['correct next', 'index', '=\\equals', '0'])
    test_command("""goto_line(2)""")
    test_say(['correct previous', 'index', '=\\equals', '0'])

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
    test_command("""goto_line(1)""")
    test_say(['correct next', 'index', '=\\equals', '0'])
    test_say(['correct next', 'index', '=\\equals', '0'])
    test_command("""goto_line(6)""")
    test_say(['correct previous', 'index', '=\\equals', '0'])
    test_say(['correct previous', 'index', '=\\equals', '0'])
    
    #
    # Testing repeated selection in both directions
    #
    test_command("""goto_line(1)""")
    test_say(['select next', 'index', '=\\equals', '0'])
    test_say(['select next', 'index', '=\\equals', '0'])
    test_command("""goto_line(6)""")
    test_say(['select previous', 'index', '=\\equals', '0'])
    test_say(['select previous', 'index', '=\\equals', '0'])
    
    test_command("""quit(save_speech_files=0, disconnect=0)""")        


auto_test.add_test('select_pseudocode', test_select_pseudocode, desc='testing mediator console commands')



##############################################################################
# Testing automatic addition of abbreviations
##############################################################################

def test_auto_add_abbrevs():
    mediator.init_simulator()
    test_command("""open_file('D:/blah.c')""")
    file = vc_globals.test_data + os.sep + 'small_buff.c'    
    test_command("""compile_symbols(['""" + file + """'])""")
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
    mediator.init_simulator(symdict_pickle_fname=fname)

    #
    # Compile symbols
    #
    test_command("""compile_symbols(['""" + vc_globals.test_data + os.sep + """small_buff.c'])""")

    #
    # Restart the mediator, with saved SymDict. The symbols should still be
    # there
    #
    print '\n\n>>> Restarting mediator with persistence. Compiled symbols should still be in the dictionary.\n'
    test_command("""quit(save_speech_files=0, disconnect=0)""")
    mediator.init_simulator(symdict_pickle_fname=fname)
    test_command("""print_symbols()""")

    #
    # Restart the mediator without saved SymDict. The symbols should not be
    # there anymore.
    #
    print '\n\n>>> Restarting mediator WITHOUT persistence. There should be NO symbols in the dictionary.\n'
    test_command("""quit(save_speech_files=0, disconnect=0)""")
    mediator.init_simulator(symdict_pickle_fname=None)
    test_command("""print_symbols()""")
    test_command("""quit(save_speech_files=0, disconnect=0)""")        
    

auto_test.add_test('persistence', test_persistence, desc='testing persistence between VoiceCode sessions')    


##############################################################################
# Testing redundant translation of LSAs and symbols
##############################################################################

def test_redundant_translation():
    global small_buff_c
    
    mediator.init_simulator()    
    test_command("""open_file('blah.c')""")
    test_command("""compile_symbols(['""" + small_buff_c + """'])""")
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
    mediator.init_simulator()
    mediator.open_file('blah.py')

    mediator.say(['variable', ' \\blank space', ' = \\equals', ' \\space bar', 'index', '*\\asterisk', '2', '**\\double asterisk', '8', '\n\\newline'], user_input='1\n2\n1\n1\n1\n1\n1\n', echo_utterance=1)

    mediator.say(['variable', ' = \\equals', 'variable', '/\\slash', '2', '+\\plus sign', '1', '-\\minus sign', 'index', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['variable', ' = \\equals', 'index', '%\\percent', '2', ' + \\plus', 'index', '%\\percent sign', '3', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['if', 'index', '&\\and percent', 'variable', 'then'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['if', 'index', '|\\pipe', 'variable', '|\\pipe sign', 'index', '|\\vertical bar', 'value', 'then'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['index', ' = \\equals', '0', ';\\semicolon', 'variable', ' = \\equals', '0', ';\\semi', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['index', '.\\dot', 'function', '()\\without arguments', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['variable', ' = \\equals', 'new', 'list', '0', '...\\ellipsis', '10', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['#\\pound', '!\\bang', 'python', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['#\\pound sign', '!\\exclamation mark', 'python', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['if', '~\\tilde', 'index', 'and', '~\\squiggle', 'variable', 'then'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['variable', '::\\double colon', 'index', '::\\colon colon', 'field', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['if', 'index', '<\\less sign', '0', ' and \\and', 'index', '>\\greater sign', '-\\minus sign', '1', 'then'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    

    mediator.say(['index', '=\\equal sign', '0', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['function', '(\\open paren', '0', ')\\close paren', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['function', 'parens', '0', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['function', '()\\empty parens', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['list', '[\\open bracket', '0', ']\\close bracket', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['list', 'brackets', '0', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['list', '[]\\empty brackets', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    


## BUG: causes recognitionMimic error    
##    mediator.say(['dictionary', '{\\open brace', '0', '}\\close brace', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['dictionary', 'braces', '0', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

## BUG: causes recognitionMimic error
##    mediator.say(['dictionary', '{}\\empty braces', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['<\\open angled', 'head', '>\\close angled', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['angled brackets', 'head', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['<>\\empty angled', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    
    mediator.say(['string', ' = \\equals', '\'\\open single quote', 'message', '\'\\close single quote', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['string', ' = \\equals', 'single', 'quotes', 'message', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['\'\'\\empty single quotes', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['string', ' = \\equals', '\"\\open quote', 'message', '\"\\close quote', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['string', ' = \\equals', 'quotes', 'message', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['""\\empty quotes', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['string', ' = \\equals', '`\\open back quote', 'message', '`\\close back quote', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['string', ' = \\equals', 'back', 'quotes', 'message', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['``\\empty back quotes', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    mediator.say(['\\a\\back slash a.', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\a\\back slash alpha', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\b\\back slash b.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\b\\back slash bravo'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\c\\back slash c.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\c\\back slash charlie'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\d\\back slash d.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\d\\back slash delta'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\e\\back slash e.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\e\\back slash echo'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\f\\back slash f.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\f\\back slash foxtrot'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\g\\back slash g.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\g\\back slash golf'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\h\\back slash h.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\h\\back slash hotel'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\i\\back slash i.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\i\\back slash india'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\j\\back slash j.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\j\\back slash juliett'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\k\\back slash k.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\k\\back slash kilo'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\l\\back slash l.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\l\\back slash lima'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\m\\back slash m.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\m\\back slash mike'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\n\\back slash n.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\n\\back slash november'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\o\\back slash o.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\o\\back slash oscar'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\p\\back slash p.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\p\\back slash papa'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\q\\back slash q.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\q\\back slash quebec'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\r\\back slash r.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\r\\back slash romeo'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\s\\back slash s.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\s\\back slash sierra'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\t\\back slash t.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\t\\back slash tango'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\u\\back slash u.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\u\\back slash uniform'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\v\\back slash v.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\v\\back slash victor'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\w\\back slash w.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\w\\back slash whiskey'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\x\\back slash x.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\x\\back slash xray'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\y\\back slash y.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\y\\back slash yankee'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\z\\back slash z.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\z\\back slash zulu'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\A\\back slash cap a.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\A\\back slash cap alpha', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\B\\back slash cap b.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\B\\back slash cap bravo', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#BUG:    mediator.say(['quotes', '\\C\\back slash cap c.', '\\C\\back slash cap charlie', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\D\\back slash cap d.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\D\\back slash cap delta', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\E\\back slash cap e.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\E\\back slash cap echo', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\F\\back slash cap f.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\F\\back slash cap foxtrot', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\G\\back slash cap g.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\G\\back slash cap golf', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\H\\back slash cap h.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\H\\back slash cap hotel', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\I\\back slash cap i.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\I\\back slash cap india', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\J\\back slash cap j.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\J\\back slash cap juliett', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\K\\back slash cap k.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\K\\back slash cap kilo', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\L\\back slash cap l.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\L\\back slash cap lima', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\M\\back slash cap m.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\M\\back slash cap mike', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\N\\back slash cap n.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\N\\back slash cap november', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\O\\back slash cap o.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\O\\back slash cap oscar', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\P\\back slash cap p.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\P\\back slash cap papa', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\Q\\back slash cap q.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\Q\\back slash cap quebec', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\R\\back slash cap r.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\R\\back slash cap romeo', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\S\\back slash cap s.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\S\\back slash cap sierra', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\T\\back slash cap t.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\T\\back slash cap tango', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\U\\back slash cap u.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\U\\back slash cap uniform', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\V\\back slash cap v.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\V\\back slash cap victor', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\W\\back slash cap w.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\W\\back slash cap whiskey', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\X\\back slash cap x.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\X\\back slash cap xray', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\Y\\back slash cap y.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\Y\\back slash cap yankee', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\Z\\back slash cap z.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['\\Z\\back slash cap zulu', 'new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    
    mediator.say(['index', 'semi', 'variable', 'semi'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['previous semi', 'previous semi'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['after semi'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['before previous semi'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['after semi'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#OK up to here            
    mediator.say(['before semi'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['variable', ' = \\equals', 'brackets', '0', ',\\comma', '1', ',\\comma', '3'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['previous', 'previous comma'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['after comma'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before previous comma'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before next comma'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['variable', '.\\dot', 'field', '.\\dot', 'value'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['previous dot', 'previous dot'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['after dot'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before previous dot'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before next dot'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['braces', 'variable', ': \\colon', '0', 'value', ': \\colon', '0'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['previous colon', 'previous colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['after colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before previous colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before next colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['variable', ' = \\equals', '2', '*\\asterisk', '3', '*\\asterisk', '4'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['previous asterisk', 'previous star'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['after star'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before previous asterisk'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before next star'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['variable', ' = \\equals', '2', '/\\slash', '3', '/\\slash', '4'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['previous slash', 'previous slash'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['after slash'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before previous slash'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before next slash'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['variable', ' = \\equals', '2', ' + \\plus', '3', ' + \\plus', '4'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['previous plus', 'previous plus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['after plus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before previous plus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before next plus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['variable', ' = \\equals', '2', ' - \\minus', '3', ' - \\minus', '4'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['previous minus', 'previous minus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['after minus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before previous minus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before next minus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['variable', ' = \\equals', '2', ' % \\modulo', '3', ' % \\modulo', '4'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['previous percent', 'previous percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['after percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before previous percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before next percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['0', '&\\and percent', '1', '&\\and percent', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['previous and percent', 'previous and percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['after and percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before previous and percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before next and percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['0', '|\\pipe', '1', '|\\pipe', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['previous pipe', 'previous pipe'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['after pipe'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before previous pipe'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before next pipe'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['0', '...\\ellipsis', '1', '...\\ellipsis', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['previous ellipsis', 'previous ellipsis'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['after ellipsis'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before previous ellipsis'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before next ellipsis'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['0', '!\\bang', '1', '!\\bang', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['previous bang', 'previous bang'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['after bang'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before previous bang'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before next bang'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['0', '?\\question mark', '1', '?\\question mark', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['previous question mark', 'previous question mark'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['after question mark'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before previous question mark'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before next question mark'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['0', '#\\pound', 'sign', '1', '#\\pound', 'sign', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['previous pound sign', 'previous pound sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['after pound sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before previous pound sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before next pound sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['0', '::\\double colon', '1', '::\\double colon', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['previous double colon', 'previous double colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['after double colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before previous double colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before next double colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['0', '~\\tilde', '1', '~\\tilde', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['previous tilde', 'previous tilde'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['after tilde'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before previous tilde'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before next tilde'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['0', '<\\less sign', '1', '<\\less sign', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['previous less sign', 'previous less sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['after less sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before previous less sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before next less sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['0', '>\\greater sign', '1', '>\\greater sign', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['previous greater sign', 'previous greater sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['after greater sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before previous greater sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before next greater sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['0', '=\\equal sign', '1', '=\\equal sign', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['previous equal sign', 'previous equal sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['after equal sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before previous equal sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['before next equal sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.say(['between parens', '1'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['before previous paren'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    mediator.say(['after paren'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['before paren'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['previous paren'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    mediator.say(['out of parens'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['before previous paren'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    mediator.say(['back out of parens'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['between brackets', '1'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['before previous bracket'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    mediator.say(['after bracket'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['before bracket'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['previous bracket'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['out of brackets'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['before previous bracket'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    mediator.say(['back out of brackets'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['between braces', '1'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['before previous brace'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    mediator.say(['after brace'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['before brace'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['previous brace'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    mediator.say(['out of braces'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['before previous brace'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    mediator.say(['back out of braces'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n', echo_utterance=1)


    mediator.say(['between angled', '1'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['before previous angled'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    mediator.say(['after angled'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['before angled'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['previous angled'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    mediator.say(['out of angled'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['before previous angled'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    mediator.say(['back out of angled'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['between single quotes', '1'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['before previous single quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    mediator.say(['after single quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['before single quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['previous single quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    mediator.say(['out of single quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['before previous single quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    mediator.say(['back out of single quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['between quotes', '1'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['before previous quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    mediator.say(['after quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['before quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['previous quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    mediator.say(['out of quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['before previous quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    mediator.say(['back out of quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n', echo_utterance=1)

    mediator.say(['between back quotes', '1'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['before previous back quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    mediator.say(['after back quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['before back quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['previous back quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    mediator.say(['out of back quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['before previous back quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    mediator.say(['back out of back quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    mediator.say(['new statement'], user_input='2\n2\n2\n2\n', echo_utterance=1)

    mediator.quit(save_speech_files=0, disconnect=0)    

auto_test.add_test('punctuation', test_punctuation, 'testing the various Python CSCs and LSAs')



##############################################################################
# Testing the various Python CSCs and LSAs
##############################################################################
auto_test.add_test('python', test_pseudo_python.run, 'testing the various Python CSCs and LSAs')


##############################################################################
# Testing repetition of last commands
##############################################################################


def test_repeat_last():
    mediator.init_simulator()    
    file_name = vc_globals.test_data + os.sep + 'large_buff.py'
    test_command("""open_file('""" + file_name + """')""")
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
    mediator.init_simulator()    
    file_name = vc_globals.test_data + os.sep + 'large_buff.py'
    test_command("""open_file('""" + file_name + """')""")
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
    mediator.init_simulator()

    test_command("""open_file('blah.py')""")

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


