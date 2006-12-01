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
          
   def test_supported_languages(self):
       languages = self.interp.supported_languages()
       languages.sort()
       self.assert_equal(
          [None, 'C', 'perl', 'python'], 
          languages, 
          "List of supported languages was wrong")
       
   def test_index_cmds_by_topic(self):
       index = self.interp.index_cmds_by_topic()
       self.assert_equal({'C':     
                               [(['multiply', 'by'], AliasMeaning(" * ")),
                                (['multiplied', 'by'], AliasMeaning(" * ")),
                                (['times'], AliasMeaning(" * "))
                                ],
                          'python': 
                                [(['multiply', 'by'], AliasMeaning(" * ")),
                                 (['multiplied', 'by'], AliasMeaning(" * ")),
                                 (['times'], AliasMeaning(" * "))
                                 ],
                          'perl': 
                                 [(['multiply', 'by'], AliasMeaning(" * ")),
                                  (['multiplied', 'by'], AliasMeaning(" * ")),
                                  (['times'], AliasMeaning(" * "))
                                  ],
                          None: []
                         }, 
                         index, 
                         "Command indexes was not as expected.")

   def test_html_cmd_outline(self):
       index = self.interp.index_cmds_by_topic()
       outline = self.interp.html_cmd_outline(index)
       self.assert_equal("""
<HTML>
<HEADER>
<TITLE>VoiceCode: What can I say?</TITLE>
</HEADER>
<BODY>

<H1>VoiceCode: What can I say?</H1>

<H2>Index</H2>

<UL>
<LI><A HREF="#Global">Global</A>

<LI><A HREF="#C">C</A>

<LI><A HREF="#perl">perl</A>

<LI><A HREF="#python">python</A>

</UL>
<HR>""", 
                         outline,
                         "HTML for command outline was wrong.")
 
   def test_html_cmds_by_topic(self):
       index = self.interp.index_cmds_by_topic()
       by_topics = self.interp.html_cmds_by_topic(index)
       self.assert_equal("""
<H2><A NAME="Global">Global commands</A></H2>


<H2><A NAME="C">C commands</A></H2>


<H2><A NAME="perl">perl commands</A></H2>


<H2><A NAME="python">python commands</A></H2>


</BODY>
</HTML>""", 
                         by_topics,
                         "HTML for Index of commands by topic was wrong.")
 
   def test_html_cmds_alphabetically(self):
       index = self.interp.index_cmds_by_topic()
       html = self.interp.html_cmds_alphabetically(index)
       self.assert_equal("", 
                         html,
                         "HTML for alphabetical index of commands was wrong.")
 
 
 ###############################################################
 # Assertions.
 ###############################################################
 
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
               
