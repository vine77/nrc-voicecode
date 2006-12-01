import debug
from CmdInterp import CmdInterp
from CmdInterp import LSAlias
from CmdInterp import AliasMeaning
import VoiceCodeRootTest
import vc_globals
import os
import regression

class CmdInterpTest(VoiceCodeRootTest.VoiceCodeRootTest):
   def __init__(self, name):
      VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
      
   def setUp(self):
       self.interp = CmdInterp()
       self.interp.add_lsa(
               LSAlias(['multiply by', 'multiplied by', 'times'], 
                       {'C': ' * ', 'python': ' * ', 'perl': ' * '}))
      
   def test_CmdInterp_init(self):
       interp = CmdInterp()

 
