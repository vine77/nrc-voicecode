"""Action functions for C language """

def c_simple_for(app, cont):
    """Insert template code for a simple C for loop"""
    app.insert_indent('for (', '=0;  <= ; ++)\n{\n\n}\n')

def c_goto_body(app, cont):
    """Move cursor to the body of a C compound statement"""
    app.search_for('\)\s*\{[ \t]*\n*')

def cpp_class_definition(app, cont):
    """Insert template code for a C++ class"""
    app.insert_indent('class ', '{\n\npublic:\n\nprivate:\n}')
    
def cpp_subclass(app, cont):
    """Inserts ': ' for subclass definition"""
    app.insert_indent(': ', '')

def cpp_class_body(app, cont):
    """Moves cursor to the body of a class"""
    app.search_for('\\{\\s*')

def c_function_declaration(app, cont):
    """Types template code for a C function or C++ method"""
    app.insert_indent('\n*** Action c_function_declaration not implemented yet ***\n', '')

def c_function_add_argument(app, cont):
    """Positions cursor for adding an argument to a C/C++ function declaration or call"""
    app.insert_indent('\n*** Action c_function_add_argument not implemented yet ***\n', '')    

def c_function_body(app, cont):
    """Moves cursor to the body of a C/C++ method or function"""
    app.insert_indent('\n*** Action c_function_body not implemented yet ***\n', '')
