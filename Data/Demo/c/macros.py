# demo file generated with mediator test of CAcceptanceTest
#
utt1 = "['wrap','header']"
exp1 = \
"""#ifndef ACCEPTANCE_TEST_MACROS_CPP
#define ACCEPTANCE_TEST_MACROS_CPP

<CURSOR>


#endif"""

utt2 = "['pound', 'include','quotes','string','after','quotes']"
exp2 = \
"""<<3 lines>>
#include "str"<CURSOR>


#endif"""

utt3 = "['new','line']"
exp3 = \
"""<<3 lines>>
#include "str"
<CURSOR>


#endif"""

utt4 = "['pound', 'include','angle-brackets','string']"
exp4 = \
"""<<4 lines>>
#include <str<CURSOR>>


#endif"""

utt5 = "['after','angle']"
exp5 = \
"""<<4 lines>>
#include <str><CURSOR>


#endif"""

utt6 = "['new','paragraph']"
exp6 = \
"""<<4 lines>>
#include <str>

<CURSOR>


#endif"""
