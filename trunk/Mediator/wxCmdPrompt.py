"""concrete implementation of CmdPromptWithHistory using wxPython
wxTextCtrl."""

# (C)2000 David C. Fox

import debug
from Object import Object
from CmdPrompt import *
from wxPython.wx import *

class wxCmdPromptWithHistory(CmdPromptWithHistory):
    """concrete implementation of CmdPromptWithHistory using a single
    line wxTextCtrl.  Up and down arrows move through the history,
    and enter enters the currently edited command.

    Note: to receive notification that a command has been entered, the
    command_callback argument must be supplied to CmdPrompt.

    **INSTANCE ATTRIBUTES**

    *wxTextCtrl* text -- underlying wxTextCtrl 

    *STR* stored -- storage for partially edited command line buffer
    when we move back through the command history.

    *(INT, INT)* stored_selection -- storage for current selection in 
    partially edited command line buffer when we move back through 
    the command history.

    **CLASS ATTRIBUTES**
    
    *none* --
    """
    def __init__(self, underlying, **args):
	"""
	**INPUTS**

	*wxTextCtrl* underlying -- existing wxTextCtrl.  Must have
	wxTE_PROCESS_ENTER style, and be a single line control 
	(not wxTE_MULTILINE)
	"""

	self.deep_construct(wxCmdPromptWithHistory,
	    {"stored": "",
	    "stored_selection": (0, 0),
	    "text": underlying},
	    args)

	EVT_TEXT_ENTER(self.text, self.text.GetId(), self._on_command_enter)
	EVT_CHAR(self.text, self._on_command_char)

    def _on_command_char(self, key_event):
	"""internal command to handle wxWindows key events

	**INPUTS**

	*wxKeyEvent* key_event -- the wxKeyEvent which triggered this
	handler.

	**OUTPUTS**

	*none*
	"""
    
	code = key_event.GetKeyCode()
	if code == WXK_UP:
	    new_buffer = self.previous()
	    if new_buffer != None:
		self.text.SetValue(new_buffer)
		self.text.SetInsertionPointEnd()
	elif code == WXK_DOWN:
	    new_buffer = self.next()
	    if new_buffer != None:
		self.text.SetValue(new_buffer)
		self.text.SetInsertionPointEnd()
	else:
# ignore other keys, allowing the default wxTextCtrl processing to proceed
	    key_event.Skip()

    def _on_command_enter(self, event):
	"""internal command to handle wxWindows 
	wxEVT_COMMAND_TEXT_ENTER events

	**INPUTS**

	*wxEvent* event -- the event which triggered this handler.

	**OUTPUTS**

	*none*
	"""
	command = self.text.GetValue()
	self.text.SetValue("")
	self._on_command(command)

    def save_edited(self):
	"""store partially edited new command.

	**INPUT**

	*none*

	**OUTPUT**

	*none*
	"""
	self.stored = self.text.GetValue()
	self.stored_selection = self.text.GetSelection()

    def restore_edited(self):
	"""restore previously saved partially edited new command.

	**INPUT**

	*none*

	**OUTPUT**

	*none*
	"""
	self.text.SetValue(self.stored)
	self.text.SetSelection(self.stored_selection[0],
	    self.stored_selection[1])

    def edited(self):
	"""contents of saved command line past the last command in the
	stack, if it has previously been saved. 
	Unlike restore_edited, this method returns only the string
	contents in the saved command line.
    
	**INPUT**

	*none*

	**OUTPUTS**

	*STR* -- partial command previously stored with save_edited, 
	or None if there is none.
	"""
	return self.stored

    def in_progress(self):
	"""contents of command line currently being edited (not the one
	stored by save_edited)
	A concrete subclass of CmdPromptWithHistory must define this method.
      
	**INPUT**

	*none*

	**OUTPUTS**

	*STR* -- partial command currently being edited
	"""
	return self.text.GetValue()


class wxCmdLog(CmdLog):
    """concrete implementation of CmdLog using a wxTextCtrl.  

    **INSTANCE ATTRIBUTES**

    *wxTextCtrl* log - underlying wxTextCtrl log window

    **CLASS ATTRIBUTES**
    
    *none* --
    """
    def __init__(self, underlying_text, **args):
	"""
	**INPUTS**

	*wxTextCtrl* underlying_text - underlying wxTextCtrl log window.
	Should be READ_ONLY
	"""
        self.deep_construct(wxCmdLog,
                            {'log':underlying_text}, 
                            args)
  
    def log_command(self, command):
	"""log a command.  Must be implemented by concrete subclass

	**INPUTS**

	*STR* command -- command string to be logged (should not include
	prompt or new-line)

	**OUTPUTS**

	*none*
	"""
	self.log.AppendText(self.prompt + command + '\n')
    
    def log_message(self, message):
	"""log output/message.  Must be implemented by concrete subclass

	**INPUTS**

	*STR* message -- message string to be logged (unlike
	log_command, should include internal and trailing new-lines)

	**OUTPUTS**

	*none*
	"""
	self.log.AppendText(message)




