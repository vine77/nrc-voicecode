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

"""A VoiceCode server that uses TCP/IP based messaging protocol to communicate with external editors.
"""

import vc_globals

import natlink, os, posixpath, pythoncom, re, select, socket
import SocketServer, string, sys, threading, time, whrandom, win32event

import AppStateEmacs, AppStateMessaging, auto_test, debug, mediator 
import messaging, Object
import AppMgr, RecogStartMgr, SourceBuffMessaging, sb_services
import sim_commands, sr_interface, util
import Queue

from tcp_threads import *



# Uncomment this and add some entries to active_traces if you want to 
# activate some traces.
debug.config_traces(status="on", 
                    active_traces={
#                                   'get_mess':1, 
#                                   'send_mess': 1,
#                                   'AppState.synchronize_with_app': 1,
#                                   'SourceBuff': 1,
#                                   'SourceBuffMessaging.line_num_of': 1,
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


def prompt_for_cmd():
    cmd = raw_input('Command> ')
    mediator.execute_command(cmd)                


class SB_MessExtEdSim(SourceBuffMessaging.SourceBuffMessaging):
    """Communicates with an external [EdSim] through a messaging link.

    This subclass of [SourceBuff] is designed to interact with an [EdSim]
    instance running in a different process.

    It is used mostly for debugging and regression testing purposes.
    
    **INSTANCE ATTRIBUTES**

    [SB_ServiceIndent] *indent_srv* -- Code indentation service used to
    provide indentation at the server level.

    {SB_ServiceLineManip] *lines_srv* -- Line numbering service.

    **CLASS ATTRIBUTES**
    
    *none* -- 

    ..[SB_ServiceLineManip] file:///./sb_services.SB_ServiceLineManip.html
    ..[SB_ServiceIndent] file:///./sb_services.SB_ServiceIndent.html
    ..[SourceBuff] file:///./SourceBuff.SourceBuff.html
    ..[EdSim] file:///./EdSim.EdSim.html"""
    
    def __init__(self, **args_super):
        self.deep_construct(SB_MessExtEdSim, 
                            {'indent_srv': sb_services.SB_ServiceIndent(buff=self, indent_level=3, indent_to_curr_level = 1),
                             'lines_srv': sb_services.SB_ServiceLineManip(buff=self)}, 
                            args_super, 
                            {})
	self.add_owned_list(['indent_srv', 'lines_srv'])

    def insert_indent(self, code_bef, code_after, range = None):
        self.indent_srv.insert_indent(code_bef, code_after, range)

    def indent(self, range = None):
        self.indent_srv.indent(range = range)
        
    def incr_indent_level(self, levels=1, range=None):
        self.indent_srv.incr_indent_level(levels=levels, range=range)

    def decr_indent_level(self, levels=1, range=None):
        self.indent_srv.decr_indent_level(levels=levels, range=range)
        
    def line_num_of(self, position = None):
	return self.lines_srv.line_num_of(position)

    def beginning_of_line(self, pos):
        return self.lines_srv.beginning_of_line(pos)

    def end_of_line(self, pos):    
        return self.lines_srv.end_of_line(pos)

    def goto_line(self, linenum, where=-1):
        self.lines_srv.goto_line(linenum, where)

class AS_MessExtEdSim(AppStateMessaging.AppStateMessaging):
    """Communicates with an external [EdSim] through a messaging link.

    This subclass of [AppState] is designed to interact with an [EdSim]
    instance running in a different process.

    It is used mostly for debugging and regression testing purposes.
    
    **INSTANCE ATTRIBUTES**
    
    *none*-- 

    **CLASS ATTRIBUTES**
    
    *none* -- 

    ..[AppState] file:///./AppState.AppState.html
    ..[EdSim] file:///./EdSim.EdSim.html"""
    
    def __init__(self, **args_super):
        self.deep_construct(AS_MessExtEdSim, 
                            {}, 
                            args_super, 
                            {})

    def new_compatible_sb(self, buff_name):
        buff = SB_MessExtEdSim(app=self, buff_name=buff_name)
        return buff
        


class AppStateFactory(Object.Object):
    """factory which produces new instances of concrete subclasses of 
    AppState for the TCP server

    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, **args):
	self.deep_construct(AppStateFactory,
			    {
			    },
			    args)

    def new_instance(self, app_name, id, listen_msgr, talk_msgr):
	"""create a new AppState of the subclass appropriate to the given
	app_name.

	**INPUTS**
	    
	STR *app_name* -- Name of the editor for which we want to
	create an [AppStateMessaging].

	STR *id* -- Unique ID of external editor connected to the [AppState]
	
	[Messenger] *listen_msgr* -- [Messenger] instance to use for the
	VC listener side of the connection.

	[Messenger] *talk_msgr* -- [Messenger] instance to use for the
	VC talker side of the connection.
        
    
	**OUTPUTS**
	
	*AppStateMessaging* -- the new AppStateMessaging representing the
	editor instance 

	..[AppState] file:///./AppState.AppState.html"""

	debug.virtual('AppStateFactory.new_instance')

class AppStateFactorySimple(AppStateFactory):
    """simple implementation of AppStateFactory for testing purposes

    **INSTANCE ATTRIBUTES**

    *BOOL use_local_srv* -- flag indicating whether we should use 
    local indent_srv and line_num_srv for external EdSim

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, use_local_srv = 1, **args):
	self.deep_construct(AppStateFactorySimple,
			    {
			     'use_local_srv': use_local_srv
			    },
			    args)
    
    def new_instance(self, app_name, id, listen_msgr, talk_msgr):
	"""create a new AppState of the subclass appropriate to the given
	app_name.

	**INPUTS**
	    
	STR *app_name* -- Name of the editor for which we want to
	create an [AppStateMessaging].

	STR *id* -- Unique ID of external editor connected to the [AppState]
	
	[Messenger] *listen_msgr* -- [Messenger] instance to use for the
	VC listener side of the connection.

	[Messenger] *talk_msgr* -- [Messenger] instance to use for the
	VC talker side of the connection.
        
    
	**OUTPUTS**
	
	*AppStateMessaging* -- the new AppStateMessaging representing the
	editor instance 

	..[AppState] file:///./AppState.AppState.html"""


	if re.match('dumbEdSim', app_name):
	    as_class = AS_MessExtEdSim
	elif re.match('EdSim', app_name):
	    if self.use_local_srv:
		as_class = AS_MessExtEdSim
            else:
		as_class = AppStateMessaging.AppStateInsertIndentMess
	elif re.match('emacs', app_name):
	    as_class = AppStateEmacs.AppStateEmacs
	else:
	    print "WARNING: Unknown editor '%s'" % app_name
	    print "Connection refused"
	    return None
        
	app = as_class(app_name=app_name, id=id, 
	    listen_msgr=listen_msgr, talk_msgr=talk_msgr)
	app.app_name = app_name
	return app




def vc_authentification(messenger):
    """Authentifies a VoiecCode user.

    For now, this function does nothing.

    **INPUTS**

    [Messenger] *messenger* -- Messenger to be used for the connection.

    [RecogStartMgr] *recog_mgr* -- Object responsible for
    dispatching recognition events to the various editors.
        

    **OUTPUTS**
        
    *none* -- 


    ..[Messenger] file:///./messaging.Messenger.html
    ..[RecogStartMgr] file:///./RecogStartMgr.RecogStartMgr.html"""
    

    pass


##############################################################################
# Classes for version of the server in which any calls to/from natlink
# are handled by the main thread.
##############################################################################


class ListenForConnThread(threading.Thread, Object.Object):
    """Listens for new socket connections on a port number.

    Adds each new socket to a list of uninitialised connections.
    
    **INSTANCE ATTRIBUTES**
    
    INT *port* -- Port on which to listen for connections.
    
    [socket] *new_socks* -- List on which to add any new connection.
    
    [lock] *new_socks_lock* -- Lock on the new connection list.

    *PyHandle raise_event* -- Win32 event to be raised when a new connection
    is opened.
    
    **CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, port, new_socks, new_socks_lock, raise_event, **args_super):
        self.deep_construct(ListenForConnThread, 
                            {'port': port, 
                             'new_socks': new_socks,
                             'new_socks_lock': new_socks_lock,
                             'raise_event': raise_event}, 
                            args_super, 
                            exclude_bases={'threading.Thread': 1})
        threading.Thread.__init__(self)        
        


    def run(self):
        """Start listening for new connections.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((socket.gethostname(), self.port))
        server_socket.listen(5)

        while 1:

            # Accept a new connection
            (client_socket, address) = server_socket.accept()

            debug.trace('ListenForConnThread.run', 'got new connection on port=%s' % self.port)
            
            #
            # Log it and Raise Win32 event to notify the main event loop that
            # it should shake hands with it
            #
            self.log_new_conn(client_socket)
            win32event.SetEvent(self.raise_event)

            #
            # When debugging, increase this if you want to see things happen
            # in slow motion
            #
            time.sleep(0.01)
#            time.sleep(1)


    def log_new_conn(self, client_socket):
        
        """Logs a newly received socket connection, so that main event
        loop can later shake hands with it.
        
        **INPUTS**
        
        *socket client_socket* -- Newly received socket connection
        
        **OUTPUTS**
        
        *none* -- 
        """
        
        self.new_socks_lock.acquire()
        self.new_socks.append((client_socket, [None, None, None]))
        self.new_socks_lock.release()        

        
class ListenForNewListenersThread(ListenForConnThread, Object.Object):
    """Listens for new connections on the VC_LISTEN port.
    
    **INSTANCE ATTRIBUTES**
    
    *none*-- 
    
    **CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, **args_super):
        global VC_LISTEN_PORT
        self.deep_construct(ListenForNewListenersThread, 
                            {}, 
                            args_super, 
                            {},
                            enforce_value={'port': VC_LISTEN_PORT})

        
class ListenForNewTalkersThread(ListenForConnThread):
    """Listens for new connections on the VC_TALK port.
    
    **INSTANCE ATTRIBUTES**
    
    *none*-- 
    
    **CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, **args_super):
        global VC_TALK_PORT
        self.deep_construct(ListenForNewTalkersThread, 
                            {}, 
                            args_super, 
                            {},
                            enforce_value={'port': VC_TALK_PORT})


class CheckReadySocksThread(threading.Thread, Object.Object):
    """This thread checks if any of the VC_LISTEN sockets have received data.

    If so, it raises a Win32 event to tell the main thread to process the
    data on the ready sockets
    
    **INSTANCE ATTRIBUTES**
    
    {socket: AppState} *socks_to_check* -- Dictionnary of sockets to
    check for readiness
    
    PyHandle *raise_event* -- Win32 event to raise if any of the
    sockets in *socks_to_check* is ready.

    [socket] *ready_socks* -- Put all the ready sockets in that list.

    *lock ready_socks_lock* -- Lock on the *ready_socks* list.
    
    **CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, socks_to_check, ready_socks, ready_socks_lock,
                 raise_event, **args_super):
        self.deep_construct(CheckReadySocksThread, 
                            {'socks_to_check': socks_to_check,
                             'ready_socks': ready_socks,
                             'ready_socks_lock': ready_socks_lock,
                             'raise_event': raise_event}, 
                            args_super, 
                            exclude_bases={'threading.Thread': 1})
        threading.Thread.__init__(self)



    def run(self):
        """Check for ready sockets.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        while 1:
            to_check = self.socks_to_check.keys()
            if len(to_check) > 0:
                self.ready_socks_lock.acquire()                
                (new_ready_socks, dum1,dum2) = select.select(to_check, [], [], 0)
		self.ready_socks.extend(new_ready_socks)
                self.ready_socks_lock.release()
                if len(self.ready_socks) > 0:
                    debug.trace('CheckReadySocksThread.run', 'some sockets are ready')
                    win32event.SetEvent(self.raise_event)

            # When debuggin, increase sleep time if you want to see things
            # happen in slow motion
            time.sleep(0.01)
            time.sleep(3)


class ServerSingleThread(Object.Object):
    """Implements a TCP/IP based VoiceCode server.

    ??? Update this documentation when the server is finalised ???
    
    **INSTANCE ATTRIBUTES**

    [(socket, (STR, STR, STR))] *new_listen_socks=[]* -- Each entry is
    a 2ple consiting of a new (uninitialised) socket on the VC_LISTEN
    port, and data about that socket. The data is itself a 3ple
    consisting of: (a) identifier of external editor, (b) name of the
    external editor and (c) window handle of the external editor.

    *[(socket, [None, None, None])] new_talk_socks* -- Like
     *new_listen_socks*, except sockets are on the VC_TALK port, and
     the data part of the 2ple is useless.
    
    {socket: STR} *active_listen_socks={}* -- Key is a VC_LISTEN
    sockets that HAS been initialised and associated with an
    [AppStateMessaging]. Value is the [AppStateMessaging] instance
    that's connected to the socket.

    [socket] *ready_socks*=[] -- List of active VC_LISTEN socks which
    are ready for input.

    *threading.lock new_socks_lock* -- Lock used to make sure that the
     main thread doesn't access the lists *new_listen_socks*
     and *new_talk_socks* at the same time as the threads that listen
     for new socket connections.

    *lock.lock ready_socks_lock* -- Lock for the list *ready_socks*.     

    [ListenForNewListenersThread] *new_listener_server* -- Thread that
    listens for new connections on the VC_LISTEN port.

    [ListenForNewTalkersThread] *new_talker_server* -- Thread that
    listens for new connections on the VC_TALK port.

    [CheckReadySocksThread] *ready_socks_checker* -- This thread
    monitors all the VC_LISTEN sockets to see if any of them has
    received new data.

    *PyHandle evt_new_listen_conn* -- Win32 event raised when a new
     socket connection is opened on VC_LISTEN port.
    
    *PyHandle evt_new_talk_conn* -- Win32 event raised when a new
     socket connection is opened on VC_TALK port.
    
    *PyHandle evt_sockets_ready* -- Win32 event raised when one of the
     active VC_LISTEN sockets has unread data.
    
    *PyHandle evt_quit* -- Win32 event raised when we are shutting
     down the server.

    *AppStateFactory editor_factory* -- factory for creating new
    AppStateMessaging instances

    {STR : MediatorObject} *active_meds* -- map from unique socket IDs
    to active mediators driving external edtiors.

    STR *test_suite=None* -- If not *None*, then upon connection by a
    new editor run regression test suite *test_suite*.

    **CLASS ATTRIBUTES**
    
    *none* -- 

    ..[AppStateMessaging] file:///./AppStateMessaging.AppStateMessaging.html
    ..[ListenForNewListenersThread] file:///./tcp_server.ListenForNewListenersThread.html
    ..[ListenForNewTalkersThread] file:///./tcp_server.ListenForNewTalkersThread.html
    """
    
    def __init__(self, editor_factory, test_suite=None, **args_super):
        self.deep_construct(ServerSingleThread, 
                            {'new_listen_socks': [],
                             'new_talk_socks': [],
                             'new_socks_lock': threading.Lock(),
                             'active_listen_socks': {},
                             'ready_socks': [],
                             'ready_socks_lock': threading.Lock(),                             
                             'evt_new_listen_conn': win32event.CreateEvent(None, 0, 0, None),
                             'evt_new_talk_conn': win32event.CreateEvent(None, 0, 0, None),
                             'evt_sockets_ready': win32event.CreateEvent(None, 0, 0, None),
                             'evt_quit': win32event.CreateEvent(None, 0, 0, None),
                             'active_meds': {},
			     'editor_factory': editor_factory,
                             'test_suite': None
                             }, 
                            args_super, 
                            {threading.Thread: 1})


    def package_sock_pair(self, id, app_name, window, listen_sock, talk_sock):
        
        """Packages a listen and talk socket into an
        [AppStateMessaging] instance
        
        **INPUTS**
        
        STR *id* -- The unique identifier assigned by VoiceCode to
        that socket pair.

        STR *app_name* -- Name of the external editor.

        STR *window* -- Window handle for the external editor.
        
        socket *listen_sock* -- The listen socket
        
        socket *talk_sock* -- The talk socket
        

        **OUTPUTS**
        
        *none* -- 

        ..[AppStateMessaging] file:///./messaging.AppStateMessaging.html"""        
        
        listen_msgr = messaging.messenger_factory(listen_sock)
        talk_msgr = messaging.messenger_factory(talk_sock)        
        an_app_state = self.editor_factory.new_instance(app_name, id, 
	    listen_msgr, talk_msgr)

        #
        # Give external editor a chance to configure the AppStateMessaging
        #
        an_app_state.config_from_external()

        ###################################################################
        #
        # When the AppMgr is functional, the code below will be used.
        #
        ###################################################################
        #
        # Tell the recognition start manager about this new editor instance
        #
        # window = self.new_listen_socks[listen_sock][1]
        # self.apps.new_instance(an_app_state.app_name, an_app_state, window)


        ###################################################################
        #
        # But for now, we create a MediatorObject instance as per the old
        # architecture of the system.
        #
        ###################################################################

        if opts['t'] != None:
            mediator.init_simulator_regression(on_app=an_app_state)
        else:
            exclusive = 1
            allResults = 0
            mediator.init_simulator(on_app=an_app_state, disable_dlg_select_symbol_matches=1, window=window, exclusive = exclusive, allResults = allResults)

        #
        # Add the listen socket to the list of active ones
        #
        self.active_listen_socks[listen_sock] = an_app_state        

        #
        # Run regression test?
        #
        if self.test_suite != None:
	    an_app_state.print_buff_when_changed = 1
            args = [self.test_suite]
            auto_test.run(args)

	    # notify external editor that we are quitting
	    an_app_state.talk_msgr.send_mess("terminating")

            # Send a quit event to quit the server
            win32event.SetEvent(self.evt_quit)            

        #
        # Copy the mediator to the list of active mediators.
        #
        self.active_meds[id] = mediator.the_mediator
        mediator.the_mediator = None

    def handshake_listen_socks(self):
        """Invoked when a new socket connection was opened on VC_LISTEN port.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        #
        # Get window handle of active application.
        #
        window = natlink.getCurrentModule()[2]

        self.new_socks_lock.acquire()

        #
        # Assume active window is the application that opened the last
        # socket conneciton in the list self.new_listen_socks.  This
        # may not hold if two editors connect to VoiceCode back to back
        # and rapidly.
        
        (most_rec_sock, most_rec_data) = self.new_listen_socks[len(self.new_listen_socks)-1]
        
        #
        # Create a temporary messenger for handshaking
        #
        a_messenger = messaging.messenger_factory(most_rec_sock)
               
        #
        # Get the external application name
        #
        a_messenger.send_mess('send_app_name')
        mess = a_messenger.get_mess(expect=['app_name'])
        app_name = mess[1]['value']
                
        #
        # Assign a random ID to the external editor, and send it on the socket
        # connection.
        #
        id = '%s_%s' % (app_name, repr(whrandom.random()))
        a_messenger.send_mess('your_id_is', {'value': id})
        a_messenger.get_mess(expect=['ok'])
        
        #
        # Assign window, id and app_name to the last socket in the list of
        # new listen sockets
        #
        most_rec_data[0] = id
        most_rec_data[1] = app_name
        most_rec_data[2] = window
        
        self.new_socks_lock.release()
        

    def handshake_talk_socks(self):
        
        """Does a handshake on a the new socket connection that were opened on
        VC_LISTEN port.
        
        **INPUTS**
        
        *none*

        **OUTPUTS**
        
        *none* -- 
        """

	self.new_socks_lock.acquire()

        #
        # Loop through list of new VC_TALK sockets, handshake with them
        # and package them into an AppState instance with their corresponding
        # VC_LISTEN sockets.
        #
        ii = 0
        while ii < len(self.new_talk_socks):            

            (talk_sock, dummy) = self.new_talk_socks[ii]
        
            #
            # Shake hands with that VC_TALK socket.
            # Get the ID of external editor that started this VC_TALK socket
            #
            a_msgr = messaging.messenger_factory(talk_sock)
            a_msgr.send_mess('send_id')
            mess = a_msgr.get_mess(expect=['my_id_is'])
            id = mess[1]['value']

            #
            # Find the corresponding VC_LISTEN socket
            #
            found = None
            jj = 0
            while jj < len(self.new_listen_socks):
                (listen_sock, listen_data) = self.new_listen_socks[jj]
                (a_listen_id, app_name, window) = listen_data
                if a_listen_id == id:
                    #
                    # Found it. Remove the two sockets from the list of
                    # new connections.
                    #
                    found = (listen_sock, app_name, window)
                    del self.new_listen_socks[jj]
                    del self.new_talk_socks[ii]
                    break

                jj = jj + 1
                
            if found != None:
                self.package_sock_pair(id, app_name, window, listen_sock, talk_sock)
                        
        self.new_socks_lock.release()        


    def process_ready_socks(self):
        """Processes socket connections that have received new data.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        debug.trace('ServerSingleThread.process_ready_socks', 'self.ready_socks=%s' % id(self.ready_socks))

        self.ready_socks_lock.acquire()

	while self.ready_socks:
	    a_sock = self.ready_socks.pop()
            an_app_state = self.active_listen_socks[a_sock]
            an_app_state.listen_one_transaction()
        
        self.ready_socks_lock.release()        

    def run(self):
        """Start the server

        This method runs 3 threads that raise Win32 events respectively when:

        - a request for a new connections on VC_LISTEN port is
          received (*self.evt_new_listen_conn* event).

        - a request for a new connections on VC_PORT port is received
          (*self.evt_new_talk_conn* event)

        - one or more existing connections on VC_LISTEN port has
          unread data (*self.evt_sockets_ready* event)

        These events (plus *self.evt_quit*) are handled inside an
        event loop run by this method.

        We need this event loop so that speech events can be processed
        (actually, I think the speech events are just forwarded to
        NatSpeak by calling pythoncom.PumpWaitingMessages()).

        Also, the reason why the above four events are not processed
        directly in the threads that raise them, is that processing
        the events involves invoking some natlink methods, and Natlink
        does not behave well outside of the main thread.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        #
        # Start threads for monitoring socket connections.
        # We make the threads daemonic so that the program exits automaticall
        # when only those three threads are left
        #

        #
        # This thread listens for new socket connections on VC_LISTEN port.
        # New connections are stored in a list, so that the main thread
        # can later on initialise them.
        #
        self.new_listener_server = \
           ListenForNewListenersThread(new_socks=self.new_listen_socks,
                                   new_socks_lock=self.new_socks_lock,
                                   raise_event=self.evt_new_listen_conn)
        self.new_listener_server.setDaemon(1)
        self.new_listener_server.start()

        #
        # This thread listens for new socket connections on VC_TALK port.
        # New connections are stored in a list, so that the main thread
        # can later on initialise them.        
        #
        self.new_talker_server = \
           ListenForNewTalkersThread(new_socks=self.new_talk_socks,
                                   new_socks_lock=self.new_socks_lock,
                                   raise_event=self.evt_new_talk_conn)
        self.new_talker_server.setDaemon(1)        
        self.new_talker_server.start()

        #
        # This thread checks active VC_LISTEN sockets to see if they have
        # received new data.
        #
        self.ready_socks_checker = CheckReadySocksThread(socks_to_check=self.active_listen_socks, ready_socks=self.ready_socks, ready_socks_lock=self.ready_socks_lock, raise_event=self.evt_sockets_ready)
        self.ready_socks_checker.setDaemon(1)
        self.ready_socks_checker.start()

        
        #
        # This is the event loop. It is based on a recipe found at:
        # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/82236        
        #
        TIMEOUT = 200  #msecs
#        TIMEOUT = 5000  #msecs
        counter = 0
        while 1:		
            rc = win32event.MsgWaitForMultipleObjects(
		        (self.evt_new_listen_conn, self.evt_new_talk_conn,
                         self.evt_sockets_ready, self.evt_quit), 
                        0, # wait for all = false
			win32event.QS_ALLEVENTS, # type of input
			TIMEOUT) #  (or win32event.INFINITE)


            if rc == win32event.WAIT_OBJECT_0:
                #
                # A new VC_LISTEN connection was opened
                #
                debug.trace('ServerSingleThread.run', 'got evt_new_listen_conn')
                self.handshake_listen_socks()

            elif rc == win32event.WAIT_OBJECT_0+1:
                #
                # A new VC_TALK connection was opened
                #
                debug.trace('ServerSingleThread.run', 'got evt_new_talk_conn')
                self.handshake_talk_socks()

                
            elif rc == win32event.WAIT_OBJECT_0+2:
                #
                # Some of the active VC_LISTEN sockets have received data
                #
                debug.trace('ServerSingleThread.run', 'got evt_sockets_ready')
                self.process_ready_socks()

            elif rc == win32event.WAIT_OBJECT_0+3:
                #
                # Server is shutting down. Exit the event loop.
                #
                debug.trace('ServerSingleThread.run', 'got evt_quit')
                break
                
            elif rc == win32event.WAIT_OBJECT_0+4:
                # A windows message is waiting - take care of it.
                # (Don't ask me why a WAIT_OBJECT_MSG isn't defined < WAIT_OBJECT_0)
                # Note: this must be done for COM and other windowsy
                #   things to work.
#                debug.trace('ServerSingleThread.run', 'forwarding unknown message')
                if pythoncom.PumpWaitingMessages():
                    break # wm_quit
                
            elif rc == win32event.WAIT_TIMEOUT:
                # Our timeout has elapsed.
                # Do some work here (e.g, poll something can you can't thread)
                #   or just feel good to be alive.
                # Good place to call watchdog(). (Editor's note: See my "thread lifetime" recepie.)
                pass
#                debug.trace('ServerSingleThread.run', 'nothing to do, counter=%s' % counter)
            else:
                raise RuntimeError( "unexpected win32wait return value")

            counter = counter + 1

##############################################################################
# Classes for new version of the server with abstract interfaces for
# sending messages between threads.
#
# calls to/from natlink are still handled by the main thread, like in
# ServerSingleThread.
##############################################################################

class ServerMainThread(Object.Object):
    """Abstract base class for the main thread of a TCP/IP based 
    VoiceCode server.

    ServerMainThread will launch several other threads:
    
    ListenNewEditorsThread listens for new editors to connect on the
    VC_LISTEN port.  It puts the new socket on the new_listen_socks
    Queue, and notifies ServerMainThread through a InterThreadEvent.
    This event will ensure that handshake_listen_socks is called to do
    the initial handshaking.  Once the listen socket has completed
    the initial handshaking, handshake_listen_socks appends it to the 
    pending_listen_socks list.  The editor will then open a 
    
    NewConnListThread listens for the talker connections on the VC_TALK
    port.  It appends the new socket to the new_talk_socks list and 
    notifies ServerMainThread through a InterThreadEvent.  This event
    will ensure that handshake_talk_socks is called.
    handshake_talk_socks will go through the new_talk_socks list and
    pair them up with the elements of the pending_listen_socks with
    matching IDs, and will call package_sock_pair.  
    
    package_sock_pair will create a ListenAndQueueMsgsThread to listen 
    for data on the listen_sock and queue complete messages.  
    package_sock_pair will also create an instance of a subclass of 
    AppStateMessaging, with a MixedMessenger which sends messages 
    directly on the talk_sock, but reads them from this queue.  
    The LAQM Thread also notifies ServerMainThread using a
    SocketHasDataEvent.  This event will ensure that
    process_ready_socks is called, which will call
    listen_one_transaction on the appropriate AppStateMessaging.
    AppStateMessaging will also get messages from the editor off of the
    queue when it synchronizes with the editor at recognition starting

    The communication between the subsidiary threads and the main
    thread requires the event objects described above and a message loop 
    which receives messages from these event objects and calls the proper 
    ServerMainThread methods.  Some subclasses of ServerMainThread
    (ServerOldMediatorWin32Evt) supply these events themselves, and 
    have an internal message loop.  Others require an external object,
    which owns ServerMainThread (directly or indirectly), to supply the 
    event objects and the message loop.  the events to be 
    
    This flexibility means that ServerMainThread relies on
    virtual functions to create the subsidiary threads.

    **INSTANCE ATTRIBUTES**

    [Queue] *new_listen_socks* -- Queue from which to get any new connections.
    Each item is [(socket, (STR, STR, STR))] 
    a 2ple consiting of a new (uninitialised) socket on the VC_LISTEN
    port, and data about that socket. The data is itself a 3ple
    consisting of: (a) identifier of external editor, (b) name of the
    external editor and (c) window handle of the external editor.

    *[(socket, [None, None, None])] new_talk_socks* -- the socket
    element of each 2ple is a new (uninitialised) socked
     on the VC_TALK port.  The data part of the 2ple is useless.

    [(socket, (STR, STR, STR))] *pending_listen_socks=[]* -- Each entry is
    a 2ple consiting of a new (uninitialised) socket on the VC_LISTEN
    port, and data about that socket. The data is itself a 3ple
    consisting of: (a) identifier of external editor, (b) name of the
    external editor and (c) window handle of the external editor.
    Socks on the pending_listen_socks list have been through
    handshaking, but have not yet been packaged with corresponding
    talk_socks.
    
    *threading.lock new_socks_lock* -- Lock used to make sure that the
     main thread doesn't access the *new_talk_socks* list at the same 
     time as the thread that listen for new socket connections.

    [ListenNewEditorsThread] *new_listener_server* -- Thread that
    listens for new connections on the VC_LISTEN port.

    [NewConnListThread] *new_talker_server* -- Thread that
    listens for new connections on the VC_TALK port.

    {STR : ListenAndQueueMsgsThread} *data_threads* -- map from unique 
    socket IDs to threads which poll for data from the listen messenger
  
    {STR : Event} *connection_ending* -- map from each unique 
    socket IDs to a corresponding threading.Event 
    used to signal to the corresponding data thread that the connection is 
    ending, or the server is quitting

    {STR : Event} *server_quitting* -- threading.Event used to signal to other
    threads that the server is quitting (or to let them sleep until a 
    timeout, or such a signal).
    
    *AppStateFactory editor_factory* -- factory for creating new
    AppStateMessaging instances
  
    **CLASS ATTRIBUTES**
    
    *none* -- 

    ..[AppStateMessaging] file:///./AppStateMessaging.AppStateMessaging.html
    ..[ListenForNewListenersThread] file:///./tcp_server.ListenForNewListenersThread.html
    ..[ListenForNewTalkersThread] file:///./tcp_server.ListenForNewTalkersThread.html
    """
    
    def __init__(self, editor_factory, **args_super):
        self.deep_construct(ServerMainThread, 
                            {'pending_listen_socks': [],
                             'new_talk_socks': [],
                             'new_socks_lock': threading.Lock(),
			     'new_listen_socks': Queue.Queue(5),
			     'data_threads': {},
			     'new_listener_server': None,
			     'new_talker_server': None,
			     'connection_ending': {},
			     'server_quitting': threading.Event(),
			     'editor_factory': editor_factory
                             }, 
                            args_super)
      
    def quit(self):
	"""Perform any cleanup prior to quitting.  Called when the main 
	thread has exited its event loop.  Subclasses which override
	this method should be sure to call their parent class's version.

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	for id in self.data_threads.keys():
	    self.deactivate_data_thread(id)

    def new_listener_thread(self):
        """creates a new ListenNewEditorsThread to monitor 
	for new connections on the VC_LISTEN port.

	**INPUTS**

	*none*

	**OUTPUTS**

	*[ListenNewEditorsThread]* -- Thread that
	listens for new connections on the VC_LISTEN port.

	..[ListenForNewListenersThread] 
	file:///./tcp_server.ListenForNewListenersThread.html
	"""
	debug.virtual('ServerMainThread.new_listener_thread')

    def new_talker_thread(self):
        """creates a new NewConnListThread to monitor 
	for new connections on the VC_TALK port.

	**INPUTS**

	*none*

	**OUTPUTS**

	*[NewConnListThread]* -- Thread that
	listens for new connections on the VC_TALK port.

	..[NewConnListThread] 
	file:///./tcp_server.NewConnListThread.html
	"""
	debug.virtual('ServerMainThread.new_listener_thread')


    def data_event(self, id):
	"""virtual method which supplies a data_event for ServerMainThread 
	subclasses 
        
        **INPUTS**

        STR *id* -- The unique ID of the listen socket
        
        **OUTPUTS**
        
        *SocketHasDataEvent* -- the data event which will allow the
	data thread to ensure that process_ready_socks is called.
	"""
	debug.virtual('ServerMainThread.data_event')

    def new_data_thread(self, id, listen_sock, connection_ending):
        """creates a new ListenAndQueueMsgsThread to monitor the
	listen_sock
        
        **INPUTS**

        STR *id* -- The unique ID of the listen socket
        
        socket *listen_sock* -- The listen socket

	Event *connection_ending* -- threading.Event 
	used to signal to the data thread that the connection is 
	ending, or the server is quitting
        
        **OUTPUTS**
        
        [ListenAndQueueMsgsThread] -- the new threading.Thread object

        ..[ListenAndQueueMsgsThread] 
	file:///./tcp_server.ListenAndQueueMsgsThread.html"""        
	data_event = self.data_event(id)
	return self.new_data_thread_given_event(id, listen_sock, data_event, 
	    connection_ending)

    def new_data_thread_given_event(self, id, listen_sock, data_event,
	    connection_ending):
        """creates a new ListenAndQueueMsgsThread to monitor the
	listen_sock
        
        **INPUTS**

        STR *id* -- The unique ID of the listen socket
        
        socket *listen_sock* -- The listen socket

	SocketHasDataEvent *data_event* -- the SocketHasDataEvent event
	to pass to the new thread

	Event *connection_ending* -- threading.Event 
	used to signal to the data thread that the connection is 
	ending, or the server is quitting
        
        **OUTPUTS**
        
        [ListenAndQueueMsgsThread] -- the new threading.Thread object

        ..[ListenAndQueueMsgsThread] 
	file:///./tcp_server.ListenAndQueueMsgsThread.html"""        
	a_msgr = messaging.messenger_factory(listen_sock, sleep = 0.05)
	queue = Queue.Queue(10)
	broken_connection = ('connection_broken', {})
	thread = ListenAndQueueMsgsThread( a_msgr, queue, data_event,
	    connection_ending, broken_connection)
	return thread
      
    def deactivate_data_thread(self, id):
	"""method to deactivate the data thread associated with a 
	given socket id.  **Note:** if the thread is daemonic (will not
	prevent the mediator process from ending), and the particular 
	thread class used doesn't provide a way to kill the thread, 
	this method may simply ensure that no messages from that thread
	are processed.

	**INPUTS**

        STR *id* -- The unique identifier assigned by VoiceCode to
        the socket pair.

	**OUTPUTS**

	*none*
	"""
# we don't currently have a perfect way of deactivating the thread before 
# it puts any more messages on the Queue.  However,
# process_ready_socks does check to see if the id's it receives in the
# ready_socks argument are included in active_meds.keys().  Therefore,
# as long as the caller also removes the corresponding mediator, this
# may be sufficient.
	self.connection_ending[id].set()

    def _new_instance(self, id, instance):
        """add a new AppStateMessaging.  Called internally by
	package_sock_pair
        
        **INPUTS**
        
        STR *id* -- The unique ID of the listen socket

	AppStateMessaging *instance*  -- the new instance

        **OUTPUTS**
        
	*BOOL* -- false if the server should exit (because we're done
	running the test suite)
	"""
	debug.virtual('ServerMainThread._new_instance')
        
    def known_instance(self, id):
	"""returns a reference to the AppStateMessaging instance 
	associated with  the given ID
        **INPUTS**
        
        STR *id* -- The unique ID of the listen socket

        **OUTPUTS**

	*AppStateMessaging* -- the corresponding instance, or None if
	the id is unknown
        
        *none*
	"""
	debug.virtual('ServerMainThread.known_instance')

    def package_sock_pair(self, id, app_name, window, listen_sock, talk_sock):
        
        """Packages a listen and talk socket into an
        [AppStateMessaging] instance
        
        **INPUTS**
        
        STR *id* -- The unique identifier assigned by VoiceCode to
        that socket pair.

        STR *app_name* -- Name of the external editor.

        STR *window* -- Window handle for the external editor.
        
        socket *listen_sock* -- The listen socket
        
        socket *talk_sock* -- The talk socket
        

        **OUTPUTS**
        
	*BOOL* -- false if the server should exit (because we're done
	running the test suite)

        ..[AppStateMessaging] file:///./messaging.AppStateMessaging.html"""        
        
	disconnect_event = threading.Event()
	self.connection_ending[id] = disconnect_event
	data_thread = self.new_data_thread(id, listen_sock, disconnect_event)
	messages = data_thread.message_queue()

        talk_msgr = messaging.messenger_factory(talk_sock)        
        listen_response_msgr = messaging.messenger_factory(listen_sock)        
        listen_msgr = messaging.MixedMessenger(listen_response_msgr, messages)
        an_app_state = self.editor_factory.new_instance(app_name, id, 
	    listen_msgr, talk_msgr)

	data_thread.setDaemon(1)
	data_thread.start()

        #
        # Give external editor a chance to configure the AppStateMessaging
        #
        an_app_state.config_from_external()

	stay_alive = self._new_instance(id, an_app_state)
	if stay_alive:
	    self.data_threads[id] = data_thread
	    return 1
	else:
	    self.deactivate_data_thread(id)
	    del data_thread
	    an_app_state.cleanup()
	    return 0
	
    def handshake_listen_socks(self):
        """Invoked when a new socket connection was opened on VC_LISTEN port.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        #
        # Get window handle of active application.
        #
        window = natlink.getCurrentModule()[2]


        #
        # Assume active window is the application that opened the last
        # socket conneciton in the list self.new_listen_socks.  This
        # may not hold if two editors connect to VoiceCode back to back
        # and rapidly.

#  handshake_listen_socks should never be called if there isn't a new listen 
#  sock, but just in case we catch the exception and ignore it
	try:
# 0 means don't block
	    most_rec_sock = self.new_listen_socks.get(0)
	except Queue.Empty:
	    return
        
        #
        # Create a temporary messenger for handshaking
        #
        a_messenger = messaging.messenger_factory(most_rec_sock)
               
        #
        # Get the external application name
        #
        a_messenger.send_mess('send_app_name')
        mess = a_messenger.get_mess(expect=['app_name'])
        app_name = mess[1]['value']
                
        #
        # Assign a random ID to the external editor, and send it on the socket
        # connection.
        #
        id = '%s_%s' % (app_name, repr(whrandom.random()))
        a_messenger.send_mess('your_id_is', {'value': id})
        a_messenger.get_mess(expect=['ok'])
        
        #
        # Assign window, id and app_name to the last socket in the list of
        # new listen sockets
        #
	most_rec_data = (id, app_name, window)
        
# using this lock shouldn't be necessary, since only
# handshake_talk_socks is the only other one accessing
# pending_listen_socks, and it runs in the main thread just like we do,
# but just in case.
        self.new_socks_lock.acquire()

	self.pending_listen_socks.append((most_rec_sock, most_rec_data))

        self.new_socks_lock.release()
        

    def handshake_talk_socks(self):
        
        """Does a handshake on a the new socket connection that were opened on
        VC_LISTEN port.
        
        **INPUTS**
        
        *none*

        **OUTPUTS**
        
	*BOOL* -- false if the server should exit (because we're done
	running the test suite)
        """

	stay_alive = 1
	self.new_socks_lock.acquire()

        #
        # Loop through list of new VC_TALK sockets, handshake with them
        # and package them into an AppState instance with their corresponding
        # VC_LISTEN sockets.
        #
        ii = 0
        while ii < len(self.new_talk_socks):            

            (talk_sock, dummy) = self.new_talk_socks[ii]
        
            #
            # Shake hands with that VC_TALK socket.
            # Get the ID of external editor that started this VC_TALK socket
            #
            a_msgr = messaging.messenger_factory(talk_sock)
            a_msgr.send_mess('send_id')
            mess = a_msgr.get_mess(expect=['my_id_is'])
            id = mess[1]['value']

            #
            # Find the corresponding VC_LISTEN socket
            #
            found = None
            jj = 0
            while jj < len(self.pending_listen_socks):
                (listen_sock, listen_data) = self.pending_listen_socks[jj]
                (a_listen_id, app_name, window) = listen_data
                if a_listen_id == id:
                    #
                    # Found it. Remove the two sockets from the list of
                    # new connections.
                    #
                    found = (listen_sock, app_name, window)
                    del self.pending_listen_socks[jj]
                    del self.new_talk_socks[ii]
                    break

                jj = jj + 1
                
            if found != None:
                stay_alive = self.package_sock_pair(id, app_name, 
		    window, listen_sock, talk_sock)
                        
        self.new_socks_lock.release()        
	return stay_alive


    def process_ready_socks(self, ready_socks):
        """Processes socket connections that have received new data.
        
        **INPUTS**

        [STR] *ready_socks*  =[] -- List of IDs of sockets which may
	have messages waiting
        
        **OUTPUTS**
        
        *none* -- 
        """

	for id in ready_socks:
            an_app_state = self.known_instance(id)
	    if an_app_state != None:
		an_app_state.listen_one_transaction()

    def start_other_threads(self, listener_evt, talker_evt):
        """method called to start the secondary threads which
	monitor the VC_TALK and VC_LISTEN ports.  These threads communicate
        with the main thread by means of InterThreadEvent objects, to
	let the main thread know to initialize them.

	These tasks are handled by separate threads because they can
	block.   The secondary threads do not do the initialization
	directly because that involves invoking some natlink methods, 
	and Natlink does not behave well outside of the main thread.
        
        **INPUTS**
        
	*InterThreadEvent* listener_evt -- event object for the
	ListenNewEditorsThread to use to notify the main thread that a
	new editor has connected on the VC_LISTEN port, and that
	handshake_listen_socks should be called
	
	*InterThreadEvent* talker_evt -- event object for the
	NewConnListThread to use to notify the main thread that a
	new talker connection has been established on the VC_TALK port, 
	and that handshake_talk_socks should be called

        **OUTPUTS**
        
        *none* 
        """

        #
        # Start threads for monitoring socket connections.
        # We make the threads daemonic so that the program exits automaticall
        # when only those threads are left
        #

        #
        # This thread listens for new socket connections on VC_LISTEN port.
        # New connections are stored in a list, so that the main thread
        # can later on initialise them.
        #
        self.new_listener_server = \
           ListenNewEditorsThread(port = VC_LISTEN_PORT, event = listener_evt,
	       new_socks=self.new_listen_socks)
        self.new_listener_server.setDaemon(1)
        self.new_listener_server.start()

        #
        # This thread listens for new socket connections on VC_TALK port.
        # New connections are stored in a list, so that the main thread
        # can later on initialise them.        
        #
        self.new_talker_server = \
           NewConnListThread(port = VC_TALK_PORT, event = talker_evt,
	       new_socks=self.new_talk_socks,
	       new_socks_lock=self.new_socks_lock)
        self.new_talker_server.setDaemon(1)        
        self.new_talker_server.start()

class ServerOldMediator(ServerMainThread):
    """partial implementation of ServerMainThread using the old MediatorObject

    **INSTANCE ATTRIBUTES**

    {STR : MediatorObject} *active_meds* -- map from unique socket IDs
    to active mediators driving external edtiors.
    
    STR *test_suite=None* -- If not *None*, then upon connection by a
    new editor run regression test suite *test_suite*.
    """
    
    def __init__(self, test_suite = None, **args_super):
        self.deep_construct(ServerOldMediator, 
                            {'active_meds': {},
			     'test_suite': test_suite
                             }, 
                            args_super)
    def quit(self):
	"""Perform any cleanup prior to quitting.  Called when the main 
	thread has exited its event loop.  Subclasses which override
	this method should be sure to call their parent class's version.

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	ServerMainThread.quit(self)
	for id in self.active_meds.keys():
# except for editors running regression tests, the MediatorObject should
# own its editor, so quitting the former should cleanup the editor
	    self._destroy_mediator(id)

#       in their current implementation, the new_talker and new_listener
#       threads block while waiting for new connections, so there is no
#       way to tell them to quit.  We just rely on the fact that they
#       are daemon threads which won't prevent the program from
#       quitting.  We are no longer in the message loop, so any events
#       they continue to send will be ignored.

    def _new_instance(self, id, instance):
        """add a new AppStateMessaging.  Called internally by
	package_sock_pair
        
        **INPUTS**
        
        STR *id* -- The unique ID of the listen socket

	AppStateMessaging *instance*  -- the new instance

        **OUTPUTS**
        
	*BOOL* -- false if the server should exit (because we're done
	running the test suite)
	"""
        if self.test_suite != None:
            mediator.init_simulator_regression(on_app=instance)
	    instance.print_buff_when_changed = 1
            args = [self.test_suite]
            auto_test.run(args)

	    # notify data thread that we are quitting
	    self.server_quitting.set()

	    # notify external editor that we are quitting
	    instance.talk_msgr.send_mess("terminating")

	    if mediator.the_mediator:
		mediator.the_mediator.quit(clean_sr_voc=0, save_speech_files=0, 
		    disconnect=0)
		mediator.the_mediator = None

            # return 0 to quit the server
	    return 0
        else:
            exclusive = 1
            allResults = 0
            mediator.init_simulator(on_app=instance, 
	        disable_dlg_select_symbol_matches=1, window=window, 
		exclusive = exclusive, allResults = allResults, 
		owns_app = 1, owner = self, id = id)


	    self.active_meds[id] = mediator.the_mediator
	    mediator.the_mediator = None
	    return 1

    def known_instance(self, id):
	"""returns a reference to the AppStateMessaging instance 
	associated with  the given ID
    
        **INPUTS**
        
        STR *id* -- The unique ID of the listen socket

        **OUTPUTS**

	*AppStateMessaging* -- the corresponding instance, or None if
	the id is unknown
        
        *none*
	"""
	if self.active_meds.has_key(id):
	    return self.active_meds[id].app
	return None
    
    def delete_instance_cbk(self, id, unexpected = 0):
        """callback to let MediatorObject notify us that the
	corresponding external editor has exited or disconnected from
	the mediator.  Only used with the old MediatorObject

	**INPUTS**

        STR *id* -- The unique identifier assigned by VoiceCode to
        that socket pair.
      
 	*BOOL unexpected* -- 1 if the editor broke the connection
	without first sending an editor_disconnecting message

	**OUTPUTS**

	*none*
	"""
	if self.active_meds.has_key(id):
	    self.deactivate_data_thread(id)
	    self._destroy_mediator(id)
	    del active_meds[id]
	    if unexpected:
	        sys.stderr.write('Mediator %d disconnected unexpectedly\n' \
		    % id)


    def _destroy_mediator(self, id):
	"""private method to destroy one the old MediatorObject
	corresponding to the given id

	**INPUTS**

        STR *id* -- The unique identifier assigned by VoiceCode to
        that mediator.

	**OUTPUTS**

	*none*
	"""
	self.active_meds[id].quit(clean_sr_voc=0, save_speech_files=0, 
	    disconnect=0)
	
class ServerOldMediatorIntLoop(ServerOldMediator):
    """concrete subclass of ServerOldMediator(ServerMainThread) which uses 
    win32event events to communicate with an internal Windows
    message loop.

    **INSTANCE ATTRIBUTES**

    *PyHandle evt_new_listen_conn* -- Win32 event raised when a new
     socket connection is opened on VC_LISTEN port.
    
    *PyHandle evt_new_talk_conn* -- Win32 event raised when a new
     socket connection is opened on VC_TALK port.
    
    *PyHandle evt_sockets_ready* -- Win32 event raised when one of the
     active VC_LISTEN sockets has unread data.
    """
    def __init__(self, **args_super):
        self.deep_construct(ServerOldMediatorIntLoop, 
                            {'evt_new_listen_conn': 
			         win32event.CreateEvent(None, 0, 0, None),
                             'evt_new_talk_conn': 
			         win32event.CreateEvent(None, 0, 0, None),
                             'evt_sockets_ready': 
			         win32event.CreateEvent(None, 0, 0, None)
                             }, 
                            args_super)

    def data_event(self, id):
	"""virtual method which supplies a data_event for ServerMainThread 
	subclasses 
        
        **INPUTS**

        STR *id* -- The unique ID of the listen socket
        
        **OUTPUTS**
        
        *SocketHasDataEvent* -- the data event which will allow the
	data thread to ensure that process_ready_socks is called.
	"""
	return Win32SomeSocketHasDataEvent(self.evt_sockets_ready)


    def run(self):
        """Start the server
        This method calls runs 2 threads that raise Win32 events respectively 
	when:

        - a request for a new connections on VC_LISTEN port is
          received (*self.evt_new_listen_conn* event).

        - a request for a new connections on VC_PORT port is received
          (*self.evt_new_talk_conn* event)

	It also runs an additional thread for each connected editor,
	once both the listen and talk sockets have been created and
	packaged by package_sock_pair, which uses the
	self.evt_sockets_ready event.

        These events (plus *self.evt_quit*) are handled inside an
        event loop run by this method.

        We need this event loop so that speech events can be processed
        (actually, I think the speech events are just forwarded to
        NatSpeak by calling pythoncom.PumpWaitingMessages()).

        Also, the reason why the above four events are not processed
        directly in the threads that raise them, is that processing
        the events involves invoking some natlink methods, and Natlink
        does not behave well outside of the main thread.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        # Start threads for monitoring socket connections.

	listener_evt = Win32InterThreadEvent(self.evt_new_listen_conn)
	talker_evt = Win32InterThreadEvent(self.evt_new_talk_conn)
	self.start_other_threads(listener_evt, talker_evt)

        #
        # This is the event loop. It is based on a recipe found at:
        # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/82236        
        #
        TIMEOUT = 200  #msecs
#        TIMEOUT = 5000  #msecs
        counter = 0
	events = (self.evt_new_listen_conn, self.evt_new_talk_conn,
                         self.evt_sockets_ready), 
        while 1:		
            rc = win32event.MsgWaitForMultipleObjects(
		        (self.evt_new_listen_conn, self.evt_new_talk_conn,
                         self.evt_sockets_ready), 
#                         self.evt_sockets_ready, self.evt_quit), 
                        0, # wait for all = false
			win32event.QS_ALLEVENTS, # type of input
			TIMEOUT) #  (or win32event.INFINITE)


            if rc == win32event.WAIT_OBJECT_0:
                #
                # A new VC_LISTEN connection was opened
                #
                debug.trace('ServerSingleThread.run', 'got evt_new_listen_conn')
                self.handshake_listen_socks()

            elif rc == win32event.WAIT_OBJECT_0+1:
                #
                # A new VC_TALK connection was opened
                #
                debug.trace('ServerSingleThread.run', 'got evt_new_talk_conn')
                if not self.handshake_talk_socks():
		    break

                
            elif rc == win32event.WAIT_OBJECT_0+2:
                #
                # Some of the active VC_LISTEN sockets have received data
                #
                debug.trace('ServerSingleThread.run', 'got evt_sockets_ready')
# ServerMainThread.process_ready_socks takes a list of sockets to check,
# but win32event.Event doesn't seem to provide any way of sending data
# with the event.  Really, I should add a ready_socks list and lock,
# like in ServerSingleThread.  However, for now, just check all sockets.
# process_ready_socks uses Queue's and avoids blocking if there are no
# messages, so this is safe, if slightly inefficient.
                self.process_ready_socks(self.data_threads.keys())

            elif rc == win32event.WAIT_OBJECT_0+3:
                #
                # Server is shutting down. Exit the event loop.
                #
                debug.trace('ServerSingleThread.run', 'got evt_quit')
                break
                
            elif rc == win32event.WAIT_OBJECT_0 + len(events):
                # A windows message is waiting - take care of it.
                # (Don't ask me why a WAIT_OBJECT_MSG isn't defined < WAIT_OBJECT_0)
                # Note: this must be done for COM and other windowsy
                #   things to work.
#                debug.trace('ServerSingleThread.run', 'forwarding unknown message')
                if pythoncom.PumpWaitingMessages():
                    break # wm_quit
                
            elif rc == win32event.WAIT_TIMEOUT:
                # Our timeout has elapsed.
                # Do some work here (e.g, poll something can you can't thread)
                #   or just feel good to be alive.
                # Good place to call watchdog(). (Editor's note: See my "thread lifetime" recepie.)
                pass
#                debug.trace('ServerSingleThread.run', 'nothing to do, counter=%s' % counter)
            else:
                raise RuntimeError( "unexpected win32wait return value")

            counter = counter + 1

	self.quit()




class DataEvtSource(Object.Object):
    """abstract class which supplies a data_event for ServerMainThread 
    subclasses with external message loops.

    **INSTANCE ATTRIBUTES**

    *none*
    """
    def __init__(self, **args_super):
        self.deep_construct(DataEvtSource, 
                            {}, 
                            args_super)
    def data_event(self, id):
	"""virtual method which supplies a data_event for ServerMainThread 
	subclasses 
        
        **INPUTS**

        STR *id* -- The unique ID of the listen socket
        
        **OUTPUTS**
        
        *SocketHasDataEvent* -- the data event which will allow the
	data thread to ensure that process_ready_socks is called.
	"""
	debug.virtual('DataEvtSource.data_event')


class ServerOldMediatorExtLoop(ServerOldMediator):
    """partial implementation of ServerOldMediator(ServerMainThread) which
    uses an external message loop and queries its owner for data events

    **INSTANCE ATTRIBUTES**

    *ExtLoop owner* -- the owner of the server

    """
    def __init__(self, owner, **args_super):
        self.deep_construct(ServerOldMediatorExtLoop, 
                            {'owner': owner}, 
                            args_super)

    def data_event(self, id):
	"""virtual method which supplies a data_event for ServerMainThread 
	subclasses 
        
        **INPUTS**

        STR *id* -- The unique ID of the listen socket
        
        **OUTPUTS**
        
        *SocketHasDataEvent* -- the data event which will allow the
	data thread to ensure that process_ready_socks is called.
	"""
	return self.owner.data_event(id)

class ExtLoopWin32(Object.Object):
    """class providing an external win32 message message loop for
    ServerOldMediator using win32event

    **INSTANCE ATTRIBUTES**

    *ServerOldMediator server* -- the underlying server

    *PyHandle evt_new_listen_conn* -- Win32 event raised when a new
     socket connection is opened on VC_LISTEN port.
    
    *PyHandle evt_new_talk_conn* -- Win32 event raised when a new
     socket connection is opened on VC_TALK port.
    
    *PyHandle evt_sockets_ready* -- Win32 event raised when one of the
     active VC_LISTEN sockets has unread data.

    STR *test_suite=None* -- If not *None*, then upon connection by a
    new editor run regression test suite *test_suite*.
    """
    def __init__(self, test_suite = None, local_srv = 0, **args_super):
        self.deep_construct(ExtLoopWin32, 
                            {'test_suite': test_suite,
			     'server': None,
			     'evt_new_listen_conn': 
			         win32event.CreateEvent(None, 0, 0, None),
                             'evt_new_talk_conn': 
			         win32event.CreateEvent(None, 0, 0, None),
                             'evt_sockets_ready': 
			         win32event.CreateEvent(None, 0, 0, None)
                             }, 
                            args_super)
	factory = AppStateFactorySimple(use_local_srv = local_srv)
	self.server = ServerOldMediatorExtLoop(owner = self,
			     test_suite = test_suite, 
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
	return Win32SomeSocketHasDataEvent(self.evt_sockets_ready)

    def run(self):
        """Start the server as well as the ExtLoopWin32 message loop.

	The server will run 2 threads that raise Win32 events respectively 
	when:

        - a request for a new connections on VC_LISTEN port is
          received (*self.evt_new_listen_conn* event).

        - a request for a new connections on VC_PORT port is received
          (*self.evt_new_talk_conn* event)

	It will also runs an additional thread for each connected editor,
	once both the listen and talk sockets have been created and
	packaged by package_sock_pair, which uses the
	self.evt_sockets_ready event.

        These events (plus *self.evt_quit*) are handled inside an
        event loop run by this method.

        We need this event loop so that speech events can be processed
        (actually, I think the speech events are just forwarded to
        NatSpeak by calling pythoncom.PumpWaitingMessages()).

        Also, the reason why the above four events are not processed
        directly in the threads that raise them, is that processing
        the events involves invoking some natlink methods, and Natlink
        does not behave well outside of the main thread.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        # Start threads for monitoring socket connections.

	listener_evt = Win32InterThreadEvent(self.evt_new_listen_conn)
	talker_evt = Win32InterThreadEvent(self.evt_new_talk_conn)
	self.server.start_other_threads(listener_evt, talker_evt)

        #
        # This is the event loop. It is based on a recipe found at:
        # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/82236        
        #
        TIMEOUT = 200  #msecs
#        TIMEOUT = 5000  #msecs
        counter = 0
	events = (self.evt_new_listen_conn, self.evt_new_talk_conn,
                         self.evt_sockets_ready), 
        while 1:		
            rc = win32event.MsgWaitForMultipleObjects(
		        (self.evt_new_listen_conn, self.evt_new_talk_conn,
                         self.evt_sockets_ready), 
#                         self.evt_sockets_ready, self.evt_quit), 
                        0, # wait for all = false
			win32event.QS_ALLEVENTS, # type of input
			TIMEOUT) #  (or win32event.INFINITE)


            if rc == win32event.WAIT_OBJECT_0:
                #
                # A new VC_LISTEN connection was opened
                #
                debug.trace('ExtLoopWin32.run', 'got evt_new_listen_conn')
                self.server.handshake_listen_socks()

            elif rc == win32event.WAIT_OBJECT_0+1:
                #
                # A new VC_TALK connection was opened
                #
                debug.trace('ExtLoopWin32.run', 'got evt_new_talk_conn')
                if not self.server.handshake_talk_socks():
		    break

                
            elif rc == win32event.WAIT_OBJECT_0+2:
                #
                # Some of the active VC_LISTEN sockets have received data
                #
                debug.trace('ExtLoopWin32.run', 'got evt_sockets_ready')
# ServerMainThread.process_ready_socks takes a list of sockets to check,
# but win32event.Event doesn't seem to provide any way of sending data
# with the event.  Really, I should add a ready_socks list and lock,
# like in ServerSingleThread.  However, for now, just check all sockets.
# process_ready_socks uses Queue's and avoids blocking if there are no
# messages, so this is safe, if slightly inefficient.
                self.server.process_ready_socks(self.data_threads.keys())

            elif rc == win32event.WAIT_OBJECT_0+3:
                #
                # Server is shutting down. Exit the event loop.
                #
                debug.trace('ExtLoopWin32.run', 'got evt_quit')
                break
                
            elif rc == win32event.WAIT_OBJECT_0 + len(events):
                # A windows message is waiting - take care of it.
                # (Don't ask me why a WAIT_OBJECT_MSG isn't defined < WAIT_OBJECT_0)
                # Note: this must be done for COM and other windowsy
                #   things to work.
#                debug.trace('ExtLoopWin32.run', 'forwarding unknown message')
                if pythoncom.PumpWaitingMessages():
                    break # wm_quit
                
            elif rc == win32event.WAIT_TIMEOUT:
                # Our timeout has elapsed.
                # Do some work here (e.g, poll something can you can't thread)
                #   or just feel good to be alive.
                # Good place to call watchdog(). (Editor's note: See my "thread lifetime" recepie.)
                pass
#                debug.trace('ExtLoopWin32.run', 'nothing to do, counter=%s' % counter)
            else:
                raise RuntimeError( "unexpected win32wait return value")

            counter = counter + 1

	self.server.quit()




##############################################################################
# start test standalone server
##############################################################################
def run_int_server(test_suite=None, local_srv = 1):
    """Start a ServerMainThread with internal message loop using
    win32event and the old MediatorObject.
    """

    sys.stderr.write('running ServerOldMediatorIntLoop\n')
    print 'running ServerOldMediatorIntLoop'
    factory = AppStateFactorySimple(use_local_srv = local_srv)
    a_server = ServerOldMediatorIntLoop(test_suite = test_suite,
	editor_factory = factory)
        
    a_server.run()
    
def run_ext_server(test_suite=None, local_srv = 1):
    """Start a ServerMainThread with external message loop using
    win32event and the old MediatorObject.
    """

    sys.stderr.write('running ExtLoopWin32 with ServerOldMediator\n')
    print 'running ExtLoopWin32 with ServerOldMediator'
    a_loop = ExtLoopWin32(test_suite, local_srv = local_srv)

    a_loop.run()
    
def run_smt_server(test_suite=None, local_srv = 1):
    """Start a ServerMainThread with internal message loop using
    win32event and the old MediatorObject.
    """
    run_ext_server(test_suite, local_srv = local_srv)
    
def run_server(test_suite=None, local_srv = 1):
    """Start a single thread, single process server.
    """

    factory = AppStateFactorySimple(use_local_srv = local_srv)
    a_server = ServerSingleThread(editor_factory = factory)
    a_server.test_suite = test_suite
        
    a_server.run()
    


def help():
    print """
Usage: python tcp_server.py [OPTIONS]

Runs the VoiceCode TCP server.

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

-r :
   Let remote editor handle indentation, line-numbering (if it can)

--sst :
   Use ServerSingleThread (default)

--int : 
   Run ServerOldMediatorIntLoop, which uses old MediatorObject, and 
   an internal win32event message loop

--ext :
   Run ExtLoopWin32 and ServerOldMediatorExtLoop, which uses old 
   MediatorObject and an external win32event message loop

--smt :
   Use the latest ServerMainThread version (currently --ext)
    """

if __name__ == '__main__':


    opts, args = util.gopt(['h', None, 't=', None, 'r', None,
			    'int', None, 'sst', None,
                            'ext', None, 'smt', None])

    if opts['t'] != None:        
        #
        # Load definition of regression tests
        #
        tests_def_fname = posixpath.expandvars('$VCODE_HOME' + os.sep + 'Admin' + os.sep + 'tests_def.py')
        execfile(tests_def_fname)        
    
    sr_interface.connect()

    #
    # Create a global grammar manager
    #
#    the_recog_start_mgr = RecogStartMgr.RecogStartMgr()

    #
    # Start servers on the VC_LISTEN and VC_TALK ports
    #
    local_srv = 1
    if opts['r'] != None:
	local_srv = 0
    if opts['int'] != None:
	run_int_server(test_suite=opts['t'], local_srv = local_srv)
    elif opts['ext'] != None:
	run_ext_server(test_suite=opts['t'], local_srv = local_srv)
    elif opts['smt'] != None:
	run_smt_server(test_suite=opts['t'], local_srv = local_srv)
    else:
	run_server(test_suite=opts['t'], local_srv = local_srv)

    sr_interface.disconnect()
