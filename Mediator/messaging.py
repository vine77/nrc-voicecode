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
# (C)2000, National Research Council of Canada
#
##############################################################################

"""Classes for communicating with an external editor through a messaging protocol"""

import re
import Object

class Messenger(Object.Object):
   
    """This class transports messages betweeen external editor and
    mediator, through some network communication pipe.

    The class uses a three layer messaging protocol. The layers are:

    *Message transport* -- This layer is responsible for carrying
     bytes across the network.

     This is implemented by class [MessTransporter]

    *Message encoding* -- This layer is responsible for encoding the
     semantic content of the message into a string.

     This is implemented by class [MessEncoder]

    *Message packaging* -- This layer is responsible for packaging an
     encoded message (produced using the *Message encoding* layer)
     into a form that can be reliably sent over the net. Also
     responsible for sending the messages using the *Message
     Transport* layer.

     This is implemented by class [MessPackager]

     All three of [MessTransporter], [MessEncoder] and [MessPackager]
     are abstract classes. This allows [Messenger] to support a
     variety of different protocols by mixing appropriate concrete
     subclasses of those.
     

    *NOTE:* The functionality for packaging and shipping/receiving of
     messages are bundled together in [MessagePackager] because
     packaging generally affects the way you receive a message.

    For example, if you package the message as a fixed length string,
    you will receive it by reading that fixed length. If you package it
    as a length prefixed string, you will receive it by first reading
    the length and then reading that many characters.     

    
    **INSTANCE ATTRIBUTES**

    [MessPackager] *packager* -- Used to package and send messages, or
    receive and unpack them.

    [MessEncoder] *encoder* -- Used to translate a string
    message to a list of attribute/value pairs, and vice versa.
        
    [MessTransporter] *transporter* -- Transport channel used to carry
    bytes to to/from a connection.
    

    CLASS ATTRIBUTES**
    
    *none* --

    .. [MessTransporter] file:///./messenger.MessTransporter.html
    .. [MessEncoder] file:///./messenger.MessEncoder.html
    .. [MessPackager] file:///./messenger.MessPackager.html"""
    
    def __init__(self, packager, encoder, transporter, **args_super):
        self.deep_construct(Messenger, 
                            {'packager': packager,
                             'encoder': encoder,
                             'transporter': transporter}, 
                            args_super, 
                            {})



    def send_mess(self, mess_name, mess_argvals):
        
        """Sends a message to the external editor.

        **INPUTS**

        STR *mess_name* -- Identifier indicating what kind of message this is.
        
        {STR: STR} *mess_argvals* -- Dictionary of arguments and
        values for the message to be sent to the editor.
                
        **OUTPUTS**
        
        *none* response -- 
        """

#        print '-- send_mess: mess_name=\'%s\', mess_argvals=%s' % (mess_name, repr(mess_argvals))
        unpkd_mess = self.encoder.encode(mess_name, mess_argvals)
#        print '-- send_mess: unpkd_mess=\'%s\'' % unpkd_mess
        pkd_mess = self.packager.pack_mess(unpkd_mess)
#        print '-- send_mess: pkd_mess=\'%s\'' % pkd_mess        
        self.packager.send_packed_mess(pkd_mess, self.transporter)



    def get_mess(self):
        """Gets a message from the external editor.
        
        **INPUTS**
        
        *none* --

        **OUTPUTS**
        
        (STR, {STR: STR}) name_argvals_mess -- The message retrieved
         from external editor in *(mess_name, {arg:val})* format."""


#        print '-- get_mess: started'
        pkd_mess = self.packager.get_packed_mess(self.transporter)
#        print '-- get_mess: pkd_mess=\'%s\'' % pkd_mess                
        unpkd_mess = self.packager.unpack_mess(pkd_mess)
#        print '-- get_mess: unpkd_mess=\'%s\'' % unpkd_mess        
        name_argvals_mess = self.encoder.decode(unpkd_mess)
#        print '-- get_mess: received \'%s\', %s' % (name_argvals_mess[0], repr(name_argvals_mess[1]))
        return name_argvals_mess
        


class MessPackager(Object.Object):
    """'Shipping and receiving department' for messages.
    
    This class is used to package string messages and send them over a
    transport channel.

    Also used to receive string messages on a transport channel, and
    unpackage them.

    This is an abstract class.


    **INSTANCE ATTRIBUTES**
    
    *none*-- 
    
    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, **args_super):
        self.deep_construct(MessPackager, \
                            {}, \
                            args_super, \
                            {})



    def send_packed_mess(self, pkd_mess, transporter):
        """Send a packaged message over a transport channel.
        
        **INPUTS**
        
        STR *pkd_mess* -- The packed message
        
        [MessTransporter] *transporter* -- Transport channel to be used
        

        **OUTPUTS**
        
        *none* --

        .. [MessTransporter] file:///./messaging.MessTransporter.html"""
        
        debug.virtual('send_pkd_mess')

    def get_packed_mess(self, transporter):
        """Receive a packaged message over a transport channel.
        
        **INPUTS**
                
        [MessTransporter] *transporter* -- Transport channel to be used
        

        **OUTPUTS**

        STR *pkd_mess* -- The packed message

        .. [MessTransporter] file:///./messaging.MessTransporter.html"""
        
        debug.virtual('get_pkd_mess')        



    def pack_mess(self, mess):
        
        """Packs a message into a string that can be carried on a
        transport connection.
        
        **INPUTS**
        
        STR *mess* -- The message as a raw string
        

        **OUTPUTS**
        
        *STR packed_mess* -- The packed message
        """
        
        debug.virtual('pack_mess')

    def unpack_mess(self, mess):
        
        """Unpacks a message to a raw string..
        
        **INPUTS**
        
        *STR* mess -- The packed message
        

        **OUTPUTS**
        
        *STR un_packed_mess* -- The message unpacked to a raw string.
        """
        
        debug.virtual('unpack_mess')


class MessPackager_FixedLenSeq(MessPackager):
    """"Packages messages as a sequence of fixed length chunks.

    Message is packaged as a string which consists of a sequence of
    strings of length *chunk_len* (called the chunks). Chunks are in
    the format:
            
        fXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    where the first character f is 1 if this is the last chunk of the
    message and 0 otherwise. The last chunk in a message is padded
    with blanks on the right.
        

    **INSTANCE ATTRIBUTES**
    
    *none*-- 
    
    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, chunk_len=1024, **args_super):
        self.deep_construct(MessPackager_FixedLenSeq, 
                            {'chunk_len': chunk_len}, 
                            args_super, 
                            {})



    def send_packed_mess(self, pkd_mess, transporter):
        """Send a packaged message as a sequence of fixed length chunks.
        
        **INPUTS**
        
        STR *pkd_mess* -- The packed message
        
        [MessTransporter] *transporter* -- Transport channel to be used
        

        **OUTPUTS**
        
        *none* --

        ..[MessTransporter] file:///./messaging.MessTransporter.html"""
        
        #
        # Nothing particular about how such messages need to be sent.
        #
        transporter.send_string(pkd_mess)

    def get_packed_mess(self, transporter):
        """Receive a message packed as a sequence of fixed length chunks.
        
        **INPUTS**
                
        [MessTransporter] *transporter* -- Transport channel to be used
        

        **OUTPUTS**

        STR *pkd_mess* -- The packed message        

        .. [MessTransporter] file:///./messaging.MessTransporter.html"""

        #
        # Read the fixed length messages until we get one that starts with 1
        #
        pkd_message = ''
        last_chunk = 0
        while not (last_chunk == '1'):
            a_chunk = transporter.receive_string(self.chunk_len)
            pkd_message = pkd_message + a_chunk
            last_chunk = a_chunk[0]
            
        return pkd_message


    def pack_mess(self, mess):
        
        """Pack the message into a sequence of fixed length chunks.
        
        **INPUTS**
        
        STR *mess* -- The message as a raw string
        

        **OUTPUTS**
        
        *STR packed_mess* -- The packed message
        """

        packed_mess = ''
        while not mess == '':

            #
            # Make sure you leave room for the single character prefix
            #
            a_chunk = mess[:self.chunk_len-1]

            #
            # If this is last chunk in message, pad it with blanks to the
            # right
            #
            num_padding = (self.chunk_len - 1) - len(mess)
            for ii in range(num_padding):
                a_chunk = a_chunk + ' '

            #
            # Is this last chunk in the message?
            # 
            mess = mess[self.chunk_len-1:]
            prefix = (mess == '')
            a_chunk = "%s%s" % (prefix, a_chunk)
            
            packed_mess = packed_mess + a_chunk

        return packed_mess
            

    def unpack_mess(self, mess):
        
        """Unpacks a message encoded as a sequence of fixed length chunks.
        
        **INPUTS**
        
        *STR* mess -- The packed message
        

        **OUTPUTS**
        
        *STR unpacked_mess* -- The message unpacked to a raw string.
        """

#        print '-- unpack_mess: invoked with \'%s\'' % mess
        unpacked_mess = ''
        while mess != '':
            a_chunk = mess[:self.chunk_len]
#            print '-- unpack_mess: a_chunk=\'%s\'' % a_chunk
            unpacked_mess = unpacked_mess + a_chunk[1:]
            mess = mess[self.chunk_len:]
        return unpacked_mess


class MessEncoder(Object.Object):
    """Encoding scheme for messages.
    
    Used to go translates messages between the (name, {arg:val}) format
    and raw string format.
    
    Virtual class.
    
    **INSTANCE ATTRIBUTES**
    
    *none*-- 
    
    CLASS ATTRIBUTES**
    
    *none* -- 
    """
        
    def __init__(self, **args_super):
        self.deep_construct(MessEncoder, \
                            {}, \
                            args_super, \
                            {})



    def encode(self, mess_name, mess_argvals):
        """Encodes a message as a raw string
        
        **INPUTS**

        STR *mess_name* -- An identifier indicating what type of
        message this is.
        
        {STR: STR} *mess_argvals* -- Dictionnary giving the arguments of the 
         message in {argument:value} format
        

        **OUTPUTS**
        
        *STR str_mess* -- The message encoded as a string
        """

        debug.virtual('encode')


    def decode(self, str_mess):
        """Decodes a message to (name, {arg:val}) format.
      
        **INPUTS**
        
        *STR* str_mess -- The message in raw string format
        
        **OUTPUTS**
        
        *(STR, {STR: STR}) name_argvals_mess* -- First element is the
        message name, second element is message arguments in
        *(name, {arg:val})* format.  """

        debug.virtual('decode')


class MessEncoder_LenPrefArgs(Object.Object):
    """Encoding scheme for messages with length prefixed argument values.
    
    Used to go translates messages between the (name, {arg:val}) format
    and raw string format.
    
    The format of messages is assumed to be:

           mess_name arg_name1=arg_len1|arg_val1 ... arg_nameN=arg_lenN|arg_valN    
    
    **INSTANCE ATTRIBUTES**
    
    *none*-- 
    
    CLASS ATTRIBUTES**
    
    *none* -- 
    """
        
    def __init__(self, **args_super):
        self.deep_construct(MessEncoder_LenPrefArgs, \
                            {}, \
                            args_super, \
                            {})


    def encode(self, mess_name, mess_argvals):
        """Encodes a message as a raw string, with length prefixed argument values.

        See [MessEncoder_LenPrefArgs] for details of the encoded message.         
        **INPUTS**

        STR *mess_name* -- An identifier indicating what type of
        message this is.
        
        {STR: STR} *mess_argvals* -- Dictionnary describing the
         message in {argument:value} format
        
        **OUTPUTS**
        
        *STR str_mess* -- The message encoded as a string

        .. [MessEncoder_LenPrefArgs] file:///./messaging.MessEncoder_LenPrefArgs.html"""

#        print '-- encode: mess_name=\'%s\', mess_argvals=%s' % (mess_name, repr(mess_argvals))
        str_mess = mess_name + ' '
        for an_arg in mess_argvals.keys():
            an_arg_value = mess_argvals[an_arg]

            #
            # Make sure argument value is a string
            #
            try:
                dum = len(an_arg_value)
            except:
                an_arg_value = repr(an_arg_value)
                
#            print '-- encode: an_arg=%s, an_arg_value=%s' % (an_arg, an_arg_value)
            str_mess = '%s %s=%s|%s' % (str_mess, an_arg, len(an_arg_value), an_arg_value)
        return str_mess


    def decode(self, str_mess):
        """Decodes a message with lenght prefixed argument values.

        Decodes it to the format (name, {arg:val}).

        See [MessEncoder_LenPrefArgs] for details of the encoded message. 
        
        **INPUTS**
        
        *STR* str_mess -- The message in raw string format
        

        **OUTPUTS**
        
        *(STR, {STR: STR}) name_argvals* -- First element is the
        message name, second element is message arguments in
        *(name, {arg:val})* format.

        .. [MessEncoder_LenPrefArgs] file:///./messaging.MessEncoder_LenPrefArgs.html"""        
        
        argvals = {}
        orig_mess = str_mess

        #
        # Read the name of the message
        #
        a_match = re.match('\s*([^\s]*)\s+', str_mess)
        if not a_match:
            raise RuntimeError, "malformed VoiceCode message '%s'" % orig_mess
        
        mess_name = a_match.group(1)
        if a_match.end() <= len(str_mess):
            str_mess = str_mess[a_match.end():]
        else:
            str_mess = ''

        #
        # Read argument value pairs
        #
        while 1:

            #
            # Name of the argument and length of its value
            #
            a_match = re.match('\s*([^=]*)=([\d]+)', str_mess)
            if not a_match:
                #
                # No more arguments in the message. Make sure what's left is
                # just blanks
                #
                if not re.match('^\s*$', str_mess):
                    raise RuntimeError, "malformed VoiceCode message '%s'" % orig_mess
                #
                # If everything is ok, break out of the loop
                #
                break
                            
            arg_name = a_match.group(1)
            arg_len = int(a_match.group(2))
            if a_match.end() <= len(str_mess):
                str_mess = str_mess[a_match.end():]
            else:
                str_mess = ''

            #
            # Read the '|' separating the argument length from its value
            #
            str_mess = str_mess[1:]

            #
            # Read specified number of bytes for the argument value
            #
            arg_val = str_mess[:arg_len]
            str_mess = str_mess[arg_len:]
            argvals[arg_name] = arg_val

        return (mess_name, argvals)


class MessTransporter(Object.Object):
    """Used to send/receive strings on a connection.

    Virtual class.
    
    **INSTANCE ATTRIBUTES**
    
    *none*-- 
    
    CLASS ATTRIBUTES**
            
    *none* -- 
    """
    
    def __init__(self, **args_super):
        self.deep_construct(MessTransporter, \
                            {}, \
                            args_super, \
                            {})



    def send_string(self, a_string):
        """Sends a string on the connection.
        
        **INPUTS**
        
        *STR* a_string -- String to send
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        debug.virtual('send_string')

    def receive_string(self, num_bytes):
        """Receives a string on the connection.
        
        **INPUTS**
        
        INT *num_bytes* -- Number of bytes to receive.
        

        **OUTPUTS**
        
        STR *a_string* -- The received string
        """
        
        debug.virtual('receive_string')        




    def close(self):
        """Close the connection.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        debug.not_implemented('close')


class MessTransporter_Socket(MessTransporter):
    """Used to send/receive strings on a Socket connection.

    Virtual class.
    
    **INSTANCE ATTRIBUTES**
    
    *socket sock*-- The socket connection used to transport the bytes.
    
    CLASS ATTRIBUTES**
            
    *none* -- 
    """
    
    def __init__(self, sock, **args_super):
        self.deep_construct(MessTransporter_Socket, \
                            {'sock': sock}, \
                            args_super, \
                            {})



    def send_string(self, a_string):
        """Sends a string on the Socket connection.
        
        **INPUTS**
        
        *STR* a_string -- String to send
        

        **OUTPUTS**
        
        *none* -- 
        """

#        print '-- send_string: sending \'%s\''% a_string
        mess_len = len(a_string)
        totalsent = 0
        while totalsent < mess_len:
            sent = self.sock.send(a_string[totalsent:])
            if sent == 0:
                raise RuntimeError, "socket connection broken"
            totalsent = totalsent + sent

#        print '-- send_string: done'           
        

    def receive_string(self, num_bytes):
        """Receives a string on the Socket connection.
        
        **INPUTS**
        
        INT *num_bytes* -- Number of bytes to receive.
        

        **OUTPUTS**
        
        STR *a_string* -- The received string
        """

#        print '-- receive_string: started'
        a_string = ''
        while len(a_string) < num_bytes:
            chunk = self.sock.recv(num_bytes - len(a_string))
            if chunk == '':
                raise RuntimeError, "socket connection broken"
            a_string = a_string + chunk

#        print '-- receive_string: received \'%s\'' % a_string
        return a_string         



    def close(self):
        """Close the socket connection.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        self.sock.close()
