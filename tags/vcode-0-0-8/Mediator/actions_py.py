"""Action functions for Python language"""

import re
import SymDict

def py_empty_dictionary(app, cont):
    """Types code for an empty Python dictionary (e.g. {}^)"""
    app.insert_indent('{}', '')

def py_simple_for(app, cont):
    """Insert template code for a simple Python for loop"""
    app.insert_indent('for ', ':\n')

def py_goto_body(app, cont):
    """Move cursor to the body of a Python compound statement"""
    app.search_for(':\s*\n[ \t]*\n*')

def py_if(app, cont):
    """Types template code for an if statement"""
    app.insert_indent('if ', ':\n')

def py_else_if(app, cont):
    """Types template code for an else if statement"""
    app.insert_indent('elif ', ':\n')

def py_else(app, cont):
    """Types template code for an else clause."""
    app.insert_indent('else:\n', '')

def py_logical_and(app, cont):
    """Types a logical and with spaces"""
    app.insert_indent(' and ', '')

def py_logical_equal(app, cont):
    """Types a logical equality operator with spaces"""
    app.insert_indent(' == ', '')

def py_logical_not_equal(app, cont):
    """Types a logical inequality operator with spaces"""
    app.insert_indent(' != ', '')
    
def py_assignment(app, cont):
    """Types an assignment operator with spaces"""
    app.insert_indent(' = ', '')

def py_new_statement(app, cont):
    """Inserts a new line below current one"""
    app.search_for('(\n|$)')
    app.insert_indent('\n', '')

def py_class_definition(app, cont):
    """Inserts template code for a Python class"""
    app.insert_indent('class ', ':\n')

def py_class_body(app, cont):
    """Moves cursor to the body of a class"""
    app.search_for(':\\s*')

def py_method_declaration(app, cont):
    """Types template code for a method"""
    app.insert_indent('def ', '(self):\n')

def py_function_add_argument(app, cont):
    """Positions cursor for adding an argument to a Python function declaration or call"""
    found = app.search_for('\\)\s*:{0,1}', where=-1)
    if found:
        #
        # See if argument list was empty
        #        
        arg_list_empty = 1
        pos = app.curr_buffer.cur_pos - 1
        
        #
        # Find first preceding non-space character
        #
        while pos >= 0:
            if not re.match('\s', app.curr_buffer.content[pos]):
                #
                # The first preceding non-space character is (
                #    => argument list is empty
                #
                arg_list_empty = app.curr_buffer.content[pos] == '('
                break
            pos = pos - 1

        #
        # Insert comma if this is not the first argument in the list
        #
        if not arg_list_empty:
            app.insert_indent(', ', '')

def py_function_body(app, cont):
    """Moves cursor to the body of a Python method or function"""
    app.search_for(':\s*')

def py_continue_statement(app, cont):
    """Continues a Python statement on the next line (i.e. inserts \\\\n"""
    app.insert_indent('\\\n', '')
