from wxPython.wx import *
import WinSystemMSW
import debug
import TestCaseWithHelpers
import MediatorConsoleWX
from SymbolResult import SymbolResult
import time
from SpokenUtterance import MockSpokenUtterance
from CmdInterp import MockUtteranceInterpretation


class MockReformatFromRecentWX(MediatorConsoleWX.ReformatFromRecentWX):
   """mock implementation of a dialog for reformatting a selected symbol.
   
   This mock implementation can be "displayed modally" without blocking.
   
   **INSTANCE ATTRIBUTES**
   
   *BOOL was_displayed_modally* -- flag indicating whether or not this dialog
   has been displayed modally yet. Initially false.
   """
   
   def __init__(self, **args):
      debug.trace('MockReformatFromRecentWX.__init__', '** invoked')
      self.deep_construct(MockReformatFromRecentWX,
                          {'was_displayed_modally': None},
                          args
                          )
      debug.trace('MockReformatFromRecentWX.__init__', '** upon exit, self.view()=%s, self.view_layer=%s' % (self.view(), self.view_layer))
                          
   def ShowModal(self):
      self.was_displayed_modally = 1
      
   def make_view(self):
      return MockReformatFromRecentViewWX(console = self.console, parent = self.parent,
                                          symbol = self.symbol,
                                          model = self)   
      
   def reset(self, symbol):
      self.was_displayed_modally = None
      MediatorConsoleWX.ReformatFromRecentWX.reset(self, symbol)

class MockReformatFromRecentViewWX(MediatorConsoleWX.ReformatFromRecentViewWX):
   """mock implementation of the view layer for a dialog to reformat a
   seleted symbol"""
   
   def __init__(self, **args):
      self.deep_construct(MockReformatFromRecentViewWX, {}, args)
   

class SymbolReformattingUITestCase(TestCaseWithHelpers.TestCaseWithHelpers):    
    
    frame = wxFrame(None, wxNewId(), "test console", 
            wxDefaultPosition, wxDefaultSize)
 
    console = MediatorConsoleWX.MediatorConsoleWX(frame, win_sys = WinSystemMSW.WinSystemMSW())
    
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
        self.mock_reformat_from_recent = \
           MockReformatFromRecentWX(console = SymbolReformattingUITestCase.console, 
                                     parent = None, symbol = None)
        self.ui = \
           MediatorConsoleWX.ReformatRecentSymbols(SymbolReformattingUITestCase.console, 
                                                   None, 
                                                   SymbolReformattingUITestCase.sym_list, 
                                                   None,
                                                   dlg_reformat_from_recent = self.mock_reformat_from_recent)

        # AD: Uncomment this if you want to see what the window looks like. 
#        self.ui.ShowModal()
        
                                                         
    def tearDown(self):
        SymbolReformattingUITestCase.console.destroy_main_frame()
        self.mock_reformat_from_recent.Destroy()
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

    def test_choose(self):
       debug.trace('test_choose', '** upon entry, self.mock_reformat_from_recent.view_layer=%s' % self.mock_reformat_from_recent.view_layer)
       self.ui.do_choose(0)
       debug.trace('test_choose', '** after choose, self.mock_reformat_from_recent.view_layer=%s' % self.mock_reformat_from_recent.view_layer)
       self.assert_equals("Selected symbol was wrong.", 0, self.ui.selected_symbol_index())
       debug.trace('test_choose', '** upon exit, self.mock_reformat_from_recent.view_layer=%s' % self.mock_reformat_from_recent.view_layer)