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
# (C) 2001, National Research Council of Canada
#
##############################################################################

"""Use this interface if the link between VoiceCode and the external editor is slow"""

import AppState, debug, SourceBuffCached

class AppStateCached(AppState.AppState):
    
    """Interface optimised for editors that communicate with VoiceCode
    through a slow link.

    In order to minimise communication between VoiceCode and the
    editor, *AppStateCached* keeps a local copy of the state of the
    editor. This avoids having to query the editor for the same
    information all the time.

    Methods in *AppStateCached* assume that:

    - The cached information will be synchronised with the editor's
      state at the beginning of every utterance.

    - *AppStateCached* methods that affect the state of the editor
      *directly* (that is, without going through an other [AppState]
      or [SourceBuff] method) will synchronize the cache before
      exiting.

    For any method *readingMethod* that reads the state of the
    external editor, *AppStateCached* implements two methods:

    *readingMethod* -- This is the public method (usually a method of
     [AppState]) used to read the state. It usually just checks if
     value is cached, and if so, reads it from cache. If value is not
     cached, it retrieves it from the external editor an caches it.

    *_readingMethod_from_app* -- This is a private method which reads
     the state directly from the external editor. Such methods are not
     expected to save the read state to cache (this will done by
     [synchronize_with_app] method).

    For any method *writingMethod* that changes the state of the
    external editor, *AppStateCached* implements two methods:

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

    ..[curr_buffer_name] file:///./AppStateCached.AppStateCached.html#curr_buffer_name
    ..[multiple_buffers] file:///./AppStateCached.AppStateCached.html#multiple_buffers
    ..[synchronize_with_app] file:///./AppStateCached.AppStateCached.html#synchronize_with_app
    ..[AppState] AppState.AppState.html
    ..[SourceBuff] SourceBuff.SourceBuff.html"""
    
    def __init__(self, **args_super):
        self.init_attrs({'cache': {}})
        self.deep_construct(AppStateCached, 
                            {}, 
                            args_super, 
                            {})

    def init_cache(self):
        """Initialises the cache with data obtained from external editor.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        self.cache = {}

