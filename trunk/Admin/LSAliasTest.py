import debug
import VoiceCodeRootTest
from vc_globals import *
import os, glob, shutil
import regression
import itertools
from pprint import pprint
from copy import copy
from CmdInterp import AliasMeaning, CmdInterp, LSAlias

lsa_multiply_spoken_forms = ['multiply by', 'times']
lsa_multiply_meanings  = {all_languages: " * "}

lsa_not_spoken_forms = ['not']
lsa_not_meanings  = dict(python='not', C="!", perl="!")

eindex_contents = []
                  
expected_lsa_index = {}
expected_lsa_index['C'] = [('multiply by', " * "),('not', '!'), ('times', " * ")]
# new javascript, php, only " * "::::
expected_lsa_index['javascript'] = [('multiply by', " * "), ('times', " * ")]
expected_lsa_index['php'] = [('multiply by', " * "), ('times', " * ")]

expected_lsa_index['perl'] =[('multiply by', " * "), ('not', '!'), ('times', " * ")]
expected_lsa_index['python'] = [('multiply by', " * "), ('not', 'not'), ('times', " * ")]


class LSAliasTest(VoiceCodeRootTest.VoiceCodeRootTest):
    """tests of CSCmd and CSCmdDict

    """
    def __init__(self, name):
        VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
        
    def setUp(self):
        self.interp = CmdInterp()
 
        self.interp = CmdInterp()
        self.interp.add_lsa(LSAlias(lsa_multiply_spoken_forms, lsa_multiply_meanings))
        self.interp.add_lsa(LSAlias(lsa_not_spoken_forms, lsa_not_meanings))
    


        
##########################################################
# Documentation tests
#
# These tests illustrate how to use the class.
##########################################################
        

    def test_This_is_how_you_create_a_LSAlias__instance(self):

        interp = CmdInterp()        

        interp.add_lsa(LSAlias(['spoken', 'form'],
                                    {'C':  'sss', 'python': 'ppp'}))
                                                         
        all_lsas = interp.language_specific_aliases
        languages = all_lsas.keys()
        languages.sort()
        expected = ['C', 'python']
        self.assert_equal(expected, languages, "LSAs, languages not as expected")
        self.assert_equal(expected, interp.supported_languages(),
                          "LSAs, languages not as expected through interp method")
        python_lsas = all_lsas['python']
        # extract and check only one item:
        for an_LSA in python_lsas.items():
            wordList, entry = an_LSA
            spoken_form_text = ' '.join(wordList)
            written_form_text = getattr(entry, 'written_form', '')
            expected_spoken_form = 'spoken'
            expected_written_form = 'ppp'
            self.assert_equal(expected_spoken_form, spoken_form_text,
                               "LSA spoken form is not as expected")
            self.assert_equal(expected_written_form, written_form_text,
                               "LSA written form is not as expected")
            break
        
            
##########################################################
# Unit tests lsa and general commands
#
# These tests check the internal workings of the class.
##########################################################

    def test_Test_contents_of_test_LSAliases(self):
        aliases_visible = {}
        for lang in self.interp.language_specific_aliases:
            aliases_visible[lang] = []
            for wordList, entry in self.interp.language_specific_aliases[lang].items():
                spoken_form_text = ' '.join(wordList)
                written_form_text = getattr(entry, 'written_form', '')
                aliases_visible[lang].append( (spoken_form_text, written_form_text) )
        self.assert_equal(expected_lsa_index, aliases_visible,
                          "testcase language_specific_aliases (made visible) not as expected")


    def test_Test_erroneous_definitions(self):
        
        interp = CmdInterp()
        # unknown language 'D'
        self.assertRaises(ValueError, LSAlias, (['wrong'],), {'D':  'oops'})
        self.assertRaises(DeprecationError, LSAlias, (['deprecated'],), {None:  'oops'})
        
