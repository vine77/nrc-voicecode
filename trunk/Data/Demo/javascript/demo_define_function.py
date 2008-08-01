# demo file generated with mediator test of JavascriptAcceptanceTest
#
utt1 = "new statement"
exp1 = \
"""<CURSOR>;
"""
utt2 = "define variable"
exp2 = \
"""var <CURSOR>;;
"""
utt3 = "example equals zero"
exp3 = \
"""var example = 0<CURSOR>;;
"""
utt4 = "new statement"
exp4 = \
"""var example = 0;;
<CURSOR>;
"""
utt5 = "define function"
exp5 = \
"""var example = 0;;
function <CURSOR>(){

};
"""
utt6 = "example function"
exp6 = \
"""var example = 0;;
function example_function<CURSOR>(){

};
"""
utt7 = "with argument India"
exp7 = \
"""var example = 0;;
function example_function(i<CURSOR>){

};
"""
utt8 = "do the following new statement"
exp8 = \
"""var example = 0;;
function example_function(i){

  <CURSOR>;
};
"""
utt9 = "new statement"
exp9 = \
"""var example = 0;;
function example_function(i){

  ;
  <CURSOR>;
};
"""
utt10 = "alert"
exp10 = \
"""var example = 0;;
function example_function(i){

  ;
  alert<CURSOR>;
};
"""
utt11 = "with arguments"
exp11 = \
"""var example = 0;;
function example_function(i){

  ;
  alert(<CURSOR>);
};
"""
utt12 = "between quotes"
exp12 = \
"""var example = 0;;
function example_function(i){

  ;
  alert("<CURSOR>");
};
"""
utt13 = "new value colon"
exp13 = \
"""var example = 0;;
function example_function(i){

  ;
  alert("new value: <CURSOR>");
};
"""
utt14 = "jump out"
exp14 = \
"""var example = 0;;
function example_function(i){

  ;
  alert("new value: "<CURSOR>);
};
"""
utt15 = "plus example"
exp15 = \
"""var example = 0;;
function example_function(i){

  ;
  alert("new value: " + example<CURSOR>);
};
"""