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
from debug import trace

import SourceBuff

from Object import Object

class SourceBuffCached(SourceBuff.SourceBuffWithServices):
    
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

        SourceBuff.SourceBuff.rename_buff_cbk(new_buff_name)
        self.cache['language_name'] = None
        self.cache['file_name'] = None

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
        trace('SourceBuffCached.get_pos_selection', 'first, check cache...')
        if self.cache['get_selection'] == None or \
            self.cache['cur_pos'] == None:
            pos, range = self._get_pos_selection_from_app()
            trace('SourceBuffCached.get_pos_selection',
                'pos = %s' % repr(pos))
            trace('SourceBuffCached.get_pos_selection',
                'range = %s' % repr(range))
            self.cache['cur_pos'] = pos
            self.cache['get_selection'] = range
        return self.cache['cur_pos'], self.cache['get_selection']

    def _get_pos_selection_from_app(self):
        """retrieves current position of cursor and the range of 
        current selection directly from the external application
        
        **INPUTS**
        
        *none*
        
        **OUTPUTS**
        
        *(INT, (INT, INT))* (pos, (start, end))
        
        pos is the offset into buffer of current cursor position
        start is the offset into the buffer of the start of the current
        selection.  end is the offset into the buffer of the character 
        following the selection (this matches Python's slice convention).
        """
        debug.virtual('SourceBuff._get_pos_selection_from_app')

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
        trace('SourceBuffCached.get_text', 'start=%s, end=%s' % (start, end))
            
        
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
            
        trace('SourceBuffCached.get_text', '** before returning, start=%s, end=%s, self.cache["get_text"][start:end]="%s"' % (start, end, self.cache['get_text'][start:end]))
        trace('SourceBuffCached.get_text', '** before returning, len(self.cache[\'get_text\'])=%s, self.cache[\'get_text\']="%s"' % (len(self.cache['get_text']), self.cache['get_text']))

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

#        if range == None:
#            range = self.get_selection()
# bad: if this gets the selection from the application, it will be all
# screwed up because the application will already have made the change.
# Basically, callbacks should never use defaults for the range

        SourceBuff.SourceBuff.delete_cbk(self, range)

        if self.cache['get_text'] == None:
# if we don't have the buffer contents cached, just get the entire
# current contents (which should already include the deletion), thereby
# caching it
            self.get_text()
        else:
            old_text = self.get_text()
            self.cache['get_text'] = old_text[:range[0]] + old_text[range[1]:]

        self.uncache_data_after_buffer_change(what_changed = 'get_text')
        

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
        trace('SourceBuffCached.insert_cbk', 'range=%s, text=\'%s\'' % (range, text))
        trace('SourceBuffCached.insert_cbk', '** upon entry, self.cache["cur_pos"]=%s, self.cache["get_text"]="%s"' % (self.cache["cur_pos"], self.cache["get_text"]))        

#        if range == None:
#            range = self.get_selection()
# bad: if this gets the selection from the application, it will be all
# screwed up because the application will already have made the change.
# Basically, callbacks should never use defaults for the range

        SourceBuff.SourceBuff.insert_cbk(self, range, text)
        if self.cache['get_text'] == None:
# if we don't have the buffer contents cached, just get the entire
# current contents (which should already include the insertion), thereby
# caching it
            self.get_text()
        else:
            old_text = self.get_text()
            self.cache['get_text'] = old_text[:range[0]] + text + \
                     old_text[range[1]:]

        self.uncache_data_after_buffer_change(what_changed = 'get_text')
        
        trace('SourceBuffCached.insert_cbk', '** upon exit, self.cache["cur_pos"]=%s, self.cache["get_text"]="%s"' % (self.cache["cur_pos"], self.cache["get_text"]))

    def pos_selection_cbk(self, pos, selection):
        """External editor invokes that callback to notify VoiceCode
        of a change in the current position or selection

        **INPUTS**
        
        INT *pos* -- Position the cursor was moved to.

        (INT, INT) *selection* -- Start and end position of selected text
        
        **OUTPUTS**
        
        *none* -- 
        """
        trace('SourceBuffCached.pos_selection_cbk',
            'pos is %d, selection is %d, %d' % (pos, selection[0],
            selection[1]))
        self.cache['get_selection'] = selection
        self.cache['cur_pos'] = pos
            
# DCF: this should only be called after changes to the buffer *contents*
#        self.uncache_data_after_buffer_change('get_selection')            

    def uncache_data_after_buffer_change(self, what_changed=None):
        trace('SourceBuffCached.uncache_data_after_buffer_change',
              'invoked, what_changed="%s"' % what_changed)
        #
        # Uncache data that may have become obsolete as a result of a
        # buffer change.
        #
        for cache_entry_name in ('cur_pos', 'get_visible', 'get_selection'):
            trace('SourceBuffCached.uncache_data_after_buffer_change',
                  '** cache_entry_name="%s"' % cache_entry_name)
            
            if cache_entry_name != what_changed:
                #
                # Don't uncache the data that was changed, because we assume
                # that it has been cached to the appropriate value.
                #
                self.cache[cache_entry_name] = None
                
        trace('SourceBuffCached.uncache_data_after_buffer_change',
              'exited')
        
