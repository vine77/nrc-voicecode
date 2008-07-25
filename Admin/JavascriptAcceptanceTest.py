import debug
import VoiceCodeRootTest

class JavascriptAcceptanceTest(VoiceCodeRootTest.VoiceCodeRootTest):
     
    def __init__(self, name):
        VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
    
    def setUp(self):
        self._init_simulator_regression()
        self._open_empty_test_file("blah.js")
        self.collect_mode = 0   # return the contents of the buffer, for future tests
                                # can be set in indiviual test to 1 if you wish, but reset
                                # for real testing!
        self.collect_data = []
        
    def tearDown(self):
        if self.collect_mode:
            print '\n'.join(self.collect_data)
      
###############################################################
# Assertions.
# 
# Demo of statements, use collect_mode to set up...
###############################################################

    def test_define_variable_and_function(self):
        """the define variable statement sucks, to be studied!!!!"""
        
        self._say("new statement")
        expected = """\
<CURSOR>;
"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("define variable")
        expected = """\
define_variable<CURSOR>;
"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("example equals zero")
        expected = """\
define_variableexample = 0<CURSOR>;
"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("new statement")
        expected = """\
define_variableexample = 0;
<CURSOR>;
"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("define function")
        expected = """\
define_variableexample = 0;
function <CURSOR>(){

  };
"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("example function")
        expected = """\
define_variableexample = 0;
function example_function<CURSOR>(){

  };
"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("with argument India")
        expected = """\
define_variableexample = 0;
function example_function(i<CURSOR>){

  };
"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("do the following")
        expected = """\
define_variableexample = 0;
function example_function(i){
<CURSOR>
  };
"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("example plus equals India")
        expected = """\
define_variableexample = 0;
function example_function(i){
example += i<CURSOR>
  };
"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("new statement")
        expected = """\
define_variableexample = 0;
function example_function(i){
example += i
  <CURSOR>;
  };
"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("alert")
        expected = """\
define_variableexample = 0;
function example_function(i){
example += i
  alert<CURSOR>;
  };
"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("with arguments")
        expected = """\
define_variableexample = 0;
function example_function(i){
example += i
  alert(<CURSOR>);
  };
"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("between quotes")
        expected = '''\
define_variableexample = 0;
function example_function(i){
example += i
  alert("<CURSOR>");
  };
'''
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("new value colon")
        expected = '''\
define_variableexample = 0;
function example_function(i){
example += i
  alert("new_value: <CURSOR>");
  };
'''
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("jump out")
        expected = '''\
define_variableexample = 0;
function example_function(i){
example += i
  alert("new_value: "<CURSOR>);
  };
'''
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("plus example")
        expected = '''\
define_variableexample = 0;
function example_function(i){
example += i
  alert("new_value: " + example<CURSOR>);
  };
'''
        self._assert_active_buffer_content_with_selection_is(expected)
        #
