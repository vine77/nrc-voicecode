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

We have two versions of the server.

The multi-threaded version is the most elegant implementation, but is causing
problems with NatLink. It seems NatLink functions like natconnect cannot be
called outside of the main thread.

The single-threaded version is a bit of a hack, but it is able to call all
NatLink functions from the main thread (except for callback functions like
gotResults, which don't seem to cause problems outside of the main thread).

???????????????????????????????????????????????????????????????????????????????
Actually, it could be that gotResults ends up invoking functions
like getWordInfo, which may not be thread safe.

In that case, the only solution left is for server to do EVERYTHING in
main thread as follows:

1. when hears a new connection, use the SERVER_sockets to get the two
   CLIENT_sockets on the two ports.

2. Then unbind the SERVER_sockets from the ports, and start a new
   tcp_server.py script which will start listening on those ports.

3. then use the CLIENT_sockets in the main thread to do the usual
   VoiceCode stuff.


This approach has many disadvantages

a) slow because need to start a new instance of python every time

b) more memory intensive (one copy of python interpreter per external editor)

c) may drop some connection requests if sent while the new server
script is starting.

d) problems with SymDict persistence.


Point d)is the biggest problem. Basically, all mediator instances will have
a different copy of SymDict. When they exit and write it to file, they will
therefore overwrite changes that may have been done by other instances.

A solution to d) is for VoiceCode interpret_NL_cmd to:

ii) compare the date of the symdict_pkl.dat file against the date of
its internal version at the beginning of an utterance. If not the
same, reloads it from disk.

iii) at the end of the utterance, it writes it to disk.

This will be very slow if symdict gets large.
???????????????????????????????????????????????????????????????????????????????
"""

import natlink, os, posixpath, pythoncom, re, select, socket
import SocketServer, string, sys, threading, time, whrandom, win32event

import AppStateMessaging, auto_test, mediator, messaging, Object
import RecogStartMgr, SourceBuffMessaging, sb_services
import sim_commands, sr_interface, util


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

    CLASS ATTRIBUTES**
    
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

    def refresh_if_necessary(self):
	self.app.talk_msgr.send_mess('refresh_if_necessary')
        self.app.talk_msgr.get_mess(expect=['refresh_if_necessary_resp'])
        self.print_buff()
        
    def line_num_of(self, position = None):
	return self.lines_srv.line_num_of(position)

    def number_lines(self, astring, startnum=1):
        return self.lines_srv.number_lines(astring, startnum)

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

    CLASS ATTRIBUTES**
    
    *none* -- 

    ..[AppState] file:///./AppState.AppState.html
    ..[EdSim] file:///./EdSim.EdSim.html"""
    
    def __init__(self, **args_super):
        self.deep_construct(AS_MessExtEdSim, 
                            {}, 
                            args_super, 
                            {})

    def new_compatible_sb(self, fname):
#        print '-- AS_MessExtEdSim.new_compatible_sb: fname=%s' % fname
        buff = SB_MessExtEdSim(app=self, fname=fname)
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
    encoder = messaging.MessEncoder_LenPrefArgs()
    a_messenger = messaging.Messenger(packager=packager, transporter=transporter, encoder=encoder)        
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
    else:
        print "WARNING: Unknown editor '%s'" % app_name
        print "Connection refused"
    app.app_name = app_name
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


class VCListenerHandler(SocketServer.BaseRequestHandler):
    def handle(self):

        global the_recog_start_mgr

        print '... Listener connection %s: Starting handler' % self.request.__dict__ 
        f = self.request.makefile()

        self.recog_mgr = the_recog_start_mgr
        
        #
        # Create a messenger
        #
        self.messenger = messenger_factory(self.request)

        #
        # Do the handshake
        #
        self.handshake()
        


    def handshake(self):
        """Does the handshake for a new VC listener connection.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
      
        #
        # Find the window handle for the external editor. Assume it's the
        # active window.
        #
        # This may not work if there are some timing issues. If this turns out
        # to be a problem, may have to ask the user to point VoiceCode to the
        # editor's window, then click OK in some dialog box.
        #
        # ???PROBLEM???
        # -------------
        # getCurrentModule doesn't work unless it's called in the main
        # thread. Maybe we don't need the server to run in a separate thread
        # (i.e. maybe just the Listener and Talker need to run in separate
        # threads, but the server that listens for new connections doesn't
        # have to. On the other hand, probably need to because there are 2
        # servers that need to listen at the same time.
        #
        # Another possible fix is to have the main thread call getCurrentModule
        # at regular interval (say every 10th of a second) and store the value
        # in a global variable that could be accessed by the Listener thread.
        # This could cause timing problems, but if the look is fast enough
        # it shouldn't be a problem.
        #

        natlink.natConnect(1)
        window = natlink.getCurrentModule()[2]
#        window = 0
        
        
        #
        # Authenticate the user
        #
        vc_authentification(self.messenger)
        
        #
        # Get the name of the editor
        #
        mess = self.messenger.get_mess(expect=['app_name'])
        app_name = mess[1]['value']
        self.messenger.send_mess('ok')
                
        #
        # Send random key to the external editor. 
        #
        ran_key = repr(whrandom.random())
        self.messenger.send_mess('your_id_is', {'id': ran_key})

        #
        # Create an AppState fit for that editor
        #
        app = app_state_factory(app_name, id=ran_key, listen_msgr = self.messenger, talk_msgr=None)
        
        
        #
        # Let the external editor configure the AppState if it wants to
        #
        app.config_from_external()    

        
        # Should eventually do some kind of error checking on answer
        reply = self.messenger.get_mess(expect=['ok'])

        ###################################################################
        #
        # When the RecogStartMgr is functional, the code below will be used.
        #
        ###################################################################
        #
        # Tell the recognition start manager about this new editor instance
        #
        # self.recog_mgr.new_instance(app.app_name, app, window)

        ###################################################################
        #
        # But for now, we create a MediatorObject instance as per the old
        # architecture of the system.
        #
        ###################################################################
        mediator.init_simulator_regression(disable_dlg_select_symbol_matches=1)
        mediator.the_mediator.interp.on_app = app
        
        #
        # Start listening for commands from editor.
        #
#        app.listen()
        


class VCTalkerHandler(SocketServer.BaseRequestHandler):
    def handle(self):

        global the_recog_start_mgr
        
        print '... Talker connection %s: Starting handler' % self.request.__dict__         
        f = self.request.makefile()
        self.recog_start_mgr = the_recog_start_mgr

        #
        # Create a messenger
        #
        self.messenger = messenger_factory(self.request)

        #
        # Do the handshake
        #
        self.handshake()



    def handshake(self):
        """Does the handshake for a new VC Talker connection.
        
        **INPUTS**
        
        *none*
        
        **OUTPUTS**
        
        *none* --
        """
        
        #
        # Authenticate the user
        #
        vc_authentification(self.messenger)
        
        
        #
        # Get the ID of the external application
        # Eventually, should do some kind of error checking on the received
        # message
        #
        mess = self.messenger.get_mess(expect=['your_id_is'])
        id = mess[1]['id']
        self.messenger.send_mess('ok')
        
        #
        # Find the AppState with that ID, and bind its talker to the
        # messenger
        #
        for an_app in self.recog_mgr.app_instances():
            if an_app.id == id:
                app.talk_msgr = self.messenger
                break

        
class ConnectionServer(threading.Thread):
   
   def __init__(self, port, handler_class):
       self.server = SocketServer.ThreadingTCPServer(("", port), handler_class)
       threading.Thread.__init__(self)
       
   def run(self):
       self.server.serve_forever()


def run_server_multithread():

    """Start 2 servers listening for new connections from external editors

    One server listens for VC listener connections (i.e. connections
    that will be used by VC to listen for commands from the editor)

    The other server listens for VC talker connections
    (i.e. connections that will be used by VC to send commands to the
    editor).

    This version is multithreaded, i.e. each socket is started in its
    own separate thread. Each thread can then listen indpendantly in
    their own thread.

    This version is more elegant than the multithreaded version, but
    it seems to cause problems with natlink (it seems natlink
    functions are not meant to be invoked outside of the main thread).

    **INPUTS**

    *none*
    
    **OUTPUTS**
        
    *none* -- 
    """
    
    vc_listen_server = ConnectionServer(port=VC_LISTEN_PORT, handler_class=VCListenerHandler)
    vc_listen_server.start()
    
    vc_talk_server = ConnectionServer(port=VC_TALK_PORT, handler_class=VCTalkerHandler)
    vc_talk_server.start()
    


##############################################################################
# Classes for single-threaded version of the server
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
    
    CLASS ATTRIBUTES**
    
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

#            print '-- ListenForConnThread.run: got new connection on port=%s' % self.port
            
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
    
    CLASS ATTRIBUTES**
    
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
    
    CLASS ATTRIBUTES**
    
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
    
    CLASS ATTRIBUTES**
    
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
                (self.ready_socks, dum1,dum2) = select.select(to_check, [], [], 0)
                self.ready_socks_lock.release()
                if len(self.ready_socks) > 0:
#                    print '-- CheckReadySocksThread.run: some sockets are ready'
                    win32event.SetEvent(self.raise_event)

            # When debuggin, increase sleep time if you want to see things
            # happen in slow motion
            time.sleep(0.01)
            time.sleep(3)


class ServerSingleThread(Object.Object):
    """Implements a TCP/IP based VoiceCode server.

    ??? Update this documentation when the server is finalised ???
    
    This version is singlethread, i.e. all sockets are started in the
    main thread. The server then polls the various sockets using
    *select*, and then listens to whatever socket happens to be
    sending data.

    This version is less elegant than the multithreaded version, but
    it doesn't cause problems with natlink.getCurrentModule (it seems
    natlink functions are not meant to be invoked outside of the main
    thread). That's because natlink.getCurrentModule is invoked in the
    main thread.

    ???? PROBLEM ????

    On the other hand, it doesn't seem to hear me when I talk. This is
    because it seems you need to start an event loop (e.g. by calling
    natlink.waitForSpeech()) IN THE MAIN THREAD in order to hear
    speech events.

    This is a problem because I need at least two threads, and both of
    them need to be the main thread.

    One thread waits for socket connections from external
    editors. Whenver it gets a new request for a connection, this
    thread needs to generate VoiceCode grammars, and tie them to the
    external editor's window. This means that the thread must be able
    to invoke natlink.getCurrentModule() (to know the window of the
    editor), which means it has to be the main thread (because of
    natlink.getCurrentModule() problem).

    In the other thread, I need to start an event loop (either by invoking
    waitForSpeech() or by starting some other GUI window), so that I can
    intercept speech events. This means that this thread must also be the
    main thread (because of event loop problem).

    But obviously those threads can't both be the main thread!!!!
    
    
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

    CLASS ATTRIBUTES**
    
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

#        print '-- ServerSingleThread.package_sock_pair: called'
        
        
        listen_msgr = messenger_factory(listen_sock)
        talk_msgr = messenger_factory(talk_sock)        
        an_app_state = app_state_factory(app_name, id, listen_msgr, talk_msgr)

        #
        # Give external editor a chance to configure the AppStateMessaging
        #
        an_app_state.config_from_external()

        ###################################################################
        #
        # When the RecogStartMgr is functional, the code below will be used.
        #
        ###################################################################
        #
        # Tell the recognition start manager about this new editor instance
        #
        # window = self.new_listen_socks[listen_sock][1]
        # self.recog_mgr.new_instance(an_app_state.app_name, an_app_state, window)


        ###################################################################
        #
        # But for now, we create a MediatorObject instance as per the old
        # architecture of the system.
        #
        ###################################################################

        #
        # ??????????????????????????????????????????????????????????
        # May need to use init_simulator_regression() instead
        # if self.test_suite != None. Otherwise, external editor will
        # have to keep the focus throughout the regression test
        #
        # Actually not, because regression test will invoke
        # init_simulator_regression() which will reinitialise that
        # mediator object with proper settings.
        #
        # ??????????????????????????????????????????????????????????        
        #

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
#            print '-- ServerSingleThread.package_sock_pair: running regression test suite %s' % self.test_suite
            args = [self.test_suite]
            auto_test.run(args)
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
       
#        print '-- ServerSingleThread.handshake_listen_socks: self=%s, getting app_name' % self
        
        #
        # Get the external application name
        #
        mess = a_messenger.get_mess(expect=['app_name'])
        app_name = mess[1]['value']
        
#        print '-- ServerSingleThread.handshake_listen_socks: self=%s, sending ID' % self
        
        #
        # Assign a random ID to the external editor, and send it on the socket
        # connection.
        #
        id = '%s_%s' % (app_name, repr(whrandom.random()))
        a_messenger.send_mess('your_id_is', {'value': id})
        a_messenger.get_mess(expect=['ok'])


#        print '-- ServerSingleThread.handshake_listen_socks: self=%s, storing new sock' % self
        
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

#        print '-- SeverSingleThread.handshake_talk_conn: self=%s, started' % self

#        print '-- SeverSingleThread.handshake_talk_conn: self=%s, getting ID' % self

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
            mess = a_msgr.get_mess(expect=['my_id_is'])
            id = mess[1]['value']
            a_msgr.send_mess('ok')

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
                
            if found != None:
                self.package_sock_pair(id, app_name, window, listen_sock, talk_sock)
                
#        print '-- SeverSingleThread.handshake_talk_conn: self=%s, acquiring lock' % self
        
        self.new_socks_lock.release()        

#        print '-- SeverSingleThread.handshake_talk_conn: self=%s, done'% self



    def process_ready_socks(self):
        """Processes socket connections that have received new data.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

#        print '-- ServerSingleThread.process_ready_socks: self.ready_socks=%s' % repr(self.ready_socks)

        self.ready_socks_lock.acquire()

        for a_sock in self.ready_socks:
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
#                print '-- ServerSingleThread.run: got evt_new_listen_conn'
                self.handshake_listen_socks()

            elif rc == win32event.WAIT_OBJECT_0+1:
                #
                # A new VC_TALK connection was opened
                #
#                print '-- ServerSingleThread.run: got evt_new_talk_conn'
                self.handshake_talk_socks()

                
            elif rc == win32event.WAIT_OBJECT_0+2:
                #
                # Some of the active VC_LISTEN sockets have received data
                #
#                print '-- ServerSingleThread.run: got evt_sockets_ready'
                self.process_ready_socks()

            elif rc == win32event.WAIT_OBJECT_0+3:
                #
                # Server is shutting down. Exit the event loop.
                #
#                print '-- ServerSingleThread.run: got evt_quit'
                break
                
            elif rc == win32event.WAIT_OBJECT_0+4:
                # A windows message is waiting - take care of it.
                # (Don't ask me why a WAIT_OBJECT_MSG isn't defined < WAIT_OBJECT_0)
                # Note: this must be done for COM and other windowsy
                #   things to work.
#                print '-- ServerSingleThread.run: forwarding unknown message'
                if pythoncom.PumpWaitingMessages():
                    break # wm_quit
                
            elif rc == win32event.WAIT_TIMEOUT:
                # Our timeout has elapsed.
                # Do some work here (e.g, poll something can you can't thread)
                #   or just feel good to be alive.
                # Good place to call watchdog(). (Editor's note: See my "thread lifetime" recepie.)
                pass
#                print '-- ServerSingleThread.run: nothing to do, counter=%s' % counter
            else:
                raise RuntimeError( "unexpected win32wait return value")

            counter = counter + 1


def run_server_singlethread(test_suite=None):
    """Start a single thread, single process server.
    """

#    print '-- start_server_singlethread: called'

    a_server = ServerSingleThread()
    a_server.test_suite = test_suite
        
    a_server.run()
    
#    print '-- start_server_multiprocesses: done'


##############################################################################
# Classes for single-threaded multi-processes version of the server
##############################################################################


class ServerMultiProcesses(Object.Object):
    """Multi processes version of the TCP server.

    This "server" listens for a single connection, then it starts servicing
    that connection only.

    This version could not possibly be used in production setting because
    it can only service one external editor.

    Even if we spawned a new server script, this wouldn't work because the
    recogStartMgr would not be able to communicate across different scripts.

    Maybe that doesn't matter. Each script would have its own
    recogStartMgr which would manage the grammars it knows about.

    But we still would have problems with persistence of SymDict. See
    details at beginning of this file.
    
    
    **INSTANCE ATTRIBUTES**
    
    *none*-- 

    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, **args_super):
        self.deep_construct(ServerMultiProcesses, 
                            {}, 
                            args_super, 
                            {})


    def vc_listener_handshake(self, sock):
        """Does the preliminary handshake for a new VC_LISTENER connection.
        
        **INPUTS**
        
        socket *sock* -- The socket on which to do the handshake.
        

        **OUTPUTS**
        
        INT *id* -- The unique identifier assigned by the server to
        that connection.        
        """
        
#        print '-- ServerMultiProcesses.vc_listener_handshake: called'
        
        a_messenger = messenger_factory(sock)
       

#        print '-- ServerMultiProcesses.vc_listener_handshake: self=%s, getting app_name' % self
        
        #
        # Get the external application name
        #
        mess = a_messenger.get_mess(expect=['app_name'])
        app_name = mess[1]['value']
        
#        print '-- ServerMultiProcesses.vc_listener_handshake: self=%s, sending ID' % self
        
        #
        # Assign a random ID to the external editor, and send it on the socket
        # connection.
        #
        id = '%s_%s' % (app_name, repr(whrandom.random()))
        a_messenger = messenger_factory(sock)        
        a_messenger.send_mess('your_id_is', {'value': id})
        a_messenger.get_mess(expect=['ok'])



#        print '-- ServerMultiProcesses.vc_listener_handshake: self=%s, done' % self
        
        return (app_name, id)



    def vc_talker_handshake(self, id, sock):
        """Does the preliminary handshake for a new VC_TALKER connection.
        
        **INPUTS**

        socket *sock* -- Socket on which to do the handshaking.
        
        STR *id* -- ID of the connection for which we want to do the
        handshake. If this VC_LISTENER connection does not have that
        ID, it will simply be rejected.
        

        **OUTPUTS**
        
        BOOL *success* -- Returns *true* if the VC_LISTENER connection
        had the right ID.
        
        """

#        print '-- ServerMultiProcesses.vc_talker_handshake: self=%s, started' % self
        success = 0


#        print '-- ServerMultiProcesses.vc_talker_handshake: self=%s, getting ID' % self
        
        #
        # Read the ID previously assigned by VoiceCode to the external editor.
        #
        a_msgr = messenger_factory(sock)        
        mess = a_msgr.get_mess(expect=['my_id_is'])
        this_id = mess[1]['value']
        a_msgr.send_mess('ok')

        if this_id == id:
            success = 1

#        print '-- ServerMultiProcesses.vc_talker_handshake: returning success=%s' % success
        
        return success




    def package_socks_pair(self, app_name, id, window, listen_sock, talk_sock):
        """Connects a pair of socket connections with a VoiceCode mediator.
        
        **INPUTS**
        
        STR *id* -- ID of that socket pair.
        
        STR *window* -- window handler of the external editor using
        that connection pair.
        
        socket *listen_sock* -- Socket connection used by
        external editor to send commands to VoiceCode.
        
        socket *talk_sock* -- Socket connection used by
        VoiceCode to send commands to external editor.
        
        **OUTPUTS**
        
        *none* -- 
        """

#        print '-- ServerMultiProcesses.package_sock_pair: called'


        #
        # Create an AppStateMessaging
        #
        listen_msgr = messenger_factory(listen_sock)
        talk_msgr = messenger_factory(talk_sock)        
        an_app_state = app_state_factory(app_name=app_name, id=id, listen_msgr=listen_msgr, talk_msgr=talk_msgr)

        #
        # Let the external editor configure that AppStateMessaging
        #
        an_app_state.config_from_external()

        ###################################################################
        #
        # When the RecogStartMgr is functional, the code below will be used.
        #
        ###################################################################
        #
        # Tell the recognition start manager about this new editor instance
        #
        # self.recog_mgr.new_instance(an_app_state.app_name, an_app_state, window)


        ###################################################################
        #
        # But for now, we create a MediatorObject instance as per the old
        # architecture of the system.
        #
        ###################################################################
#        mediator.init_simulator_regression(disable_dlg_select_symbol_matches=1)
        mediator.init_simulator(disable_dlg_select_symbol_matches=1, window=window)
        mediator.the_mediator.interp.on_app = an_app_state
        sim_commands.the_mediator = mediator.the_mediator        
        # define some useful local variables
        home = os.environ['VCODE_HOME']
        sim_commands.command_space['home'] = home
        sim_commands.command_space['testdata'] = \
                  os.path.join(home, 'Data', 'TestData')


        

    def spawn_new_server_process(self):
        """Spawns a new VoiceCode server in a new process.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

#        print '-- ServerSingleThread.spawn_new_server_process: starting new server'
        vc_home = os.environ['VCODE_HOME']
        win32api.WinExec('python %s\\Mediator\\tcp_server.py' % vc_home)
#        print '-- ServerSingleThread.spawn_new_server_process: DONE starting new server'        



    def run(self):
        """Start the server
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        #
        # Listen for connection on VC_LISTEN_PORT
        #
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((socket.gethostname(), VC_LISTEN_PORT))
        server_socket.listen(5)

#        print '-- ServerMultiProcesses.start: listening for new VC_LISTEN connection'
        (vc_listener_socket, address) = server_socket.accept()
        server_socket.close()
        
#        print '-- ServerMultiProcesses.start: received new VC_LISTEN connection'        

        #
        # Get the window handle of active application.
        # Assume that this is the application which requested the connection.
        #
#        window = natlink.getCurrentModule()[2]
        window = 0

        #
        # Do the handshake for that VC_LISTENER socket
        #
        (app_name, id) = self.vc_listener_handshake(vc_listener_socket)

        #
        # Listen for connection on VC_TALK_PORT until we get the right
        # connection.
        #
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((socket.gethostname(), VC_TALK_PORT))
        server_socket.listen(5)
        while 1:
            (vc_talker_socket, address) = server_socket.accept()

            #
            # Do the handshake for that 
            #
            success = self.vc_talker_handshake(id, vc_talker_socket)
            if success:
                break

        #
        # Package the sockets pair into an AppState
        #
        self.package_socks_pair(app_name, id, window, vc_listener_socket, vc_talker_socket)
        
        #
        # Start a brand new server process
        #
        self.spawn_new_server_process()

        #beg
        sys.exit()
        #end
        
        #
        # Start listening
        #
        sim_commands.listen()

        #
        # Uncomment this when debugging the server
        # Allows user to type commands 
        #
        sim_commands.help()
        while (not sim_commands.quit_flag):    
            prompt_for_cmd()        



def run_server_multiprocesses():
    """Start a single-thread, multi-processes server.
    """

#    print '-- start_server_absolutely_singlethread: called'

    a_server = ServerMultiProcesses()
        
    a_server.run()

    
#    print '-- start_server_multiprocesses: done'
    

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


#    print '-- tcp_server.__main__: started'
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
    run_server_singlethread(test_suite=opts['t'])
#    run_server_multiprocesses()


    sr_interface.disconnect()
