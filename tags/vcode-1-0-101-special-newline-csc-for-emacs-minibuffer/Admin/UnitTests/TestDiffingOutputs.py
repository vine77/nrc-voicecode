class TestOutputDiffs(TestCaseDiffingOutputs):

    def test_dont_fail_when_shouldnt(self):
         sys.stderr.write('STDERR -- TestOutputDiffs.test_dont_fail_when_shouldnt: invoked\n')
         self.start_new_test('dont_fail_when_shouldnt')
         print 'This should be the same as benchmark'
         self.compare_outputs()
         sys.stderr.write('STDERR -- TestOutputDiffs.test_dont_fail_when_shouldnt: exited\n')

    def test_fail_when_should(self):
         sys.stderr.write('STDERR -- TestOutputDiffs.test_fail_when_should: invoked\n')
         self.start_new_test('fail_when_should')
         print 'This should NOT be the same as benchmark'
         self.compare_outputs()
         sys.stderr.write('STDERR -- TestOutputDiffs.test_fail_when_should: exited\n') 
   

test_runner.add_suite(TestOutputDiffs)

