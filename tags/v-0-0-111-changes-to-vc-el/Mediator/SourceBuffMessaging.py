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

class SourceBuffMessaging(SourceBuffCached.SourceBuffCached):
    
    """Class representing a source buffer connected to VoiceCode via a
    messaging protocol.

    This abstract class defines interface for manipulating buffer containing
    source code in some programming language.
    
    **INSTANCE ATTRIBUTES**


    No new instance attributes.
    
    Note however that the *app* attribute (defined in [SourceBuff])
    needs to be a subclass of [AppStateMessaging]

    **CLASS ATTRIBUTES**
    
    *none* --

    ..[SourceBuff] file:///./SourceBuff.SourceBuff.py
    ..[AppStateMessaging] file:///./AppStateMessaging.AppStateMessaging.html"""
    
    def __init__(self, **attrs):
        self.init_attrs({})        
        self.deep_construct(SourceBuffMessaging,
                            {},
                            attrs
                            )

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
