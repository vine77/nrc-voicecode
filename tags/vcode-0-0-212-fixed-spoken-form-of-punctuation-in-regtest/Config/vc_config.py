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

# should this be here, or should the contents of these modules be added
# to the configuration namespace by NewMediatorObject?
from SpacingState import *
from config_helpers import *

import CmdInterp

from CSCmd import CSCmd
from CmdInterp import LSAlias
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

mod_pythonw = KnownTargetModule.LocalInterpreter(module_name = 'PYTHONW',
    title_varies = 1)
  
#     add them to the RecogStartMgr
add_module(mod_Emacs)
add_module(mod_exceed)
add_module(mod_ttssh)
add_module(mod_python)
add_module(mod_pythonw)

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

acmd = CSCmd(spoken_forms=['compile symbols'], 
             meanings={ContLanguage(None): ActionCompileSymbols()}, 
             docstring='compile symbols from active buffer.')
add_csc(acmd)


#############################################################################
# Punctuation marks.
#############################################################################

# NOTE: DO NOT DELETE OR EDIT THE FOLLOWING STANDARD FORMS
#
# They are necessary to generate LSAs corresponding to the standard built-in
# punctuation words, without which CmdInterp will generate new symbols 
# from their spoken forms.  If you want to suppress a particular form, delete
# it from the speech-engine's vocabulary, and VoiceCode will
# automatically omit the corresponding LSA.  If you want to change the
# spacing of a standard form, simply add your own LSA with the same
# written and spoken form and VoiceCode will again automatically omit
# the corresponding standard form.

# If you are using a different speech engine which defines different
# standard forms, or a different language, check at the VoiceCode web
# site for alternative lists of standard forms, or go through the
# speech engine's vocabulary and create your own list (and please
# contribute it to VoiceCode for the benefit of other users).

# These standard forms for punctuation, as defined in the US English
# vocabulary of NaturallySpeaking 6.  They are used for
# the navigation-by-punctuation CSCs and to define corresponding LSAs
# for dictating punctuation.  

std_US_punc = \
    SinglePunctuation(name = 'standard punctuation (US English)')
std_US_punc.add('\\', ['backslash'], like_backslash)
std_US_punc.add('', ['New-Line', 'Next-Line'], hard_new_line)
std_US_punc.add('', ['New-Paragraph', 'Next-Paragraph'], 
    hard_paragraph)
std_US_punc.add('', ['space-bar'], hard_space)
std_US_punc.add('', ['tab-key'], hard_tab)
std_US_punc.add('!', ['exclamation-mark', 'exclamation-point'])
std_US_punc.add('#', ['number-sign', 'pound-sign'], 
    no_space_after)
std_US_punc.add('$', ['dollar-sign'], no_space_after)
std_US_punc.add('%', ['percent-sign'])
std_US_punc.add('&', ['ampersand', 'and-sign'], 
    no_space_after)
std_US_punc.add("'", ['apostrophe'], no_space_before | letters_and_digits)
std_US_punc.add("*", ['asterisk'])
std_US_punc.add("+", ['plus-sign'])
std_US_punc.add("-", ['minus-sign'])
std_US_punc.add("-", ['hyphen', 'numeric-hyphen'], 
    like_hyphen)
std_US_punc.add(",", ['comma'], like_comma)
std_US_punc.add(",", ['numeric-comma'], like_dot)
std_US_punc.add("--", ['dash'])
std_US_punc.add(".", ['dot'], like_dot)
std_US_punc.add(".", ['period'], end_sentence)
std_US_punc.add(".", ['point'], like_point)
std_US_punc.add("...", ['ellipsis'], like_dot)
std_US_punc.add("/", ['slash', 'forward-slash'], 
    like_slash)
std_US_punc.add(":", ['colon'], like_colon)
std_US_punc.add(":", ['numeric-colon'], like_dot)
std_US_punc.add(";", ['semicolon'], no_space_before)
std_US_punc.add("<", ['less-than'])
std_US_punc.add(">", ['greater-than'])
std_US_punc.add("=", ['equal-sign'])
std_US_punc.add('?', ['question-mark'], like_dot)
std_US_punc.add('@', ['at-sign'], like_hyphen)
std_US_punc.add('^', ['caret'], like_dot)
std_US_punc.add('_', ['underscore'], like_hyphen)
std_US_punc.add('|', ['vertical-bar'])
std_US_punc.add('~', ['tilde'], no_space_after)
std_US_punc.add('`', ['backquote'],
    no_space_after)
# this is a standard form, though open-/left-/right-/close- forms are
# not defined, so we need to add it as SinglePunctuation, not
# as PairedQuotes

# change this assignment if you are not using (NaturallySpeaking) US
# English edition
std_punc = std_US_punc

alt_US_punc = \
    SinglePunctuation(name = 'alternative punctuation')
alt_US_punc.add('', ['blank space'], 
    spacing = hard_space)
alt_US_punc.add('*', ['star'], spacing = like_dot)
# what is the correct spacing for this?  should it be different for
# different languages? (e.g. exponentiation vs. Python keyword
# arguments)
alt_US_punc.add('**', ['double star', 'double asterisk'],
    like_dot)
alt_US_punc.add('|', ['pipe', 'pipe sign'])
alt_US_punc.add('!', ['bang'], no_space_after)
alt_US_punc.add('~', ['squiggle'], no_space_after)
alt_US_punc.add('::', ['double colon', 'colon colon'], 
    spacing = like_hyphen)

# shorter forms
alt_US_punc.add("+", ['plus'])
alt_US_punc.add("-", ['minus'])
alt_US_punc.add('%', ['percent'])
alt_US_punc.add('#', ['pound'], no_space_after)
alt_US_punc.add(";", ['semi'], no_space_before)


# Alain's
alt_US_punc.add('&', ['and percent'])
alt_US_punc.add('<', ['less sign'], spacing =
    like_dot)
alt_US_punc.add('>', ['greater sign'], spacing =
    like_dot)

alt_punc = alt_US_punc


#
# Generic balanced expressions (e.g. "", '', (), [], {})
#

std_US_grouping = \
    LeftRightPunctuation(name = 'standard grouping (US English)',
        singular_pair = ['%s pair'], 
        plural_pair = ['between %s', '%s pair', '%s'])
    
std_US_grouping.add('(',')', 
    ['paren'], ['parens'])
std_US_grouping.add('(',')', 
    ['parenthesis'])
# added separately so that if the user overrides paren, the singular
# LSAs for parenthesis are still added
std_US_grouping.add('[',']', 
    ['bracket'], ['brackets'])
std_US_grouping.add('{','}', 
    ['brace'], ['braces'])
std_US_grouping.add('<','>', 
    ['angle-bracket'], ['angle-brackets'])

# change this assignment if you are not using (NaturallySpeaking) US
# English edition
std_grouping = std_US_grouping

std_US_quotes = \
    PairedQuotes(name = 'standard quotes (US English)',
        plural_pair = ['between %s', '%s'])

std_US_quotes.add('"', ['quote', 'quotes'], ['quotes'])
# begin-quotes and open-quotes are both standard forms for a 'single'
# double-quote symbol (")
std_US_quotes.add("'", ['single-quote'], ['single-quotes'])

# change this assignment if you are not using (NaturallySpeaking) US
# English edition
std_quotes = std_US_quotes


# alternative forms
alt_US_grouping = \
    LeftRightPunctuation(name = 'alternate grouping',
        singular_pair = ['%s pair'], 
        plural_pair = ['between %s', '%s pair', '%s'])
    
alt_US_grouping.add('[',']', 
    ['square-bracket'], ['square-brackets'])
alt_US_grouping.add('{','}', 
    ['curly', 'curly-brace', 'curly-bracket'], 
    ['curlies', 'curly-braces', 'curly-brackets'])
alt_US_grouping.add('<','>', 
    ['angle'], ['angles'])

alt_grouping = alt_US_grouping

alt_US_quotes = \
    PairedQuotes(name = 'alternate quotes',
        plural_pair = ['between %s', '%s'])
alt_US_quotes.add('`', ['backquote', 'reverse-quote'], 
    ['backquotes', 'reverse-quotes'])
# oops - punctuation regression test tests empty backquotes (even though
# it is nonsense)
#alt_US_quotes.add('`', ['backquote', 'reverse-quote'], 
#   ['backquotes', 'reverse-quotes'], no_empty = 1)

alt_quotes = alt_US_quotes

#
# Generic balanced expressions (e.g. "", '', (), [], {})
#
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


#
# Escaped characters (back slash a., a, alpha, etc.)
#

escaped_characters = LSAliasSet(name = 'escaped characters', 
    description = 'characters escaped with backslashes')
add_escaped_characters(escaped_characters)

add_lsa_set(escaped_characters)

#
# Commands for jumping to a specific punctuation mark
# Not exhaustive.
# This really calls for some sort of grammar to automatically generate the
# spoken forms. But for now, exhaustively (or "exhaustingly" ;-) listing all
# possible spoken forms will have to do (although it's definitely exhausting"
#



#
# All balanced expressions
#
acmd = CSCmd(spoken_forms=['jump out'],
             meanings={ContAny(): ActionSearchRepeat(regexp='[\]\)\}\'\"] {0,1}')},
             docstring='jump out of innermost balanced expression')
add_csc(acmd)

acmd = CSCmd(spoken_forms=['back jump out', 'jump back out'],
             meanings={ContAny(): ActionSearchRepeat(regexp=' {0,1}[\[\(\{\'\"]',direction=-1, where=-1)},
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

repeat_last = CSCmdSet(name = 'repeat last command', 
    description = """Repeat last command.  
        Note: If "N times" is used immediatly after the command to be repeated
        (e.g. ['page down', '3 times']), then the command is repeated only N-1
        times because we already executed it once. If it doesn't immediatly
        follow the command to be repeated (e.g.'4 times' in: ['page down', '3
        times', '4 times]) then it is repeated N times.

        Utterances like "again N times" on the other hand, always repeat the
        action N times.
        """)

add_repeats(repeat_last)

acmd = CSCmd(spoken_forms = \
                 ['again', 'do that again', 'repeat', 'repeat that', 'redo'],
             meanings={ContLastActionWas([ActionRepeatable]): \
                 ActionRepeatLastCmd(n_times=1)},
             docstring='Repeat last command')

# add extra forms for repeat 1 time which don't match the pattern
repeat_last.add_csc(acmd, name = 'repeat once')

add_csc_set(repeat_last)


#############################################################################
# Changing direction of last command
#############################################################################

change_direction = CSCmdSet(name = 'change direction of last command', 
    description = "Repeat last command (e.g. search) " + \
                  "in the opposite direction.")

acmd = CSCmd(spoken_forms=['reverse', 'reverse direction'],
             meanings={ContLastActionWas([ActionRepeatable, ActionBidirectional]): ActionRepeatBidirectCmd(n_times=1, direction=None)},
             docstring='Reverses the direction of previous command')
change_direction.add_csc(acmd)

acmd = CSCmd(spoken_forms=['backward', 'upward', 'leftward', 'previous one'],
             meanings={ContLastActionWas([ActionRepeatable, ActionBidirectional]): ActionRepeatBidirectCmd(n_times=1, direction=-1)},
             docstring='Repeats the previous command in backward/up/left direction.')
change_direction.add_csc(acmd)

acmd = CSCmd(spoken_forms=['forward', 'downward', 'rightward', 'next one'],
             meanings={ContLastActionWas([ActionRepeatable, ActionBidirectional]): ActionRepeatBidirectCmd(n_times=1, direction=1)},
             docstring='Repeats the previous command in forward/down/right direction.')
change_direction.add_csc(acmd)


add_csc_set(change_direction)

#############################################################################
# Insertions and deletions
#############################################################################

#
# repeatable backspace commands (back space / delete backwards "" and 2 to 5
#

backspacing  = CSCmdSet(name = 'backspace multiple times',
    description = "backspace 1 to n times.")

add_backspacing(backspacing)


add_csc_set(backspacing)
##############################################################################
# CSCs and LSAs that apply for more than one language (but not necessarily
# all)
##############################################################################

add_lsa(LSAlias(['multiply by', 'multiplied by', 'times'], 
        {'C': ' * ', 'python': ' * ', 'perl': ' * '}))
add_lsa(LSAlias(['to the power', 'to the power of', 'power of'], 
        {'C': '**', 'python': '**', 'perl': '**'}))
add_lsa(LSAlias(['divide by', 'divided by'],
        {'C': ' / ', 'python': ' / ', 'perl': ' / '}))
add_lsa(LSAlias(['plus'], {'C': ' + ', 'python': ' + ', 'perl': ' + '}))
add_lsa(LSAlias(['minus'], {'C': ' - ', 'python': ' - ', 'perl': ' - '}))
add_lsa(LSAlias(['modulo'], {'C': ' % ', 'python': ' % '}))
add_lsa(LSAlias(['left shift'], {'C': ' << ', 'python': ' << ', 'perl': ' << '}))
add_lsa(LSAlias(['right shift'], {'C': ' >> ', 'python': ' >> ', 'perl': ' >> '}))
add_lsa(LSAlias(['not'], {'python': 'not ', 'C': '!', 'perl': '!'}))
add_lsa(LSAlias(['or'], {'python': ' or ', 'C': ' || ', 'perl': ' || '}))
add_lsa(LSAlias(['and'], {'python': ' and ', 'C': ' && ', 'perl': ' && '}))
add_lsa(LSAlias(['binary and', 'bitwise and'], {'C': ' & ', 'python': ' & '}))
add_lsa(LSAlias(['binary or', 'bitwise or'], {'C': ' | ', 'python': ' | '}))
add_lsa(LSAlias(['binary not', 'bitwise not'], {'C': '~', 'python': '~'}))
add_lsa(LSAlias(['binary exclusive or', 'binary X. or', 'bitwise exclusive or', 'bitwise X. or'], {'C': ' ^ ', 'python': ' ^ '}))
add_lsa(LSAlias(['equals', 'equal', 'is assigned', 'assign value'],
        {'C': ' = ', 'python': ' = '}))
add_lsa(LSAlias(['less than', 'is less than'],
        {'C': ' < ', 'python': ' < ', 'perl': ' < '}))
add_lsa(LSAlias(['greater than', 'is greater than'],
        {'C': ' > ', 'python': ' > ', 'perl': ' > '}))
add_lsa(LSAlias(['less or equal to', 'is less or equal to', 'less or equal',
        'is less or equal'],
        {'C': ' <= ', 'python': ' <= ', 'perl': ' <= '}))
add_lsa(LSAlias(['greater or equal to', 'is greater or equal to', 'greater or equal',
        'is greater or equal'],
        {'C': ' >= ', 'python': ' >= ', 'perl': ' >= '}))
add_lsa(LSAlias(['not equal', 'is not equal', 'not equal to', 'is not equal to',
        'is different from', 'differs from', 'bang equal'],
        {'C': ' != ', 'python': ' != ', 'perl': ' != '}))
add_lsa(LSAlias(['equal to', 'is equal to', 'is equal'],
        {'C': ' == ', 'python': ' == ', 'perl': ' == '}))
add_lsa(LSAlias(['without arguments', 'with no arguments', 'without argument',
        'with no argument'],
        {'python': '()', 'perl': '()', 'C': '()'}))
add_lsa(LSAlias(['print'], {'python': 'print ', 'perl': 'print '}))


acmd = CSCmd(spoken_forms=['with arguments', 'with argument', 'call with',
                           'called with'],
             meanings={ContC(): gen_parens_pair, ContPy(): gen_parens_pair,
                       ContPerl(): gen_parens_pair},
             docstring='argument list for function')
add_csc(acmd)        
add_lsa(LSAlias(['comment line', 'new comment'], {'perl': '\n# ', 'python': '\n# '}))
add_lsa(LSAlias(['return'], {'C': 'return ', 'python': 'return '}))
add_lsa(LSAlias(['empty dictionary', 'empty hash'], {'python': '{}', 'perl': '{}'}))
acmd = CSCmd(spoken_forms=['dictionary with elements', 'hash with elements', 
                           'new dictionary', 'new hash',
                           'dictionary with items', 'hash with items'],
             meanings={ContPy(): ActionInsert('{', '}'),
                       ContPerl(): ActionInsert('(', ')')},
             docstring='dictionary with enumareted elements')
add_csc(acmd)             
add_lsa(LSAlias(['empty list'], {'python': '[]', 'perl': '()'}))
acmd = CSCmd(spoken_forms=['list with elements', 'new list',
                           'list with items'],
             meanings={ContPy(): ActionInsert('[', ']'),
                       ContPerl(): ActionInsert('(', ')')},
             docstring='list with enumareted elements')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['at index', 'indexed by'],
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
             meanings={ContPy(): ActionInsertNewClause('($|\n)', 
                           code_bef = 'elif ', code_after = ': \n\t', 
#                           back_indent_by=0,
# I suspect the default value of back_indent_by = 1 won't hurt in the
# Emacs case, because elif will have the correct indentatation
# initially, and Emacs will be smart enough to leave it alone.  
# It is, except if something on the previous line (like a return
# statement) triggers a back indent
                           where = -1),
# Using where = -1 should solve the problem of the extra \n
# -- DCF
#                           code_bef = 'elif ', code_after = ': \n\t', where = -1),
                       ContC(): c_else_if,
                       ContPerl(): perl_else_if},
             docstring = 'else if clause of conditional statement')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['else clause', 'else'],
             meanings={ContPy(): ActionInsertNewClause('($|\n)', 
                          code_bef = 'else:\n\t', code_after = '', where = -1),
# try where = -1 here as well 
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
acmd = CSCmd(spoken_forms=['define method', 'declare method', 'add method'],
             meanings={ContC(): c_function_declaration,
                       ContPy(): py_method_declaration},
             docstring='method definition')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['define function', 'declare function'],
             meanings={ContC(): c_function_declaration,
                       ContPy(): c_function_declaration},
             docstring='function definition')
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
add_lsa(LSAlias(['none'], {'python': 'None'}))
add_lsa(LSAlias(['self dot'], {'python': 'self.'}))
add_lsa(LSAlias(['continue statement'], {'python': '\\\n'}))
add_lsa(LSAlias(['assert'], {'python': 'assert '}))
add_lsa(LSAlias(['del', 'delete', 'delete', 'delete', 'delete object',
         'delete instance'],
        {'python': 'del '}))
add_lsa(LSAlias(['raise', 'raise exception'], {'python': 'raise '}))
acmd = CSCmd(spoken_forms=['lambda'],
             meanings={ContPy(): ActionInsert('lambda ', ': ')},
             docstring='python lamdba function')
add_csc(acmd)
add_lsa(LSAlias(['return'], {'python': 'return '}))
add_lsa(LSAlias(['break'], {'python': 'break\n'}))
add_lsa(LSAlias(['global', 'global variable', 'global variables'],
        {'python': 'global '}))
add_lsa(LSAlias(['from', 'from module'], {'python': 'from '}))
# this form used for statements : import module1, module2, etc...
add_lsa(LSAlias(['import', 'import module', 'import modules'], {'python': 'import '}))
# this form used for statements like: from module symbol1, symbol2, etc...
add_lsa(LSAlias(['import symbols', 'import symbol'], {'python': ' import '}))
# this form used for statements like: from module import all
add_lsa(LSAlias(['import all'], {'python': ' import all'}))
acmd = CSCmd(spoken_forms=['try'],
             meanings={ContPy(): ActionInsert('try:\n\t', '')},
             docstring='python try statement')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['except', 'except for', 'catch exceptions', 'except when', 'except clause'],
             meanings={ContPy(): ActionInsertNewClause('($|\n)', 'except ', ': \n\t')},
             docstring='python except statement')
add_csc(acmd)
acmd = CSCmd(spoken_forms=['finally', 'finally do'],
             meanings={ContPy(): ActionInsertNewClause('($|\n)', 'finally:\n\t', '')},
             docstring='finally clause of python try statement')
add_csc(acmd)
add_lsa(LSAlias(['continue'], {'python': 'continue\n'}))
add_lsa(LSAlias(['exec'], {'python': 'exec '}))
add_lsa(LSAlias(['pass'], {'python': 'pass\n'}))
add_lsa(LSAlias(['in', 'in list'], {'python': ' in '}))
add_lsa(LSAlias(['triple quote', 'open triple quote', 'close triple quote'],
        {'python': '"""'}))
add_lsa(LSAlias(['empty triple quotes', 'empty triple'], {'python': '""""""'}))
acmd = CSCmd(spoken_forms=['between triple quotes', 'triple quotes'],
             meanings={ContAny(): ActionInsert('"""', '"""')},
             docstring = 'put cursor between triple quotes: """^"""')
add_csc(acmd)

add_lsa(LSAlias(['three single quote', 'open three single quote',
         'open three single', 'close three single quote',
         'close three single'],
         {'python': '\'\'\''}))
add_lsa(LSAlias(['empty three single quotes', 'empty three single'],
         {'python': '\'\'\'\'\'\''}))
acmd = CSCmd(spoken_forms=['between three single quotes',
                           'between three single', 'three single quotes'],
             meanings={ContAny(): ActionInsert('\'\'\'', '\'\'\'')},
             docstring = 'put cursor between three single quotes: \'\'\'^\'\'\'')
add_csc(acmd)
add_lsa(LSAlias(['concatenate', 'concatenate with'], {'python': ' + '}))
add_lsa(LSAlias(['collect arguments', 'collect rest'], {'python': '**'}))

# '<>' is obsolete in python ('!=' is now the encouraged form), but we include
# it so we can select code that uses the obsolete form
add_lsa(LSAlias(['not equal', 'is not equal', 'not equal to', 'is not equal to',
        'is different from', 'differs from', 'less greater',
        'less than greater than'],
        {'python': ' <> '}))
add_lsa(LSAlias(['is', 'is same', 'same as', 'is same as'], {'python': ' is '}))
add_lsa(LSAlias(['empty tuple'], {'python': '()'}))
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

add_lsa(LSAlias(['macro define'], {'C': '#define'}))

add_lsa(LSAlias(['macro include'], {'C': '#include'}))

add_lsa(LSAlias(['macro undo define'], {'C': '#undef'}))

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

alt_punc.create(interpreter, force = 1)
std_punc.create(interpreter)
alt_grouping.create(interpreter, force = 1)
std_grouping.create(interpreter)
alt_quotes.create(interpreter, force = 1)
std_quotes.create(interpreter)

if (__name__ == '__main__'): sr_interface.disconnect()