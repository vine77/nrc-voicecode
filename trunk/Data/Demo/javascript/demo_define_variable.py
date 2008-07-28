# demo file generated with mediator test of JavascriptAcceptanceTest
#
name = "define variable" 
utt1 = 'new statement'
exp1 = \
"""<CURSOR>;
"""
#
utt2 = "define variable"
exp2 = \
"""define_variable<CURSOR>;
"""
#
utt3 = "example equals zero"
exp3 = \
"""define_variableexample = 0<CURSOR>;
"""
#
utt4 = "new statement"
exp4 = \
"""define_variableexample = 0;
<CURSOR>;
"""
#
utt5 = "india plus plus"
exp5 = \
"""define_variableexample = 0;
i++<CURSOR>;
"""
#
utt6 = "new statement"
exp6 = \
"""define_variableexample = 0;
i++;
<CURSOR>;
"""
#
