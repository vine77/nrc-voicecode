from wxPython.wx import *
import WinSystemMSW
import TestCaseWithHelpers
import MediatorConsoleWX
from SymbolResult import SymbolResult
import time
from SpokenUtterance import MockSpokenUtterance
from CmdInterp import MockUtteranceInterpretation


class SymbolReformattingUITestCase(TestCaseWithHelpers.TestCaseWithHelpers):    
    
#>    frame = wxFrame(None, wxNewId(), "test console", 
#>            wxDefaultPosition, wxDefaultSize)
 
#>    console = MediatorConsoleWX.MediatorConsoleWX(frame, win_sys = WinSystemMSW.WinSystemMSW())
    
    utter1 = MockSpokenUtterance(['new', 'symbol', 'one', 'one', 'equals', 'new', 'symbol', 'one', 'two'])
            
                                  
    sym1_1 = SymbolResult('new_symbol_1_1', ['new', 'symbol', 'one', 'one'], None, '', None, [], 
                          in_utter_interp=None)
    sym1_2 = SymbolResult('new_symbol_1_2', ['new', 'symbol', 'one', 'two'], None, '', None, [], 
                          in_utter_interp=None)               
    sym_list = [sym1_1, sym1_2]
                                   
    phrase1 = MockUtteranceInterpretation(utter1, symbols = sym_list, )
    sym1_1.in_utter_interp = phrase1
    sym1_2.in_utter_interp = phrase1

    
    def __init__(self, name):
        TestCaseWithHelpers.TestCaseWithHelpers.__init__(self, name)
        self.ui = None
    
    def setUp(self):
        self.ui = \
           MediatorConsoleWX.ReformatRecentSymbols(None, None, 
                                                        SymbolReformattingUITestCase.sym_list, 
                                                         None)
#>        self.ui = \
#>           MediatorConsoleWX.ReformatRecentSymbols(SymbolReformattingUITestCase.console, None, 
#>                                                        SymbolReformattingUITestCase.sym_list, 
#>
#>                                                         None)
        # AD: Uncomment this if you want to see what the window looks like. 
#        self.ui.ShowModal()
        
                                                         
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

#    def test_choose(self):
#       print "** test_choose"
#       self.ui.do_choose(0)
#       self.assert_equals("Selected symbol was wrong.", 0, self.ui.selected_symbol_index())