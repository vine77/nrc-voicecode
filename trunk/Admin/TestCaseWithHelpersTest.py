import TestCaseWithHelpers
import debug


class TestCaseWithHelpersTest(TestCaseWithHelpers.TestCaseWithHelpers):
    
    def __init__(self, name):
       TestCaseWithHelpers.TestCaseWithHelpers.__init__(self, name)
    
    def test_bad_length_in_assert_sequences_have_same_content(self):
        self.assert_sequences_have_same_content("NEVERMIND, this is supposed to fail",
                                                [], [1, 2])