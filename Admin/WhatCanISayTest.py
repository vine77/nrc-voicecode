import debug
import VoiceCodeRootTest
import vc_globals
import os, glob, shutil
import regression
import itertools

from CmdInterp import AliasMeaning, CmdInterp, LSAlias
from WhatCanISay import WhatCanISay

# test data:
expected_languages = ['C', 'perl', 'python']
expected_all_commands_keys = ['actual_sb_s', 'actual_sb__w', 'C_sb_s', 'C_sb__w',
                              'common_sb_s', 'common_sb__w',
                              'perl_sb_s', 'perl_sb__w', 'python_sb_s', 'python_sb_w']
expected_languages.sort()
lsa_multiply_list = ['multiply by', 'multiplied by', 'times']
lsa_multiply_dict  = dict.fromkeys(expected_languages, ' * ')
lsa_not_list = ['not']
lsa_not_dict  = dict(python='not', C="!", perl="!")


# expected index contents of the 3 languages: values of self.index (raw LSA commands)
# first one is equal over the 2 languages
# second one differs with python:
index_contents =  [(['multiply', 'by'], AliasMeaning(" * ")),
                   (['multiplied', 'by'], AliasMeaning(" * "))]
                  
expected_index = {}
expected_index[None] = []
expected_index['C'] = index_contents + [(['not'], AliasMeaning('!')),
                                        (['times'], AliasMeaning(" * "))]
expected_index['perl'] = index_contents + [(['not'], AliasMeaning('!')),
                                           (['times'], AliasMeaning(" * "))]
expected_index['python'] = index_contents + [(['not'], AliasMeaning('not')),
                                             (['times'], AliasMeaning(" * "))]
                            

expected_lsa_commands = dict(C_sb__w=[('not', '!')],
                             actual_sb__w= [('multiplied by', ' * '),
                                          ('multiply by', ' * '),
                                          ('times', ' * '),
                                          ('not', 'not')],
                             C_sb_s=[('not', '!')],
                             actual_sb_s=[('multiplied by', ' * '),
                                         ('multiply by', ' * '),
                                         ('not', 'not'),
                                         ('times', ' * ')],
                             python_sb_s=[('not', 'not')],
                             perl_sb_s= [('not', '!')],
                             perl_sb__w=[('not', '!')],
                             common_sb_s=[('multiplied by', ' * '),
                                         ('multiply by',' * '),
                                         ('times', ' * ')],
                             python_sb__w=[('not', 'not')],
                             common_sb__w=[('multiplied by', ' * '),
                                         ('multiply by', ' * '),
                                         ('times', ' * ')])




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

   The test websites are created in  VCODE_HOME\Data\Tmp\language folders.

   """
   
   def __init__(self, name):
      VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
      
   def setUp(self):
       self.wciSay = WhatCanISay()
       self.interp = CmdInterp()
       self.interp.add_lsa(LSAlias(lsa_multiply_list, lsa_multiply_dict))
       self.interp.add_lsa(LSAlias(lsa_not_list, lsa_not_dict))
       self.wciSay.load_commands_from_interpreter(self.interp)

      
##########################################################
# Documentation tests
#
# These tests illustrate how to use the class.
##########################################################
      

   def test_This_is_how_you_create_a_WhatCanISay_instance(self):
       """after this call the lsa list should be created (self.index)"""
       wciSay = WhatCanISay()
       interp = CmdInterp()
       wciSay.load_commands_from_interpreter(interp)
       Expected = {None: []}
       self.assert_equal(Expected, wciSay.index, 'lsa commands index should be equal (and nearly empty, no commands loaded)')

   def test_This_is_how_you_create_the_lsa_commands_for_showing(self):
       """lsa commands elaborated from self.index, should be empty now"""
       wciSay = WhatCanISay()
       interp = CmdInterp()
       wciSay.create_cmds(interp, 'C')
       Expected =  {'actual_sb__w': [], 'actual_sb_s': []}
       self.assert_equal(Expected, wciSay.lsa_commands, "lsa_commands should be empty lists, nothing loaded yet")

   def test_This_is_how_to_create_the_pages(self):
       """in order to automatically show the pages
 
       hard to test, except by eye...
       note: disable when doing all tests automatically
       """
       self.wciSay.show_cmds(self.interp, 'python')
       
##########################################################
# Unit tests
#
# These tests check the internal workings of the class.
##########################################################

   def test_bring_to_top(self):
       """Testing the simple function bring_to_top

       Bringing a list item to the top (position zero)"""
       List = [1, 2, 3, 4]
       self.wciSay.bring_to_top(List, 2)
       Expected = [2, 1, 3, 4]
       self.assert_equal(Expected, List, "Bring_to_top function does not change correctly in place")
       self.wciSay.bring_to_top(List, 5)
       self.assert_equal(Expected, List, "Bring_to_top function should not change when called with non existing item")

   def test_extract_common_commands(self):
       """extract items that are common within the programming languages

       """
       # no common at start:
       D = dict(python=[1,3,4], C=[1,3,5], letters=['a'], numbers=[1,3,4,5])
       Expected = dict(common=[1, 3], python=[4], C=[5], letters=['a'], numbers=[1, 3, 4, 5])   
       self.wciSay.extract_common_commands(D)
       self.assert_equal(Expected, D,
                         "extract_common_commands result unexpected (no common at start.")  

       # common at start too:
       D = dict(common=[1,6,7], python=[1,3,4], C=[1,3,5], numbers=[1,3,4,5])
       # note no sorting of keys here, can have strange test result:
       Expected = dict(common=[1, 6, 7, 3], python=[4], C=[5], numbers=[1, 3, 4, 5])
       self.wciSay.extract_common_commands(D)
       self.assert_equal(Expected, D,
                         "extract_common_commands result unexpected, common at start.")  


       # nothing common:
       D = dict(python=[1,4], C=[5], numbers=[1,3,4,5])
       # note no sorting of keys here, can have strange test result:
       Expected = dict(common=[], python=[1,4], C=[5], numbers=[1, 3, 4, 5])
       self.wciSay.extract_common_commands(D)
       self.assert_equal(Expected, D,
                         "extract_common_commands result unexpected, no common commands")  




   
   def test_index_dict(self):
       """testing self.index (lsa commands) with test data multiply and not"""
       self.wciSay.create_cmds(self.interp, 'python')  
       actual_languages = self.wciSay.languages
       self.assert_(None in actual_languages, "None is not in supported languages")
       actual_languages.remove(None)
       actual_languages.sort()
       self.assert_equal(expected_languages, actual_languages,
                         "List of supported languages was wrong.")  
       
       self.assert_equal(expected_index,
                         self.wciSay.index, 
                         "Command index (lsa) with multiply and not are NOT as expected.")
 
   def test_lsa_commands(self):
       """testing elaborated lsa commands with test data multiply and not"""
       self.wciSay.create_cmds(self.interp, 'python')  
       actual_languages = self.wciSay.languages
       self.assert_(None in actual_languages, "None is not in supported languages")
       actual_languages.remove(None)
       actual_languages.sort()
       self.assert_equal(expected_languages, actual_languages,
                         "List of supported languages was wrong.")  
       
       self.assert_equal(expected_lsa_commands,
                         self.wciSay.lsa_commands, 
                         "lsa_commands with multiply and not are NOT as expected.")
 
   def test_control_standard_files(self):
       """Controls the existence of some standard files"""
       folder= self.wciSay.html_folder
       self.assert_(os.path.isdir(folder),
            'WhatCanISay does not have a valid folder %s'%folder)
       for f in required_non_html_files:
           F = os.path.join(folder, f)
           self.assert_(os.path.isfile(F),
               'file "%s" is missing (and is required for the WhatCanISay website (%s)).'% (f, F))

       
   def test_resulting_websites(self):
       """check if all the files are equal"""
       for lang in self.wciSay.languages:
           if lang == None:
               continue
           html_folder= self.wciSay.html_folder

           html_files = glob.glob(os.path.join(html_folder, "*.html"))
           for f in html_files:
               os.remove(f)
           self.wciSay.create_cmds(self.interp, lang)
           index_page = self.wciSay.create_html_pages()

           home = os.environ['VCODE_HOME']
           test_folder = os.path.join(home, 'Data','Benchmark',
                                      'WhatCanISayTestResults', lang)
           if os.path.isdir(test_folder):
               print 'using test folder: %s'% test_folder
           else:
               print 'no test folder yet for language %s, assume correct results, copy to %s'% \
                     (lang, test_folder)
               self.copy_html_files(html_folder, test_folder)
               continue
           
           Tmp_folder = os.path.join(home,'Data', 'Tmp')
           if not os.path.isdir(Tmp_folder):
               os.path.makedirs(Tmp_folder)
           tmp_folder = os.path.join(Tmp_folder, lang)
           if os.path.isdir(tmp_folder):
               shutil.rmtree(tmp_folder)
           self.copy_html_files(html_folder, tmp_folder)
       
           self.assert_equal_html_files(test_folder, tmp_folder,
                                        'WhatCanISay website of language %s'% lang)

###############################################################
# Assertions.
###############################################################
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
           
