"""Action functions that span different languages"""

def gen_parens_pair(app, cont):
    """Insert parens"""
    app.insert_indent('(', ')')

def gen_brackets_pair(app, cont):
    """Insert brackets"""
    app.insert_indent('[', ']')

def gen_quotes_pair(app, cont):
    """Insert quotes"""
    app.insert_indent('"', '"')

def gen_single_quotes_pair(app, cont):
    """Insert single quotes"""
    app.insert_indent('\'', '\'')
    
    
