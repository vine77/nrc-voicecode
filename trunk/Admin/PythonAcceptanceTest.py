import debug
import VoiceCodeRootTest

class PythonAcceptanceTest(VoiceCodeRootTest.VoiceCodeRootTest):
     
    def __init__(self, name):
        VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
    
    def setUp(self):
       self._init_simulator_regression(exclusive=0)
                                                         
    def tearDown(self):
        pass
      
###############################################################
# Assertions.
# 
# Use these methods to check the state of the class.
###############################################################

    def test_dictate_some_statements(self):
        
        self._open_empty_test_file("blah.py")

        self._say("text mode off")
        self._say(["join", "under", "testing", "python"])
        self._say("with voicecode")
        expected = ['/* ', 'testing python', '*/']
        
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
        self._say("plus equals one")
        self._assert_active_buffer_content_is('\n'.join(expected))
        

        self._say("new statement")
        self._say("india plus plus")
        self._say("jump out two times")
        self._assert_active_buffer_content_is('\n'.join(expected))

