"""Action functions for C language """

def c_simple_for(app, cont):
    """Insert template code for a simple C for loop"""
    print '-- actions_C.c_simple_for: called'
    app.insert_indent('for (', '=0;  <= ; ++)\n{\n\n}\n')

def c_goto_body(app, cont):
    """Move cursor to the body of a C compound statement"""
    app.search_for('\)\s*\{[ \t]*\n*')

