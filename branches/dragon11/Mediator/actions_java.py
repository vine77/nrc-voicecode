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

"""Action functions for java language """

from actions_gen import Action, ActionInsert,ActionSearch, ActionInsertNewClause



java_function_definition = \
    ActionInsert(code_bef='',
                 code_after='(){\n\t\n}',
                 docstring = """Types template code for a java function (including body)""")

java_function_declaration = java_function_definition

# this assumes the if ends with a '}' (not a one-liner)
java_else_if = \
                ActionInsertNewClause(end_of_clause_regexp='\}', 
                                      where = 1, direction = 1,
                                      add_lines = 1,
                                      code_bef='\nelse if (', code_after='){\n\t\n}',
                                      back_indent_by=0,
                                      docstring='else-if clause of a Java conditional')

java_class_body = \
    ActionSearch(regexp=r'\{\s*',
                 docstring="""Moves cursor to the body of a class""")

java_class_definition = \
    ActionInsert(code_bef='class ',
                 code_after='\r\t{\n\t\n}',
                 docstring = """Insert template code for a Java class""",
                 expect="class")
#   ActionInsert(code_bef='class ',
#                  code_after='{\n\t\n}',
#                  docstring = """Insert template code for a Java class""",
#                  expect="class")


java_interface_definition= \
    ActionInsert(code_bef='interface ',
                 code_after='\r\t{\n\t\n}',
                 docstring = """Insert template code for a Java interface""",
                 expect="interface")

java_subclass = \
    ActionInsert(code_bef=' extends ', code_after='',
                 docstring = """Subclass definition""", expect='class')

