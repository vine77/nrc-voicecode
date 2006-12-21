import debug
import VoiceCodeRootTest
import SymDict

class SymDictTest(VoiceCodeRootTest.VoiceCodeRootTest):
   def __init__(self, name):
      VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
      
   def setUp(self):
       self._init_simulator_regression()
       self.sym_dict = self._symbol_dictionary()

##########################################################
# Documentation tests
#
# These tests illustrate how to use the class.
##########################################################

   def test_reminder(self):
       self.fail("remember to reactivate all other tests in SymDictTest")
      
   def ___test_this_is_how_you_create_a_SymDict(self):
       interp = SymDict.SymDict()
       
   def ___test_this_is_how_you_add_a_symbol_to_the_SymDict(self):
       self.sym_dict.add_symbol('ThisIsASymbol')
       
   def ___test_this_is_how_you_match_a_naturally_spoken_phrase_to_symbols_in_a_SymDict(self):
       sample_spoken_phrase = ['this', 'is', 'a', 'spoken', 'phrase']
       matches = self.sym_dict.match_phrase(sample_spoken_phrase)
       list_of_matching_symbols = matches[0]
       list_of_remaining_unmatched_words_in_spoken_phrase = matches[1]
              

##########################################################
# Unit tests
#
# These tests check the internal workings of the class.
##########################################################

   def ___test_match_pseudo_symbol(self):
       self.sym_dict.add_symbol('ThisIsASmb')
       
       # Example of use
       matches = self.sym_dict.match_pseudo_symbol('this is a symbol')
       good_matches = matches[0]
       weak_matches = matches[1]
       forbidden_matches = matches[2]
       self.assert_equal([(0.76719576719576721, 'ThisIsASmb')], 
                         good_matches, epsilon=0.01,
                         mess="Good matches were wrong for pseudo-symbol")
       self.assert_equal([], weak_matches, 
                         mess="Weak matches were wrong for pseudo-symbol")
       self.assert_equal([], forbidden_matches, 
                         mess="Forbidden matches were wrong for pseudo-symbol")
       
       # Testing match_pseudo_symbol() under varied conditions
       self.assert__match_pseudo_symbol__returns('', ([], [], []),
                "Matching pseudo-symbol failed for empty pseudo-symbol.")

   def test_delete_me_later(self):
       self.sym_dict.add_symbol('ThisIsASymbol')

       self.assert_phrase_matches(phrase=['this', 'is', 'a', 'symbol', 'but', 'not', 'this'],
                                  expected_matches=(['ThisIsASmb'], []),
                                  mess="Nevermind... I'm just trying to see how WordTrie.match_phrase works")
       

   def test_match_phrase(self):
       self.sym_dict.add_symbol('ThisIsASmb')

       self.assert_phrase_matches(phrase=['this', 'is', 'a', 'symbol'],
                                  expected_matches=(['ThisIsASmb'], []))
       
       self.assert_phrase_matches(phrase=['this', 'is', 'a', 'symbol', 'but', 'not', 'this'],
                                  expected_matches=(['ThisIsASmb'], ['but', 'not', 'this']))
       
   def test_fuzzy_match_phrase(self):
       self.sym_dict.add_symbol('a_known_smb')

       # Example of use
       phrase = ['a', 'known', 'symbol', 'equal', 'to', 'another', 'one']
       fuzzy_matches = self.sym_dict.fuzzy_match_phrase(phrase)
       self.assert_equal(([(0.65079365079365081, 'a_known_smb')], ['equal', 'to', 'another', 'one']),
                         fuzzy_matches,
                         epsilon=0.005,
                         mess="Fuzzy match of phrase %s to a symbol failed." % phrase)
       
       # Testing under different conditions
 
###############################################################
# Assertions.
# 
# Use these methods to check the state of the class.
###############################################################

   def assert_phrase_matches(self, phrase, expected_matches, mess=""):
       got_matches = self.sym_dict.match_phrase(phrase)
       mess = mess + "\nSymbol matches for phrase %s were wrong" % repr(phrase)
       self.assert_equal(expected_matches, got_matches, mess)
       
   def assert__match_pseudo_symbol__returns(self, pseudo_symbol,
          expected_matches, mess=""):
       matches = self.sym_dict.match_pseudo_symbol(pseudo_symbol)
       good_matches = matches[0]
       weak_matches = matches[1]
       forbidden_matches = matches[2]
       self.assert_equal(expected_matches[0], good_matches, epsilon=0.01,
                         mess="List of good symbol matches were wrong for pseudo-symbol '%s'" % pseudo_symbol)
       self.assert_equal(expected_matches[1], weak_matches, epsilon=0.01,
                         mess="List of weak symbol matches were wrong for pseudo-symbol '%s'" % pseudo_symbol)
       self.assert_equal(expected_matches[2], forbidden_matches, epsilon=0.01,
                         mess="List of forbidden symbol matches were wrong for pseudo-symbol '%s'" % pseudo_symbol)
