import debug
import cont_gen
import VoiceCodeRootTest

class ContPyInsideArgumentsTest(VoiceCodeRootTest.VoiceCodeRootTest):
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
        self.context = cont_gen.ContPyInsideArguments()

##########################################################
# Documentation tests
#
# These tests illustrate how to use the class.
##########################################################
      
    def test_This_is_how_you_create_a_ContPyInsideArguments(self):
        context = cont_gen.ContPyInsideArguments()
        self.assert_(isinstance(context, cont_gen.ContPyInsideArguments))
        
    def test_ContPyInsideArguments_applies_if_cursor_is_inside_function_arguments(self):
        self._open_empty_test_file('temp.py')
        self._insert_in_active_buffer("outside = f(inside)")
        self._say("select inside")
        self._assert_active_buffer_content_is('outside = f(inside<CURSOR>)')
        self.assert_(self.context.applies(self._app()), 
                     "Context should have applied because cursor inside function arguments")

    def test_ContPyInsideArguments_fails_if_cursor_is_outside_function_arguments(self):
        self._open_empty_test_file('temp.py')
        self._insert_in_active_buffer("outside = f(inside)")
        self._say("select outside")
        self._assert_active_buffer_content_is('outside<CURSOR> = f(inside)')
        self.failIf(self.context.applies(self._app()), 
                     "Context should not apply because cursor is outside function arguments")

    def test_ContPyInsideArguments_applies_only_for_python(self):

        self._open_empty_test_file('temp.py')
        self._insert_in_active_buffer("outside = f(inside)")
        self._say("select inside")
        self.assert_(self.context.applies(self._app()), 
                     "Context should have applied because cursor was inside function arguments, in the correct language.")
        self._open_empty_test_file('temp.c')
        self._insert_in_active_buffer("outside = f(inside)")
        self._say("select inside")
        self.failIf(self.context.applies(self._app()), 
                     "Context should NOT have applied because the file was in the wrong language.")


##########################################################
# Unit tests
#
# These tests check the internal workings of the class.
##########################################################
    def test_Results_of_equalsign(self):
        """testing the results in a python buffer"""
        self.fail("this works not in regression mode, equalsign QH testing")

        # nevermind:        
        self._open_empty_test_file('temp.py')
        self._say("golf assign value none")
        self._assert_active_buffer_content_is('g = None<CURSOR>')

        self._say("new statement")
        self._say("hotel equals")
        self._say("function with arguments")
        self._say("three comma four")
        self._assert_active_buffer_content_is("""g = None
h = func(3, 4)<CURSOR>""")

        
        self._say("new statement")
        self._say("define function test")
        self._say("after paren")
        self._say("India equals one")
        self._say("do the following")
        self._say("juliett equals india plus one")
        self._say("New-Line")
        self._say("kilo equals")
        self._say("test with arguments")
        self._say("India equal three")
        self._say("jump out")
        self._assert_active_buffer_content_is("""g = None
h = func(3, 4)
i = None'
def test(i=1):
    j = i + 1
    k = test(i=3)<CURSOR>""")
        
    
###############################################################
# Assertions.
# 
# Use these methods to check the state of the class.
###############################################################
