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

import natlink, os, posixpath, pythoncom, re, select, socket
import SocketServer, string, sys, threading, time, whrandom, win32event

import AppStateEmacs, AppStateMessaging, auto_test, debug, mediator 
import messaging, Object
import AppMgr, RecogStartMgr, SourceBuffMessaging, sb_services
import sim_commands, sr_interface, util
import Queue



# Uncomment this and add some entries to active_traces if you want to 
# activate some traces.
#debug.config_traces(status="on", active_traces={'get_mess':1, 'send_mess': 1})

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
        


def messenger_factory(sock):
    """Creates a messenger from proper compenents
    
    **INPUTS**
    
    *socket sock* -- Socket to use for creating the messenger
    
    
    **OUTPUTS**
    
    [Messenger] *a_messenger* -- The created [Messenger] instance

    ..[Messenger] file:///./messaging.Messenger.html"""
    

    #
    # Create a messenger
    #
    packager = messaging.MessPackager_FixedLenSeq()
    transporter = messaging.MessTransporter_Socket(sock=sock)
    encoder = messaging.MessEncoderWDDX()
    a_messenger = messaging.MessengerBasic(packager=packager, 
	transporter=transporter, encoder=encoder)        
    return a_messenger

def app_state_factory(app_name, id, listen_msgr, talk_msgr):
    """
        
    **INPUTS**
        
    STR *app_name* -- Name of the editor for which we want to
    create an [AppStateMessaging].

    STR *id* -- Unique ID of external editor connected to the [AppState]
    
    [Messenger] *listen_msgr* -- [Messenger] instance to use for the
    VC listener side of the connection.

    [Messenger] *talk_msgr* -- [Messenger] instance to use for the
    VC talker side of the connection.
        
    
    **OUTPUTS**
    
    *none* -- 

    ..[AppState] file:///./AppState.AppState.html"""

    if re.match('EdSim', app_name):
        app = AS_MessExtEdSim(app_name=app_name, id=id, listen_msgr=listen_msgr, talk_msgr=talk_msgr)
    elif re.match('emacs', app_name):
        app = AppStateEmacs.AppStateEmacs(app_name=app_name, id=id, listen_msgr=listen_msgr, talk_msgr=talk_msgr)        
    else:
        print "WARNING: Unknown editor '%s'" % app_name
        print "Connection refused"
        
    if app: app.app_name = app_name
    return app


def vc_authentification(messenger):
    """Authentifies a VoiecCode user.

    For now, this function does nothing.

    **INPUTS**

    [Messenger] *messenger* -- Messenger to be used for the connection.

    [RecogStrartMgr] *recog_mgr* -- Object responsible for
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

    [MediatorObject] *active_meds* -- Active mediators driving
    external edtiors. NOTE: This will eventually be moved to the
    grammar manager class.

    STR *test_suite=None* -- If not *None*, then upon connection by a
    new editor run regression test suite *test_suite*.

    **CLASS ATTRIBUTES**
    
    *none* -- 

    ..[AppStateMessaging] file:///./AppStateMessaging.AppStateMessaging.html
    ..[ListenForNewListenersThread] file:///./tcp_server.ListenForNewListenersThread.html
    ..[ListenForNewTalkersThread] file:///./tcp_server.ListenForNewTalkersThread.html
    """
    
    def __init__(self, test_suite=None, **args_super):
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
                             'active_meds': [],
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
        
        listen_msgr = messenger_factory(listen_sock)
        talk_msgr = messenger_factory(talk_sock)        
        an_app_state = app_state_factory(app_name, id, listen_msgr, talk_msgr)

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
        self.active_meds.append(mediator.the_mediator)
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
        a_messenger = messenger_factory(most_rec_sock)
               
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
            a_msgr = messenger_factory(talk_sock)
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

class InterThreadEvent(Object.Object):
    """abstract interface for sending a dataless message between threads.
    Particular implementations may use win32 events or wxPython custom
    events.

    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, **args):
	"""abstract base class so no arguments
	"""
	self.deep_construct(InterThreadEvent,
			    {},
			    args)
    def notify(self):
	"""send the message, and return asynchronously

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	debug.virtual('InterThreadEvent.notify')

class SocketHasDataEvent(Object.Object):
    """abstract interface for sending a message from to the main thread 
    indicating that a particular socket has data waiting to be read.

    The concrete subclass will have a reference to the particular
    socket.
    
    Particular implementations may use win32 events or wxPython custom
    events.

    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, **args):
	"""abstract base class so no arguments
	"""
	self.deep_construct(SocketHasDataEvent,
			    {},
			    args)
    def notify(self):
	"""send the message, and return asynchronously

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	debug.virtual('SocketHasDataEvent.notify')

class ListenAndQueueMsgsThread(threading.Thread, Object.Object):
    """class for a thread which listens for messages using a given 
    Messenger puts completed messages on a Queue.

    **INSTANCE ATTRIBUTES**

    [Messenger] *underlying* -- underlying messenger (usually
    [MessengerBasic]) used to receive and unpack them messages.

    Queue.Queue *completed_msgs* -- Queue on which to deposit the
    completed messages.

    SocketHasDataEvent *event* -- object used to notify the main thread
    that a socket has data

    CLASS ATTRIBUTES**
    
    *none* --

    .. [Messenger] file:///./messenger.Messenger.html
    .. [MessengerBasic] file:///./messenger.MessengerBasic.html"""
    def __init__(self, underlying, completed_msgs, event, **args_super):
        self.deep_construct(ListenAndQueueMsgsThread, 
                            {'underlying': underlying,
			     'completed_msgs': completed_msgs,
			     'event': event}, 
                            args_super, 
                            exclude_bases={'threading.Thread': 1})
        threading.Thread.__init__(self)

    def message_queue(self):
	"""returns a reference to the message queue in which the thread
	puts completed messages

	**INPUTS**

	*none*

	**OUTPUTS**

	*Queue.Queue* -- the message queue
	"""
	return self.completed_msgs

    def get_mess(self):
        """Gets a message from the external editor.
        
        **INPUTS**

	*none*
        
        **OUTPUTS**
        
        (STR, {STR: STR}) name_argvals_mess -- The message retrieved
         from external editor in *(mess_name, {arg:val})* format.
         from external editor in *(mess_name, {arg:val})* format, or
	 None if no message is available."""

	return self.get_mess()
        
    def notify_main(self):
	"""notify the main thread that there is a new message waiting in 
	the Queue, and return asynchronously.
	
	**INPUTS**

	**OUTPUTS**

	*none*
	"""
	self.event.notify()

    def run(self):
        """Start listening for data.
        
        **INPUTS**
        
        *none* -- 
        
        **OUTPUTS**
        
        *none* -- 
        """
        while 1:
	    data = self.get_mess()
	    self.completed_msgs.put(data)
	    self.notify_main()
            time.sleep(0.01)
#            time.sleep(1)


class ListenNewConnThread(threading.Thread, Object.Object):
    """Abstract base class which listens for new socket connections on 
    a port number and uses an InterThreadEvent object to
    notify the main thread about the new connection.

    Concrete subclasses will define log_conn method to add each new socket 
    to a data structure containing uninitialised connections.
    
    **INSTANCE ATTRIBUTES**
    
    INT *port* -- Port on which to listen for connections.
    
    InterThreadEvent *event* -- object use to send event to the main
    thread

    **CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, port, event, **args_super):
        self.deep_construct(ListenForNewConnThread, 
                            {'port': port, 
			     'event': event},
                            args_super, 
                            exclude_bases={'threading.Thread': 1})
        threading.Thread.__init__(self)        
        
    def notify_main(self):
	"""notify the main thread that there is a new connection waiting
	for a handshake, and return asynchronously.
	
	**INPUTS**

	**OUTPUTS**

	*none*
	"""
	self.event.notify()

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
            # Log it notify the main event loop that
            # it should shake hands with it
            #
            self.log_new_conn(client_socket)
	    self.notify_main()

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
	debug.virtual('ListenNewConnThread.log_new_conn')


class NewConnListThread(ListenNewConnThread):
    """Listens for new socket connections on a port number
    and use an InterThreadEvent object to
    notify the main thread about the new connection.

    Adds each new socket to a list of uninitialised connections.

    This version is used for new talker sockets, because they may not
    come in in the same order as the previously connected new listener
    sockets, so you have to look through the whole list anyway.
    
    **INSTANCE ATTRIBUTES**
    
    [socket] *new_socks* -- List on which to add any new connection.
    
    [lock] *new_socks_lock* -- Lock on the new connection list.

    **CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, port, new_socks, new_socks_lock, **args_super):
        self.deep_construct(ListenNewConnThread, 
                            {'new_socks': new_socks,
                             'new_socks_lock': new_socks_lock},
                            args_super)
        
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

class ListenNewEditorsThread(ListenNewConnThread):
    """Listens for new socket editor connections on a port number
    and use an InterThreadEvent object to notify the main thread about 
    the new connection.

    Adds each new socket to a Queue of uninitialised connections.

    This version is used for new listener sockets, which should be
    processed in the order they come in.
    
    **INSTANCE ATTRIBUTES**
    
    [Queue] *new_socks* -- Queue to which to add any new connection.

    **CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, new_socks, **args_super):
        self.deep_construct(ListenForNewEditorsThread, 
                            {'new_socks': new_socks},
                            args_super)

    def log_new_conn(self, client_socket):
        
        """Logs a newly received socket connection, so that main event
        loop can later shake hands with it.
        
        **INPUTS**
        
        *socket client_socket* -- Newly received socket connection
        
        **OUTPUTS**
        
        *none* -- 
        """
        
        self.new_socks.put(client_socket)
    
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
     
    Much of the above behaviour depends on a set of virtual 
    functions which will be implemented by a concrete subclass of
    ServerMainThread.  In particular, the mechanism by which 
    InterThreadEvent and SocketHasDataEvent events ensure that the main 
    mediator message loop calls the appropriate methods of ServerMainThread
    will vary from one concrete subclass to another.  A necessary
    consequence of this fact is that ServerMainThread relies on
    virtual functions to create the subsidiary threads.

    Even more drastically, in some cases ServerMainThread will contain the 
    main message loop of the mediator, while in others, the message loop
    which routes the events to the appropriate ServerMainThread methods
    will reside in the GUI console.

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
    
    **CLASS ATTRIBUTES**
    
    *none* -- 

    ..[AppStateMessaging] file:///./AppStateMessaging.AppStateMessaging.html
    ..[ListenForNewListenersThread] file:///./tcp_server.ListenForNewListenersThread.html
    ..[ListenForNewTalkersThread] file:///./tcp_server.ListenForNewTalkersThread.html
    """
    
    def __init__(self, new_listen_socks, **args_super):
        self.deep_construct(ServerSingleThread, 
                            {'pending_listen_socks': [],
                             'new_talk_socks': [],
                             'new_socks_lock': threading.Lock(),
			     'new_listen_socks': new_listen_socks,
			     'data_threads': {},
			     'new_listener_server': None,
			     'new_talker_server': None,
                             'active_meds': []
                             }, 
                            args_super)


    def new_data_thread(self, id, listen_sock):
        """creates a new ListenAndQueueMsgsThread to monitor the
	listen_sock
        
        **INPUTS**

        STR *id* -- The unique ID of the listen socket
        
        socket *listen_sock* -- The listen socket
        
        **OUTPUTS**
        
        [ListenAndQueueMsgsThread] -- the new threading.Thread object

        ..[ListenAndQueueMsgsThread] 
	file:///./tcp_server.ListenAndQueueMsgsThread.html"""        
	debug.virtual('ServerMainThread.new_data_thread')

    def _new_instance(self, id, instance):
        """add a new AppStateMessaging.  Called internally by
	package_sock_pair
        
        **INPUTS**
        
        STR *id* -- The unique ID of the listen socket

	AppStateMessaging *instance*  -- the new instance

        **OUTPUTS**
        
        *none*
	"""
	debug.virtual('ServerMainThread._new_instance')
        
    def known_instance(self, id):
	"""returns a reference to the AppStateMessaging instance 
	associated with  the given ID
        **INPUTS**
        
        STR *id* -- The unique ID of the listen socket

        **OUTPUTS**

	*AppStateMessaging* -- the corresponding instance
        
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
        
        *none* -- 

        ..[AppStateMessaging] file:///./messaging.AppStateMessaging.html"""        
        
	data_thread = self.new_data_thread(id, listen_sock)
	data_threads[id] = data_thread
	messages = data_thread.message_queue()

        talk_msgr = messenger_factory(talk_sock)        
        listen_msgr = messaging.MixedMessenger(talk_msgr, messages)
        an_app_state = app_state_factory(app_name, id, listen_msgr, talk_msgr)

	data_thread.setDaemon(1)
	data_thread.start()

        #
        # Give external editor a chance to configure the AppStateMessaging
        #
        an_app_state.config_from_external()

	self.new_instance(id, an_app_state)

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
        a_messenger = messenger_factory(most_rec_sock)
               
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
# pending_talk_socks, and it runs in the main thread just like we do,
# but just in case.
        self.new_socks_lock.acquire()

	self.pending_socks_lock.append((most_rec_sock, most_rec_data))

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
            a_msgr = messenger_factory(talk_sock)
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
                self.package_sock_pair(id, app_name, window, listen_sock, talk_sock)
                        
        self.new_socks_lock.release()        


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
        

##############################################################################
# start test standalone server
##############################################################################
def run_server(test_suite=None):
    """Start a single thread, single process server.
    """

    a_server = ServerSingleThread()
    a_server.test_suite = test_suite
        
    a_server.run()
    


def help():
    print """
Usage: python tcp_server.py -ht

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
    """

if __name__ == '__main__':


    opts, args = util.gopt(['h', None, 't=', None])

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
    run_server(test_suite=opts['t'])

    sr_interface.disconnect()
