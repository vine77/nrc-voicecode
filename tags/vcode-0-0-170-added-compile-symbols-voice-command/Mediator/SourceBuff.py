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

"""Interface to a buffer being edited in the programming environment"""


import debug
from debug import trace
import re, string, sys

from Object import Object, OwnerObject


class SourceBuffCookie(OwnerObject):
    """abstract class which represents a restore-able SourceBuff state

    SourceBuffCookie itself is simply a dummy class which acts as a
    placeholder.  Its only purpose is to serve as ostensible return or 
    argument type for various pure virtual SourceBuff functions.  The
    actual return or argument type will be a subclass of
    SourceBuffCookie which will vary with SourceBuff subclass.

    **INSTANCE ATTRIBUTES**

    *None*

    **CLASS ATTRIBUTES**

    *None*
    """
    def __init__(self, **attrs):
        self.deep_construct(SourceBuffCookie, {}, attrs)

    def rename_buffer_cbk(self, new_buff_name):
        """callback which notifies us that the application
        has renamed the buffer corresponding to this cookie

        **INPUTS**

        *STR* new_buff_name -- new name of the buffer 

        **OUTPUTS**

        *none*
        """
        debug.virtual('SourceBuffCookie.rename_buffer_cbk')

class SourceBuff(OwnerObject):
    """Interface to a buffer being edited in the programming environment
   
    This abstract class defines interface for manipulating buffer containing
    source code in some programming language.
    
    **INSTANCE ATTRIBUTES**
    
    *STR buff_name=None* -- Unique name for the buffer.
    
    *AppState app* -- application object containing the buffer

    (STR, INT, INT, INT) *last_search* -- Remember the details of the
    last search or selection that was done with method *search_for* or
    with *Select Pseudocode*. This is so that if the user repeats the
    same search or selection, we don't end up returning the same
    occurence over and over.

    The first 3 entries of the tuple correspond to the value of
    *regexp*, *direction*,
    and *where*. The last entry correspond to the position where
    cursor was put after last search.

    INT *print_nlines* -- When printing content of buffer to STDOUT
    (*print_buff* methods), print this number of lines before and
    after current line.

    CLASS ATTRIBUTES**
    
    """
    
    def __init__(self, app, buff_name=None, **attrs):
        self.init_attrs({'last_search': None})
        self.deep_construct(SourceBuff,
                            {'app': app,
                             'buff_name': buff_name,
                             'print_nlines': 3},
                            attrs
                            )
        self.name_parent('app')        

    def name(self):
        """returns the name of the buffer
        
        **INPUTS**

        *none*
        
        **OUTPUTS**
        
        STR -- name of the buffer."""
        return self.buff_name
        
    def on_change(self, start, end, text, program_initiated):
        """method which should be called after the contents of a buffer
        is changed.  If the SourceBuff represents a buffer in an 
        external editor which does not support change notification, then 
        on_change may only be called for mediator-initiated changes 
        (including responses from the external editor to 
        mediator-initiated changes).

        **INPUTS**

        *INT* start -- start of the modified range

        *INT* end -- end of the modified range

        *STR* text -- the new text replacing this range

        *BOOL* program_initiated -- true if the change was initiated by
        the mediator

        **OUTPUTS**

        *none*
        """
        if program_initiated:
            debug.trace('SourceBuff.on_change', 
                '(%d, %d) "%s" in %s\n' % (start, end, text, self.name()))
        self.app.on_change(self.name(), start, end, text, program_initiated)

    def rename_buffer_cbk(self, new_buff_name):
        """AppState invokes this method when 
        AppState.rename_buffer_cbk is called to notify VoiceCode that 
        an existing text buffer has been renamed
        
        **INPUTS**

        STR *new_buff_name* -- new name of the buffer.
        
        **OUTPUTS**
        
        *none*
        
        ..[SourceBuff] file:///./SourceBuff.SourceBuff.html"""

        self.buff_name = new_buff_name

    def file_name(self):
        """Returns the name of the file being displayed in a buffer.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        STR *name* -- 
        """        
        debug.virtual('SourceBuff.file_name')

    def to_sync(self, item, what, exclude):
        """Determines if an item is to be synchronised
        
        **INPUTS**
        
        STR *item* -- Type of item to be synchronised. Valid entries
        are: 'buff_name', 'content', 'cur_pos', 'selection'

        [STR] *what=[]* -- List of items to be included in or excluded
        from the list of things to synchronize (depending on value of
        *exclude*. Valid entries are: 'buff_name', 'content',
        'cur_pos', 'selection'.  *exclude_what=1*, this should be
        interpreted as a list of items that don't need to be
        synchronised. If *exclude_what=0*, then it should be
        interpreted as a list of items that need to be syncrhonized.

        BOOL *exclude* -- If *true*, then *what* is a list of items to
        be excluded from syncrhonization. Otherwise, *what* is a list
        of itmes to be included in the synchronization.

        **OUTPUTS**
        
        *none* -- 
        """
        
        in_list = (item in what)
        if exclude:
            answer = not in_list
        else:
            answer = in_list
        return in_list


    def application(self):
        """returns the AppState object of the application
        containing this buffer.

        **INPUTS**        

        *none*

        **OUTPUTS**

        *AppState* -- application object containing the buffer
        """
        return self.app

    def drop_breadcrumb(self, pos=None):

        """Drops a breadcrumb -- see AppState.drop_breadcrumb

        NOTE: the breadcrumb stack is maintained at the AppState level,
        where both the position and the buffer are stored. 
        There are no separate buffer-by-buffer stacks.  Therefore, it
        would make no sense to define SourceBuff.pop_breadcrumb.
        SourceBuff.drop_breadcrumb is included only as a convenient
        shorthand for

          buff.application().drop_breadcrumb(buffname = buff.file_name(),
          pos = ...)
        
        *INT pos* is the position where to drop the crumb. *STR
         buffname* is the name of the source buffer.
        
        If *pos* not specified, drop breadcrumb at cursor position.
        """
        self.application.drop_breadcrumb(buffname = self.file_name(), pos = pos)


    def language_name(self):
        """Returns the name of the language a file is written in
        
        **INPUTS**        

        *none*

        **OUTPUTS**

        *STR* -- the name of the language
        """
        debug.virtual('SourceBuff.language_name')


    def is_language(self, lang):
        """Check if a source buffer is in a particular language.

        Outputs *true* if and only if *self* is displaying a file
        written in programming language *STR lang*.
        """
        return (self.language_name() == lang)


    def region_distance(self, region1_start, region1_end, region2_start, region2_end):
        """Computes the distance between two regions of text
        
        **INPUTS**
        
        *INT* region1_start -- start position of first region
        
        *INT* region1_end -- end position of first region
        
        *INT* region2_start -- start position of 2nd region
        
        *INT* region2_end -- end position of 2nd region
        

        **OUTPUTS**
        
        *INT* distance -- distance between the two regions of text
        """

        distance = min(abs(region1_start - region2_start), abs(region1_start - region2_end), abs(region1_end - region2_start), abs(region1_end - region2_end))
        return distance

    def cur_pos(self):
        """retrieves current position of cursor .  Note: the current
        position should coincide with either the start or end of the
        selection.  

        **INPUTS**

        *none*
        
        **OUTPUTS**

        *INT* pos -- offset into buffer of current cursor position
        """
        ps = self.get_pos_selection()
        debug.trace('SourceBuff.cur_pos', 'pos, selection = %s' % repr(ps))
        pos = ps[0]
        debug.trace('SourceBuff.cur_pos', 'pos = %s' % repr(pos))
        return pos

    def get_selection(self):
        """retrieves range of current selection
        
        Note: the current position should coincide with either the 
        start or end of the selection. 
        
        **INPUTS**
        
        *none*
        
        **OUTPUTS**
        
        *INT* (start, end)
        
        start is the offset into the buffer of the start of the current
        selection.  end is the offset into the buffer of the character 
        following the selection (this matches Python's slice convention).
        """
        ps = self.get_pos_selection()
        debug.trace('SourceBuff.get_selection', 'pos, selection = %s' % repr(ps))
        selection = ps[1]
        debug.trace('SourceBuff.get_selection', 'selection = %s' % repr(selection))
        return selection

    def get_pos_selection(self):
        """retrieves current position of cursor and the range of 
        current selection
        
        **INPUTS**
        
        *none*
        
        **OUTPUTS**
        
        *(INT, (INT, INT))* (pos, (start, end))
        
        pos is the offset into buffer of current cursor position
        start is the offset into the buffer of the start of the current
        selection.  end is the offset into the buffer of the character 
        following the selection (this matches Python's slice convention).
        """
        debug.virtual('SourceBuff.get_pos_selection')


    def bidirectional_selection(self):
        """does editor support selections with cursor at left?

        **INPUTS**

        *none*

        **OUTPUTS**
        
        *BOOL* -- true if editor allows setting the selection at the
        left end of the selection"""
        return self.app.bidirectional_selection()

    def goto_end_of_selection(self, end = 1):
        """moves cursor to one end of the selection, clearing the
        selection.

        **INPUTS**

        *INT* end -- left (0) or right (1) end of selection

        **OUTPUT**

        *none*
        """
        target = self.get_selection()[end]
        self.goto(target)

    def set_selection(self, range, cursor_at = 1):
        """sets range of current selection, and sets the position to 
        beginning or end of the selection.

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
        debug.virtual('SourceBuff.set_selection')

    def get_text(self, start = None, end = None):
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
        debug.virtual('SourceBuff.get_text')

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
        debug.virtual('SourceBuff.set_text')
        

    def contents(self):
        """retrieves entire contents of the buffer
    
        **INPUTS**

        *none*

        **OUTPUTS**

        *STR* contents 
        """
        return self.get_text()

    def distance_to_selection(self, start, *opt_end):
        """Computes the distance of a region to the current selection.
        
        **INPUTS**
        
        *INT* start -- start position of region
        
        *[INT]* *opt_end -- end position of region (optional)
        

        **OUTPUTS**
        
        *INT* -- the distance
        """
        if len(opt_end) > 0:
            end = opt_end[0]
        else:
            end = start
        # make sure start < end and start2 < end2
        if start > end:
            tmp = end
            end = start
            start = tmp            
        start2, end2 = self.get_selection()
        # make sure start2 < end2
        if start2 > end2:
            tmp = end2
            start2 = end2
            end2 = tmp        
        if start2 == None or end2 == None:
            start2 = self.cur_pos()
            end2 = start2
        return self.region_distance(start, end, start2, end2)
        
    def get_visible(self):
        """ get start and end offsets of the currently visible region of
        the buffer.  End is the offset of the first character not
        visible (matching Python's slice convention)

        **INPUTS**

        *none*

        **OUTPUTS**

        *INT* (start, end)
        """
        debug.virtual('SourceBuff.get_visible')

    def make_position_visible(self):
        """scroll buffer (if necessary) so that the current position
        is visible

        **INPUTS**

        **OUTPUTS**

        *none*
        """
        debug.virtual('SourceBuff.make_position_visible')
    
    def line_num_of(self, position = None):
        """
        Returns the line number for a particular cursor position
        
        **INPUTS**
        
        *INT* position -- The position.  (defaults to the current position)
        
        **OUTPUTS**
        
        *INT line_num* -- The line number of that position
        """
        
        debug.virtual('SourceBuff.line_num_of')


    def number_lines(self, astring, startnum=1):
        """Assign numbers to lines in a string.

        Used mainly for the purpose of doing a printout of the buffer
        content around the cursor (usually during regression testing).

        *STR astring* is the string in question.

        *INT startnum* is the number of the first line in *astring*
        
        Returns a list of pairs *[(INT, STR)]* where first entry is
        the line number and the second entry is the line."""

        #
        # Note: need to split using regexp self.buff.newline_regexp()
        #       but for now this will do.
        #

        regexp = re.compile(self.newline_regexp())
        lines = regexp.split(astring)
        result = []

        if (astring != ''):
            lineno = startnum                
            for aline in lines:
                result[len(result):] = [(lineno, aline)]
                lineno = lineno + 1
            
        return result



    def len(self):
        """return length of buffer in characters.

        **INPUTS**

        *none*

        **OUTPUTS**

        *INT* length 
        """
        debug.virtual('SourceBuff.len')

    def make_valid_range(self, range):
        """Makes sure a region is increasing and within the buffer's range.
        
        **INPUTS** 
        
        *(INT, INT)* range -- offsets of initial range
        
        **OUTPUTS**
        
        *(INT, INT)* -- increasing range within bounds
        """

#        print '-- SourceBuff.make_valid_range: range=%s' % repr(range)
        
        start, end = range        
        if start == None: start = 0
# DCF: ugh, another one of these errors:
#          the end is after index self.len() -1 so at index self.len()
#        if end == None: end = self.len() - 1
        if end == None: end = self.len()
        if end < start:
            tmp = end
            end = start
            start = tmp
        start = self.make_within_range(start)
        end = self.make_within_range(end)
        return start, end
  
    def make_within_range(self, position):
        """Makes sure a position is within the buffer's range.
        
        **INPUTS**
        
        *INT* position -- The position. If outside of bounds, bring it back
        to the first or last position of the buffer.
        

        **OUTPUTS**
        
        *INT* position -- The possibly corrected position
        """

        length = self.len()
        if position < 0:
            position = 0
# cursor can be after last character in the buffer
        elif position > length and length > 0:
            position = length
        return position


    def beginning_of_line(self, pos):
        """Returns the position of the beginning of line at position *pos*
        
        **INPUTS**
        
        *INT* pos -- Position for which we want to know the beginning of line.
        

        **OUTPUTS**
        
        *INT* beg_pos -- Position of the beginning of the line
        """
        debug.virtual('SourceBuff.beginning_of_line')


    def end_of_line(self, pos):
        """Returns the position of the end of line at position *pos*
        
        **INPUTS**
        
        *INT* pos -- Position for which we want to know the end of line.
        

        **OUTPUTS**
        
        *INT* end_pos -- Position of the end of the line
        """
        debug.virtual('SourceBuff.end_of_line')
        
        
    def move_relative(self, rel_movement):
        """Move cursor to plus or minus a certain number of characters
        
        **INPUTS** 
        
        *INT rel_movement* -- number of characters to move, relative to 
        current position.  If < 0 then move to the left. Otherwise, move to the
        right.

        **OUTPUTS**

        *none*
        """
        pos = self.cur_pos()+rel_movement
        self.goto(pos)

    def move_relative_line(self, direction=1, num=1):
        """Moves up or down a certain number of lines
        
        **INPUTS**
        
        *INT* direction=1 -- If positive, line down. If negative, line up.
        
        *INT* num=1 -- Number of pages to move.
        

        **OUTPUTS**
        
        *none* -- 
        """

        #
        # Note: if moving downwards, put cursor after \n. Otherwise, put it
        # before.
        #
        self.search_for(regexp='(^|$|\n)', direction=direction,
                        where=direction, num=num)


    def move_relative_page(self, direction=1, num=1):
        """Moves up or down a certain number of pages
        
        **INPUTS**
        
        *INT* direction=1 -- If positive, page down. If negative, page up.
        
        *INT* num=1 -- Number of pages to move.
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        debug.virtual('SourceBuff.move_relative_page')

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

        #
        # Tabs in the code to insert are only useful when using
        # server-side indentation. This version of insert_indent()
        # is meant for client-side indentation, so remove them
        #
        code_bef = re.sub('\t', '', code_bef)        
        code_after = re.sub('\t', '', code_after)      


        trace('SourceBuff.insert_indent',
              '... code_bef=%s, code_after=%s, range=%s' % (code_bef, code_after, range))
        if range == None:
            range = self.get_selection()
            trace('SourceBuff.insert_indent',
                'got selection ... range=%s' % repr(range))
        range = self.make_valid_range(range)          

        trace('SourceBuff.insert_indent', '** inserting code_bef')    
        indent_from = range[0]
        self.insert(code_bef, range)
    
        trace('SourceBuff.insert_indent', '** indenting code_bef')        
        self.indent((indent_from, self.cur_pos()))        
        final_cur_pos = self.cur_pos()
        if code_after != '':
            trace('SourceBuff.insert_indent', '** inserting code_after')
            self.insert(code_after, (self.cur_pos(), self.cur_pos()))
            trace('SourceBuff.insert_indent', '** indenting code_after')
            self.indent((final_cur_pos, self.cur_pos()))
            self.goto(final_cur_pos)


    def insert(self, text, range = None):
        """Replace text in range with 
        with text

        **INPUTS**

        *STR text* -- new text

        *(INT, INT)* range -- code range to be replaced.  If None,
        defaults to the current selection.

        **OUTPUTS**

        *none*
        """

        debug.virtual('SourceBuff.insert')

    def indent(self, range = None):
        
        """Automatically indent the code in a source buffer region. Indentation
        of each line is determined automatically based on the line's context.

        **INPUTS**

        *(INT, INT)* range -- code range to be replaced.  If None,
        defaults to the current selection.

        **OUTPUTS**

        *none*
        """

        debug.virtual('SourceBuff.indent')


    def incr_indent_level(self, levels=1, range=None):
        
        """Increase the indentation of a region of code by a certain
        number of levels.
        
        **INPUTS**
        
        *INT* levels=1 -- Number of levels to indent by.
        
        *(INT, INT)* range=None -- Region of code to be indented 
        

        **OUTPUTS**
        
        *none* -- 
        """

        debug.virtual('SourceBuff.incr_indent_level')

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

        debug.virtual('SourceBuff.decr_indent_level')


    def delete(self, range = None):
        """Delete text in a source buffer range.

        **INPUTS**

        *(INT, INT)* range -- code range to be deleted.  If None,
        defaults to the current selection.

        **OUTPUTS**

        *none*
        """
        debug.virtual('SourceBuff.delete')
        
    def backspace(self, n_times):
        """Delete a number of spaces before the cursor.
        
        **INPUTS**
        
        INT *n_times* -- number of characters to delete.
        
        **OUTPUTS**
        
        *none*
        """
        self.delete((self.cur_pos() - n_times, self.cur_pos()))
        
    def goto(self, pos):

        """Moves the cursor to position *INT pos* of source buffer
        (and make selection empty)
        """
        
        debug.virtual('SourceBuff.goto')

    def goto_line(self, linenum, where=-1):
        """Go to a particular line in a buffer.

        *INT linenum* is the line number.

        *INT where* indicates if the cursor should go at the end
         (*where > 0*) or at the beginning (*where < 0*) of the line.
        """
        debug.virtual('SourceBuff.goto_line')

                
    def print_buff_if_necessary(self):
        """Prints content of current buffer if necessary.

        This method serves two purposes:

        - When regression testing an external editor, it is used to display
        the content of the buffer of the external editor whenever it has
        changed

        - When using the EdSim line-based editor, it refreshes the printout
        of the current content after each change."""

        if self.app.print_buff_when_changed:
            self.print_buff()
        

    def refresh(self):
        """Force a refresh of the buffer"""
        debug.virtual('SourceBuff.refresh')

    def _state_cookie_class(self):
        """returns the class object for the type of cookie used by
        store_current_state.

        **INPUTS**

        *none*

        **OUTPUTS**

        *CLASS* -- class of state cookies corresponding to this
        SourceBuff

        """
        debug.virtual('SourceBuff._state_cookie_class')
        
    def store_current_state(self):
        """stores the current state of the buffer, including both the
        contents and the current selection, for subsequent restoration.
        Store_current_state returns a "cookie" which can be passed to
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

        This method does not synchronize with the editor prior to
        storing the state.  The caller is responsible for synchronizing 
        if desired.  (This avoids having duplicate synchronize calls 
        when storing the current state of more than one buffer).

        **INPUTS**

        *none*

        **OUTPUTS**

        *SourceBuffCookie* -- state cookie (see above).  Note that
        SourceBuffCookie is a dummy class.  The
        actual return type will vary with SourceBuff subclass.
        """
        debug.virtual('SourceBuff.store_current_state')

    def restore_state(self, cookie):
        """restores the buffer to its state at the time when
        the cookie was returned by store_current_state.  Both the
        contents and the selection will be restored.  However, other
        data, such as the search history, may not.  The restore
        operation can fail, which will be indicated by a return value of
        0, so the caller should always check the return value.
        
        **INPUTS**

        *SourceBuffCookie cookie* -- see above.  Note that
        SourceBuffCookie is a dummy type, not an actual class.  The
        actual type will vary with SourceBuff subclass.

        **OUTPUTS**

        *BOOL* -- true if restore was successful

        """
        debug.virtual('SourceBuff.restore_state')

    def compare_states(self, first_cookie, second_cookie, selection = 0):
        """compares the buffer states at the times when
        two cookies were returned by store_current_state.  By default,
        only the buffer contents are compared, not the selection, unless
        selection == 1.  If the state corresponding to either cookie has
        been lost, compare_states will return false.

        This method does not synchronize with the editor prior to
        comparing with "current".  To ensure that the "current" state 
        is really current, the caller must synchronize.
        (This avoids having duplicate synchronize calls 
        when comparing with the current state of more than one buffer).

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
        debug.virtual('SourceBuff.compare_states')


    def compare_with_current(self, cookie, selection = 0):
        """compares the current buffer state to its state at the time when
        the cookie was returned by store_current_state.  By default,
        only the buffer contents are compared, not the selection, unless
        selection == 1.  If the state corresponding to the cookie has
        been lost, compare_with_current will return false.

        **INPUTS**

        *SourceBuffCookie cookie* -- see store_current_state.  Note that
        SourceBuffCookie is a dummy type, not an actual class.  The
        actual type will vary with SourceBuff subclass.

        *BOOL* selection -- compare selection as well as contents

        **OUTPUTS**

        *BOOL* -- true if state is the same, false if it is not, or
        it cannot be determined due to expiration of the cookie
        """
        debug.virtual('SourceBuff.compare_with_current')


    def valid_cookie(self, cookie):
        """checks whether a state cookie is valid or expired.
        If the state corresponding to the cookie has
        been lost, valid_cookie will return false.

        **INPUTS**

        *SourceBuffCookie cookie* -- see store_current_state.  Note that
        SourceBuffCookie is a dummy type, not an actual class.  The
        actual type will vary with SourceBuff subclass.

        **OUTPUTS**

        *BOOL* -- true if cookie is valid (i.e. restore_state should be
        able to work)
        """
        debug.virtual('SourceBuff.valid_cookie')


    def newline_conventions(self):
        
        """Returns a list of the forms of newline the editor can
        recognise for this buffer.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        debug.virtual('SourceBuff.newline_conventions')



    def pref_newline_convention(self):
        """Returns the form of newline that the editor prefers for this buffer.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        debug.virtual('SourceBuff.pref_newline_convention')


    def newline_regexp(self):
        
        """Returns a regexp that matches all the forms of newline that
        the editor can recognise in this buffer.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        #
        # We use (?: form so that the order of groups on the original
        # regexp is not screwed up.
        #
        regexp = '(?:'
        first_one = 1

        for a_nl_form in self.newline_conventions():
            if not first_one:
                regexp = regexp + '|'
            regexp = regexp + a_nl_form
            first_one = 1                
        regexp = regexp + ')'

        return regexp


    def search_for(self, regexp, direction=1, num=1, where=1, 
        unlogged = 0):
        
        """Moves cursor to the next occurence of regular expression
           *STR regexp* in buffer.

           *INT* direction -- if positive, search forward, otherwise
            search backward

           *INT* num -- number of occurences to search for

           *INT* where -- if positive, move cursor after the occurence,
           otherwise move it before

           *BOOL* unlogged -- if true, don't log the results of this
           search (used for searches done by mediator without user-initiation)

           Returns *None* if no occurence was found. Otherwise,
           returns a match object."""

        trace('SourceBuff.search_for', 
              "regexp='%s', direction=%s, num=%s, where=%s, unlogged=%s" %
               (regexp, direction, num, where, unlogged))
        success = None

        #
        # Change the \n in the regexp so they match any of the forms
        # recognised by the editor in this buffer
        #
        re.sub('\n', self.newline_regexp(), regexp)

        
        #
        # Find position of all matches
        #
        reobject = re.compile(regexp)        
        pos = 0; all_matches_pos = []
        while 1:
           a_match = reobject.search(self.get_text(), pos)
           if a_match and pos < len(self.get_text()):
# this allows for overlapping matches - ugh
#               pos = a_match.start() + 1
               pos = a_match.end()
# if we get a zero length match (e.g. '$' matching end of line, then we
# will continue to get the same match unless we advance the position
               if a_match.start() == a_match.end():
                 pos = pos + 1
               all_matches_pos = all_matches_pos + [(a_match.start(), a_match.end())]               
           else:
               break


        #
        # Look in the list of matches for the num'th match closest to
        # the cursor in the right direction
        #
        closest_match = self.closest_occurence_to_cursor(all_matches_pos,
                                                         regexp=regexp,
                                                         direction=direction,
                                                         where=where)

        new_cur_pos = None
        the_match_index = None        
        if closest_match != None:
            if direction > 0:
                the_match_index = closest_match + num - 1
                if the_match_index >= len(all_matches_pos):
                    the_match_index = len(all_matches_pos) - 1
            else:
                the_match_index = closest_match - num + 1
                if the_match_index < 0:
                    the_match_index = 0

            new_cur_pos = self.pos_extremity(all_matches_pos[the_match_index], where)


        #
        # Log the search so we don't keep bringing back same occurence
        # if the user repeats the same search.
        #
        if not unlogged:
            the_match = None
            if the_match_index != None: the_match = all_matches_pos[the_match_index]
            self.log_search (regexp, direction, where, the_match)
        
        if new_cur_pos != None:
            self.goto(new_cur_pos)
            success = 1
        else:
            success = 0
            
        return success


    def closest_occurence_to_cursor(self, occurences, direction=None, regexp=None, where=1):
        
        """Determines which occurence of a search pattern (or a
        *Select Pseudocode* pattern) is closest to the current cursor
        location.

        If the closest occurence is the one that was previously found for the
        same search or *Select Pseudocode* operation, take next closest one.

        **INPUTS**

        *(INT, INT)* occurences -- List of occurences (start and end positions).
        Assumed that they are sorted in increasing order of their start
        position.

        *INT* direction -- If negative, only consider occurences that are before
        the cursor. If positive, only consider occurences that are past the
        cursor. If *None*, consider all occurences whether before or after cursor.

        *STR* regexp -- The regular expression used to generate the
         list of occurences.
         

        **OUTPUTS**
        
        *INT* closest_index -- Index in *occurences* of the closest
         occurence. If no such occurence, returns *None*"""
         
        trace('SourceBuff.closest_occurence_to_cursor', '** occurences=%s, direction=%s, regexp="%s", where=%s' % 
                                                        (repr(occurences), direction, regexp, where))

        closest_index = None
        
        #
        # Look in the list of occurences for the one closest to the cursor
        # in the right direction
        #
        shortest_distance = None
        trace('SourceBuff.closest_occurence_to_cursor', '** cur_pos=%s' % self.cur_pos())
        for ii in range(len(occurences)):
            trace('SourceBuff.closest_occurence_to_cursor', '** ii=%s, occurences[ii]=%s' % (ii, repr(occurences[ii])))

            if direction == None:
                #
                # Don't care if closest occurence is before or after cursor
                #
                distance = self.region_distance(occurences[ii][0], occurences[ii][1], self.cur_pos(), self.cur_pos())
                trace('SourceBuff.closest_occurence_to_cursor', '** distance=%s, shortest_distance=%s' % (distance, shortest_distance))
                if ((shortest_distance == None or distance < shortest_distance)
                    and not self.same_as_previous_search(regexp, direction,
                                                         where, occurences[ii])):
                    shortest_distance = distance
                    closest_index = ii
                trace('SourceBuff.closest_occurence_to_cursor', '** closest_index=%s' % closest_index)
            elif direction < 0:
                #
                # Looking for closest occurence before cursor ...
                #
#                if occurences[ii][0] >= self.cur_pos():
# make sure the entire match is before the cursor
                if occurences[ii][1] > self.cur_pos():
                    #
                    # ... but we have passed cursor.
                    #
                    break
                else:
                    #
                    # ... and we haven't passed the cursor. So this is
                    # closest occurence before cursor yet.
                    #
                    if not self.same_as_previous_search(regexp, direction,
                                                   where, occurences[ii]):
                        closest_index = ii
            else:
                #
                # Looking for closest occurence after cursor ...
                #                
                if occurences[ii][0] >= self.cur_pos():
                    #
                    # ... and we have just passed cursor. So this
                    # is the closest occurence after cursor
                    #
                    if not self.same_as_previous_search(regexp, direction,
                                                   where, occurences[ii]):
                        closest_index = ii
                        break

        trace('SourceBuff.closest_occurence_to_cursor', '** returning closest_index=%s' % closest_index)
        return closest_index

    def same_as_previous_search(self, regexp, direction, where, match):
        
        """Determines whether a particular match found by *search_for* is the
        same as the one found by its last invocation.
        
        **INPUTS**
        
        *STR* regexp -- The regexp for current [search_for]. If
         *None*, then we are not currently doint a [search_for]
         operation.
        
        *INT* direction -- Direction of the search 
        
        *INT* where -- Put cursor at end or start of occurence
                
        *(INT, INT)* match -- Star and end position of the match
        

        **OUTPUTS**
        
        *BOOL* -- true if this is the same match as last invocation of
        *search_for*

        ..[search_for] file:///./SourceBuff.SourceBuff.html#search_for"""


        #
        # We consider this to be the same occurence as last search iif:
        #
        # a. Start/end position of both occurences are the same
        # b. Both occurences were found using same *regexp*
        # c. Both occurences were found using same *where*
        # d. Cursor hasn't moved since last search.
        #
        # Condition d. is because if the user moves the cursor to an other
        # location and redoes the same search again, he/she probably means
        # to do a new search starting from this new cursor location.
        #
        # Note that two occurences may be deemed identical even if they were
        # found using different *direction*. This is because if the user does
        # a search forward and then reverses the direction, we don't want
        # to go back to the occurence found in the forward direction (instead
        # we want to go directly to the one preceding).
        #
        # On the other hand, two occurences will be deemed identical only if
        # they were found using same *where* (condition c.). This is so you can
        # search for an occurence and then move the cursor to the beginning/end
        # of that occurence using a command like: "before that" or "after that"
        #
        answer = 0
        if (self.last_search != None and
            match == self.last_search[3] and            
            regexp == self.last_search[0] and
            where == self.last_search[2] and
            self.cur_pos() == self.pos_extremity(self.last_search[3], self.last_search[2])):
                answer = 1

        return answer
          
    def pos_extremity(self, range, where):
        """Returns the position of a given extremity of a range

        **INPUTS**

        *(INT, INT) range* -- Start and end position of the range

        *INT where* -- If positive, return position of end of
         range. Otherwise, return start position.

        **OUTPUTS**

        *INT* -- The approriate position
        """
        if where > 0:
            answer = range[1]
        else:
            answer = range[0]
        return answer

    def log_search(self, regexp, direction, where, match):
        """Logs the result of most recent search or selection operation, so
        that we know not to return the same match if the user repeats it
        
        **INPUTS**
        
        *STR* regexp -- Regular expreesion used for the search.
        
        *BOOL* direction -- If negative, then we were looking
         backwards. Forward if positive. If *None*, then we were doing
         a *Select Pseudocode* operation and we didn't care about
         direction.
        
        *INT* where -- If positive, then we wanted to put cursor after
         occurence. Before occurence if negative.
        
        *(INT, INT)* match -- Start and end position of the match that was
        used.
        

        **OUTPUTS**
        
        *none* --
        """
        self.last_search = (regexp, direction, where, match)

    #
    # Callback methods. These are invoked by the external editor to notify
    # VoiceCode that certain events have taken place in the editor.
    #
    def delete_cbk(self, range):
        """External editor invokes that callback to notify VoiceCode
        of a deletion event.

        NOTE: This method should NOT update the V-E map, because that is
        already taken care of outside of the method.
        
        **INPUTS**
        
        (INT, INT) *range* -- Start and end pos of range to be deleted
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        self.on_change(range[0], range[1], "", 0)

    def insert_cbk(self, range, text):
        
        """External editor invokes that callback to notify VoiceCode
        of a deletion event.

        NOTE: This method should NOT update the V-E map, because that is
        already taken care of outside of the method.
        
        **INPUTS**
        
        (INT, INT) *range* -- Start and end position of text to be
        replaced by the insertion.

        STR *text* -- Text to be inserted

        **OUTPUTS**
        
        *none* -- 
        """
        
        trace('SourceBuff.isnert_cbk.insert_cbk', 'range=%s, text=\'%s\'' % (range, text))
        self.on_change(range[0], range[1], text, 0)

    def pos_selection_cbk(self, pos, selection):
        """External editor invokes that callback to notify VoiceCode
        of a change in the current position or selection

        **INPUTS**
        
        INT *pos* -- Position the cursor was moved to.

        (INT, INT) *selection* -- Start and end position of selected text
        
        **OUTPUTS**
        
        *none* -- 
        """
        pass

    def print_buff(self, from_line=None, to_line=None):
        """Prints buffer to STDOUT.

        This is mostly used when running regression test on an
        external editor (or the EdSim simulation editor).
        
        **INPUTS**
        
        *INT* from_line = None -- First line to be printed. If *None*, then
        print *print_nlines* lines around cursor.

        *INT* to_line = None -- Last line to be printed.

        **OUTPUTS**
        
        *none* -- 
        """

        #
        # Figure out the first and last line to be printed
        #
        if from_line == None or to_line == None:
           from_line, to_line = self.lines_around_cursor()
           trace('SourceBuff.print_buff', '** now, from_line=%s, to_line=%s' % (from_line, to_line))           
        
        #
        # Figure out the text before/withing/after the selection
        #
        selection_start, selection_end = self.get_selection()

        trace('SourceBuff.print_buff', 'from_line=%s, to_line=%s, selection_start=%s, selection_end=%s' % (from_line, to_line, selection_start, selection_end))

        before_content = self.get_text(0, selection_start)
        selection_content = self.get_text(selection_start, selection_end)
        after_content = self.get_text(selection_end)

        printed = before_content
        if selection_content == '':
            printed = printed + '<CURSOR>'
        else:
            printed = printed + '<SEL_START>'
            printed = printed + selection_content
            printed = printed + '<SEL_END>'
        printed = printed + after_content

        trace('SourceBuff.print_buff', 'printed="%s"' % printed)

        lines_with_num = self.number_lines(printed, startnum = 1)
        
        if from_line == 1:
            sys.stdout.write("*** Start of source buffer ***\n")
        for aline in lines_with_num[from_line-1:to_line]:
            sys.stdout.write('%3i: %s\n' % (aline[0], aline[1]))
        if to_line == len(lines_with_num):
            sys.stdout.write("\n*** End of source buffer ***\n")
        return

    def lines_around_cursor(self):
        """Returns the line numbers of lines around cursor
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *(INT from_line, INT to_line)*

        *INT from_line* -- First line of the window.

        *INT to_line* -- Last line of the window.
        """

        curr_line = self.line_num_of(self.cur_pos())
        from_line = curr_line - self.print_nlines
        to_line = curr_line + self.print_nlines
        trace('SourceBuff.lines_around_cursor', '** curr_line=%s, self.cur_pos()=%s, self.print_nlines=%s, from_line=%s, to_line=%s' 
                                                % (curr_line, self.cur_pos(), self.print_nlines, from_line, to_line))                
        if from_line < 1:
            from_line = 1
        last_line = self.line_num_of(self.len())    
        trace('SourceBuff.lines_around_cursor', '** self.len()=%s, last_line=%s' % (self.len(), last_line))
        if to_line > last_line:
            to_line = last_line    
        return from_line, to_line


    def __getitem__(self, key):
        """Get a character of the buffer using the buff[i] syntax.
        
        **INPUTS**
        
        *INT* key -- The index of the character to return
        
        **OUTPUTS**
        
        *CHAR* -- the character at position *key*
        """
        return self.content()[key]

    def __setitem__(self, key, value):
        """Set a character of the buffer using the buff[i] syntax.
        
        **INPUTS**
        
        *INT* key -- The index of the character to return

        *STR* value -- The string to insert at position *key*

        **OUTPUTS**
        
        *none* -- 
        """
        self.insert(value, (key, key))

    def __getslice__(self, start, end):
        """Returns a slice of the buffer using the buff[start:end] syntax.
        
        **INPUTS**
        
        *INT* start, end -- The start and end indices of the slice

        **OUTPUTS**
        
        *STR* -- the slice from *start* to *end*
        """
        return self.content()[start:end]

    def __getslice__(self, start, end, value):
        """Sets slice of the buffer using the buff[start:end] = value syntax.
        
        **INPUTS**
        
        *INT* start, end -- The start and end indices of the slice to be set

        *STR* value -- The string to be inserted in place of the slice.

        **OUTPUTS**
        
        """
        self.insert(value, (start,end))


