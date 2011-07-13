import debug
import VoiceCodeRootTest
import sr_interface

class SrInterfaceTest(VoiceCodeRootTest.VoiceCodeRootTest):
   def __init__(self, name):
      VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)

   def setUp(self):
       self._init_simulator_regression()
       self.getDragonVersion()
       
   def getDragonVersion(self):
      """report the Dragon version, being 10 (older) or 11 (newer)
      
      this influences the . after a single capital letter spoken form
      and a category included in each word, meaning double backslashes in a word
      """
      self.DragonVersion = 10
      if sr_interface.category_information_in_vocabulary_entries:
         self.DragonVersion = 11
         
   ##########################################################
   # Documentation tests
   #
   # These tests illustrate how to use the class.
   ##########################################################

   def ___test_reminder(self):
       pass
       #self.fail("remember to reactivate all other tests in SrInterfaceTest")
      
   def test_This_is_how_you_add_a_word_to_sr(self):
      self._open_empty_test_file('temp.py')
      self._insert_in_active_buffer("testing sr_interface")
      
      word = "testAddAWord"
      print 'exists %s: %s'% (word, sr_interface.word_exists(word))
      print 'add %s: %s'% (word, sr_interface.addWord(word))
      print 'exists %s: %s'% (word, sr_interface.word_exists(word))
      self._say([word])
      print 'delete %s: %s'% (word, sr_interface.deleteWord("testAddAWord"))
      print 'exists (deleted word) %s: %s'% (word, sr_interface.word_exists(word))
      self._say([word])
             
               
  
  ##########################################################
  # Unit tests
  #
  # These tests check the internal workings of the class.
  ##########################################################

   
  ###############################################################
  # Assertions.
  # 
  # Use these methods to check the state of the class.
  ###############################################################

