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

"""Use this interface if the link between VoiceCode and the external
buffer is slow"""


import debug

from Object import Object

class SourceBuffCached(SourceBuff.SourceBuff):
    
    """Interface optimised for editors that communicate with VoiceCode
    through a slow link.

    In order to minimise communication between VoiceCode and the
    editor, *SourceBuffCached* keeps a local copy of the state of the
    buffer. This avoids having to query the editor for the same
    information all the time.

    Methods in *SourceBuffCached* assume that:

    - The cached information will be synchronised with the editor's
      state at the beginning of every utterance.

    - *SourceBuffCached* methods that affect the state of the editor
      *directly* (that is, without going through an other [AppState]
      or [SourceBuff] method) will synchronize the cache before
      exiting.

    For any method *readingMethod* that reads the state of the
    external editor, *SourceBuffCached* implements two methods:

    *readingMethod* -- This is the public method (usually a method of
     [SourceBuff]) used to read the state. It usually just reads the
     value from *self.cache*
     
    *_readingMethod_from_app* -- This is a private method which reads
     the state directly from the external editor. Such methods are not
     expected to save the read state to cache (this will done by
     [synchronize_with_app] method).

    For any method *writingMethod* that changes the state of the
    external editor, *SourceBuffCached* implements two methods:

    *writingMethod* -- This is the public method. It does the change
     on the external editor (i.e. invoke *_writingMethod_from_app*)
     and then synchronises the cache with the external editor.

    *_writingMethod_from_app* -- This is a private method that just
     effects the change on the external editor, without synchronizing
     the cache.

    **INSTANCE ATTRIBUTES**

    {STR: STR} *cache* -- Key is the name of a cached information
    about the buffer, and value is the value of that information.

    CLASS ATTRIBUTES**
    
    *none* -- 

    ..[synchronize_with_app] file:///./AppStateCached.AppStateCached.html#synchronize
    ..[AppState] AppState.AppState.html
    ..[SourceBuff] SourceBuff.SourceBuff.html"""

    def __init__(self, **attrs):
        self.init_attrs({'cache': {}})        
        self.deep_construct(SourceBuffCached,
                            {},
                            attrs
                            )


    def apply_this_update(self, an_update):
        
        """Applies a single buffer update received from the external
        application.
        
        **INPUTS**
        
        [SB_Update] *an_update* -- The update to be applied.
        

        **OUTPUTS**
        
        *none* -- 

        ..[SB_Update] file:///./AppState.SB_Update.html"""
        
        ??? Large case statement based on the class of SB_Updates

    def language_name(self):
        """Returns the name of the language a file is written in
        
        **INPUTS**        

	*none*

        **OUTPUTS**

        *STR* -- the name of the language
        """
        return self.cache['language_name']

    def _language_name_from_app(self):
        """Returns the name of the language a file is written in
        
        **INPUTS**        

	*none*

        **OUTPUTS**

        *STR* -- the name of the language
        """
        debug.virtual('SourceBuffCached.language_name_from_app')


    def cur_pos(self):
	"""retrieves current position of cursor .  Note: the current
	position should coincide with either the start or end of the
	selection.  

	**INPUTS**

	*none*
	
	**OUTPUTS**

	*INT* pos -- offset into buffer of current cursor position
	"""

	return self.cache['cur_pos']

    def _cur_pos_from_app(self):
        
	"""retrieves current position of cursor directly from external
	application.

	**INPUTS**

	*none*
	
	**OUTPUTS**

	*INT* pos -- offset into buffer of current cursor position
	"""

	debug.virtual('SourceBuffCached._cur_pos_from_app')        

    def get_selection(self):
	"""retrieves range of current selection.  Note: the current
	position should coincide with either the start or end of the
	selection. 

	**INPUTS**

	*none*
	
	**OUTPUTS**

	*INT* (start, end)

	start is the offset into the buffer of the start of the current
	selection.  end is the offset into the buffer of the character 
	following the selection (this matches Python's slice convention).
	"""
	return self.cache['get_selection']
        

    def _get_selection_from_app(self):
	"""retrieves range of current selection directly from external editor.

	**INPUTS**

	*none*
	
	**OUTPUTS**

	*INT* (start, end)

	start is the offset into the buffer of the start of the current
	selection.  end is the offset into the buffer of the character 
	following the selection (this matches Python's slice convention).
	"""
        
	debug.virtual('SourceBuffCached._get_selection_from_app')	


    def set_selection(self, range, cursor_at = 1):
        
	"""sets range of current selection in external editor, then
	synchronises cache.

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
	self._set_selection_from_app(range, cursor_at)
        self.synchronize_with_app()

    def _set_selection_from_app(self, range, cursor_at = 1):
	"""sets range of current selection in external editor.

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
	debug.virtual('SourceBuffCached._set_selection_from_app')        


    def get_text(self, start = None, end = None):
	"""retrieves a portion of the buffer from the cache.

	**INPUTS**

	*INT start* is the start of the region returned.
	Defaults to start of buffer.

	*INT end* is the offset into the buffer of the character following 
	the region to be returned (this matches Python's slice convention).
	Defaults to end of buffer.

	**OUTPUTS**

	*STR* -- contents of specified range of the buffer
	"""

	return self.cache['get_text']


    def _get_text_from_app(self, start = None, end = None):
	"""retrieves a portion of the buffer directly from external editor.

	**INPUTS**

	*INT start* is the start of the region returned.
	Defaults to start of buffer.

	*INT end* is the offset into the buffer of the character following 
	the region to be returned (this matches Python's slice convention).
	Defaults to end of buffer.

	**OUTPUTS**

	*STR* -- contents of specified range of the buffer
	"""

	debug.virtual('SourceBuffCached._get_text_from_app')


    def get_visible(self):
	"""Gets start and end positions of visible region from cache.

	**INPUTS**

	*none*

	**OUTPUTS**

	*INT* (start, end)
	"""
	return self.cache['get_visible']

    def _get_visible_from_app(self):
        
	"""Gets start and end positions of visible region directly
	from external editor.

	**INPUTS**

	*none*

	**OUTPUTS**

	*INT* (start, end)
	"""
	debug.virtual('SourceBuff._get_visible_from_app')        

    def len(self):
	"""return length of buffer in characters from cache.

	**INPUTS**

	*none*

	**OUTPUTS**

	*INT* length 
	"""
	return len(self.cache['contents'])

    def insert_indent(self, code_bef, code_after, range = None):
        """Insert code into source buffer and indent it.

        Does it on external editor, then synchronizes cache.
        
        Replace code in range 
        with the concatenation of
        code *STR code_bef* and *str code_after*. Cursor is put right
        after code *STR bef*.

	**INPUTS**

	*STR* code_bef -- code to be inserted before new cursor location
        
	*STR* code_bef -- code to be inserted after new cursor location

	*(INT, INT)* range -- code range to be replaced.  If None,
	defaults to the current selection.

	**OUTPUTS**

	*none*
	"""
        
	self._insert_indent_from_app(code_bef, code_after, range)
        self.synchronize_with_app()

        
    def _insert_indent_from_app(self, code_bef, code_after, range = None):
        """Insert code into source buffer and indent it.

        Does it on external editor without synchronizing cache.
        
        Replace code in range 
        with the concatenation of
        code *STR code_bef* and *str code_after*. Cursor is put right
        after code *STR bef*.

	**INPUTS**

	*STR* code_bef -- code to be inserted before new cursor location
        
	*STR* code_bef -- code to be inserted after new cursor location

	*(INT, INT)* range -- code range to be replaced.  If None,
	defaults to the current selection.

	**OUTPUTS**

	*none*
	"""
        debug.virtual('SourceBuffCached._insert_indent_from_app')

    def insert(self, text, range = None):
        """Replace text in range with with text.

        Does it on external editor, then resynchronizes the cache.

	**INPUTS**

	*STR text* -- new text

	*(INT, INT)* range -- code range to be replaced.  If None,
	defaults to the current selection.

	**OUTPUTS**

	*none*
	"""

        self._insert_from_app(text, range)
        self.synchronize_with_app()        
        

    def _insert_from_app(self, text, range = None):
        """Replace text in range with with text.

        Does it on external editor, without resynchronizing the cache.

	**INPUTS**

	*STR text* -- new text

	*(INT, INT)* range -- code range to be replaced.  If None,
	defaults to the current selection.

	**OUTPUTS**

	*none*
	"""
        debug.virtual('SourceBuffCached._insert_from_app')


    def indent(self, range = None):
        
        """Automatically indent the code in a source buffer region.

        Does it on external editor without resynchronizing cache.

	**INPUTS**

	*(INT, INT)* range -- code range to be replaced.  If None,
	defaults to the current selection.

	**OUTPUTS**

	*none*
	"""
        self._indent_from_app(range)
        self.synchronize_with_app()


    def incr_indent_level(self, levels=1, range=None):
        
        """Increase the indentation of a region of code by a certain
        number of levels.

        Does it on editor and then resynchronizes cache.
        
        **INPUTS**
        
        *INT* levels=1 -- Number of levels to indent by.
        
        *(INT, INT)* range=None -- Region of code to be indented 
        

        **OUTPUTS**
        
        *none* -- 
        """

        self._incr_indent_level_from_app(levels, range)
        self.synchronize_with_app()


    def _incr_indent_level_from_app(self, levels, range):
        
        """Increase the indentation of a region of code by a certain
        number of levels.

        Does it on editor without resynchronizing cache.
        
        **INPUTS**
        
        *INT* levels=1 -- Number of levels to indent by.
        
        *(INT, INT)* range=None -- Region of code to be indented 
        

        **OUTPUTS**
        
        *none* -- 
        """

        debug.virtual('AppStateCached._incr_indent_level_from_app')


    def decr_indent_level(self, levels=1, range=None):

        """Decrease the indentation of a region of code by a certain number
        of levels.

        Does it to external editor, then resynchronises cache.
        
        **INPUTS**
        
        *STR* levels=1 -- Number of levels to unindent

        *(INT, INT)* range=None -- Start and end position of code to be indent.
        If *None*, use current selection

        **OUTPUTS**
        
        *none* -- 
        """

        print '-- SourceBuffCached.decr_indent_level: called'
        self._decr_indent_level_on_app(levels, range)


    def _decr_indent_level_from_app(self, levels, range):

        """Decrease the indentation of a region of code by a certain number
        of levels.

        Does it to external editor without resynchronizing cache.
        
        **INPUTS**
        
        *STR* levels=1 -- Number of levels to unindent

        *(INT, INT)* range=None -- Start and end position of code to be indent.
        If *None*, use current selection

        **OUTPUTS**
        
        *none* -- 
        """

        debug.virtual('SourceBuffCached._decr_indent_level_from_app')

    def delete(self, range = None):
        """Delete text in a source buffer range.

        Does it to external editor, then resynchronizes cache.

	**INPUTS**

	*(INT, INT)* range -- code range to be deleted.  If None,
	defaults to the current selection.

	**OUTPUTS**

	*none*
	"""
        self._delete_from_app(range)
        self.synchronize_with_app()
        


    def _delete_from_app(self, range):
        """Delete text in a source buffer range.

        Does it to external editor without resynchronizing cache.

	**INPUTS**

	*(INT, INT)* range -- code range to be deleted.  If None,
	defaults to the current selection.

	**OUTPUTS**

	*none*
	"""
        debug.virtual('SourceBuffCached._delete_from_app')

    def goto(self, pos):

        """Moves the cursor to position *INT pos* of source buffer
	(and make selection empty)
        """
        
        debug.virtual('SourceBuff.goto')

    def goto(self, pos):

        """Moves the cursor to position *INT pos* of source buffer
	(and make selection empty)

        Does that to the external editor, then resynchronizes cache.
        """
        
        self._goto_on_app(pos)
        self.synchronize_with_app()

    def _goto_on_app(self, pos):

        """Moves the cursor to position *INT pos* of source buffer
	(and make selection empty)

        Does that to the external editor without resynchronizing cache.
        """
        
        debug.virtual('SourceBuffCached.goto_on_app')

    def newline_conventions(self):
        
        """Returns a list of the forms of newline the editor can
        recognise for this buffer (read from cache).
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        return self.cache['newline_conventions']

    def _newline_conventions_from_app(self):
        
        """Returns a list of the forms of newline the editor can
        recognise for this buffer (read directly from editor).
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        debug.virtual('SourceBuffCached._newline_conventions_from_app')

    def pref_newline_convention(self):
        
        """Returns the form of newline that the editor prefers for
        this buffer (read from cache).
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        return self.cache['pref_newline_convention']

    def pref_newline_convention(self):
        
        """Returns the form of newline that the editor prefers for
        this buffer (read directly from editor).
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        debug.virtual('SourceBuffCached._pref_newline_convention_from_app')
