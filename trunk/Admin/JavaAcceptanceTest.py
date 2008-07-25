import debug
import VoiceCodeRootTest

class JavaAcceptanceTest(VoiceCodeRootTest.VoiceCodeRootTest):
     
    def __init__(self, name):
        VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
    
    def setUp(self):
        self._init_simulator_regression()
        self._open_empty_test_file("blah.java")
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

    def test_dictate_some_statements(self):

## this was (stripped with all misrecognitions) the output of a voicecode
## session, all the Heard lines copied and edited to self._say(" etc
## note the self.collect_mode, the output of the test is the copied below
## so serves for further testing. I plan to use for what can I say demo as well...
##        self.collect_mode = 1
##        self._say("new statement")
##        self._say("import")
##        self._say("example module")
##        self._say("new statement")
##        self._say("define function")
##        self._say("hello")
##        self._say("with argument India")
##        self._say("do the following")
##        self._say("new statement")
##        self._say("india plus plus")

        self._say("new statement")
        expected = """\
<CURSOR>;
"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        #QH: import must probably as special word be defined, see javascript examples in vc_config...
        self._say("import")
        expected = """\
import<CURSOR>;
"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("example module")
        expected = """\
importexample_module<CURSOR>;
"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("new statement")
        expected = """\
importexample_module;
<CURSOR>;
"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("define function")
        expected = """\
importexample_module;
function <CURSOR>(){

    };
"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("hello")
        expected = """\
importexample_module;
function hello<CURSOR>(){

    };
"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("with argument India")
        expected = """\
importexample_module;
function hello(i<CURSOR>){

    };
"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("do the following")
        expected = """\
importexample_module;
function hello(i){
<CURSOR>
    };
"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("new statement")
        expected = """\
importexample_module;
function hello(i){

    <CURSOR>;
};
"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("india plus plus")
        expected = """\
importexample_module;
function hello(i){

    i++<CURSOR>;
};
"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
