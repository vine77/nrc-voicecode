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


import debug, SourceBuff

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
    external editor, *SourceBuffCached* should implement two methods:

    *readingMethod* -- This is the public method (usually a method of
     [SourceBuff]) used to read the state. It usually checks to see if
     the value is cached, and if so, it reads if from cache. If the
     value is not cached, it will retrieve it from the external
     application and cache it.
     
    *_readingMethod_from_app* -- This is a private method which reads
     the state directly from the external editor. Such methods are not
     expected to save the read state to cache (this will done by
     [synchronize_with_app] method).

    For any method *writingMethod* that changes the state of the
    external editor, *SourceBuffCached* assumes that subclasses will
    define *writingMethod* such that it invokes the change on the
    external editor AND make sure to synchronise the cache with the
    external editor.

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
        self.init_cache()


    def init_cache(self):
        """Initializes the cache from data acquired from external buffer.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

#        print '-- SourceBuffCached.init_cache: called'

        self.cache = {'file_name': None,
                      'language_name': None, 'cur_pos': None,
                      'get_selection': None, 'get_text': None,
                      'get_visible': None, 'newline_conventions': None,
                      'pref_newline_convention': None}


    def file_name(self):
        """Returns the name of the file being displayed in this buffer.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        STR *name* -- 
        """
        if self.cache['file_name'] == None:
            self.cache['file_name'] = self._file_name_from_app()
        return self.cache['file_name']
        

    def language_name(self):
        """Returns the name of the language a file is written in
        
        **INPUTS**        

	*none*

        **OUTPUTS**

        *STR* -- the name of the language
        """
        if self.cache['language_name'] == None:
            self.cache['language_name'] = self._language_name_from_app()
        return self.cache['language_name']

    def _language_name_from_app(self):
        """Returns the name of the language a file is written in
        
        **INPUTS**        

	*none*

        **OUTPUTS**

        *STR* -- the name of the language
        """
        debug.virtual('SourceBuffCached._language_name_from_app')

    def rename_buffer_cbk(self, new_buff_name):
        
        """AppState invokes this method when 
	AppState.rename_buffer_cbk is called to notify VoiceCode that 
	an existing text buffer has been renamed
        
        **INPUTS**

        STR *new_buff_name* -- new name of the buffer.
        
        **OUTPUTS**
        
        *none*
        
        ..[SourceBuff] file:///./SourceBuff.SourceBuff.html"""

	SourceBuff.rename_buff_cbk(new_buff_name)
        self.cache['language_name'] = None
        self.cache['file_name'] = None

    def cur_pos(self):
	"""retrieves current position of cursor .  Note: the current
	position should coincide with either the start or end of the
	selection.  

	**INPUTS**

	*none*
	
	**OUTPUTS**

	*INT* pos -- offset into buffer of current cursor position
	"""
        if self.cache['cur_pos'] == None:
            self.cache['cur_pos'] = self._cur_pos_from_app()
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
        if self.cache['get_selection'] == None:
            self.cache['get_selection'] = self._get_selection_from_app()
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
#        print '-- SourceBuffCached.get_text: start=%s, end=%s' % (start, end)
            
        
        if self.cache['get_text'] == None:
            self.cache['get_text'] = self._get_text_from_app()


        #
        # Note: cannot invoke self.make_valid_range() because it causes
        #       infinite recursion, ie:
        #       -> get_text() -> make_valid_range() -> len() -> get_text() -
        #      | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ | 
        #             
        if start == None: start = 0
        if end == None: end = len(self.cache['get_text'])
	if end < start:
            tmp = end
            end = start
            start = tmp

        return self.cache['get_text'][start:end]


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
        if self.cache['get_visible'] == None:
            self.cache['get_visible'] = self._get_visible_from_app()
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
	return len(self.contents())


    def newline_conventions(self):
        
        """Returns a list of the forms of newline the editor can
        recognise for this buffer (read from cache).
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        if self.cache['newline_conventions'] == None:
            self.cache['newline_conventions'] = self._newline_conventions_from_app()
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
        if self.cache['pref_newline_convention'] == None:
            self.cache['pref_newline_convention'] = self._pref_newline_convention_from_app()
        return self.cache['pref_newline_convention']

    def _pref_newline_convention_from_app(self):
        
        """Returns the form of newline that the editor prefers for
        this buffer (read directly from editor).
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        debug.virtual('SourceBuffCached._pref_newline_convention_from_app')


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

        if range == None:
            range = self.get_selection()
        old_text = self.get_text()
        self.cache['get_text'] = old_text[:range[0]] + old_text[range[1]+1:]

        #
        # Uncache visible region.
        #        
        # Note: we don't recache it from external application for efficiency
        # reasons. That's because the visible region is only needed at the
        # beginning of an utterance, but delete_cbk() can be invoked many
        # times within an utterance (which would result in many unecessary
        # calls to _get_visible_from_app()).
        #
        self.cache['get_visible'] = None

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
#        print '-- SourceBuffCached.insert_cbk: range=%s, text=\'%s\'' % (range, text)

        if range == None:
            range = self.get_selection()        
        old_text = self.get_text()
        self.cache['get_text'] = old_text[:range[0]] + text + old_text[range[1]:]

        #
        # Uncache visible region.
        #        
        # Note: we don't recache it from external application for efficiency
        # reasons. That's because the visible region is only needed at the
        # beginning of an utterance, but insert_cbk() can be invoked many
        # times within an utterance (which would result in many unecessary
        # calls to _get_visible_from_app()).
        #
        self.cache['get_visible'] = None        

    def set_selection_cbk(self, range, cursor_at=1):
        
        """External editor invokes that callback to notify VoiceCode
        of a set selection event.

        NOTE: This method should NOT update the V-E map, because that is
        already taken care of outside of the method.
        
        **INPUTS**
        
        (INT, INT) *range* -- Start and end position of selected text


        INT *cursor_at* -- indicates whether cursor was left at the
        beginning or end of *range*
        
        **OUTPUTS**
        
        *none* -- 
        """
        
#        print '-- SourceBuffCached.set_selection_cbk: called, range=%s, cursor_at=%s' % (repr(range), cursor_at)

        self.cache['get_selection'] = range
        if cursor_at > 0:
            self.cache['cur_pos'] = range[1]
        else:
            self.cache['cur_pos'] = range[0]

        #
        # Uncache visible region.
        #        
        # Note: we don't recache it from external application for efficiency
        # reasons. That's because the visible region is only needed at the
        # beginning of an utterance, but set_selection_cbk() can be invoked
        # many times within an utterance (which would result in many unecessary
        # calls to _get_visible_from_app()).
        #
        self.cache['get_visible'] = None
            

    def goto_cbk(self, pos):
        
        """External editor invokes that callback to notify VoiceCode
        of a cursor movement event.

        NOTE: This method should NOT update the V-E map, because that is
        already taken care of outside of the method.
        
        **INPUTS**
        
        INT *pos* -- Position the cursor was moved to.
        
        **OUTPUTS**
        
        *none* -- 
        """
#        print '-- SourceBuffCached.goto_cbk: called,pos=%s' % pos
        self.cache['cur_pos'] = pos

        #
        # Uncache visible region.
        #        
        # Note: we don't recache it from external application for efficiency
        # reasons. That's because the visible region is only needed at the
        # beginning of an utterance, but goto_cbk() can be invoked many
        # times within an utterance (which would result in many unecessary
        # calls to _get_visible_from_app()).
        #
        self.cache['get_visible'] = None
