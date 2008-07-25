import debug
import VoiceCodeRootTest

class PythonAcceptanceTest(VoiceCodeRootTest.VoiceCodeRootTest):
     
    def __init__(self, name):
        VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
    
    def setUp(self):
        self._init_simulator_regression()
        self._open_empty_test_file("blah.py")
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
        self._say("total equals zero new statement")
        expected = """\
total = 0
<CURSOR>"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("for india in list")
        expected = """\
total = 0
for i in <CURSOR>:
    """
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("range with arguments")
        expected = """\
total = 0
for i in range(<CURSOR>):
    """
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("ten do the following")
        expected = """\
total = 0
for i in range(10):
    <CURSOR>"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("square equals india times india new statement")
        expected = """\
total = 0
for i in range(10):
    square = i * i
    <CURSOR>"""
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("print between quotes")
        expected = '''\
total = 0
for i in range(10):
    square = i * i
    print "<CURSOR>"'''
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("square of  colon")
        expected = '''\
total = 0
for i in range(10):
    square = i * i
    print "square_of: <CURSOR>"'''
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("percent sierra")
        expected = '''\
total = 0
for i in range(10):
    square = i * i
    print "square_of: %s<CURSOR>"'''
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("space-bar is colon")
        expected = '''\
total = 0
for i in range(10):
    square = i * i
    print "square_of: %s is: <CURSOR>"'''
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("percent sierra")
        expected = '''\
total = 0
for i in range(10):
    square = i * i
    print "square_of: %s is: %s<CURSOR>"'''
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("jump out percent-sign")
        expected = '''\
total = 0
for i in range(10):
    square = i * i
    print "square_of: %s is: %s"%<CURSOR>'''
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("between parens india comma square")
        expected = '''\
total = 0
for i in range(10):
    square = i * i
    print "square_of: %s is: %s"%(i, square<CURSOR>)'''
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("new statement")
        expected = '''\
total = 0
for i in range(10):
    square = i * i
    print "square_of: %s is: %s"%(i, square)
    <CURSOR>'''
        self._assert_active_buffer_content_with_selection_is(expected)
        #
        self._say("total plus equals square")
        expected = '''\
total = 0
for i in range(10):
    square = i * i
    print "square_of: %s is: %s"%(i, square)
    total += square<CURSOR>'''
        self._assert_active_buffer_content_with_selection_is(expected)
        #
