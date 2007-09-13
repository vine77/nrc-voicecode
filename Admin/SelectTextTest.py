import debug
import cont_gen
import VoiceCodeRootTest
from vc_globals import all_languages, c_style_languages
import sr_grammars  # for test of WinGram function

class SelectTextTest(VoiceCodeRootTest.VoiceCodeRootTest):
    """Test different select results, with and without "through"

    """   
    def __init__(self, name):
        VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
      
    def setUp(self):
        self._init_simulator_regression()

##########################################################
# Documentation tests
#
# These tests illustrate how to use the class.
##########################################################
      
    def test_This_is_how_you_select_text(self):
        self._open_empty_test_file('temp.py')
        self._insert_in_active_buffer("small = small + 1\nlarge = large + small\n")
        self._say("select small")
        self._assert_active_buffer_content_is(\
'''small = small + 1
large = large + small<CURSOR>
''')
      
        self._say("previous one")
        self._assert_active_buffer_content_is(\
'''small = small<CURSOR> + 1
large = large + small
''')

        self._goto(0)
        self._assert_active_buffer_content_is(\
'''<CURSOR>small = small + 1
large = large + small
''')
        self._say("select large")
        self._assert_active_buffer_content_is(\
'''small = small + 1
large<CURSOR> = large + small
''')
      
        self._say(["select", "+\\plus-sign"])
        self._assert_active_buffer_content_is(\
'''small = small +<CURSOR> 1
large = large + small
''')

      
        self._say("next one")
        self._assert_active_buffer_content_is(\
'''small = small + 1
large = large +<CURSOR> small
''')

    def test_This_is_how_you_select_through_text(self):
        self._open_empty_test_file('temp.py')
        self._insert_in_active_buffer("small = small + 1\nlarge = large + small\n")
        self._say("select small through large")
        self._assert_active_buffer_content_with_selection_is(\
'''small = <SEL_START>small + 1
large<SEL_END> = large + small
''')
                   
        
    def test_This_is_how_you_select_in_explicit_direction(self):
        self._open_empty_test_file('temp.py')
        self._insert_in_active_buffer("small = small + 1\ncenter = 3\nlarge = large + small\n")
        self._say("select center")
        self._say(["select next", "small"])
        self._assert_active_buffer_content_with_selection_is(\
'''small = small + 1
center = 3
large = large + <SEL_START>small<SEL_END>
''')
        self._say(["select previous", "small"])
        self._assert_active_buffer_content_with_selection_is(\
'''small = <SEL_START>small<SEL_END> + 1
center = 3
large = large + small
''')


        self._say(["select next",  "=\\equal-sign"])
        self._assert_active_buffer_content_with_selection_is(\
'''small = small + 1
center <SEL_START>=<SEL_END> 3
large = large + small
''')
        self._say(["select previous",  "+\\plus-sign"])
        self._assert_active_buffer_content_with_selection_is(\
'''small = small <SEL_START>+<SEL_END> 1
center = 3
large = large + small
''')



    def test_This_is_how_you_select_through_or_until_text_from_cursor(self):
        self._open_empty_test_file('temp.c')
        self._insert_in_active_buffer("small = small + 1;\ncenter = 3\nlarge = large + small\n")
        self._say("select center")
        self._assert_active_buffer_content_with_selection_is(\
'''small = small + 1;
<SEL_START>center<SEL_END> = 3
large = large + small
''')
        # until::::::::::
        # note: select until is one grammar word:
        self._say(["select until", "small"])
        self._assert_active_buffer_content_with_selection_is(\
'''small = small + 1;
<SEL_START>center = 3
large = large + <SEL_END>small
''')

        self._say(["previous", "one"])
        self._assert_active_buffer_content_with_selection_is(\
'''small = small<SEL_START> + 1;
center<SEL_END> = 3
large = large + small
''')
        # through::::
        self._say("select center")
        self._assert_active_buffer_content_with_selection_is(\
'''small = small + 1;
<SEL_START>center<SEL_END> = 3
large = large + small
''')
        # note: select until is one grammar word:
        self._say(["select through", "small"])
        self._assert_active_buffer_content_with_selection_is(\
'''small = small + 1;
<SEL_START>center = 3
large = large + small<SEL_END>
''')

        self._say(["previous", "one"])
        self._assert_active_buffer_content_with_selection_is(\
'''small = <SEL_START>small + 1;
center<SEL_END> = 3
large = large + small
''')

        self._say("select center")
        self._assert_active_buffer_content_with_selection_is(\
'''small = small + 1;
<SEL_START>center<SEL_END> = 3
large = large + small
''')
        # back until::::::::::
        # note: select until is one grammar word:
        self._say(["select back until", "small"])
        self._assert_active_buffer_content_with_selection_is(\
'''small = small<SEL_START> + 1;
center<SEL_END> = 3
large = large + small
''')

        self._say(["next", "one"])
        self._assert_active_buffer_content_with_selection_is(\
'''small = small + 1;
<SEL_START>center = 3
large = large + <SEL_END>small
''')
        # back through::::
        self._say("select center")
        self._assert_active_buffer_content_with_selection_is(\
'''small = small + 1;
<SEL_START>center<SEL_END> = 3
large = large + small
''')
        # note: select until is one grammar word:
        self._say(["select back through", "small"])
        self._assert_active_buffer_content_with_selection_is(\
'''small = <SEL_START>small + 1;
center<SEL_END> = 3
large = large + small
''')

        self._say(["previous", "one"])
        self._assert_active_buffer_content_with_selection_is(\
'''<SEL_START>small = small + 1;
center<SEL_END> = 3
large = large + small
''')
        self._say("next one next one")
        self._assert_active_buffer_content_with_selection_is(\
'''small = small + 1;
<SEL_START>center = 3
large = large + small<SEL_END>
''')
        # nothing changes any more:
        self._say("next one")
        self._assert_active_buffer_content_with_selection_is(\
'''small = small + 1;
<SEL_START>center = 3
large = large + small<SEL_END>
''')



        



##########################################################
# Unit tests
#
# These tests check the internal workings of the class.
##########################################################
    def test_get_smaller_ranges_only(self):
        dummy = 1
        win_gram = sr_grammars.WinGram(dummy)
        ranges = [(1,3), (5,10), (5,20), (30,40), (35,40)]
        expected = [(1,3), (5,10), (35,40)]
        smaller_ranges = win_gram.get_smaller_ranges_only(ranges)
        self.assert_equal(expected, smaller_ranges, "get_smaller_ranges_only result not as expected")

###############################################################
# Assertions.
# 
# Use these methods to check the state of the class.
###############################################################
