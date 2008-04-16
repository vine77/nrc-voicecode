import debug
import cont_gen
import VoiceCodeRootTest
from vc_globals import all_languages, c_style_languages

class ContInsideArgumentsTest(VoiceCodeRootTest.VoiceCodeRootTest):
    """Test the InsideArguments Context in python

    This context should apply if The cursor is inside the arguments section of a function definition or a function call.  So between the parens.

    def f(here):
        pass

    or 

    x = f(here)

    This context can be used for formatting the "=" without spacing when inside. 
    (QH, dec 2006)

    """   
    def __init__(self, name):
        VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
      
    def setUp(self):
        self._init_simulator_regression()
        self.python_context = cont_gen.ContInsideArguments('python')
        self.c_context = cont_gen.ContInsideArguments('C')
        self.javascript_context = cont_gen.ContInsideArguments('javascript')
        self.java_context = cont_gen.ContInsideArguments('java')
        self.php_context = cont_gen.ContInsideArguments('php')
        self.perl_context = cont_gen.ContInsideArguments('perl')
        self.all_context = cont_gen.ContInsideArguments(all_languages)
        self.c_style_context = cont_gen.ContInsideArguments(c_style_languages)

##########################################################
# Documentation tests
#
# These tests illustrate how to use the class.
##########################################################
      
    def test_This_is_how_you_create_a_ContInsideArguments(self):
        python_context = cont_gen.ContInsideArguments('python')
        self.assert_(isinstance(python_context, cont_gen.ContInsideArguments))
        
    def test_ContInsideArguments_applies_if_cursor_is_inside_function_arguments(self):
        self._open_empty_test_file('temp.py')
        self._insert_in_active_buffer("outside = f(inside)")
        self._say("select inside")
        self._assert_active_buffer_content_is('outside = f(inside<CURSOR>)')
        self.assert_(self.python_context.applies(self._app()), 
                     "python_context should have applied because cursor inside function arguments")
        self.assert_(self.all_context.applies(self._app()), 
                     "all_context should have applied because cursor inside function arguments")

        self._open_empty_test_file('temp.c')
        self._insert_in_active_buffer("outside = f(inside)")
        self._say("select inside")
        self._assert_active_buffer_content_is('outside = f(inside<CURSOR>)')
        self.assert_(self.c_context.applies(self._app()), 
                     "c_context should have applied because cursor inside function arguments")
        self.assert_(self.c_style_context.applies(self._app()), 
                     "c_style_context should have applied because cursor inside function arguments")
        self.assert_(self.all_context.applies(self._app()), 
                     "all_context should have applied because cursor inside function arguments")



        self._open_empty_test_file('temp.js')
        self._insert_in_active_buffer("outside = f(inside)")
        self._say("select inside")
        self._assert_active_buffer_content_is('outside = f(inside<CURSOR>)')
        self.assert_(self.javascript_context.applies(self._app()), 
                     "javascript_context should have applied because cursor inside function arguments")
        self.assert_(self.c_style_context.applies(self._app()), 
                     "c_style_context should have applied because cursor inside function arguments")
        self.assert_(self.all_context.applies(self._app()), 
                     "all_context should have applied because cursor inside function arguments")

        self._open_empty_test_file('temp.java')
        self._insert_in_active_buffer("outside = f(inside)")
        self._say("select inside")
        self._assert_active_buffer_content_is('outside = f(inside<CURSOR>)')
        self.assert_(self.java_context.applies(self._app()), 
                     "java_context should have applied because cursor inside function arguments")
        self.assert_(self.c_style_context.applies(self._app()), 
                     "c_style_context should have applied because cursor inside function arguments")
        self.assert_(self.all_context.applies(self._app()), 
                     "all_context should have applied because cursor inside function arguments")

        self._open_empty_test_file('temp.php')
        self._insert_in_active_buffer("outside = f(inside)")
        self._say("select inside")
        self._assert_active_buffer_content_is('outside = f(inside<CURSOR>)')
        self.assert_(self.php_context.applies(self._app()), 
                     "php_context should have applied because cursor inside function arguments")
        self.assert_(self.c_style_context.applies(self._app()), 
                     "c_style_context should have applied because cursor inside function arguments")
        self.assert_(self.all_context.applies(self._app()), 
                     "all_context should have applied because cursor inside function arguments")


        self._open_empty_test_file('temp.pl')
        self._insert_in_active_buffer("outside = f(inside)")
        self._say("select inside")
        self._assert_active_buffer_content_is('outside = f(inside<CURSOR>)')
        self.assert_(self.perl_context.applies(self._app()), 
                     "perl_context should have applied because cursor inside function arguments")
        self.assert_(self.c_style_context.applies(self._app()), 
                     "c_style_context should have applied because cursor inside function arguments")
        self.assert_(self.all_context.applies(self._app()), 
                     "all_context should have applied because cursor inside function arguments")



    def test_ContInsideArguments_fails_if_cursor_is_outside_function_arguments(self):
        self._open_empty_test_file('temp.py')
        self._insert_in_active_buffer("outside = f(inside)")
        self._say("select outside")
        self._assert_active_buffer_content_is('outside<CURSOR> = f(inside)')
        self.failIf(self.python_context.applies(self._app()), 
                     "Context should not apply because cursor is outside function arguments")
        self.failIf(self.all_context.applies(self._app()), 
                     "all_context should not apply because cursor is outside function arguments")

    def test_ContInsideArguments_applies_only_for_python(self):

        self._open_empty_test_file('temp.py')
        self._insert_in_active_buffer("outside = f(inside)")
        self._say("select inside")
        self.assert_(self.python_context.applies(self._app()), 
                     "Context should have applied because cursor was inside function arguments, in the correct language.")
        self._open_empty_test_file('temp.c')
        self._insert_in_active_buffer("outside = f(inside)")
        self._say("select inside")
        self.failIf(self.python_context.applies(self._app()), 
                     "Context should NOT have applied because the file was in the wrong language.")

        self._open_empty_test_file('temp.java')
        self._insert_in_active_buffer("outside = f(inside)")
        self._say("select inside")
        self.failIf(self.python_context.applies(self._app()), 
                     "Context should NOT have applied because the file was in the wrong language.")


##########################################################
# Unit tests
#
# These tests check the internal workings of the class.
##########################################################
    def test_Results_of_equalsign(self):
        """testing the results in a python buffer"""

        # nevermind:        
        self._open_empty_test_file('temp.py')
        self._insert_in_active_buffer("""g = None
h = func(3, 4)
i = None'
def test(i=5):
j = i + 6
k = test(i=7)""")
        self._say("select three")
        self._assert_current_line_content_is("h = func(3<CURSOR>, 4)")
        self.assert_(self.python_context.applies(self._app()), '3 should apply, because inside a function call')
        self._say("select four")
        self.assert_(self.python_context.applies(self._app()), '4 should apply, because inside a function call')
        self._say("select five")
        self.assert_(self.python_context.applies(self._app()), '5 should apply, because inside a function call')
        self._say("select six")
        self.failIf(self.python_context.applies(self._app()), '6 should NOT apply, because inside a function call')
        self._say("select seven")
        self.assert_(self.python_context.applies(self._app()), '7 should apply, because inside a function call')
        self._say("select test")
        self.failIf(self.python_context.applies(self._app()), 'at test should NOT apply, because inside a function call')
        self._say("select none")
        self.failIf(self.python_context.applies(self._app()), 'at None should NOT apply, because inside a function call')
        

    def test_Results_of_equalsign_multiple_lines(self):
        """testing the results in a python buffer"""

        # nevermind:        
        self._open_empty_test_file('temp.py')
        self._insert_in_active_buffer(\
"""g = None
h = func(3,
         4)
i = None
def test(i=5,
         j=dict(a='bravo', c='delta'),
         k, l=10):
x = y + 6""")
        self._say("select three")
        self._assert_current_line_content_is("h = func(3<CURSOR>,")
        self.assert_(self.python_context.applies(self._app()), '3 should apply, because inside a function call')
        self._say("select four")
        # if this test goes wrong, probably the automatic indent of
        # emacs is not working well
        self._assert_current_line_content_is("                  4<CURSOR>)")
        self.assert_(self.python_context.applies(self._app()), '4 should apply, because inside a function call')
        self._say("select five")
        self.assert_(self.python_context.applies(self._app()), '5 should apply, because inside a function call')
        self._say("select bravo")
        self.assert_(self.python_context.applies(self._app()), 'bravo should apply, because inside a function call')
        self._say("select charlie")
        self.assert_(self.python_context.applies(self._app()), 'charlie should apply, because inside a function call')
        self._say("select kilo")
        self.assert_(self.python_context.applies(self._app()), 'kilo should apply, because inside a function call')
        self._say("select test")
        self.failIf(self.python_context.applies(self._app()), 'at test should NOT apply, because inside a function call')
        self._say("select none")
        self.failIf(self.python_context.applies(self._app()), 'at None should NOT apply, because inside a function call')
        self._say("select x-ray")
        self.failIf(self.python_context.applies(self._app()), 'at x should NOT apply, because inside a function call')
 
        
    
###############################################################
# Assertions.
# 
# Use these methods to check the state of the class.
###############################################################
