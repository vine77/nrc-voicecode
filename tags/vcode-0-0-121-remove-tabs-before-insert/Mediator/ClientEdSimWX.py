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

"""test implementation of a VoiceCode TCP/IP client using EdSim as its
editor, but with a wxPython message loop.
"""


import os, posixpath, pythoncom, re, select, socket
import SocketServer, string, sys, threading, time, whrandom, win32event

import AppState

import debug
import EdSim
import messaging, Object
import util
import Queue

import thread_communication_WX
import tcp_client
from tcp_threads import *
from wxPython.wx import *

def EVT_MINE(evt_handler, evt_type, func):
    evt_handler.Connect(-1, -1, evt_type, func)

# create a unique event type
wxEVT_SOCKET_DATA = wxNewEventType()

class ClientEdSimPane(wxPanel, Object.OwnerObject):
    def __init__(self, parent, ID, client_name, **args):
	self.deep_construct(ClientEdSimPane,
	                    {'parent': parent,
			     'client_name': client_name,
			     'connection': tcp_client.ClientConnection(),
			     'connect_button': None,
			     'text': None,
			     'exiting': 0
			    }, args, exclude_bases = {wxPanel:1}) 
        wxPanel.__init__(self, parent, ID, wxDefaultPosition, wxDefaultSize)
	self.name_parent('parent')

        vbox = wxBoxSizer(wxVERTICAL)
	ID_CONNECT_DISCONNECT = wxNewId()
	ID_TEXT = wxNewId()
	self.connect_button = wxButton(self, ID_CONNECT_DISCONNECT, "Connect", 
	    wxDefaultPosition, wxDefaultSize)
	self.text = wxStaticText(self, ID_TEXT, "", wxDefaultPosition, 
	    wxDefaultSize)
	vbox.Add(self.connect_button, 0) # don't stretch vertically (or horizontally)
	vbox.Add(self.text, 1, wxEXPAND) # stretch in both directions


	EVT_BUTTON(self, ID_CONNECT_DISCONNECT, self.on_toggle_connection)
        self.SetAutoLayout(1)
        self.SetSizer(vbox)
        vbox.Fit(self)
        vbox.SetSizeHints(self)

    def on_toggle_connection(self, event):
	if self.exiting:
	    event.Skip()
	    return
	if self.connection.is_connected():
	    self.disconnect()
	else:
	    self.connect()

    def disconnected(self):
	self.connection.disconnect()
	self.update_button()

    def update_button(self):
        if self.connection.is_connected():
	    self.connect_button.SetLabel("Disconnect")
	else:
	    self.connect_button.SetLabel("Connect")
	self.connect_button.Enable(1)

    def disconnect(self):
	if not self.connection.is_connected():
	    return 1
	dlg = wxMessageDialog(self, "Disconnect: Are you sure?",
	    "Disconnect from Server", wxYES_NO | wxNO_DEFAULT)
	answer = dlg.ShowModal()
	dlg.Destroy()
	if answer == wxID_YES:
	    self.parent.app.editor.disconnected()
	    self.connection.disconnect()
	    self.connect_button.SetLabel("Connect")
	    return 1
	return 0

    def connect(self):
	self.connect_button.Enable(0)
# hook that type to the app's on_data method
	EVT_MINE(self.parent.app, wxEVT_SOCKET_DATA, 
	    self.parent.app.on_data)
# unlike server, only one event per client, so we don't need to use
# SocketHasDataWX, which is designed to be constructed with a socket_ID
	event = thread_communication_WX.InterThreadEventWX(self.parent.app,
	    wxEVT_SOCKET_DATA) 
	try:
	    messengers = self.connection.connect(self.client_name, event,
		test_client = 1)
	except socket.error:
	    messengers = None
	if messengers == None:
	    dlg = wxMessageDialog(self, "Unable to connect to server",
	        "Connection Error",
		wxICON_ERROR | wxOK)
	    dlg.ShowModal()
	    dlg.Destroy()
	    self.connect_button.Enable(1)
	    return
	self.connect_button.Enable(1)
	self.connect_button.SetLabel("Disconnect")
	talk, listen = messengers
	self.parent.app.editor.connected(talk, listen)

    def remove_other_references(self):
	self.exiting = 1
	Object.OwnerObject.remove_other_references(self)
	self.connect_button.Destroy()
	self.text.Destroy()

class ClientEdSimFrame(wxFrame, Object.OwnerObject):

    def remove_other_references(self):
	self.exiting = 1
	Object.OwnerObject.remove_other_references(self)


    def disconnected(self):
        self.pane.disconnected()

    def __init__(self, app, parent, ID, title, client_name, **args):
	self.deep_construct(ClientEdSimFrame,
	                    {'app': app,
			     'pane': None,
			     'exiting': 0
			    }, args, exclude_bases = {wxFrame:1}) 
        wxFrame.__init__(self, parent, ID, title, wxDefaultPosition,
	    wxSize(1000, 600))
	self.name_parent('app')
	self.add_owned('pane')

	self.pane = ClientEdSimPane(self, -1, client_name) 
        EVT_CLOSE(self, self.on_close)        

    def on_close(self, event):
	if not self.exiting:
	    should_close = self.pane.disconnect()
	    if should_close:
		self.cleanup()
		event.Skip()        


class ClientEdSimWX(wxApp, Object.OwnerObject):
    """class for running the EdSim editor simulator as a TCP client, but
    using the event mechanism of wxPython for inter-thread communication

    **INSTANCE ATTRIBUTES**

    ClientEditorChangeSpec *editor* -- the client wrapper for the EdSim 
    instance

    BOOL *client_indentation* -- if true, use the name
    EdSimClientIndent when handshaking with the server, to ensure that
    the server will not override indentation on the server-side.

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, multiple = 0, print_buff = 0, client_indentation = 0,
	**args):
	"""
	**INPUTS**

	*BOOL multiple* -- should this EdSim allow for multiple open
	buffers?

	*BOOL print_buff* -- should this EdSim call print_buff whenever
	the buffer changes?

	BOOL *client_indentation* -- if true, use the name
	EdSimClientIndent when handshaking with the server, to ensure that
	the server will not override indentation on the server-side.
	"""
	self.deep_construct(ClientEdSimWX,
	                    {
			     'client_indentation': client_indentation,
			     'editor': None
			    }, args, 
			    exclude_bases = {wxApp: 1})
	dummy = "ceswx.err"
	dummy = 0
        wxApp.__init__(self, dummy)

	underlying_editor = EdSim.EdSim(multiple = multiple, 
	   print_buff_when_changed = print_buff)
	self.editor = tcp_client.ClientEditorChangeSpec(editor = underlying_editor, 
	    owner = self, ID = 'dummy')

    def mediator_closing(self, ID, unexpected = 0):
	self.editor.disconnected()
	self.frame.disconnected()

    def OnInit(self):
	client_name = 'EdSim'
	if self.client_indentation:
	    client_name = 'EdSimClientIndent'
	frame = ClientEdSimFrame(self, NULL, -1, "ClientEdSim", client_name)
        frame.Show(true)
#        frame.pane.initial_show()
        self.SetTopWindow(frame)
	self.frame = frame
	self.add_owned('frame')
        return true

    def on_data(self, event):
	self.editor.mediator_cmd()

    def run(self):
	self.MainLoop()
	

def run(multiple = 0, print_buff = 0, client_indentation = 0):
    app = ClientEdSimWX(multiple = multiple, print_buff = print_buff, 
	client_indentation = client_indentation)
    app.run()


if __name__ == '__main__':
    run()
