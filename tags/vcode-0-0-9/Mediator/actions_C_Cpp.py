"""Action functions for C language """

from actions_gen import Action, ActionInsert, ActionSearch, ActionSearchInsert

c_simple_for = \
    ActionInsert(code_bef='for (',
                 code_after='=0;  <= ; ++)\n{\n\n}\n',
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

