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
# Copyright 2008 Taraz Buck
#
# Modified:
# 2008-08-15 18:20: File added, modified from "actions_C_Cpp.py". Still needs
# better function definition and new statements to match Matlab's.
# 2008-10-07 04:50: else and elseif changed to insert after newlines instead
# of after end statements.
#
##############################################################################


"""Action functions for Matlab language """

from actions_gen import Action, ActionInsert, ActionSearch, ActionInsertNewClause, ActionTypeText, ActionCompound

#import whrandom
import string
import debug, sys


class ActionMAddArgument(Action):
    """Positions the cursor to add arguments to a Matlab function call or
    definition"""
    
    def __init__(self, **args_super):
        self.deep_construct(ActionMAddArgument, \
                            {}, \
                            args_super, \
                            {})

    def execute(self, app, cont, state = None):
        """See [Action.execute].
        
        .. [Action.execute] file:///./actions_gen.Action.html#execute"""
        

        found = app.search_for(r'\)', where=-1, unlogged = 1)
        if found:
            #
            # See if argument list was empty
            #        
            arg_list_empty = 0
            
            #
            # Find first preceding non-space character
            #
            buff = app.curr_buffer()
            pos = buff.char_search(r'\S', direction = -1)
            if buff.contents()[pos] == '(':
                arg_list_empty = 1
            buff.goto(pos+1)

            #
            # Insert comma if this is not the first argument in the list
            #
            if not arg_list_empty:
                app.insert_indent(', ', '')


m_simple_for = \
    ActionInsert(code_bef='for ',
#                code_after=';  <= ; ++)\n\t{\n\t\n\t}\n',
# I'm switching this to use the more common indentation, which matches
# what Emacs does anyway
# ugh - that's not true -- Emacs does it this way for for-loops which
# start at indentation = 0, but the way above for for-loops which are
# inside another block.  That's idiotic!

# because it's easy to say e.g. 'equals zero' and harder to correct it
# if we want to handle the loop another way, don't insert the '=0'
# automatically (SN)
#                code_after='=0;  <= ; ++)\n{\n\t\n}\n',
                 code_after='\nend',
                 docstring = """Insert template code for a simple Matlab for loop""")

m_simple_while = \
    ActionInsert(code_bef='while ', code_after='\nend',
                 docstring = """Insert template code for a simple Matlab while loop""")

m_do_while = \
    ActionInsert(code_bef='do\n\t', code_after='\n while ',
                 docstring = """Insert template code for a Matlab do-while loop""")

m_goto_body = \
    ActionSearch(regexp=r'\n[ \t]*',
                 docstring="""Move cursor to the body of a Matlab compound statement""")

m_function_declaration = \
    ActionInsert(code_bef='function ',
                 code_after='()',
                 docstring = """Types template code for a Matlab function declaration (no function body)""")

m_function_definition = \
    ActionInsert(code_bef='function ',
                 code_after='()\n\n',
                 docstring = """Types template code for a Matlab function (including body)""")

m_function_add_argument = \
    ActionMAddArgument(
              docstring="""Positions cursor for adding an argument to a Matlab function declaration or call""")


m_method_declaration = \
    ActionInsert(code_bef='function ',
                 code_after='(obj)',
                 docstring = """Types template code for a Matlab method declaration (no method body)""")

m_method_definition = \
    ActionInsert(code_bef='function ',
                 code_after='(obj)\n\n',
                 docstring = """Types template code for a Matlab method (including body)""")

#m_method_add_argument = \
#    ActionMAddArgument(
#              docstring="""Positions cursor for adding an argument to a Matlab method declaration or call""")

m_function_body = \
    ActionSearch(regexp=r'function\s*[?(\w+[,]?)*]?\s*=?\s*\w+\(?(\w+[,]?)*\)?\s*',
                 docstring = """Moves cursor to the body of a C/C++ method or function""")




# From actions_py.py:
m_new_statement = \
				   ActionInsertNewClause(end_of_clause_regexp='(\n|$)',
						   where = -1, direction = 1,
						   add_lines = 1,
						   code_bef='', code_after='',
						   back_indent_by=0,
						   docstring = """Inserts a new line below current one""")

m_new_statement_above = \
						 ActionInsertNewClause(end_of_clause_regexp='(^|\n)',
								 where = 1, direction=-1,
								 add_lines = 1,
								 code_bef='', code_after='', back_indent_by=0,
								 docstring = """Inserts a new line above current one""")


#### NOTE: this doesn't work well if you're in a {} pair (e.g. 'if ... then new statement')
# we need different behavior when there's a } before a ; -- insert BEFORE the }
##m_new_statement = \
##                ActionCompound(
##    (ActionInsertNewClause(
##    #    end_of_clause_regexp='([;{]|(#.*$)|(#.*\\n))', 
##                                      end_of_clause_regexp = "([;{]\\s*($|\\n)|#.*($|\\n))",
##                                      start_of_next_clause_regexp = "\\}",
##                                      where = 100, direction = 1,
##                                      add_lines = 0,
##                                      code_bef='', code_after='\n',
##                                      back_indent_by=0,
##                                      include_current_line = 1,
##                                      docstring = """Start a new C/C++ statement on next line"""),
##     ActionInsert(code_after=";"),
##     ActionSearch(";", direction=1, where=-1)))

##m_new_statement_above = \
##                      ActionInsertNewClause(
##    end_of_clause_regexp = r"(;.*\n)|(\{.*\n)|(\}.*\n)|(#.*($|\n))",
##    # since we always insert after the found symbol (e.g. }) we don't
##    # need to worry about start_of_next_clause_regexp the way we do
##    # for c_new_statement
##    # start_of_next_clause_regexp = "[\\}\\{]",
##    where = 1, direction = -1,
##    add_lines = 1,
##    code_bef='\t', code_after=';',
##    back_indent_by=0,
##    include_current_line = 0,
##    docstring = """Start a new C/C++ statement before this one""")



# this assumes the if ends with a '}' (not a one-liner)
#                ActionInsertNewClause(end_of_clause_regexp='end\n', 
m_else_if = \
                ActionInsertNewClause(end_of_clause_regexp='\n', 
                                      where = 1, direction = 1,
                                      add_lines = 1,
                                      code_bef='elseif ', code_after='',
                                      back_indent_by=0,
                                      docstring='else-if clause of an Matlab conditional')

# this assumes the if ends with a '}' (not a one-liner)
#                ActionInsertNewClause(end_of_clause_regexp='end\n', 
m_else = \
                ActionInsertNewClause(end_of_clause_regexp='\n', 
                                      where = 1, direction = 1,
                                      add_lines = 1,
                                      code_bef='else\n', code_after='',
                                      back_indent_by=0,
                                      docstring='else clause of a Matlab conditional')



class ActionMCommentAbove(Action):
    """Creates a new comment line above the current one."""

    def __init__(self, **args_super):
        self.deep_construct(ActionMCommentAbove, \
                            {}, \
                            args_super, \
                            {})

    def execute(self, app, cont, state = None):
        """See [Action.execute].

        .. [Action.execute] file:///./actions_gen.Action.html#execute"""


        was_on_line = app.line_num_of()
        found = app.search_for('(^|\n)', direction=-1, where=-1, unlogged = 1)
        app.insert('\n')
        if was_on_line == 1:
           app.goto(0)
        app.insert('# ')




m_class_definition = \
					 ActionInsert(code_bef='class ',
							 code_after='\r\t'
							 + 'properties (SetAccess = public)\n\t\t\n\tend'
							 + '\n\tproperties (SetAccess = private)\n\t\t\n\tend'
							 + '\n\tmethods (SetAccess = public)\n\t\t\n\tend'
							 + '\n\tmethods (SetAccess = private)\n\t\t\n\tend'
							 + '\nend',
							 docstring = """Insert template code for a Matlab class""",
							 expect="class")

m_subclass = \
			 ActionInsert(code_bef=' < ', code_after='',
					 docstring = """Inserts ' < ' for subclass definition""", expect='class')

m_class_alias = \
				ActionInsert(code_bef='class ', code_after=' < \rend',
						docstring = """Inserts an empty subclass definition for aliasing""", expect='class')


m_class_body = \
			   ActionSearch(regexp=r'class\s*<?\s*\w*\s*',
					   docstring="""Moves cursor to the body of a class""")



