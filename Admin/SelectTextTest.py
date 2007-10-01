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
      
    def tttest_This_is_how_you_select_text(self):
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
                   
        
    def tttest_This_is_how_you_select_in_explicit_direction(self):
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



    def tttest_This_is_how_you_select_through_or_until_text_from_cursor(self):
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

    def test_This_is_how_you_get_to_nearest_if_selection_is_there_already(self):
        self._open_empty_test_file('temp.py')
        self._insert_in_active_buffer('small = small + "abc"\nlarge = large + "def"\n')

        # until, cursor at pos already, take next one        
        self._say("after abc")
        self._assert_active_buffer_content_is(\
'''small = small + "abc<CURSOR>"
large = large + "def"
''')
        self._say(["select until", '"\\close-quote'])
        self._assert_active_buffer_content_with_selection_is(\
'''small = small + "abc<SEL_START>"
large = large + "def<SEL_END>"
''')

        # through, cursor at pos already, take this one:
        self._say("after abc")
        self._assert_active_buffer_content_is(\
'''small = small + "abc<CURSOR>"
large = large + "def"
''')
        self._say(["select through", '"\\close-quote'])
        self._assert_active_buffer_content_with_selection_is(\
'''small = small + "abc<SEL_START>"<SEL_END>
large = large + "def"
''')

    def test_This_test_of_enough_ranges_in_large_text(self):

        # large file, in order to test the visible range also
        # and more occurrences of ")" than can be held in the NatSpeak/natlink
        # range of ranges, VoiceCode must enhance this list!
        self._open_file(self._get_test_data_file_path('lots_of_parens_py'))
        self._goto_line(290)
        self._say("select center")
        self._say(["select through", ")\\close-paren"])
        self._assert_lines_with_selection_content_is(\
'''   <SEL_START>center = 1
   calc5 = (x.function1()<SEL_END> + y.function2()) /(z.function1() + z.function2())''')
        self._say(["next one"])
        self._assert_lines_with_selection_content_is(\
'''   <SEL_START>center = 1
   calc5 = (x.function1() + y.function2()<SEL_END>) /(z.function1() + z.function2())''')
        self._say(["previous one"])
        self._say(["previous one"])
        self._say(["previous one"])
        self._say(["previous one"])
        self._say(["previous one"])
        self._say(["previous one"])
        self._say(["previous one"])
        self._say(["previous one"])
        self._assert_lines_with_selection_content_is(\
'''   calc3 = (x.function1() + y.function2()) /( z.function1() + z.function2()<SEL_START>)
   calc4 = (x.function1() + y.function2()) /( z.function1() + z.function2())
   center<SEL_END> = 1''')
        
        


###############################################################
# Assertions.
# 
# Use these methods to check the state of the class.
###############################################################
