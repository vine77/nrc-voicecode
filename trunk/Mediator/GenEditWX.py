##############################################################################
# VoiceCode, a programming-by-voice environment
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# (C)2000, David C. Fox
#
##############################################################################

"""test version of new WaxEdit client editor"""


import debug
import traceback
import sys
import code # for interpreting Python code at the command line
import Object 
#import wxEditor
from wxPython.wx import *

try:
    dummy_var = wxCHANGE_DIR
    del dummy_var
except NameError:
    wxCHANGE_DIR = 0

import TextBufferWX
import GenEdit
import wxCmdPrompt
import wxAutoSplitterWindow
from wxFrameMenuMixIn import wxFrameMenuMixIn

class SimpleWaxPanel(wxPanel, Object.OwnerObject):
    """main panel containing a single text buffer 

    **CLASS ATTRIBUTES**

    *none*

    **INSTANCE ATTRIBUTES**

    *TextBufferWX* wax_text_buffer -- editor interface with change
    specification, so that we can keep track of changes to the editor
    buffer.

    *wxTextControl* editor -- underlying text control for editor window

    *BOOL* closing -- true if panel is closing (used to ensure that
    event handlers don't continue to call other methods when the panel
    may not be in a sane state)
    """
    def remove_other_references(self):
	"""additional cleanup to ensure that this object's references to
	its owned objects are the last remaining references

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
# subclasses must call their parent class's remove_other_references
# function, after performing their own duties
	self.closing = 1
	self.wax_text_buffer = None
	self.editor = None
	Object.OwnerObject.remove_other_references(self)

    def __init__(self, parent, ID, **args):
	"""
	**INPUTS**

	*wxWindow parent* -- the parent window to the frame

	*INT ID* -- the ID of the panel
	"""
	self.deep_construct(SimpleWaxPanel,
	                    {'wax_text_buffer': None,
			     'editor': None,
			     'closing': 0
			    },
			    args,
			    exclude_bases = {wxPanel:1}
			   )
        wxPanel.__init__(self, parent, ID, wxDefaultPosition, 
	    wxDefaultSize)
#	    parent.GetClientSize())

	flags = wxTE_MULTILINE 
	cr_bug = 1
	if sys.platform == 'win32':
# allows text longer than 64K
	    flags = flags | wxTE_RICH
# rich text uses \r only for new lines, so offsets into internal and 
# external buffers are the same
#	    cr_bug = 0
# but we're not using flags, so not rich so cr_bug = 1

	ID_EDITOR = wxNewId()
        editor = wxTextCtrl(self, ID_EDITOR, "", wxDefaultPosition,
#	    wxDefaultSize, flags)
#	    self.GetClientSize(), wxTE_MULTILINE)
	    wxDefaultSize, wxTE_MULTILINE)
        self.editor = editor
# because we put the editor in a panel, we need a sizer
	vbox = wxBoxSizer(wxVERTICAL)
	vbox.Add(editor, 1, wxGROW)

#	EVT_SET_FOCUS(self, self.on_focus)

#	if self.editor.IsModified():
#	    print 'modified already!'
        self.wax_text_buffer = \
	    TextBufferWX.TextBufferWX(self.editor, 
	    carriage_return_bug = cr_bug)
#	if self.wax_text_buffer.modified():
#	    print 'wax modified already!'
        self.SetAutoLayout(1)
        self.SetSizer(vbox)
        vbox.Fit(self)
        vbox.SetSizeHints(self)
#        self.most_recent_focus = editor

    def editor_buffer(self):
	"""returns a reference to the TextBufferWX embedded in the GUI

	**INPUTS**

	*none*

	**OUTPUT**

	*TextBufferWX* -- the TextBufferWX
	"""
	return self.wax_text_buffer

    def editor_has_focus(self):
	"""indicates whether the editor window has the focus

	**INPUTS**

	*none*

	**OUTPUTS**
	*BOOL* -- true if editor window has the focus
	"""
# no other controls in SimpleWaxPanel
#	return 1

	current = wxWindow_FindFocus()
	if current and current.GetId() == self.editor.GetId():
	    return 1
	return 0

    def current_font(self):
	"""find the current font for the text buffers in this window

	**INPUTS**

	*none*

	**OUTPUTS**

	*wxFont* -- the current font
	"""
	return self.editor.GetFont()

    def set_font(self, font):
	"""sets the current font for the text buffers in this window

	**INPUTS**

	*wxFont font* -- the desired font

	**OUTPUTS**

	*none*
	"""
	self.editor.SetFont(font)
    
class WaxFrameBase(wxFrame, GenEdit.GenEditFrameActivateEvent,
    wxFrameMenuMixIn):
    """partially concrete base class containing GUI elements and
    behaviors common to many subclasses.  Note: this class does not
    fill the frame with anything.

    **CLASS ATTRIBUTES**

    *none*

    **INSTANCE ATTRIBUTES**

    *wxWindow parent* -- the parent window, if any (usually not for
    single-frame applications)

    *BOOL* closing -- true if frame is closing (used to ensure that
    event handlers don't continue to call other methods when the frame
    may not be in a sane state)

    others -- the various menus
    """
    def remove_other_references(self):
	"""additional cleanup to ensure that this object's references to
	its owned objects are the last remaining references

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
# subclasses must call their parent class's remove_other_references
# function, after performing their own duties

	self.closing = 1
	GenEdit.GenEditFrameActivateEvent.remove_other_references(self)

    def __init__(self, ID, size, parent = None, **args):
	"""constructor for the base WaxEditFrame class

	**INPUTS**

	*wxWindowID ID* -- the wxWindows ID for the frame window

	*wxSize or (INT, INT) size* -- initial size for the frame

	*wxWindow parent* -- the parent window, if any (usually not for
	single-frame applications)
	"""

	self.deep_construct( WaxFrameBase,
			    {'closing': 0,
			     'ID': ID
			    }, args,
			    exclude_bases = {wxFrame: 1},
			    enforce_value = {'ID': ID}
			   )
        wxFrame.__init__(self, parent, self.ID, self.app_name, 
	    wxDefaultPosition, size)

        file_menu=wxMenu()
	ID_OPEN_FILE = wxNewId()
	ID_SAVE_FILE = wxNewId()
	ID_SAVE_AS = wxNewId()
	ID_EXIT = wxNewId()
#	print ID_OPEN_FILE
        file_menu.Append(ID_OPEN_FILE,"&Open...","Open a file")
        file_menu.Append(ID_SAVE_FILE,"&Save","Save current file")
        file_menu.Append(ID_SAVE_AS,"Save &As...","Save current file")        
        file_menu.Append(ID_EXIT,"E&xit","Terminate")

	ID_CHOOSE_FONT = wxNewId()
        format_menu = wxMenu()
        format_menu.Append(ID_CHOOSE_FONT, "&Font...")        

        edit_menu = wxMenu()

        menuBar=wxMenuBar()
        EVT_CLOSE(self, self.on_close)        
        menuBar.Append(file_menu,"&File");
        menuBar.Append(edit_menu,"&Edit");
        menuBar.Append(format_menu,"F&ormat");        
#        menuBar.Append(window_menu, "&Window");

        self.CreateStatusBar()

        self.SetMenuBar(menuBar)
        EVT_MENU(self, ID_EXIT, self.quit_now)
        EVT_MENU(self, ID_OPEN_FILE, self.on_open_file)
        EVT_MENU(self, ID_SAVE_FILE,self.on_save)
        EVT_MENU(self, ID_SAVE_AS,self.on_save_as)        
        EVT_MENU(self, ID_CHOOSE_FONT, self.choose_font)
        EVT_ACTIVATE(self, self.OnActivate) 

    def show(self):
	"""show the window corresponding to this frame

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	self.Show(1)

    def OnActivate(self, event):
	if self.closing:
	    return
        if event.GetActive():
# window is being activated
	    self.on_activate(1)
        else:
	    self.on_activate(0)

    def full_title(self):
	"""constructs the full title for the frame from the app_name,
	instance_string, if any, and buffer name

	**INPUTS**

	*none*

	**OUTPUTS**

	*STR* -- the title string
	"""
	buff_name = self.frame_active_buffer_name()
	title = self.app_name + ' - '
	if self.instance_string:
	    title = title + '[%s] - ' % self.instance_string
	title = title + buff_name
	return title

    def update_title(self):
	"""update the window title of the frame reflect a new buffer name 
	
	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	self.SetTitle(self.full_title())
    
    def close_window(self):
	"""close the window corresponding to this frame

	**NOTE:** The owner must call the frame's cleanup method before
	calling this method to close the actual GUI frame

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	if not self.closing:
# this should never happen, but if it does, report the error and make
# the best of it
	    debug.critical_warning('frame received close_window without prior cleanup')
	    self.cleanup()
	self.Close()

    def quit_now(self, event):
# owner will be responsible for prompting for the user to save files,
# and calling cleanup for this frame (and all others)
#	print 'quit_now'
	self.owner.on_exit(self.frame_ID)
    
    def on_close(self, event):
# after the owner has cleaned up the frame (on exit), go ahead and close
#	print 'on_close'
	if self.closing:
#	    print 'closing'
	    event.Skip()
	    return

# otherwise, notify the owner, which will be responsible for 
# prompting for the user to save files.
	proceed = self.owner.on_frame_close(self.frame_ID)
#	print 'proceed = ', proceed
# Unless the user cancels closing the frame, the owner will
# call cleanup for this frame, so it will be safe to close the frame
	if proceed:
	    event.Skip()
    
    def open_file_dialog(self, init_dir):
	file_path = None
        dlg = wxFileDialog(self, "Edit File", init_dir, "", "*.*",
 	    wxOPEN | wxCHANGE_DIR)
        answer = dlg.ShowModal()
        if answer == wxID_OK:
            file_path = dlg.GetPath()
	dlg.Destroy()
	return file_path

    def on_open_file(self, event):
# this is somewhat roundabout, but it allows us to get the proper
# initial directory for the Save As dialog box, and ensure that AppState
# gets an open buffer callback
#	print 'on_open'
	self.owner.open_file(user_initiated = 1)

    def save_as_dialog(self, buff_name, init_dir):
	"""prompts for a filename under which to save the file, and
	confirms overwriting

	**INPUTS**

	*STR buff_name* -- the name of the buffer (used to find the
	corresponding frame over which to pop up the Save As dialog)

	*STR init_dir* -- the path of the initial directory for the Save
	As dialog

        **OUTPUTS**

	*STR* -- the specified path, or None if the user cancelled 
	"""
        dlg = wxFileDialog(self, "Save File", init_dir,  "", "*.*",
	    wxSAVE | wxCHANGE_DIR | wxOVERWRITE_PROMPT)
	file_path = None
        answer = dlg.ShowModal()
        if answer == wxID_OK:
            file_path = dlg.GetPath()
	dlg.Destroy()
	return file_path

    def on_save_as(self, event):
#	print 'on_save_as'
	buff_name = self.frame_active_buffer_name()
# this is somewhat roundabout, but it allows us to get the proper
# initial directory for the Save As dialog box, and ensure that AppState
# gets a rename buffer callback
	self.owner.save_file(buff_name, ask_for_new_name = 1,
	    user_initiated = 1)

    def on_save(self, event):
#	print 'on_save'
	buff_name = self.frame_active_buffer_name()
	self.owner.save_file(buff_name, user_initiated = 1)

   
    def prompt_to_save(self, buff_name):
	"""prompts the user to save the current buffer before closing it, 
	or cancel.  Note: prompt_to_save should save if the user so
	indicates, and update the entry in self.filenames corresponding
	to the buffer, but should not close the buffer, because
	open_file could still fail.

	**INPUTS**

	*STR buff_name* -- the name of the buffer
	
        **OUTPUTS**

	*BOOL* -- true if the user saved or told WaxEdit to proceed
	without saving, false if the user asked for the action causing
	the buffer closing to be cancelled.
	"""
	answer = wxMessageBox("Save changes to document %s?" % buff_name, 
		"Save Changes", 
		wxICON_EXCLAMATION | wxYES_NO | wxCANCEL | wxYES_DEFAULT, 
		self)
	if answer == wxCANCEL:
	    return 0
	if answer == wxYES:
	    new_buff_name = self.owner.save_file(buff_name, rename_buff = 0)
	    if not new_buff_name:
		return 0
	return 1
 
    def current_font(self):
	"""find the current font for the text buffers in this window

	**INPUTS**

	*none*

	**OUTPUTS**

	*wxFont* -- the current font
	"""
	debug.virtual('WaxFrameBase.current_font')

    def set_font(self, font):
	"""sets the current font for the text buffers in this window

	**INPUTS**

	*wxFont font* -- the desired font

	**OUTPUTS**

	*none*
	"""
	debug.virtual('WaxFrameBase.set_font')

    def choose_font(self, event):
        current_font = self.current_font()
        current_font_data = wxFontData()
	current_font_data.SetInitialFont(current_font)
        dlg = wxFontDialog(self, current_font_data)
# the line below passed the return value (None?) of SetInitialFont to the
# dialog
#        dlg = wxFontDialog(self, wxFontData().SetInitialFont(current_font))
        dlg.ShowModal()
        chosen_font = dlg.GetFontData().GetChosenFont()
        if chosen_font:
	    self.set_font(chosen_font)
	dlg.Destroy()            

class SimpleWaxFrame(WaxFrameBase):
    """frame containing a SimpleWaxPanel

    **CLASS ATTRIBUTES**

    *none*

    **INSTANCE ATTRIBUTES**

    *SimpleWaxPanel* pane -- panel containing the controls

    *STR* curr_buffer_name -- name of the current (and only) buffer

    others -- the various menus
    """
    def __init__(self, init_buff_name = "", **args):
	self.deep_construct( SimpleWaxFrame,
			    {'pane': None,
			     'curr_buffer_name': init_buff_name
			    }, args
			   ),
	ID_PANE = wxNewId()
	self.pane = SimpleWaxPanel(self, ID_PANE)
	self.add_owned('pane')

    def frame_active_buffer_name(self):
      	"""Returns the name of the buffer currently active in this
	frame.

        **INPUTS**

        *none* 
        
	**OUTPUTS**

	*STR* -- buffer name of current buffer, or None if there is none
        """
	return self.curr_buffer_name
    
    def open_buffers(self):
	"""retrieve a list of the names of open buffers associated with
	contained by this frame.

        **INPUTS**

	*none*

        **OUTPUTS**

	*[STR]* -- list of the names of open buffers
	"""
	return [self.curr_buffer_name]

    def rename_buffer(self, buff_name, new_buff_name):
	"""notifies the frame that one of its buffers has been renamed

	**INPUTS**

	*STR buff_name* -- the old name of the new buffer

	*STR new_buff_name* -- the new name of the new buffer

	**OUTPUTS**

	*BOOL* -- false if the old buff_name was unknown, or the new
	name is already present
	"""
	if self.curr_buffer_name == buff_name:
	    self.curr_buffer_name = new_buff_name
	    return 1
	else:
	    return 0
    
    def switch_to_buffer(self, buff_name):
	"""Puts this frame in the foreground (if it isn't already), and
	changes the active buffer to buff_name

        **INPUTS**
        
        STR *buff_name* -- Name of the buffer to switch to.
       
        **OUTPUTS**
        
        *BOOL* -- true if buff_name exists and the external application
	successfully switches to it
        """
	if buff_name == self.curr_buffer_name:
	    self.SetFocus()
	    return 1
	return 0

    def delete_buffer(self, buff_name):
	"""delete a buffer 

	**INPUTS**

        STR *buff_name* -- name of buffer to remove

	**OUTPUTS**

	*none*
	"""
# for frames with only one buffer, this is a no-op
	pass
 
    def remove_buffer(self, buff_name):
	"""remove a buffer from the list of belong to this frame.  

	**Note:** this method only removes the buffer from GenEditFrame's
	records, it does not destroy the underlying GUI buffer or the
	window containing it.

	**INPUTS**

        STR *buff_name* -- name of buffer to remove

	**OUTPUTS**

	*none*
	"""
# for frames with only one buffer, this is a no-op
	pass

    def current_font(self):
	"""find the current font for the text buffers in this window

	**INPUTS**

	*none*

	**OUTPUTS**

	*wxFont* -- the current font
	"""
	return self.pane.current_font()

    def set_font(self, font):
	"""sets the current font for the text buffers in this window

	**INPUTS**

	*wxFont font* -- the desired font

	**OUTPUTS**

	*none*
	"""
	self.pane.set_font(font)
    
    def editor_buffer(self, buff_name):
	"""returns a reference to the TextBufferWX embedded in the GUI

	**INPUTS**

	*none*

	**OUTPUT**

	*TextBufferWX* -- the TextBufferWX
	"""
	if buff_name == self.frame_active_buffer_name():
	    return self.pane.editor_buffer()
	else:
	    return None

    def editor_has_focus(self):
	"""indicates whether the editor window has the focus

	**INPUTS**

	*none*

	**OUTPUTS**
	*BOOL* -- true if editor window has the focus
	"""
	return self.pane.editor_has_focus()

# defaults for vim - otherwise ignore
# vim:sw=4

