import debug
import VoiceCodeRootTest
import time

class TextModeTest(VoiceCodeRootTest.VoiceCodeRootTest):
   """Test dictation of normal text.
   """
   
   def __init__(self, name):
      VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
      
   def setUp(self):
      self._init_simulator_regression(exclusive=0)
      
##########################################################
# Documentation tests
#
# These tests illustrate how to use the class.
##########################################################
      

   def test_toggle_text_mode(self):
       self._open_file(VoiceCodeRootTest.foreground_py)   
       self._say(['new', 'statement', 'above'])

       self._say(['text', 'mode', 'on'], never_bypass_sr_recog=1)
       self._say(['this', 'should', 'be', 'typed', 'as', 'normal', 'text'], 
                 never_bypass_sr_recog=1)
       time.sleep(3)
# see if adding this makes any difference
       self._app().process_pending_updates()
       time.sleep(3)
       self._app().process_pending_updates()
       self._assert_current_line_content_is("this should be typed as normal text",
                                            "Text dictated with text mode on was wrong.")
       
       
