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
# (C)2000, National Research Council of Canada
#
##############################################################################

#
# Configuration script for VoiceCode
#

#
# Note: those import statements are not absolutely necessary because file
#       vc_config.py is evaluated in a context where those have already
#       been imported.
#
#       But having them here makes it possible to compile vc_config.py
#       with command line:
#
#           python vc_config.py
#
#       which provides better error reportingn than when evaluated by
#       MediatorObject.configure().
#
# import natlink
# from natlinkutils import *

#
# Import configuration functions
#
# from MediatorObject import associate_language, define_language, \
#      add_abbreviation, add_csc, add_lsa, print_abbreviations, \
#      standard_symbols_in

from MediatorObject import associate_language, define_language

import CmdInterp

from CSCmd import CSCmd
from LangDef import LangDef
from cont_gen import *
from actions_gen import *
from actions_C_Cpp import *
from actions_py import *
from actions_perl import *

import KnownTargetModule

import sr_interface

#test_mediator = None

if (__name__ == '__main__'):
    if not globals().has_key('add_csc') and not locals().has_key('add_csc'):
        import MediatorObject
#        global test_mediator
        test_mediator = MediatorObject.MediatorObject( \
            interp = CmdInterp.CmdInterp())
#        MediatorObject.to_configure = test_mediator
        glob_names = globals()
        test_mediator.define_config_functions(glob_names)
#        print glob_names['add_abbreviation']
#    add_abbreviation = MediatorObject.add_abbreviation
#    add_csc = MediatorObject.add_csc
#    add_lsa = MediatorObject.add_lsa
#    print_abbreviations = MediatorObject.print_abbreviations
#    standard_symbols_in = MediatorObject.standard_symbols_in
#        add_abbreviation = MediatorObject.to_configure.add_abbreviation
#        add_csc = MediatorObject.to_configure.add_csc
#        add_lsa = MediatorObject.to_configure.add_lsa
#        print_abbreviations = MediatorObject.to_configure.print_abbreviations
#        standard_symbols_in = MediatorObject.to_configure.standard_symbols_in

#        global add_abbreviation, add_csc, add_lsa, print_abbreviations, \
#            standard_symbols_in
#        add_abbreviation = test_mediator.add_abbreviation
#        add_csc = test_mediator.add_csc
#        add_lsa = test_mediator.add_lsa
#        print_abbreviations = test_mediator.print_abbreviations
#        standard_symbols_in = test_mediator.standard_symbols_in
        
        if sr_interface.speech_able():
#            natlink.natConnect()    
            sr_interface.connect()

#try:
#    print add_abbreviation
#    print add_abbreviation.im_self
#except Exception, err:
#    print 'no global add_abbreviation'
    

##############################################################################
# Customize from here only
##############################################################################

#import traceback
#try:
#    add_abbreviation('attr', ['attribute'])
#except Exception, err:
#    print 'error adding abbreviation'
#    traceback.print_exc(err)
#    raise err

#
# Load abbreviations files
#
for abbrev_file in ('user_abbrevs.py', 'py_abbrevs.py'):
    try:
        full_file = vc_globals.config + os.sep + abbrev_file
#        print '-- vc_config.__main__: full_file=\'%s\'' % full_file
        execfile(full_file)
    except Exception, err:
        print 'ERROR: in abbreviations file: %s' % full_file
        raise err

        
# print add_abbreviation
add_abbreviation('attr', ['attribute'])


###############################################################################
# Associate file extensions to programming languages
###############################################################################

#
# Doesn't seem to work for now so we set it in SourceBuff.py directly
#
#  associate_language('c', 'C')
#  associate_language('h', 'C')
#  associate_language('py', 'python')

###############################################################################
# AppMgr and RecogStartMgr (ignored by old MediatorObject)
###############################################################################


#  should the RecogStartMgr trust that the current
#  window corresponds to the editor when the editor first connects to
#  VoiceCode, or when it notifies VoiceCode of a new window.

# currently, do not trust to maintain compatibility with regression test
# results

trust_current_window(0)

# Known editor modules 

#     define modules
mod_Emacs = KnownTargetModule.DedicatedModule(module_name = 'EMACS',
        editor = 'emacs')
mod_exceed = \
    KnownTargetModule.DualModeDisplayByTitle(title_regex = '^Exceed$',
    module_name = 'EXCEED')

mod_ttssh = KnownTargetModule.RemoteShell(module_name = 'TTSSH')

mod_python = KnownTargetModule.LocalInterpreter(module_name = 'PYTHON',
    title_varies = 1)
  
#     add them to the RecogStartMgr
add_module(mod_Emacs)
add_module(mod_exceed)
add_module(mod_ttssh)
add_module(mod_python)

# Known editors and the prefixes used to form their unique instance
# strings
add_prefix('emacs', 'Yak')
add_prefix('WaxEdit', 'Floor')
add_prefix('GenEdit', 'Inside')
add_prefix('EdSim', 'Standby')
add_prefix('dumbEdSim', 'Dumbo')

#############################################################################
# CSCs and LSAs that apply for ALL languages
#############################################################################

#############################################################################
# Punctuation marks.
#############################################################################
#
# These LSAs usually don't add spaces before/after the punctuation
# mark. There are other LSAs and CSCs for inserting space padded punctuation.
#
# For example:
#   'less sign' -> '<' (i.e. no space padding)
#   'is less than' -> ' < ' (i.e. space padded)
#
# This gives the user the flexibility of padding the punctuation with signs
# or not, depending on the context in which it is said. We are careful to
# choose wordings of padded forms 
#
add_lsa(['blank space', 'space bar'], {None: ' '})
add_lsa(['newline', 'new line'], {None: '\n'})
add_lsa(['asterisk', 'star'], {None: '*'})
add_lsa(['double asterisk', 'double star'], {None: '**'})
add_lsa(['slash'], {None: '/'})
add_lsa(['plus sign'], {None: '+'})
add_lsa(['minus sign', 'hyphen'], {None: '-'})
add_lsa(['percent', 'percent sign'], {None: '%'})
add_lsa(['and percent'], {None: '&'})
add_lsa(['pipe', 'pipe sign', 'vertical bar'], {None: '|'})
add_lsa(['comma'], {None: ', '})
add_lsa(['semicolon', 'semi'], {None: ';'})
add_lsa(['dot'], {None: '.'})
add_lsa(['ellipsis'], {None: '...'})
add_lsa(['exclamation mark', 'bang'], {None: '!'})
add_lsa(['question mark'], {None: '?'})
add_lsa(['pound', 'pound sign'], {None: '#'})
add_lsa(['tilde', 'squiggle'], {None: '~'})
add_lsa(['colon'], {None: ': '})
add_lsa(['double colon', 'colon colon'], {None: '::'})
add_lsa(['less sign'], {None: '<'})
add_lsa(['greater sign'], {None: '>'})
add_lsa(['equal sign'], {None: '='})

#
# Generic balanced expressions (e.g. "", '', (), [], {})
#
#    We define LSAs for the start/end of the balanced expresion.
#       e.g. 'open paren' -> '(', 'close paren' -> ')'
#
#    We also define an LSA for typing an empty balanced expression and
#    putting the cursor after it.
#       e.g. 'empty parens' -> '()^'
#
#    We also define a CSC for typing an empty balanced expression and moving
#    the cursor in between.
#       e.g. 'between parens' -> '(^)'
#
add_lsa(['open paren'], {None: '('})
add_lsa(['close paren'], {None: ')'})
add_lsa(['empty parens'], {None: '()'})
acmd = CSCmd(spoken_forms=['between parens', 'paren pair', 'parens pair', 'parens'], 
             meanings={ContAny(): ActionInsert('(', ')')},
             docstring='put cursor between parens: (^)')
add_csc(acmd)
add_lsa(['open bracket', 'open square bracket'], {None: '['})
add_lsa(['close bracket', 'close square bracket'], {None: ']'})
add_lsa(['empty brackets', 'empty square brackets'], {None: '[]'})
acmd = CSCmd(spoken_forms=['between brackets', 'between square brackets',
                           'bracket pair', 'square bracket pair',
                           'brackets pair', 'square brackets pair',
                           'brackets', 'square brackets'], 
             meanings={ContAny(): ActionInsert('[', ']')}, 
             docstring='put cursor between square brackets: [^]')
add_csc(acmd)
add_lsa(['open brace', 'open curly bracket', 'open curly'], {None: '{'})
add_lsa(['close brace', 'close curly bracket', 'close curly'], {None: '}'})
add_lsa(['empty curly brackets', 'empty curlies', 'empty braces'], {None: '{}'})
acmd = CSCmd(spoken_forms=['between braces', 'brace pair','braces pair',
                           'braces', 'between curlies', 'curly pair',
                           'curlies pair', 'curlies', 'curly brackets'], 
             meanings={ContAny(): ActionInsert('{', '}')},
             docstring='put cursor between curly brackets: {^}')
add_csc(acmd)
add_lsa(['open angled bracket', 'open angled'], {None: '<'})
add_lsa(['close angled bracket', 'close angled'], {None: '>'})
add_lsa(['empty angled brackets', 'empty angled'], {None: '<>'})
acmd = CSCmd(spoken_forms=['between angled brackets', 'angled bracket pair',
                           'angled brackets pair', 'angled', 'between angled',
                           'angled pair', 'angled brackets'], 
             meanings={ContAny(): ActionInsert('<', '>')}, 
             docstring='put cursor between angled brackets: <^>')
add_csc(acmd)
add_lsa(['single quote', 'open single quote', 'close single quote'],
        {None: '\''})
add_lsa(['empty single quotes', 'empty single'], {None: '\'\''})
acmd = CSCmd(spoken_forms=['between single quotes', 'single quotes'],
             meanings={ContAny(): ActionInsert('\'', '\'')},
             docstring = 'put cursor between single quotes: \'^\'')
add_csc(acmd)
add_lsa(['quote', 'open quote', 'close quote', 'open quotes',
         'close quotes'],
        {None: '"'})
add_lsa(['empty quotes'], {None: '""'})
acmd = CSCmd(spoken_forms=['between quotes', 'quotes'],
             meanings={ContAny(): ActionInsert('"', '"')},
             docstring = 'put cursor between quotes: "^"')
add_csc(acmd)
add_lsa(['back quote', 'open back', 'open back quote', 'close back',
         'close back quote'],
        {None: '`'})
add_lsa(['empty back quotes', 'empty back'], {None: '``'})
acmd = CSCmd(spoken_forms=['between back quotes', 'back quotes',
                           'between back'],
             meanings={ContAny(): ActionInsert('`', '`')},
             docstring = 'put cursor between back quotes: `^`')
add_csc(acmd)

#
# Escaped characters
#
add_lsa(['back slash a.', 'back slash a', 'back slash alpha'], {None: '\\a'})
add_lsa(['back slash b.', 'back slash b', 'back slash bravo'], {None: '\\b'})
add_lsa(['back slash c.', 'back slash c', 'back slash charlie'], {None: '\\c'})
add_lsa(['back slash d.', 'back slash d', 'back slash delta'], {None: '\\d'})
add_lsa(['back slash e.', 'back slash e', 'back slash echo'], {None: '\\e'})
add_lsa(['back slash f.', 'back slash f', 'back slash foxtrot'], {None: '\\f'})
add_lsa(['back slash g.', 'back slash g', 'back slash golf'], {None: '\\g'})
add_lsa(['back slash h.', 'back slash h', 'back slash hotel'], {None: '\\h'})
add_lsa(['back slash i.', 'back slash i', 'back slash india'], {None: '\\i'})
add_lsa(['back slash j.', 'back slash j', 'back slash juliett'], {None: '\\j'})
add_lsa(['back slash k.', 'back slash k', 'back slash kilo'], {None: '\\k'})
add_lsa(['back slash l.', 'back slash l', 'back slash lima'], {None: '\\l'})
add_lsa(['back slash m.', 'back slash m', 'back slash mike'], {None: '\\m'})
add_lsa(['back slash n.', 'back slash n', 'back slash november'], {None: '\\n'})
add_lsa(['back slash o.', 'back slash o', 'back slash oscar'], {None: '\\o'})
add_lsa(['back slash p.', 'back slash p', 'back slash papa'], {None: '\\p'})
add_lsa(['back slash q.', 'back slash q', 'back slash quebec'], {None: '\\q'})
add_lsa(['back slash r.', 'back slash r', 'back slash romeo'], {None: '\\r'})
add_lsa(['back slash s.', 'back slash s', 'back slash sierra'], {None: '\\s'})
add_lsa(['back slash t.', 'back slash t', 'back slash tango'], {None: '\\t'})
add_lsa(['back slash u.', 'back slash u', 'back slash uniform'], {None: '\\u'})
add_lsa(['back slash v.', 'back slash v', 'back slash victor'], {None: '\\v'})
add_lsa(['back slash w.', 'back slash w', 'back slash whiskey'], {None: '\\w'})
add_lsa(['back slash x.', 'back slash x', 'back slash xray'], {None: '\\x'})
add_lsa(['back slash y.', 'back slash y', 'back slash yankee'], {None: '\\y'})
add_lsa(['back slash z.', 'back slash z', 'back slash zulu'], {None: '\\z'})
add_lsa(['back slash cap a.', 'back slash cap a', 'back slash cap alpha'], {None: '\\A'})
add_lsa(['back slash cap b.', 'back slash cap b', 'back slash cap bravo'], {None: '\\B'})
add_lsa(['back slash cap c.', 'back slash cap c', 'back slash cap charlie'], {None: '\\C'})
add_lsa(['back slash cap d.', 'back slash cap d', 'back slash cap delta'], {None: '\\D'})
add_lsa(['back slash cap e.', 'back slash cap e', 'back slash cap echo'], {None: '\\E'})
add_lsa(['back slash cap f.', 'back slash cap f', 'back slash cap foxtrot'], {None: '\\F'})
add_lsa(['back slash cap g.', 'back slash cap g', 'back slash cap golf'], {None: '\\G'})
add_lsa(['back slash cap h.', 'back slash cap h', 'back slash cap hotel'], {None: '\\H'})
add_lsa(['back slash cap i.', 'back slash cap i', 'back slash cap india'], {None: '\\I'})
add_lsa(['back slash cap j.', 'back slash cap j', 'back slash cap juliett'], {None: '\\J'})
add_lsa(['back slash cap k.', 'back slash cap k', 'back slash cap kilo'], {None: '\\K'})
add_lsa(['back slash cap l.', 'back slash cap l', 'back slash cap lima'], {None: '\\L'})
add_lsa(['back slash cap m.', 'back slash cap m', 'back slash cap mike'], {None: '\\M'})
add_lsa(['back slash cap n.', 'back slash cap n', 'back slash cap november'], {None: '\\N'})
add_lsa(['back slash cap o.', 'back slash cap o', 'back slash cap oscar'], {None: '\\O'})
add_lsa(['back slash cap p.', 'back slash cap p', 'back slash cap papa'], {None: '\\P'})
add_lsa(['back slash cap q.', 'back slash cap q', 'back slash cap quebec'], {None: '\\Q'})
add_lsa(['back slash cap r.', 'back slash cap r', 'back slash cap romeo'], {None: '\\R'})
add_lsa(['back slash cap s.', 'back slash cap s', 'back slash cap sierra'], {None: '\\S'})
add_lsa(['back slash cap t.', 'back slash cap t', 'back slash cap tango'], {None: '\\T'})
add_lsa(['back slash cap u.', 'back slash cap u', 'back slash cap uniform'], {None: '\\U'})
add_lsa(['back slash cap v.', 'back slash cap v', 'back slash cap victor'], {None: '\\V'})
add_lsa(['back slash cap w.', 'back slash cap w', 'back slash cap whiskey'], {None: '\\W'})
add_lsa(['back slash cap x.', 'back slash cap x', 'back slash cap xray'], {None: '\\X'})
add_lsa(['back slash cap y.', 'back slash cap y', 'back slash cap yankee'], {None: '\\Y'})
add_lsa(['back slash cap z.', 'back slash cap z', 'back slash cap zulu'], {None: '\\Z'})


#
# Commands for jumping to a specific punctuation mark
# Not exhaustive.
# This really calls for some sort of grammar to automatically generate the
# spoken forms. But for now, exhaustively (or "exhaustingly" ;-) listing all
# possible spoken forms will have to do (although it's definitely exhausting"
#


#
# semicolon
#
acmd = CSCmd(spoken_forms=['next semi', 'after semi', 'next semicolon',
                           'after semicolon'],
             meanings={ContAny(): ActionSearchRepeat(regexp=';\s{0,1}')},
             docstring='go after next semicolon')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before semi', 'before next semi', 'before semicolon', 'before next semicolon'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1};', where=-1)},
             docstring='go before next semicolon')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous semi', 'previous semicolon',
                           'after previous semi',
                           'after previous semicolon'],
             meanings={ContAny(): ActionSearchRepeat(regexp=';\s{0,1}', direction=-1)},
             docstring='go after previous semicolon')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous semi',
                           'before previous semicolon'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1};', direction=-1, where=-1)},
             docstring='go before previous semicolon')
add_csc(acmd)

#
# comma
#
acmd = CSCmd(spoken_forms=['next comma', 'after comma'],
             meanings={ContAny(): ActionSearchRepeat(regexp=',\s{0,1}')},
             docstring='go after next comma')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before comma', 'before next comma'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1},', where=-1)},
             docstring='go before next comma')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous comma', 'after previous comma'],
             meanings={ContAny(): ActionSearchRepeat(regexp=',\s{0,1}', direction=-1)},
             docstring='go after previous comma')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous comma'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1},', direction=-1, where=-1)},
             docstring='go before previous comma')
add_csc(acmd)

#
# dot
#
acmd = CSCmd(spoken_forms=['next dot', 'after dot'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\\.\s{0,1}')},
             docstring='go after next dot')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before dot', 'before next dot'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}\\.', where=-1)},
             docstring='go before next dot')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous dot', 'after previous dot'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\\.\s{0,1}', direction=-1)},
             docstring='go after previous dot')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous dot'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}\\.', direction=-1, where=-1)},
             docstring='go before previous dot')
add_csc(acmd)

#
# colon
#
acmd = CSCmd(spoken_forms=['next colon', 'after colon'],
             meanings={ContAny(): ActionSearchRepeat(regexp=':\s{0,1}')},
             docstring='go after next colon')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before colon', 'before next colon'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}:', where=-1)},
             docstring='go before next colon')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous colon', 'after previous colon'],
             meanings={ContAny(): ActionSearchRepeat(regexp=':\s{0,1}', direction=-1)},
             docstring='go after previous colon')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous colon'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}:', direction=-1, where=-1)},
             docstring='go before previous colon')
add_csc(acmd)

#
# asterisk
#
acmd = CSCmd(spoken_forms=['next asterisk', 'after asterisk', 'next star',
                           'after star'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\\*\s{0,1}')},
             docstring='go after next asterisk')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before asterisk', 'before next asterisk',
                           'before star', 'before next star'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}\\*', where=-1)},
             docstring='go before next asterisk')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous asterisk', 'previous star',
                           'after previous asterisk', 'after previous star'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\\*\s{0,1}', direction=-1)},
             docstring='go after previous asterisk')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous asterisk', 'before previous star'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}\\*', direction=-1, where=-1)},
             docstring='go before previous asterisk')
add_csc(acmd)

#
# slash
#
acmd = CSCmd(spoken_forms=['next slash', 'after slash'],
             meanings={ContAny(): ActionSearchRepeat(regexp='/\s{0,1}')},
             docstring='go after next slash')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before slash', 'before next slash'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}/', where=-1)},
             docstring='go before next slash')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous slash', 'after previous slash'],
             meanings={ContAny(): ActionSearchRepeat(regexp='/\s{0,1}', direction=-1)},
             docstring='go after previous slash')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous slash'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}/', direction=-1, where=-1)},
             docstring='go before previous slash')
add_csc(acmd)

#
# plus
#
acmd = CSCmd(spoken_forms=['next plus', 'after plus'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\\+\s{0,1}')},
             docstring='go after next plus')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before plus', 'before next plus'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}\\+', where=-1)},
             docstring='go before next plus')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous plus', 'after previous plus'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\\+\s{0,1}', direction=-1)},
             docstring='go after previous plus')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous plus'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}\\+', direction=-1, where=-1)},
             docstring='go before previous plus')
add_csc(acmd)

#
# minus
#
acmd = CSCmd(spoken_forms=['next minus', 'after minus', 'next hyphen',
                           'after hyphen'],
             meanings={ContAny(): ActionSearchRepeat(regexp='-\s{0,1}')},
             docstring='go after next minus')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before minus', 'before next minus', 'before hyphen', 'before next hyphen'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}-', where=-1)},
             docstring='go before next minus')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous minus', 'after previous minus',
                           'previous hyphen', 'after previous hyphen'],
             meanings={ContAny(): ActionSearchRepeat(regexp='-\s{0,1}', direction=-1)},
             docstring='go after previous minus')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous minus', 'before previous hyphen'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}-', direction=-1, where=-1)},
             docstring='go before previous minus')
add_csc(acmd)

#
# percent
#
acmd = CSCmd(spoken_forms=['next percent', 'after percent'],
             meanings={ContAny(): ActionSearchRepeat(regexp='%\s{0,1}')},
             docstring='go after next percent')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before percent', 'before next percent'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}%', where=-1)},
             docstring='go before next percent')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous percent', 'after previous percent'],
             meanings={ContAny(): ActionSearchRepeat(regexp='%\s{0,1}', direction=-1)},
             docstring='go after previous percent')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous percent'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}%', direction=-1, where=-1)},
             docstring='go before previous percent')
add_csc(acmd)

#
# and percent
#
acmd = CSCmd(spoken_forms=['next and percent', 'after and percent'],
             meanings={ContAny(): ActionSearchRepeat(regexp='&\s{0,1}')},
             docstring='go after next and percent')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before and percent', 'before next and percent'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}&', where=-1)},
             docstring='go before next and percent')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous and percent', 'after previous and percent'],
             meanings={ContAny(): ActionSearchRepeat(regexp='&\s{0,1}', direction=-1)},
             docstring='go after previous and percent')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous and percent'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}&', direction=-1, where=-1)},
             docstring='go before previous and percent')
add_csc(acmd)

#
# pipe
#
acmd = CSCmd(spoken_forms=['next pipe', 'after pipe', 'next pipe sign', 'after pipe sign'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\\|\s{0,1}')},
             docstring='go after next pipe')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before pipe', 'before next pipe',
                           'before pipe sign', 'before next pipe sign'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}\\|', where=-1)},
             docstring='go before next pipe sign')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous pipe', 'previous pipe sign',
                           'after previous pipe', 'after previous pipe sign'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\\|\s{0,1}', direction=-1)},
             docstring='go after previous pipe sign')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous pipe', 'before previous pipe sign'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}\\|', direction=-1, where=-1)},
             docstring='go before previous pipe sign')
add_csc(acmd)

#
# ellipsis
#
acmd = CSCmd(spoken_forms=['next ellipsis', 'after ellipsis'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\\.\\.\\.\s{0,1}')},
             docstring='go after next ellipsis')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before ellipsis', 'before next ellipsis'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}\\.\\.\\.', where=-1)},
             docstring='go before next ellipsis')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous ellipsis', 'after previous ellipsis'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\\.\\.\\.\s{0,1}', direction=-1)},
             docstring='go after previous ellipsis')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous ellipsis'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}\\.\\.\\.', direction=-1, where=-1)},
             docstring='go before previous ellipsis')
add_csc(acmd)

#
# exclamation mark
#
acmd = CSCmd(spoken_forms=['next exclamation mark', 'after exclamation mark',
                           'next bang', 'after bang'],
             meanings={ContAny(): ActionSearchRepeat(regexp='!\s{0,1}')},
             docstring='go after next exclamation mark')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before exclamation mark', 'before next exclamation mark', 'before bang', 'before next bang'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}!', where=-1)},
             docstring='go before next exclamation mark')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous exclamation mark', 'after previous exclamation mark', 'previous bang',
                           'after previous bang'],
             meanings={ContAny(): ActionSearchRepeat(regexp='!\s{0,1}', direction=-1)},
             docstring='go after previous exclamation mark')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous exclamation mark', 'before previous bang'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}!', direction=-1, where=-1)},
             docstring='go before previous exclamation mark')
add_csc(acmd)

#
# question mark
#
acmd = CSCmd(spoken_forms=['next question mark', 'after question mark'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\\?\s{0,1}')},
             docstring='go after next question mark')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before question mark', 'before next question mark'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}\\?', where=-1)},
             docstring='go before next question mark')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous question mark', 'after previous question mark'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\\?\s{0,1}', direction=-1)},
             docstring='go after previous question mark')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous question mark'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}\\?', direction=-1, where=-1)},
             docstring='go before previous question mark')
add_csc(acmd)

#
# pound
#
acmd = CSCmd(spoken_forms=['next pound', 'after pound', 'next pound sign',
                           'after pound sign'],
             meanings={ContAny(): ActionSearchRepeat(regexp='#\s{0,1}')},
             docstring='go after next pound sign')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before pound', 'before next pound',
                           'before pound sign', 'before next pound sign'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}#', where=-1)},
             docstring='go before next pound sign')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous pound', 'previous pound sign',
                           'after previous pound', 'after previous pound sign'],
             meanings={ContAny(): ActionSearchRepeat(regexp='#\s{0,1}', direction=-1)},
             docstring='go after previous pound sign')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous pound', 'before previous pound sign'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}#', direction=-1, where=-1)},
             docstring='go before previous pound sign')
add_csc(acmd)

#
# double colon
#
acmd = CSCmd(spoken_forms=['next double colon', 'after double colon'],
             meanings={ContAny(): ActionSearchRepeat(regexp='::\s{0,1}')},
             docstring='go after next double colon')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before double colon', 'before next double colon'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}::', where=-1)},
             docstring='go before next double colon')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous double colon', 'after previous double colon'],
             meanings={ContAny(): ActionSearchRepeat(regexp='::\s{0,1}', direction=-1)},
             docstring='go after previous double colon')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous double colon'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}::', direction=-1, where=-1)},
             docstring='go before previous double colon')
add_csc(acmd)

#
# tilde
#
acmd = CSCmd(spoken_forms=['next tilde', 'after tilde', 'next squiggle',
                           'after squiggle'],
             meanings={ContAny(): ActionSearchRepeat(regexp='~\s{0,1}')},
             docstring='go after next tilde')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before tilde', 'before next tilde',
                           'before squiggle', 'before next squiggle'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}~', where=-1)},
             docstring='go before next tilde')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous tilde', 'previous squiggle',
                           'after previous tilde', 'after previous squiggle'],
             meanings={ContAny(): ActionSearchRepeat(regexp='~\s{0,1}', direction=-1)},
             docstring='go after previous tilde')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous tilde', 'before previous squiggle'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}~', direction=-1, where=-1)},
             docstring='go before previous tilde')
add_csc(acmd)

#
# less sign
#
acmd = CSCmd(spoken_forms=['next less sign', 'after less sign',
                           'next less than', 'after less than'],
             meanings={ContAny(): ActionSearchRepeat(regexp='<\s{0,1}')},
             docstring='go after next less sign')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before less sign', 'before next less sign',
                           'before less than', 'before next less than'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}<', where=-1)},
             docstring='go before next less sign')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous less sign', 'previous less than',
                           'after previous less sign', 'after previous less than'],
             meanings={ContAny(): ActionSearchRepeat(regexp='<\s{0,1}', direction=-1)},
             docstring='go after previous less sign')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous less sign', 'before previous less than'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}<', direction=-1, where=-1)},
             docstring='go before previous less sign')
add_csc(acmd)

#
# greater sign
#
acmd = CSCmd(spoken_forms=['next greater sign', 'after greater sign',
                           'next greater than', 'after greater than'],
             meanings={ContAny(): ActionSearchRepeat(regexp='>\s{0,1}')},
             docstring='go after next greater sign')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before greater sign', 'before next greater sign',
                           'before greater than', 'before next greater than'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}>', where=-1)},
             docstring='go before next greater sign')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous greater sign', 'previous greater than',
                           'after previous greater sign', 'after previous greater than'],
             meanings={ContAny(): ActionSearchRepeat(regexp='>\s{0,1}', direction=-1)},
             docstring='go after previous greater sign')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous greater sign', 'before previous greater than'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}>', direction=-1, where=-1)},
             docstring='go before previous greater sign')
add_csc(acmd)

#
# equal sign
#
acmd = CSCmd(spoken_forms=['next equal sign', 'after equal sign',
                           'next equal', 'after equal'],
             meanings={ContAny(): ActionSearchRepeat(regexp='=\s{0,1}')},
             docstring='go after next equal sign')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before equal sign', 'before next equal sign',
                           'before equal', 'before next equal'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}=', where=-1)},
             docstring='go before next equal sign')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous equal sign', 'previous equal',
                           'after previous equal sign', 'after previous equal'],
             meanings={ContAny(): ActionSearchRepeat(regexp='=\s{0,1}', direction=-1)},
             docstring='go after previous equal sign')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous equal sign', 'before previous equal'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}=', direction=-1, where=-1)},
             docstring='go before previous equal sign')
add_csc(acmd)


#
# For moving into and out of balanced expressions
#


#
# parens
#
acmd = CSCmd(spoken_forms=['next paren', 'after paren'],
             meanings={ContAny(): ActionSearchRepeat(regexp='[\\(\\)]\s{0,1}')},
             docstring='go after next paren (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before paren', 'before next paren'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[\\(\\)]', where=-1)},
             docstring='go before next paren (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous paren'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[\\(\\)]', direction=-1)},
             docstring='go after previous paren (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous paren'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[\\(\\)]', direction=-1, where=-1)},
             docstring='go before previous paren (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['out of parens'],
             meanings={ContAny(): ActionSearchRepeat(regexp='[\\)]\s{0,1}')},
             docstring='jump forward out of inner most paren pair')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['back out of parens'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[\\(]', direction=-1, where=-1)},
             docstring='jump backward out of inner most paren pair')
add_csc(acmd)

#
# brackets
#
acmd = CSCmd(spoken_forms=['next bracket', 'after bracket',
                           'next square bracket', 'after square bracket',
                           'next square', 'after square'],
             meanings={ContAny(): ActionSearchRepeat(regexp='[\\[\\]]\s{0,1}')},
             docstring='go after next bracket (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before bracket', 'before next bracket',
                           'before square bracket', 'before next square bracket',
                           'before square', 'before next square'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[\\[\\]]', where=-1)},
             docstring='go before next bracket (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous bracket', 'after previous bracket'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[\\[\\]]', direction=-1)},
             docstring='go after previous bracket (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous bracket',
                           'before previous square bracket',
                           'before previous square'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[\\[\\]]', direction=-1, where=-1)},
             docstring='go before previous bracket (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['out of brackets', 'out of square brackets',
                           'out of square'],
             meanings={ContAny(): ActionSearchRepeat(regexp='[\\]]\s{0,1}')},
             docstring='jump forward out of inner most bracket pair')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['back out of brackets', 'back out of square brackets',
                           'back out of square'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[\\[]', direction=-1, where=-1)},
             docstring='jump backward out of inner most bracket pair')
add_csc(acmd)


#
# braces
#
acmd = CSCmd(spoken_forms=['next brace', 'after brace',
                           'next curly bracket', 'after curly bracket',
                           'next curly', 'after curly'],
             meanings={ContAny(): ActionSearchRepeat(regexp='[\\{\\}]\s{0,1}')},
             docstring='go after next brace (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before brace', 'before curly bracket', 'before curly'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[\\{\\}]', where=-1)},
             docstring='go before next brace (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous brace', 'after previous brace'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[\\{\\}]', direction=-1)},
             docstring='go after previous brace (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous brace',
                           'before previous curly bracket',
                           'before previous curly'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[\\{\\}]', direction=-1, where=-1)},
             docstring='go before previous brace (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['out of braces', 'out of curly brackets',
                           'out of curlies'],
             meanings={ContAny(): ActionSearchRepeat(regexp='[\\}]\s{0,1}')},
             docstring='jump forward out of inner most brace pair')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['back out of braces', 'back out of curly brackets',
                           'back out of curlies'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[\\{]', direction=-1, where=-1)},
             docstring='jump backward out of inner most brace pair')
add_csc(acmd)

#
# angled brackets
#
acmd = CSCmd(spoken_forms=['next angled bracket', 'after angled bracket',
                           'next angled', 'after angled'],
             meanings={ContAny(): ActionSearchRepeat(regexp='[<>]\s{0,1}')},
             docstring='go after next angled (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before angled bracket', 'before angled'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[<>]', where=-1)},
             docstring='go before next angled bracket (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous angled bracket', 'previous angled',
                           'after previous angled bracket',
                           'after previous angled'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[<>]]', direction=-1)},
             docstring='go after previous angled bracket (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous angled bracket',
                           'before previous angled'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[<>]', direction=-1, where=-1)},
             docstring='go before previous angled bracket (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['out of angled', 'out of angled brackets'],
             meanings={ContAny(): ActionSearchRepeat(regexp='[>]\s{0,1}')},
             docstring='jump forward out of inner most angled bracket pair')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['back out of angled', 'back out of angled brackets'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[<]', direction=-1, where=-1)},
             docstring='jump backward out of inner most angled bracket pair')
add_csc(acmd)

#
# quotes
#
acmd = CSCmd(spoken_forms=['next quote', 'after quote'],
             meanings={ContAny(): ActionSearchRepeat(regexp='["]\s{0,1}')},
             docstring='go after next quote (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before quote'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}["]', where=-1)},
             docstring='go before next quote (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous quote', 'after previous quote'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}["]]', direction=-1)},
             docstring='go after previous quote (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous quote'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}["]', direction=-1, where=-1)},
             docstring='go before previous quote (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['out of quotes'],
             meanings={ContAny(): ActionSearchRepeat(regexp='[">]\s{0,1}')},
             docstring='jump forward out of inner most quote pair')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['back out of quotes'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}["], direction=-1, where=-1')},
             docstring='jump backward out of inner most quote pair')
add_csc(acmd)

#
# single quotes
#
acmd = CSCmd(spoken_forms=['next single quote', 'after single quote'],
             meanings={ContAny(): ActionSearchRepeat(regexp='[\']\s{0,1}')},
             docstring='go after next single quote (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before single quote'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[\']', where=-1)},
             docstring='go before next single quote (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous single quote', 'after previous single quote'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[\']]', direction=-1)},
             docstring='go after previous single quote (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous single quote'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[\']', direction=-1, where=-1)},
             docstring='go before previous single quote (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['out of single quotes'],
             meanings={ContAny(): ActionSearchRepeat(regexp='[\'>]\s{0,1}')},
             docstring='jump forward out of inner most single quote pair')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['back out of single quotes'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[\']', direction=-1, where=-1)},
             docstring='jump backward out of inner most single quote pair')
add_csc(acmd)

#
# back quotes
#
acmd = CSCmd(spoken_forms=['next back quote', 'after back quote'],
             meanings={ContAny(): ActionSearchRepeat(regexp='[`]\s{0,1}')},
             docstring='go after next back quote (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before back quote'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[`]', where=-1)},
             docstring='go before next back quote (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['previous back quote', 'after previous back quote'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[`]]', direction=-1)},
             docstring='go after previous back quote (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['before previous back quote'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[`]', direction=-1, where=-1)},
             docstring='go before previous back quote (opening or closing)')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['out of back quotes'],
             meanings={ContAny(): ActionSearchRepeat(regexp='[`>]\s{0,1}')},
             docstring='jump forward out of inner most back quote pair')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['back out of back quotes'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[`]', direction=-1, where=-1)},
             docstring='jump backward out of inner most back quote pair')
add_csc(acmd)


#
# All balanced expressions
#
acmd = CSCmd(spoken_forms=['jump out'],
             meanings={ContAny(): ActionSearchRepeat(regexp='[\]\)\}\'\"]\s{0,1}')},
             docstring='jump out of innermost balanced expression')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['back jump out', 'jump back out'],
             meanings={ContAny(): ActionSearchRepeat(regexp='\s{0,1}[\[\(\{\'\"]',direction=-1, where=-1)},
             docstring='jump backwards out of innermost balanced expression')
add_csc(acmd)


#############################################################################
# Code indentation
#############################################################################

acmd = CSCmd(spoken_forms=['indent', 'tab', 'tab key'],
             meanings={ContAny(): ActionIncrIndentation(levels=1)})
add_csc(acmd)
acmd = CSCmd(spoken_forms=['back indent', 'back tab'],
             meanings={ContAny(): ActionDecrIndentation(levels=1)})
add_csc(acmd)
acmd = CSCmd(spoken_forms=['auto indent'],
             meanings={ContAny(): ActionAutoIndent()})
add_csc(acmd)


#############################################################################
# Repeating last command
#############################################################################


#
# Note: "N times" doesn't do the same thing as utterance like "again N times"
# If "N times" is used immediatly after the command to be repeated
# (e.g. ['page down', '3 times']), then the command is repeated only N-1 times
# because we already executed it once. If it doesn't immediatly follow the
# command to be repeated (e.g.'4 times' in: ['page down', '3 times', '4 times])
# then it is repeated N times.
#
# Utterances like "again N times" on the other hand, always repeat the action
# N times.
#
acmd = CSCmd(spoken_forms=['1 time', '1 times'],
             meanings={ContLastActionWas([ActionRepeatable]): ActionRepeatLastCmd(n_times=1, check_already_repeated=1)},
             docstring='Repeat last command')
add_csc(acmd)

acmd = CSCmd(spoken_forms=['again', 'do that again', 'repeat', 'repeat that', 'redo', 'again 1 time', 'again 1 times', 'repeat 1 time'],
             meanings={ContLastActionWas([ActionRepeatable]): ActionRepeatLastCmd(n_times=1)},
             docstring='Repeat last command')
add_csc(acmd)


acmd = CSCmd(spoken_forms=['2 times'],
             meanings={ContLastActionWas([ActionRepeatable]): ActionRepeatLastCmd(n_times=2, check_already_repeated=1)},
             docstring='Repeat last command')
add_csc(acmd)

acmd = CSCmd(spoken_forms=['again 2 times', 'repeat 2 times'],
             meanings={ContLastActionWas([ActionRepeatable]): ActionRepeatLastCmd(n_times=2)},
             docstring='Repeat last command')
add_csc(acmd)


acmd = CSCmd(spoken_forms=['3 times'],
             meanings={ContLastActionWas([ActionRepeatable]): ActionRepeatLastCmd(n_times=3, check_already_repeated=1)},
             docstring='Repeat last command')
add_csc(acmd)

acmd = CSCmd(spoken_forms=['again 3 times', 'repeat 3 times'],
             meanings={ContLastActionWas([ActionRepeatable]): ActionRepeatLastCmd(n_times=3)},
             docstring='Repeat last command')
add_csc(acmd)

acmd = CSCmd(spoken_forms=['4 times'],
             meanings={ContLastActionWas([ActionRepeatable]): ActionRepeatLastCmd(n_times=4, check_already_repeated=1)},
             docstring='Repeat last command')
add_csc(acmd)

acmd = CSCmd(spoken_forms=['again 4 times', 'repeat 4 times'],
             meanings={ContLastActionWas([ActionRepeatable]): ActionRepeatLastCmd(n_times=4)},
             docstring='Repeat last command')
add_csc(acmd)

acmd = CSCmd(spoken_forms=['5 times'],
             meanings={ContLastActionWas([ActionRepeatable]): ActionRepeatLastCmd(n_times=5, check_already_repeated=1)},
             docstring='Repeat last command')
add_csc(acmd)

acmd = CSCmd(spoken_forms=['again 5 times', 'repeat 5 times'],
             meanings={ContLastActionWas([ActionRepeatable]): ActionRepeatLastCmd(n_times=5)},
             docstring='Repeat last command')
add_csc(acmd)

acmd = CSCmd(spoken_forms=['6 times'],
             meanings={ContLastActionWas([ActionRepeatable]): ActionRepeatLastCmd(n_times=6, check_already_repeated=1)},
             docstring='Repeat last command')
add_csc(acmd)

acmd = CSCmd(spoken_forms=['again 6 times', 'repeat 6 times'],
             meanings={ContLastActionWas([ActionRepeatable]): ActionRepeatLastCmd(n_times=6)},
             docstring='Repeat last command')
add_csc(acmd)

acmd = CSCmd(spoken_forms=['7 times'],
             meanings={ContLastActionWas([ActionRepeatable]): ActionRepeatLastCmd(n_times=7, check_already_repeated=1)},
             docstring='Repeat last command')
add_csc(acmd)

acmd = CSCmd(spoken_forms=['again 7 times', 'repeat 7 times'],
             meanings={ContLastActionWas([ActionRepeatable]): ActionRepeatLastCmd(n_times=7)},
             docstring='Repeat last command')
add_csc(acmd)

acmd = CSCmd(spoken_forms=['8 times'],
             meanings={ContLastActionWas([ActionRepeatable]): ActionRepeatLastCmd(n_times=8, check_already_repeated=1)},
             docstring='Repeat last command')
add_csc(acmd)

acmd = CSCmd(spoken_forms=['again 8 times', 'repeat 8 times'],
             meanings={ContLastActionWas([ActionRepeatable]): ActionRepeatLastCmd(n_times=8)},
             docstring='Repeat last command')
add_csc(acmd)

acmd = CSCmd(spoken_forms=['9 times'],
             meanings={ContLastActionWas([ActionRepeatable]): ActionRepeatLastCmd(n_times=9, check_already_repeated=1)},
             docstring='Repeat last command')
add_csc(acmd)

acmd = CSCmd(spoken_forms=['again 9 times', 'repeat 9 times'],
             meanings={ContLastActionWas([ActionRepeatable]): ActionRepeatLastCmd(n_times=9)},
             docstring='Repeat last command')
add_csc(acmd)

acmd = CSCmd(spoken_forms=['10 times'],
             meanings={ContLastActionWas([ActionRepeatable]): ActionRepeatLastCmd(n_times=10, check_already_repeated=1)},
             docstring='Repeat last command')
add_csc(acmd)

acmd = CSCmd(spoken_forms=['again 10 time', 'repeat 10 time'],
             meanings={ContLastActionWas([ActionRepeatable]): ActionRepeatLastCmd(n_times=10)},
             docstring='Repeat last command')
add_csc(acmd)


#############################################################################
# Changing direction of last command
#############################################################################

acmd = CSCmd(spoken_forms=['reverse', 'reverse direction'],
             meanings={ContLastActionWas([ActionRepeatable, ActionBidirectional]): ActionRepeatBidirectCmd(n_times=1, direction=None)},
             docstring='Reverses the direction of previous command')
add_csc(acmd)

acmd = CSCmd(spoken_forms=['backward', 'upward', 'leftward', 'previous one'],
             meanings={ContLastActionWas([ActionRepeatable, ActionBidirectional]): ActionRepeatBidirectCmd(n_times=1, direction=-1)},
             docstring='Repeats the previous command in backward/up/left direction.')
add_csc(acmd)

acmd = CSCmd(spoken_forms=['forward', 'downward', 'rightward', 'next one'],
             meanings={ContLastActionWas([ActionRepeatable, ActionBidirectional]): ActionRepeatBidirectCmd(n_times=1, direction=1)},
             docstring='Repeats the previous command in forward/down/right direction.')
add_csc(acmd)



##############################################################################
# CSCs and LSAs that apply for more than one language (but not necessarily
# all)
##############################################################################

add_lsa(['multiply by', 'multiplied by', 'times'], 
        {'C': ' * ', 'python': ' * ', 'perl': ' * '})
add_lsa(['to the power', 'to the power of', 'power of'], 
        {'C': '**', 'python': '**', 'perl': '**'})
add_lsa(['divide by', 'divided by'],
        {'C': ' / ', 'python': ' / ', 'perl': ' / '})
add_lsa(['plus'], {'C': ' + ', 'python': ' + ', 'perl': ' + '})
add_lsa(['minus'], {'C': ' - ', 'python': ' - ', 'perl': ' - '})
add_lsa(['modulo'], {'C': ' % ', 'python': ' % '})
add_lsa(['left shift'], {'C': ' << ', 'python': ' << ', 'perl': ' << '})
add_lsa(['right shift'], {'C': ' >> ', 'python': ' >> ', 'perl': ' >> '})
add_lsa(['not'], {'python': 'not ', 'C': '!', 'perl': '!'})
add_lsa(['or'], {'python': ' or ', 'C': ' || ', 'perl': ' || '})
add_lsa(['and'], {'python': ' and ', 'C': ' && ', 'perl': ' && '})
add_lsa(['binary and', 'bitwise and'], {'C': ' & ', 'python': ' & '})
add_lsa(['binary or', 'bitwise or'], {'C': ' | ', 'python': ' | '})
add_lsa(['binary not', 'bitwise not'], {'C': '~', 'python': '~'})
add_lsa(['binary exclusive or', 'binary X. or', 'bitwise exclusive or', 'bitwise X. or'], {'C': ' ^ ', 'python': ' ^ '})
add_lsa(['equals', 'equal', 'is assigned', 'assign value'],
        {'C': ' = ', 'python': ' = '})
add_lsa(['less than', 'is less than'],
        {'C': ' < ', 'python': ' < ', 'perl': ' < '})
add_lsa(['greater than', 'is greater than'],
        {'C': ' > ', 'python': ' > ', 'perl': ' > '})
add_lsa(['less or equal to', 'is less or equal to', 'less or equal',
        'is less or equal'],
        {'C': ' <= ', 'python': ' <= ', 'perl': ' <= '})
add_lsa(['greater or equal to', 'is greater or equal to', 'greater or equal',
        'is greater or equal'],
        {'C': ' >= ', 'python': ' >= ', 'perl': ' >= '})
add_lsa(['not equal', 'is not equal', 'not equal to', 'is not equal to',
        'is different from', 'differs from', 'bang equal'],
        {'C': ' != ', 'python': ' != ', 'perl': ' != '})
add_lsa(['equal to', 'is equal to', 'is equal'],
        {'C': ' == ', 'python': ' == ', 'perl': ' == '})
add_lsa(['without arguments', 'with no arguments', 'without argument',
        'with no argument'],
        {'python': '()', 'perl': '()', 'C': '()'})
add_lsa(['print'], {'python': 'print ', 'perl': 'print '})


acmd = CSCmd(spoken_forms=['with arguments', 'with argument', 'call with',
                           'called with'],
             meanings={ContC(): gen_parens_pair, ContPy(): gen_parens_pair,
                       ContPerl(): gen_parens_pair},
             docstring='argument list for function')
add_csc(acmd)        
add_lsa(['comment line', 'new comment'], {'perl': '\n# ', 'python': '\n# '})
add_lsa(['return'], {'C': 'return ', 'python': 'return '})
add_lsa(['empty dictionary', 'empty hash'], {'python': '{}', 'perl': '{}'})
acmd = CSCmd(spoken_forms=['dictionary with elements', 'hash with elements', 
                           'new dictionary', 'new hash',
                           'dictionary with items', 'hash with items'],
             meanings={ContPy(): ActionInsert('{', '}'),
                       ContPerl(): ActionInsert('(', ')')},
             docstring='dictionary with enumareted elements')
add_csc(acmd)             
add_lsa(['empty list'], {'python': '[]', 'perl': '()'})
acmd = CSCmd(spoken_forms=['list with elements', 'new list',
                           'list with items'],
             meanings={ContPy(): ActionInsert('[', ']'),
                       ContPerl(): ActionInsert('(', ')')},
             docstring='list with enumareted elements')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['at index'],
             meanings={ContPy(): ActionInsert('[', ']'),
                       ContC(): ActionInsert('[', ']'),
                       ContPerl(): ActionInsert('[', ']')},
             docstring='array element access')
add_csc(acmd)             
acmd = CSCmd(spoken_forms=['at key'],
             meanings={ContPy(): ActionInsert('[', ']'), 
                       ContPerl(): ActionInsert('{', '}')},
             docstring='dictionary/hash element access')
add_csc(acmd)                          
acmd = CSCmd(spoken_forms=['new statement'],
             meanings={ContPy(): py_new_statement, ContC(): c_new_statement},
             docstring='start new statement on next line')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['body', 'goto body'],
             meanings={ContC(): c_goto_body, ContPy(): py_goto_body,
                       ContPerl(): c_goto_body},
             docstring = 'move to body of a compound statement')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['for', 'for loop'],
             meanings={ContC(): c_simple_for, ContPy(): py_simple_for,
                       ContPerl(): c_simple_for},
             docstring='for loop')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['while', 'while loop'],
             meanings={ContC(): c_simple_while,
                       ContPy(): ActionInsert('while ', ':\n\t'),
                       ContPerl(): c_simple_while},
             docstring='while loop')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['do', 'do the following', 'loop body', 'for body',
                           'while body'],
             meanings={ContC(): c_goto_body, ContPy(): py_goto_body,
                       ContPerl(): c_goto_body},
             docstring = 'move to body of loop')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['if', 'if statement'],
             meanings={ContPy(): ActionInsert('if ', ':\n\t'),
                       ContC(): ActionInsert('if (', ')\n\t{\n\t}'),
                       ContPerl(): ActionInsert('if (', ') {\n\t}')},
             docstring = 'if statement')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['else if', 'else if clause', 'elsif',
                           'elsif clause', 'elif', 'elif clause'],
             meanings={ContPy(): ActionInsertNewClause('($|\n)', 'elif ', ': \n\t'),
                       ContC(): c_else_if,
                       ContPerl(): perl_else_if},
             docstring = 'else if clause of conditional statement')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['else clause', 'else'],
             meanings={ContPy(): ActionInsertNewClause('($|\n)', 'else:\n\t', ''),
                       ContC(): c_else,
                       ContPerl(): c_else},
             docstring = 'else clause of conditional statement')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['then', 'then do', 'then do the following',
                           'if body'],
             meanings={ContPy(): py_goto_body, ContC(): c_goto_body,
                       ContPerl(): c_goto_body},
             docstring='move to body of a conditional')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['class', 'define class', 'declare class',
                           'class definition', 'class declaration',
                           'new class'],
             meanings={ContC(): cpp_class_definition,
                       ContPy(): py_class_definition},
             docstring='class definition')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['sub class of', 'inherits from', 'is subclass',
                           'is subclass of', 'with superclass',
                           'with superclasses'],
             meanings={ContC(): cpp_subclass, ContPy(): gen_parens_pair},
             docstring='superclasses of a class')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['class body'],
             meanings={ContC(): cpp_class_body, ContPy(): py_class_body},
             docstring='move to body of class definition')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['define method', 'declare method'],
             meanings={ContC(): c_function_declaration,
                       ContPy(): py_method_declaration},
             docstring='method definition')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['add argument', 'add arguments'],
             meanings={ContC(): c_function_add_argument,
                       ContPy(): py_function_add_argument},
             docstring='move to end of argument list of a function call or declaration')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['method body'],
             meanings={ContC(): c_function_body, ContPy(): py_function_body},
             docstring='move to body of a function definition')
add_csc(acmd)


###############################################################################
# Python specific stuff
###############################################################################

#
# Python standard symbols
#
standard_symbols_in([vc_globals.config + os.sep + 'py_std_sym.py'])

#
# Define the native syntax of Python
#
define_language('python',
                LangDef(regexp_symbol='[a-zA-Z_][a-zA-Z0-9_]*',
                        regexps_no_symbols=['#[^\n]*\n', '"""[\s\S]*?"""',
                                            '"([^"]|\\")*?"',
                                            '\'([^\']|\\\')*?\'']))

#
# CSCs and LSAs specific to Python
#
add_lsa(['continue statement'], {'python': '\\\n'})
add_lsa(['assert'], {'python': 'assert '})
add_lsa(['del', 'delete', 'delete', 'delete', 'delete object',
         'delete instance'],
        {'python': 'del '})
add_lsa(['raise', 'raise exception'], {'python': 'raise '})
acmd = CSCmd(spoken_forms=['lambda'],
             meanings={ContPy(): ActionInsert('lambda ', ': ')},
             docstring='python lamdba function')
add_csc(acmd)
add_lsa(['return'], {'python': 'return '})
add_lsa(['break'], {'python': 'break\n'})
add_lsa(['global', 'global variable', 'global variables'],
        {'python': 'global '})
add_lsa(['from', 'from module'], {'python': 'from '})
# this form used for statements : import module1, module2, etc...
add_lsa(['import', 'import module', 'import modules'], {'python': 'import '})
# this form used for statements like: from module symbol1, symbol2, etc...
add_lsa(['import symbols', 'import symbol'], {'python': ' import '})
# this form used for statements like: from module import all
add_lsa(['import all'], {'python': ' import all'})
acmd = CSCmd(spoken_forms=['try'],
             meanings={ContPy(): ActionInsert('try:\n\t', '')},
             docstring='python try statement')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['except', 'except for', 'catch exceptions'],
             meanings={ContPy(): ActionInsertNewClause('($|\n)', 'except ', ': \n\t')},
             docstring='python except statement')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['finally', 'finally do'],
             meanings={ContPy(): ActionInsertNewClause('($|\n)', 'finally:\n\t', '')},
             docstring='finally clause of python try statement')
add_csc(acmd)
add_lsa(['continue'], {'python': 'continue\n'})
add_lsa(['exec'], {'python': 'exec '})
add_lsa(['pass'], {'python': 'pass\n'})
add_lsa(['in', 'in list'], {'python': ' in '})
add_lsa(['triple quote', 'open triple quote', 'close triple quote'],
        {'python': '"""'})
add_lsa(['empty triple quotes', 'empty triple'], {'python': '""""""'})
acmd = CSCmd(spoken_forms=['between triple quotes', 'triple quotes'],
             meanings={ContAny(): ActionInsert('"""', '"""')},
             docstring = 'put cursor between triple quotes: """^"""')
add_csc(acmd)

add_lsa(['three single quote', 'open three single quote',
         'open three single', 'close three single quote',
         'close three single'],
         {'python': '\'\'\''})
add_lsa(['empty three single quotes', 'empty three single'],
         {'python': '\'\'\'\'\'\''})
acmd = CSCmd(spoken_forms=['between three single quotes',
                           'between three single', 'three single quotes'],
             meanings={ContAny(): ActionInsert('\'\'\'', '\'\'\'')},
             docstring = 'put cursor between three single quotes: \'\'\'^\'\'\'')
add_csc(acmd)
add_lsa(['concatenate', 'concatenate with'], {'python': ' + '})
add_lsa(['collect arguments', 'collect rest'], {'python': '**'})

# '<>' is obsolete in python ('!=' is now the encouraged form), but we include
# it so we can select code that uses the obsolete form
add_lsa(['not equal', 'is not equal', 'not equal to', 'is not equal to',
        'is different from', 'differs from', 'less greater',
        'less than greater than'],
        {'python': ' <> '})
add_lsa(['is', 'is same', 'same as', 'is same as'], {'python': ' is '})
add_lsa(['empty tuple'], {'python': '()'})
acmd = CSCmd(spoken_forms=['tuple with elements', 'new tuple',
                           'tuple with items'],
             meanings={ContPy(): ActionInsert('(', ')')},
             docstring='python tuple with enumareted elements')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['range of'],
             meanings={ContPy(): ActionInsert('range(', ')')},
             docstring='types range(^)')
add_csc(acmd)


###############################################################################
# C/C++ specific stuff
###############################################################################

#
# Define native syntax of C/C++
#
define_language('C',
                LangDef(regexp_symbol='[a-zA-Z_][a-zA-Z0-9_]*',
                        regexps_no_symbols=['/\*.*\*/', '//[^\n]*\n',
                                            '"([^"]|\\")*?"',
                                            '\'([^\']|\\\')*?\'']))

acmd = CSCmd(spoken_forms=['header wrapper', 'wrap header'],
             meanings={ContC(): ActionHeaderWrapper()},
             docstring='insert code template for unique #include')
add_csc(acmd)

acmd = CSCmd(spoken_forms=['macro if'],
             meanings={ContC(): ActionInsert('#ifdef', '\n#endif\n')},
             docstring='insert code template for #ifdef')
add_csc(acmd)

acmd = CSCmd(spoken_forms=['macro if not'],
             meanings={ContC(): ActionInsert('#ifndef', '\n#endif\n')},
             docstring='insert code template for #ifndef')
add_csc(acmd)

add_lsa(['macro define'], {'C': '#define'})

add_lsa(['macro include'], {'C': '#include'})                       

add_lsa(['macro undo define'], {'C': '#undef'})

###############################################################################
# Add words which are missing from the SR vocab
###############################################################################

sr_interface.addWord('ellipsis')
sr_interface.addWord('paren')
sr_interface.addWord('parens')
sr_interface.addWord('tilde')
# 'un' prefix as in unspecified, untranslated etc...
sr_interface.addWord('un')


#
# For some reason, if we don't add this word, ['sub', 'class'] is often
# recognised as ['sub\\sub routine', 'class'] (even if I use recognitionMimic).
# This causes problems because the spoken form of this is 'sub routine class'
# which the interpreter doesn't understand.
#
# Wonder why NatSpeak insists on sending a word with spoken form
# 'sub routine'
#
sr_interface.addWord('sub class\\sub class')


if (__name__ == '__main__'): sr_interface.disconnect()
