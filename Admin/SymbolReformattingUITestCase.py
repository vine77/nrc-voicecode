#!/usr/bin/env python
#
# This example shows how to write a pyUnit test
import unittest
import MediatorConsoleWX



class SymbolReformattingUITestCase(unittest.TestCase):
    
    
    def __init__(self, name):
        unittest.TestCase.__init__(self, name)
        self.ui = None
    
    def setUp(self):
        self.ui = \
           MediatorConsoleWX.ReformatRecentSymbolsModel(None, None, [], None)
        
    def test_fixture_initialisation(self):
        assert self.ui != None, "Symbool reformatting model not initialised properly."
        

#    def test_displayed_utterances(self):
#        self.assert_sequences_have_same_content\
#               ("Displayed utterances were wrong.", [], self.ui.displayed_utterances())

