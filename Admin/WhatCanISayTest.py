import debug
import VoiceCodeRootTest
import vc_globals
import os
import regression

from CmdInterp import AliasMeaning, CmdInterp, LSAlias
from WhatCanISay import WhatCanISay

class WhatCanISayTest(VoiceCodeRootTest.VoiceCodeRootTest):
   def __init__(self, name):
      VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
      
   def setUp(self):
       self.wciSay = WhatCanISay()
       interp = CmdInterp()
       interp.add_lsa(LSAlias(
                       ['multiply by', 'multiplied by', 'times'], 
                       {'C': ' * ', 'python': ' * ', 'perl': ' * '}))
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

       
   def test_This_is_how_you_load_a_WhatCanISay_with_commands_fromn_an_interpreter(self):
       interp = CmdInterp()
       self.wciSay.load_commands_from_interpreter(interp)
       
   def test_This_is_how_you_create_an_HTML_index_of_the_commands(self):
       html_index = self.wciSay.html_command_index()
 
##########################################################
# Unit tests
#
# These tests check the internal workings of the class.
##########################################################
        
   def test_load_commands_from_interpreter(self):
       interp = CmdInterp()
       interp.add_lsa(LSAlias(
                       ['multiply by', 'multiplied by', 'times'], 
                       {'C': ' * ', 'python': ' * ', 'perl': ' * '}))
       self.wciSay.load_commands_from_interpreter(interp)  
       
       self.assert_equal([None, 'C', 'perl', 'python'], self.wciSay.languages,
                         "List of supported languages was wrong.")  
       
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
                         self.wciSay.index, 
                         "Command indexes was not as expected.")
 
   def test_html_command_index(self): 
       html = self.wciSay.html_command_index()
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
<HR>
<H2><A NAME="Global">Global commands</A></H2>


<H2><A NAME="C">C commands</A></H2>


<H2><A NAME="perl">perl commands</A></H2>


<H2><A NAME="python">python commands</A></H2>


</BODY>
</HTML>""",
                          html,
                          "HTML for command index was wrong.")
 
   def test_html_cmd_outline(self):
       outline = self.wciSay.html_cmd_outline()
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
       html = self.wciSay.html_cmds_by_topic()
       self.assert_equal("""
<H2><A NAME="Global">Global commands</A></H2>


<H2><A NAME="C">C commands</A></H2>


<H2><A NAME="perl">perl commands</A></H2>


<H2><A NAME="python">python commands</A></H2>


</BODY>
</HTML>""", 
                         html,
                         "HTML for index of commands by topic was wrong.")
 
 
   def test_html_cmds_alphabetically(self):
       html = self.wciSay.html_cmds_alphabetically()
       self.assert_equal("", 
                         html,
                         "HTML for alphabetical index of commands was wrong.")
 
  
###############################################################
# Assertions.
###############################################################
 
