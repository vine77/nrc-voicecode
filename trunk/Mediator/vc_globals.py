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
admin = home + os.sep + 'Admin'
config = home + os.sep + 'Config'
data = home + os.sep + 'Data'
doc = home + os.sep + 'Doc'
doc_modules = doc + os.sep + 'Modules'
state = data + os.sep + 'State'
tmp = data + os.sep + 'Tmp'
test_data = data + os.sep + 'TestData'
default_config_file = config + os.sep + 'vc_config.py'
