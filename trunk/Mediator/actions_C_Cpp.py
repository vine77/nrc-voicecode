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


"""Action functions for C language """

from actions_gen import Action, ActionInsert, ActionSearch
import whrandom
import string

c_simple_for = \
    ActionInsert(code_bef='for (',
                 code_after='=0;  <= ; ++)\n\t{\n\t\n\t}\n',
                 docstring = """Insert template code for a simple C for loop""")

c_simple_while = \
    ActionInsert(code_bef='while (', code_after=')\n\t{\n\t}',
                 docstring = """Insert template code for a simple C for loop""")

c_goto_body = \
    ActionSearch(regexp='\)\s*\{[ \t]*\n{0,1}',
                 docstring="""Move cursor to the body of a C compound statement""")

cpp_class_definition = \
    ActionInsert(code_bef='class ',
                 code_after='\n\t{\n\n\tpublic:\n\t\n\tprivate:\n\t}',
                 docstring = """Insert template code for a C++ class""")
    
cpp_subclass = \
    ActionInsert(code_bef=': ', code_after='',
                 docstring = """Inserts ': ' for subclass definition""")

cpp_class_body = \
    ActionSearch(regexp='\\{\\s*',
                 docstring="""Moves cursor to the body of a class""")

c_function_declaration = \
    ActionInsert(code_bef='\n*** Action c_function_declaration not implemented yet ***\n',
                 code_after='',
                 docstring = """Types template code for a C function or C++ method""")

c_function_add_argument = \
    ActionInsert(code_bef='\n*** Action c_function_add_argument not implemented yet ***\n',
              code_after='',
              docstring="""Positions cursor for adding an argument to a C/C++ function declaration or call""")

c_function_body = \
    ActionInsert(code_bef='\n*** Action c_function_body not implemented yet ***\n',
                 code_after='',
                 docstring = """Moves cursor to the body of a C/C++ method or function""")

c_new_statement = \
    ActionInsert(code_bef='\n*** Action c_new_statement not implemented yet ***\n',
                 docstring = """Start a new C statement on next line""")

c_else_if = \
    ActionInsert(code_bef='*** action c_else_if not implemeted yet ***',
                 docstring='else if clause of a C conditional')

c_else = \
    ActionInsert(code_bef='*** action c_else_if not implemeted yet ***',
                 docstring='else clause of a C conditional')

class ActionHeaderWrapper(Action):
    """Action that inserts a code template for one time #include
        
    **INSTANCE ATTRIBUTES**
        
    *NONE*
    
    CLASS ATTRIBUTES**
    
    *none* -- 
    """
        
    def __init__(self, **args_super):
        self.deep_construct(ActionHeaderWrapper, \
                            {}, \
                            args_super, \
                            {})

        
    def execute(self, app, cont):
        """See [Action.execute].
        
        .. [Action.execute] file:///./actions_gen.Action.html#execute"""
        unique_str = str(string.upper(string.replace(app.curr_buffer_name(),'.','_'))) + \
                     str(whrandom.randint(10**6,(10**7)-1))
        before_string  = '#ifndef ' + unique_str + '\n' + '#define ' + unique_str + '\n\n'
        after_string = '\n#endif\n'
        app.insert_indent(before_string, after_string)


    def doc(self):
        """
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        if self.docstring != None:
            the_doc = self.docstring
        else:
            the_doc = 'inserts a code template for one time #include'
        return the_doc


