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

"""Regression testing script"""

import os, natlink, posixpath, sys
import MediatorObject, sim_commands, sr_interface, vc_globals

sys.path = sys.path + [vc_globals.config, vc_globals.admin]

#
# Make sure we run tests without connecting to NatSpeak
#
# Must do this before importing other VoiceCode files because creation and
# initialisation of VoiceDictation may try to link with NatSpeak
#
# NOTE: This is commented out because it causes problems with say_select
#       Don't know why.
#
# os.environ['VCODE_NOSPEECH'] = '1'

import auto_test, util


def usage():
    print """

Usage: python test.py -h -f fname [suite-name ...] -s
                      -d output1 output2
                      

OPTIONS
-------

-h       : print this help message

-f fname : evaluate the code in file fname before doing the tests. This is used
           mainly to define or import a list of tests

-s       : when this option is 1, allows the user to switch to an other window
           while the regression test is running. If at some point a particular
           test requires that the regression test window be the active one,
           the user will be asked to make it so by a voice prompt.

           Default: 0

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
    config_file = vc_globals.config + os.sep + 'vc_config.py'
    try:
        execfile(config_file)        
    except Exception, err:
        print 'ERROR: in configuration file %s.\n' % config_file
        raise err
    
    opts, args = util.gopt(('d', None, 'f', posixpath.expandvars('$VCODE_HOME' + os.sep + 'Admin' + os.sep + 'tests_def.py'), 'h', None, 's', 0))

    if (opts['h']) or len(args) == 0:
        usage()
    elif (opts['d']):
        print "-d option not implemented yet.\n"
    else:
        util.may_switch_win_during_tests = int(opts['s'])
        execfile(opts['f'])
        try:
            sr_interface.connect('off')
        except natlink.UnknownName:
            print 'NatSpeak user \'%s\' not defined. \nDefine it and restart VoiceCode' % sr_interface.vc_user_name
        else:
            auto_test.run(args)
            

    #
    # Note: we call this instead of sim_commands.quit, because the
    #       regression tests carried out may not necessarily have created an
    #       instance for sim_commands.the_mediator.
    #
    MediatorObject.disconnect_from_sr(1, 0)


