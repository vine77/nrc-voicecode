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
from MediatorObject import associate_language, define_language, add_abbreviation, add_csc, add_lsa

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
add_abbreviation('vc', ['voice code'])


###############################################################################
# Context Sensitive Commands (CSCs)
###############################################################################

#
# Cross language CSCs
#
acmd = CSCmd(spoken_forms=['between paren', 'between parens', 'paren pair', 'parens pair', 'with arguments', 'call with', 'called with'], meanings=[[ContC(), gen_parens_pair], [ContPy(), gen_parens_pair]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['bracket pair', 'brackets pair', 'at index'], meanings=[[ContC(), gen_brackets_pair], [ContPy(), gen_brackets_pair]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['single quote', 'single quotes'], meanings=[[ContC(), gen_single_quotes_pair], [ContPy(), gen_single_quotes_pair]])
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


acmd = CSCmd(spoken_forms=['after ;', 'after semi', 'after semicolon', 'goto semi', 'goto semicolon', 'goto ;', 'go semi', 'go semicolon', 'go ;', 'go after semi', 'go after semicolon', 'go after ;'], meanings=[[ContAny(), lambda app, cont: app.search_for(';\s{0,1}')]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['before ;', 'before semi', 'before semicolon', 'goto semi', 'goto semicolon', 'goto ;', 'go semi', 'go semicolon', 'go ;', 'go before semi', 'go before semicolon', 'go before ;'], meanings=[[ContAny(), lambda app, cont: app.search_for('\s{0,1};', direction=-1)]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['after ,', 'after comma', 'goto comma', 'goto ,', 'go comma', 'go ,', 'go after comma', 'go after ,'], meanings=[[ContAny(), lambda app, cont: app.search_for(',\s{0,1}')]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['before ,', 'before comma', 'goto comma', 'goto ,', 'go comma', 'go ,', 'go before comma', 'go before ,'], meanings=[[ContAny(), lambda app, cont: app.search_for('\s{0,1},', direction=-1)]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['after =', 'after equal', 'goto equal', 'goto =', 'go equal', 'go =', 'go after equal', 'go after ='], meanings=[[ContAny(), lambda app, cont: app.search_for('=\s{0,1}')]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['before =', 'before equal', 'goto equal', 'goto =', 'go equal', 'go =', 'go before equal', 'go before ='], meanings=[[ContAny(), lambda app, cont: app.search_for('\s{0,1}=', direction=-1)]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['after paren', 'after paren', 'goto paren', 'goto paren', 'go paren', 'go paren', 'go after paren', 'go after paren'], meanings=[[ContAny(), lambda app, cont: app.search_for('[\(\)]\s{0,1}')]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['before paren', 'before paren', 'goto paren', 'goto paren', 'go paren', 'go paren', 'go before paren', 'go before paren'], meanings=[[ContAny(), lambda app, cont: app.search_for('\s{0,1}[\(\)]', direction=-1)]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['jump out'], meanings=[[ContAny(), lambda app, cont: app.search_for('[\]\)\}\'\"]\s{0,1}')]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['jump out of paren', 'out of paren'], meanings=[[ContAny(), lambda app, cont: app.search_for('\)\s{0,1}')]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['and', 'logical and', 'and also'], meanings=[[ContPy(), py_logical_and]])
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

acmd = CSCmd(spoken_forms=['in'], meanings=[[ContPy(), lambda app, cont: app.insert_indent(' in ', '')]])
add_csc(acmd)

#
# Language specific aliases
#
add_lsa(['C', 'python'], ['equals', 'equal', 'is assigned', 'assign value'], ' = ')
add_lsa(['C', 'python'], ['not equal to', 'not equal', 'is not equal', 'is not equal to'], ' != ')


if (__name__ == '__main__'): natlink.natDisconnect()
