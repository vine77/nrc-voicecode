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
# (C)2002, National Research Council of Canada
#
##############################################################################

"""A NewMediatorObject-based VoiceCode server that uses TCP/IP based 
messaging protocol to communicate with external editors.
"""

import vc_globals

import NewMediatorObject
from MediatorConsoleWX import MediatorConsoleWX
import tcp_server

import os, posixpath, re
import string, sys, time

import debug
import Object
import sr_interface, util

import auto_test

from wxPython.wx import *

import SaveSpeech
from WavePlaybackWX import WavePlaybackWX
from thread_communication_WX import *

# for now, our only implementation of WinSystem is the MS Windows
# specific one
import WinSystemMSW




# Uncomment this and add some entries to active_traces if you want to 
# activate some traces.
debug.config_traces(status="on", 
                    active_traces={
#                        'CmdInterp': 1,
#                        'reinterpret_recent': 1,
#                        'wxMediator': 1,
#                        'send_mess': 1,
#                        'get_mess': 1,
#                        'RSMInfrastructure': 1,
#                      'RecogStartMgr': 1,
#                      'pop_breadcrumb': 1,
#                      'SelectWinGram': 1,
#                        'GramMgr': 1,
#                        'DictWinGram': 1,
#                        'ResMgr': 1,
#                        'BasicCorrectionWinGram': 1,
#                      'CmdInterp.is_spoken_LSA': 1
#                       'NewMediatorObject': 1,
#                       'OwnerObject': 1
#                      'init_simulator_regression': 1,
#                      'WinGramMgr': 1,
#                      'CmdInterp.interpret_NL_cmd': 1
#                      'synchronize': 1,
#                      'insert_indent': 1,
#                      'get_selection': 1,
#                      'set_selection': 1,
#                      'get_pos_selection': 1,
#                      'cur_pos': 1,
#                      'pos_selection_cbk': 1,
#                      'set_selection_cbk': 1,
#                      'goto_cbk': 1,
#                      'listen_one_transaction': 1,
#                                    'SourceBuff.on_change': 1
#                                   'get_mess':1, 
#                                   'send_mess': 1,
#                                   'RecogStartMgr': 1
#                                   'AppState.synchronize_with_app': 1,
#                                   'SourceBuff': 1,
#                                   'SourceBuffMessaging.line_num_of': 1,
#                                    'delete_instance_cbk': 1,
#                                    'listen_one_transaction': 1,
#                                    'close_app_cbk': 1,
#                                    'AppState': 1
      'now_you_can_safely_put_a_comma_after_the_last_entry_above': 0
                                   },
                                   allow_trace_id_substrings = 1)

#debug.config_traces(status="on", active_traces={'CmdInterp':1, 'sr_interface': 1, 'get_mess':1, 'send_mess': 1, 'sim_commands': 1}, allow_trace_id_substrings = 1)
#debug.config_traces(status="on", active_traces = 'all')
#debug.config_traces(status="on", active_traces = {'sr_interface':1},
#allow_trace_id_substrings = 1)

#
# Port numbers for the communication link
#
VC_LISTEN_PORT = 45770
VC_TALK_PORT = 45771

def EVT_MINE(evt_handler, evt_type, func):
    evt_handler.Connect(-1, -1, evt_type, func)

# create a unique event types
wxEVT_SOCKET_DATA = wxNewEventType()
wxEVT_NEW_LISTEN_CONN = wxNewEventType()
wxEVT_NEW_TALK_CONN = wxNewEventType()
wxEVT_CORRECT_UTTERANCE = wxNewEventType()
wxEVT_CORRECT_RECENT = wxNewEventType()

class wxMediatorMainFrame(wxFrame, Object.OwnerObject):
    """main frame for the GUI mediator

    **INSTANCE ATTRIBUTES**

    *wxMediator parent* -- the parent wxMediator (wxApp)

    *STR app_name* -- the application name

    *BOOL* closing -- true if frame is closing (used to ensure that
    event handlers don't continue to call other methods when the frame
    may not be in a sane state)
    """
    def __init__(self, parent, **args):
        """
        """
        self.deep_construct(wxMediatorMainFrame,
                            {
                             'parent': parent,
                             'app_name': 'VoiceCode',
                             'closing': 0
                            }, 
                            args,
                            exclude_bases = {wxFrame:1}
                           )
        self.name_parent('parent')
        wxFrame.__init__(self, None, wxNewId(), self.app_name,
            wxDefaultPosition, wxSize(400, 100), 
#            wxDEFAULT_FRAME_STYLE | wxSTAY_ON_TOP)
            wxDEFAULT_FRAME_STYLE)
        file_menu=wxMenu()
        ID_SAVE_SPEECH_FILES = wxNewId()
        ID_EXIT = wxNewId()
        file_menu.Append(ID_SAVE_SPEECH_FILES,
            "&Save speech files","Save speech files")
        file_menu.Append(ID_EXIT,"E&xit","Terminate")

        EVT_MENU(self, ID_EXIT, self.quit_now)

        menuBar=wxMenuBar()
        EVT_CLOSE(self, self.on_close)        
        EVT_MENU(self, ID_SAVE_SPEECH_FILES, self.save_speech_files)

        menuBar.Append(file_menu,"&File");
        self.CreateStatusBar()
        self.SetMenuBar(menuBar)

    def set_status_text(self, text):
        self.SetStatusText(text)

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
        Object.OwnerObject.remove_other_references(self)


    def show(self, initial = 0):
        """show the window corresponding to this frame

        **INPUTS**

        *BOOL* initial -- is this the initial time the frame is shown?

        **OUTPUTS**

        *none*
        """
        self.Show(1)
#        self.update_title()
#        print 'showing'
        if initial:
            self.initial_show()

    def initial_show(self):
        """**NOTE:** the application must call this method when the
        frame is initially shown.
        """
        pass

    def save_speech_files(self, event):
        self.parent.save_speech_files()

    def quit_now(self, event):
# owner will be responsible for prompting for the user to save files,
# and calling cleanup for this frame (and all others)
#        print 'quit_now'
        debug.trace('wxMediatorMainFrame.quit_now',
            'calling parent.on_exit')
        self.parent.on_exit()
    
    def close_window(self):
        debug.trace('wxMediatorMainFrame.close_window',
            'calling Close')
#        debug.print_call_stack()
        self.Close()

    def on_close(self, event):
# this method is invoked to handle a wxCloseEvent, which can be triggered
# in two cases:
#
# (1) when the user clicks on the close button for the frame
# (2) when another method (here, the wxMediator wxApp which owns the
# frame) calls wxFrame.Close()
#
# In case (2), wxMediator will first call this frame's cleanup method,
# which will set the closing flag.  In the former case, the closing flag
# will not have been set.

        debug.trace('wxMediatorMainFrame.on_close',
            'self.closing = %d' % self.closing)
        if self.closing:
# after the owner has cleaned up the frame (on exit), go ahead and close
#        print 'on_close'
#            print 'closing'
            event.Skip()
            return

# otherwise, notify the owner, which will be responsible for 
# prompting for the user to save files.
        debug.trace('wxMediatorMainFrame.on_close',
            'calling parent.on_exit')
        proceed = self.parent.on_exit(frame_closing = 1)
        debug.trace('wxMediatorMainFrame.on_close',
            'proceed = %d' % proceed)
#        print 'proceed = ', proceed
# Unless the user cancels closing the frame, the owner will
# call cleanup for this frame, so it will be safe to close the frame
        if proceed:
            event.Skip()

class wxMediator(wxApp, SaveSpeech.SaveSpeech,
    Object.OwnerObject):
    """wxApp subclass for the mediator

    **INSTANCE ATTRIBUTES**

    *ServerNewMediator the_server* -- the underlying server

    *NewMediatorObject the_mediator* -- the mediator object

    STR *test_suite=None* -- name of regression test suite to run

    *BOOL quitting* -- flag indicating that we are in the process of
    quitting
    """
    def __init__(self, test_suite = None, **args):
        self.deep_construct(wxMediator, 
                            {
                             'the_server': None,
                             'test_suite': test_suite,
                             'the_mediator': None,
                             'quitting':0
                            }, 
                            args, exclude_bases = {wxApp: 1})
        self.add_owned('the_mediator')
        testing = not (test_suite is None)
        self.the_server = self.create_server(testing)

        test_args = None
        test_space = None
        if testing:
            test_space = globals()
            test_args = [test_suite]
            sys.stderr.write('Loading test definitions...\n')
            tests_def_fname = posixpath.expandvars('$VCODE_HOME' + \
                os.sep + 'Admin' + os.sep + 'tests_def.py')
            execfile(tests_def_fname, test_space)        

        wxApp.__init__(self, 0)
#        wxApp.__init__(self, 1, 'medcrash')

# for now, our only implementation of WinSystem is the MS Windows
# specific one
        console = MediatorConsoleWX(self.main_frame(),
            win_sys = WinSystemMSW.WinSystemMSW())

        correct_evt = CorrectUtteranceEventWX(self, wxEVT_CORRECT_UTTERANCE)
        correct_recent_evt = CorrectRecentEventWX(self, wxEVT_CORRECT_RECENT)
        self.the_mediator = \
            NewMediatorObject.NewMediatorObject(server = self.the_server,
                console = console, wave_playback = WavePlaybackWX, 
                correct_evt = correct_evt,
                correct_recent_evt = correct_recent_evt,
                test_args = test_args,
                test_space = test_space, global_grammars = 1, exclusive = 1)
#        print self.the_mediator.server
        sys.stderr.write('Configuring the mediator...\n')
        self.the_mediator.configure()
#        print self.the_mediator.server
        sys.stderr.write('Finished wxMediator init...\n')

        self.main_frame().show(1)
        self.hook_events()
#        wxApp.__init__(self, 1, "crash.wxMediator")

    def main_frame(self):
        """returns a reference to the main frame of the wxMediator
        application

        **INPUTS**

        *none*

        **OUTPUTS**

        *wxFrame* -- the main wxFrame
        """
        debug.virtual('wxMediator.main_frame')

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

        debug.trace('wxMediator.remove_other_references',
            'setting self.quitting')
        self.quitting = 1
# for now, quit first, then cleanup (including server owned by the
# NewMediatorObject)
#        print 'about to quit the mediator'
        debug.trace('wxMediator.remove_other_references',
            'del ref. to server (so NewMediatorObject can clean it up)')
        self.the_server = None
        debug.trace('wxMediator.remove_other_references',
            'about to quit the mediator')
        self.the_mediator.quit(clean_sr_voc = 0, save_speech_files=0, 
            disconnect=1)
   
        debug.trace('wxMediator.remove_other_references',
            'done quitting the mediator')
        Object.OwnerObject.remove_other_references(self)

    def OnInit(self):
        self.create_main()
        self.SetTopWindow(self.main_frame())
        return 1

    def server(self):
        return self.the_server

    def run(self):
        """starts the message loop.  Note: this function does not
        return until the GUI exits.

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        self.MainLoop()
        debug.trace('wxMediator.run',
            'main loop finished, calling self.cleanup')
        self.quitting = 1
        self.cleanup()
        debug.trace('wxMediator.run', 'done with self.cleanup')


    def hook_events(self):
        """hook events up to our handlers

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        EVT_MINE(self, wxEVT_CORRECT_UTTERANCE, self.on_correct_utterance)
        EVT_MINE(self, wxEVT_CORRECT_RECENT, self.on_correct_recent)

    def on_correct_utterance(self, event):
        """handler for UtteranceCorrectionEventWX

        **INPUTS**

        *UtteranceCorrectionEventWX event* -- the event posted by 
        ResMgr.correct_nth via CorrectUtteranceEvent

        **OUTPUTS**

        *none*
        """
        if not self.quitting:
            number = event.utterance_number
            instance = event.instance_name
            self.the_mediator.correct_utterance(instance, number)

    def on_correct_recent(self, event):
        """handler for UtteranceCorrectionEventWX

        **INPUTS**

        *RecentCorrectionEventWX event* -- the event posted by 
        ResMgr.correct_recent via CorrectRecentEvent

        **OUTPUTS**

        *none*
        """
        if not self.quitting:
            instance = event.instance_name
            self.the_mediator.correct_recent(instance)


    def create_main(self):
        """create the main frame window for the mediator, but do not
        show it
        
        **INPUTS**
        
        *none*
        
        **OUTPUTS**

        *none*
        """
        debug.virtual('wxMediator.create_main')

    def create_server(self, test_server):
        """create the TCP server for the mediator, if running in server
        mode, and call hook_events, but do not start the server yet.
        
        **INPUTS**
        
        *BOOL test_server* -- true if the mediator has been started with
        a test suite and the server should listen for connections from a
        test client
        
        **OUTPUTS**

        *ServerNewMediator* -- the server, or None if we are running
        with an internal test editor instead
        """
        debug.virtual('wxMediator.create_server')
    
class wxMediatorServer(tcp_server.DataEvtSource, wxMediator):
    """wxMediator with a server

    **INSTANCE ATTRIBUTES**

    *wxMediatorMainFrame frame* -- the main frame window of the mediator
    """
    def __init__(self, **args):
        self.decl_attrs({'frame': None})
        self.deep_construct(wxMediatorServer, 
                            {}, args)

    def main_frame(self):
        """returns a reference to the main frame of the wxMediator
        application

        **INPUTS**

        *none*

        **OUTPUTS**

        *wxFrame* -- the main wxFrame
        """
        return self.frame

    def on_exit(self, frame_closing = 0):
        """method by which a frame can notify GenEdit that the user has
        selected the Exit item from the File menu.  The user may have an 
        opportunity to cancel this command (e.g. through the cancel button
        in a dialog prompting to save modified files)

        **INPUTS**

        *BOOL frame_closing* -- flag indicating if on_exit is being
        called by the close event handler of the frame (in which case we
        don't need to close the frame ourselves, just return 0).

        **OUTPUTS**

        *BOOL* -- true if the editor is exiting in response to this
        event (unless, e.g., the user has hit cancel in response to a 
        save modified files dialog)
        """
        return self.quit_now(frame_closing = frame_closing)

    def quit_now(self, prompt = 1, frame_closing = 0):
        """exit the mediator, unless the user cancels when prompted to
        save speech files

        **INPUTS**

        *BOOL prompt* -- flag indicating whether or not we should prompt
        the user to save speech files.

        **OUTPUTS**

        *BOOL* -- true if the user didn't cancel (or wasn't prompted)
        """
        exiting = 1
        if prompt:
            exiting = self.prompt_save_speech_files(self.frame)
        debug.trace('wxMediator.quit_now', 'exiting is %d' % exiting)
        if not exiting:
            return 0
        debug.trace('wxMediator.quit_now', 'cleanup frame')
        if self.frame:
            self.frame.cleanup()
            if not frame_closing:
                debug.trace('wxMediator.quit_now', 'frame.close_window')
                self.frame.close_window()
                debug.trace('wxMediator.quit_now', 'del reference to frame')
                self.frame = None
# since we called SetTopWindow with the frame, our message loop should
# close when the frame does, allowing us to perform our own cleanup when
# control returns from MainLoop to our run method

        debug.trace('wxMediator.quit_now', 'returning')
        return 1


    def create_server(self, test_server):
        """create the TCP server for the mediator, if running in server
        mode, and call hook_events, but do not start the server yet.
        
        **INPUTS**
        
        *BOOL test_server* -- true if the mediator has been started with
        a test suite and the server should listen for connections from a
        test client
        
        **OUTPUTS**

        *ServerNewMediator* -- the server, or None if we are running
        with an internal test editor instead
        """
        factory = tcp_server.AppStateFactorySimple()
        return tcp_server.ServerNewMediator(data_events = self,
                                         test_server = test_server,
                                         editor_factory = factory) 

    def data_event(self, id):
        """virtual method which supplies a data_event for ServerMainThread 
        subclasses 
        
        **INPUTS**

        STR *id* -- The unique ID of the listen socket
        
        **OUTPUTS**
        
        *SocketHasDataEvent* -- the data event which will allow the
        data thread to ensure that process_ready_socks is called.
        """
        event = SocketHasDataWX(self, wxEVT_SOCKET_DATA, id) 
        return event

    def create_main(self):
        """create the main frame window for the mediator, and show it
        
        **INPUTS**
        
        *none*
        
        **OUTPUTS**

        *wxMediatorMainFrame, wxFrame* -- the main frame 
        """
        self.frame = wxMediatorMainFrame(self)

    def run(self):
        """starts the message loop.  Note: this function does not
        return until the GUI exits.

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        listener_evt = InterThreadEventWX(self,
            wxEVT_NEW_LISTEN_CONN) 
        talker_evt = InterThreadEventWX(self,
            wxEVT_NEW_TALK_CONN) 
        server = self.server()
        sys.stderr.write('Starting server threads...\n')
        server.start_other_threads(listener_evt, talker_evt)
        wxMediator.run(self)

    def hook_events(self):
        """hook the server events up to our handlers

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        wxMediator.hook_events(self)
        EVT_MINE(self, wxEVT_SOCKET_DATA, self.on_data)
        EVT_MINE(self, wxEVT_NEW_LISTEN_CONN, self.new_listen_conn)
        EVT_MINE(self, wxEVT_NEW_TALK_CONN, self.new_talk_conn)

    def on_data(self, event):
        """event handler for data events
        """
        if not self.quitting:
            self.the_server.process_ready_socks([event.socket_ID])

    def new_listen_conn(self, event):
        if not self.quitting:
            self.the_server.handshake_listen_socks()

    def new_talk_conn(self, event):
        if not self.quitting:
            if not self.the_server.handshake_talk_socks():
# if we've just run regression tests, we quit now, without prompting
                self.quit_now(prompt = 0)


##############################################################################
def run(test_suite=None):
    """Start a ServerNewMediator/ServerMainThread with external message 
    loop using wxWindows events and the new NewMediatorObject
    """

    sys.stderr.write('creating wxMediator\n')
    app = wxMediatorServer(test_suite = test_suite)
    sys.stderr.write('starting...\n')
    app.run()
#    sys.stderr.write("run_ext_server finishing\n")
    

def help():
    print """
Usage: python wxMediator.py [OPTIONS]

Runs the VoiceCode GUI mediator with TCP server.

When this server is running, external editors can connect to VoiceCode through
TCP connections on the VC_LISTEN (45770) and VC_TALK (45771) ports.

OPTIONS
-------

-h :

   print this help message.

    
-t testSuite:

   Upon connection by a new external editor, run regression test suite
   *testSuite* on that external editor.

   (Default: None)

    """


if __name__ == '__main__':
    opts, args = util.gopt(['h', None, 't=', None])
    
    sr_interface.connect()

    #
    # Create a global grammar manager
    #
#    the_recog_start_mgr = RecogStartMgr.RecogStartMgr()


    if opts['t']:
       sys.stderr = sys.stdout
    #
    # Start servers on the VC_LISTEN and VC_TALK ports
    #
    run(test_suite=opts['t'])



# defaults for vim - otherwise ignore
# vim:sw=4
