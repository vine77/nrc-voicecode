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
from Object import Object
#import wxEditor
import TextBufferWX
import wxAutoSplitterWindow
from wxPython.wx import *

ID_NEW_FILE = 101
ID_OPEN_FILE = 102
ID_SAVE_FILE = 103
ID_SAVE_FILE_AS = 104
ID_CLOSE_FILE = 105
ID_EXIT = 106


#ID_DICTATED=102

ID_TEXT_CONTROL=103
ID_SPLITTER=104
ID_FOCUS_TEXT_CONTROL = 108
ID_PANE = 120

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

    *wxAutoSplitterWindow* top_and_bottom -- parent window of text
     area with adjustable sash

    *TextBufferWX* wax_text_buffer -- TextBuffer interface with change
    specification, so that we can keep track of changes to the editor
    buffer.
    

    """

    def __del__(self):
        print 'pane breaking'

    def __init__(self, parent, ID, title):
        wxPanel.__init__(self, parent, ID, wxDefaultPosition, wxDefaultSize,
	name = title)
        self.parent = parent

        self.vbox = wxBoxSizer(wxVERTICAL)

        top_and_bottom = wxAutoSplitterWindow.wxFixedFocusSplitter(self,
	    ID_SPLITTER, 1)
        top_and_bottom.SetMinimumPaneSize(30)
        self.top_and_bottom=top_and_bottom
        text_control =wxTextCtrl(top_and_bottom, ID_TEXT_CONTROL, "", wxDefaultPosition,
	    wxDefaultSize,wxTE_MULTILINE)

        self.vbox.Add(top_and_bottom, 1, wxEXPAND | wxALL, 4)


	EVT_SET_FOCUS(self, self.on_focus)


  
        self.wax_text_buffer = \
	    TextBufferWX.TextBufferWX(text_control, change_callback=self.on_text_control_change)
        self.SetAutoLayout(1)
        self.SetSizer(self.vbox)
        self.vbox.Fit(self)
        self.vbox.SetSizeHints(self)
        self.most_recent_focus = text_control
    
    def p_focus(self, event):
        current = wxWindow_FindFocus()
        
    def on_focus(self, event):
	if self.most_recent_focus == 0:
	    self.most_recent_focus = self.wax_text_buffer.underlying
	self.most_recent_focus.SetFocus()
    
    def initial_show(self):
	"""create editor window.  This is done here, rather
	than in __init__ because this is the first time that the actual
	size of the parent splitter window, top_and_bottom, is known
	"""
	self.top_and_bottom.SplitHorizontally(self.wax_text_buffer.underlying, None, 0)
    
    def focus_text_control(self, event):
        self.wax_text_buffer.underlying.SetFocus()

    def on_text_control_change(self, start, end, text, selection_start,
        selection_end, buffer, program_initiated):
        pass



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
        file_menu.Append(ID_NEW_FILE,"N&ew","New File")
        file_menu.Append(ID_OPEN_FILE,"O&pen","Open File")
        file_menu.Append(ID_SAVE_FILE,"S&ave","Save File")
        file_menu.Append(ID_SAVE_FILE_AS,"S&ave as","Save File")
        file_menu.Append(ID_CLOSE_FILE,"C&lose","Close File")
        file_menu.Append(ID_EXIT,"E&xit","Terminate")

        window_menu = wxMenu()
        window_menu.Append(ID_FOCUS_TEXT_CONTROL, "&Editor Window")


        edit_menu = wxMenu()

        menuBar=wxMenuBar()
        menuBar.Append(file_menu,"&File");
        menuBar.Append(edit_menu,"&Edit");
        menuBar.Append(window_menu, "&Window");

        self.CreateStatusBar()

        self.SetMenuBar(menuBar)
        EVT_MENU(self,ID_NEW_FILE,self.new_file)
        EVT_MENU(self,ID_OPEN_FILE,self.open_file)        
        EVT_MENU(self,ID_SAVE_FILE,self.save_file)        
        EVT_MENU(self,ID_SAVE_FILE_AS,self.save_file_as)
        EVT_MENU(self,ID_CLOSE_FILE,self.save_file_as)
        EVT_MENU(self,ID_EXIT,self.quit_now)

        self.pane = WaxEditPane(self, ID_PANE, "WaxEdPanel")
	self.most_recent_focus=self.pane
	EVT_SET_FOCUS(self, self.on_focus)
    
        EVT_MENU(self,ID_FOCUS_TEXT_CONTROL,self.pane.focus_text_control)
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

    def new_file(self, event):
        pass

    def open_file(self, event):
        dlg = wxFileDialog(self)
        answer = dlg.ShowModal()
        if answer == wxID_OK:
            file_path = dlg.GetPath()
        self.pane.wax_text_buffer.underlying.LoadFile(file_path)
        
    def save_file(self, event):
        pass

    def save_file_as(self, event):
        pass

    def close_file(self, event):
        pass
    
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
