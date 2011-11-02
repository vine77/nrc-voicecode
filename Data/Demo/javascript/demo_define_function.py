# demo file generated with mediator test of JavascriptAcceptanceTest
#
utt1 = "new statement"
exp1 = "<CURSOR>;"

utt2 = "define variable"
exp2 = "var <CURSOR>;;"

utt3 = "example equals zero"
exp3 = "var example = 0<CURSOR>;;"

utt4 = "new statement"
exp4 = \
"""var example = 0;;
<CURSOR>;"""

utt5 = "define function"
exp5 = \
"""<<1 line>>
function <CURSOR>(){

};"""

utt6 = "example function"
exp6 = \
"""<<1 line>>
function example_function<CURSOR>(){

};"""

utt7 = "with argument i\\india"
exp7 = \
"""<<1 line>>
function example_function(i<CURSOR>){

};"""

utt8 = "do the following new statement"
exp8 = \
"""<<1 line>>
function example_function(i){

  <CURSOR>;
};"""

utt9 = "new statement"
exp9 = \
"""<<3 lines>>
  ;
  <CURSOR>;
};"""

utt10 = "alert"
exp10 = \
"""<<4 lines>>
  alert<CURSOR>;
};"""

utt11 = "with arguments"
exp11 = \
"""<<4 lines>>
  alert(<CURSOR>);
};"""

utt12 = "between quotes"
exp12 = \
"""<<4 lines>>
  alert("<CURSOR>");
};"""

utt13 = "new value colon"
exp13 = \
"""<<4 lines>>
  alert("new value: <CURSOR>");
};"""

utt14 = "jump out"
exp14 = \
"""<<4 lines>>
  alert("new value: "<CURSOR>);
};"""

utt15 = "plus example"
exp15 = \
"""<<4 lines>>
  alert("new value: " + example<CURSOR>);
};"""
