#
# Configuration script for VoiceCode
#


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


#
# Python specific CSCs
#
acmd = CSCmd(spoken_forms=['with superclasses'], meanings=[[ContPy(), gen_parens_pair]])
add_csc(acmd)

