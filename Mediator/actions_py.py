"""Action functions for Python language"""

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

