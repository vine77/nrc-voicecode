"""interfaces for command-line prompt with history """ 
# (C)2000 David C. Fox


import debug
from Object import Object

class CmdPrompt(Object):
    """abstract base class defining basic command-line prompt interface.

    **INSTANCE ATTRIBUTES**

    *FCT BOOL* command_callback --
    command_callback( *CmdPrompt* cmd_line, *STR* command)
    function to be called when the user enters a command.  cmd_line
    is the CmdPrompt object.  command is the text of the command entered
    the underlying buffer.  The function should return true if the command 
    was valid.  (This is not used by CmdPrompt, but may be used by subclasses)

    **CLASS ATTRIBUTES**
    
    *none* 
    """
    def __init__(self, command_callback=None, **args):
	"""
	**INPUTS**

	*FCT BOOL* command_callback --
	command_callback( *CmdPrompt* cmd_line, *STR* command)
	-- function to be called when the user enters a command.  cmd_line
	is the CmdPrompt object.  command is the text of the command entered
	the underlying buffer.  The function should return true if the command 
	was valid.  (This is not used by CmdPrompt, but may be used by 
	subclasses)
	"""
    
        self.deep_construct(CmdPrompt,
                            {'command_callback':command_callback}, 
                            args)

    def set_command_callback(self, command_callback = None):
	"""changes the callback to a new function

	**INPUTS**
    
	*FCT BOOL* command_callback --
	command_callback( *CmdPrompt* cmd_line, *STR* command)
	-- function to be called when the user enters a command.  cmd_line
	is the CmdPrompt object.  command is the text of the command entered
	the underlying buffer.  The function should return true if the command 
	was valid.  (This is not used by CmdPrompt, but may be used by 
	subclasses)

	**OUTPUTS**

	*none*
	"""
	self.command_callback = command_callback

    def _on_command(self, command):
	"""internal function which triggers the
	entry_callback.  Only the concrete subclass of
	CmdPrompt implementing the command entry
	should call this function
	
	**INPUTS**
	
	*STR* command -- text of the command entered (without newline)
	"""
	if self.command_callback:
	    (self.command_callback)(self, command)
	    # note: command_callback is an attribute of 
	    # CmdPrompt, which is a function, not a method of
	    # CmdPrompt.  This looks a bit funny (like a
	    # method being called with a duplicate self argument) but it
	    # is actually correct.

class CmdPromptWithHistory(CmdPrompt):
    """(still partly abstract) class which implements the history stack.
    A concrete subclass must still provide the GUI and event
    functionality, as well as methods save_edited, restore_edited, 
    edited, and in_progress.

    **INSTANCE ATTRIBUTES**

    *[STR]* command_stack -- stack of previous commands

    *INT* max_stack -- maximum size of stack

    *INT* stack_index -- index (from back of command_stack) of currently
	recalled command

    **CLASS ATTRIBUTES**
    
    *none* 

    All previously entered commands, except for empty strings, are
    stored in the command_stack, with the most recent command at the end
    of the list.  (Max_stack can optionally be used to limit the size of
    the stack).  The interface is modeled on the command history of
    Unix tcsh.  The user can move backwards and forwards through the
    command_stack.  Any partially edited command-line is stored when the
    user first moves back into the stack and restored if the user moves
    forward past the most recent command.  The previous commands may be
    edited, but these changes are lost when the user moves in either
    direction.
    """

    def __init__(self, max_stack = None, saved_stack = None, **args):
	"""create a new history stack

	**INPUT**

	*INT* max_stack -- maximum size of stack (if None, unlimited)

	*[STR]* saved_stack -- initial stack

	"""
        self.deep_construct(CmdPromptWithHistory,
                            {"command_stack": saved_stack,
			    "max_stack": max_stack,
			    "stack_index":0},
                            args)
	if self.command_stack == None:
	    self.command_stack = []

    def save_edited(self):
	"""store partially edited new command.  A concrete subclass
	of CmdPromptWithHistory must define this method.
	Note: if appropriate, this command should store additional data,
	such as the current selection and insertion point.

	**INPUT**

	*none*

	**OUTPUT**

	*none*
	"""
	pass


    def restore_edited(self):
	"""restore previously saved partially edited new command.
	A concrete subclass of CmdPromptWithHistory must define this method.
	Note: if appropriate, this command should restore additional data,
	such as the selection and insertion point.

	**INPUT**

	*none*

	**OUTPUT**

	*none*
	"""
	pass

    def edited(self):
	"""contents of saved command line past the last command in the
	stack, if it has previously been saved.  A concrete subclass 
	of CmdPromptWithHistory must define this method.
	Unlike restore_edited, this method returns only the string
	contents in the saved command line.
    
	**INPUT**

	*none*

	**OUTPUTS**

	*STR* -- partial command previously stored with save_edited, 
	or None if there is none.
	"""
	pass

    def in_progress(self):
	"""contents of command line currently being edited (not the one
	stored by save_edited)
	A concrete subclass of CmdPromptWithHistory must define this method.
	**INPUT**

	*none*

	**OUTPUTS**

	*STR* -- partial command currently being edited
	"""
	pass

    def index(self):
	"""current index into stack
	**INPUT**

	*none*

	**OUTPUTS**

	*INT* -- index of command currently pointed to in stack
	"""
	return self.stack_index

    def peek(self, index):
	"""peek at command at index from last command in stack

	**INPUT**

	*INT* index -- how far from end of stack

	**OUTPUT**

	*STR* -- text of command pointed to by index
	"""
	if index:
# for index non-zero, simply return the appropriate element of the stack
	    return self.command_stack[-index]
# if index == 0, 
	if self.stack_index:
# and if we are currently editing the new command buffer, return that
	    return self.in_progress()
# otherwise return the saved partially edited command, or ""
	bottom = self.edited()
	if bottom:
	    return bottom
	return ""

    def depth(self):
	"""current depth of stack

	**INPUT**

	*none*

	**OUTPUTS**

	*INT* -- number of commands currently on the stack
	"""
	return len(self.command_stack)
    
    def previous(self):
	"""move pointer to previous command in stack
	**INPUTS**

	*none*

	**OUTPUTS**

	*STR* -- text of the previous command, or None if we
	have reached the first command in the stack 
	"""
	if self.stack_index == 0:
	    self.save_edited()
	if self.stack_index < self.depth():
	    self.stack_index = self.stack_index + 1
	    return self.peek(self.stack_index)
# already at the beginning of the stack
	return None

    def next(self):
	"""move pointer to next command in stack
	**INPUTS**

	*none*

	**OUTPUTS**

	*STR* -- text of the next command in the stack, or None if we pass
	the last command on the stack or are already past it.  The
	caller must check for None and avoid clearing the command-line
	buffer if it is returned, since restore_edited() will already
	have restored the buffer.
	"""
	if self.stack_index > 0:
	    self.stack_index = self.stack_index -1
	    if self.stack_index:
		return self.peek(self.stack_index)
# if we are returning past the last command on the stack, restore the
# stored partially edited command, and return None so the caller does
# not change the just-restored command-line.
	    self.restore_edited()
	return None

    def _raw_push(self, command):
	"""push a command onto the stack, without changing stack_index

	**INPUTS**

	*STR* command -- text of the command entered (without newline)

	**OUTPUTS**

	*none*

	Note: the stack_index should normally be reset to zero 
	when a command is pushed onto the stack, but _raw_push does not
	perform this task.  Unless this is specifically desired, push
	should be used instead.
	"""
	self.command_stack.append(command)
	if self.max_stack and self.depth() > self.max_stack:
	    del self.command_stack[0]
	self.stack_index = 0

    def push(self, command):
	"""push a (non-empty) command onto the stack, 
	and reset stack_index to zero.

	**INPUTS**

	*STR* command -- text of the command entered (without newline)

	**OUTPUTS**

	*none*

	"""
# only store non-empty commands
	if command:
	     self._raw_push(command)
	self.stack_index = 0

    def _on_command(self, command):
	"""internal function which triggers the
	entry_callback.  Only the concrete subclass of
	CmdPrompt implementing the command entry
	should call this function
	
	**INPUTS**
	
	*STR* command -- text of the command entered (without newline)

	**OUTPUTS**

	*none*
	"""
    
	self.push(command)
	CmdPrompt._on_command(self, command)

class CmdLog(Object):
    """abstract base class for logging command-line commands and 
    resulting output/error messages.

    **INSTANCE ATTRIBUTES**

    *STR* prompt -- prompt string

    **CLASS ATTRIBUTES**
    
    *none* 
    """
    def __init__(self, prompt=None, **args):
	"""
	**INPUTS**

	*STR* prompt -- prompt string to prepend to commands
	"""
        self.deep_construct(CmdLog,
                            {'prompt':prompt}, 
                            args)
	if not prompt:
	    self.prompt = ""

    def log_command(self, command):
	"""log a command.

	**INPUTS**

	*STR* command -- command string to be logged (should not include
	prompt or new-line)

	**OUTPUTS**

	*none*
	"""
	self.write(self.prompt + command + '\n')
    
    def write(self, string):
	"""add a string to the command log.
	Must be implemented by concrete subclass.
	This interface allows CmdLog to be used to capture
	standard output.

	**INPUTS**

	*STR* string -- message string to be logged (unlike
	log_command, should include internal and trailing new-lines)

	**OUTPUTS**

	*none*
	"""
	pass

    def log_message(self, message):
	"""log output/message.  

	**INPUTS**

	*STR* message -- message string to be logged (unlike
	log_command, should include internal and trailing new-lines)

	**OUTPUTS**

	*none*
	"""
	self.write(message)

class CmdLogFile(CmdLog):
    """implementation of CmdLog which writes to a file, and also
    optionally passes messages through to another CmdLog implementation.

    **INSTANCE ATTRIBUTES**

    *FILE* log_file -- file (open for writing or appending) used to
    log commands.  The file will be closed when the CmdLog is destroyed

    *CmdLog* second -- optional second CmdLog object to which the 
    write message will be passed (in addition to writing to the file)

    *BOOL* flush -- flush on each write?

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, log_file, second_cmd_log = None, flush = 0, **args):
	"""create a new CmdLog

	**INPUTS**

	*FILE* log_file -- file (should already be open for writing or
	appending) to use to log commands
    
	*CmdLog* second_cmd_log -- optional second CmdLog object to which the 
	write message will be passed (in addition to writing to the file)

	*BOOL* flush -- flush on each write?
	"""
        self.deep_construct(CmdLogFile,
                            {'log_file':log_file,
			     'second': second_cmd_log,
			     'flush': flush}, 
                            args)

    def __del__(self):
	"""destructor.  Shouldn't be called explicitly.
	"""
	self.log_file.flush()
	self.log_file.close()

    def write(self, string):
	"""add a string to the command log.
	This interface allows CmdLog to be used to capture
	standard output.

	**INPUTS**

	*STR* string -- message string to be logged (unlike
	log_command, should include internal and trailing new-lines)

	**OUTPUTS**

	*none*
	"""
	self.log_file.write(string)
	if self.flush:
	    self.log_file.flush()
	if self.second:
	    self.second.write(string)






    

