"""Define a series of regression tests for VoiceCode"""

import CmdInterp, EdSim, MediatorObject, SymDict

##############################################################################
# Testing SymDict
##############################################################################

def compilation_test(a_mediator, source):
    """Does a compilation test on file *source*        
    """
    print '*** Compiling symbols from file: %s ***' % source
    a_mediator.interp.known_symbols.parse_symbols(source)
    print 'Parsed symbols are: '
    a_mediator.interp.known_symbols.print_symbols()
    print '\n\nUnresolved abbreviations are:'
    sorted_unresolved = a_mediator.interp.known_symbols.unresolved_abbreviations.keys()
    sorted_unresolved.sort()
    for an_abbreviation in sorted_unresolved:
        symbol_list = a_mediator.interp.known_symbols.unresolved_abbreviations[an_abbreviation].keys()
        print '\'%s\': appears in %s' % (an_abbreviation, str(symbol_list))
        
    print '\n*** End of compilation test ***\n'
        
        
def test_SymDict():
    """Self test for SymDict"""

    a_mediator = MediatorObject.MediatorObject(interp=CmdInterp.CmdInterp(on_app=EdSim.EdSim()))
    a_mediator.configure()
    
    compilation_test(a_mediator, vc_globals.test_data + os.sep + 'small_buff.c')
    compilation_test(a_mediator, vc_globals.test_data + os.sep + 'large_buff.py')

auto_test.add_test('SymDict', test_SymDict, desc='self-test for SymDict.py')


##############################################################################
# Testing CmdInterp
##############################################################################


def test_CmdInterp():    
    #
    # Create a command interpreter connected to the editor simulator
    #
    a_mediator = MediatorObject.MediatorObject(interp=CmdInterp.CmdInterp(on_app=EdSim.EdSim()))
    MediatorObject.to_configure = a_mediator
    acmd = CSCmd(spoken_forms=['for', 'for loop'], meanings=[[ContC(), c_simple_for], [ContPy(), py_simple_for]])
    MediatorObject.add_csc(acmd)
    acmd = CSCmd(spoken_forms=['loop body', 'goto body'], meanings=[[ContC(), c_goto_body], [ContPy(), py_goto_body]])
    MediatorObject.add_csc(acmd)

    
    a_mediator.interp.on_app.open_file(vc_globals.test_data + os.sep + 'small_buff.c')
    a_mediator.interp.on_app.goto(41)
    print '\n\n>>> Testing command interpreter\n\n'
    print '\n>>> Interpreting \'for loop index loop body\' in a C buffer'    
    print '\n>>> Current buffer is:\n'
    a_mediator.interp.on_app.print_buff_content()
    a_mediator.interp.interpret_NL_cmd('for loop index loop body')
    print '\n>>> Buffer is now:'
    a_mediator.interp.on_app.print_buff_content()
    

    a_mediator.interp.on_app.open_file(vc_globals.test_data + os.sep + 'small_buff.py')
    a_mediator.interp.on_app.goto(43)
    a_mediator.interp.on_app.curr_buffer.language = 'python'
    print '\n>>> Interpreting \'for loop index loop body\' in a Python buffer'    
    print '\n>>> Current buffer is:\n'
    a_mediator.interp.on_app.print_buff_content()
    a_mediator.interp.interpret_NL_cmd('for loop index loop body')
    print '\n>>> Buffer is now:'
    a_mediator.interp.on_app.print_buff_content()
        

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
    sim.print_buff_content()

    print "\n\n>>> Moving to position 5"
    sim.move_to(5)
    sim.print_buff_content()

    print "\n\n>>> Testing breadcrumbs"
    print "\n>>> Dropping one here"; sim.print_buff_content()
    sim.drop_breadcrumb()
    sim.move_to(10)
    sim.drop_breadcrumb()
    print "\n>>> Dropping one here"; sim.print_buff_content()    
    print "\n>>> Popping 2 crumbs -> end up here:"
    sim.pop_breadcrumbs(num=2)
    sim.print_buff_content()
    print "\n>>> Dropping one here"; sim.print_buff_content()    
    sim.drop_breadcrumb()
    sim.move_to(10)
    print "\n>>> Dropping one here"; sim.print_buff_content()    
    sim.drop_breadcrumb()
    sim.move_to(20)
    sim.print_buff_content()
    sim.pop_breadcrumbs()
    print "\n>>> Popping 1 crumb -> end up here..."    
    sim.print_buff_content()

    print '\n\n>>> Testing code indentation. Inserting for loop.'
    sim.goto(42)
    sim.insert_indent('for (ii=0; ii <= maxValue; ii++)\n{\n', '\n}\n')
    sim.print_buff_content()


auto_test.add_test('EdSim', test_EdSim, desc='self-test for EdSim.py')



