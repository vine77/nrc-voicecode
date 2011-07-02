# demo file generated with mediator test of CAcceptanceTest
#
utt1 = "comment line"
exp1 = \
"""
// <CURSOR>"""

utt2 = "test comment"
exp2 = "<<1 line>>// test_comment<CURSOR>"

utt3 = "new paragraph"
exp3 = \
"""<<1 line>>
// test_comment

<CURSOR>"""

utt4 = "begin long comment this"
exp4 = "<<3 lines>>/* this<CURSOR>"

utt5 = "new line"
exp5 = \
"""<<3 lines>>
/* this
   <CURSOR>"""

utt6 = "is an important"
exp6 = "<<4 lines>>   is_an_important<CURSOR>"

utt7 = "new line"
exp7 = \
"""<<4 lines>>
   is_an_important
   <CURSOR>"""

utt8 = "bit of information end long comment"
exp8 = "<<5 lines>>   bit_of_information*/<CURSOR>"

utt9 = "new paragraph"
exp9 = \
"""<<5 lines>>
   bit_of_information*/

<CURSOR>"""
