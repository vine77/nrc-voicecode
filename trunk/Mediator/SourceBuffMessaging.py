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

"""State information for an external source buffer connected to
VoiceCode via a messaging protocol."""

import messaging, SourceBuffCached
import sb_services
from debug import trace

class SourceBuffMessaging(SourceBuffCached.SourceBuffCached):
    
    """Class representing a source buffer connected to VoiceCode via a
    messaging protocol.

    This abstract class defines interface for manipulating buffer containing
    source code in some programming language.
    
    **INSTANCE ATTRIBUTES**

    [SB_ServiceFullState] *state_srv* -- Buffer state save/restore service. 
    (for basic correction -- subclasses can override these methods to
    provide more efficient state save/restore mechanism)
    
    Note however that the *app* attribute (defined in [SourceBuff])
    needs to be a subclass of [AppStateMessaging]

    **CLASS ATTRIBUTES**
    
    *none* --

    ..[SourceBuff] file:///./SourceBuff.SourceBuff.py
    ..[AppStateMessaging] file:///./AppStateMessaging.AppStateMessaging.html"""
    
    def __init__(self, **attrs):
        self.init_attrs({})        
        self.deep_construct(SourceBuffMessaging,
                            {'state_srv': 
                              sb_services.SB_ServiceFullState(buff=self)},
                            attrs
                            )
        self.add_owned('state_srv')


    def _state_cookie_class(self):
        """returns the class object for the type of cookie used by
	store_current_state.

	**INPUTS**

	*none*

	**OUTPUTS**

	*CLASS* -- class of state cookies corresponding to this
	SourceBuff

	"""
        return self.state_srv._state_cookie_class()
        
    def store_current_state(self):
        """stores the current state of the buffer, including both the
	contents and the current selection, for subsequent restoration.
	store_current_state returns a "cookie" which can be passed to
	restore_state or compare_with_current.  The type and attributes
	of the cookie will depend on the specific subclass of
	SourceBuff.  In the most straightforward implementation, it 
	may include a copy of the entire contents of the
	buffer and the selection.  In other cases, particularly when the
	editor or SourceBuff provides an internal undo stack, it may simply be a
	reference to a point in this stack.
	
	Important Notes:
	
        You should only pass the cookie to methods of
	the SAME SourceBuff object from which it came.  Generally,
	cookies can not be pickled and retrieved.

	The type of cookie will vary with the concrete subclass 
	of SourceBuff.  The corresponding class object is 
	returned by _state_cookie_class.  However, external callers
	should not depend on the type, attributes, or methods 
	of the cookie.

	**INPUTS**

	*none*

	**OUTPUTS**

	*SourceBuffState* -- state cookie (see above)
	"""
        return self.state_srv.store_current_state()

    def restore_state(self, cookie):
        """restores the buffer to its state at the time when
	the cookie was returned by store_current_state.  Both the
	contents and the selection will be restored.  However, other
	data, such as the search history, may not.  The restore
	operation can fail, which will be indicated by a return value of
	0, so the caller should always check the return value.
	
	**INPUTS**

	*SourceBuffState cookie* -- see above.

	**OUTPUTS**

	*BOOL* -- true if restore was successful

	"""
        return self.state_srv.restore_state(cookie)

    def compare_states(self, first_cookie, second_cookie, selection = 0):
        """compares the buffer states at the times when
	two cookies were returned by store_current_state.  By default,
	only the buffer contents are compared, not the selection, unless
	selection == 1.  If the state corresponding to either cookie has
	been lost, compare_states will return false.

	**INPUTS**

	*SourceBuffCookie* first_cookie, second_cookie -- see 
        store_current_state.  Note that SourceBuffCookie is a dummy 
        type, not an actual class.  The actual type will vary with 
        SourceBuff subclass.

	*BOOL* selection -- compare selection as well as contents

	**OUTPUTS**

	*BOOL* -- true if states are the same, false if they are not, or
	it cannot be determined due to expiration of either cookie
	"""
        return self.state_srv.compare_states(first_cookie,
            second_cookie, selection)

    def compare_with_current(self, cookie, selection = 0):
        """compares the current buffer state to its state at the time when
	the cookie was returned by store_current_state.  By default,
	only the buffer contents are compared, not the selection, unless
	selection == 1.  If the state corresponding to the cookie has
	been lost, compare_with_current will return false.

	**INPUTS**

	*SourceBuffState cookie* -- see store_current_state.

	*BOOL* selection -- compare selection as well as contents

	**OUTPUTS**

	*BOOL* -- true if state is the same, false if it is not, or
	it cannot be determined due to expiration of the cookie
	"""
        return self.state_srv.compare_with_current(cookie, selection)
        
    def valid_cookie(self, cookie):
        """checks whether a state cookie is valid or expired.
	If the state corresponding to the cookie has
	been lost, valid_cookie will return false.

	**INPUTS**

	*SourceBuffState cookie* -- see store_current_state. 

	**OUTPUTS**

	*BOOL* -- true if cookie is valid (i.e. restore_state should be
	able to work)
	"""
        return self.state_srv.valid_cookie(cookie)


    def _file_name_from_app(self):
        """Gets from the external editor, the name of the file being
        displayed in this buffer.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        STR *name* -- 
        """
        self.app.talk_msgr.send_mess('file_name', {'buff_name': self.buff_name})
        response = self.app.talk_msgr.get_mess(expect=['file_name_resp'])
        return response[1]['value']
        

    def _language_name_from_app(self):
        """Returns the name of the language a file is written in
        
        **INPUTS**        

	*none*

        **OUTPUTS**

        *STR* -- the name of the language
        """
        self.app.talk_msgr.send_mess('language_name',
            {'buff_name': self.name()})
        response = self.app.talk_msgr.get_mess(expect=['language_name_resp'])
        return response[1]['value']


    def _cur_pos_from_app(self):
        """retrieves current position of cursor from external editor.

	**INPUTS**

	*none*
	
	**OUTPUTS**

	*INT* pos -- offset into buffer of current cursor position
	"""

        self.app.talk_msgr.send_mess('cur_pos',
            {'buff_name': self.name()})
        response = self.app.talk_msgr.get_mess(expect=['cur_pos_resp'])
        return messaging.messarg2int(response[1]['value'])

    def _get_selection_from_app(self):
        """retrieves range of current selection from external editor.

	**INPUTS**

	*none*
	
	**OUTPUTS**

	*INT* (start, end)

	start is the offset into the buffer of the start of the current
	selection.  end is the offset into the buffer of the character 
	following the selection (this matches Python's slice convention).
	"""

        self.app.talk_msgr.send_mess('get_selection',
            {'buff_name': self.name()})
        response = self.app.talk_msgr.get_mess(expect=['get_selection_resp'])
        range = messaging.messarg2intlist(response[1]['value'])
        return range
        

    def set_selection(self, range, cursor_at = 1):
        """sets range of current selection, in the external editor.

        Also sets the position to beginning or end of the selection.

	**INPUTS**

	*(INT, INT)* range -- offsets into buffer of the start and end
	of the selection.  end is the offset into the buffer of the character 
	following the selection (this matches Python's slice convention).

	*INT* cursor_at -- indicates whether the cursor should be
	placed at the left (0) or right (1) end of the selection.  Note:
        cursor_at is ignored unless the application supports this
	choice, as indicated by bidirectional_selection.  
	Most Windows applications do not.

	**OUTPUTS**

	*none*
	"""

        #
        # Set the selection and get updates from the editor
        #
        trace('SourceBuffMessaging.set_selection', '** range=%s, cursor_at=%s' % (repr(range), cursor_at))
        args = {'range': range, 'cursor_at': cursor_at,
            'buff_name': self.name()}
        self.app.talk_msgr.send_mess('set_selection', args)
        response = self.app.talk_msgr.get_mess(expect=['set_selection_resp'])

        #
        # Apply the updates
        #
        self.app.update_response = 1
        self.app.apply_upd_descr(response[1]['updates'])
        self.app.update_response = 0

    def _get_text_from_app(self, start = None, end = None):
        """retrieves a portion of the buffer

	**INPUTS**

	*INT start* is the start of the region returned.
	Defaults to start of buffer.

	*INT end* is the offset into the buffer of the character following 
	the region to be returned (this matches Python's slice convention).
	Defaults to end of buffer.

	**OUTPUTS**

	*STR* -- contents of specified range of the buffer
	"""

#        print '-- SourceBuffMessaging._get_text_from_app: start=%s, end=%s' % (start, end)
        
        args = {'start': start, 'end': end,
            'buff_name': self.name()}
        self.app.talk_msgr.send_mess('get_text', args)
        response = self.app.talk_msgr.get_mess(expect=['get_text_resp'])
        
        return response[1]['value']
        
    def set_text(self, text, start = None, end = None):
        """changes a portion of the buffer

	**INPUTS**

	*STR text* is the new text.
	
	*INT start* is the offset into the buffer of the text to the
	replaced.  Defaults to start of buffer.

	*INT end* is the offset into the buffer of the character following 
	the text to be replaced (this matches Python's slice convention).
	Defaults to end of buffer.

	**OUTPUTS**

	*none*
	"""
        args = {'text': text, 'start': start, 'end': end,
            'buff_name': self.name()}
        self.app.talk_msgr.send_mess('set_text', args)
        response = self.app.talk_msgr.get_mess(expect=['set_text_resp'])
        
        self.app.update_response = 1
        self.app.apply_upd_descr(response[1]['updates'])
        self.app.update_response = 0

        

    def _get_visible_from_app(self):
        """ get start and end offsets of the currently visible region of
	the buffer.  End is the offset of the first character not
	visible (matching Python's slice convention)

	**INPUTS**

	*none*

	**OUTPUTS**

	*INT* (start, end)
	"""
        self.app.talk_msgr.send_mess('get_visible',
            {'buff_name': self.name()})
        response = self.app.talk_msgr.get_mess(expect=['get_visible_resp'])
        return messaging.messarg2intlist(response[1]['value'])        
        

    def make_position_visible(self):
        """scroll buffer (if necessary) so that the current position
	is visible

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""

        args = {'buff_name': self.name()}
        self.app.talk_msgr.send_mess('make_position_visible', args)
        response = self.app.talk_msgr.get_mess(expect=['make_position_visible_resp'])

#        self.app.update_response = 1
#        self.app.apply_upd_descr(response[1]['updates'])
#        self.app.update_response = 0
        
    def line_num_of(self, position = None):
        """
        Returns the line number for a particular cursor position
        
        **INPUTS**
        
        *INT* position -- The position.  (defaults to the current position)
        
        **OUTPUTS**
        
        *INT line_num* -- The line number of that position
        """
        
        args = {'position': position, 'buff_name': self.name()}
        self.app.talk_msgr.send_mess('line_num_of', args)
        response = self.app.talk_msgr.get_mess(expect=['line_num_of_resp'])

        return messaging.messarg2int(response[1]['value'])

    def _len_from_app(self):
        """return length of buffer in characters.

	**INPUTS**

	*none*

	**OUTPUTS**

	*INT* length 
	"""
        self.app.talk_msgr.send_mess('len', {'buff_name': self.name()})
        response = self.app.talk_msgr.get_mess(expect=['len_resp'])

        return messaging.messarg2int(response[1]['value'])
        

    def _newline_conventions_from_app(self):
        
        """Returns a list of the forms of newline the editor can
        recognise for this buffer (read directly from editor).
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        self.app.talk_msgr.send_mess('newline_conventions',
            {'buff_name': self.name()})
        response = self.app.talk_msgr.get_mess(expect=['newline_conventions_resp'])
        return response[1]['value']

    def _pref_newline_convention_from_app(self):
        
        """Returns the form of newline that the editor prefers for
        this buffer (read directly from editor).
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        self.app.talk_msgr.send_mess('pref_newline_convention',
            {'buff_name': self.name()})
        response = self.app.talk_msgr.get_mess(expect=['pref_newline_convention_resp'])
        return response[1]['value']

    def beginning_of_line(self, pos):
        """Returns the position of the beginning of line at position *pos*
        
        **INPUTS**
        
        *INT* pos -- Position for which we want to know the beginning of line.
        

        **OUTPUTS**
        
        *INT* beg_pos -- Position of the beginning of the line
        """
        args = {'pos': pos, 'buff_name': self.name()}
        self.app.talk_msgr.send_mess('beginning_of_line', args)
        response = \
            self.app.talk_msgr.get_mess(expect=['beginning_of_line_resp'])

        return messaging.messarg2int(response[1]['value'])
        


    def end_of_line(self, pos):
        """Returns the position of the end of line at position *pos*
        
        **INPUTS**
        
        *INT* pos -- Position for which we want to know the end of line.
        

        **OUTPUTS**
        
        *INT* end_pos -- Position of the end of the line
        """
        args = {'pos': pos, 'buff_name': self.name()}
        self.app.talk_msgr.send_mess('end_of_line', args)
        response = \
            self.app.talk_msgr.get_mess(expect=['end_of_line_resp'])

        return messaging.messarg2int(response[1]['value'])

    def move_relative_page(self, direction=1, num=1):
        """Moves up or down a certain number of pages
        
        **INPUTS**
        
        *INT* direction=1 -- If positive, page down. If negative, page up.
        
        *INT* num=1 -- Number of pages to move.
        

        **OUTPUTS**
        
        *none* -- 
        """
        args = {'direction': direction, 'num': num,
            'buff_name': self.name()}
        self.app.talk_msgr.send_mess('move_relative_page', args)
        response = self.app.talk_msgr.get_mess(expect=['move_relative_page_resp'])

        self.app.update_response = 1
        self.app.apply_upd_descr(response[1]['updates'])
        self.app.update_response = 0

    def indent(self, range = None):
        
        """Automatically indent the code in a source buffer region. Indentation
        of each line is determined automatically based on the line's context.

	**INPUTS**

	*(INT, INT)* range -- code range to be replaced.  If None,
	defaults to the current selection.

	**OUTPUTS**

	*none*
	"""
# by default, assume that the remote editor does indentation.
# Subclasses for particular editors which use mediator-based indentation 
# can always override this choice.
        args = {'range': range, 'buff_name': self.name()}
        self.app.talk_msgr.send_mess('indent', args)
        response = self.app.talk_msgr.get_mess(expect=['indent_resp'])        

        self.app.update_response = 1
        self.app.apply_upd_descr(response[1]['updates'])
        self.app.update_response = 0
        
    def incr_indent_level(self, levels=1, range=None):
        
        """Increase the indentation of a region of code by a certain
        number of levels.
        
        **INPUTS**
        
        *INT* levels=1 -- Number of levels to indent by.
        
        *(INT, INT)* range=None -- Region of code to be indented 
        

        **OUTPUTS**
        
        *none* -- 
        """
# by default, assume that the remote editor does indentation.
# Subclasses for particular editors which use mediator-based indentation 
# can always override this choice.
        args = {'levels': levels, 'range': range, 'buff_name': self.name()}
        self.app.talk_msgr.send_mess('incr_indent_level', args)
        response = self.app.talk_msgr.get_mess(expect=['incr_indent_level_resp'])        
        self.app.update_response = 1
        self.app.apply_upd_descr(response[1]['updates'])
        self.app.update_response = 0
        
    def decr_indent_level(self, levels=1, range=None):

        """Decrease the indentation of a region of code by a certain number
        of levels.
        
        **INPUTS**
        
        *STR* levels=1 -- Number of levels to unindent

        *(INT, INT)* range=None -- Start and end position of code to be indent.
        If *None*, use current selection

        **OUTPUTS**
        
        *none* -- 
        """

# by default, assume that the remote editor does indentation.
# Subclasses for particular editors which use mediator-based indentation 
# can always override this choice.
        args = {'levels': levels, 'range': range, 'buff_name': self.name()}
        self.app.talk_msgr.send_mess('decr_indent_level', args)
        response = self.app.talk_msgr.get_mess(expect=['decr_indent_level_resp'])        
        self.app.update_response = 1
        self.app.apply_upd_descr(response[1]['updates'])
        self.app.update_response = 0
        


    def insert(self, text, range = None):
        
        """Ask external editor to replace text in range with with text

	**INPUTS**

	*STR text* -- new text

	*(INT, INT)* range -- code range to be replaced.  If None,
	defaults to the current selection.

	**OUTPUTS**

	*none*
	"""

#        print '-- SourceBuffMessaging.insert: text=%s, range=%s' % (text, range)
        
        args = {'text': text, 'range': range,
            'buff_name': self.name()}
        self.app.talk_msgr.send_mess('insert', args)
        response = self.app.talk_msgr.get_mess(expect=['insert_resp'])        
        self.app.update_response = 1
        self.app.apply_upd_descr(response[1]['updates'])
        self.app.update_response = 0
        

    def delete(self, range = None):
        """Delete text in a source buffer range.

	**INPUTS**

	*(INT, INT)* range -- code range to be deleted.  If None,
	defaults to the current selection.

	**OUTPUTS**

	*none*
	"""
        
        #
        # Ask external editor to delete the region
        #
        args = {'range': range,
            'buff_name': self.name()}
        self.app.talk_msgr.send_mess('delete', args)
        response = self.app.talk_msgr.get_mess(expect=['delete_resp'])

        self.app.update_response = 1
        self.app.apply_upd_descr(response[1]['updates'])        
        self.app.update_response = 0
        
        
    def goto(self, pos):

        """Moves the cursor to position *INT pos* of source buffer
	(and make selection empty)
        """

        #
        # Ask external editor to delete the region
        #
        args = {'pos': pos,
            'buff_name': self.name()}
        self.app.talk_msgr.send_mess('goto', args)
        response = self.app.talk_msgr.get_mess(expect=['goto_resp'])

        self.app.update_response = 1
        self.app.apply_upd_descr(response[1]['updates'])
        self.app.update_response = 0
        
    def goto_line(self, linenum, where=-1):
        """Go to a particular line in a buffer.

        *INT linenum* is the line number.

        *INT where* indicates if the cursor should go at the end
         (*where > 0*) or at the beginning (*where < 0*) of the line.
        """
        args = {'linenum': linenum, 'where': where,
            'buff_name': self.name()}
        self.app.talk_msgr.send_mess('goto_line', args)
        response = self.app.talk_msgr.get_mess(expect=['goto_line_resp'])

        self.app.update_response = 1
        self.app.apply_upd_descr(response[1]['updates'])
        self.app.update_response = 0
      
class SourceBuffInsertIndentMess(SourceBuffMessaging):
    """subclass of SourceBuffMessaging which sends an insert_indent
    message to the external editor, instead of using the generic
    SourceBuff implementation of insert_indent in terms of insert and
    indent.

    **NOTE:** This class is used only for test editors.  Real editors 
    supporting client-side indentation should use SourceBuffMessaging.  
    Real editors not supporting client-side indentation should use 
    server-side indentation (see SB_MessExtEdSim in tcp_server.py 
    for an example).

    Its purpose is to work with clients with an incomplete implementation 
    of client-side indentation which won't work with the generic 
    AppState.insert_indent, because indent is implemented as a no-op.
    
    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**

    *none*
    """
    def __init__(self, **args):
        self.deep_construct(SourceBuffInsertIndentMess, {}, args)

    def insert_indent(self, code_bef, code_after, range = None):
        """Insert code into source buffer and indent it.

        Replace code in range 
        with the concatenation of
        code *STR code_bef* and *str code_after*. Cursor is put right
        after code *STR bef*.

	**INPUTS**

	*STR* code_bef -- code to be inserted before new cursor location
        
	*STR* code_after -- code to be inserted after new cursor location

	*(INT, INT)* range -- code range to be replaced.  If None,
	defaults to the current selection.

	**OUTPUTS**

	*none*
	"""
# by default, assume that the remote editor does indentation.
# Subclasses for particular editors which use mediator-based indentation 
# can always override this choice.
        args = {'code_bef': code_bef, 'code_after': code_after, 'range': range,
            'buff_name': self.name()}
        self.app.talk_msgr.send_mess('insert_indent', args)
        response = self.app.talk_msgr.get_mess(expect=['insert_indent_resp'])        
        self.app.update_response = 1
        self.app.apply_upd_descr(response[1]['updates'])
        self.app.update_response = 0
        
