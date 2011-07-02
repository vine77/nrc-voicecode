import debug
import TestCaseWithHelpers
import vc_globals
import os
import re

mediator_used_for_testing = None

class VoiceCodeRootTest(TestCaseWithHelpers.TestCaseWithHelpers):
   """Root class for all VoiceCode PyUnit tests.

   It essentially defines some helper methods needed by most VoiceCode
   unit tests."""

   def __init__(self, name):
      TestCaseWithHelpers.TestCaseWithHelpers.__init__(self, name)
      
      self._set_automatic_buffer_printing(0)
      self.collect_data = [] # only for collect mode, see _say function and AcceptanceTests (PythonAcceptanceTest.py for example)
      self.collect_mode = 0
      self._test_data_file_pathes = {}
      for name in ['large_buff_py', 'lots_of_parens_py', 'lots_of_selections_py']:
          parts = name.split("_")
          self.assert_(len(parts) > 1)
          filename = '_'.join(parts[:-1])
          ext = parts[-1]
          full_path = os.path.join(vc_globals.test_data, filename + "." + ext)
##          print 'full_path: %s'% full_path
          self.assert_(os.path.isfile(full_path))
          self._test_data_file_pathes[name] = full_path
          self._test_data_file_pathes[name] = full_path
              
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
      
   def _say(self, utterance, user_input=None, never_bypass_sr_recog=0, echo_utterance=0, echo_cmd=0):
        """do an utterance, make collect_data mode possible for easier acceptance test setup...

        in that case (self.collect_mode is set to 1), the utterance and the buffer contents are printed to stdout,
        for later input in the test you are working on.

         Affects also   _assert_active_buffer_content_with_selection_is, because it is pypassed.
         Forget about _assert_active_buffer_content_is, with no selection on the result is identical, but
         with selection on the former one is better. (QH, july 2008)
   
        an utterance must be a list of words, but if a string is passed, this string is
        splitted into a list (by spaces)
        """
        if isinstance(utterance, basestring):
            if self.collect_mode:
                self.collect_data.append(' '*8 + 'self._say("%s")'% utterance)
            utterance = utterance.split()
        else:
            if self.collect_mode:
                self.collect_data.append(' '*8 + 'self._say(%s)'% utterance)
  
        self._commands().say(utterance, user_input, never_bypass_sr_recog, echo_utterance, echo_cmd)
  

   def _goto(self, pos):
      self._app().goto(pos)
      
   def _set_selection(self, range, cursor_at = 1):
      self._app().set_selection(range, cursor_at)
      
   def _open_empty_test_file(self, file_name):
       fpath = os.path.join(vc_globals.tmp, file_name)
       self._open_file(fpath)  
       self._app().delete_buffer_content()
       
   def _clear_active_buffer(self):
       self._app().delete_buffer_content()
      
   def _open_file(self, fpath):
      self._app().open_file(fpath)    
      
   def _insert_in_active_buffer(self, text):
       self._app().insert(text)
  
   def _init_simulator_regression(self, alt_sym_file = None, exclusive = 1, 
                                  print_buffer_content_after_commands=1):
      return self._mediator_testing_namespace(). \
                  init_simulator_regression(alt_sym_file, exclusive, 
                                  print_buffer_content_after_commands)
      
   def _mediator(self):
      global mediator_used_for_testing
      return mediator_used_for_testing
  
   def _command_interpreter(self):
      return self._mediator().interp
  
   def _symbol_dictionary(self):
      return self._command_interpreter().known_symbols
      
   def _goto(self, pos):
      return self._app().goto(pos)   

   def _goto_line(self, line_num, where=-1):
      return self._app().goto_line(line_num, where)   
      
   def _cur_pos(self):
      return self._app().cur_pos()

   def _active_buffer_name(self):
      return self._app().curr_buffer().name()

      
   def _get_text(self, start_pos, end_pos):
      return self._app().get_text(start_pos, end_pos)

   def _get_buffer_content_with_cursor_position(self, buff_name=None):
      got_content = self._app().find_buff(buff_name).contents()
      got_cur_pos = self._app().find_buff(buff_name).cur_pos()
      got_content = got_content[:got_cur_pos] + "<CURSOR>" + got_content[got_cur_pos:]      
      return got_content      

   def _get_buffer_content_with_selection_position(self, buff_name=None):
      got_content = self._app().find_buff(buff_name).contents()
      start, end = self._app().find_buff(buff_name).get_selection()
      if start > end:
         raise ValueError("test error, start > end: %s, %s"% (start, end))
      elif start == end:
         got_content = got_content[:start] + "<CURSOR>" + got_content[start:]
      else:
         got_content = got_content[:start] + "<SEL_START>" + got_content[start:end] + \
                            "<SEL_END>" + got_content[end:]
      return got_content      
      
   def _get_lines_with_selection_position(self, buff_name=None):
      start, end = self._app().find_buff(buff_name).get_selection()
      selected_lines, offset = self._app().find_buff(buff_name).get_text_of_selection()
      # make start, end relative to selected_lines
      start -= offset
      end -= offset
      if start > end:
         raise ValueError("test error, start > end: %s, %s"% (start, end))
      elif start == end:
         
         selected_lines = selected_lines[:start] + "<CURSOR>" + selected_lines[start:]
      else:
         selected_lines= selected_lines[:start] + "<SEL_START>" + selected_lines[start:end] + \
                            "<SEL_END>" + selected_lines[end:]
      return selected_lines
      
   def _len(self):
      return self._app().len()      
            
   def _assert_cursor_looking_at(self, exp_looking_at, direction=1, 
                                 message=""):
      start_pos = self._cur_pos()
      end_pos = start_pos + len(exp_looking_at)*direction
      debug.trace('VoiceCodeRootTest._assert_cursor_looking_at', 
                  '** exp_looking_at=%s, start_pos=%s, end_pos=%s' % 
                  (exp_looking_at, start_pos, end_pos))
      actually_looking_at = self._get_text(start_pos, end_pos)
      self.assert_equal(exp_looking_at, actually_looking_at,
             message +"At postion %s, expected to be looking at string '%s' in direction %s, but was actually looking at '%s'" %
             (start_pos, exp_looking_at, direction, actually_looking_at))
             
   def _assert_cur_pos_is(self, exp_pos, mess=""):
      got_pos = self._cur_pos()
      self.assert_equal(exp_pos, got_pos,  
                   mess + "Cursor was at the wrong place")
      
   def _assert_active_buffer_is_called(self, exp_name, mess=""):
      got_name = self._app().curr_buffer().name()
      mess = mess + "\nName of active buffer was wrong."
      self.assert_equal(exp_name, got_name, mess)
   
      
   def _assert_active_buffer_content_is(self, exp_content, mess=""):
      got_content = self._get_buffer_content_with_cursor_position()
      self.assert_equal(exp_content, got_content, 
                        mess + "\nContent of the active buffer was not as expected.")
         
   def _assert_active_buffer_content_with_selection_is(self, exp_content, mess=""):
        """bypass checking if collect_mode is on, only when setting up acceptance tests
        """
        if self.collect_mode:
            return
        got_content = self._get_buffer_content_with_selection_position()
        self.assert_equal(exp_content, got_content, 
                          mess + "\nContent of the active buffer was not as expected.")


   def _assert_current_line_content_is(self, expected_text, mess="",
                                       compare_as_regexp=False, regexp_flags=''):
      current_line_text = self._app().get_text_of_line() 
      cur_pos = self._app().cur_pos()
      start_of_line_pos = self._app().beginning_of_line()
      end_of_line_pos = self._app().beginning_of_line()
      before_cursor = current_line_text[:cur_pos - start_of_line_pos]
      after_cursor = current_line_text[cur_pos - start_of_line_pos:]
      got_text = before_cursor + '<CURSOR>' + after_cursor
      mess = mess + "\nContent of current line in the active buffer was wrong."
      if not compare_as_regexp:
         self.assert_equal(expected_text, got_text, mess)    
      else:
         mess = mess + "\nExpected to match regexp:\n'%s'\nGot:\n'%s'" % (expected_text, got_text)
         self.assert_(re.match(expected_text, got_text, regexp_flags), mess)
      
   def _assert_lines_with_selection_content_is(self, expected_text, mess="",
                                       compare_as_regexp=False, regexp_flags=''):

      got_text = self._get_lines_with_selection_position()
      mess = mess + "\nContent of selected lines in the active buffer was wrong."
      if not compare_as_regexp:
         self.assert_equal(expected_text, got_text, mess)    
      else:
         mess = mess + "\nExpected to match regexp:\n'%s'\nGot:\n'%s'" % (expected_text, got_text)
         self.assert_(re.match(expected_text, got_text, regexp_flags), mess)
      
   def _find_cur_pos_in_expected_translation(self, expected_translation):
       match = re.search("\\^", expected_translation)
       pos = match.start()
       expected_translation = re.sub("\\^", "", expected_translation)
       return pos

  