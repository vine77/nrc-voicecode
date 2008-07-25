import debug
import VoiceCodeRootTest

class JavascriptAcceptanceTest(VoiceCodeRootTest.VoiceCodeRootTest):
     
    def __init__(self, name):
        VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
    
    def setUp(self):
       self._init_simulator_regression(exclusive=0)
       self._open_empty_test_file("blah.js")
       self.source_buff = self._app().curr_buffer()
                                                         
    def tearDown(self):
        pass
      
###############################################################
# Assertions.
# 
# Use these methods to check the state of the class.
###############################################################

    def test_dictate_some_statements(self):
        
        self._say("voice coder what can I say")
        self._say("testing javascript")
        self._say("with voicecode")
        self._say("end long comment")
        expected = ['/* ', 'testing javascript', '*/']
        
        self._assert_active_buffer_content_is('\n'.join(expected))

        self._say("new paragraph")
        self._say("define function")
        self._say("testing")
        self._assert_active_buffer_content_is('\n'.join(expected))

        self._say("do the following")
        self._say("if statement")
        self._say("condition")
        self._say("do the following")
        self._say("new statement")
        self._say("India")
        self._say("equals one")
        self._assert_active_buffer_content_is('\n'.join(expected))
        

        self._say("new statement")
        self._say("india plus plus")
        self._say("jump out two times")
        self._assert_active_buffer_content_is('\n'.join(expected))

