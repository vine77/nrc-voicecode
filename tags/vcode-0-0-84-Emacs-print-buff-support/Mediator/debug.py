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

import exceptions, sys, traceback, types

"""Functions for debugging purposes."""

def not_implemented(name):
    """Prints warning message when a stub function is called."""
    print "WARNING: stub function %s is not implemented yet!!!" % name

def virtual(name):
    """Prints warning message when a virtual method is called."""
    print "WARNING: virtual method '%s' called!!!" % name    


def print_call_stack(print_to_file=sys.stdout):
    """Prints the call stack.

    This is done by raising an exception, catching it and printing the
    traceback object. In Python 2, there is a more direct way of doing this.
    """
    try:
        raise exceptions.Exception()
    except exceptions.Exception, err:        
        traceback.print_stack(file=print_to_file)


def what_class(instance):
    """Returns a string describing the class of an instance.

    It works with any Python class or Python standard data types (int, float,
    string, etc.), but not with extension classes."""

    is_class = 'unknown'
    try:
        tmp = instance.__class__
        is_class = tmp
    except exceptions.AttributeError:
        #
        # The instance is not a python class. Maybe one of the
        # standard python data types?
        #
        is_class = type(instance)

    return is_class
