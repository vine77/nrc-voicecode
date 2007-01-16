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
from debug import trace
from Object import Object
import vc_globals
import pprint
import webbrowser
import re, os
reIsInt = re.compile(r'^\d+$')
reIsLetter = re.compile(r'^[a-zA-Z]$')
from copy import copy
from cont_gen import *
from Context import scope_order, valid_scope

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
                            {'lsa_index': {}, 'csc_index': {}, 'languages': [],}, 
                            args)

    def load_commands_from_interpreter(self, cmd_interp):
        """Get a dictionary of all commands from the interpreter

        The list of languages goes in self.languages

        The LSA commands are put in self.lsa_index, a dict
         with keys None and all the possible languages.
         and values:  a list of tuples (wordList, LSAentry)

        The CSC commands are put in self.csc_index.
         with keys: the languages
         with values: a dict with keys 'spoken form'
                             and values: [(context key, action),...]

        """
        self.create_html_folder()            
        self.languages = cmd_interp.supported_languages()
        self.languages.sort()
        
        self.index_lsas(cmd_interp)
        self.index_cscs(cmd_interp)        


    def index_lsas(self, cmd_interp):
        self.lsa_index = {}
        for a_language in self.languages:
            self.lsa_index[a_language] = []
            wTrie = cmd_interp.language_specific_aliases[a_language]
            for an_LSA in wTrie.items():
                wordList, entry = an_LSA
                spoken_form_text = ' '.join(wordList)
                self.lsa_index[a_language].append((spoken_form_text, entry))

    def index_cscs(self, cmd_interp):
        self.csc_index = {}
        for a_language in self.languages:
            if a_language == None:
                continue
            self.csc_index[a_language] = {}
        
        wTrie = cmd_interp.commands
        for a_csc_entry in wTrie.items():
            the_spoken_form = ' '.join(a_csc_entry[0])
            the_meanings = a_csc_entry[1]
            trace('WhatCanISay.index_cscs', "** Processing a_csc_entry: the_spoken_form: %s, the_meanings: %s" % \
                  (the_spoken_form, the_meanings))
            self.index_contextual_meanings(the_spoken_form, the_meanings)
           
    def index_contextual_meanings(self, spoken_form, meanings_dict):
        contexts = meanings_dict.contexts.values()
        for a_context in contexts:
           trace('WhatCanISay.index_contextual_meanings', "** Processing a_context=%s" % repr(a_context))           
           for a_language in self.languages:
               if a_language == None:
                   continue
               if self.context_applies_for_lang(a_language, a_context):
                   a_context_key = a_context.equivalence_key()
         #          a_context_scope = a_context.scope()
                   trace('WhatCanISay.index_contextual_meanings', 
                         "** a_context=%s, applies for a_language=%s" % \
                            (a_context, a_language))
                   action_for_this_context = meanings_dict.actions[a_context_key]
                   self.csc_index[a_language].setdefault(spoken_form, []).append((a_context,
                                                                                  action_for_this_context))
                 
           
    def context_applies_for_lang(self, language, context):
        trace
        ('WhatCanISay.context_applies_for_lang', "** language=%s, context=%s" %(language, context))
        answer = False        
        if isinstance(context, ContLanguage) and \
            language in context.language:
           answer = True
        elif isinstance(context, ContAny):
           answer = True
        return answer

    def create_cmds(self, cmd_interp, curr_lang):
        self.language = curr_lang
        self.load_commands_from_interpreter(cmd_interp)
        self.create_lsa_cmds(cmd_interp, self.language)
        self.create_csc_cmds(cmd_interp, self.language)

    def create_lsa_cmds(self, cmd_interp, curr_lang):
        """Create all lsa commands, separated by language

        First all LSA commands are extracted from self.lsa_index.

        Commands that are in None, or appear to be equal in all languages come in language 'global'.

        The wordList is joined into a string,
        The written_form is extracted from the LSA entry.

        the result is in self.all_commands

        """
        all_commands = {}
        for lang in self.lsa_index:
            part = self.lsa_index[lang]
            if lang == None:
                lang = 'common'
            all_commands[lang] = []
            for tup in part:
                words = tup[0]
                written = getattr(tup[1], 'written_form', '')
                if not written:
                    all_commands[lang].append((words, written))
                elif reIsInt.match(written):
                    all_commands.setdefault('numbers', []).append((words, written))
                elif reIsLetter.match(written):
                    all_commands.setdefault('letters', []).append((words, written))
                else:
                    all_commands[lang].append((words, written))

        # manipulating all_commands (in place):
##        print '1: %s'% all_commands.keys()
        self.extract_common_commands(all_commands)
##        print '2: %s'% all_commands.keys()
        self.elaborate_commands(all_commands)
##        print '3: %s'% all_commands.keys()
        self.lsa_commands = all_commands


    def create_csc_cmds(self, cmd_interp, curr_lang):
        """Create all csc commands, separated by language

        """
        all_commands = {}
        for lang, part in self.csc_index.items():
            if lang == None:
                raise ValueError("value of self.csc_index[None] should not exist")
            all_commands[lang] = []
            for words, action_tuple in part.items():
                action_list = []
                for a_context, act in action_tuple:
                    written = self.get_written_form_from_action(act)
                    a_context_equivalence = a_context.equivalence_key()
                    a_context_scope = a_context.scope()
                    action_list.append((a_context_equivalence, a_context_scope, written))
                all_commands[lang].append((words, action_list))
        self.csc_commands = all_commands

    def get_written_form_from_action(self, action):
        try:
            doc = action.doc()
        except AttributeError:
            doc = 'no doc for %s'% repr(action).split()[0][1:]
        return doc

    def extract_common_commands(self, all_commands):
        """change (inplace) the Commands dict

        input:  all_commands: a dict like {'common': [(...), (...)], 'C': [(...), ...],
                                     'python': [(...), (...)], ...}
                              a dict like {'C': [(...), ...],
                                     'python': [(...), (...)], ...} ('common' created in this function)
        output: tuples that are common to all specific languages are put in 'common' and
        deleted from specific.

        'letters' and 'numbers' are kept separate and ignored in this function

        """
        specific_languages = [k for k in all_commands if k not in ('common', 'letters', 'numbers')]
        common = all_commands.setdefault('common', [])
        if len(specific_languages) <= 1:
            return
        first, rest = all_commands[specific_languages[0]], [all_commands[k] for k in specific_languages[1:]]
        # first changes, so copy the list:
        for item in copy(first):
            for c in rest:
                if item not in c: break
            else:
                # command is global, add and delete:
                if item not in common:
                    common.append(item)
                for c in rest:
                    c.remove(item)
                first.remove(item)
    
    def elaborate_commands(self, all_commands):
        """Extend the commands dictionary

        1. with actual commands
        2. make two versions sbs (sorted by spoken), sbw (sorted by written)
        """
        # here I make an entry for actual commands (LSA), being global + language specific:
        all_commands.setdefault('actual', copy(all_commands['common']))
        # we have at least actual and common commands, possibly empty.
        if self.language in all_commands:
            for c in all_commands[self.language]:
                if c not in all_commands['actual']:
                    all_commands['actual'].append(c)
                
        # here I make two groups of each, sorted by written and sorted by spoken form:
        for group, cmds in copy(all_commands.items()):
            if cmds == []:
                # remove empty groups, except for "actual"
                if group != 'actual':
                    del all_commands[group]
                    continue
                
            if group not in ('numbers','letters'):
                cmds = self.sort_by_spoken(cmds)
                all_commands[group + '_sb_s'] = cmds[:]
            cmds = self.sort_by_written(cmds)
            if group not in ('numbers','letters'):
                del all_commands[group]
                group = group + '_sb__w'
            all_commands[group] = cmds[:]
            
        
    def create_html_pages(self):
        """Created the actual pages, using HTMLgen
        
        the input is from the self.lsa_commands dict for the lsa menu
        and from csc_commands (future) for the csc menu
        
        returns the entry pages for the webbrowser
        """
        self.top_menu = ['lsa', 'csc'] 
        self.lsa_pages = self.lsa_commands.keys()
        self.lsa_pages.sort()
        want_in_top = ['actual_sb__w', 'actual_sb_s', 'common_sb__w', 'common_sb_s',
                       self.language + '_sb__w', self.language + '_sb_s', 'letters', 'numbers']
        want_in_top.reverse()
        for w in want_in_top:
            self.bring_to_top(self.lsa_pages, w)
        self.csc_pages = 'dummy'
        self.html_command_index()
        for top in self.top_menu:
            self.html_command_pages(top)
        index_page = os.path.join(self.html_folder, 'index.html')
        return index_page

    def bring_to_top(self, List, item):
        """Change inplace the list"""
        if item in List:
            List.remove(item)
            List.insert(0, item)

    def show_cmds(self, cmd_interp, curr_lang):
        """Do all the steps to make and show  the WhatCanISay website

        collect the commands
        create the html files,
        then show with webbrowser
        """
        self.create_cmds(cmd_interp,curr_lang)
        index_page = self.create_html_pages()
        webbrowser.open_new(index_page)

    def create_html_folder(self):
        """create a folder for the WhatCanISay website

        this foldername is also returned
        """
        self.html_folder = vc_globals.wcisay_html_folder

        try:
            os.makedirs(self.html_folder)
            print 'WARNING: whatCanISay folder did not exist, stylesheet will not be available'
        except:
            pass
        if not os.path.isdir(self.html_folder):
            raise Exception('not a valid directory for What Can I Say website: %s'% self.html_folder)
        return self.html_folder
        
    
    
    def html_command_index(self):
        """make the index page of the website"""
        doc = SimpleDocument()
        doc.stylesheet = "vc.css"
        page = 'index.html'
        page_type = 'index'
        page_html = 'index.html'
        doc.append(self.html_header(page, page_type=page_type, page_html=page_html))
        tlpage = FullTable(Class="page")
        trpage = TR()
        tdpage = TD(Class="body")
        # produce the menu (left):
        # produce the body:
        VcodeWebsite = Href("http://voicecode.iit.nrc.ca/VoiceCode/public/ywiki.cgi", "Voice Code website", target="_blank")
        text =[ 'This is the What Can I Say (actual) information of your VoiceCode instance.', '',
               'The lsa section gives the Language Sensitive Aliases, in different categories.',
                'The "numbers" and the "letters" are taken apart for better readability of the other commands.',
                'The different sections are sorted by written form (sb written) and  by spoken form (sb spoken)',
                '', '',
                'The csc part is not ready yet. It is going to contain the Context Sensitive Aliases',
                '', '',
                'For the general information please consult the '+VcodeWebsite+'.',
                '',
                '']
        for t in text:
            if t:
                tdpage.append(Paragraph(t))
            else:
                tdpage.append(Paragraph("&nbsp;", Class="blank"))
        doc.append(tlpage(trpage(tdpage)))
        doc.append(self.html_footer(page, page_type=page_type, page_html=page_html))
        outfile = os.path.join(self.html_folder, 'index.html')
   
        trace('WhatCanISay.files', 'making page: %s'% outfile)
        doc.write(outfile)

    def get_left_menu(self, me, page_type, pages):
        """produce a menu with me without link

        me = name of calling page, page_type is to be included before the link name

        """
        td = TD(Class="leftmenu")
        for p in pages:
            niceP = p
            if niceP.endswith('_sb_s'):
                niceP = p.replace('_sb_s', ' (sb spoken)')
            if niceP.endswith('_sb__w'):
                niceP = p.replace('_sb__w', ' (sb written)')
                
            if p == me:
                td.append(Paragraph(niceP, Class="lefton"))
            else:                
                td.append(Paragraph(Href('%s_%s.html'% (page_type, p), niceP), Class="leftoff"))
        return td

    def html_command_pages(self, page_type):
        """generate the pages"""

        if page_type == 'lsa':
            for p in self.lsa_pages:
                self.html_lsa_page(p)
        else:
            self.html_csc_page('index')

    def html_lsa_page(self, page):
        """generate one lsa page, with a menu to the other pages"""
        doc = SimpleDocument()
        doc.stylesheet = "vc.css"
        page_type = 'lsa'
        
        content = self.lsa_commands[page]
        page_html = 'lsa_%s.html'% page
        doc.append(self.html_header(page, page_type=page_type, page_html=page_html))
        tlpage = FullTable(Class="page")
        trpage = TR()
        # produce the menu (left):
        leftMenu = self.get_left_menu(page, page_type=page_type, pages=self.lsa_pages)
        trpage.append(leftMenu)

        # now the contents:        
        tl = FullTable(Class="body")
        tr = TR()
        per_col = 3
        tdspacer = TD("&nbsp;", Class="spacer")
        rows = len(content)/per_col
        if len(content)%per_col:
            rows += 1
        cell_num = 0
        for start in range(rows):
            cell_num = start % 2
            for col in range(start, len(content), rows):
                cell_num += 1
                k, v = content[col]
                tr.append(TD(v, Class="spoken%s"% (cell_num%2,)))
                tr.append(TD(k, Class="written%s"% (cell_num%2,)))
                tr.append(tdspacer())
            tl.append(tr)
            tr.empty()
        
        trpage.append(TD(tl, Class="body"))
        tlpage.append(trpage)
        doc.append(tlpage)
        doc.append(self.html_footer(page, page_type=page_type, page_html=page_html))
        outfile = os.path.join(self.html_folder, page_html)
        trace('WhatCanISay.files', 'making page: %s'% outfile)
        doc.write(outfile)
                  
    def html_csc_page(self, page):
        """generate one csc page"""
        doc = SimpleDocument()
        doc.stylesheet = "vc.css"
        page_type = 'csc'
        page_html = 'csc_%s.html'% page
        content = self.csc_commands['python']
        trace('WhatCanISay.html_csc_page', 'csc_commands: %s'% content)
        doc.append(self.html_header(page, page_type=page_type, page_html=page_html))

        if 1:
            tlpage = FullTable(Class="page")
            doc.append(Header(1, 'begin of csc commands, python'))
            trpage = TR()

            # produce the menu (left):
#            leftMenu = self.get_left_menu(page, page_type=page_type, pages=self.lsa_pages)
#            trpage.append(leftMenu)
            
            # now the contents:        
            tl = FullTable(Class="body")
            tr = TR()
            per_col = 1
            tdspacer = TD("&nbsp;", Class="spacer")
            rows = len(content)/per_col
            if len(content)%per_col:
                rows += 1
            for start in range(rows):
                cell_num = start%2
                for col in range(start, len(content), rows):
                    cell_num += 1
                    class_name = "written%s"% (cell_num%2,)
                    k, v = content[col]
                    rows_inside = len(v)
                    tr.append(TD(k, Class=class_name, rowspan=rows_inside))
                    if rows_inside > 1:
                        v = self.sort_csc_values_by_scope(v)
                        v.reverse()
                    for row_inside in v:
                        cont, scope, value = row_inside
                        tr.append(TD(value, Class=class_name))
                        tr.append(TD(scope, Class=class_name))
                        tr.append(TD(cont, Class=class_name))
                        tr.append(tdspacer())
                        tl.append(tr)
                        tr.empty()
                tr.empty()
        
            trpage.append(TD(tl, Class="body"))
            tlpage.append(trpage)
            doc.append(tlpage)
            doc.append(self.html_footer(page, page_type=page_type, page_html=page_html))
        outfile = os.path.join(self.html_folder, page_html)
        trace('WhatCanISay.files', 'making page: %s'% outfile)
        doc.write(outfile)
                  
    def html_header(self, page, page_type, page_html):
        """produce the header at the top of the html page, with the name mentioned

        Include the top menu, lsa, csc...

        page_type can be 'index', 'lsa', 'csc'


        """
        # assume height of picture = 90, h2 is height of top_menu
        h_pic = 90
        h2 = 28
        h1 = h_pic - h2 + 20 # allow 20 for MLB number space in firefox
        # assume w of picture = 134
        w = 134
        im = Img('vcodeuser.jpg', alt='what can i say website for voicecoder')
        L = []
##        print 'header of page: %s, page_type: %s'% (page, page_type)
        if page_type == 'index' and page == 'index.html':
            pass
        else:
            im = Href('index.html', im)

        if page_type != 'index':
            niceP = '%s commands, %s'% (page_type, page)
            niceP = niceP.replace('_sb_s', ' (sorted by spoken forms)')
            niceP = niceP.replace('_sb__w', ' (sorted by written forms)')
        else:
            niceP = 'home'
            
        text = "VoiceCoder What Can I Say (%s): %s"% (self.language, niceP)
        tl = FullTable(Class="header")
        tl_menu = FullTable(Class="header", height=h2)
        tl.append(TR(TD(im, Class="bannerim", rowspan=2, width=w, height=h_pic),
                     TD(text, Class="bannertext", height=h1)))
        # make the top menu:
        tr = TR()
        for menu in self.top_menu:
            start_page = self.get_first_page(menu)
#            print 'menu: %s, start_page: %s, page: %s, page_html: %s'% \
#                  (menu, start_page, page, page_html)
            if page_html.startswith(menu):
                if page_html == start_page:
                    tr.append(TD(menu, Class="topon"))
                else:
                    tr.append(TD(Href(start_page, menu), onclick="location='%s';"%start_page, Class="topon", height=h2))
            else:
                tr.append(TD(Href(start_page, menu), onclick="location='%s';"%start_page, Class="topoff", height=h2))
            tr.append(TD('&nbsp;', Class="blank"))
        tl_menu.append(tr)
        tl.append(TR(TD(tl_menu, Class="topmenu")))
        return tl

    def html_footer(self, page, page_type, page_html):
        """construct a footer for the webpage"""
        
        tl = FullTable(Class="footer")
        if page_type == 'index' and page == 'index.html':
            scramble = 'home'
        else:
            niceP = page
            niceP = niceP.replace('_sb_s', ' (sorted by spoken forms)')
            niceP = niceP.replace('_sb__w', ' (sorted by written forms)')
            scramble = join(Href('index.html', 'home'), ' &gt; ', niceP)
        scramble += " &gt; " + str(Href("javascript:scrollTo(0,0);", " top"))
        tim = time.localtime(time.time())
        copyright = time.strftime("%a, %d %b %Y", tim)
        tl.append(TR(TD(scramble, Class="scramble"),
                     TD(copyright, Class="copyright")))
        return join(tl)

    def get_first_page(self, menu):
        """Extract from the list of pages the first page to display"""
        if menu == 'lsa':
            return 'lsa_%s.html'% self.lsa_pages[0]
        elif menu == 'csc':
            return 'csc_%s.html'% 'index'
        else:
            return 'index.html'
        

    def sort_by_spoken(self, cmds):
        """sort list of tuples by the first key

        note the presentation is the other way
        each cmd is (spoken, written), but presentation in
        html is (written, spoken)

        """
        cmds.sort()
        return cmds

    def sort_by_written(self, cmds):
        """sort list of tuples by the second key
        
        note the presentation is the other way
        each cmd is (spoken, written), but presentation in
        html is (written, spoken)

        """
        decorated = [(s,w) for (w,s) in cmds]
        decorated.sort()
        undecorated = [(s,w) for (w,s) in decorated]
        return undecorated

    def sort_csc_values_by_scope(self, csc_values):
        """sort list of tuples by skope

        [(str context_equivalence, str skop, str docs), ...]
        """
        for  csc_value in  csc_values:
            a, skope, c = csc_value
            if not valid_scope(skope):
                trace("WhatCanISay.sort_csc_value_by_scope",
                      "WARNING: invalid skope in csc entry WhatCanISay: %s"% \
                      repr(csc_value))
                return csc_values
        scope_order_list = scope_order()
        dec = [(scope_order_list.index(skope), (a, skope, c)) for (a, skope, c) in csc_values]
        dec.sort()
        return [b for (a,b) in dec]
        
                

# defaults for vim - otherwise ignore
# vim:sw=4
