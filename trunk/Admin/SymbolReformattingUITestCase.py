import TestCaseWithHelpers
import MediatorConsoleWX
from SpokenUtterance import MockSpokenUtterance



class SymbolReformattingUITestCase(TestCaseWithHelpers.TestCaseWithHelpers):
    
    
    
    utter1 = MockSpokenUtterance([('new', 'new'), ('symbol', 'symbol'), 
                                   (' = ', 'equals'), ('0', 'zero')])
                                   
    utter_list = [(utter1, 1, 1, ['new_symbol'])]
                                   
    
    def __init__(self, name):
        TestCaseWithHelpers.TestCaseWithHelpers.__init__(self, name)
        self.ui = None
    
    def setUp(self):
        self.ui = \
           MediatorConsoleWX.ReformatRecentSymbolsModel(None, None, 
                                                        SymbolReformattingUITestCase.utter_list, 
                                                         None)
                                                         
    def tearDown(self):
        print "Tearing down"
        self.ui.Close()
                                                       
        
    def test_fixture_initialisation(self):
        assert self.ui != None, "Symbool reformatting model not initialised properly."

    def test_displayed_utterances(self):
        self.assert_sequences_have_same_content\
               ("Displayed utterances were wrong.", [], self.ui.displayed_utterances())

