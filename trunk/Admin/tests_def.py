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
    a_mediator.interp.on_app.curr_buffer.language = 'python'
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
    test_command("""say_select(['select', 'horiz_pos\\horizontal position', '=\equals'])""")
    test_command("""quit(save_speech_files=0, disconnect=0)""")        


auto_test.add_test('mediator_console', test_mediator_console, desc='testing mediator console commands')


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
# Testing the various Python CSCs and LSAs
##############################################################################
auto_test.add_test('python', test_pseudo_python.run, 'testing the various Python CSCs and LSAs')

