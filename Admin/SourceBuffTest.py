import debug
import VoiceCodeRootTest

class SourceBuffTest(VoiceCodeRootTest.VoiceCodeRootTest):
     
    def __init__(self, name):
        VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
    
    def setUp(self):
      self._init_simulator_regression(exclusive=0)
      self._open_empty_test_file('blah.py')
      self.source_buff = self._app().curr_buffer()
      self.source_buff.insert("line1\nline2\nline3\nline4")
      self.source_buff.goto(0)
                                                         
    def tearDown(self):
        pass
        
##########################################################
# Documentation tests
#
# These tests illustrate how to use the class.
##########################################################


##########################################################
# Unit tests
#
# These tests check the internal workings of the class.
##########################################################

    def test_get_text_of_line(self):
       self.source_buff.goto_line(0)
       got_text = self.source_buff.get_text_of_line(3)
       self.assert_equal("line3", got_text, 
                         "Got wrong content of line 3.")
    
    
       self.source_buff.goto_line(2)
       got_text = self.source_buff.get_text_of_line()
       self.assert_equal("line2", got_text, 
                         "Got wrong content of current line when current line was line no 2.")
                         
       got_text = self.source_buff.get_text_of_line(1)
       self.assert_equal("line1", got_text, 
                         "Got wrong content of line 1")
                         
       got_text = self.source_buff.get_text_of_line(4)
       self.assert_equal("line4", got_text, 
                         "Got wrong content of last line")
                         
       got_text = self.source_buff.get_text_of_line(999)
       self.assert_equal("line4", got_text, 
                         "Asking for content of line beyond length of buffer should have returned content of last line.")
                         
       got_text = self.source_buff.get_text_of_line(-1)
       self.assert_equal("line1", got_text, 
                         "Asking for content of line before first line, should return content of first line.")
      
      
###############################################################
# Assertions.
# 
# Use these methods to check the state of the class.
###############################################################