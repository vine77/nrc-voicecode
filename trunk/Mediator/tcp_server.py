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
# (C)2001, National Research Council of Canada
#
##############################################################################

Import SocketServer, whrandom, threading

import messaging


#???? Choose ports based on Mathieu and Daniel's names ??????????
#VC_LISTENER_PORT = 50007
#VC_TALKER_PORT = 50008

VC_LISTENER_PORT = 45770
VC_TALKER_PORT = 45771


def vc_authentification(messenger, recog_mgr):
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


def vc_listener_handshake(self, messenger, recog_mgr):
    """Does the handshake for a new VC listener connection.
        
    **INPUTS**
        
    [Messenger] *messenger* -- Messenger to be used for the connection.

    [RecogStrartMgr] *recog_mgr* -- Object responsible for
    dispatching recognition events to the various editors.
        

    **OUTPUTS**
        
    *none* -- 


    ..[Messenger] file:///./messaging.Messenger.html
    ..[RecogStartMgr] file:///./RecogStartMgr.RecogStartMgr.html"""
    
    
    #
    # Find the window handle for the external editor. Assume it's the
    # active window.
    #
    # This may not work if there are some timing issues. If this turns out
    # to be a problem, may have to ask the user to point VoiceCode to the
    # editor's window, then click OK in some dialog box.
    #
    window = natlink.getCurrentModule()[2]


    #
    # Authenticate the user
    #
    vc_authentification(messenger, recog_mgr)
    
    #
    # Create an AppStateMessaging bound to that messenger
    #
    app = AppStateMessaging.AppStateMessaging(listen_msgr = messenger)
    
    #
    # Send random key to the external editor. 
    #
    ran_key = repr(whrandom.random())
    app.id = ran_key
    messenger.send_mess('your_id_is', {'id': ran_key})
    
    # Should eventually do some kind of error checking on answer
    reply = messenger.get_mess(expect=['ok'])
    
    #
    # Tell the recognition start manager about this new editor instance
    #
    ???SomeRecogStartMgr???.new_instance(app.editor_name, app, window)
    
    #
    # Start listening for commands from editor.
    #
    app.listen()



def vc_talker_handshake(self, messenger, recog_mgr):
    """Does the handshake for a new VC listener connection.
    
    **INPUTS**
    
    [Messenger] *messenger* -- Messenger to be used for the connection.
    
    [RecogStrartMgr] *recog_mgr* -- Object responsible for
    dispatching recognition events to the various editors.
    
    **OUTPUTS**
    
    *none* -- 
    
    ..[Messenger] file:///./messaging.Messenger.html
    ..[RecogStartMgr] file:///./RecogStartMgr.RecogStartMgr.html"""

    #
    # Authenticate the user
    #
    vc_authentification(messenger, recog_mgr)

    
    #
    # Get the ID of the external application
    # Eventually, should do some kind of error checking on the received
    # message
    #
    mess = messenger.get_mess(expect=['your_id_is'])
    id = mess[1]['id']
    messenger.send_mess('ok')
    
    #
    # Find the AppState with that ID, and bind its talker to the
    # messenger
    #
    for an_app in recog_mgr.app_instances():
        if an_app.id == id:
            app.talk_msgr = messenger
            break
        

class VCConnectionHandler(SocketServer.BaseRequestHandler):
    
    """Creates a new VoiceCode connection (listener or talker) tied to
    a new external editor.
    
    **INSTANCE ATTRIBUTES**
    
    [Messenger] *messenger* -- Messenger to be used for communication.

    FCT *handshaker* -- Handshake protocol to be used. This function
    must accept a [Messenger] and [RecogStartMgr] as arguments.

    CLASS ATTRIBUTES**
    
    *none* --

    ..[Messenger] file:///./messaging.Messenger.html"""
    
    def __init__(self, messenger, handshaker, **args_super):
        self.deep_construct(VCConnectionHandler, 
                            {'messenger': messenger,
                             'handshaker': handshaker}, 
                            args_super, 
                            {})
   
    def handle(self):
        print '... Connection %s: Starting handler' % self.request.__dict__
        f = self.request.makefile()        
        self.messenger.transporter.sock = self.request
        self.handshaker(self.messenger, ???Some RecogStartMgr instance???)


class VCListenerHandler(VCConnectionHandler):
    """Creates a VC listener connection for a new editor.
    
    **INSTANCE ATTRIBUTES**

    [Messenger] *messenger* -- Messenger to be used for communication.

    FCT *handshaker* -- Handshake protocol to be used. This function
    must accept a [Messenger] and [RecogStartMgr] as arguments.

    CLASS ATTRIBUTES**
    
    *none* --

    ..[Messenger] file:///./messaging.Messenger.html"""    
                                
    def __init__(self, messenger=None, **args_super):

        #
        # Note: Enforce handshaker=vc_listener_handshake
        #
        self.deep_construct(VCListenerHandler, 
                            {'messenger': messenger, 
                             'handshaker': handshake}, 
                            args_super, 
                            {},
                            enforce_value={'handshaker': vc_listener_handshake}
                           )

class VCTalkerHandler(VCConnectionHandler):
    """Creates a VC talker connection for a new editor.
    
    **INSTANCE ATTRIBUTES**

    [Messenger] *messenger* -- Messenger to be used for communication.

    FCT *handshaker* -- Handshake protocol to be used. This function
    must accept a [Messenger] and [RecogStartMgr] as arguments.

    CLASS ATTRIBUTES**
    
    *none* --

    ..[Messenger] file:///./messaging.Messenger.html"""    
                                
    def __init__(self, messenger=None, **args_super):

        #
        # Note: Enforce handshaker=vc_talker_handshake
        #
        self.deep_construct(VCTalkerHandler, 
                            {'messenger': messenger, 
                             'handshaker': handshake}, 
                            args_super, 
                            {},
                            enforce_value={'handshaker': vc_talker_handshake}
                           )


        
class ConnectionServer(threading.Thread):
    """Listens for new connections from external editor.
            
    **INSTANCE ATTRIBUTES**

    INT *port* -- Port number on which to listen for the new connections.
    
    CLASS *handler_class* -- Class to be used for spawning a handler
    for a new conneciton. This class must be a subclass of
    [BaseRequestHandler].

    CLASS ATTRIBUTES**
    
    *none* --

    ..[Messenger] file:///./messaging.Messenger.html"""    

    
   def __init__(self, port, handler_class):
       self.server = SocketServer.ThreadingTCPServer(("", port), handler_class)
       threading.Thread.__init__(self)
       
   def run(self):
       self.server.serve_forever()


def start_servers():
    """Start 2 servers listening for new connections from external editors

    One server listens for VC listener connections (i.e. connections
    that will be used by VC to listen for commands from the editor)

    The other server listens for VC talker connections
    (i.e. connections that will be used by VC to send commands to the
    editor).    
    """
    
    vc_listener_server = ConnectionServer(port=VC_LISTENER_PORT, handler_class=VCListenerHandler)
    vc_listener_server.start()
    
    vc_talker_server = ConnectionServer(port=VC_TALKER_PORT, handler_class=VCTalkerHandler)
    vc_talker_server.start()


    
if __name__ == '__main__':
    start_server()
    
