
"""Action functions for C language """

from actions_gen import Action, ActionInsert, ActionSearch, ActionSearchInsert

c_simple_for = \
    ActionInsert(code_bef='for (',
                 code_after='=0;  <= ; ++)\n{\n\n}\n',
                 docstring = """Insert template code for a simple C for loop""")

c_simple_while = \
    ActionInsert(code_bef='while (', code_after=')\n{\n}',
                 docstring = """Insert template code for a simple C for loop""")

c_goto_body = \
    ActionSearch(regexp='\)\s*\{[ \t]*\n*',
                 docstring="""Move cursor to the body of a C compound statement""")

cpp_class_definition = \
    ActionInsert(code_bef='class ',
                 code_after='{\n\npublic:\n\nprivate:\n}',
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
