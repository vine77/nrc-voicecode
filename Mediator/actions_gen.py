"""Action functions that span different languages"""

import exceptions, os, re
import vc_globals

#
# Index of the current anonymous action function.
#
anonymous_action_curr_num = 0

class AnonymousAction(exceptions.Exception):
    """Raised when the code for an anonymous action function has syntax errors"""

def indent_code(num, code):
    padding = ''
    for ii in range(num): padding = padding + ' '
    code = re.sub('(^|\n)', '\\1' + padding, code)
    return code

def anonymous_action(code, description):
    """This function creates an anonymous action function.

    The anonymous function gets an internal name of the form
    *anonymous_action_N* where *N* is some number.

    *STR code* -- Code for the anoymous action function. This code
     should assume that the application object is called *app*, and
     the context object is called *cont*.

    *STR description* -- Description of the action function
    """

    global anonymous_action_curr_num

    #
    # Create code for a new anymous action function *anonymous_action_N*
    # in a temporary file (for some reason, *exec* can't compile code
    # that declares a new function, whereas *execfile* can)
    #
    tmp_file_name = vc_globals.tmp + os.sep + 'tmp_anonymous_action.py'
    tmp_file = open(tmp_file_name, 'w')
    tmp_file.write('def anonymous_action_%s(app, cont):\n%s\n%s' % (anonymous_action_curr_num, indent_code(4, '"""' + description + '"""'), indent_code(4, code)))
    tmp_file.close()

    try:
        execfile(tmp_file_name)
        fct = eval('anonymous_action_%s' % anonymous_action_curr_num)
        anonymous_action_curr_num = anonymous_action_curr_num + 1
        return fct        
    except:
        raise AnonymousAction, 'Syntax error in code of anonymous action function.\Code was:\n%s\n' % code

def gen_parens_pair(app, cont):
    """Insert parens and puts cursor in between"""
    app.insert_indent('(', ')')

def gen_brackets_pair(app, cont):
    """Insert brackets"""
    app.insert_indent('[', ']')

def gen_braces_pair(app, cont):
    """Insert braces"""
    app.insert_indent('{', '}')


def gen_quotes_pair(app, cont):
    """Insert quotes and moves cursor in between"""
    app.insert_indent('"', '"')

def gen_single_quotes_pair_after(app, cont):
    """Insert single quotes and moves cursor after"""
    app.insert_indent('""', '')

def gen_single_quotes_pair(app, cont):
    """Insert single quotes and moves cursor in between"""
    app.insert_indent('\'', '\'')

def gen_single_quotes_pair_after(app, cont):
    """Insert single quotes and moves cursor after"""
    app.insert_indent('\'\'', '')
