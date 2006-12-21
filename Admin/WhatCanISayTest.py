import debug
import VoiceCodeRootTest
import vc_globals
import os
import regression

from CmdInterp import AliasMeaning, CmdInterp, LSAlias
from WhatCanISay import WhatCanISay

# test data:
expected_languages = ['C', 'perl', 'python']
expected_languages.sort()
lsa_multiply_list = ['multiply by', 'multiplied by', 'times']
lsa_multiply_dict  = dict.fromkeys(expected_languages, ' * ')

# expected index contents of the 3 languages: values of self.index:
index_contents =  [(['multiply', 'by'], AliasMeaning(" * ")),
                   (['multiplied', 'by'], AliasMeaning(" * ")),
                   (['times'], AliasMeaning(" * "))
                  ]

expected_index = dict.fromkeys(expected_languages, index_contents)
expected_index[None] = []

class WhatCanISayTest(VoiceCodeRootTest.VoiceCodeRootTest):
   def __init__(self, name):
      VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
      
   def setUp(self):
       self.wciSay = WhatCanISay()
       interp = CmdInterp()
       interp.add_lsa(LSAlias(lsa_multiply_list, lsa_multiply_dict))
       self.wciSay.load_commands_from_interpreter(interp)

      
##########################################################
# Documentation tests
#
# These tests illustrate how to use the class.
##########################################################
      
      
   def test_This_is_how_you_create_a_WhatCanISay_instance(self):
       wciSay = WhatCanISay()
       interp = CmdInterp()
       wciSay.load_commands_from_interpreter(interp)

       
#   def test_This_is_how_you_load_a_WhatCanISay_with_commands_fromn_an_interpreter(self):
#       interp = CmdInterp()
#       self.wciSay.load_commands_from_interpreter(interp)
       
#   def test_This_is_how_you_create_an_HTML_index_of_the_commands(self):
#       html_index = self.wciSay.html_command_index()
 
##########################################################
# Unit tests
#
# These tests check the internal workings of the class.
##########################################################
        
   def test_load_commands_from_interpreter(self):
       interp = CmdInterp()
       interp.add_lsa(LSAlias(lsa_multiply_list, lsa_multiply_dict))
       self.wciSay.load_commands_from_interpreter(interp)  
       actual_languages = self.wciSay.languages
       self.assert_(None in actual_languages, "None is not in supported languages")
       actual_languages.remove(None)
       actual_languages.sort()
       self.assert_equal(expected_languages, actual_languages,
                         "List of supported languages was wrong.")  
       
       self.assert_equal(expected_index,
                         self.wciSay.index, 
                         "Command indexes was not as expected.")
 
   def test_html_command_index(self):
       pass
 
 
###############################################################
# Assertions.
###############################################################
 
