import debug
import VoiceCodeRootTest
from vc_globals import *
import vc_globals

import os, glob, shutil
import regression
import itertools
import pprint
from copy import copy
from CmdInterp import AliasMeaning, CmdInterp, LSAlias, LSAliasSet, CSCmdSet
from CSCmd import CSCmd
from cont_gen import *
import WhatCanISay

from actions_gen import gen_parens_pair, ActionInsertNewClause, ActionInsert
from actions_C_Cpp import c_else
from config_helpers import *


# language context instances:
for lang in all_languages:
   exec('cont%s = ContLanguage("%s")'% (lang.capitalize(), lang))
contAnyLanguage = ContLanguage(all_languages)
contCStyleLanguage = ContLanguage(c_style_languages)
contAny = ContAny()


# test data:
expected_languages = ['python'] # for the default test case
expected_all_commands_keys = ['actual_sb_s', 'actual_sb__w', 'C_sb_s', 'C_sb__w',
                              'common_sb_s', 'common_sb__w',
                              'perl_sb_s', 'perl_sb__w', 'python_sb_s', 'python_sb_w']
expected_languages.sort()


lsa_multiply_spoken_forms = ['multiply by', 'times']
lsa_multiply_meanings  = dict.fromkeys(expected_languages, ' * ')
lsa_not_spoken_forms = ['not']
lsa_not_meanings  = dict(python='not', C="!", perl="!")

csc_with_arguments_spoken_forms = ['with arguments']
csc_with_arguments_meanings = {all_languages: gen_parens_pair}

csc_with_arguments_docstring = 'giving the parens after a function call, position inside'
csc_else_spoken_forms = ['else']
csc_else_meanings ={contPython: ActionInsertNewClause('($|\n)',
                                                    code_bef = 'else:\n\t',
                                                    code_after = '',
                                                    where = -1),
                    c_style_languages: c_else}

csc_else_docstring = 'else clause'
csc_equals_spoken_forms = ['equals']
csc_equals_meanings ={ContPyInsideArguments(): ActionInsert("="),
                      ContAny(): ActionInsert(' = ')}
csc_equals_docstring = 'equal sign'

# lsa in case csc does not apply:
lsa_equals_spoken_forms = ['equals']
lsa_equals_meanings = {('python', 'C'):  ' = '}

expected_index = {'python': {\
       'else': [[{'action': 'no docstring available',
                  'doc': 'else clause',
                  'equiv': 'Language: python',
                  'scope': 'buffer',
                  'setdescription': 'description of cscs',
                  'setname': 'cscs'}]],
       'equals':   [[{'action': "Inserts '=^' in current buffer",
                      'doc': 'equal sign',
                      'equiv': 'ContPyInsideArguments: python',
                      'scope': 'immediate',
                      'setdescription': 'description of cscs',
                      'setname': 'cscs'},
                     {'action': "Inserts ' = ^' in current buffer",
                      'doc': 'equal sign',
                      'equiv': 'Any',
                      'scope': 'global',
                      'setdescription': 'description of cscs',
                      'setname': 'cscs'}],
                    {'name': 'equals lsa',
                     'new_symbol': None,
                     'setdescription': 'description of lsas',
                     'setname': 'lsas',
                     'spacing': 0,
                     'written_form': ' = '}],
       'multiply by': [{'name': 'multiply',
                        'new_symbol': None,
                        'setdescription': 'description of lsas',
                        'setname': 'lsas',
                        'spacing': 0,
                        'written_form': ' * '}],
       'not': [{'name': 'not',
                'new_symbol': None,
                'setdescription': 'description of lsas',
                'setname': 'lsas',
                'spacing': 0,
                'written_form': 'not'}],
       'times': [{'name': 'multiply',
                  'new_symbol': None,
                  'setdescription': 'description of lsas',
                  'setname': 'lsas',
                  'spacing': 0,
                  'written_form': ' * '}],
       'with arguments': [[{'action': 'Insert parens and puts cursor in between',
                            'doc': 'giving the parens after a function call, position inside',
                            'equiv': 'Language: any',
                            'scope': 'buffer',
                            'setdescription': 'description of cscs',
                            'setname': 'cscs'}]]}}

expected_boilerplate =  {\
    'percent sign':\
                   [{'name': '',
                    'new_symbol': None,
                    'setdescription': 'dictating punctuation',
                    'setname': 'standard punctuation',
                    'spacing': 0,
                    'written_form': '%'}],
   'after next percent sign': \
        [[{'action': "Moves to next occurence of \\%. (can be repeated or qualified by subsequent utterance like: 'do that again' and 'previous one').",
           'doc': 'go after next percent-sign',
           'equiv': 'Any',
           'scope': 'global',
           'setdescription': 'navigation by punctuation',
           'setname': 'standard punctuation navigation'}]],
   'after percent sign':\
        [[{'action': "Moves to next occurence of \\%. (can be repeated or qualified by subsequent utterance like: 'do that again' and 'previous one').",
           'doc': 'go after next percent-sign',
           'equiv': 'Any',
           'scope': 'global',
           'setdescription': 'navigation by punctuation',
           'setname': 'standard punctuation navigation'}]],
   'after previous percent sign': \
        [[{'action': "Moves to previous occurence of \\%. (can be repeated or qualified by subsequent utterance like: 'do that again' and 'previous one').",
           'doc': 'go after previous percent-sign',
           'equiv': 'Any',
           'scope': 'global',
           'setdescription': 'navigation by punctuation',
           'setname': 'standard punctuation navigation'}]],
   'before next percent sign':\
        [[{'action': "Moves to next occurence of \\%. Puts cursor after occurence. (can be repeated or qualified by subsequent utterance like: 'do that again' and 'previous one').",
           'doc': 'go before next percent-sign',
           'equiv': 'Any',
           'scope': 'global',
           'setdescription': 'navigation by punctuation',
           'setname': 'standard punctuation navigation'}]],
   'before percent sign': \
        [[{'action': "Moves to next occurence of \\%. Puts cursor after occurence. (can be repeated or qualified by subsequent utterance like: 'do that again' and 'previous one').",
           'doc': 'go before next percent-sign',
           'equiv': 'Any',
           'scope': 'global',
           'setdescription': 'navigation by punctuation',
           'setname': 'standard punctuation navigation'}]],
   'before previous percent sign':\
        [[{'action': "Moves to previous occurence of \\%. Puts cursor after occurence. (can be repeated or qualified by subsequent utterance like: 'do that again' and 'previous one').",
           'doc': 'go before previous percent-sign',
           'equiv': 'Any',
           'scope': 'global',
           'setdescription': 'navigation by punctuation',
           'setname': 'standard punctuation navigation'}]],
    'next percent sign': \
        [[{'action': "Moves to next occurence of \\%. (can be repeated or qualified by subsequent utterance like: 'do that again' and 'previous one').",
           'doc': 'go after next percent-sign',
           'equiv': 'Any',
           'scope': 'global',
           'setdescription': 'navigation by punctuation',
           'setname': 'standard punctuation navigation'}]],
    'previous percent sign': \
        [[{'action': "Moves to previous occurence of \\%. (can be repeated or qualified by subsequent utterance like: 'do that again' and 'previous one').",
           'doc': 'go after previous percent-sign',
           'equiv': 'Any',
           'scope': 'global',
           'setdescription': 'navigation by punctuation',
           'setname': 'standard punctuation navigation'}]]}



# files testing (required apart from generated html files:
required_non_html_files = ['vc.css', 'vcodeuser.jpg', 'waveform.gif']


class WhatCanISayTest(VoiceCodeRootTest.VoiceCodeRootTest):
   """tests of WhatCanISay functionality

   testing the actual html output files is a bit fake:
   if the folder WhatCanISayTestResults in VCODE_HOME\Data\Benchmark, or
   subfolders like "python", "C", "perl" (and possibly additional languages) do not exist,
   the test run creates them and uses them for comparison with future testing. So mainly for
   the developers of these functions.

   If you are working on WhatCanISay, it is pretty safe to remove above folders as long as you
   test the results in your webbrowser afterwards.

   The test websites are created in  VCODE_HOME\Data\Tmp\language folders(see vc_config)

   """
   
   def __init__(self, name):
      VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
      
   def setUp(self):
       self.wciSay = WhatCanISay.WhatCanISay()
       self.interp = CmdInterp()

       # lsa set:
       lsas = LSAliasSet("lsas", description="description of lsas")
       lsas.add_lsa(LSAlias(lsa_multiply_spoken_forms, lsa_multiply_meanings, name="multiply"))
       lsas.add_lsa(LSAlias(lsa_not_spoken_forms, lsa_not_meanings, name="not"))
       lsas.add_lsa(LSAlias(lsa_equals_spoken_forms, lsa_equals_meanings, name="equals lsa"))
       self.interp.add_lsa_set(lsas)

       # csc set:
       cscs = CSCmdSet('cscs', description='description of cscs')
       cscs.add_csc(CSCmd(spoken_forms=csc_with_arguments_spoken_forms,
                           meanings=csc_with_arguments_meanings,
                           docstring=csc_with_arguments_docstring))
       cscs.add_csc(CSCmd(spoken_forms=csc_else_spoken_forms,
                           meanings=csc_else_meanings,
                           docstring=csc_else_docstring))
       cscs.add_csc(CSCmd(spoken_forms=csc_equals_spoken_forms,
                           meanings=csc_equals_meanings,
                           docstring=csc_equals_docstring))
       self.interp.add_csc_set(cscs)

       # punctuation:
       punc = SinglePunctuation(name = 'standard punctuation')
       punc.add('%', ['percent-sign'])
       punc.create(self.interp)
       
       self.wciSay.load_commands_from_interpreter(self._app(), self.interp, 'python')

      
##########################################################
# Documentation tests
#
# These tests illustrate how to use the class.
##########################################################
      

   def test_This_is_how_you_create_a_WhatCanISay_instance(self):
       wciSay = WhatCanISay.WhatCanISay()
       interp = CmdInterp()
       # load one lsa and one csc:
       interp.add_csc(CSCmd(["equals"], meanings={contAny: ActionInsert("====")}, name="equals csc"))
       interp.add_lsa(LSAlias(["plus"], meanings={all_languages: " + "}, name="plus sign"))
       wciSay.load_commands_from_interpreter(self._app(), interp, 'C')
       

   def test_This_is_how_you_create_the_commands_for_showing(self):
       wciSay = WhatCanISay.WhatCanISay()
       interp = CmdInterp()
       # load one lsa and one csc:
       interp.add_csc(CSCmd(["equals"], meanings={contAny: ActionInsert("====")}, name="equals csc"))
       interp.add_lsa(LSAlias(["plus"], meanings={all_languages: " + "}, name="plus sign"))
       wciSay.load_commands_from_interpreter(self._app(), interp, 'C')
       wciSay.create_cmds()
##       self.assert_equal(expected_csc, wciSay.csc_commands, "csc_commands should be empty lists, nothing loaded yet")



   def test_This_is_how_to_create_the_pages(self):
       """in order to automatically show the pages
 
       hard to test, except by eye...
       note: possibly disable when doing all tests automatically
       """
       return
       self.wciSay.show_cmds(self.interp, 'python')
       
##########################################################
# Unit tests lsa and general commands
#
# These tests check the internal workings of the class.
##########################################################

   def test_the_index_of_WhatCanISay_default(self):

       # all_lang = None, curr_context = None, curr_lang = 'python' in this test case
       self.assert_equal(expected_index, self.wciSay.index, "test index of WhatCanISay (default) is not as expected")

       self.assert_equal({}, self.wciSay.boilerplate, \
                         "test boilerplate of WhatCanISay (default) is not as expected")

   def test_the_index_of_WhatCanISay_all_lang(self):

       # all_lang = 1, curr_context = None, curr_lang = 'python' in this test case
       self.wciSay.load_commands_from_interpreter(self._app(), self.interp, 'python', all_lang=1)
       expected_index_keys_all_lang = list(all_languages)
       actual_keys = self.wciSay.index.keys()
       actual_keys.sort()
       self.assert_equal(expected_index_keys_all_lang, actual_keys, "test index of WhatCanISay .(all_lang) has not expected keys")
       self.assert_equal(expected_boilerplate, self.wciSay.boilerplate, \
                         "test boilerplate of WhatCanISay (all_lang) is not as expected")

   def test_the_index_of_WhatCanISay_curr_context(self):

       self._open_empty_test_file('temp.py')
       self.wciSay.load_commands_from_interpreter(self._app(), self.interp, 'python', curr_context=1)
       pprint.pprint(self.wciSay.index['python']['equals'])
       

   def test_the_index_of_simple_csc__and_an_lsa_definition(self):
       wciSay = WhatCanISay.WhatCanISay()
       interp = CmdInterp()
       # do one csc and one lsa:
       interp.add_csc(CSCmd(["equals"], meanings={contAny: ActionInsert("====")}, name="equals csc"))
       interp.add_lsa(LSAlias(["plus"], meanings={all_languages: " + "}, name="plus sign"))
       wciSay.load_commands_from_interpreter(self._app(), interp, 'C')
       expected = {'C':\
                  {'equals': [[{'action': "Inserts '====^' in current buffer",
                                'doc': None,
                                'equiv': 'Any',
                                'scope': 'global',
                                'setdescription': 'no description',
                                'setname': 'cscs'}]],
                  'plus': [{'description': 'no description',
                            'name': 'plus sign',
                            'new_symbol': None,
                            'setname': 'lsas',
                            'spacing': 0,
                            'written_form': ' + '}]}}
       self.assert_equal(expected, wciSay.index, "index of one CSC and one LSA command is not as expected")


   def test_extract_common_commands(self):
       """extract items that are common within the programming languages

       tested on numbers here, in practice the items are tuples or instances...

       """
       # no common at start:
       D = dict(python=[1,3,4], C=[1,3,5], letters=['a'], numbers=[1,3,4,5])
       expected = dict(common=[1, 3], python=[4], C=[5], letters=['a'], numbers=[1, 3, 4, 5])   
       self.wciSay.extract_common_commands(D)
       self.assert_equal(expected, D,
                         "extract_common_commands result unexpected (no common at start.")  

       # common at start too:
       D = dict(common=[1,6,7], python=[1,3,4], C=[1,3,5], numbers=[1,3,4,5])
       # note no sorting of keys here, can have strange test result:
       expected = dict(common=[1, 6, 7, 3], python=[4], C=[5], numbers=[1, 3, 4, 5])
       self.wciSay.extract_common_commands(D)
       self.assert_equal(expected, D,
                         "extract_common_commands result unexpected, common at start.")  


       # nothing common:
       D = dict(python=[1,4], C=[5], numbers=[1,3,4,5])
       # note no sorting of keys here, can have strange test result:
       expected = dict(common=[], python=[1,4], C=[5], numbers=[1, 3, 4, 5])
       self.wciSay.extract_common_commands(D)
       self.assert_equal(expected, D,
                         "extract_common_commands result unexpected, no common commands")  

 
   def test_lsa_commands(self):
       """testing elaborated lsa commands with test data multiply and not"""
       return
       self.wciSay.create_cmds(self.interp, 'python')  
       actual_languages = self.wciSay.languages
       self.failIf(None in actual_languages, "None should not be in supported languages")
       actual_languages.sort()
       self.assert_equal(expected_languages, actual_languages,
                         "List of supported languages was wrong.")  
       
       self.assert_equal(expected_lsa_commands,
                         self.wciSay.lsa_commands, 
                         "lsa_commands with multiply and not are NOT as expected.")

   def test_csc_commands(self):
       return
       self.wciSay.create_cmds(self.interp, 'python')  
       actual_languages = self.wciSay.languages
       self.failIf(None in actual_languages, "None should not be in supported languages")
       actual_languages.sort()
       self.assert_equal(expected_languages, actual_languages,
                         "List of supported languages was wrong.")  
       
       self.assert_equal(expected_csc_commands,
                         self.wciSay.csc_commands, 
                         'csc_commands with with "with arguments" and "equals" and "else" is NOT as expected')
 
   def test_control_standard_files(self):
       """Controls the existence of some standard files"""
       return
       folder= self.wciSay.html_folder
       self.assert_(os.path.isdir(folder),
            'WhatCanISay does not have a valid folder %s'%folder)
       for f in required_non_html_files:
           F = os.path.join(folder, f)
           self.assert_(os.path.isfile(F),
               'file "%s" is missing (and is required for the WhatCanISay website (%s)).'% (f, F))

       
   def test_resulting_websites(self):
       """check if all the files are equal"""
       return
       for lang in self.wciSay.languages:
           if lang == None:
               continue
           html_folder= self.wciSay.html_folder

           html_files = glob.glob(os.path.join(html_folder, "*.html"))
           for f in html_files:
               os.remove(f)
           self.wciSay.create_cmds(self.interp, lang)
           index_page = self.wciSay.create_html_pages()

           test_home = vc_globals.wcisay_test_folder
           self.assert_(os.path.isdir(test_home), "No valid folder for testing the resulting websites")
           test_folder = os.path.join(test_home, lang)
           if os.path.isdir(test_folder):
               print 'using test folder: %s'% test_folder
           else:
               print 'no test folder yet for language %s, assume correct results, copy to %s'% \
                     (lang, test_folder)
               self.copy_html_files(html_folder, test_folder)
               continue
           
           Tmp = vc_globals.tmp
           if not os.path.isdir(Tmp):
               os.path.makedirs(Tmp)
           tmp_folder = os.path.join(Tmp, lang)
           if os.path.isdir(tmp_folder):
               shutil.rmtree(tmp_folder)
           self.copy_html_files(html_folder, tmp_folder)
       
           self.assert_equal_html_files(test_folder, tmp_folder,
                                        'WhatCanISay website of language %s'% lang)

   def test_context_applies_for_lang(self):
        self.assert_(self.wciSay.context_applies_for_lang('python', contPython), 
                     "ContPy should applie for langage python")
        self.failIf(self.wciSay.context_applies_for_lang('C', contPython), 
                     "ContPy should not apply for langage C")

        self.assert_(self.wciSay.context_applies_for_lang('C', contC), 
                     "ContC should apply for langage C")                     
        self.failIf(self.wciSay.context_applies_for_lang('python', contC), 
                     "ContC should not apply for langage python")
                     
        self.assert_(self.wciSay.context_applies_for_lang('python', ContAny()), 
                     "ContAny should apply for langage python")
        self.assert_(self.wciSay.context_applies_for_lang('C', ContAny()), 
                     "ContAny should apply for langage C")         
        

###############################################################
# Assertions and utility function testing:
#
###############################################################
   def test_bring_to_top(self):
       """Testing the simple function bring_to_top

       Bringing a list item to the top (position zero)"""
       List = [1, 2, 3, 4]
       self.wciSay.bring_to_top(List, 2)
       expected_lsa = [2, 1, 3, 4]
       self.assert_equal(expected_lsa, List, "Bring_to_top function does not change correctly in place")
       self.wciSay.bring_to_top(List, 5)
       self.assert_equal(expected_lsa, List, "Bring_to_top function should not change when called with non existing item")

   def test_sort_csc_values_by_scope(self):
       """Testing the function that sorts csc entries by scope

       """
       return
       list_to_sort_by_scope = [('Any', 'global', "... in current buffer"),
                    ('ContPyInsideArguments', 'immediate', "Inserts ")]
       wrong_list_to_sort_by_scope = [('Any', 'globaly', "wrong word in scope..."),
                    ('ContPyInsideArguments', 'immediate', "Inserts ")]
       
       
       sorted = self.wciSay.sort_csc_values_by_scope(list_to_sort_by_scope)
       expected = copy(list_to_sort_by_scope)
       expected.reverse()
       
       self.assert_equal(expected, sorted, "csc_sorted list by scope not as expected")

       sorted = self.wciSay.sort_csc_values_by_scope(wrong_list_to_sort_by_scope)
       expected = wrong_list_to_sort_by_scope
       
       self.assert_equal(expected, sorted, "csc_sorted list, when error should return the original list")




   def assert_equal_html_files(self, expected_folder, actual_folder, mess):
       """test the equality of the html files"""
       expected_list = glob.glob(os.path.join(expected_folder, '*.html'))
       actual_list = glob.glob(os.path.join(actual_folder, '*.html'))
       expected_list.sort()
       actual_list.sort()
       self.assert_equal(len(expected_list), len(actual_list), mess + '\n' + \
                      "number of expected html files not equal to actual\nExpected: %s\nActual: %s"%
                         (expected_list, actual_list))
       for e, a in zip(expected_list, actual_list):
           self.assert_equal_files(e, a, "files are not equal:\n%s and\n%s"%
                                (e, a))

  
   def assert_equal_files(self, expected_file, actual_file, mess):
       for i, k, l in itertools.izip(itertools.count(1),
                                     open(expected_file),
                                     open(actual_file)):
         
           if k.find('class="copyright"') >= 0 and \
              l.find('class="copyright"') >= 0:
               continue  # dates can differ, is expected and accepted
           self.assert_equal(k,l,mess + '\nthe two files------------\n%s\nand\n %s should have been equal\nThey differ in line %s'%
                              (expected_file, actual_file, i))


   def copy_html_files(self, src_dir, dest_dir):
       """copy only html files from src to dest"""
       if os.path.isdir(dest_dir):
           shutil.rmtree(dest_dir)
       os.makedirs(dest_dir)
       self.assert_(os.path.isdir(dest_dir), 'could not make empty folder %s'% dest_dir)

       html_files = glob.glob(src_dir + os.sep + '*.html')
       for src in html_files:
           dest = src.replace(src_dir, dest_dir)
           shutil.copyfile(src, dest)
           
   def test_WhatCanISay_with_all_lang_and_curr_context_should_fail(self):
       self.assertRaises(ValueError, self.wciSay.load_commands_from_interpreter,
                         self._app(), self.interp, 'python', 1, 1)


       
        

def _test():
    reload(WhatCanISay)
    wciSay = WhatCanISay.WhatCanISay()
    wciSay.curr_lang = 'python'
    wciSay.all_lang = None
    wciSay.curr_context = None
    wciSay.index = expected_index
    wciSay.create_cmds()

if __name__ == "__main__":
    _test()
