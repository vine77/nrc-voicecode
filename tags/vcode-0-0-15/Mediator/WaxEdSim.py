"""test version of new GUI interface to the mediator simulation"""

# (C)2000 David C. Fox


import debug
import traceback
import sys
from Object import Object
#import wxEditor
import TextBufferWX
import wxCmdPrompt
import wxAutoSplitterWindow
from wxPython.wx import *

ID_EXIT = 101
ID_DICTATED=102
ID_EDITOR=103
ID_SPLITTER=104
ID_FOCUS_COMMAND = 107
ID_FOCUS_EDITOR = 108
ID_PANE = 120
ID_PROMPT = 130
ID_COMMAND_LINE = 140
ID_PUSH_ME = 110

def error(string):
    """test capture of output to standard error"""

    sys.stderr.write(string)

class WaxEditPane(wxPanel):

    """main panel containing the GUI controls

    **CLASS ATTRIBUTES**

    *none*

    **INSTANCE ATTRIBUTES**

    (some self-expanatory controls and attributes omitted for brevity)

    *wxWindow* parent -- parent frame

    *wxWindow* most_recent_focus -- reference to window which held the
    focus most recently, so that the application remembers the focus
    when the user switches back from another application

    *wxBoxSizer* vbox -- sizer which allocates vertical space to the
    controls

    *wxAutoSplitterWindow* top_and_bottom -- parent window of editor and
    log windows, with adjustable sash

    *wxCmdLog* command_log -- handler to prove editable command-line 
    with history, and log

    *wxTextCtrl* command_line -- the command-line GUI control itself

    *{STR: ANY}* command_space -- local name space for user commands
    entered at the command line

    *wxTextControl* log -- text control for log window to display
    output, error messages, and command history

    *TextBufferWX* wax_text_buffer -- editor interface with change
    specification, so that we can keep track of changes to the editor
    buffer.

    *wxTextControl* editor -- underlying text control for editor window

    """

    def __del__(self):
        print 'pane breaking'

    def __init__(self, parent, ID, title):
        wxPanel.__init__(self, parent, ID, wxDefaultPosition, wxDefaultSize,
	name = title)
        self.parent = parent

        self.vbox = wxBoxSizer(wxVERTICAL)

	self.button = wxButton(self, ID_PUSH_ME, "Push me")
        self.button_line= wxBoxSizer(wxHORIZONTAL)
        self.button_line.Add(self.button, 0, wxALL, 4)

        top_and_bottom = wxAutoSplitterWindow.wxFixedFocusSplitter(self,
	    ID_SPLITTER, 1)
        top_and_bottom.SetMinimumPaneSize(30)
        self.top_and_bottom=top_and_bottom
        editor =wxTextCtrl(top_and_bottom, ID_EDITOR, "", wxDefaultPosition,
	    wxDefaultSize,wxTE_MULTILINE)
        log =wxTextCtrl(top_and_bottom, ID_EDITOR, "", wxDefaultPosition,
	    wxDefaultSize,wxTE_MULTILINE | wxTE_READONLY)
        self.editor = editor
        self.log = log
	self.prompt_text = "Command> "
	self.command_log = wxCmdPrompt.wxCmdLog(log, prompt = self.prompt_text)

        self.prompt_line = wxBoxSizer(wxHORIZONTAL)
        self.vbox.Add(self.button_line, 0, wxEXPAND | wxALL, 4)
        self.vbox.Add(top_and_bottom, 1, wxEXPAND | wxALL, 4)
        self.vbox.Add(self.prompt_line, 0, wxEXPAND | wxALL, 4)

        self.prompt = wxStaticText(self, ID_PROMPT, "&Command")
	EVT_SET_FOCUS(self, self.on_focus)
	EVT_SET_FOCUS(self.prompt, self.p_focus)

        command_line=wxTextCtrl(self, ID_COMMAND_LINE, 
            "", wxDefaultPosition, wxDefaultSize,
	    style =wxTE_PROCESS_ENTER)

        self.command_line = command_line
# dictionary to provide local name space for user commands
	self.command_space = {}
# provide extra access for testing - get rid of this in the end
	self.command_space['the_pane'] = self
	self.command_prompt = wxCmdPrompt.wxCmdPromptWithHistory(command_line,
	    command_callback = self.on_command_enter)

        self.prompt_line.Add(self.prompt, 0, wxALL, 4)
        self.prompt_line.Add(self.command_line, 1, wxALL, 4)

  
        self.wax_text_buffer = \
	    TextBufferWX.TextBufferWX(self.editor, change_callback=self.on_editor_change)
        self.SetAutoLayout(1)
        self.SetSizer(self.vbox)
        self.vbox.Fit(self)
        self.vbox.SetSizeHints(self)
        self.most_recent_focus = editor
    
    def p_focus(self, event):
        current = wxWindow_FindFocus()
	self.command_line.SetFocus()
    def on_focus(self, event):
	if self.most_recent_focus == 0:
	    self.most_recent_focus = self.editor
	self.most_recent_focus.SetFocus()
    def on_command_enter(self, command_line, command):
	self.command_log.log_command(command)
	stdout = sys.stdout
	stderr = sys.stderr
        # capture standard output and standard error from exec and redirect them
	# to the command log
	try:
	    sys.stdout = self.command_log
	    sys.stderr = self.command_log
	    try:
	        exec command \
		    in sys.modules[self.__class__.__module__].__dict__, \
		    self.command_space
                #	  exec command in self.command_space
	    except Exception, err:
	        traceback.print_exc()
	finally:
            # make sure to restore standard output and standard error,
	    # so that errors in the GUI don't go unreported if the GUI
	    # crashes
	    sys.stdout = stdout
	    sys.stderr = stderr
    
    def initial_show(self):
	"""create editor and log windows.  This is done here, rather
	than in __init__ because this is the first time that the actual
	size of the parent splitter window, top_and_bottom, is known
	"""
	self.top_and_bottom.SplitHorizontally(self.editor, self.log, 0)
# I don't think this is necessary or correct any more, now that we
# handle focus events hierarchically
#	self.parent.most_recent_focus=self.editor
    
    def focus_editor(self, event):
        self.editor.SetFocus()
    def focus_command_line(self, event):
        self.command_line.SetFocus()
    def on_editor_change(self, start, end, text, selection_start,
        selection_end, buffer, program_initiated):
        w, h = self.GetSizeTuple()
        w2, h2 = self.top_and_bottom.GetSizeTuple()
        we, he = self.editor.GetSizeTuple()
        wl, hl = self.log.GetSizeTuple()
        msg = "Change: %d %d %s" % (start, end, text)
        msg = msg + "Height self %d split %d top %d bottom %d" \
                % (h, h2, he, hl)
        self.parent.update_status_bar(msg)



class WaxEditFrame(wxFrame):
    """the main frame and its contents

    **CLASS ATTRIBUTES**

    *none*

    **INSTANCE ATTRIBUTES**

    *WaxEditPane* pane -- panel containing the controls

    *wxWindow* most_recent_focus -- subwindow which had the focus most
    recently.  Used to restore focus to this window when the user
    switches back to this application from another.

    others -- the various menus
    """

    def __init__(self, parent, ID, title):
        wxFrame.__init__(self, parent, ID, title, wxDefaultPosition,
        wxSize(1000, 600))

        file_menu=wxMenu()
        file_menu.Append(ID_EXIT,"E&xit","Terminate")

        window_menu = wxMenu()
        window_menu.Append(ID_FOCUS_EDITOR, "&Editor Window")
        window_menu.Append(ID_FOCUS_COMMAND, "&Command Line")

        edit_menu = wxMenu()

        menuBar=wxMenuBar()
        menuBar.Append(file_menu,"&File");
        menuBar.Append(edit_menu,"&Edit");
        menuBar.Append(window_menu, "&Window");

        self.CreateStatusBar()

        self.SetMenuBar(menuBar)
        EVT_MENU(self,ID_EXIT,self.quit_now)

        self.pane = WaxEditPane(self, ID_PANE, "WaxEdPanel")
	self.most_recent_focus=self.pane
	EVT_SET_FOCUS(self, self.on_focus)
    
        EVT_MENU(self,ID_FOCUS_EDITOR,self.pane.focus_editor)
        EVT_MENU(self,ID_FOCUS_COMMAND,self.pane.focus_command_line)
        EVT_ACTIVATE(self, self.on_activate) 

    def on_focus(self, event):
	if self.most_recent_focus == 0:
	    self.most_recent_focus = self.pane
	self.most_recent_focus.SetFocus()
    def update_status_bar(self, m):
	"""change the message in the status bar

	**INPUTS**

	*STR* m -- new message

	**OUTPUTS**

	*none*
	"""
        self.SetStatusText(m)
        return
    def quit_now(self, event):
	print 'closing'
        self.Close(true)
    def on_activate(self, event):
        current = wxWindow_FindFocus()
        if event.GetActive():
# window is being activated
            if not current:
                self.most_recent_focus.SetFocus()
        else:
            self.most_recent_focus = current


class WaxEdit(wxApp):
    """application class

    **CLASS ATTRIBUTES**

    *none*

    **INSTANCE ATTRIBUTES**

    *WaxEditFrame* frame -- the main frame window of the class
    """

    def OnInit(self):
        frame = WaxEditFrame(NULL, -1, "WaxEdit")
        frame.Show(true)
        frame.pane.initial_show()
        self.SetTopWindow(frame)
        return true

def run():
    app=WaxEdit(0)
    app.MainLoop()

if __name__ =='__main__':
    run()
