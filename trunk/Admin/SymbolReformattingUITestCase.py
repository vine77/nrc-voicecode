import TestCaseWithHelpers
import MediatorConsoleWX
import MediatorConsole
import time
from SpokenUtterance import MockSpokenUtterance


class SymbolReformattingUITestCase(TestCaseWithHelpers.TestCaseWithHelpers):    
    
    utter1 = MockSpokenUtterance([('new', 'new'), ('symbol', 'symbol'), ('one', 'one'), ('one', 'one'), 
                                  ('equals', ' = '), 
                                  ('new', 'new'), ('symbol', 'symbol'), ('one', 'one'), ('two', 'two')])
    sym1_1 = MediatorConsole.SymbolToReformat('new_symbol_1_1', 'new symbol one one', utter1, 1)
    sym1_2 = MediatorConsole.SymbolToReformat('new_symbol_1_2', 'new symbol one two', utter1, 1)    
                                   
    sym_list = [sym1_1, sym1_2]
                                   
    
    def __init__(self, name):
        TestCaseWithHelpers.TestCaseWithHelpers.__init__(self, name)
        self.ui = None
    
    def setUp(self):
        self.ui = \
           MediatorConsoleWX.ReformatRecentSymbolsModel(None, None, 
                                                        SymbolReformattingUITestCase.sym_list, 
                                                         None)
        # AD: Uncomment this if you want to see what the window looks like. 
        # self.ui.ShowModal()
        
                                                         
    def tearDown(self):
        self.ui.Destroy()
                                                       
        
    def test_fixture_initialisation(self):
        assert self.ui != None, "Symbool reformatting model not initialised properly."

    def test_displayed_symbols(self):
        self.assert_sequences_have_same_content\
               ("Displayed utterances were wrong.", 
                  [
                     ['2', 'new_symbol_1_1', 'new symbol one one', 
                      'new symbol one one equals new symbol one two'], 
                     ['1', 'new_symbol_1_2', 'new symbol one two', 
                      'new symbol one one equals new symbol one two']
                  ], 
                self.ui.displayed_symbols())

