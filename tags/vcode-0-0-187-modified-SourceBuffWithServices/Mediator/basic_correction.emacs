
C:\eclipse\workspace\VCode\Mediator>rem  

C:\eclipse\workspace\VCode\Mediator>rem Shortcut for invoking VoiceCode server 

C:\eclipse\workspace\VCode\Mediator>rem

C:\eclipse\workspace\VCode\Mediator>c:

C:\eclipse\workspace\VCode\Mediator>cd C:\Eclipse\workspace\VCode\Mediator 

C:\eclipse\workspace\VCode\Mediator>python new_server.py -t basic_correction 
running ExtLoopWin32NewMediator with ServerNewMediator
running ExtLoopWin32NewMediator with ServerNewMediator
Loading test definitions...
Configuring the mediator...
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Finished ExtLoop init...
Running ExtLoopWin32...
Starting server threads...
Starting message loop...
-- send_mess: self=<messaging.MessengerBasic instance at 1897278>, mess_name='send_app_name'
-- send_mess: mess_argvals='{}'
-- get_mess: self=<messaging.MessengerBasic instance at 1897278>, expecting ['app_name']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('app_name', {'value': 'emacs'})
-- send_mess: self=<messaging.MessengerBasic instance at 1897278>, mess_name='your_id_is'
-- send_mess: mess_argvals='{'value': 'emacs_0.30766550938'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1897278>, expecting ['ok']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('ok', {})
-- send_mess: self=<messaging.MessengerBasic instance at 1897278>, mess_name='test_client_query'
-- send_mess: mess_argvals='{}'
-- get_mess: self=<messaging.MessengerBasic instance at 1897278>, expecting ['test_client_query_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('test_client_query_resp', {'value': 1.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1836f00>, mess_name='send_id'
-- send_mess: mess_argvals='{}'
-- get_mess: self=<messaging.MessengerBasic instance at 1836f00>, expecting ['my_id_is']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('my_id_is', {'value': 'emacs_0.30766550938'})
-- get_mess: self=<messaging.MessengerBasic instance at ba4c88>, expecting None
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='set_instance_string'
-- send_mess: mess_argvals='{'instance_string': '(Yak 0)'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['set_instance_string_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('set_instance_string_resp', {'value': '(Yak 0)'})
universal instance named "emacs(0)"
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='list_open_buffers'
-- send_mess: mess_argvals='{}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['list_open_buffers_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('list_open_buffers_resp', {'value': [' *Minibuf-1*', '*scratch*', '*Messages*']})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='close_buffer'
-- send_mess: mess_argvals='{'save': 0, 'buff_name': ' *Minibuf-1*'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['close_buffer_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('close_buffer_resp', {'value': 1.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='confirm_buffer_exists'
-- send_mess: mess_argvals='{'buff_name': ' *Minibuf-1*'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['confirm_buffer_exists_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('confirm_buffer_exists_resp', {'value': 1.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='close_buffer'
-- send_mess: mess_argvals='{'save': 0, 'buff_name': '*scratch*'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['close_buffer_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('updates', {'buff_name': ' *Minibuf-1*', 'action': 'close_buff'})
-- get_mess: self=<messaging.MessengerBasic instance at ba4c88>, expecting None
-- get_mess: got it!
-- get_mess: name_argvals_mess=('close_buffer_resp', {'value': 1.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='confirm_buffer_exists'
-- send_mess: mess_argvals='{'buff_name': '*scratch*'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['confirm_buffer_exists_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('confirm_buffer_exists_resp', {'value': 0.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='close_buffer'
-- send_mess: mess_argvals='{'save': 0, 'buff_name': '*Messages*'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['close_buffer_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('close_buffer_resp', {'value': 1.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='confirm_buffer_exists'
-- send_mess: mess_argvals='{'buff_name': '*Messages*'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['confirm_buffer_exists_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('confirm_buffer_exists_resp', {'value': 1.0})


*******************************************************************************
* Name        : basic_correction
* Description : Testing basic correction infrastructure with ResMgr.
*******************************************************************************

Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='list_open_buffers'
-- send_mess: mess_argvals='{}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['list_open_buffers_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('list_open_buffers_resp', {'value': [' *Minibuf-1*', '*scratch*', '*Messages*']})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='close_buffer'
-- send_mess: mess_argvals='{'save': -1, 'buff_name': ' *Minibuf-1*'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['close_buffer_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('close_buffer_resp', {'value': 1.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='confirm_buffer_exists'
-- send_mess: mess_argvals='{'buff_name': ' *Minibuf-1*'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['confirm_buffer_exists_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('confirm_buffer_exists_resp', {'value': 1.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='close_buffer'
-- send_mess: mess_argvals='{'save': -1, 'buff_name': '*scratch*'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['close_buffer_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('close_buffer_resp', {'value': 1.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='confirm_buffer_exists'
-- send_mess: mess_argvals='{'buff_name': '*scratch*'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['confirm_buffer_exists_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('confirm_buffer_exists_resp', {'value': 1.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='close_buffer'
-- send_mess: mess_argvals='{'save': -1, 'buff_name': '*Messages*'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['close_buffer_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('close_buffer_resp', {'value': 1.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='confirm_buffer_exists'
-- send_mess: mess_argvals='{'buff_name': '*Messages*'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['confirm_buffer_exists_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('confirm_buffer_exists_resp', {'value': 1.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='open_file'
-- send_mess: mess_argvals='{'file_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['open_file_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('open_file_resp', {'buff_name': 'blah.py'})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='file_name'
-- send_mess: mess_argvals='{'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['file_name_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('file_name_resp', {'value': 'c:/eclipse/workspace/VCode/Environments/Emacs/blah.py'})
WARNING: source file 'blah.py' doesn't exist.
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='active_buffer_name'
-- send_mess: mess_argvals='{}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['active_buffer_name_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('active_buffer_name_resp', {'value': 'blah.py'})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='cur_pos'
-- send_mess: mess_argvals='{'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['cur_pos_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('cur_pos_resp', {'value': 0.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='line_num_of'
-- send_mess: mess_argvals='{'buff_name': 'blah.py', 'position': 0}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['line_num_of_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('line_num_of_resp', {'value': 1.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='get_text'
-- send_mess: mess_argvals='{'end': None, 'buff_name': 'blah.py', 'start': None}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['get_text_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('get_text_resp', {'value': ''})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='line_num_of'
-- send_mess: mess_argvals='{'buff_name': 'blah.py', 'position': 0}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['line_num_of_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('line_num_of_resp', {'value': 1.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='get_selection'
-- send_mess: mess_argvals='{'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['get_selection_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('get_selection_resp', {'value': [0.0, 0.0]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='newline_conventions'
-- send_mess: mess_argvals='{'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['newline_conventions_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('newline_conventions_resp', {'value': ['\012']})
*** Start of source buffer ***
  1: <CURSOR>

*** End of source buffer ***

***Testing initial state***


0 stored utterances, as expected


recent dictation is empty, as expected


***Some simple dictation***



>>> Testing console command: say(['class', 'clown', 'inherits', 'from', 'student'], user_input='0
0
')
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='active_buffer_name'
-- send_mess: mess_argvals='{}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['active_buffer_name_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('active_buffer_name_resp', {'value': 'blah.py'})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='recog_begin'
-- send_mess: mess_argvals='{'block': 0, 'window_id': None}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['recog_begin_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('recog_begin_resp', {'value': 1.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='get_visible'
-- send_mess: mess_argvals='{'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['get_visible_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('get_visible_resp', {'value': [1.0, 1.0]})
-- BasicCorrectionWinGramNL.activate: received activate
-- BasicCorrectionWinGramNL.activate: not already active
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='confirm_buffer_exists'
-- send_mess: mess_argvals='{'buff_name': 'c:/eclipse/workspace/VCode/Environments/Emacs/blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['confirm_buffer_exists_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('confirm_buffer_exists_resp', {'value': 0.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='confirm_buffer_exists'
-- send_mess: mess_argvals='{'buff_name': 'c:/eclipse/workspace/VCode/Environments/Emacs/blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['confirm_buffer_exists_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('confirm_buffer_exists_resp', {'value': 0.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='set_selection'
-- send_mess: mess_argvals='{'cursor_at': 1, 'buff_name': 'blah.py', 'range': [0, 0]}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['set_selection_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('set_selection_resp', {'updates': [{'cursor_at': 1.0, 'range': [0.0, 0.0], 'buff_name': 'blah.py', 'action': 'select'}]})
-- ResMgrBasic.interpret_dictation: about to interpret
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='list_open_buffers'
-- send_mess: mess_argvals='{}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['list_open_buffers_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('list_open_buffers_resp', {'value': ['blah.py', ' *Minibuf-1*', '*scratch*', '*Messages*']})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='confirm_buffer_exists'
-- send_mess: mess_argvals='{'buff_name': ' *Minibuf-1*'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['confirm_buffer_exists_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('confirm_buffer_exists_resp', {'value': 1.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='get_text'
-- send_mess: mess_argvals='{'end': None, 'buff_name': ' *Minibuf-1*', 'start': None}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['get_text_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('get_text_resp', {'value': ''})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='get_selection'
-- send_mess: mess_argvals='{'buff_name': ' *Minibuf-1*'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['get_selection_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('get_selection_resp', {'value': [0.0, 0.0]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='confirm_buffer_exists'
-- send_mess: mess_argvals='{'buff_name': '*scratch*'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['confirm_buffer_exists_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('confirm_buffer_exists_resp', {'value': 1.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='get_text'
-- send_mess: mess_argvals='{'end': None, 'buff_name': '*scratch*', 'start': None}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['get_text_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('get_text_resp', {'value': ''})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='get_selection'
-- send_mess: mess_argvals='{'buff_name': '*scratch*'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['get_selection_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('get_selection_resp', {'value': [0.0, 0.0]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='confirm_buffer_exists'
-- send_mess: mess_argvals='{'buff_name': '*Messages*'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['confirm_buffer_exists_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('confirm_buffer_exists_resp', {'value': 1.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='get_text'
-- send_mess: mess_argvals='{'end': None, 'buff_name': '*Messages*', 'start': None}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['get_text_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('get_text_resp', {'value': ''})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='get_selection'
-- send_mess: mess_argvals='{'buff_name': '*Messages*'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['get_selection_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('get_selection_resp', {'value': [0.0, 0.0]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='insert'
-- send_mess: mess_argvals='{'range': (0, 0), 'buff_name': 'blah.py', 'text': 'class '}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['insert_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('insert_resp', {'updates': [{'buff_name': 'blah.py', 'range': [0.0, 0.0], 'text': 'class ', 'action': 'insert'}]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='cur_pos'
-- send_mess: mess_argvals='{'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['cur_pos_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('cur_pos_resp', {'value': 6.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='indent'
-- send_mess: mess_argvals='{'range': (0, 6), 'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['indent_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('indent_resp', {'updates': []})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='insert'
-- send_mess: mess_argvals='{'range': (6, 6), 'buff_name': 'blah.py', 'text': ':\012'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['insert_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('insert_resp', {'updates': [{'buff_name': 'blah.py', 'range': [6.0, 6.0], 'text': ':\012', 'action': 'insert'}]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='cur_pos'
-- send_mess: mess_argvals='{'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['cur_pos_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('cur_pos_resp', {'value': 8.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='indent'
-- send_mess: mess_argvals='{'range': (6, 8), 'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['indent_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('indent_resp', {'updates': []})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='goto'
-- send_mess: mess_argvals='{'buff_name': 'blah.py', 'pos': 6}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['goto_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('goto_resp', {'updates': [{'cursor_at': 1.0, 'range': [6.0, 6.0], 'buff_name': 'blah.py', 'action': 'select'}]})
Associate 'clown' with symbol (Enter selection):

  '0': no association
  '1': clown (*new*)
  '2': Clown (*new*)
  '3': CLOWN (*new*)

> -- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='insert'
-- send_mess: mess_argvals='{'range': (6, 6), 'buff_name': 'blah.py', 'text': 'clown'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['insert_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('insert_resp', {'updates': [{'buff_name': 'blah.py', 'range': [6.0, 6.0], 'text': 'clown', 'action': 'insert'}]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='cur_pos'
-- send_mess: mess_argvals='{'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['cur_pos_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('cur_pos_resp', {'value': 11.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='indent'
-- send_mess: mess_argvals='{'range': (6, 11), 'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['indent_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('indent_resp', {'updates': []})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='get_selection'
-- send_mess: mess_argvals='{'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['get_selection_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('get_selection_resp', {'value': [11.0, 11.0]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='insert'
-- send_mess: mess_argvals='{'range': (11, 11), 'buff_name': 'blah.py', 'text': '('}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['insert_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('insert_resp', {'updates': [{'buff_name': 'blah.py', 'range': [11.0, 11.0], 'text': '(', 'action': 'insert'}]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='cur_pos'
-- send_mess: mess_argvals='{'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['cur_pos_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('cur_pos_resp', {'value': 12.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='indent'
-- send_mess: mess_argvals='{'range': (11, 12), 'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['indent_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('indent_resp', {'updates': []})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='insert'
-- send_mess: mess_argvals='{'range': (12, 12), 'buff_name': 'blah.py', 'text': ')'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['insert_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('insert_resp', {'updates': [{'buff_name': 'blah.py', 'range': [12.0, 12.0], 'text': ')', 'action': 'insert'}]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='cur_pos'
-- send_mess: mess_argvals='{'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['cur_pos_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('cur_pos_resp', {'value': 13.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='indent'
-- send_mess: mess_argvals='{'range': (12, 13), 'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['indent_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('indent_resp', {'updates': []})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='goto'
-- send_mess: mess_argvals='{'buff_name': 'blah.py', 'pos': 12}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['goto_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('goto_resp', {'updates': [{'cursor_at': 1.0, 'range': [12.0, 12.0], 'buff_name': 'blah.py', 'action': 'select'}]})
Associate 'student' with symbol (Enter selection):

  '0': no association
  '1': student (*new*)
  '2': Student (*new*)
  '3': STUDENT (*new*)

> -- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='insert'
-- send_mess: mess_argvals='{'range': (12, 12), 'buff_name': 'blah.py', 'text': 'student'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['insert_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('insert_resp', {'updates': [{'buff_name': 'blah.py', 'range': [12.0, 12.0], 'text': 'student', 'action': 'insert'}]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='cur_pos'
-- send_mess: mess_argvals='{'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['cur_pos_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('cur_pos_resp', {'value': 19.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='indent'
-- send_mess: mess_argvals='{'range': (12, 19), 'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['indent_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('indent_resp', {'updates': []})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='recog_end'
-- send_mess: mess_argvals='{}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['recog_end_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('recog_end_resp', {})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='list_open_buffers'
-- send_mess: mess_argvals='{}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['list_open_buffers_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('list_open_buffers_resp', {'value': ['blah.py', ' *Minibuf-1*', '*scratch*', '*Messages*']})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='get_selection'
-- send_mess: mess_argvals='{'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['get_selection_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('get_selection_resp', {'value': [19.0, 19.0]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='line_num_of'
-- send_mess: mess_argvals='{'buff_name': 'blah.py', 'position': 19}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['line_num_of_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('line_num_of_resp', {'value': 1.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='line_num_of'
-- send_mess: mess_argvals='{'buff_name': 'blah.py', 'position': 22}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['line_num_of_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('line_num_of_resp', {'value': 2.0})
*** Start of source buffer ***
  1: class clown(student<CURSOR>):
  2: 

*** End of source buffer ***
-- ResMgrBasic.store: storing an utterance (already have 0)


>>> Testing console command: say(['class', 'body'], user_input='')
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='active_buffer_name'
-- send_mess: mess_argvals='{}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['active_buffer_name_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('active_buffer_name_resp', {'value': 'blah.py'})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='recog_begin'
-- send_mess: mess_argvals='{'block': 0, 'window_id': None}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['recog_begin_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('recog_begin_resp', {'value': 1.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='get_visible'
-- send_mess: mess_argvals='{'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['get_visible_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('get_visible_resp', {'value': [1.0, 23.0]})
-- BasicCorrectionWinGramNL.activate: received activate
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='goto'
-- send_mess: mess_argvals='{'buff_name': 'blah.py', 'pos': 5}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['goto_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('goto_resp', {'updates': [{'cursor_at': 1.0, 'range': [5.0, 5.0], 'buff_name': 'blah.py', 'action': 'select'}]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='confirm_buffer_exists'
-- send_mess: mess_argvals='{'buff_name': 'c:/eclipse/workspace/VCode/Environments/Emacs/blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['confirm_buffer_exists_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('confirm_buffer_exists_resp', {'value': 0.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='goto'
-- send_mess: mess_argvals='{'buff_name': 'blah.py', 'pos': 22}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['goto_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('goto_resp', {'updates': [{'cursor_at': 1.0, 'range': [22.0, 22.0], 'buff_name': 'blah.py', 'action': 'select'}]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='confirm_buffer_exists'
-- send_mess: mess_argvals='{'buff_name': 'c:/eclipse/workspace/VCode/Environments/Emacs/blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['confirm_buffer_exists_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('confirm_buffer_exists_resp', {'value': 0.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='set_selection'
-- send_mess: mess_argvals='{'cursor_at': 1, 'buff_name': 'blah.py', 'range': [19, 19]}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['set_selection_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('set_selection_resp', {'updates': [{'cursor_at': 1.0, 'range': [19.0, 19.0], 'buff_name': 'blah.py', 'action': 'select'}]})
-- ResMgrBasic.interpret_dictation: about to interpret
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='list_open_buffers'
-- send_mess: mess_argvals='{}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['list_open_buffers_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('list_open_buffers_resp', {'value': ['blah.py', ' *Minibuf-1*', '*scratch*', '*Messages*']})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='goto'
-- send_mess: mess_argvals='{'buff_name': 'blah.py', 'pos': 22}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['goto_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('goto_resp', {'updates': [{'cursor_at': 1.0, 'range': [22.0, 22.0], 'buff_name': 'blah.py', 'action': 'select'}]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='recog_end'
-- send_mess: mess_argvals='{}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['recog_end_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('recog_end_resp', {})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='list_open_buffers'
-- send_mess: mess_argvals='{}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['list_open_buffers_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('list_open_buffers_resp', {'value': ['blah.py', ' *Minibuf-1*', '*scratch*', '*Messages*']})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='line_num_of'
-- send_mess: mess_argvals='{'buff_name': 'blah.py', 'position': 22}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['line_num_of_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('line_num_of_resp', {'value': 2.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='line_num_of'
-- send_mess: mess_argvals='{'buff_name': 'blah.py', 'position': 22}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['line_num_of_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('line_num_of_resp', {'value': 2.0})
*** Start of source buffer ***
  1: class clown(student):
  2: <CURSOR>

*** End of source buffer ***
-- ResMgrBasic.store: storing an utterance (already have 1)


>>> Testing console command: say(['define', 'method', 'popularity', 'method', 'body'], user_input='0
')
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='active_buffer_name'
-- send_mess: mess_argvals='{}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['active_buffer_name_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('active_buffer_name_resp', {'value': 'blah.py'})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='recog_begin'
-- send_mess: mess_argvals='{'block': 0, 'window_id': None}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['recog_begin_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('recog_begin_resp', {'value': 1.0})
-- BasicCorrectionWinGramNL.activate: received activate
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='goto'
-- send_mess: mess_argvals='{'buff_name': 'blah.py', 'pos': 5}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['goto_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('goto_resp', {'updates': [{'cursor_at': 1.0, 'range': [5.0, 5.0], 'buff_name': 'blah.py', 'action': 'select'}]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='confirm_buffer_exists'
-- send_mess: mess_argvals='{'buff_name': 'c:/eclipse/workspace/VCode/Environments/Emacs/blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['confirm_buffer_exists_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('confirm_buffer_exists_resp', {'value': 0.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='goto'
-- send_mess: mess_argvals='{'buff_name': 'blah.py', 'pos': 22}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['goto_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('goto_resp', {'updates': [{'cursor_at': 1.0, 'range': [22.0, 22.0], 'buff_name': 'blah.py', 'action': 'select'}]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='confirm_buffer_exists'
-- send_mess: mess_argvals='{'buff_name': 'c:/eclipse/workspace/VCode/Environments/Emacs/blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['confirm_buffer_exists_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('confirm_buffer_exists_resp', {'value': 0.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='set_selection'
-- send_mess: mess_argvals='{'cursor_at': 1, 'buff_name': 'blah.py', 'range': [22, 22]}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['set_selection_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('set_selection_resp', {'updates': [{'cursor_at': 1.0, 'range': [22.0, 22.0], 'buff_name': 'blah.py', 'action': 'select'}]})
-- ResMgrBasic.interpret_dictation: about to interpret
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='list_open_buffers'
-- send_mess: mess_argvals='{}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['list_open_buffers_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('list_open_buffers_resp', {'value': ['blah.py', ' *Minibuf-1*', '*scratch*', '*Messages*']})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='insert'
-- send_mess: mess_argvals='{'range': (22, 22), 'buff_name': 'blah.py', 'text': 'def '}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['insert_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('insert_resp', {'updates': [{'buff_name': 'blah.py', 'range': [22.0, 22.0], 'text': 'def ', 'action': 'insert'}]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='cur_pos'
-- send_mess: mess_argvals='{'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['cur_pos_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('cur_pos_resp', {'value': 26.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='indent'
-- send_mess: mess_argvals='{'range': (22, 26), 'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['indent_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('indent_resp', {'updates': []})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='insert'
-- send_mess: mess_argvals='{'range': (26, 26), 'buff_name': 'blah.py', 'text': '(self):\012'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['insert_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('insert_resp', {'updates': [{'buff_name': 'blah.py', 'range': [26.0, 26.0], 'text': '(self):\012', 'action': 'insert'}]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='cur_pos'
-- send_mess: mess_argvals='{'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['cur_pos_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('cur_pos_resp', {'value': 34.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='indent'
-- send_mess: mess_argvals='{'range': (26, 34), 'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['indent_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('indent_resp', {'updates': []})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='goto'
-- send_mess: mess_argvals='{'buff_name': 'blah.py', 'pos': 26}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['goto_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('goto_resp', {'updates': [{'cursor_at': 1.0, 'range': [26.0, 26.0], 'buff_name': 'blah.py', 'action': 'select'}]})
Associate 'popularity' with symbol (Enter selection):

  '0': no association
  '1': popularity (*new*)
  '2': Popularity (*new*)
  '3': POPULARITY (*new*)

> -- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='insert'
-- send_mess: mess_argvals='{'range': (26, 26), 'buff_name': 'blah.py', 'text': 'popularity'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['insert_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('insert_resp', {'updates': [{'buff_name': 'blah.py', 'range': [26.0, 26.0], 'text': 'popularity', 'action': 'insert'}]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='cur_pos'
-- send_mess: mess_argvals='{'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['cur_pos_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('cur_pos_resp', {'value': 36.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='indent'
-- send_mess: mess_argvals='{'range': (26, 36), 'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['indent_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('indent_resp', {'updates': []})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='goto'
-- send_mess: mess_argvals='{'buff_name': 'blah.py', 'pos': 44}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['goto_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('goto_resp', {'updates': [{'cursor_at': 1.0, 'range': [44.0, 44.0], 'buff_name': 'blah.py', 'action': 'select'}]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='recog_end'
-- send_mess: mess_argvals='{}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['recog_end_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('recog_end_resp', {})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='list_open_buffers'
-- send_mess: mess_argvals='{}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['list_open_buffers_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('list_open_buffers_resp', {'value': ['blah.py', ' *Minibuf-1*', '*scratch*', '*Messages*']})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='line_num_of'
-- send_mess: mess_argvals='{'buff_name': 'blah.py', 'position': 44}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['line_num_of_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('line_num_of_resp', {'value': 3.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='line_num_of'
-- send_mess: mess_argvals='{'buff_name': 'blah.py', 'position': 44}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['line_num_of_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('line_num_of_resp', {'value': 3.0})
*** Start of source buffer ***
  1: class clown(student):
  2: def popularity(self):
  3: <CURSOR>

*** End of source buffer ***
-- ResMgrBasic.store: storing an utterance (already have 2)


>>> Testing console command: say(['return', '8'], user_input='')
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='active_buffer_name'
-- send_mess: mess_argvals='{}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['active_buffer_name_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('active_buffer_name_resp', {'value': 'blah.py'})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='recog_begin'
-- send_mess: mess_argvals='{'block': 0, 'window_id': None}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['recog_begin_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('recog_begin_resp', {'value': 1.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='get_visible'
-- send_mess: mess_argvals='{'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['get_visible_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('get_visible_resp', {'value': [1.0, 45.0]})
-- BasicCorrectionWinGramNL.activate: received activate
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='goto'
-- send_mess: mess_argvals='{'buff_name': 'blah.py', 'pos': 21}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['goto_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('goto_resp', {'updates': [{'cursor_at': 1.0, 'range': [21.0, 21.0], 'buff_name': 'blah.py', 'action': 'select'}]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='confirm_buffer_exists'
-- send_mess: mess_argvals='{'buff_name': 'c:/eclipse/workspace/VCode/Environments/Emacs/blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['confirm_buffer_exists_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('confirm_buffer_exists_resp', {'value': 0.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='goto'
-- send_mess: mess_argvals='{'buff_name': 'blah.py', 'pos': 44}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['goto_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('goto_resp', {'updates': [{'cursor_at': 1.0, 'range': [44.0, 44.0], 'buff_name': 'blah.py', 'action': 'select'}]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='confirm_buffer_exists'
-- send_mess: mess_argvals='{'buff_name': 'c:/eclipse/workspace/VCode/Environments/Emacs/blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['confirm_buffer_exists_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('confirm_buffer_exists_resp', {'value': 0.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='set_selection'
-- send_mess: mess_argvals='{'cursor_at': 1, 'buff_name': 'blah.py', 'range': [44, 44]}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['set_selection_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('set_selection_resp', {'updates': [{'cursor_at': 1.0, 'range': [44.0, 44.0], 'buff_name': 'blah.py', 'action': 'select'}]})
-- ResMgrBasic.interpret_dictation: about to interpret
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='list_open_buffers'
-- send_mess: mess_argvals='{}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['list_open_buffers_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('list_open_buffers_resp', {'value': ['blah.py', ' *Minibuf-1*', '*scratch*', '*Messages*']})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='insert'
-- send_mess: mess_argvals='{'range': (44, 44), 'buff_name': 'blah.py', 'text': 'return '}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['insert_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('insert_resp', {'updates': [{'buff_name': 'blah.py', 'range': [44.0, 44.0], 'text': 'return ', 'action': 'insert'}]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='cur_pos'
-- send_mess: mess_argvals='{'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['cur_pos_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('cur_pos_resp', {'value': 51.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='indent'
-- send_mess: mess_argvals='{'range': (44, 51), 'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['indent_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('indent_resp', {'updates': []})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='get_selection'
-- send_mess: mess_argvals='{'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['get_selection_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('get_selection_resp', {'value': [51.0, 51.0]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='insert'
-- send_mess: mess_argvals='{'range': (51, 51), 'buff_name': 'blah.py', 'text': '8'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['insert_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('insert_resp', {'updates': [{'buff_name': 'blah.py', 'range': [51.0, 51.0], 'text': '8', 'action': 'insert'}]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='cur_pos'
-- send_mess: mess_argvals='{'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['cur_pos_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('cur_pos_resp', {'value': 52.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='indent'
-- send_mess: mess_argvals='{'range': (51, 52), 'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['indent_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('indent_resp', {'updates': []})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='recog_end'
-- send_mess: mess_argvals='{}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['recog_end_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('recog_end_resp', {})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='list_open_buffers'
-- send_mess: mess_argvals='{}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['list_open_buffers_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('list_open_buffers_resp', {'value': ['blah.py', ' *Minibuf-1*', '*scratch*', '*Messages*']})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='get_selection'
-- send_mess: mess_argvals='{'buff_name': 'blah.py'}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['get_selection_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('get_selection_resp', {'value': [52.0, 52.0]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='line_num_of'
-- send_mess: mess_argvals='{'buff_name': 'blah.py', 'position': 52}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['line_num_of_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('line_num_of_resp', {'value': 3.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='line_num_of'
-- send_mess: mess_argvals='{'buff_name': 'blah.py', 'position': 52}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['line_num_of_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('line_num_of_resp', {'value': 3.0})
*** Start of source buffer ***
  1: class clown(student):
  2: def popularity(self):
  3: return 8<CURSOR>

*** End of source buffer ***
-- ResMgrBasic.store: storing an utterance (already have 3)

***Testing state***


4 stored utterances, as expected

-- get_mess: self=<messaging.MixedMessenger instance at 199cca0>, expecting ['updates', 'suspended', 'resuming', 'editor_disconnecting', 'connection_broken']

WARNING: 0 recently dictated utterances (expected 4)
-- get_mess: self=<messaging.MixedMessenger instance at 199cca0>, expecting ['updates', 'suspended', 'resuming', 'editor_disconnecting', 'connection_broken']
-- ResMgrBasic.recent_dictation: safe depth = 4

***Testing scratch that***

scratching 1

-- RSMInfrastructure.scratch_recent: instance emacs(0)
-- ResMgrBasic.scratch_recent: attempting to scratch n = 1
-- get_mess: self=<messaging.MixedMessenger instance at 199cca0>, expecting ['updates', 'suspended', 'resuming', 'editor_disconnecting', 'connection_broken']
-- get_mess: self=<messaging.MixedMessenger instance at 199cca0>, expecting ['updates', 'suspended', 'resuming', 'editor_disconnecting', 'connection_broken']
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='list_open_buffers'
-- send_mess: mess_argvals='{}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['list_open_buffers_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('list_open_buffers_resp', {'value': ['blah.py', ' *Minibuf-1*', '*scratch*', '*Messages*']})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='set_text'
-- send_mess: mess_argvals='{'end': None, 'buff_name': 'blah.py', 'text': 'class clown(student):\012def popularity(self):\012return 8', 'start': None}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['set_text_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('set_text_resp', {'updates': [{'buff_name': 'blah.py', 'range': [0.0, 52.0], 'text': '', 'action': 'insert'}, {'buff_name': 'blah.py', 'range': [0.0, 0.0], 'text': 'class clown(student):\012def popularity(self):\012return 8', 'action': 'insert'}]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='set_selection'
-- send_mess: mess_argvals='{'cursor_at': 1, 'buff_name': 'blah.py', 'range': [52, 52]}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['set_selection_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('set_selection_resp', {'updates': [{'cursor_at': 1.0, 'range': [52.0, 52.0], 'buff_name': 'blah.py', 'action': 'select'}]})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='line_num_of'
-- send_mess: mess_argvals='{'buff_name': 'blah.py', 'position': 52}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['line_num_of_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('line_num_of_resp', {'value': 3.0})
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='line_num_of'
-- send_mess: mess_argvals='{'buff_name': 'blah.py', 'position': 52}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['line_num_of_resp']
-- get_mess: got it!
-- get_mess: name_argvals_mess=('line_num_of_resp', {'value': 3.0})
*** Start of source buffer ***
  1: class clown(student):
  2: def popularity(self):
  3: return 8<CURSOR>

*** End of source buffer ***
-- send_mess: self=<messaging.MessengerBasic instance at 1992730>, mess_name='set_text'
-- send_mess: mess_argvals='{'end': None, 'buff_name': ' *Minibuf-1*', 'text': '', 'start': None}'
-- get_mess: self=<messaging.MessengerBasic instance at 1992730>, expecting ['set_text_resp']
