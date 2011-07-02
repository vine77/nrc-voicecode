import debug
import cont_gen
import VoiceCodeRootTest
from vc_globals import all_languages, c_style_languages

class ContBeforeArgumentsTest(VoiceCodeRootTest.VoiceCodeRootTest):
    """Test the BeforeArguments Context in several languages

    This context should apply if The cursor is just before the arguments of a function definition or a function call.
    So before the parens.

    def HERE(arg):
        pass

    or 

    x = HERE()

    But not HERE or f(HERE)

    This context can be used for integrating add arguments and with arguments.
    QH march 2007, augmented to all languages august 2007

    """   
    def __init__(self, name):
        VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
      
    def setUp(self):
        self._init_simulator_regression()
        self.python_context = cont_gen.ContBeforeArguments('python')
        self.c_context = cont_gen.ContBeforeArguments('C')
        self.javascript_context = cont_gen.ContBeforeArguments('javascript')
        self.perl_context = cont_gen.ContBeforeArguments('perl')
        self.java_context = cont_gen.ContBeforeArguments('java')
        self.php_context = cont_gen.ContBeforeArguments('php')
        self.all_context = cont_gen.ContBeforeArguments(all_languages)
        self.c_style_context = cont_gen.ContBeforeArguments(c_style_languages)

##########################################################
# Documentation tests
#
# These tests illustrate how to use the class.
##########################################################
      
    def test_This_is_how_you_create_a_ContPyBeforeArguments(self):
        context = cont_gen.ContBeforeArguments(all_languages)
        self.assert_(isinstance(context, cont_gen.ContBeforeArguments))
        
    def test_ContBeforeArguments_applies_if_cursor_is_just_before_open_paren(self):
        self._open_empty_test_file('temp.py')
        self._insert_in_active_buffer("outside = here()")
        self._say("select here")
        self._assert_active_buffer_content_is('outside = here<CURSOR>()')
        self.assert_(self.python_context.applies(self._app()), 
                     "python context should have applied because cursor is in front of open paren")
        self.assert_(self.all_context.applies(self._app()), 
                     "Context should have applied because cursor is in front of open paren")

        self._open_empty_test_file('temp.c')
        self._insert_in_active_buffer("outside = here()")
        self._say("select here")
        self._assert_active_buffer_content_is('outside = here<CURSOR>()')
        self.assert_(self.c_context.applies(self._app()), 
                     "c_context should have applied because cursor is in front of open paren")
        self.assert_(self.all_context.applies(self._app()), 
                     "Context should have applied because cursor is in front of open paren")
        self.assert_(self.c_style_context.applies(self._app()), 
                     "c_style context should have applied because cursor is in front of open paren")


        self._open_empty_test_file('temp.js')
        self._insert_in_active_buffer("outside = here()")
        self._say("select here")
        self._assert_active_buffer_content_is('outside = here<CURSOR>()')
        self.assert_(self.javascript_context.applies(self._app()), 
                     "javascript_context should have applied because cursor is in front of open paren")
        self.assert_(self.all_context.applies(self._app()), 
                     "Context should have applied because cursor is in front of open paren")
        self.assert_(self.c_style_context.applies(self._app()), 
                     "c_style context should have applied because cursor is in front of open paren")
        self.failIf(self.python_context.applies(self._app()), 
                     "python_context should NOT apply because in javascript buffer")
        self.failIf(self.c_context.applies(self._app()), 
                     "c_context should NOT apply because in javascript buffer")

        self._open_empty_test_file('temp.java')
        self._insert_in_active_buffer("outside = here()")
        self._say("select here")
        self._assert_active_buffer_content_is('outside = here<CURSOR>()')
        self.assert_(self.java_context.applies(self._app()), 
                     "java_context should have applied because cursor is in front of open paren")
        self.assert_(self.all_context.applies(self._app()), 
                     "Context should have applied because cursor is in front of open paren")
        self.assert_(self.c_style_context.applies(self._app()), 
                     "c_style context should have applied because cursor is in front of open paren")

        self._open_empty_test_file('temp.php')
        self._insert_in_active_buffer("outside = here()")
        self._say("select here")
        self._assert_active_buffer_content_is('outside = here<CURSOR>()')
        self.assert_(self.php_context.applies(self._app()), 
                     "php_context should have applied because cursor is in front of open paren")
        self.assert_(self.all_context.applies(self._app()), 
                     "Context should have applied because cursor is in front of open paren")
        self.assert_(self.c_style_context.applies(self._app()), 
                     "c_style context should have applied because cursor is in front of open paren")

    def test_ContBeforeArguments_applies_if_cursor_is_just_before_space_open_paren(self):
        self._open_empty_test_file('temp.py')
        self._insert_in_active_buffer("outside = here ()")
        # Although rare also a space between the function name and the "(" is recognised.
        # testing only for python now
        self._say("before here")
        
        self._assert_active_buffer_content_is('outside = <CURSOR>here ()')
        self.assert_(self.python_context.applies(self._app()), 
                     "python context should have applied because cursor is in front of space open paren")

    
    def test_ContPyBeforeArguments_fails_if_cursor_is_not_just_before_open_paren(self):
        self._open_empty_test_file('temp.py')
        self._insert_in_active_buffer("outside = f()")
        self._say("select outside")
        self._assert_active_buffer_content_is('outside<CURSOR> = f()')
        self.failIf(self.python_context.applies(self._app()), 
                     "Context should not apply because cursor is not just before open paren")

        self._open_empty_test_file('temp.c')
        self._insert_in_active_buffer("outside = f()")
        self._say("select outside")
        self._assert_active_buffer_content_is('outside<CURSOR> = f()')
        self.failIf(self.c_context.applies(self._app()), 
                     "Context should not apply because cursor is not just before open paren")

        self._open_empty_test_file('temp.js')
        self._insert_in_active_buffer("outside = f()")
        self._say("select outside")
        self._assert_active_buffer_content_is('outside<CURSOR> = f()')
        self.failIf(self.javascript_context.applies(self._app()), 
                     "Context should not apply because cursor is not just before open paren")

        self._open_empty_test_file('temp.java')
        self._insert_in_active_buffer("outside = f()")
        self._say("select outside")
        self._assert_active_buffer_content_is('outside<CURSOR> = f()')
        self.failIf(self.java_context.applies(self._app()), 
                     "Context should not apply because cursor is not just before open paren")

        self._open_empty_test_file('temp.php')
        self._insert_in_active_buffer("outside = f()")
        self._say("select outside")
        self._assert_active_buffer_content_is('outside<CURSOR> = f()')
        self.failIf(self.php_context.applies(self._app()), 
                     "Context should not apply because cursor is not just before open paren")

    def test_ContBeforeArguments_applies_only_for_python(self):

        # also see tests above...
        self._open_empty_test_file('temp.py')
        self._insert_in_active_buffer("outside = f(inside)")
        self._say("select f")
        self.assert_(self.python_context.applies(self._app()), 
                     "Context should have applied because cursor was inside function arguments, in the correct language.")
        self.failIf(self.c_context.applies(self._app()), 
                     "c_context should NOT applied because in python buffer")


        self._open_empty_test_file('temp.c')
        self._insert_in_active_buffer("outside = f(inside)")
        self._say("select f")
        self.failIf(self.python_context.applies(self._app()), 
                     "Context should NOT have applied because the file was in the wrong language.")


##########################################################
# Unit tests
#
# These tests check the internal workings of the class.
##########################################################
    def test_Results_of_with_arguments(self):
        """testing the results in a python buffer"""

        self._open_empty_test_file('temp.py')
        self._insert_in_active_buffer(\
"""g = None
h = func(3, 4)
i = None
def test(i=5):
j = i + 6
k = test(i=7)""")
        self._assert_current_line_content_is("    k = test(i=7)<CURSOR>""")
        self._say("select func")
        self._assert_current_line_content_is("h = func<CURSOR>(3, 4)") 
        self.assert_(self.python_context.applies(self._app()), 'func should apply, because before a function call')
        self._say("select four")
        self.failIf(self.python_context.applies(self._app()), '4 should not apply')
        self._say("select five")
        self.failIf(self.python_context.applies(self._app()), '5 should not apply')
        self._say("select test")
        self.assert_(self.python_context.applies(self._app()), 'at test should apply')
        self._say("select None")
        self._assert_current_line_content_is("i = None<CURSOR>")
        self.failIf(self.python_context.applies(self._app()), 'at None should NOT apply')
        
        
    
###############################################################
# Assertions.
# 
# Use these methods to check the state of the class.
###############################################################
