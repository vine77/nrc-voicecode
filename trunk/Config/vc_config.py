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
from CSCmd import CSCmd
from config import add_csc
from cont_gen import *
from actions_gen import *
from actions_C_Cpp import *
from actions_py import *

#
# Cross language CSCs
#
acmd = CSCmd(spoken_forms=['with arguments', 'call with', 'called with'], meanings=[[ContC(), gen_parens_pair], [ContPy(), gen_parens_pair]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['at index'], meanings=[[ContC(), gen_brackets_pair], [ContPy(), gen_brackets_pair]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['for', 'for loop'], meanings=[[ContC(), c_simple_for], [ContPy(), py_simple_for]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['loop body', 'goto body'], meanings=[[ContC(), c_goto_body], [ContPy(), py_goto_body]])
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

acmd = CSCmd(spoken_forms=['jump out'], meanings=[[ContAny(), lambda app, cont: app.search_for('[\]\)\}]\s{0,1}')]])
add_csc(acmd)

acmd = CSCmd(spoken_forms=['jump out of paren', 'out of paren'], meanings=[[ContAny(), lambda app, cont: app.search_for('\)\s{0,1}')]])
add_csc(acmd)

#
# Python specific CSCs
#
acmd = CSCmd(spoken_forms=['with superclasses'], meanings=[[ContPy(), gen_parens_pair]])
add_csc(acmd)

