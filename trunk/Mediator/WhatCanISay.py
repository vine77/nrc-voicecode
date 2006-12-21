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
from HTMLgen import *
import debug
from Object import Object
import pprint
import webbrowser
import re, os
reIsInt = re.compile(r'^\d+$')
reIsLetter = re.compile(r'^[a-zA-Z]$')



class WhatCanISay(Object):
    """
    A class for generating, and displaying an index of all the active
    voice commands.

    Written mainly by Quintijn Hoogenboom, Dec 2006.

    Collects all commands (LSA and CSC (later)), and puts them in a website.

    The website is placed on VCODE_HOME/Data/WhatCanISay.


    
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
        self.create_html_folder()            
        self.languages = cmd_interp.supported_languages()
        Commands = cmd_interp.commands
        Symbols = cmd_interp.known_symbols.abbreviations
        for k,v in Symbols.items():
            print k, Symbols[k]
            
        Dir = dir(Commands)
       # for i in Dir:
       #     print 'commands %s: %s'% (i, type(getattr(Commands, i)))
        self.languages.sort()
        for a_language in self.languages:
            self.index[a_language] = []
            wTrie = cmd_interp.language_specific_aliases[a_language]
            for an_LSA in wTrie.items():
                wordList, entry = an_LSA
                self.index[a_language].append((wordList, entry))

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

    def show_cmds(self, cmd_interp, currLang):
        print 'currLang: %s'% currLang
        self.language = currLang
        self.load_commands_from_interpreter(cmd_interp)
        allCommands = {}
        for lang in self.index:
            part = self.index[lang]
            if lang == None:
                lang = 'global'
            for tup in part:
                words = ' '.join(tup[0])  # ['is', 'equal', 'to'] -->> 'is equal to')
                written = getattr(tup[1], 'written_form', '')
##                print 'words: %s, written: %s'% (words, written)
                if not written:
##                    print 'empty, lang: %s'% lang
                    allCommands.setdefault(lang, []).append((words, written))
                elif reIsInt.match(written):
##                    print 'number'
                    allCommands.setdefault('numbers', []).append((words, written))
                elif reIsLetter.match(written):
##                    print 'letter'
                    allCommands.setdefault('letters', []).append((words, written))
                else:
##                    print 'else'
                    allCommands.setdefault(lang, []).append((words, written))

        allCommands['Actual'] = allCommands['global'][:]

        # here I make an entry for actual commands (LSA), being global + language specific:
        for c in allCommands[self.language]:
            if c not in allCommands['Actual']:
                allCommands['Actual'].append(c)
                
        # here I make two groups of each, sorted by written and sorted by spoken form:
        for group, cmds in allCommands.items():
            if group not in ('numbers','letters'):
                cmds = self.sortBySpoken(cmds)
                allCommands[group + 'sbs'] = cmds[:]
            cmds = self.sortByWritten(cmds)
            if group not in ('numbers','letters'):
                del allCommands[group]
                group = group + 'sbw'
            allCommands[group] = cmds[:]
            
        self.allCommands = allCommands
        
        self.pages = self.allCommands.keys()
        self.pages.sort()
        
        self.html_command_index()
        self.html_command_pages()
        indexPage = os.path.join(self.htmlFolder, 'index.html')
        webbrowser.open_new(indexPage)

    def create_html_folder(self):
        """create a folder for the simple website"""
        self.htmlFolder = r'C:\vcodeWhat'
        home = os.environ['VCODE_HOME']
        print 'home: %s'% home
        self.htmlFolder = os.path.join(home, 'Data', 'whatCanISay')
        try:
            os.makedirs(self.htmlFolder)
            print 'warning: whatCanISay folder did not exist, stylesheet will not be available'
        except:
            pass
        if not os.path.isdir(self.htmlFolder):
            raise Exception('not a valid directory for What Can I Say website: %s'% self.htmlFolder)
        
    
    
    def html_command_index(self):
        """make the index page of the website"""
        doc = SimpleDocument()
        doc.stylesheet = "vc.css"

        doc.append(self.html_header('index'))
        tlpage = FullTable(Class="page")
        trpage = TR()
        # produce the menu (left):
        leftMenu = self.getMenu('index')
        trpage.append(leftMenu)
        # produce the body:
        text =[ 'this is the index page, more info will follow',
                'sbs: sorted by spoken form',
                'sbw: sorted by written form']
        trpage.append(TD(map(Paragraph, text), Class="body"))
        tlpage.append(trpage)
        doc.append(tlpage)
        outfile = os.path.join(self.htmlFolder, 'index.html')
   
        print 'making page: %s'% outfile
        doc.write(outfile)

    def getMenu(self, me):
        """produce a menu with me without link

        me = name of calling page

        """
        td = TD(Class="leftmenu")
        for p in self.pages:
            niceP = p
#            if niceP.startswith('only'):
#                niceP = 'only ' + niceP[4:]
#            if niceP.endswith('sbs'):
#                niceP = niceP[:-3] + '(sorted by spoken)'
#            if niceP.endswith('sbw'):
#                niceP = niceP[:-3] + '(sorted by written)'
                
            if p == me:
                td.append(Paragraph(niceP, Class="lefton"))
            else:                
                td.append(Paragraph(Href('%s.html'% p, niceP), Class="leftoff"))
        return td

    def html_command_pages(self):
        """generate the pages"""

        for p in self.pages:
            self.html_command_page(p)

    def html_command_page(self, page):
        """generate one page, with a menu to the other pages"""
        doc = SimpleDocument()
        doc.stylesheet = "vc.css"
        content = self.allCommands[page]
        
        doc.append(self.html_header(page))
        tlpage = FullTable(Class="page")
        trpage = TR()
        # produce the menu (left):
        leftMenu = self.getMenu(page)
        trpage.append(leftMenu)

        # now the contents:        
        tl = FullTable(Class="body")
        tr = TR()
        perCol = 3
        tdspacer = TD("&nbsp;", Class="spacer")
        rows = len(content)/perCol
        if len(content)%perCol:
            rows += 1
        cellNum = 0
        for start in range(rows):
            for col in range(start, len(content), rows):
                cellNum += 1
                k, v = content[col]
                tr.append(TD(v, Class="spoken%s"% (cellNum%2,)))
                tr.append(TD(k, Class="written%s"% (cellNum%2,)))
                tr.append(tdspacer())
            tl.append(tr)
            tr.empty()
        
        trpage.append(TD(tl, Class="body"))
        tlpage.append(trpage)
        doc.append(tlpage)
        outfile = os.path.join(self.htmlFolder, '%s.html'% page)
        print 'making page: %s'% outfile
        doc.write(outfile)
                  
    def html_header(self, page):
        """produce the header at the top of the html page, with the name mentioned"""
        im = Img('vcodeuser.jpg', alt='what can i say website for voicecoder')
        if page == 'index':
            pass
        else:
            im = Href('index.html', im)
        text = "VoiceCoder What Can I Say (%s): %s"% (self.language, page)
        tl = FullTable(Class="header")
        return Div(tl(TR(TD(text, Class="bannertext"), TD(im, Class="bannerim"))), Class="header")

    def sortBySpoken(self, cmds):
        """sort list of tuples by the first key

        note the presentation is the other way
        each cmd is (spoken, written), but presentation in
        html is (written, spoken)

        """
        cmds.sort()
        return cmds

    def sortByWritten(self, cmds):
        """sort list of tuples by the second key
        
        note the presentation is the other way
        each cmd is (spoken, written), but presentation in
        html is (written, spoken)

        """
        decorated = [(s,w) for (w,s) in cmds]
        decorated.sort()
        undecorated = [(s,w) for (w,s) in decorated]
        return undecorated

# defaults for vim - otherwise ignore
# vim:sw=4
