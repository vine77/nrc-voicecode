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

"""classes for creating VoiceCode TCP/IP client as a counterpart to 
AppStateMessaging and communicating with it via the ServerMainThread classes in tcp_server.py
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
from tcp_server import messenger_factory



# Uncomment this and add some entries to active_traces if you want to 
# activate some traces.
#debug.config_traces(status="on", active_traces={'get_mess':1, 'send_mess': 1})
#debug.config_traces(status="on", active_traces = 'all')
#debug.config_traces(status="on", active_traces = {'sr_interface':1},
#allow_trace_id_substrings = 1)

#
# Port numbers for the communication link
#
VC_LISTENER_PORT = 45770
VC_TALKER_PORT = 45771

class ClientConnection(Object.Object):
    """class for connecting to the TCP mediator server and listening for 
    incoming messages.

    connect will create a ListenAndQueueMsgsThread to listen 
    for data on the talk_sock (the mediator server talks on the talk_sock, 
    while we listen) and queue complete messages.  
    The LAQM Thread also notifies the main thread of a pending message using a
    SocketHasDataEvent.  

    **INSTANCE ATTRIBUTES**

    ListenAndQueueMsgsThread *data_thread* -- 
    thread which polls for data from the listen messenger

    BOOL *connecting* -- flag indicating that the server is in the
    process of connecting to the mediator

    BOOL *connected* -- flag indicating that the server is 
    connected to the mediator

    STR *ID* -- unique ID assigned to this connection

    Queue *listen_queue* -- the queue to which the listen thread will
    append complete messages received on the vc_listen connection

    **CLASS ATTRIBUTES**
    
    *none* -- 

    """
    
    def __init__(self, **args_super):
        self.deep_construct(ClientConnection, 
                            {
			     'data_thread': None,
			     'connecting': 0,
			     'connected': 0,
			     'ID': None,
			     'listen_queue': None
                             }, 
                            args_super)

    def new_data_thread_given_event(self, listen_sock, data_event):
        """creates a new ListenAndQueueMsgsThread to monitor the
	listen_sock
        
        **INPUTS**

	SocketHasDataEvent *data_event* -- the SocketHasDataEvent event
	to pass to the new thread

        STR *ID* -- The unique ID of the listen socket
        
        socket *listen_sock* -- The listen socket
        
        **OUTPUTS**
        
        [ListenAndQueueMsgsThread] -- the new threading.Thread object

        ..[ListenAndQueueMsgsThread] 
	file:///./tcp_server.ListenAndQueueMsgsThread.html"""        
	a_msgr = messenger_factory(listen_sock)
	queue = Queue.Queue(10)
	thread = ListenAndQueueMsgsThread( a_msgr, queue, data_event)
	return thread

    def is_connected(self):
	"""tells whether the client is currently connected or connecting
	to the mediator

	**INPUTS**

	*none*

	**OUTPUTS**

	*BOOL* -- true if the  client is currently connected (or
	connecting) to a mediator
	"""
	return self.connecting or self.connected

    def open_vc_listener_conn(self, app_name, host, listen_port):
        """Connects to VoiceCode on the listen port

	**INPUTS**

	*STR* app_name -- name of the application to give to the
	mediator

	*STR* host -- name or IP address of the host on which the
	mediator server is running.  Defaults to a server running
	locally.

	*INT* listen_port -- port number on which the server expects
	new listen connections

	**OUTPUTS**

	*Messenger* -- a Messenger for the vc_listener connection, or 
	None if the connection was not made successfully
	"""

        a_socket = socket(AF_INET, SOCK_STREAM)
        a_socket.connect(host, listen_port)
        
        #
        # Create a messenger
        #
        packager = messaging.MessPackager_FixedLenSeq()
        transporter = messaging.MessTransporter_Socket(sock=a_socket)
        encoder = messaging.MessEncoderWDDX()
        vc_listen_msgr = messaging.MessengerBasic(packager=packager, 
	    transporter=transporter, encoder=encoder)

        trace('ClientConnection.open_vc_listener_conn',
              'sending name of editor')
        
        #
        # Send name of editor
        #
        vc_listen_msgr.get_mess(expect=['send_app_name'])
        vc_listen_msgr.send_mess('app_name', {'value': app_name})


        trace('ClientConnection.open_vc_listener_conn',
              'getting ID')
        
        #
        # Get unique identifier from VoiceCode
        #
        msg = vc_listen_msgr.get_mess(expect=['your_id_is'])
        self.ID = msg[1]['value']
        vc_listen_msgr.send_mess('ok')
        
        trace('ClientConnection.open_vc_listener_conn',
              'done')

	return vc_listen_msgr

    def open_vc_talker_conn(self, host, talk_port):
        """Connects to VoiceCode on the talk port
        
        **INPUTS**

	*STR* host -- name or IP address of the host on which the
	mediator server is running.  Defaults to a server running
	locally.

	*INT* talk_port -- port number on which the server expects
	new talk connections

	**OUTPUTS**

	*socket* -- socket for the talk connection, or None if the 
	connection was not made successfully
        """

        trace('ClientConnection.open_vc_talker_conn', 'started')
        
        #
        # Open the socket
        #
        a_socket = socket(AF_INET, SOCK_STREAM)
        a_socket.connect(host, talk_port)

        trace('ClientConnection.open_vc_talker_conn', 'socket opened')
        
        #
        # Create a temporary messenger
        #
        packager = messaging.MessPackager_FixedLenSeq()
        transporter = messaging.MessTransporter_Socket(sock=a_socket)
        encoder = messaging.MessEncoderWDDX()
        vc_talk_msgr = messaging.MessengerBasic(packager=packager, transporter=transporter, encoder=encoder)
        

        trace('ClientConnection.open_vc_talker_conn', 'sending ID')
        
        #
        # Send the connection pair ID to the remote server
        #
        vc_talk_msgr.get_mess(expect=['send_id'])
        vc_talk_msgr.send_mess('my_id_is', {'value': self.ID})
        
        trace('test_TCP_server.open_vc_talker_conn', 'done')
	return a_socket

    def connect(self, app_name, data_event,
	    host = None, 
	    listen_port = VC_LISTENER_PORT,
	    talk_port = VC_TALKER_PORT):
	"""connect to the mediator

	**INPUTS**

	*STR* app_name -- name of the application to give to the
	mediator

	SocketHasDataEvent *data_event* -- the SocketHasDataEvent event
	to pass to the new data thread so it can notify the main thread
	when there is a command waiting in the queue.

	*STR* host -- name or IP address of the host on which the
	mediator server is running.  Defaults to a server running
	locally.

	*INT* listen_port -- port number on which the server expects
	new listen connections

	*INT* talk_port -- port number on which the server expects
	new talk connections

	**OUTPUTS**

	*Messenger* -- a Messenger for the talk connection, or None if the 
	connection was not made successfully
	"""
	if self.is_connected():
	    return None
	self.connecting = 1

	if host == None:
	    host = gethostname()
	# vc listener means the VoiceCode mediator is listening -- we're
	# talking
        talk_msgr = self.open_vc_listener_conn(app_name, host, listen_port)
	if talk_msgr == None:
	    self.connecting = 0
	    return None
	# vc talker means the VoiceCode mediator is talking -- we're
	# listening
        listen_sock = self.open_vc_talker_conn(host, talk_port)
	if listen_sock == None:
	    self.connecting = 0
	    return None

	self.connecting = 0
	self.connected = 1

	self.listen_queue = self.listen(listen_sock, data_event)
	return talk_msgr

    def disconnect(self, notify = 1):
	"""disconnect from the mediator
	
	**INPUTS**

	*BOOL* notify -- true if we should notify the mediator that we
	are disconnecting.  False if we are calling disconnect in
	response to a disconnection from the mediator and should
	therefore disconnect silently.

	**OUTPUTS**

	*BOOL* -- true if we disconnected successfully
	"""
	if not self.is_connected():
	    return 0

    def listen(self, listen_sock):
        """creates and starts a data thread on the listen_sock
        
        **INPUTS**
        
        socket *listen_sock* -- The listen socket

        **OUTPUTS**
        
	*Queue* -- the Queue to which complete messages from the 
	listen_sock will be appended.
	"""
        
	data_thread = self.new_data_thread_given_event(listen_sock,
	    data_event)
	self.data_thread = data_thread
	messages = data_thread.message_queue()
	data_thread.setDaemon(1)
	data_thread.start()
	
	return messages

class ClientEditor(Object.OwnerObject):
    """abstract base class for handling messages to and from the client editor

    **INSTANCE ATTRIBUTES**

    Messenger *talk_msgr* -- Messenger for sending commands to the mediator

    MixedMessenger *listen_msgr* -- MixedMessenger for receiving commands from 
    the mediator without blocking

    AppState *editor* -- the AppState interface to the underlying editor

    *{STR:FCT}* msg_map -- map from message names to (unbound) methods
    taking *(self, {arg:val})* to handle that message

    *[STR] expect* -- list of commands expected from the mediator

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, **args):
	self.deep_construct(ClientEditor,
	                    {
			     'talk_msgr': None,
			     'listen_msgr': None,
			     'editor': editor,
			     'msg_map': {},
			     'expect': []
			    },
			    args)
	self.expect=['recog_begin', 'recog_end', 'cur_pos', 
	    'confirm_buffer_exists', 'list_open_buffers', 'get_selection', 
	    'set_selection', 'get_text', 'make_position_visible', 'len', 
	    'insert', 'delete', 'goto', 'active_buffer_name', 
	    'multiple_buffers', 'bidirectional_selection', 'get_visible', 
	    'language_name', 'newline_conventions', 
	    'pref_newline_convention', 'open_file', 'close_buffer', 
	    'terminating', 'mediator_closing', 'update']
	for msg_name in self.expect:
	    method_name = 'cmd_' + msg_name
	    msg_handler = self.__class__.__dict__[method_name]
	    self.msg_map[msg_name] = msg_handler

    def disconnected(self):
	"""method to call to let the ClientEditor know that the client
	has disconnected from the mediator
	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	self.talk_msgr = None
	self.listen_msgr = None
	self.editor.set_change_callback(None)

    def connected(self, talk_msgr, listen_msgr):
	"""method to call to let the ClientEditor know that the client
	has connected to the mediator, and can communicate with it by
	means of the provided talk_msgr and listen_msgr.

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	self.talk_msgr = talk_msgr
	self.listen_msgr = listen_msgr
	self.editor.set_change_callback(self.on_change)
	
    def on_change(self, start, end, text, selection_start,
	selection_end, buff_name, program_initiated):
	pass
     
    def mediator_cmd(self):
	"""method to call when the main thread receives a message
	from the data thread that a command from the mediator is waiting
	in the queue

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	if self.mediator_cmds:
	    cmd = self.listen_msgr.get_mess(expect = self.expect)
	    if cmd:
		self.do_cmd(cmd)

    def do_cmd(self, cmd):
	"""perform the appropriate action in response to the command
	from the mediator

	**INPUTS**

	(STR, {STR: STR}) cmd -- The message retrieved
        from external editor in *(mess_name, {arg:val})* format
 
	**OUTPUTS**

	*none*
	"""
	handler = self.msg_map[cmd[0]]
	handler(self, cmd[1])

    def cmd_recog_begin(self, arguments):
	window_id = arguments['window_id']
	block = arguments['block']
	value = self.editor.recog_begin(window_id, block)
	self.listen_msgr.send_mess('recog_begin_resp', {'value': value}) 

    def cmd_recog_end(self, arguments):
	value = self.editor.recog_end()
	self.listen_msgr.send_mess('recog_end_resp')

    def cmd_cur_pos(self, arguments):
	buff_name = arguments['buff_name']
	value = self.editor.cur_pos(buff_name = buff_name)
	self.listen_msgr.send_mess('cur_pos_resp', {'value': value})

    def cmd_confirm_buffer_exists(self, arguments):
	buff_name = arguments['buff_name']
	value = self.editor.query_buffer_from_app(buff_name)
	self.listen_msgr.send_mess('confirm_buffer_exists_resp', 
	    {'value': value})

    def cmd_list_open_buffers(self, arguments):
	value = self.editor.open_buffers_from_app()
	self.listen_msgr.send_mess('list_open_buffers_resp', {'value': value})

    def cmd_get_selection(self, arguments):
	buff_name = arguments['buff_name']
	value = self.editor.get_selection(buff_name = buff_name)
	self.listen_msgr.send_mess('get_selection_resp', 
	    {'value': value})
 
    def sel_update(self, buff_name = None):
	"""create update descriptions for the current cursor location
	and selection for a given buffer

	**INPUTS**

	*STR buff_name* -- name of the buffer, or None for the current
	buffer

	**OUTPUTS**

	*[{STR:ANY}]* -- the update descriptions
	"""
	if buff_name == None:
	    buff_name = self.editor.app_active_buffer_name()
	buff = self.editor.find_buff(buff_name)
        updates = []

        updates.append({'action': 'select', 'range': buff.get_selection(), 
	    'buff_name': buff_name})        
        updates.append({'action': 'goto', 'pos': buff.cur_pos(), 
	    'buff_name': buff_name})

        return updates
     


        
    def cmd_set_selection(self, arguments):
	buff_name = arguments['buff_name']
	range = arguments['range']
	cursor_at = arguments['cursor_at']
	self.editor.set_selection(range, cursor_at, buff_name = buff_name)
	updates =  self.sel_updates(buff_name)
	self.listen_msgr.send_mess('set_selection_resp',
	    {'updates': updates})

    def cmd_get_text(self, arguments):
	buff_name = arguments['buff_name']
	value = self.editor.get_text(buff_name = buff_name)
	self.listen_msgr.send_mess('get_text_resp', 
	    {'value': value})
 
    def cmd_set_text(self, arguments):
	buff_name = arguments['buff_name']
	range = arguments['range']
	cursor_at = arguments['cursor_at']
	self.editor.set_text(range, cursor_at, buff_name = buff_name)
	self.listen_msgr.send_mess('set_text_resp')




  	


class ClientMainThread(Object.OwnerObject):
    """abstract base class for the main thread of an editor client to
    the mediator server.

    **INSTANCE ATTRIBUTES**

    ClientConnection *connection* -- the connection to the mediator
    server

    Queue *mediator_cmds* -- the queue to which commands from the
    mediator are added

    AppState, AppChangeSpec *editor* -- the editor, supporting the
    AppState interface, as well as the AppChangeSpec interface for

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, **args):
	self.deep_construct(ClientMainThread,
	                    {
			     'connection': None,
			     'editor': None,
			     'mediator_cmds': None
			    },
			    args)






