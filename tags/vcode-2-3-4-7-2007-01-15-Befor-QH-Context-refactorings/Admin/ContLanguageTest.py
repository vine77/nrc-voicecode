from debug import trace
import cont_gen
import VoiceCodeRootTest
from vc_globals import *
from cont_gen import *


class ContLanguageTest(VoiceCodeRootTest.VoiceCodeRootTest):
    """Test the different possibilities to test for ContLanguage instance

    and its subclasses.

    """   
    def __init__(self, name):
        VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
      
    def setUp(self):
        self._init_simulator_regression()
        self.context = ContLanguage()
        self.context_py = ContPy()
        self.context_all = ContLanguage(all_languages)
        self.context_c = ContC()
        self.context_c_like = ContLanguage(c_style_languages)
        
##########################################################
# Documentation tests
#
# These tests illustrate how to use the class.
##########################################################
      
    def test_This_is_how_you_create_a_ContLanguage(self):
        # call with 1 language as string:
        context = cont_gen.ContLanguage(language="python")
        # call with language as tuple of languages:
        context = ContLanguage(all_languages)
        
    def test_ContLanguage_applies_for_python(self):

        context = ContLanguage(language='python')
        self._open_empty_test_file('temp.py')
        self.assert_(context.applies(self._app()), 
                     "Context language='python' should have applied because in python file")

        self._open_empty_test_file('temp.c')
        self.failIf(context.applies(self._app()), 
                     "Context should NOT have applied because the file was in the wrong language.")

        # equivalent to above examples:
        context_py = ContPy()
        self._open_empty_test_file('temp.py')
        self.assert_(context_py.applies(self._app()), 
                     "Context language='python' should have applied because in python file")

        self._open_empty_test_file('temp.c')
        self.failIf(context_py.applies(self._app()), 
                     "Context should NOT have applied because the file was in the wrong language.")

    def test_ContLanguage_equivalence_keys(self):
        for lang in all_languages:
            context = ContLanguage(lang)
            expected = "Language: %s"% lang 
            self.assert_equal(expected, context.equivalence_key(),
                              "single language ContLanguage context does not produce expected equivalence key")

        context = ContCStyleLanguage()
        expected = "Language: %s"% '|'.join(c_style_languages)
        self.assert_equal(expected, context.equivalence_key(),
                              "ContCStyleLanguage context does not produce expected equivalence key")

        context = ContAnyLanguage()
        expected = "Language: any"
        self.assert_equal(expected, context.equivalence_key(),
                              "ContAnyLanguage context does not produce expected equivalence key")

        context = ContPy()
        expected = "Language: %s"% 'python'
        self.assert_equal(expected, context.equivalence_key(),
                              "ContPy context does not produce expected equivalence key")

        context = ContC()
        expected = "Language: %s"% 'C'
        self.assert_equal(expected, context.equivalence_key(),
                              "ContC context does not produce expected equivalence key")

        context = ContPerl()
        expected = "Language: %s"% 'perl'
        self.assert_equal(expected, context.equivalence_key(),
                              "ContPerl context does not produce expected equivalence key")

##########################################################
# Unit tests
#
# These tests check the internal workings of the class.
##########################################################
    def test_ContLanguage_try_all_possible_languages(self):

        # try all known languages:
        self._open_empty_test_file('temp.py')
        for lang in all_languages:
            context = ContLanguage(language=lang)
            if lang == 'python':
                self.assert_(context.applies(self._app()), 
                     "Context language='python' should have applied because in python file")
            else:
                self.failIf(context.applies(self._app()), 
                     "Context language='%s' should have failed because in python file"% lang)

        # try all_languages in once:
        self._open_empty_test_file('temp.c')
        context = ContLanguage(language=all_languages)
        self.assert_(context.applies(self._app()), 
                      'Context language=all_languages should have applied because in "C" file')

        # trying set of languages:
        context = ContLanguage(c_style_languages)
        self._open_empty_test_file('temp.c')
        self.assert_(context.applies(self._app()), 
                     'Context language="%s" should have applied because in "C" file'% \
                     repr(c_style_languages))
        self._open_empty_test_file('temp.py')
        self.failIf(context.applies(self._app()), 
                     'Context language="%s" should have failed in python file'
                     ' because it is not a c_style_language'% repr(c_style_languages))
        
    def test_ContLanguage_subclasses(self):

        # ContPy:
        context = ContPy()
        self._open_empty_test_file('temp.py')
        self.assert_(context.applies(self._app()), 
                     "ContPy should have applied because in python file")
        self._open_empty_test_file('temp.c')
        self.failIf(context.applies(self._app()), 
                     'ContPy should have failed, because in "C" file')

        # ContC:
        context = ContC()
        self._open_empty_test_file('temp.c')
        self.assert_(context.applies(self._app()), 
                     "ContC should have applied because in C file")
        self._open_empty_test_file('temp.py')
        self.failIf(context.applies(self._app()), 
                     'ContC should have failed, because in "python" file')

        # ContPerl:
        context = ContPerl()
        self._open_empty_test_file('temp.c')
        self.failIf(context.applies(self._app()), 
                     'ContPerl should have failed, because in "C" file')

        # ContCStyleLanguage
        context = ContCStyleLanguage()
        self._open_empty_test_file('temp.py')
        self.failIf(context.applies(self._app()), 
                     'ContCStyleLanguage should have failed, because in "python" file')
        self._open_empty_test_file('temp.c')
        self.assert_(context.applies(self._app()), 
                      "ContCStyleLanguage should have applied because in C file")

        # ContAnyLanguage
        context = ContAnyLanguage()
        self._open_empty_test_file('temp.py')
        self.assert_(context.applies(self._app()), 
                      "ContAnyLanguage should have applied because in python file")
        self._open_empty_test_file('temp.c')
        self.assert_(context.applies(self._app()), 
                      "ContAnyLanguage should have applied because in C file")

        

    def test_ContLanguage_should_fail_with_invalid_input(self):

        self.assertRaises(ValueError, ContLanguage, "unknown")
        self.assertRaises(TypeError, ContLanguage, ['C', 'perl'])
                                                 
    
###############################################################
# Assertions.
# 
# Use these methods to check the state of the class.
###############################################################
