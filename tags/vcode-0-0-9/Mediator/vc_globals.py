"""Various global functions and constants relevant to VoiceCode

The following variables are defined in this module

*STR* home -- path of the home directory for VoiceCode (*VCODE_HOME* environment variable(

*STR* data -- path of the data directory

*STR* test_data -- path of the test data directory

*STR* config -- path of the configuartion directory

"""

import os

#
# Various directories
#
home = os.environ['VCODE_HOME']
data = home + os.sep + 'Data'
doc = home + os.sep + 'Doc'
doc_modules = doc + os.sep + 'Modules'
state = data + os.sep + 'State'
tmp = data + os.sep + 'Tmp'
test_data = data + os.sep + 'TestData'
config = home + os.sep + 'Config'
default_config_file = config + os.sep + 'vc_config.py'
