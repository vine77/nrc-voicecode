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
   
class MediatorConsoleWXTestCase(TestCaseWithHelpers.TestCaseWithHelpers): 
   """class for test cases that require a running mediator console ui."""
   def __init__(self, name):
      TestCaseWithHelpers.TestCaseWithHelpers.__init__(self, name)
      frame = wxFrame(None, wxNewId(), "test console", 
            wxDefaultPosition, wxDefaultSize)
 
      self.console = MediatorConsoleWX.MediatorConsoleWX(frame, win_sys = WinSystemMSW.WinSystemMSW())
      

class ReformatRecentTestCase(MediatorConsoleWXTestCase):    
     
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
        MediatorConsoleWXTestCase.__init__(self, name)
        self.dlg = None
    
    def setUp(self):
        self.mock_reformat_from_recent = \
           MockReformatFromRecentWX(console = self.console, 
                                     parent = None, symbol = ReformatRecentTestCase.sym1_1)
        self.dlg = \
           MediatorConsoleWX.ReformatRecentSymbols(self.console, 
                                                   None, 
                                                   ReformatRecentTestCase.sym_list, 
                                                   None,
                                                   dlg_reformat_from_recent = self.mock_reformat_from_recent)

        # AD: Uncomment this if you want to see what the window looks like. 
#        self.dlg.ShowModal()
        
                                                         
    def tearDown(self):
        self.console.destroy_main_frame()
        self.mock_reformat_from_recent.Destroy()
        self.dlg.Destroy()
        
    def test_fixture_initialisation(self):
        self.assert_(self.dlg != None, "Symbool reformatting model not initialised properly.")
        
    def test_displayed_symbols(self):
        self.assert_sequences_have_same_content\
               ("Displayed utterances were wrong.", 
                  [
                     ['2', 'new_symbol_1_1', 'new symbol one one', 
                      'new symbol one one equals new symbol one two'], 
                     ['1', 'new_symbol_1_2', 'new symbol one two', 
                      'new symbol one one equals new symbol one two']
                  ], 
                self.dlg.displayed_symbols())

    def assert_reformat_from_recent_invoked_with_symbol(self, symbol):
       self.assert_(self.dlg.dlg_reformat_from_recent.was_displayed_modally,
                    "Reformat from recent dialog was not displayed")
       self.assert_equals("Reformat from recent dialog invoked with wrong symbol", 
                          symbol, self.dlg.dlg_reformat_from_recent.symbol)

    def test_choose(self):
       self.dlg.do_choose(0)
       self.assert_equals("Selected symbol was wrong.", 0, self.dlg.selected_symbol_index())
       self.assert_reformat_from_recent_invoked_with_symbol(self.dlg.symbols[0])
       
class ReformatFromRecentTestCase(MediatorConsoleWXTestCase):
    def __init__(self, name):
       MediatorConsoleWXTestCase.__init__(self, name)
       self.dlg = None
       
    def setUp(self):
       self.utter1 = MockSpokenUtterance(['new', 'symbol', 'one', 'one', 'equals', 'new', 'symbol', 'one', 'two'])                                  
       self.sym1_1 = SymbolResult('new_symbol_1_1', ['new', 'symbol', 'one', 'one'], None, '', None, [], 
                          in_utter_interp=None)
       self.sym1_1.alternate_forms = ['new_sym_1_1', 'NewSym1_1', 'newSym11', 
                                      'NEW_SYMBOL_1_1', 'new_symbol_1_1']
       self.dlg = MediatorConsoleWX.ReformatFromRecentWX \
                        (console = self.console, 
                        parent = None, symbol = self.sym1_1)
       # AD: Uncomment this if you want to see what the window looks like. 
#       self.dlg.ShowModal()


    def tearDown(self):
        self.console.destroy_main_frame()
        self.dlg.Destroy()

    def assert_displayed_form_is(self, expected, mess=''):
        self.assert_equals(mess + "Corrected form displayed by view was wrong",
                           expected, self.dlg.chosen_form())
                           
    def assert_displayed_alternate_forms_are(self, expected, mess=''):
        self.assert_sequences_have_same_content("%s\nAlternate forms for the symbol displayed by the view were wrong." % mess,
                                                expected, self.dlg.displayed_list_of_alternate_forms())

    def test_fixture_initialisation(self):
        self.assert_(self.dlg != None, "Reformat from recent dialog not initialised properly.")
        self.assert_displayed_form_is('new_symbol_1_1')
        self.assert_displayed_alternate_forms_are(self.sym1_1.alternate_forms)
        
    def test_on_select(self):
        self.dlg.do_select_nth_form(2)
        self.assert_displayed_form_is(self.sym1_1.alternate_forms[2], 'Selecting new format did not change the displayed form.')
