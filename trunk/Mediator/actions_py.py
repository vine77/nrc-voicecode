"""Action functions for Python language"""

def py_simple_for(app, cont):
    """Insert template code for a simple Python for loop"""
    app.insert_indent('for ', ' in :\n')


def py_goto_body(app, cont):
    """Move cursor to the body of a Python compound statement"""
    app.search_for(':\s*\n[ \t]*\n*')
