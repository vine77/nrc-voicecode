##############################################################################
# VoiceCode, a programming-by-voice environment
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# (C) 2000, National Research Council of Canada
#
##############################################################################

import debug
from Object import Object

class WhatCanISay(Object):
    """
    A class for generating, and displaying an index of all the active
    voice commands.
    """
    def __init__(self, **args):
        self.deep_construct(WhatCanISay, 
                            {'index': {}, 'languages': [],}, 
                            args)

    def load_commands_from_interpreter(self, cmd_interp):
        self.index = {}

        #
        # First, index the LSAs
        #
        self.languages = cmd_interp.supported_languages()
        self.languages.sort()
        for a_language in self.languages:
            self.index[a_language] = []
            wTrie = cmd_interp.language_specific_aliases[a_language]
            for an_LSA in wTrie.items():
                debug.trace('WhatCanISay.load_commands_from_interpreter', 
                            '** an_LSA=%s, len an_LSA: %s' % 
                            (an_LSA, len(an_LSA)))
                wordList, entry = an_LSA
                self.index[a_language].append((wordList, entry))
                debug.trace('WhatCanISay.load_commands_from_interpreter', 
                            '** written %s:  %s'% (' '.join(wordList), entry.written()))
##
##                for at in dir(entry):
##                    if at == '__doc__' or not at.startswith('__'):
##                        print 'at: %s: %s'% (at, getattr(entry, at))
               
##                spoken, written = sr_interface.spoken_written_form(an_LSA.voc_entry)
##                print 'spoken: %s, written: %s'% (spoken, written)
##                written = re.sub('\n', '\\n', written)
##                descr = 'insert \'written\''
##                for a_topic in an_LSA.topics:                    
##                    self.html_create_index_entry(a_language, a_topic, spoken, descr)

        #
        # Then the CSCs
        #
##        for a_CSC in self.cmd_index:
##            for spoken in a_CSC.spoken_forms:
##                for a_topic in a_CSC.topics:
##                    for a_context, an_action in a_CSC.meanings:
##                        descr = an_action.doc()
##                        try:
##                            a_language = a_context.language
##                        except:
##                            # context is not a language context
##                            a_language = None
##                        if a_language:
##                            self.html_create_index_entry(a_language, a_topic, spoken, descr)

    def show_cmds(self, cmd_interp):    
        self.load_commands_from_interpreter(cmd_interp)
        print self.html_command_index()
    
    
    def html_command_index(self):
        html = ''
        html = html + self.html_cmd_outline()
        html = html + self.html_cmds_by_topic()
        html = html + self.html_cmds_alphabetically()
        return html

    def html_cmd_outline(self):
        html = """
<HTML>
<HEADER>
<TITLE>VoiceCode: What can I say?</TITLE>
</HEADER>
<BODY>

<H1>VoiceCode: What can I say?</H1>

<H2>Index</H2>

<UL>"""

        for a_language in self.languages:
            if not a_language:
                a_lang_name = 'Global'
            else:
                a_lang_name = a_language

            html = html +  "\n" + \
                      '<LI><A HREF="#%s">%s</A>\n' % (a_lang_name, a_lang_name)
   
# AD: Not sure what you mean by a topic, so I'm commenting this out for now.
#
#            topics = index[a_language].keys().sort()
#            for a_topic in topics:
#                url = a_lang_name + '-' + a_topic
#                html = html + "\n" + \
#                          '      <LI><A HREF="#%s">%s</A>' % (url, a_topic)
#            html = html + "\n" + \
#                      '   </UL>'

        html = html + "\n" + '</UL>\n<HR>'
        
        return html

    def html_cmds_by_topic(self):
        html = ""    
        for a_language in self.languages:        
            if not a_language:
                a_lang_name = 'Global'
            else:
                a_lang_name = a_language

            html = html + "\n" + \
                   '<H2><A NAME="%s">%s commands</A></H2>\n\n' % (a_lang_name, a_lang_name)

# AD: Not sure what you mean by a topic, so I'm commenting this out for now.        
#            topics = index[a_language].keys().sort()
#            for a_topic in topics:
#                url = a_lang_name + '-' + a_topic
#                print '<H3><A NAME="%s">%s</A></H3>\n\n' % (url, a_topic)
#                for spoken, descr in index[a_language][a_topic]:
#                    print '<STRONG>"%s"</STRONG><BR><DD>%s' % (spoken, descr)
#        

        html = html + "\n" + '</BODY>\n</HTML>'
        
        return html

    def html_cmds_alphabetically(self):
        return ''

# defaults for vim - otherwise ignore
# vim:sw=4
