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

"""test version of new GUI interface to the mediator simulation"""



import debug
import traceback
import sys
import os
import shutil
import tempfile
from Object import Object
import CmdPrompt
import wxCmdPrompt
import wxAutoSplitterWindow
from wxPython.wx import *
import find_difference
import TextBuffer
import TextBufferWX
import VoiceDictBuffer
import natlink
from natlinkutils import *

ID_EXIT = 101
ID_DICTATED=102
ID_EDITOR=103
ID_LOG=105
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

    *wxCmdPromptWithHistory* command_prompt -- handler to provide 
    editable command-line 

    *wxCmdLog* command_log -- visible command and output log

    *CmdLogFile* command_log_file -- copies log to a file

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
	self.command_log = None
	shutil.copy(self.log_file, 'vdbtest.log')

    def __init__(self, parent, ID, title):
        wxPanel.__init__(self, parent, ID, wxDefaultPosition, wxDefaultSize,
	name = title)
        self.parent = parent
	self.count = 0

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
	flags = wxTE_MULTILINE | wxTE_READONLY
	if sys.platform == 'win32':
# allows log longer than 64K
	    flags = flags | wxTE_RICH
        log =wxTextCtrl(top_and_bottom, ID_LOG, "", wxDefaultPosition,
	    wxDefaultSize,wxTE_MULTILINE | wxTE_READONLY)
#        log =wxTextCtrl(top_and_bottom, ID_LOG, "", wxDefaultPosition,
#	    wxDefaultSize, flags)
        self.editor = editor
        self.log = log
	self.prompt_text = "Command> "
	self.screen_log= wxCmdPrompt.wxCmdLog(log, prompt = self.prompt_text)
	# global tempdir
	# if os.environ.has_key('TEMP'):
	#     tempdir = os.environ['TEMP']
	# elif os.environ.has_key('TMP'):
	#     tempdir = os.environ['TMP']
	global template
	template = 'vdbtest'
	self.log_file_name = tempfile.mktemp()
	self.log_file = open(self.log_file_name, 'w')
	self.command_log= CmdPrompt.CmdLogFile(self.log_file, 
	    second_cmd_log = self.screen_log, flush = 1, 
	    prompt = self.prompt_text)

	thiswin = natlink.getCurrentModule()[2]
	self.spy = SpyGrammar(self.command_log)

        self.prompt_line = wxBoxSizer(wxHORIZONTAL)
        self.vbox.Add(self.button_line, 0, wxEXPAND | wxALL, 4)
        self.vbox.Add(top_and_bottom, 1, wxEXPAND | wxALL, 4)
        self.vbox.Add(self.prompt_line, 0, wxEXPAND | wxALL, 4)

        self.prompt = wxStaticText(self, ID_PROMPT, "&Command")
	self.have_focus = 0
	EVT_SET_FOCUS(self, self.on_focus)
	EVT_KILL_FOCUS(self, self.on_kill_focus)
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

	self.spy.initialize()
        self.wax_text_buffer = TextBufferWX.TextBufferWX(editor,
	    change_callback=self.on_editor_change)
	underlying_voice_buffer = \
	    VoiceDictBuffer.VoiceDictBuffer(change_callback =
	    self.on_voice_change, recog_start_callback= self.on_recog_start)
	self.voice_buffer = \
	    TextBuffer.SelectionTextBufferCRToNL(underlying = underlying_voice_buffer)
        self.SetAutoLayout(1)
        self.SetSizer(self.vbox)
        self.vbox.Fit(self)
        self.vbox.SetSizeHints(self)
        self.most_recent_focus = editor
    def p_focus(self, event):
        current = wxWindow_FindFocus()
	self.command_line.SetFocus()
    def on_recog_start(self, buffer, window_matches):
#        return
	self.command_log.log_message('recog starting')
#	print 'recog start'
	if window_matches and self.parent.activated:
#	    print '(parent is activated, window matches)'
	    self.command_log.log_message('(parent is activated, window matches)')
#	    print 'parent is activated'
	    current = wxWindow_FindFocus()
#	    print current, self.editor
#	    self.command_log.log_message('\n%s %s\n' % (current.GetId(),
#	    self.editor.GetId()))
	    if current.GetId() == self.editor.GetId():
		visible = self.wax_text_buffer.get_visible()
		selection_start, selection_end \
		    = self.wax_text_buffer.get_selection()
		self.voice_buffer.set_lock(1)
		self.voice_buffer.set_selection(selection_start, selection_end)
#make everything visible
#		self.voice_buffer.set_visible()
		self.voice_buffer.set_visible(visible)
		self.voice_buffer.set_lock(0)
		if 0:
		    st, en = self.voice_buffer.get_selection()
		    if (st, en) != (selection_start, selection_end):
			self.command_log.log_message(\
			    'mismatch (%d, %d) vs. (%d, %d)' % (st, en,
			    selection_start, selection_end))
			self.command_log.log_message('sel should be [%s]\n' % 
			(self.wax_text_buffer.get_text(selection_start,
			selection_end)))
			self.command_log.log_message( \
			    'sel appears to be [%s]\n' % \
			    (self.voice_buffer.get_text(st, en)))
#		self.voice_buffer.set_visible(visible)
#		self.command_log.log_message('%d %d\n' % visible)
#		self.command_log.log_message('[%s]\n' % 
#		(self.wax_text_buffer.get_text(visible[0],visible[1])))
		self.command_log.log_message('-- buffer active\n')
#		print repr(self.voice_buffer.get_text())
		self.voice_buffer.reactivate()
#		self.spy.reactivate()
		return
	    else:
		self.command_log.log_message( 'wrong id')
#	else:
#	    print 'not active'
#	print 'deactivating'
	self.voice_buffer.deactivate()
#	self.spy.deactivate_spy()
#	self.command_log.log_message('-- buffer inactive\n')
    def on_voice_change(self, start, end, text, selection_start,
	selection_end, buffer, program_initiated):
#	return
#	print 'yielding'
	sys.stdout.flush()
	wxSafeYield()
#	print 'locking'
	sys.stdout.flush()
	self.voice_buffer.set_lock(1)
#	print 'just locked'
	sys.stdout.flush()
	sts, ste = self.voice_buffer.get_selection()
	if ((sts, ste) != (selection_start, selection_end)):
	    self.command_log.log_message( 'warning - selection mismatch')
	    self.command_log.log_message(\
	        'mismatch (%d, %d) vs. (%d, %d)' % (sts, ste,
			    selection_start, selection_end))
#	else:
#	    print 'selection matches'
	self.command_log.log_message('voice change: %d %d %s %d %d %d\n' %
	(start, end, text, selection_start, selection_end, program_initiated))
#	print 'vdbtest.on voice change: %d %d %s %d %d %d\n' % \
#	(start, end, text, selection_start, selection_end, program_initiated)
#	print repr(text)
#	print selection_start
	if (not program_initiated):
#	    print selection_start
#	    self.command_log.log_message('about to set text in GUI\n')
	    self.wax_text_buffer.set_text(text, start, end)
#	    self.command_log.log_message('about to select in GUI\n')
	    self.wax_text_buffer.set_selection(selection_start, selection_end)
#	    self.command_log.log_message('done\n')
#	self.command_log.log_message('about to get text from GUI for comparison\n')
        vis = self.wax_text_buffer.get_text()
#	self.command_log.log_message('about to get text from voice buffer for comparison\n')
        voc = self.voice_buffer.get_text()
	if vis != voc:
	    dif = \
		find_difference.find_string_difference(vis, voc)
	    if dif:
		d_start, d_end, d_text = dif
		if d_text:
		    self.command_log.log_message( \
			'vdbtest discrepancy %d %d' % (d_start, d_end))
		    self.command_log.log_message( '\nscreen:\n' + \
		        repr(vis[d_start:d_end]))
		    self.command_log.log_message( '\nvoice:\n' + \
		        repr(d_text) + '\n')
#	self.command_log.log_message('about to get selecton from voice buffer for comparison\n')
	sts, ste = self.voice_buffer.get_selection()
	if ((sts, ste) != (selection_start, selection_end)):
	    self.command_log.log_message( 'warning - selection mismatch')
	    self.command_log.log_message('%d, %d vs. %d, %d' % (sts, 
		ste, selection_start, selection_end))
#	self.command_log.log_message('about to set selecton from voice buffer for comparison\n')
	self.voice_buffer.set_selection(selection_start, selection_end)
#	self.command_log.log_message('about to release lock\n')
	self.voice_buffer.set_lock(0)
#	self.command_log.log_message('about to return\n')
    def log_window_change(self):
#	print 'yielding'
	sys.stdout.flush()
	wxSafeYield()
	print 'window changing'
	sys.stdout.flush()
        self.command_log.log_message('window changing')
    def on_kill_focus(self, event):
        self.have_focus = 0
    def on_focus(self, event):
        self.have_focus = 1
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
	self.voice_buffer.activate()
	print natlink.getCurrentModule()
# I don't think this is necessary or correct any more, now that we
# handle focus events hierarchically
#	self.parent.most_recent_focus=self.editor
    
    def focus_editor(self, event):
        self.editor.SetFocus()
    def focus_command_line(self, event):
        self.command_line.SetFocus()
    def on_editor_change(self, start, end, text, selection_start,
        selection_end, buffer, program_initiated):
#	self.voice_buffer.set_lock(1)
#	self.command_log.log_message('editor change')
	self.command_log.log_message('editor change: %d %d %s %d %d %d\n' %
	(start, end, text, selection_start, selection_end, program_initiated))
#	print 'editor change: %d %d %s %d %d %d\n' % \
#	(start, end, text, selection_start, selection_end, program_initiated)
	if not program_initiated:
#	    print 'feeding back to voice'
	    self.voice_buffer.set_text(text, start, end)
	    self.voice_buffer.set_selection(selection_start, selection_end)
        vis = self.wax_text_buffer.get_text()
        voc = self.voice_buffer.get_text()
	if vis != voc:
	    dif = \
		find_difference.find_string_difference(vis, voc)
	    if dif:
		d_start, d_end, d_text = dif
		if d_text:
		    self.command_log.log_message( \
			'vdbtest discrepancy %d %d' % (d_start, d_end))
		    self.command_log.log_message( \
		        '\nscreen:\n' + repr(vis[d_start:d_end]))
		    self.command_log.log_message( '\nvoice:\n' + \
			repr(d_text) + '\n')
        w, h = self.GetSizeTuple()
        w2, h2 = self.top_and_bottom.GetSizeTuple()
        we, he = self.editor.GetSizeTuple()
        wl, hl = self.log.GetSizeTuple()
        msg = "Change: %d %d %s" % (start, end, text)
        msg = msg + "Height self %d split %d top %d bottom %d" \
                % (h, h2, he, hl)
        self.parent.update_status_bar(msg)
#	self.voice_buffer.set_lock(0)



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

	self.activated = 0
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
	print 'pane is ', self.pane
	if self.pane:
	    self.pane.spy.unload()
	    self.pane.spy = None
	    print self.pane.voice_buffer
	    if self.pane.voice_buffer:
		self.pane.voice_buffer.underlying.underlying.setChangeCallback(None)
		self.pane.voice_buffer.deactivate()
		self.pane.voice_buffer = None
        self.Close(true)
    def on_activate(self, event):
        current = wxWindow_FindFocus()
        if event.GetActive():
# window is being activated
	    self.activated=1
            if not current:
                self.most_recent_focus.SetFocus()
        else:
            self.most_recent_focus = current
	    self.activated=0
	    self.pane.log_window_change()


class WaxEdit(wxApp):
    """application class

    **CLASS ATTRIBUTES**

    *none*

    **INSTANCE ATTRIBUTES**

    *WaxEditFrame* frame -- the main frame window of the class
    """

    def OnInit(self):
	natlink.natConnect(1)
        frame = WaxEditFrame(NULL, -1, "WaxEdit")
        frame.Show(true)
        frame.pane.initial_show()
	self.frame = frame
        self.SetTopWindow(frame)
        return true
    def OnExit(self):
#	print 'exiting'
	self.frame.Destroy()
	self.frame = None
	natlink.natDisconnect()

#
# Python Macro Language for Dragon NaturallySpeaking
#   (c) Copyright 2000 by Joel Gould
#
# This is the implementation of "repeat that".  In this implementation, you
# can say "repeat that" or "repeat that N times" to repeat the last
# recognition.
# 

class SpyGrammar(GrammarBase):

    gramSpec = """
        <start> exported = {emptyList};
    """

    def __init__(self, log):
	GrammarBase.__init__(self)
	self.log = log
#	self.win = win

    def reactivate(self):
#        self.activateAll(window=self.win)
        self.activateAll()

    def deactivate_spy(self):
        self.deactivateAll()

    def initialize(self):
        self.load(self.gramSpec,allResults=1)
#        self.activateAll(window=self.win)
        self.activateAll()

    def gotResultsObject(self,recogType,resObj):
        global lastResult
        if recogType == 'reject':
            lastResult = None
        elif resObj.getWords(0)[:2] != ['repeat','that']:
            self.log.write(repr(resObj.getResults(0)))
#            self.log.write(repr(resObj.getWords(0)))
#	    print repr(resObj.getWords(0))
            
def run():
    try:
	app=WaxEdit(0)
	print natlink.getCurrentModule()
	app.MainLoop()
    finally:
	natlink.natDisconnect()


if __name__ =='__main__':
    run()