"""This script implements a simple editor (based on EdSim) that
communicates with VoiceCode through a TCP/IP messaging protocol.
"""

import threading
import EdSim, messaging, server

VC_LISTENER_PORT = 45770
VC_TALKER_PORT = 45771


class ListenThread(threading.Thread):
    """Thread that listens for commands from VoiceCode and executes them.
    
    **INSTANCE ATTRIBUTES**
    
    [Messenger] *messenger=None* -- Messenger used to listen for requests.

    CLASS ATTRIBUTES**
    
    *none* -- 

    ..[Messenger] file:///./messaging.Messenger.html"""
    
    def __init__(self, messenger, **args_super):
        self.deep_construct(ListenThread, 
                            {'messenger': messenger}, 
                            args_super, 
                            {})



    def run(self):
        """Listen for requests from VoiceCode and execute them.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        ???? Not completed
        while 1:
            print '..  polling VoiceCode'
            try:
                request = self.messenger.get_mess()
                if not request:
                    print '.. Connection to VoiceCode closed!!!'
                    break                
                else:
                    print '.. Received request: %s' % repr(request)
                    self.execute_request(request)
                    resp = ('ok', {})
                    self.messenger.send_mess(resp[0], resp[1])
                    print 'FROM_SERVER (%s) -> %s, %s\n' % (self.id, resp[0], repr(resp[1]))
                
            except error:
                print '.. FROM_SERVER (%s): error received' % self.id
                break
                
            time.sleep(1)

        self.messenger.transporter.close()


class ExternalEdSim:
    """A simple external editor for testing the TCP/IP link.
    
    **INSTANCE ATTRIBUTES**
    
    [EdSim] *ed* -- The editor object.

    CLASS ATTRIBUTES**
    
    *none* -- 

    ..[EdSim] file:///./EdSim.EdSim.html"""
    
    def __init__(self, **args_super):
        self.deep_construct(ExternalEdSim, 
                            {'ed': EdSim.EdSim(), 'id': None}, 
                            args_super, 
                            {})




    def open_vc_listener_conn(self):
        """Connects to VoiceCode on the VC_LISTENER port.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none*
        """
        threading.Thread.__init__(self)
        a_socket = socket(AF_INET, SOCK_STREAM)
        a_socket.connect(HOST, VC_LISTENER_PORT)
        
        #
        # Create a messenger
        #
        packager = messaging.MessPackager_FixedLenSeq()
        transporter = messaging.MessTransporter_Socket(sock=a_socket)
        encoder = messaging.MessEncoder_LenPrefArgs()
        self.messenger = messaging.Messenger(packager=packager, transporter=transporter, encoder=encoder)

        #
        # Get unique identifier from VoiceCode
        #
        msg = self.messenger.get_mess()
        self.id = msg[1]['id']



    def open_vc_talker_conn(self):
        """Connects to VoiceCode on the VC_TALKER port
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        #
        # Open the socket
        #
        a_socket = socket(AF_INET, SOCK_STREAM)
        a_socket.connect(HOST, VC_TALKER_PORT)      
        
        #
        # Create a messenger
        #
        packager = messaging.MessPackager_FixedLenSeq()
        transporter = messaging.MessTransporter_Socket(sock=a_socket)
        encoder = messaging.MessEncoder_LenPrefArgs()
        self.messenger = messaging.Messenger(packager=packager, transporter=transporter, encoder=encoder)
        
        answer = self.messenger.get_mess()
        
        #
        # Send the connection pair ID to the remote server
        #
        self.messenger.send_mess('my_id_is', {'id': self.id})
        answer = self.messenger.get_mess()        
        


    def listen(self):
        """Listens for commands from VoiceCode and executes them.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        new_thread = ListenThread(messenger=???)
        new_thread.start()


    def connect(self):
        """Connect to VoiceCode
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        self.open_vc_listener_conn()
        self.open_vc_talker_conn()
        self.listen()
        


if __name__ == '__main__':

    an_editor = ExternalEdSim()
    an_editor.connect()
    an_editor.start_shell()

