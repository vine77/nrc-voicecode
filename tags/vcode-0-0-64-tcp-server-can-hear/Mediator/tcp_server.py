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

import natlink, os, re, socket, SocketServer, sys, time, whrandom
import select, string, threading, time

import AppStateMessaging, mediator, messaging, Object, RecogStartMgr, SourceBuffMessaging, sb_services, sim_commands, sr_interface


#
# Port numbers for the communication link
#
VC_LISTEN_PORT = 45770
VC_TALK_PORT = 45771


class SB_MessExtEdSim(SourceBuffMessaging.SourceBuffMessaging):
    """Communicates with an external [EdSim] through a messaging link.

    This subclass of [SourceBuff] is designed to interact with an [EdSim]
    instance running in a different process.

    It is used mostly for debugging and regression testing purposes.
    
    **INSTANCE ATTRIBUTES**

    [SB_ServiceIndent] *indent_srv* -- Code indentation service used to
    provide indentation at the server level.

    CLASS ATTRIBUTES**
    
    *none* -- 

    ..[SB_ServiceIndent] file:///./SB_ServiceIndent.SB_ServiceIndent.html
    ..[SourceBuff] file:///./SourceBuff.SourceBuff.html
    ..[EdSim] file:///./EdSim.EdSim.html"""
    
    def __init__(self, **args_super):
        print '-- SB_MessExtEdSim.__init__: called, args_super=%s' % repr(args_super)
        self.deep_construct(SB_MessExtEdSim, 
                            {'indent_srv': sb_services.SB_ServiceIndent(buff=self, indent_level=3, indent_to_curr_level = 1)}, 
                            args_super, 
                            {})

    def insert_indent(self, code_bef, code_after, range = None):
        print '-- SB_MessExtEdSim.insert_indent: called'
        self.indent_srv.insert_indent(code_bef, code_after, range)        


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
        return SB_MessExtEdSim(app=self, fname=fname)
        


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
        window = 0
        
        
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


def start_server_multithread():

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
    
    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, port, new_socks, new_socks_lock, **args_super):
        self.deep_construct(ListenForConnThread, 
                            {'port': port, 
                             'new_socks': new_socks,
                             'new_socks_lock': new_socks_lock}, 
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
#        print '-- ListenForConnThread.run: self=%s, binding to port %s' % (self, self.port)
        server_socket.bind((socket.gethostname(), self.port))
        server_socket.listen(5)

        while 1:
#            print '-- ListenForConnThread.run: self=%s, accepting a client socket' % self
            (client_socket, address) = server_socket.accept()
#            print '-- ListenForConnThread.run: self=%s, client socket accepted' % self
#            print '-- ListenForConnThread.run: self=%s,  port=%s' % (self, self.port)
#            print '-- ListenForConnThread.run: self=%s, client_socket=%s' % (self, client_socket)
            self.handshake(client_socket)
            time.sleep(1)


    def handshake(self, sock):
        
        """Does a preliminary handshake on the socket, and adds it to
        the list of uninitialised connections.

        Further handshaking may be done later by an [AppState] instance.
        
        **INPUTS**
        
        socket *sock* -- The socket on which to handshake.
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        debug.virtual('ListenForConnThread.handshake')

        
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

    def handshake(self, sock):
        """Does a handshake on the listen socket.
        
        **INPUTS**
        
        socket *sock* -- The listen socket on which to handshake.
        

        **OUTPUTS**
        
        *none* -- 
        """

#        print '-- ListenForNewListenersThread.handshake: self=%s, started, sock=%s' % (self, sock)


        a_messenger = messenger_factory(sock)
       
        #
        # Ideally, this would be invoked right away here, but can't do it
        # outside of main thread. Need to wait a bit longer to process it
        # in main thread. This may cause some timing problems aluded to below.
        #
        #
        # Find the window handle for the external editor. Assume it's the
        # active window.
        #
        # This may not work if there are some timing issues. If this turns out
        # to be a problem, may have to ask the user to point VoiceCode to the
        # editor's window, then click OK in some dialog box.
        #
 #       window = natlink.getCurrentModule()[2]
 

#        print '-- ListenForNewListenersThread.handshake: self=%s, getting app_name' % self
        
        #
        # Get the external application name
        #
        mess = a_messenger.get_mess(expect=['app_name'])
        app_name = mess[1]['value']
        
#        print '-- ListenForNewListenersThread.handshake: self=%s, sending ID' % self
        
        #
        # Assign a random ID to the external editor, and send it on the socket
        # connection.
        #
        id = '%s_%s' % (app_name, repr(whrandom.random()))
        a_messenger = messenger_factory(sock)        
        a_messenger.send_mess('your_id_is', {'value': id})
        a_messenger.get_mess(expect=['ok'])


#        print '-- ListenForNewListenersThread.handshake: self=%s, storing new sock' % self
        
        #
        # Store the new socket in the connection list.
        # Make sure you lock it first.
        #
        self.new_socks_lock.acquire()
        self.new_socks[sock] = [id, app_name]
        self.new_socks_lock.release()

#        print '-- ListenForNewListenersThread.handshake: self=%s, done' % self
        

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

    def handshake(self, sock):
        """Does a handshake on the talk socket.
        
        **INPUTS**
        
        socket *sock* -- The talk socket on which to handshake.
        

        **OUTPUTS**
        
        *none* -- 
        """

#        print '-- ListenForNewTalkersThread.handshake: self=%s, started' % self


#        print '-- ListenForNewTalkersThread.handshake: self=%s, getting ID' % self
        
        #
        # Read the ID previously assigned by VoiceCode to the external editor.
        #
        a_msgr = messenger_factory(sock)        
        mess = a_msgr.get_mess(expect=['my_id_is'])
        id = mess[1]['value']
        a_msgr.send_mess('ok')


#        print '-- ListenForNewTalkersThread.handshake: self=%s, acquiring lock' % self
        
        #
        # Store the new socket in the connection list.
        # Make sure you lock it first.
        #
        self.new_socks_lock.acquire()
        self.new_socks[id] = sock
        self.new_socks_lock.release()        

#        print '-- ListenForNewTalkersThread.handshake: self=%s, done'% self

class ServerSingleThread(Object.Object):
    """Implements a TCP/IP based VoiceCode server.

    This version is singlethread, i.e. all sockets are started in the
    main thread. The server then polls the various sockets using
    *select*, and then listens to whatever socket happens to be
    sending data.

    This version is less elegant than the multithreaded version, but
    it doesn't cause problems with natlink (it seems natlink functions
    are not meant to be invoked outside of the main thread).
    
    
    **INSTANCE ATTRIBUTES**
    
    {socket: (STR, STR, STR)} *new_listen_socks={}* -- Key is a new socket on
    the VC_LISTEN port, that has yet to be initialised and associated
    with an [AppStateMessaging]. Value is 3ple specifying:

    - the unique identifier assigned by VoiceCode to the external
      editor that requested that connection.
    - the name of the editor
    - the window handle the editor is running in

    {STR: socket} *new_talk_socks={}* -- VALUE (not key as in
    *new_listen_socks*) is a new socket on the VC_TALK port, that has yet
    to be initialised and associated with an [AppStateMessaging]. KEY (not
    value as in *new_listen_socks*) is the unique identifier assigned by
    VoiceCode to the external editor that requested that connection.
    
    {socket: STR} *active_listen_socks={}* -- Key is a VC_LISTEN
    sockets that HAS been initialised and associated with an
    [AppStateMessaging]. Value is the [AppStateMessaging] instance
    that's connected to the socket.

    *threading.lock new_socks_lock* -- Lock used to make sure that the
     mainthread doesn't access the dicts *new_listen_socks*
     and *new_talk_socks* at the same time as the threads that listen
     for new socket connections.

    CLASS ATTRIBUTES**
    
    *none* -- 

    ..[AppStateMessaging] file:///./AppStateMessaging.AppStateMessaging.html"""
    
    def __init__(self, **args_super):
        self.deep_construct(ServerSingleThread, 
                            {'new_listen_socks': {},
                             'new_talk_socks': {},
                             'new_socks_lock': threading.Lock(),
                             'active_listen_socks': {}}, 
                            args_super, 
                            {threading.Thread: 1})


    def package_sock_pair(self, id, app_name, listen_sock, talk_sock):
        """Packages a listen and talk socket into an AppStateMessaging instance
        
        **INPUTS**
        
        STR *id* -- The unique identifier assigned by VoiceCode to
        that socket pair.
        
        socket *listen_sock* -- The listen socket
        
        socket *talk_sock* -- The talk socket
        

        **OUTPUTS**
        
        *none* -- 
        """

        print '-- ServerSingleThread.package_sock_pair: called'
        
        
        listen_msgr = messenger_factory(listen_sock)
        talk_msgr = messenger_factory(talk_sock)        
        an_app_state = app_state_factory(app_name, id, listen_msgr, talk_msgr)
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
        mediator.init_simulator_regression(disable_dlg_select_symbol_matches=1)
#        mediator.init_simulator(disable_dlg_select_symbol_matches=1, window=window)
        mediator.the_mediator.interp.on_app = an_app_state
        sim_commands.the_mediator = mediator.the_mediator        
        # define some useful local variables
        home = os.environ['VCODE_HOME']
        sim_commands.command_space['home'] = home
        sim_commands.command_space['testdata'] = \
                  os.path.join(home, 'Data', 'TestData')        
        
        return an_app_state
    

    def start(self):
        """Start the server
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        #
        # This server listens for new socket connections on VC_LISTEN port.
        # New connections are stored in a dictionary, so that the main thread
        # can later on initialise them.
        #
        new_listener_server = \
           ListenForNewListenersThread(new_socks=self.new_listen_socks,
                                   new_socks_lock=self.new_socks_lock)
        new_listener_server.start()

        #
        # This server listens for new socket connections on VC_TALK port.
        # New connections are stored in a dictionary, so that the main thread
        # can later on initialise them.        
        #
        new_talker_server = \
           ListenForNewTalkersThread(new_socks=self.new_talk_socks,
                                   new_socks_lock=self.new_socks_lock)
        new_talker_server.start()
        
        #
        # Process connections created by the above 2 threads.
        #
        
        #beg
        ii = 0
        #end
        
        while 1:

            #beg
            print '-- -- ServerSingleThread.start: while, ii=%s' % ii
            ii = ii + 1
            #end


            time.sleep(5)
            
            #
            # Look to see if there are some new connections that need to be
            # initialised
            #

            # First make sure we lock the dicts of new connections
            self.new_socks_lock.acquire()

            new_listen_socks_list = self.new_listen_socks.keys()
            
            for a_listen_sock in new_listen_socks_list:

                print '-- ServerSingleThread.start: spotted new connection'
                
                #
                # Find the window handle for the external editor. Assume it's
                # the active window.
                #
                # Ideally, this would be done right away when the socket is
                # opened. But can't do that because socket is opened in
                # a secondary thread and it seems you can
                # only call getCurrentModule in main thread.
                #
                # This may cause some timing problems where the user (or
                # some process) changes the active window before VoiceCode
                # gets a chance to invoke getCurrentModule.
                #
                # If this turns out to be a problem, may have to ask the user
                # to point VoiceCode to the editor's window, then click OK in
                # some dialog box.
                #
                window = natlink.getCurrentModule()[2]

                #
                # Find the id and application name for that LISTEN socket
                #
                (id, app_name) = self.new_listen_socks[a_listen_sock]
                
                #
                # Check to see if we have a VC_TALK socket that
                # corresponds to that VC_LISTEN socket.
                #
                # If so, package the two sockets in a single AppStateMessaging
                #
                id = self.new_listen_socks[a_listen_sock][0]
                if self.new_talk_socks.has_key(id):

                    a_talk_sock = self.new_talk_socks[id]
                    
                    #
                    # We do have new talker socket for that
                    # connection. Package the two sockets.
                    #
                    
                    an_app_state = self.package_sock_pair(app_name, id, a_listen_sock, a_talk_sock)
                    self.active_listen_socks[a_listen_sock] = an_app_state

                    #
                    # Delete the two sockets from the list of unitialised
                    # socket connections
                    #
                    del self.new_listen_socks[a_listen_sock]
                    del self.new_talk_socks[id]

            #
            # Now unlock the dicts of new connections
            #
            self.new_socks_lock.release()
#            print '-- ServerSingleThread.start: finished with new connections'

            #
            # Now check to see if one of the initialised listener sockets has
            # received data
            #
            listening_sockets = self.active_listen_socks.keys()

#            print '-- ServerSingleThread.start: listen_sockets=%s' % listening_sockets
            
            if len(listening_sockets) > 0:
#                print '-- ServerSingleThread.start: selecting socket'
                (ready_sockets, dum1,dum2) = select.select(listening_sockets, [], [], 0)
#                print '-- ServerSingleThread.start: ready_sockets=%s, dum1=%s' % (repr(ready_sockets), dum1)

#                print '-- ServerSingleThread.start: finished selecting socket'

                
                #
                # Complete a single transaction for each socket that has
                # received some data
                #
                for a_socket in ready_sockets:
#                    print '-- ServerSingleThread.start: ready socket %s' % a_socket
                    an_app = self.active_listen_socks[a_socket]
#                    print '-- ServerSingleThread.start: ready an_app.listen_msgr.transporter.sock=%s' % an_app.listen_msgr.transporter.sock
#                    print '-- ServerSingleThread.start: an_app.%s' % an_app                    
#                    an_app.listen_one_transaction()

                

def start_server_singlethread():
    """Start a single thread, single process server.
    """

#    print '-- start_server_singlethread: called'

    a_server = ServerSingleThread()
        
    a_server.start()
    print '-- start_server_multiprocesses: done'


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
        
        print '-- ServerMultiProcesses.vc_listener_handshake: called'
        
        a_messenger = messenger_factory(sock)
       

        print '-- ServerMultiProcesses.vc_listener_handshake: self=%s, getting app_name' % self
        
        #
        # Get the external application name
        #
        mess = a_messenger.get_mess(expect=['app_name'])
        app_name = mess[1]['value']
        
        print '-- ServerMultiProcesses.vc_listener_handshake: self=%s, sending ID' % self
        
        #
        # Assign a random ID to the external editor, and send it on the socket
        # connection.
        #
        id = '%s_%s' % (app_name, repr(whrandom.random()))
        a_messenger = messenger_factory(sock)        
        a_messenger.send_mess('your_id_is', {'value': id})
        a_messenger.get_mess(expect=['ok'])



        print '-- ServerMultiProcesses.vc_listener_handshake: self=%s, done' % self
        
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

        print '-- ServerMultiProcesses.vc_talker_handshake: self=%s, started' % self
        success = 0


        print '-- ServerMultiProcesses.vc_talker_handshake: self=%s, getting ID' % self
        
        #
        # Read the ID previously assigned by VoiceCode to the external editor.
        #
        a_msgr = messenger_factory(sock)        
        mess = a_msgr.get_mess(expect=['my_id_is'])
        this_id = mess[1]['value']
        a_msgr.send_mess('ok')

        if this_id == id:
            success = 1

        print '-- ServerMultiProcesses.vc_talker_handshake: returning success=%s' % success
        
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

        print '-- ServerMultiProcesses.package_sock_pair: called'


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
        mediator.init_simulator_regression(disable_dlg_select_symbol_matches=1)
#        mediator.init_simulator(disable_dlg_select_symbol_matches=1, window=window)
        mediator.the_mediator.interp.on_app = an_app_state
        sim_commands.the_mediator = mediator.the_mediator        
        # define some useful local variables
        home = os.environ['VCODE_HOME']
        sim_commands.command_space['home'] = home
        sim_commands.command_space['testdata'] = \
                  os.path.join(home, 'Data', 'TestData')

        
        

    def start(self):
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

        print '-- ServerMultiProcesses.start: listening for new VC_LISTEN connection'
        (vc_listener_socket, address) = server_socket.accept()
        print '-- ServerMultiProcesses.start: received new VC_LISTEN connection'        

        #
        # Get the window handle of active application.
        # Assume that this is the application which requested the connection.
        #
        window = natlink.getCurrentModule()[2]

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
        # win32api.WinExec('python %VCODE_HOME%\\Mediator\\tcp_server.py')



def start_server_multiprocesses():
    """Start a single-thread, multi-processes server.
    """

#    print '-- start_server_absolutely_singlethread: called'

    a_server = ServerMultiProcesses()
        
    a_server.start()
#    print '-- start_server_multiprocesses: done'


if __name__ == '__main__':

    sr_interface.connect()
    sr_interface.set_mic('on')

    #
    # Create a global grammar manager
    #
#    the_recog_start_mgr = RecogStartMgr.RecogStartMgr()

    #
    # Start servers on the VC_LISTEN and VC_TALK ports
    #
#    start_server_singlethread()
    start_server_multiprocesses()

    #
    # Uncomment this when debugging the server
    #
    sim_commands.sleep_before_recognitionMimic = 5
    sim_commands.help()
    while (not sim_commands.quit_flag):
      cmd = raw_input('Command> ')
      mediator.execute_command(cmd)                


    sr_interface.disconnect()
