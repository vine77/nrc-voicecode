"""Various global functions and constants relevant to VoiceCode

The following variables are defined in this module

*STR* home -- path of the home directory for VoiceCode (*VCODE_HOME* environment variable(

*STR* data -- path of the data directory

*STR* test_data -- path of the test data directory

*STR* config -- path of the configuartion directory

[CmdInterp] interp -- the VoiceCode command interpreter (NOTE: because *CmdInterp.py* imports *vc_globals.py*, this variable is initialised in *CmdInterp.py* to avoid circular reference)

.. [CmdInterp] file:///./CmdInterp.CmdInterp

"""

import os
import CmdInterp

#
# Various directories
#
home = os.environ['VCODE_HOME']
data = home + os.sep + 'Data'
test_data = data + os.sep + 'TestData'
config = home + os.sep + 'Config'


