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
import code # for interpreting Python code at the command line
from Object import Object
#import wxEditor
import TextBufferWX
import wxCmdPrompt
import wxAutoSplitterWindow
from wxPython.wx import *

try:
    dummy_var = wxCHANGE_DIR
    del dummy_var
except NameError:
    wxCHANGE_DIR = 0

import OldWaxEdit

ID_EXIT = 101
ID_OPEN_FILE = 200
ID_CONF_SCRIPT = 210
ID_SAVE_FILE = 220
ID_SAVE_AS = 230
ID_DICTATED=102
ID_EDITOR=103
ID_SPLITTER=104
ID_CHOOSE_FONT=105
ID_FOCUS_COMMAND = 107
ID_FOCUS_EDITOR = 108
ID_PANE = 120
ID_PROMPT = 130
ID_COMMAND_LINE = 140
ID_MIC_BUTTON = 150
ID_MIC_LABEL = 151


class WaxEdSimPane(wxPanel):

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

    *InteractiveInterpreter* command_line_interp -- from standard module
    code

    *wxTextControl* log -- text control for log window to display
    output, error messages, and command history

    *TextBufferWX* wax_text_buffer -- editor interface with change
    specification, so that we can keep track of changes to the editor
    buffer.

    *wxTextControl* editor -- underlying text control for editor window

    *FCT* change_callback --
    change_callback( *INT* start, *INT* end, *STR* text, 
    *INT* selection_start, *INT* selection_end, 
    *STR* buff_name, *BOOL* program_initiated).   See set_change_callback 
    below for details


    """
    def __del__(self):
        wxBell()

    def cleanup(self):
        self.exiting = 1

#        wxBell()
#        self.mic_button.SetBitmapLabel(wxNullBitmap)
#        self.mic_button.Destroy()
#        print 'hello'
#        self.green_light.Destroy()
        del self.green_light
        del self.grey_light
        del self.dark_grey_light
        del self.parent
        
        
    def __init__(self, parent, ID, title, command_space = None,
            change_callback = None):
        wxPanel.__init__(self, parent, ID, wxDefaultPosition, wxDefaultSize,
            name = title)
        self.parent = parent
        self.exiting = 0

        self.change_callback = change_callback

# dictionary to provide local name space for user commands
        self.command_space = {}
        if command_space != None:
            self.command_space = command_space

        self.vbox = wxBoxSizer(wxVERTICAL)

        self.button_line = wxBoxSizer(wxHORIZONTAL)

        self.green_light = wxBitmap("bitmaps/green.bmp", wxBITMAP_TYPE_BMP)
#        self.grey_light = wxBitmap("bitmaps/yellow.bmp", wxBITMAP_TYPE_BMP)
        self.grey_light = wxBitmap("bitmaps/grey.bmp", wxBITMAP_TYPE_BMP)
        self.dark_grey_light = wxBitmap("bitmaps/darkgrey.bmp", wxBITMAP_TYPE_BMP)
        self.mic_button = wxBitmapButton(self, ID_MIC_BUTTON, self.grey_light, 
        wxDefaultPosition,
        (self.grey_light.GetWidth()+10,self.grey_light.GetHeight()+10))
        self.mic_label = wxStaticText(self, ID_MIC_LABEL, "Microphone: ")
        self.button_line.Add(self.mic_label, 0, wxALIGN_CENTER)
        self.button_line.Add(self.mic_button, 0)
        EVT_BUTTON(self, ID_MIC_BUTTON, self.on_mic_button)

        top_and_bottom = wxAutoSplitterWindow.wxFixedFocusSplitter(self,
            ID_SPLITTER, 1)
        top_and_bottom.SetMinimumPaneSize(30)
        self.top_and_bottom=top_and_bottom
        flags = wxTE_MULTILINE | wxTE_NOHIDESEL 
        cr_bug = 1
        if sys.platform == 'win32':
# allows text longer than 64K
            flags = flags | wxTE_RICH
# rich text uses \r only for new lines, so offsets into internal and 
# external buffers are the same
#            cr_bug = 0
        editor =wxTextCtrl(top_and_bottom, ID_EDITOR, "", wxDefaultPosition,
#            wxDefaultSize, flags)
            wxDefaultSize, wxTE_MULTILINE | wxTE_NOHIDESEL)
        log =wxTextCtrl(top_and_bottom, ID_EDITOR, "", wxDefaultPosition,
            wxDefaultSize, flags | wxTE_READONLY)
        self.editor = editor
        self.log = log
        self.prompt_text = "Command> "
        self.command_log = wxCmdPrompt.wxCmdLog(log, prompt = self.prompt_text)
#        self.command_log.write('Microphone button: %d %d\n' % \
#            (self.mic_button.GetSizeTuple()))
#        self.command_log.write('Microphone button shown = %d\n' % \
#            (self.mic_button.IsShown()))

        self.prompt_line = wxBoxSizer(wxHORIZONTAL)
        self.vbox.Add(self.button_line, 0)
        self.vbox.Add(top_and_bottom, 1, wxEXPAND | wxALL, 4)
        self.vbox.Add(self.prompt_line, 0, wxEXPAND | wxALL, 4)

        self.prompt = wxStaticText(self, ID_PROMPT, "&Command")
        EVT_SET_FOCUS(self, self.on_focus)
        EVT_SET_FOCUS(self.prompt, self.p_focus)

        command_line=wxTextCtrl(self, ID_COMMAND_LINE, 
            "", wxDefaultPosition, wxDefaultSize,
            style =wxTE_PROCESS_ENTER)

        self.command_line = command_line
# provide extra access for testing - get rid of this in the end
        self.command_space['the_pane'] = self
        self.command_prompt = wxCmdPrompt.wxCmdPromptWithHistory(command_line,
            command_callback = self.on_command_enter)
        self.command_line_interp = code.InteractiveInterpreter(self.command_space)

        self.prompt_line.Add(self.prompt, 0, wxALL, 4)
        self.prompt_line.Add(self.command_line, 1, wxALL, 4)

  
        self.wax_text_buffer = \
            TextBufferWX.TextBufferWX(self.editor, 
            carriage_return_bug = cr_bug,
            change_callback=self.on_editor_change)
        self.SetAutoLayout(1)
        self.SetSizer(self.vbox)
        self.vbox.Fit(self)
        self.vbox.SetSizeHints(self)
        self.most_recent_focus = editor

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
#fudge so that recog mimic works from the command line.
#        return self.parent.is_active()

        current = wxWindow_FindFocus()
        if current.GetId() == self.editor.GetId():
            return 1
        return 0
    
    def p_focus(self, event):
        current = wxWindow_FindFocus()
        self.command_line.SetFocus()
    def on_focus(self, event):
        if self.exiting:
            event.Skip()
            return
        if self.most_recent_focus == 0:
            self.most_recent_focus = self.editor
        self.most_recent_focus.SetFocus()
    def on_mic_button(self, event):
        current = self.command_space['getmic']()
        if current == 'off':
            self.command_space['setmic']('on')
            self.most_recent_focus = self.editor
            self.most_recent_focus.SetFocus()
        else:
            self.command_space['setmic']('off')
            self.most_recent_focus = self.editor
            self.most_recent_focus.SetFocus()
    def update_mic_button(self, state = None):
        if state == None:
            state = self.command_space['getmic']()
        if state == 'on':
            self.mic_button.SetBitmapLabel(self.green_light)
            self.mic_button.Refresh()
        elif state == 'off':
            self.mic_button.SetBitmapLabel(self.grey_light)
            self.mic_button.Refresh()
        else:
            self.mic_button.SetBitmapLabel(self.dark_grey_light)
            self.mic_button.Refresh()
    def mic_change(self, state):
        self.command_log.write('Microphone is now '+state+'\n')
        self.update_mic_button(state)
    def on_command_enter(self, command_line, command):
        self.command_log.log_command(command)
        stdout = sys.stdout
        stderr = sys.stderr
        # capture standard output and standard error from exec and redirect them
        # to the command log
        try:
            sys.stdout = self.command_log
            sys.stderr = self.command_log
            self.editor.SetFocus()
            try:
                if self.command_line_interp.runsource(command):
                    sys.stderr.write('Error: incomplete input\n')
#                exec command \
#                    in sys.modules[self.__class__.__module__].__dict__, \
#                    self.command_space
                #  exec command in self.command_space
#                print self.command_space['quit_flag']
            except Exception, err:
                traceback.print_exc()
        finally:
            # make sure to restore standard output and standard error,
            # so that errors in the GUI don't go unreported if the GUI
            # crashes
            self.command_line.SetFocus()
            sys.stdout = stdout
            sys.stderr = stderr
        if self.command_space['quit_flag']:
            self.parent.quit_now(None)
    
    def initial_show(self):
        """create editor and log windows.  This is done here, rather
        than in __init__ because this is the first time that the actual
        size of the parent splitter window, top_and_bottom, is known
        """
        self.top_and_bottom.SplitHorizontally(self.editor, self.log, 0)
    
    def focus_editor(self, event):
        self.editor.SetFocus()
    def focus_command_line(self, event):
        self.command_line.SetFocus()
    def on_editor_change(self, start, end, text, selection_start,
        selection_end, buffer, program_initiated):
        if self.change_callback != None:
            buff_name = self.parent.app_control.app_active_buff_name()
            self.change_callback(start, end, text, selection_start,
                selection_end, buff_name, program_initiated)

    def set_change_callback(self, change_callback = None):
        """changes the callback to a new function

        **INPUTS**
      
        *FCT* change_callback --
        change_callback( *INT* start, *INT* end, *STR* text, 
        *INT* selection_start, *INT* selection_end, 
        *STR* buff_name, *BOOL* program_initiated)

        The arguments to the change callback specify the character offsets
        of the start and end of the changed region (before the change),
        the text with which this region was replaced, the start and end
        of the selected region (after the change), the name of the
        buffer reporting the change, and whether the change was
        program-initiated or editor-initiated.

        Note the difference between this change_callback and the
        TextBufferWX one: here the name of the buffer is returned,
        rather than a reference to the underlying TextBufferWX.  

        **OUTPUTS**

        *none*
        """
        self.change_callback = change_callback


class WaxEdSimFrame(wxFrame):
    """the main frame and its contents

    **CLASS ATTRIBUTES**

    *none*

    **INSTANCE ATTRIBUTES**

    *WaxEdSim* pane -- panel containing the controls

    *wxWindow* most_recent_focus -- subwindow which had the focus most
    recently.  Used to restore focus to this window when the user
    switches back to this application from another.

    *AppStateWaxEdit* app_control -- AppState interface

    *STR* title -- window title (without filename)

    others -- the various menus
    """

    def cleanup(self):
        """necessary because of circular references: 
        child contains reference to parent.  Note: quit_now calls
        cleanup"""
        self.exiting = 1
        try:
            self.pane.cleanup()
            self.pane.Destroy()
            del self.most_recent_focus
            del self.pane
        except AttributeError:
            pass

    def __init__(self, parent, ID, title, command_space = None):
        wxFrame.__init__(self, parent, ID, title, wxDefaultPosition,
        wxSize(1000, 600))

        self.title = title
        self.the_instance_string = ""
        self.name = None
        self.exiting = 0
        self.app_control = None
        self.activated = 0
        file_menu=wxMenu()
        file_menu.Append(ID_OPEN_FILE,"&Open...","Open a file")
        file_menu.Append(ID_CONF_SCRIPT,"&Config Script","Execute a python configuration script for the environment (ex: a demo file)")
        file_menu.Append(ID_SAVE_FILE,"&Save","Save current file")
        file_menu.Append(ID_SAVE_AS,"Save &As...","Save current file")        
        file_menu.Append(ID_EXIT,"E&xit","Terminate")

        window_menu = wxMenu()
        window_menu.Append(ID_FOCUS_EDITOR, "&Editor Window")
        window_menu.Append(ID_FOCUS_COMMAND, "&Command Line")

        format_menu = wxMenu()
        format_menu.Append(ID_CHOOSE_FONT, "&Font...")        

        edit_menu = wxMenu()

        menuBar=wxMenuBar()
        EVT_CLOSE(self, self.on_close)        
        menuBar.Append(file_menu,"&File");
        menuBar.Append(edit_menu,"&Edit");
        menuBar.Append(format_menu,"F&ormat");        
        menuBar.Append(window_menu, "&Window");

        self.CreateStatusBar()

        self.SetMenuBar(menuBar)
        EVT_MENU(self,ID_EXIT,self.quit_now)
        EVT_MENU(self,ID_OPEN_FILE,self.open_file)
        EVT_MENU(self,ID_CONF_SCRIPT,self.execute_file)
        EVT_MENU(self,ID_SAVE_FILE,self.save_file)
        EVT_MENU(self,ID_SAVE_AS,self.save_as)        
        EVT_MENU(self, ID_CHOOSE_FONT, self.choose_font)

        self.pane = WaxEdSimPane(self, ID_PANE, "WaxEdPanel",
            command_space = command_space)
        self.most_recent_focus=self.pane
        EVT_SET_FOCUS(self, self.on_focus)
    
        EVT_MENU(self,ID_FOCUS_EDITOR,self.pane.focus_editor)
        EVT_MENU(self,ID_FOCUS_COMMAND,self.pane.focus_command_line)
        EVT_ACTIVATE(self, self.on_activate) 

    def set_instance_string(self, instance_string):
        """sets the title string which is included in the full title 
        displayed in the title bar

        **INPUTS**

        *STR* instance_string -- string to include as part of the title

        **OUTPUTS**

        *BOOL* -- true if the editor, given the title escape sequence, 
        can and will include the instance string in its window title 
        for all windows containing editor buffers.

        """
        self.the_instance_string = instance_string
        self.update_title()
        return 1
      
    def set_name(self, name):
        """sets the filename to name (usually indicated in the title bar)

        **INPUTS**

        *STR* name -- name of current file

        **OUTPUTS**

        *none*
        """
        self.name = name
        self.update_title()

    def update_title(self):
        """update the window title to reflect the file name as well as
        the title string
        """
        title = self.title
        if self.instance_string:
            title = title + ' ' + self.instance_string
        if self.name:
            title = title + ' - ' + self.name
        self.SetTitle(title)

    def editor_buffer(self):
        """returns a reference to the TextBufferWX embedded in the GUI

        **INPUTS**

        *none*

        **OUTPUT**

        *TextBufferWX* -- the TextBufferWX
        """
        return self.pane.editor_buffer()

    def editor_has_focus(self):
        """indicates whether the editor window has the focus

        **INPUTS**

        *none*

        **OUTPUTS**
        *BOOL* -- true if editor window has the focus
        """
        if not self.is_active():
            return 0
        return self.pane.editor_has_focus()

    def on_focus(self, event):
        if self.exiting:
            event.Skip()
            return
        if self.most_recent_focus == 0:
            self.most_recent_focus = self.pane
        self.most_recent_focus.SetFocus()
    def update_mic_button(self, state = None):
        self.pane.update_mic_button(state)
    def mic_change(self, state):
        self.pane.mic_change(state)
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
#        print 'closing'
        self.cleanup()
        self.Close(true)
    def on_close(self, event):
        self.cleanup()
        event.Skip()        
    def open_file(self, event):
        init_dir = self.app_control.curr_dir
        dlg = wxFileDialog(self, "Edit File", init_dir, "", "*.*",
            wxOPEN | wxCHANGE_DIR)
        answer = dlg.ShowModal()
        if answer == wxID_OK:
            file_path = dlg.GetPath()
# hack to get CmdInterp to scan for symbols    
            self.pane.command_space['open_file'](file_path)
#            self.app_control.open_file(file_path)
        dlg.Destroy()



    def execute_file(self, event):
        init_dir = self.app_control.curr_dir
        dlg = wxFileDialog(self, "Execute Script File", init_dir, "",
            "*.*", wxOPEN)
        answer = dlg.ShowModal()
        print '-- WaxEdSim.execute_file: answer=%s, wxID_OK=%s' % (answer, wxID_OK)
        if answer == wxID_OK:
            file_path = dlg.GetPath()
            
            self.pane.command_prompt._on_command("execfile('%s')" % file_path)
        dlg.Destroy()

    def save_as(self, event):
        init_dir = self.app_control.curr_dir
        dlg = wxFileDialog(self, "Save File", init_dir, "", "*.*",
            wxSAVE | wxCHANGE_DIR | wxOVERWRITE_PROMPT)
        answer = dlg.ShowModal()
        if answer == wxID_OK:
            file_path = dlg.GetPath()
# file dialog will already have prompted
            self.app_control.save_file(file_path, no_prompt = 1)
        dlg.Destroy()


    def save_file(self, event):
        name = self.app_control.curr_buffer_name()
        if name:
            self.app_control.save_file(name, no_prompt = 1)
        else:
            self.save_as(self, event)


    def choose_font(self, event):

        on_window = self.pane.editor
        current_font = on_window.GetFont()
        current_font_data = wxFontData()
        current_font_data.SetInitialFont(current_font)
        dlg = wxFontDialog(self, current_font_data)
# the line below passed the return value (None?) of SetInitialFont to the
# dialog
#        dlg = wxFontDialog(self, wxFontData().SetInitialFont(current_font))
        dlg.ShowModal()
        chosen_font = dlg.GetFontData().GetChosenFont()
        if chosen_font:
            on_window.SetFont(chosen_font)
        dlg.Destroy()            

        
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
    def is_active(self):
        """indicates whether the editor frame is active

        **INPUTS**

        *none*

        **OUTPUTS**

        *BOOL* -- true if frame window is active
        """
        return self.activated

class WaxEdSim(wxApp, OldWaxEdit.WaxEdit):
    """application class

    **CLASS ATTRIBUTES**

    *none*

    **INSTANCE ATTRIBUTES**

    *WaxEdSimFrame* frame -- the main frame window of the class
    *{STR:ANY}* command_space -- a namespace (dictionary) in which to
    execute commands from the command line
    """
    def __init__(self, command_space = None, dummy = 0):
        """
        **INPUTS**

        *INT* dummy -- passed on to wxApp: don't know what this does,
        but it always seems to be set to zero

        *{STR:ANY}* command_space -- a namespace (dictionary) in which to
        execute commands from the command line
        """
        self.command_space = command_space
        wxApp.__init__(self, dummy)

    def OnInit(self):
        frame = WaxEdSimFrame(NULL, -1, "WaxEdit", 
            command_space = self.command_space)
        frame.Show(true)
        frame.pane.initial_show()
        self.SetTopWindow(frame)
        self.frame = frame
        return true

    def editor_buffer(self):
        """returns a reference to the TextBufferWX embedded in the GUI

        **INPUTS**

        *none*

        **OUTPUT**

        *TextBufferWX* -- the TextBufferWX
        """
        return self.frame.editor_buffer()

    def open_file_in_buffer(self, name):
        """opens a new file in the existing TextBufferWX

        **INPUTS**

        *none*

        **OUTPUTS**

        *BOOL* -- true on success (otherwise the existing file is left
        there)
        """
        return self.frame.editor_buffer().underlying.LoadFile(name)
    
    def save_file(self, full_path, no_prompt = 0):
        """Saves the file in the existing TextBufferWX

        **INPUTS**

        *STR full_path* -- path name of file to save

        *BOOL no_prompt* -- if true, don't prompt before overwriting
        an existing file.

        **OUTPUTS**

        *BOOL* -- true on success (otherwise the existing file is left
        there)
        """
        if not no_prompt:
            answer = wxMessageBox("Replace file %s?" % (full_path), 
                "Save File", wxYES_NO, self.frame)
            if answer != wxYES:
                return 0
        return self.frame.editor_buffer().underlying.SaveFile(full_path)


    def is_active(self):
        """indicates whether the editor frame is active

        **INPUTS**

        *none*

        **OUTPUTS**

        *BOOL* -- true if frame window is active
        """
        return self.frame.is_active()

    def editor_has_focus(self):
        """indicates whether the editor window has the focus

        **INPUTS**

        *none*

        **OUTPUTS**
        *BOOL* -- true if editor window has the focus
        """
        return self.frame.editor_has_focus()

    def mic_change(self, state):
        """function to receive microphone state change callbacks

        **INPUTS**

        *STR* state -- new state ('on', 'off', 'sleeping', 'disabled')

        **OUTPUTS**

        *none*
        """
        self.frame.mic_change(state)


    def update_mic_button(self, state = None):
        self.frame.update_mic_button(state)
      
    def set_instance_string(self, instance_string):
        """sets the title string which is included in the full title 
        displayed in the title bar

        **INPUTS**

        *STR* instance_string -- string to include as part of the title

        **OUTPUTS**

        *none*
        """
        return self.frame.set_instance_string(instance_string)
      
    def set_name(self, name):
        """sets the filename to name (usually indicated in the title bar)

        **INPUTS**

        *STR* name -- name of current file

        **OUTPUTS**

        *none*
        """
        self.frame.set_name(name)
    def run(self, app_control):
        """starts the message loop.  Note: this function does not
        return until the GUI exits.

        **INPUTS**

        *AppStateWaxEdit app_control* -- reference to corresponding 
        AppState interface

        **OUTPUTS**

        *none*
        """
        self.frame.app_control = app_control
        self.update_mic_button()
        self.MainLoop()

def run():
    app=WaxEdSim()
    app.MainLoop()

if __name__ =='__main__':
    run()
