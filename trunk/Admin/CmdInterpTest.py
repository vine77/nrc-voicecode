import debug
from CmdInterp import CmdInterp
from CmdInterp import LSAlias
from CmdInterp import AliasMeaning
import VoiceCodeRootTest
import vc_globals
import os
import regression
from SpokenUtterance import MockSpokenUtterance

class CmdInterpTest(VoiceCodeRootTest.VoiceCodeRootTest):
   def __init__(self, name):
      VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
      
   def setUp(self):
       self._init_simulator_regression()
       self.interp = self._command_interpreter()

##########################################################
# Documentation tests
#
# These tests illustrate how to use the class.
##########################################################

      
   def test_this_is_how_you_create_a_CmdInterp(self):
       interp = CmdInterp()
       
   def test_this_is_how_you_add_a_known_symbol(self):
       self.interp.add_symbol('thiIsASymbol')
       

##########################################################
# Unit tests
#
# These tests check the internal workings of the class.
##########################################################


       
   def test_symbol_containing_an_LSA(self):
       self._open_empty_test_file('test.c')
       self.interp.add_symbol('MyVec_INT')
       utterance = MockSpokenUtterance(['my', 'vector', 'int'])
       self.interp.interpret_utterance(utterance, 
                                       self._app())
       self._assert_active_buffer_content_is('MyVec_INT', 
               "Failed to correctly translate a symbol that contained the spoken form for a LSA.")
       

 
###############################################################
# Assertions.
# 
# Use these methods to check the state of the class.
###############################################################
