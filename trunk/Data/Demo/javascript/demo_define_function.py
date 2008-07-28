# demo file generated with mediator test of JavascriptAcceptanceTest
#
name = "demo define function"
utt1 = 'new statement'
exp1 = \
"""<CURSOR>;
"""
#
utt2 = 'define variable'
exp2 = \
"""define_variable<CURSOR>;
"""
#
utt3 = 'example equals zero'
exp3 = \
"""define_variableexample = 0<CURSOR>;
"""
#
utt4 = 'new statement'
exp4 = \
"""define_variableexample = 0;
<CURSOR>;
"""
#
utt5 = 'define function'
exp5 = \
"""define_variableexample = 0;
function <CURSOR>(){

};
"""
#
utt6 = 'example function'
exp6 = \
"""define_variableexample = 0;
function example_function<CURSOR>(){

};
"""
#
utt7 = 'with argument India'
exp7 = \
"""define_variableexample = 0;
function example_function(i<CURSOR>){

};
"""
#
utt8 = 'do the following new statement'
exp8 = \
"""define_variableexample = 0;
function example_function(i){

  <CURSOR>;
};
"""
#
utt9 = 'new statement'
exp9 = \
"""define_variableexample = 0;
function example_function(i){

  ;
  <CURSOR>;
};
"""
#
utt10 = 'alert'
exp10 = \
"""define_variableexample = 0;
function example_function(i){

  ;
  alert<CURSOR>;
};
"""
#
utt11 = 'with arguments'
exp11 = \
"""define_variableexample = 0;
function example_function(i){

  ;
  alert(<CURSOR>);
};
"""
#
utt12 = 'between quotes'
exp12 = \
'''define_variableexample = 0;
function example_function(i){

  ;
  alert("<CURSOR>");
};
'''
#
utt13 = 'new value colon'
exp13 = \
'''define_variableexample = 0;
function example_function(i){

  ;
  alert("new_value: <CURSOR>");
};
'''
#
utt14 = 'jump out'
exp14 = \
'''define_variableexample = 0;
function example_function(i){

  ;
  alert("new_value: "<CURSOR>);
};
'''
#
utt15 = 'plus example'
exp15 = \
'''define_variableexample = 0;
function example_function(i){

  ;
  alert("new_value: " + example<CURSOR>);
};
'''
#