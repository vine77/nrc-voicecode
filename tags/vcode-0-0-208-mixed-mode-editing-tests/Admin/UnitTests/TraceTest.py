class TraceTest(TestCase):
    def setUp(self):
        self.old_trace_fct = trace_fct
        self.old_trace_file = trace_file
        self.old_to_be_traced = to_be_traced
        self.old_activate_trace_id_substrings = activate_trace_id_substrings

    def reset_traces_config(self):
        trace_fct = self.old_trace_fct
        trace_file = self.old_trace_file
        to_be_traced = self.old_to_be_traced        
    
    def do_some_traces(self, status, activate_all=0, allow_trace_id_substring=None):
        global mock_stdout
        mock_stdout = StreamMock(mode='w')
        if activate_all:
            active_traces = 'all'
        else:
            active_traces = {'always_in_active_list': 1}
            
        config_traces(print_to=mock_stdout, status=status,
                      active_traces=active_traces,
                      allow_trace_id_substrings=allow_trace_id_substring)
        trace('always_in_active_list', '')
        trace('never_in_active_list', '')
        trace('XXXXXalways_in_active_list', '')        
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

    def test_substring_traces_not_printed_when_substrings_not_allowed(self):
        assert not containsString(self.do_some_traces('on'),
                                 'XXXalways_in_active_list'), \
               'substring trace printed eventhough substrings were not allowed' + \
               self.what_was_printed()

    def test_traces_printed_when_activated_through_substring(self):
        assert containsString(self.do_some_traces('on', allow_trace_id_substring=1),
                              'XXXXalways_in_active_list'), \
               'trace NOT printed eventhough activated through regexp' + \
               self.what_was_printed()
            
    def test_traces_not_printed_when_not_activated_through_substring(self):
        assert not containsString(self.do_some_traces('on', allow_trace_id_substring=1),
                                  '-- never_in_active_list'), \
               'trace printed eventhough NOT activated through regexp' + \
               self.what_was_printed()
                                      
test_runner.add_suite(TraceTest)
