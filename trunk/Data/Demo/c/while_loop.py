# demo file generated with mediator test of CAcceptanceTest
#
utt1 = "['while','loop']"
exp1 = \
"""while (<CURSOR>)
  {

  }"""
utt2 = "['conditional','function','with','argument','index']"
exp2 = \
"""while (conditional_function(index<CURSOR>))
  {

  }"""
utt3 = "['do', 'the', 'following', 'some','stuff']"
exp3 = \
"""while (conditional_function(index))
  {
some_stuff<CURSOR>
  }"""
utt4 = "['empty','parens','semicolon']"
exp4 = \
"""<<2 lines>>
    some_stuff(); <CURSOR>
  }"""
utt5 = "['after','semi','new','line']"
exp5 = \
"""<<2 lines>>
    some_stuff();
    <CURSOR>
  }"""