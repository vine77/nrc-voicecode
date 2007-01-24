import debug
import VoiceCodeRootTest

class TemporaryTest(VoiceCodeRootTest.VoiceCodeRootTest):
     
    def __init__(self, name):
        VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
    
    def setUp(self):
       self._init_simulator_regression(exclusive=0)
##       self._open_empty_test_file('blah.py')
##       self.source_buff = self._app().curr_buffer()
                                                         
    def tearDown(self):
        pass
      
###############################################################
# Assertions.
# 
# Use these methods to check the state of the class.
###############################################################

    def test_dictate_less_than(self):
        self._open_empty_test_file('temp.py')
        self._insert_in_active_buffer("hello\n")
        self._assert_active_buffer_content_is('hello\n<CURSOR>')
        self._say("variable less than three")
        self._assert_active_buffer_content_is('hello\nvariable < 3<CURSOR>')

    def test_dictate_greater_than(self):
        self._open_empty_test_file('temp.py')
        self._say("variable greater than four")
        self._assert_active_buffer_content_is('hello\nvariable < 3<CURSOR>')


    def test_dictate_less_than_compound(self):
        self._open_empty_test_file('temp.py')
        self._say("variable less-than five")
        self._assert_active_buffer_content_is('hello\nvariable < 5<CURSOR>')

    def test_dictate_greater_than_compound(self):
        self._open_empty_test_file('temp.py')
        self._say("variable greater-than six")
        self._assert_active_buffer_content_is('hello\nvariable > 6<CURSOR>')


