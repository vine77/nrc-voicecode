import exceptions, re, string, sys
from debug import trace, config_traces, trace_file, trace_fct, to_be_traced
from unittest import makeSuite, TestCase, TestSuite, TextTestRunner

config_traces(status='off', active_traces='all')

def containsString(str, substring):
    return string.find(str, substring) >= 0

class VCTestSuite(TestSuite):
    def __init__(self, name_indexed_tests):
        self.invert_test_indexing(name_indexed_tests)
        TestSuite.__init__(self, self.test_name.keys())

    def invert_test_indexing(self, name_indexed_tests):
        self.test_name = {}
        for (a_test_name, a_test) in name_indexed_tests.items():
            self.test_name[a_test] = a_test_name

    def __call__(self, result):
        tests_so_far = 0
        total_tests = self.countTestCases()
        for test in self._tests:
            tests_so_far = tests_so_far + test.countTestCases()
            sys.stderr.write('\n... running %s (%s of %s)\n' %
                             (self.test_name[test], tests_so_far,
                              total_tests))
            if result.shouldStop:
                break
            test(result)
        return result
    

class VCPyUnitTestRunner(TextTestRunner):
    def __init__(self):
        self.all_suites = {}
        TextTestRunner.__init__(self)

    def get_test_class_name(self, test_class):
        a_match = re.match('\s*<\s*class\s+[\s\S]*?\\.([^\\.]*)\s+at',
                           repr(test_class))
        return a_match.group(1)

    def add_suite(self, test_class):
        self.all_suites[self.get_test_class_name(test_class)] = makeSuite(test_class, 'test')

    
    def generate_suite_to_run(self, test_names_list):
        test_suites_to_run = {}
        for a_suite_name in test_names_list:
            if a_suite_name == 'all':
                test_suites_to_run = self.all_suites
                break
            test_suites_to_run[a_suite_name] = self.all_suites[a_suite_name]
            
        suite_with_all_tests = VCTestSuite(test_suites_to_run)
            
        return suite_with_all_tests


    def run_tests_with_names(self, test_names_list):
        test_runner = TextTestRunner()        
        test_suite_to_run = self.generate_suite_to_run(test_names_list)
        self.run(test_suite_to_run)
           
test_runner = VCPyUnitTestRunner()

class HelloTest(TestCase):
    def test_hello(self):
        abc = "hello"
        assert (abc == 1), 'string was not 1'

    def test_1(self):
        abc = 1
        assert (abc == 1), 'string was not 1'

test_runner.add_suite(HelloTest)
                              

class TraceTest(TestCase):
    def setUp(self):
        self.old_trace_fct = trace_fct
        self.old_trace_file = trace_file
        self.old_to_be_traced = to_be_traced

    def reset_traces_config(self):
        trace_fct = self.old_trace_fct
        trace_file = self.old_trace_file
        to_be_traced = self.old_to_be_traced        
    
    def do_some_traces(self, status, activate_all=0):
        global mock_stdout
        mock_stdout = StreamMock(mode='w')
        if activate_all:
            active_traces = 'all'
        else:
            active_traces = {'always_in_active_list': 1}
        config_traces(print_to=mock_stdout, status=status,
                      active_traces=active_traces)
        trace('always_in_active_list', '')
        trace('never_in_active_list', '')
        self.reset_traces_config()        
        return mock_stdout.stream

    def what_was_printed(self):
        return '\nTraces printed: "%s"' % mock_stdout.stream

    def test_traces_not_printed_when_status_off(self):
        assert self.do_some_traces(status='off') == '', \
               'traces printed even though trace status was \'off\'' + \
               self.what_was_printed()                

    def test_traces_printed_when_active(self):
        assert containsString(self.do_some_traces('on'),
                                  '-- always_in_active_list'), \
               'active trace not printed even though trace status was \'on\'' + \
               self.what_was_printed()                

    def test_traces_not_printed_when_inactive(self):
        assert not containsString(self.do_some_traces('on'),
                              '-- never_in_active_list'), \
               'inactive trace was printed' + \
               self.what_was_printed()        

    def test_traces_printed_when_all_active(self):
        assert containsString(self.do_some_traces('on', activate_all=1),
                              '-- never_in_active_list'), \
               'inactive trace not printed even though overode all traces with active.' + \
               self.what_was_printed()
        
        assert containsString(self.do_some_traces('on', activate_all=1),
                              '-- always_in_active_list'), \
               'active trace not printed when all traces overriden with active.' + \
               self.what_was_printed()
                
        

test_runner.add_suite(TraceTest)


###############################################################################
# Some useful support classes for building tests
###############################################################################

class StreamMock:
    """Mimicks the behaviour of a file, except that it reads writes to a
    string.

    I bet there is something like this in Python, but I didn't find it."""
    
    def __init__(self, mode='r'):
        if re.search('r', mode):
            self.mode = 'r'
        else:
            self.mode = 'w'
            if not re.search('a', mode):
                self.stream = ''

        
    def write(self, str):
        self.stream = self.stream + str

mock_stdout = StreamMock()


if __name__ == '__main__':
    test_runner.run_tests_with_names(['all'])
#    test_runner.run_tests_with_names(['TraceTest'])
