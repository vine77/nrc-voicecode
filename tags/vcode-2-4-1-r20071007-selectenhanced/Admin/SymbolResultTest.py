import debug
from SymbolResult import SymbolResult
from CmdInterp import CmdInterp
import VoiceCodeRootTest

class SymbolResultTest(VoiceCodeRootTest.VoiceCodeRootTest):
     
    def __init__(self, name):
        VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
        self.sym_res1 = None
    
    def setUp(self):
        self._init_simulator_regression()
        self.written1 = 'some_symb'
        self.sym_res1 = SymbolResult(native_symbol = 'some_symb', 
                                     spoken_phrase = ['some', 'symbol'], 
                                     exact_matches = ['SomeSymb'],
                                     as_inserted='',
                                     buff_name=None,
                                     builder_preferences=['std_underscores', 'std_intercaps',
                                                          'std_all_caps_underscores'],
                                     possible_matches = [(2, 's_sym'), (1, 'sSmb'), (3, 'so_sbl')],
                                     forbidden=None,
                                     new_symbol=0,
                                     in_utter_interp=None)
                                                         
    def tearDown(self):
        pass
        
    def test_fixture_initialisation(self):
        pass
        
    def test_suggestions_list(self):
        self.assert_equal(
                     ['some_symb', 'SomeSymb', 'so_sbl', 's_sym', 'sSmb',
                     'some_symbol', 'SomeSymbol', 'SOME_SYMBOL'], 
                     self.sym_res1.suggestions_list(), 
                     "Suggested alternate forms for symbol were wrong.")

    def test_builder_preferences_python(self):
        """This test should be made to work.  But I cannot get the right procedure here.

        This wasn't tested before.  Quintijn
        """
        interp = CmdInterp()
        interp.set_builder_preferences(['std_lower_intercaps', 'std_underscores', 'std_run_together'],
                        language=('python', 'javascript', 'php'))
        self._open_empty_test_file('temp.py')
        self._say("new variable equals old variable")
##        self._assert_active_buffer_content_is('newVariable = oldVariable<CURSOR>')
