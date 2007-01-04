import debug
import VoiceCodeRootTest
class BasicBufferTest(VoiceCodeRootTest.VoiceCodeRootTest):
   """test and demonstrate some of the basic test facilities

   also see road map to the test harness (QH, dec 2006)
   """ 
   def __init__(self, name):
       VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
      
   def setUp(self):
       self._init_simulator_regression()
       self._open_empty_test_file('temp.py')
       self.sourcebuff = self._app().curr_buffer()

##########################################################
# Documentation tests
#
# These tests illustrate how to use the class
# Test and demonstrate basic test functions, from VoiceCodeRootTest
#
#
##########################################################
      

##########################################################
# Unit tests
#
# These tests check the internal workings of the class.
##########################################################
   def test_Move_around_in_buffer(self):
      """Showing the basic moving around with buffer functions
      """

      # putting something in buffer and testing length and cursor position
      self._assert_cur_pos_is(0, "Cursor starts startswith zero")
      self.sourcebuff.insert("line 1\nline 2\n")
      self.assert_equal(14, self.sourcebuff.len(), "The length of the buffer")

