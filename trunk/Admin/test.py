"""Regression testing script"""

import os, natlink, posixpath
import auto_test, debug, EdSim, util

def usage():
    print """

Usage: python test.py -h -f fname [suite-name ...]
                      -d output1 output2
                      

OPTIONS
-------

-h       : print this help message

-f fname : evaluate the code in file fname before doing the tests. This is used
           mainly to define or import a list of tests

-d       : instead of doing tests, compare the outputs of two tests runs.
           Typically used to compare output of a test run done on a new
           (and possibly buggy) version of the system to output of a test run
           done on a bug-free (yeah, right ;-) version of the system.

ARGUMENTS
---------

suite-name : name of a test or test suite, or regexp to be matched against
             names of tests

output1, output2 :
             two test run ouput files to be compared
    """


if (__name__ == '__main__'):



    opts, args = util.gopt(('d', None, 'f', posixpath.expandvars('$VCODE_HOME' + os.sep + 'Admin' + os.sep + 'tests_def.py'), 'h', None))
    
    if (opts['h']):
        usage()
    elif (opts['d']):
        print "-d option not implemented yet.\n"
    else:
        execfile(opts['f'])
        auto_test.run(args)


    #
    # Loading VoiceDictation caused a connection to NatSpeak.
    # Need to disconnect otherwise the DOS window hangs up after script
    # terminates.
    #
    natlink.natDisconnect()
