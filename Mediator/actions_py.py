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

"""Action functions for Python language"""

import re
import SymDict
from actions_gen import Action, ActionInsert, ActionSearch, ActionInsertNewClause


py_empty_dictionary = ActionInsert(code_bef='{}', code_after='',
                                   docstring="""Types code for an empty Python dictionary (e.g. {}^)""")

py_simple_for = ActionInsert(code_bef='for ', code_after=':\n\t',
                             docstring="""Insert template code for a simple Python for loop""")

py_goto_body = \
    ActionSearch(regexp=':[ \t]*(\n|$)[ \t]*',
                 docstring="""Move cursor to the body of a Python compound statement""")

py_new_statement = \
    ActionInsertNewClause(end_of_clause_regexp='(\n|$)', add_lines = 1, 
                          code_bef='', code_after='',
                           back_indent_by=0,
                           docstring = """Inserts a new line below current one""")

py_class_definition = \
    ActionInsert(code_bef='class ', code_after=':\n\t',
                 docstring="""Inserts template code for a Python class""")

py_class_body = \
    ActionSearch(regexp=':\\s*',
                 docstring="""Moves cursor to the body of a class""")

py_method_declaration = \
    ActionInsert(code_bef='def ', code_after='(self):\n\t',
                 docstring="""Types template code for a method""")

class ActionPyAddArgument(Action):
    """Positions the cursor to add arguments to a Python function call or
    definition"""
    
    def __init__(self, **args_super):
        self.deep_construct(ActionPyAddArgument, \
                            {}, \
                            args_super, \
                            {})

    def execute(self, app, cont):
        """See [Action.execute].
        
        .. [Action.execute] file:///./actions_gen.Action.html#execute"""
        

        found = app.search_for('\\)\s*:{0,1}', where=-1)
        if found:
            #
            # See if argument list was empty
            #        
            arg_list_empty = 1
            pos = app.curr_buffer().cur_pos() - 1
            
            #
            # Find first preceding non-space character
            #
            while pos >= 0:
                if not re.match('\s', app.curr_buffer().contents()[pos]):
                    #
                    # The first preceding non-space character is (
                    #    => argument list is empty
                    #
                    arg_list_empty = app.curr_buffer().contents()[pos] == '('
                    break
                pos = pos - 1

            #
            # Insert comma if this is not the first argument in the list
            #
            if not arg_list_empty:
                app.insert_indent(', ', '')

py_function_add_argument = \
    ActionPyAddArgument()

py_function_body = \
    ActionSearch(regexp=':\s*',
                 docstring="""Moves cursor to the body of a Python method or function""")
