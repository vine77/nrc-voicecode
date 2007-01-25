import debug
import VoiceCodeRootTest
from vc_globals import *
import os, glob, shutil
import regression
import itertools
from pprint import pprint
from copy import copy
from CmdInterp import AliasMeaning, CmdInterp, LSAlias
from CSCmd import CSCmd
from cont_gen import *
from actions_gen import *
from actions_C_Cpp import *


# language context instances:
for lang in all_languages:
    exec('cont%s = ContLanguage("%s")'% (lang.capitalize(), lang))
contAnyLanguage = ContLanguage(all_languages)
contCStyleLanguage = ContLanguage(c_style_languages)

# test data:
expected_languages = ['C', 'perl', 'python']

csc_with_arguments_spoken_forms = ['with arguments', 'function of']
csc_with_arguments_meanings = {all_languages: gen_parens_pair}

csc_with_arguments_docstring = 'giving the parens after a function call, position inside'
csc_else_spoken_forms = ['else']
csc_else_meanings ={contPython: ActionInsertNewClause('($|\n)',
                                                                     code_bef = 'else:\n\t',
                                                                     code_after = '',
                                                                     where = -1),
                          c_style_languages: c_else}
csc_else_docstring = 'else clause'
csc_equals_spoken_forms = ['equals', 'assign value']

csc_equals_meanings ={all_languages: ActionInsert("="),
                             ContAny(): ActionInsert(' = ')}
csc_equals_docstring = 'equal sign'

expected_csc_index =  {\
     'python':\
         {'function of': [(contPython, gen_parens_pair)],
          'with arguments': [(contPython, gen_parens_pair)],
          'assign value': [(ContAny(), ActionInsert(" = ")),
                                 (ContPyInsideArguments(), ActionInsert("="))],
          'equals': [(ContAny(), ActionInsert(" = ")),
                         (ContPyInsideArguments(), ActionInsert("="))],
          'else': [(contPython, ActionInsertNewClause('($|\n)',
                                                                     code_bef = 'else:\n\t',
                                                                     code_after = ''))]},
     'C':\
         {'function of': [(contC, gen_parens_pair)],
          'with arguments':[(contC, gen_parens_pair)],
          'assign value': [(ContAny(),  ActionInsert(" = "))],
          'equals': [(ContAny(), ActionInsert(" = "))],
          'else': [(c_style_languages, c_else)]},
    'perl':\
         {'function of': [(contPerl, gen_parens_pair)],      
          'with arguments': [(contPerl, gen_parens_pair)],
          'assign value': [(ContAny(), ActionInsert(" = "))],
          'equals': [(ContAny(), ActionInsert(" = "))],
          'else': [(c_style_languages, c_else)]}}



class CSCmdTest(VoiceCodeRootTest.VoiceCodeRootTest):
    """tests of CSCmd and CSCmdDict

    """
    
    def __init__(self, name):
        VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
        
    def setUp(self):
         self.interp = CmdInterp()
         self.interp.add_csc(CSCmd(spoken_forms=csc_with_arguments_spoken_forms,
                                    meanings=csc_with_arguments_meanings,
                                    docstring=csc_with_arguments_docstring))
         self.interp.add_csc(CSCmd(spoken_forms=csc_else_spoken_forms,
                                    meanings=csc_else_meanings,
                                    docstring=csc_else_docstring))
         self.interp.add_csc(CSCmd(spoken_forms=csc_equals_spoken_forms,
                                    meanings=csc_equals_meanings,
                                    docstring=csc_equals_docstring))


        
##########################################################
# Documentation tests
#
# These tests illustrate how to use the class.
##########################################################
        

    def test_This_is_how_you_create_a_CSCmd_instance(self):
         command1 = CSCmd(spoken_forms=['hello'],
                         meanings = {'python': ActionInsert('hello python'),
                                         'C': ActionInsert('hello C')})
         command2 = CSCmd(spoken_forms=['hello'],
                         meanings = {contPython: ActionInsert('hello python'),
                                         contC: ActionInsert('hello C')})
         self.assert_equal(command2, command1, \
                                 "Csc commands should have been the same with different ways to define")


    def test_This_is_how_you_collect_all_the_CSC_commands(self):
         interp = CmdInterp()
         contAny = ContAny()
         actionHello = ActionInsert("hello")
         contBlankLine = ContBlankLine()
         actionThere = ActionInsert("there")
         actionOtherwise = ActionInsert("there otherwise")
         interp.add_csc(CSCmd(spoken_forms=['hello'],
                                     meanings={contAny: actionHello},
                                     docstring="hello"))
         
         interp.add_csc(CSCmd(spoken_forms=['there'],
                                     meanings={contBlankLine: actionThere,
                                               contAny: actionOtherwise},
                                     docstring="there on blankline or otherwise"))
         
         wTrie = interp.commands
         for spoken, cscmd_list in wTrie.items():
             
             if spoken == ['hello']:
                 cscmd_list_expected = ["global||Any||Inserts 'hello^' in current buffer"]
             elif spoken == ['there']:
                 cscmd_list_expected = ["immediate||BlankLine: any||Inserts 'there^' in current buffer",
                                        "global||Any||Inserts 'there otherwise^' in current buffer"]
             
             visible_list = cscmd_list.get_visible_list()
             self.assert_equal(cscmd_list_expected, visible_list,
                               'wTrie CSCmdList of meanings with spoken form "%s" is not as expected'% repr(spoken))
             

##########################################################
# Unit tests lsa and general commands
#
# These tests check the internal workings of the class.
##########################################################

    def test_Test_conflicing_context_instances(self):
          pass
