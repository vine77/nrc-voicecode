#
# Configuration script for VoiceCode
#

#
# Note: those import statements are not absolutely necessary because file
#       vc_config.py is evaluated in a context where those have already
#       been imported.
#
#       But having them here makes it possible to compile vc_config.py
#       with command line:
#
#           python vc_config.py
#
#       which provides better error reporting.
#
import natlink
from natlinkutils import *

#
# Import configuration functions
#
from MediatorObject import associate_language, define_language, add_abbreviation, add_csc, add_lsa, standard_symbols_in

from CSCmd import CSCmd
from LangDef import LangDef
from cont_gen import *
from actions_gen import *
from actions_C_Cpp import *
from actions_py import *

import sr_interface


if (__name__ == '__main__'):
    import MediatorObject
    MediatorObject.to_configure = MediatorObject.MediatorObject()
    
    if sr_interface.speech_able():
        natlink.natConnect()    


##############################################################################
# Customize from here only
##############################################################################


###############################################################################
# Associate file extensions to programming languages
###############################################################################

#
# Doesn't seem to work for now so we set it in SourceBuff.py directly
#
#  associate_language('c', 'C')
#  associate_language('h', 'C')
#  associate_language('py', 'python')
# print '-- vc_config: SourceBuff.file_language=%s' % str(SourceBuff.file_language)


###############################################################################
# Definition of the syntax of various languages
###############################################################################
define_language('C',
                LangDef(regexp_symbol='[a-zA-Z_][a-zA-Z0-9_]*', \
                        regexps_no_symbols=['/\*.*\*/', '//[^\n]*\n', \
                                            '"([^"]|\\")*?"', \
                                            '\'([^\']|\\\')*?\'']))

define_language('python',
                LangDef(regexp_symbol='[a-zA-Z_][a-zA-Z0-9_]*', \
                        regexps_no_symbols=['#[^\n]*\n', '"""[\s\S]*?"""', \
                                            '"([^"]|\\")*?"', \
                                            '\'([^\']|\\\')*?\'']))

###############################################################################
# Define abbreviations
###############################################################################
add_abbreviation('attr', ['attribute'])
add_abbreviation('buff', ['buffer'])
add_abbreviation('cmd', ['command'])
add_abbreviation('cpp', ['C. plus plus'])
add_abbreviation('arg', ['argument'])
add_abbreviation('cond', ['condition'])
add_abbreviation('cont', ['control'])
add_abbreviation('curr', ['current'])
add_abbreviation('def', ['definition', 'default', 'define', 'defined', 'deaf'])
add_abbreviation('dict', ['dictionary'])
add_abbreviation('environ', ['environment'])
add_abbreviation('exc', ['exception'])
add_abbreviation('gen', ['general', 'generic'])
add_abbreviation('getattr', ['get attribute'])
add_abbreviation('horiz', ['horizontal', 'horizontally'])
add_abbreviation('inc', ['increment', 'include'])
add_abbreviation('init', ['initial', 'initialize'])
add_abbreviation('interp', ['interpreter'])
add_abbreviation('mtime', ['M. time'])
add_abbreviation('os', ['operating system', 'O. S.'])
add_abbreviation('pos', ['position', 'positionning'])
add_abbreviation('prof', ['profile', 'profiling', 'professional'])
add_abbreviation('py', ['python'])
add_abbreviation('regexp', ['regular expression'])
add_abbreviation('st', ['standard'])
add_abbreviation('sys', ['system'])
add_abbreviation('undef', ['undefined'])
add_abbreviation('vert', ['vertical', 'vertically'])

###############################################################################
# Language sensitive aliases (LSAs)
###############################################################################

#
# LSAs active for all languages
#
add_lsa(None, ['blank space'], ' ')
add_lsa(None, ['asterisk'], '*')
add_lsa(None, ['double asterisk'], '**')
add_lsa(None, ['colon'], ': ')
add_lsa(None, ['plus'], ' + ')
add_lsa(None, ['plus sign'], '+')
add_lsa(None, ['open bracket'], '[')
add_lsa(None, ['newline', 'new line'], '\n')
add_lsa(None, ['comma'], ', ')
add_lsa(None, ['dot'], '.')


#
# LSAs active for more than one language
#
add_lsa(['C', 'python'], ['equals', 'equal', 'is assigned', 'assign value'], ' = ')
add_lsa(['C', 'python'], ['not equal to', 'not equal', 'is not equal', 'is not equal to'], ' != ')

# Note: different action gen_parens_pair (the later puts cursor
# between the parens)
add_lsa(['C', 'python'], ['without arguments', 'with no arguments', 'without argument', 'with no argument'], '()')

add_lsa(['C', 'python'], ['return'], 'return ')


add_lsa(['perl', 'python'], ['back slash s.', 'back slash s', 'back slash sierra', 'space character'], '\\s')

#
# Python specific aliases
#

# This one is used for 'import blah', said as: 'import module blah'
add_lsa(None, ['import module', 'import modules'], 'import ')

#
# while this one is used for 'from blah import blob',
# said as: 'from module blah import symbols blob'
#
add_lsa(['python'], ['import symbols', 'import symbol'], ' import ')

add_lsa(['python'], ['from module'], 'from ')
add_lsa(['python'], ['import all'], ' import all')
add_lsa(['python'], ['not', 'not true'], 'not ')


#
# C specific LSAs
#
add_lsa(['C'], ['double colon', 'colon colon'], '::')

###############################################################################
# Context Sensitive Commands (CSCs)
###############################################################################

#
# CSCs useful for more than one language
#
acmd = CSCmd(spoken_forms=['between paren', 'between parens', 'paren pair', 'parens pair', 'with arguments', 'call with', 'called with'], meanings=[[ContC(), gen_parens_pair], [ContPy(), gen_parens_pair]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['bracket pair', 'brackets pair', 'at index'], meanings=[[ContC(), gen_brackets_pair], [ContPy(), gen_brackets_pair]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['brace pair', 'braces pair', 'between braces', 'between brace'], meanings=[[ContC(), gen_braces_pair], [ContPy(), gen_braces_pair]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['single quote', 'single quotes'], meanings=[[ContC(), gen_single_quotes_pair], [ContPy(), gen_single_quotes_pair]])
add_csc(acmd)

# This one moves cursor after the quotes.
# Can't be created as an LSA because the '' cause problems in the
# automatically generated CSC (it doesn't compile). Reevaluate this when
# actions are made into objects
acmd = CSCmd(spoken_forms=['empty single quote', 'empty single quotes'], meanings=[[ContC(), gen_single_quotes_pair_after], [ContPy(), gen_single_quotes_pair_after]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['quotes', 'quote'], meanings=[[ContC(), gen_quotes_pair], [ContPy(), gen_quotes_pair]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['for', 'for loop'], meanings=[[ContC(), c_simple_for], [ContPy(), py_simple_for]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['loop body', 'goto body'], meanings=[[ContC(), c_goto_body], [ContPy(), py_goto_body]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['if statement', 'if'], meanings=[[ContPy(), py_if]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['else if', 'else if clause'], meanings=[[ContPy(), py_else_if]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['else clause', 'else'], meanings=[[ContPy(), py_else]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['then', 'if body'], meanings=[[ContPy(), py_goto_body]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['after ;', 'after semi', 'after semicolon', 'goto semi', 'goto semicolon', 'goto ;', 'go semi', 'go semicolon', 'go ;', 'go after semi', 'go after semicolon', 'go after ;'], meanings=[[ContAny(), ActionSearch(';\s{0,1}')]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['before ;', 'before semi', 'before semicolon', 'goto semi', 'goto semicolon', 'goto ;', 'go semi', 'go semicolon', 'go ;', 'go before semi', 'go before semicolon', 'go before ;'], meanings=[[ContAny(), ActionSearch('\s{0,1};', direction=-1)]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['after ,', 'after comma', 'goto comma', 'goto ,', 'go comma', 'go ,', 'go after comma', 'go after ,'], meanings=[[ContAny(), ActionSearch(',\s{0,1}')]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['before ,', 'before comma', 'goto comma', 'goto ,', 'go comma', 'go ,', 'go before comma', 'go before ,'], meanings=[[ContAny(), ActionSearch('\s{0,1},', direction=-1)]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['after =', 'after equal', 'goto equal', 'goto =', 'go equal', 'go =', 'go after equal', 'go after ='], meanings=[[ContAny(), ActionSearch('=\s{0,1}')]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['before =', 'before equal', 'goto equal', 'goto =', 'go equal', 'go =', 'go before equal', 'go before ='], meanings=[[ContAny(), ActionSearch('\s{0,1}=', direction=-1)]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['after paren', 'after paren', 'goto paren', 'goto paren', 'go paren', 'go paren', 'go after paren', 'go after paren'], meanings=[[ContAny(), ActionSearch('[\(\)]\s{0,1}')]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['before paren', 'before paren', 'goto paren', 'goto paren', 'go paren', 'go paren', 'go before paren', 'go before paren'], meanings=[[ContAny(), ActionSearch('\s{0,1}[\(\)]', direction=-1)]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['jump out'], meanings=[[ContAny(), ActionSearch('[\]\)\}\'\"]\s{0,1}')]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['jump out of paren', 'out of paren'], meanings=[[ContAny(), ActionSearch('\)\s{0,1}')]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['and', 'logical and', 'and also'], meanings=[[ContPy(), py_logical_and]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['define class', 'declare class', 'class definition'], meanings=[[ContC(), cpp_class_definition], [ContPy(), py_class_definition]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['sub class of', 'inherits from', 'is subclass', 'is subclass of'], meanings=[[ContC(), cpp_subclass], [ContPy(), gen_parens_pair]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['class body'], meanings=[[ContC(), cpp_class_body], [ContPy(), py_class_body]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['define method'], meanings=[[ContC(), c_function_declaration], [ContPy(), py_method_declaration]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['add argument', 'add arguments'], meanings=[[ContC(), c_function_add_argument], [ContPy(), py_function_add_argument]])
add_csc(acmd)


acmd = CSCmd(spoken_forms=['method body'], meanings=[[ContC(), c_function_body], [ContPy(), py_function_body]])
add_csc(acmd)


#
# This is now a language specific abbreviation
#
# acmd = CSCmd(spoken_forms=['equals', 'assigned value', 'is assigned value'], meanings=[[ContPy(), py_assignment]])
# add_csc(acmd)

acmd = CSCmd(spoken_forms=['is equal to', 'equal to'], meanings=[[ContPy(), py_logical_equal]])
add_csc(acmd)

# This is now a language specific abbreviation
# acmd = CSCmd(spoken_forms=['is not equal to', 'not equal to'], meanings=[[ContPy(), py_logical_not_equal]])
# add_csc(acmd)


#
# Python specific CSCs
#
acmd = CSCmd(spoken_forms=['with superclasses'], meanings=[[ContPy(), gen_parens_pair]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['in list'], meanings=[[ContPy(), ActionInsert(' in ', '')]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['new statement'], meanings=[[ContPy(), py_new_statement]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['empty dictionary'], meanings=[[ContPy(), py_empty_dictionary]])


add_csc(acmd)


#
# Note: this one can't be defined as an LSA because it inserts a \n
# (which means that the anonymous function can't compile)
# When we replace action functions with action objects, we should revisit
# this question
#
acmd = CSCmd(spoken_forms=['continue statement'], meanings=[[ContPy(), py_continue_statement]])
add_csc(acmd)


###############################################################################
# Compile standard symbols for various languages
###############################################################################

#
# Python
#
standard_symbols_in([vc_globals.config + os.sep + 'py_std_sym.py'])

###############################################################################
# Add words which are missing from the SR vacab
###############################################################################
sr_interface.addWord('un')


if (__name__ == '__main__'): natlink.natDisconnect()
