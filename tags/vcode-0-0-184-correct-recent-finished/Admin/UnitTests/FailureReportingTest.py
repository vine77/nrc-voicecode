class FailureReportingTest(TestCase):
    def test_failure_reporting(self):
        assert 0, 'NEVER MIND THIS FAILURE!\nJust testing that PyUnit reports failures.'


test_runner.add_suite(FailureReportingTest)
                              
