import unittest
import debug

class TestCaseWithHelpers(unittest.TestCase):
    
    
    def __init__(self, name):
        unittest.TestCase.__init__(self, name)
    
    def assert_sequences_have_same_content(self, mess, expected, got):
        debug.trace('TestCaseWithHelpers.assert_sequences_have_same_content', 
                    '** expected=%s, got=%s' % (expected, got))
        debug.trace('TestCaseWithHelpers.assert_sequences_have_same_content', 
                    '** len(expected)=%s, len(got)=%s' % (len(expected), len(got)))
                    
        if len(expected) != len(got):  
           self.fail(mess + "\nExpeted sequence of length %s, but got sequence of length %s" \
                     % (len(expected), len(got)))
                     

        for ii in range(len(expected)):
           if expected[ii] != got[ii]:
              self.fail(mess + "\nItem at position %s was wrong. Expected %s, but got %s" \
                     % (ii, expected[ii], got[ii]))
           
