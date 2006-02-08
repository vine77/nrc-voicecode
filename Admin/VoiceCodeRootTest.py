import debug
import TestCaseWithHelpers
import vc_globals
import os

mediator_used_for_testing = None

class VoiceCodeRootTest(TestCaseWithHelpers.TestCaseWithHelpers):
   """Root class for all VoiceCode PyUnit tests.

   It essentially defines some helper methods needed by most VoiceCode
   unit tests."""

   def __init__(self, name):
      TestCaseWithHelpers.TestCaseWithHelpers.__init__(self, name)
      
      self._set_automatic_buffer_printing(0)
      
      self._test_data_file_pathes = \
              {
               'large_buff_py': vc_globals.test_data + os.sep + 'large_buff.py'
              }
              
   def __del__(self):              
      self._set_automatic_buffer_printing(1)      
      
   def _set_automatic_buffer_printing(self, state=0):   
      app_mgr = self._mediator().editors
      for an_app in app_mgr.instances.values():
         an_app.print_buff_when_changed = state
      
   def _get_test_data_file_path(self, file_name):
      return self._test_data_file_pathes[file_name]
      
   def _mediator_testing_namespace(self):
      return self._mediator().test_space["testing"]
      
   def _app(self):
    instance_name = self._mediator_testing_namespace().instance_name()
    app = self._mediator().editors.app_instance(instance_name)
    return app

      
   def _commands(self):
      debug.trace('VoiceCodeRootTest._commands', 'self._mediator_testing_namespace=%s' % self._mediator_testing_namespace())
      return  self._mediator_testing_namespace().namespace()['commands'] 
      
   def _say(self, utterance):
      self._commands().say(utterance)
      
   def _open_file(self, fpath):
      self._commands().open_file(fpath)    
  
   def _init_simulator_regression(self):
      return self._mediator_testing_namespace().init_simulator_regression()
      
   def _mediator(self):
      global mediator_used_for_testing
      return mediator_used_for_testing
      