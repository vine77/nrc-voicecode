"""This script implements a simple editor (based on EdSim) that
communicates with VoiceCode through a TCP/IP messaging protocol.
"""

from socket import *
import os, natlink, sys, threading
import EdSim, mediator, messaging, Object, SourceBuffEdSim, sim_commands, sr_interface

VC_LISTENER_PORT = 45770
VC_TALKER_PORT = 45771


HOST = gethostname()


def create_tcp_mess(sock):
    """Creates a TCP/IP messenger
    
    **INPUTS**
    
    socket *sock* -- The socket to connect the messenger to.
    
    
    **OUTPUTS**
    
    [Messenger] *msgr* -- 

    file:///./messaging.Messenger.html"""

    packager = messaging.MessPackager_FixedLenSeq()
    transporter = messaging.MessTransporter_Socket(sock=sock)
    encoder = messaging.MessEncoderWDDX()
    msgr = messaging.Messenger(packager, transporter, encoder)
    
    return msgr


class ListenThread(threading.Thread, Object.Object):
    """Thread that listens for commands from VoiceCode and executes them.
    
    **INSTANCE ATTRIBUTES**
    
    [Messenger] *messenger* -- Messenger used to listen for requests.

    [ExternalEdSim] *xed* -- The external editor to execute the requests on.

    CLASS ATTRIBUTES**
    
    *none* -- 

    ..[Messenger] file:///./messaging.Messenger.html]
    ..[ExternalEdSim] file:///./test_TCP_server.ExternalEdSim.html"""
    
    def __init__(self, xed, messenger, **args_super):
        threading.Thread.__init__(self)        
        self.deep_construct(ListenThread, 
                            {'messenger': messenger, 'xed': xed}, 
                            args_super, 
                            {})


    def upd_curpos_sel(self):
        
        """Returns a list of updates, whose effect is to synchronise the cursor position and selection.

       
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        buff_name = self.xed.ed.app_active_buffer_name()
        updates = []

        updates.append({'action': 'set_selection', 'range': self.xed.ed.get_selection(), 'buff_name': buff_name})        
        updates.append({'action': 'goto', 'pos': self.xed.ed.cur_pos(), 'buff_name': buff_name})

        return updates
            

    def execute_request(self, req):
        """Executes a request received from VoiceCode.
        
        **INPUTS**
        
        ANY *req* -- undocumented 
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        print '-- execute_request: req=%s' % repr(req)
        
        buff_name = self.xed.ed.app_active_buffer_name()
        action = req[0]
        args = req[1]
        if action == 'active_buffer_name':
            self.xed.vc_talk_msgr.send_mess('active_buffer_name_resp', {'value': self.xed.ed.only_buffer_name})
        elif action == 'language_name':
            self.xed.vc_talk_msgr.send_mess('language_name_resp', {'value': self.xed.ed.only_buffer.language_name()})
        elif action == 'newline_conventions':
            self.xed.vc_talk_msgr.send_mess('newline_conventions_resp', {'value': self.xed.ed.only_buffer.newline_conventions()})
        elif action == 'pref_newline_convention':
            self.xed.vc_talk_msgr.send_mess('pref_newline_convention_resp', {'value': self.xed.ed.only_buffer.pref_newline_convention()})                        
        elif action == 'cur_pos':
            self.xed.vc_talk_msgr.send_mess('cur_pos_resp', {'value': self.xed.ed.cur_pos()})

        elif action == 'multiple_buffers':
            self.xed.vc_talk_msgr.send_mess('multiple_buffers_resp', {'value': 0})            
        elif action == 'bidirectional_selection':
            self.xed.vc_talk_msgr.send_mess('bidirectional_selection_resp', {'value': 0})    
        elif action == 'get_selection':
            self.xed.vc_talk_msgr.send_mess('get_selection_resp', {'value': self.xed.ed.get_selection()})
        elif action == 'set_selection':
            range = messaging.messarg2intlist(args['range'])
            cursor_at = messaging.messarg2int(args['cursor_at'])
            self.xed.ed.set_selection(range=range, cursor_at=cursor_at)
            self.xed.vc_talk_msgr.send_mess('set_selection_resp', {'updates': self.upd_curpos_sel()})
        elif action == 'get_text':
            print '-- execute_request: get_text, args[\'start\']=%s, args[\'end\']=%s' % ( args['start'], args['end'])
            start = messaging.messarg2int(args['start'])
            end = messaging.messarg2int(args['end'])
            self.xed.vc_talk_msgr.send_mess('get_text_resp', {'value': self.xed.ed.get_text(start, end)})
            print '-- execute_request: request=\'get_text\', sending self.xed.ed.get_text(start, end)[0:100]=%s' % self.xed.ed.get_text(start, end)[0:100]

        elif action == 'get_visible':
            self.xed.vc_talk_msgr.send_mess('get_visible_resp', {'value': self.xed.ed.get_visible()})            

        elif action == 'make_position_visible':
            self.xed.vc_talk_msgr.send_mess('make_position_visible_resp', {'updates': self.upd_curpos_sel()})

        elif action == 'len':
            self.xed.vc_talk_msgr.send_mess('len', {'value': self.xed.ed.len()})

        elif action == 'insert':
            print '-- execute_request: args=%s' % repr(args)
            text = args['text']
            range = messaging.messarg2intlist(args['range'])
            self.xed.ed.insert(text, range)
            updates = [{'action': 'insert', 'range': range, 'text': text, 'buff_name': buff_name}]
            updates = updates + self.upd_curpos_sel()
            self.xed.vc_talk_msgr.send_mess('insert_resp', {'updates': updates})
            
        elif action == 'delete':
            range = messaging.messarg2intlist(args['range'])            
            self.xed.ed.delete(range=range)
            updates = [{'action': 'delete', 'range': range, 'buff_name': buff_name}]
            print "-- execute_request: updates=%s, self.upd_curpos_sel()=%s" % (repr(updates), repr(self.upd_curpos_sel()))
            updates = updates + self.upd_curpos_sel()
            self.xed.vc_talk_msgr.send_mess('delete_resp', {'updates': updates})

        elif action == 'goto':
            pos = messaging.messarg2int(args['pos'])
            self.xed.ed.goto(pos)
            self.xed.vc_talk_msgr.send_mess('goto_resp', {'updates': self.upd_curpos_sel()})
        elif action == 'get_visible':
            self.xed.vc_talk_msgr.send_mess('get_visible_resp', {'value': self.xed.ed.get_visible()})
        elif action == 'stop_responding':
            self.xed.vc_talk_msgr.send_mess('stop_responding_resp')            
        elif action == 'start_responding':
            #
            # *start_responding* is invoked at the end of an utterance.
            # print the updated buffer content.
            #
            self.xed.vc_talk_msgr.send_mess('start_responding_resp')
            self.xed.ed.refresh()
        elif action == 'refresh_if_necessary':
            self.xed.ed.refresh()
            self.xed.vc_talk_msgr.send_mess('refresh_if_necessary_resp')
        elif action == 'open_file':
            print '-- execute_request: action=\'open_file\''
            self.xed.ed.open_file(name=args['name'])

            #deb
#              print '-- test_tcp_server: after open_file("%s"), buffer contains:' % args['name']
#              self.xed.ed.print_buff()
            #fin
            
            self.xed.vc_talk_msgr.send_mess('open_file_resp')
        elif action == 'close_buffer':
            print '-- execute_request: action=\'close_buffer\''
            self.xed.ed.close_buffer(buff_name=args['buff_name'], save=['save'])
            self.xed.vc_talk_msgr.send_mess('ok')

    def run(self):
        """Listen for requests from VoiceCode and execute them.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        while 1:
#            print '--  ListenThread.run: polling VoiceCode'
            try:
                request = self.xed.vc_talk_msgr.get_mess(expect=['cur_pos', 'get_selection', 'set_selection', 'get_text', 'make_position_visible', 'len', 'insert', 'delete', 'goto', 'active_buffer_name', 'multiple_buffers', 'bidirectional_selection', 'get_visible', 'language_name', 'newline_conventions', 'pref_newline_convention', 'start_responding', 'stop_responding', 'open_file', 'refresh_if_necessary', 'close_buffer'])
                
                if not request:
                    print '.. Connection to VoiceCode closed!!!'
                    break                
                else:
                    print '.. Received request: %s' % repr(request)
                    self.execute_request(request)
            except error:
                print '.. ERROR RECEIVING REQUEST!!!'
                break
                
#            time.sleep(1)

        self.xed.vc_talk_msgr.transporter.close()


class ExternalEdSim(Object.Object):
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

        print '-- open_vc_listener_conn: started'

        global HOST
        a_socket = socket(AF_INET, SOCK_STREAM)
        a_socket.connect(HOST, VC_LISTENER_PORT)
        
        #
        # Create a messenger
        #
        packager = messaging.MessPackager_FixedLenSeq()
        transporter = messaging.MessTransporter_Socket(sock=a_socket)
        encoder = messaging.MessEncoderWDDX()
        self.vc_listen_msgr = messaging.Messenger(packager=packager, transporter=transporter, encoder=encoder)

        print '-- open_vc_listener_conn: sending name of editor'
        
        #
        # Send name of editor
        #
        self.vc_listen_msgr.send_mess('app_name', {'value': 'EdSim'})


        print '-- open_vc_listener_conn: getting ID'
        
        #
        # Get unique identifier from VoiceCode
        #
        msg = self.vc_listen_msgr.get_mess(expect=['your_id_is'])
        self.id = msg[1]['value']
        self.vc_listen_msgr.send_mess('ok')
        
        print '-- open_vc_listener_conn: done'




    def open_vc_talker_conn(self):
        """Connects to VoiceCode on the VC_TALKER port
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        global HOST

        print '-- open_vc_talker_conn: started'
        
        #
        # Open the socket
        #
        a_socket = socket(AF_INET, SOCK_STREAM)
        a_socket.connect(HOST, VC_TALKER_PORT)      

        print '-- open_vc_talker_conn: socket opened'
        
        #
        # Create a messenger
        #
        packager = messaging.MessPackager_FixedLenSeq()
        transporter = messaging.MessTransporter_Socket(sock=a_socket)
        encoder = messaging.MessEncoderWDDX()
        self.vc_talk_msgr = messaging.Messenger(packager=packager, transporter=transporter, encoder=encoder)
        

        print '-- open_vc_talker_conn: sending ID'
        
        #
        # Send the connection pair ID to the remote server
        #
        self.vc_talk_msgr.send_mess('my_id_is', {'value': self.id})
        answer = self.vc_talk_msgr.get_mess(expect=['ok'])        
        
        print '-- open_vc_talker_conn: done'

    def listen(self):
        """Listens for commands from VoiceCode and executes them.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        new_thread = ListenThread(xed=self, messenger=self.vc_talk_msgr)
        new_thread.start()


    def connect(self):
        """Connect to VoiceCode
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        self.open_vc_listener_conn()
        print '-- ExternalEdSim.connect: after open_vc_listener_conn'
        self.open_vc_talker_conn()
        print '-- ExternalEdSim.connect: after open_vc_talker_conn'

        #begin
#          while 1:
#              print '-- just shooting the breeze'
#              pass
        #end
        
        self.listen()



    def start_shell(self):
        """
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        sr_interface.connect()

        # define some useful local variables
        home = os.environ['VCODE_HOME']
        sim_commands.command_space['home'] = home
        sim_commands.command_space['testdata'] = \
                  os.path.join(home, 'Data', 'TestData')

        sim_commands.help()

# This needs to be rewritten with select() so that it is non-blocking
#          while not sim_commands.quit_flag:
#              cmd = raw_input('Command> ')
#              mediator.execute_command(cmd)            
        
        sr_interface.disconnect()

        print '-- start_shell: disconnected'

        sys.exit()


if __name__ == '__main__':

    sr_interface.connect()
    window = natlink.getCurrentModule()[2]
    print '-- __main__: window=%s' % window
    sr_interface.disconnect()

    an_editor = ExternalEdSim()
    an_editor.ed.open_file('abc.py')
    an_editor.connect()
#    an_editor.start_shell()

