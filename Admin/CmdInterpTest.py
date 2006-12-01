import debug
from CmdInterp import CmdInterp
from CmdInterp import LSAlias
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
          
   def test_supported_languages(self):
       languages = self.interp.supported_languages()
       languages.sort()
       self.assert_sequences_have_same_content(
          [None, 'C', 'perl', 'python'], 
          languages, 
          "List of supported languages was wrong")
       
   def test_index_cmds_by_topic(self):
       index = self.interp.index_cmds_by_topic()
       self.assert_cmd_index_is({'C':     
                                    [(['multiply', 'by'], None, None),
                                     (['multiplied', 'by'], None, None),
                                     (['times'], None, None)],
                                 'python': 
                                    [(['multiply', 'by'], None, None),
                                     (['multiplied', 'by'], None, None),
                                     (['times'], None, None)],
                                 'perl': 
                                    [(['multiply', 'by'], None, None),
                                     (['multiplied', 'by'], None, None),
                                     (['times'], None, None)],
                                 None: []
                                 }, 
                                index, 
                                "Command indexes were not the same")
       self.fail('test not finalized yet')
 
   def assert_cmd_index_is(self, expected, got, mess):
       self.assert_dicts_have_same_keys(expected, got, 
              mess + "\nCommand index did not cover same list of languages")
       languages = expected.keys()
       for a_lang in languages:
           exp_this_lang = expected[a_lang]
           got_this_lang = got[a_lang]
           self.assert_sequences_have_same_length(exp_this_lang, got_this_lang,
                  mess + "\nList of commands for language %s differed." % a_lang)
#           for  in exp_this_lang:
               
