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

"""Automated regression testing function.

This file contains functions for defining and running automated
regression tests.
"""

import re, sys, time
import profile
import util
from debug import trace

test_reg = {}
suite_reg = {'all': ['.*']}
suite_reg['highlights'] = ['automatic_abbreviations',
'mediator_console', 'python']
suite_reg['fabfour'] = ['SymDict', 'automatic_abbreviations',
'mediator_console', 'python']

suite_reg['upto'] = ['CmdInterp', 'EdSim', 'EdSim_alloc_cleanup', 'SymDict', 
'Object', 'Symdict', 'am_dictionaries', 'automatic_abbreviations']

suite_reg['mostupto'] = ['CmdInterp', 'EdSim', 'EdSim_alloc_cleanup', 
'SymDict', 'automatic_abbreviations']

suite_reg['threeupto'] = ['CmdInterp', 'EdSim', 
'SymDict', 'automatic_abbreviations']

suite_reg['twobefore'] = ['CmdInterp', 'EdSim', 
'automatic_abbreviations']

suite_reg['cibefore'] = ['CmdInterp', 'automatic_abbreviations']

suite_reg['edbefore'] = ['EdSim', 'automatic_abbreviations']
suite_reg['insdel'] = ['basic_correction', 'change_direction',
'compile_symbols', 'insert_delete']
suite_reg['insdel2'] = ['basic_correction', 'insert_delete']

test_header_fmt = '\n\n******************************************************************************\n* Test       : %s\n* Description : %s\n******************************************************************************\n\n'


def add_test(name, fct, desc="", order=0):
    """Add a test to the test registry.

    Adds a test with name *STR name* and function *FCT fct* to the
    tests registry. An optional description string *STR desc* can also
    be specified.

    WARNING: if *fct* uses *profile.run*, then this doesn't work. For
    some reason, *profile.run* seems to be running the code in the
    name space of *auto_test* instead of whatever module *fct* was
    defined in.
    """
    
    if (test_reg.has_key(name)):
        sys.stderr.write("WARNING: Test '%s' defined twice\n" % [name])
    else:
        test_reg[name] = [fct, desc, order]

def add_suite(name, *patterns):
    """Adds a new test suite to the registry.

    *STR name* is the name of the suite, *[STR] patterns* is the list of tests
    in the suite, where each entry is either the name of a test or a
    regexp to be matched against test names.
    """
    suite_reg[name] = patterns

def tests_names_by_priority_and_name(tests_to_do):
    test_priorities_and_names = []
    for a_test in tests_to_do.items():
       test_priorities_and_names.append((a_test[1][2], a_test[0]))
    test_priorities_and_names.sort()
    sorted_test_names = []
    for a_test_priority_and_name in test_priorities_and_names: 
      sorted_test_names.append((a_test_priority_and_name[1]))
    return sorted_test_names
    

def run(to_run, profile_prefix = None):
    """
    Runs a series of test suites.
    
    Runs all test suites defined in *[STR] to_run*. Each entry
    in *to_run*is either the name of a test or the name of a test suite, or a
    regexp to be matched against test names.

    If profile_prefix is specified, use the profile module to run each
    test, sending the outputs to a file
    profile_prefix + '.' + testname + '.dat'
    """
    trace('auto_test.run', '** to_run=%s' % repr(to_run))
    tests_to_do = {}
    for an_entry in to_run:
        test_suite = expand_suite(an_entry)
        tests_to_do = util.dict_merge(tests_to_do, test_suite)
        
    test_names = tests_names_by_priority_and_name(tests_to_do)

    start_time = time.time()
    end_time = start_time
    
    for a_test_name in test_names:
        [fct, desc, order] = tests_to_do[a_test_name]
        sys.stdout.write(test_header(a_test_name, desc))
        sys.stdout.flush()
        if profile_prefix is None:
            apply(fct)
        else:
            import __main__
            __main__.test_to_profile = fct
            outfile = profile_prefix + '.' + a_test_name + '.dat'
            profile.run('test_to_profile()', outfile)
        sys.stdout.flush()
#        print "-- auto_test.run: global_dicts[a_test_name]=%s" % global_dicts[a_test_name]
#        print "-- auto_test.run: local_dicts[a_test_name]=%s" % local_dicts[a_test_name]
#        exec(fct, global_dicts[a_test_name], local_dicts[a_test_name])

        end_time = time.time()
        
    elapsed_time = end_time - start_time     
    print '\n\n\n-----------------------------------------------'
    print 'Test suite completed in:  %s secs' % elapsed_time
    print '-----------------------------------------------'            


def expand_suite(suite_name):
    """Returns list of tests in a suite.
    
    *STR suite_name* may be the name of a test or the name of a test
    suite, or a regexp to be matched against test names.
    
    """

    test_suite = {}
    if (len(find_tests(suite_name)) > 0):
        #
        # suite_name is the name of an actual test
        #
        test_suite = find_tests(suite_name)
#        print "-- expand_suite: test_suite=%s" % test_suite
 
    elif (suite_reg.has_key(suite_name)):
        #
        # suite_name is the name of a suite to expand.
        #
        for an_entry in suite_reg[suite_name]:
#            print "-- expand_suite: an_entry=%s" % an_entry
            test_suite = util.dict_merge(test_suite, find_tests(an_entry))
    else:
        #
        # suite_name is a regexp to be matched against the names of tests
        #
        test_suite = find_tests(suite_name, is_regexp=1)

    if (len(test_suite) == 0):
        print "WARNING: no test or test suite matching '%s'" % suite_name
#    print "-- expand_suite: returning test_suite=%s" % test_suite
    return test_suite
            

def find_tests(name, is_regexp=None):
    """Find all tests matching a name or regexp.

    Returns a list of tests whose names match name or regexp *STR
    name*. Entries in the list are of the form *[STR name, FCT fct]*

    If *is_regexp* is false, then *name* is treated as an actual test name,
    otherwise it is treated as a regexp against which to match test names.

    Returns *None* if no tests were found.
    """
#    print "-- find_tests: name=%s, is_regexp=%s" % (name, is_regexp)
    found_tests = {}
    if (is_regexp or (not test_reg.has_key(name))):
        #
        # name is a regular expression to be matched against test names
        #
#        print "-- find_tests: trying as regexp"
        patt = '^' + name + '$'
        for an_entry in test_reg.items():        
            this_name, [fct, desc, order] = an_entry
            if (re.match(patt, this_name)):
#                print "-- find_tests: test %s matched %s" % (str(this_name), str(patt))
                found_tests[this_name] = [fct, desc, order]
        
    else:
        #
        # name is an actual test name
        #
#        print "-- find_tests: trying an actual test name"
        found_tests[name] = [test_reg[name][0], test_reg[name][1], test_reg[name][2]]
#    print ("-- find_tests: returns found_tests=%s" % found_tests)


    return found_tests


def test_header(name, desc):
    """Returns the header of a test
    
    ... with test name *STR test_name* and description *STR desc*.
    """
    return '\n\n' + ('*' * 79) + '\n* Name        : ' + name + '\n* Description : ' + desc + '\n' + ('*' * 79) + '\n\n'

if (__name__ == '__main__'):
    
    def a_test_1_1():
        print "This is a_test_1_1\n"
    add_test('a_test_1_1', a_test_1_1, 'This is the description of a_test_1_1')
    
    def a_test_1_2():
        print "This is a_test_1_2\n"
    add_test('a_test_1_2', a_test_1_2, 'This is the description of a_test_1_2')

    def a_test_1_3():
        print "This is a_test_1_3\n"
    add_test('a_test_1_3', a_test_1_3, 'This is the description of a_test_1_3')

    def a_test_2_1():
        print "This is a_test_2_1\n"
    add_test('a_test_2_1', a_test_2_1, 'This is the description of a_test_2_1')

    def a_test_2_2():
        print "This is a_test_2_2\n"
    add_test('a_test_2_2', a_test_2_2, 'This is the description of a_test_2_2')

    def a_test_3_3():
        print "This is a_test_3_3\n"
    add_test('a_test_3_3', a_test_3_3, 'This is the description of a_test_3_3')


    add_suite('a_suite', '.*_2_.*', '.*_.*_1', 'a_test_3_3')

    print 'Running a_test_1_1\n\n'
    run(['a_test_1_1'])

    print 'Running a_suite\n\n'
    run(['a_suite'])

    print 'Running [\'.*1_.*\', \'a_test_2_1\']'
    run(['.*1_.*', 'a_test_2_1'])

    print "Running 'non_existant'\n"
    run(['non_existant'])
    
