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
# (C)2000, David C. Fox
#
##############################################################################

"""classes for managing results of the dictation grammar 
"""

from Object import Object, OwnerObject
import debug
import re

import CmdInterp, AppState
from SpokenUtterance import *

class ResMgr(OwnerObject):
    """abstract class defining interface for an object which manages
    results of the dictation grammar for a particular editor instance.

    **INSTANCE ATTRIBUTES**

    *RecogStartMgr* recog_mgr -- the parent RecogStartMgr object, 
    which provides information about editor application instances, as
    well as access to the CmdInterp interpreter object

    *STR* name -- the name of the editor instance

    **CLASS ATTRIBUTES**
    
    *none*
    """

    def __init__(self, recog_mgr, instance_name, **args):
        """
        **INPUTS**

        *RecogStartMgr* recog_mgr -- the parent RecogStartMgr object, 
        which provides information about editor application instances, as
        well as access to the CmdInterp interpreter object

        *STR* instance_name -- the name of the editor instance
        """

        self.deep_construct(ResMgr,
                            {'recog_mgr': recog_mgr,
                             'name': instance_name
                            },
                            args)
        self.name_parent('recog_mgr')
        
    def interpreter(self):
        """return a reference to the mediator's current CmdInterp object

        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        return self.recog_mgr.interpreter()

    def editor(self):
        """return a reference to the editor corresponding to this ResMgr

        **INPUTS**

        *none*

        **OUTPUTS**

        *AppState* -- the AppState interface to the editor responding
        to this ResMgr
        """
        return self.recog_mgr.app_instance(self.name)

    def interpret_dictation(self, result, initial_buffer = None):
        """interpret the result of recognition by a dictation grammar,
        and store the relevant information to allow for correction.

        **INPUTS**

        *SpokenUtterance result* -- a SpokenUtterance object
        representing the recognition results

        *STR initial_buffer* -- the name of the initial buffer which was
        active at recognition-starting

        **OUTPUTS**

        *none*
        """
        debug.virtual('ResMgr.interpret_dictation')

    def rename_buffer_cbk(self, old_buff_name, new_buff_name):
        """callback which notifies us that the given editor
        instance has renamed a buffer

        **INPUTS**

        *STR* old_buff_name -- old name of the buffer 

        *STR* new_buff_name -- new name of the buffer 

        **OUTPUTS**

        *none*
        """
        debug.virtual('ResMgr.rename_buffer_cbk')

    def stored_utterances(self):
        """tells how many dictated utterances have been stored

        **INPUTS**

        *none*

        **OUTPUTS**

        *INT* -- number of utterances which can be retrieved with
        recent_dictation
        """
        debug.virtual('ResMgr.stored_utterances')

    def recent_dictation(self, n = None):
        """returns a list of SpokenUtterance objects

        **Note:** additional dictation into the editor will increment
        the indices of specific utterances, so the mediator must not
        allow dictation into the editor between the call to 
        recent_dictation to get the utterances and the call to 
        reinterpret_recent.

        **INPUTS**

        *INT n* -- the number of utterances to return, or None to return 
        all available utterances.

        **OUTPUTS**

        *[(SpokenUtterance, BOOL)]* -- the n most recent dictation 
        utterances (or all available if < n), sorted most recent last, 
        with corresponding flags indicating if the utterance can be 
        undone and re-interpreted, or None if no utterances are stored.

        Note:  These utterances should not be stored permanently, nor
        should they be modified except as part of the correction
        process.  Also, the status of whether a given utterance can be
        re-interpreted may change if the user makes other changes to the 
        """
        debug.virtual('ResMgr.recent_dictation')

    def scratch_recent(self, n = 1):
        """undo the effect of the most recent n utterances, if possible.

        **INPUTS**

        *INT n* -- number of utterances to undo

        **OUTPUTS**

        *INT* -- number of utterances actually undone
        """
        debug.virtual('ResMgr.scratch_recent')

    def reinterpret_recent(self, changed):
        """undo the effect of one or more recent utterances, if
        possible, and reinterpret these utterances (and possibly any
        intervening utterances), making the appropriate changes to the
        editor buffers.

        **Note:** additional dictation into the editor will increment
        the indices of specific utterances, so the mediator must not
        allow dictation into the editor between the call to 
        recent_dictation to get the utterances and the call to 
        reinterpret_recent.

        **Note:** this method does not perform adaption of the changed
        utterances.  The caller should do that itself.

        **INPUTS**

        *[INT] changed* -- the indices into the stack of recent
        utterances of those utterances which were corrected by the user

        **NOTE:** particular implementations of ResMgr may reinterpret 
        all utterances subsequent to the oldest changed utterance

        **OUTPUTS**

        *[INT]* -- the indices of the utterances actually reinterpreted
        (including intervening ones), sorted with the oldest first, or 
        None if no utterances could be reinterpreted
        """
        debug.virtual('ResMgr.reinterpret_recent')
   
    def can_reinterpret(self, n):
        """can we safely reinterpret the nth most recent utterance

        **INPUTS**

        *INT n* -- the depth in the editor state stack of the utterance
        to be reinterpreted

        **OUTPUTS**

        *BOOL* -- true if we can safely reinterpret that utterance
        """
        debug.virtual('ResMgr.can_reinterpret')
   

class ResMgrStd(ResMgr):
    """implementation of ResMgr including the standard processing of 
    dictation utterances.

    **INSTANCE ATTRIBUTES**

    *none*
    """
    def __init__(self, **args):
        self.deep_construct(ResMgrStd,
                            {
                            },
                            args)
        
    def _std_interp(self, result, app, initial_buffer = None, 
        before = None, after = None):
        """internal method for the standard sequence of calls to
        interpret the result of recognition by a dictation grammar,
        with callbacks to allow the caller to store the relevant 
        information to allow for correction.

        **INPUTS**

        *SpokenUtterance result* -- a SpokenUtterance object
        representing the recognition results

        *AppState app* -- the AppState interface to the editor (or a
        proxy object)

        *STR initial_buffer* -- the name of the initial buffer which was
        active at recognition-starting

        *FCT* before -- a callback function, 
        before(*AppState* app, *STR* initial_buffer), to be called before
        interpretation starts, or None to do nothing

        *FCT* after -- a callback function, 
        after(*AppState* app, *STR* initial_buffer), to be called after
        interpretation is done, or None to do nothing

        **OUTPUTS**

        *none*
        """
        debug.trace('ResMgrStd._std_interp', 'standard interpretation')
        if before:
            debug.trace('ResMgrStd._std_interp', 'about to call before')
            before(app, initial_buffer = initial_buffer)
        interp = self.interpreter()
        words = result.words()
        interp.interpret_cmd_tuples(words, app, 
            initial_buffer = initial_buffer)
        if after:
            debug.trace('ResMgrStd._std_interp', 'about to call after')
            after(app, initial_buffer = initial_buffer)
        app.print_buff_if_necessary(buff_name = initial_buffer)

    def interpret_dictation(self, result, initial_buffer = None):
        """interpret the result of recognition by a dictation grammar,
        and store the relevant information to allow for correction.

        **INPUTS**

        *SpokenUtterance result* -- a SpokenUtterance object
        representing the recognition results

        *STR initial_buffer* -- the name of the initial buffer which was
        active at recognition-starting

        **OUTPUTS**

        *none*
        """
        app = self.editor()
        debug.trace('ResMgrStd.interpret_dictation', 'about to interpret')
        self._std_interp(result, app, initial_buffer = initial_buffer)

    def rename_buffer_cbk(self, old_buff_name, new_buff_name):
        """callback which notifies us that the given editor
        instance has renamed a buffer

        **INPUTS**

        *STR* old_buff_name -- old name of the buffer 

        *STR* new_buff_name -- new name of the buffer 

        **OUTPUTS**

        *none*
        """
# no information stored, so do nothing, but subclasses will need to
# define this
        pass

    def stored_utterances(self):
        """tells how many dictated utterances have been stored

        **INPUTS**

        *none*

        **OUTPUTS**

        *INT* -- number of utterances which can be retrieved with
        recent_dictation
        """
        return 0
# no information stored, but subclasses will need to
# define this

    def recent_dictation(self, n = None):
        """returns a list of SpokenUtterance objects

        **Note:** additional dictation into the editor will increment
        the indices of specific utterances, so the mediator must not
        allow dictation into the editor between the call to 
        recent_dictation to get the utterances and the call to 
        reinterpret_recent.

        **INPUTS**

        *INT n* -- the number of utterances to return, or None to return 
        all available utterances.

        **OUTPUTS**

        *[(SpokenUtterance, BOOL)]* -- the n most recent dictation 
        utterances (or all available if < n), sorted most recent last, 
        with corresponding flags indicating if the utterance can be 
        undone and re-interpreted, or None if no utterances are stored.

        Note:  These utterances should not be stored permanently, nor
        should they be modified except as part of the correction
        process.  Also, the status of whether a given utterance can be
        re-interpreted may change if the user makes other changes to the 
        """
        return None
# no information stored, but subclasses will need to
# define this

    def scratch_recent(self, n = 1):
        """undo the effect of the most recent n utterances, if possible.

        **INPUTS**

        *INT n* -- number of utterances to undo

        **OUTPUTS**

        *INT* -- number of utterances actually undone
        """
# no information stored, but subclasses will need to
# define this
        return 0

    def reinterpret_recent(self, changed):
        """undo the effect of one or more recent utterances, if
        possible, and reinterpret these utterances (and possibly any
        intervening utterances), making the appropriate changes to the
        editor buffers.

        **Note:** additional dictation into the editor will increment
        the indices of specific utterances, so the mediator must not
        allow dictation into the editor between the call to 
        recent_dictation to get the utterances and the call to 
        reinterpret_recent.

        **Note:** this method does not perform adaption of the changed
        utterances.  The caller should do that itself.

        **INPUTS**

        *[INT] changed* -- the indices into the stack of recent
        utterances of those utterances which were corrected by the user

        **NOTE:** particular implementations of ResMgr may reinterpret 
        all utterances subsequent to the oldest changed utterance

        **OUTPUTS**

        *[INT]* -- the indices of the utterances actually reinterpreted
        (including intervening ones), sorted with the oldest first, or 
        None if no utterances could be reinterpreted
        """
# no information stored, but subclasses will need to
# define this
        return None
   
    def can_reinterpret(self, n):
        """can we safely reinterpret the nth most recent utterance

        **INPUTS**

        *INT n* -- the depth in the editor state stack of the utterance
        to be reinterpreted

        **OUTPUTS**

        *BOOL* -- true if we can safely reinterpret that utterance
        """
# no information stored, but subclasses will need to
# define this
        return 0
   

   
   

class BufferStates(Object):
    """Abstract interface which collects source buffer cookies for all
    buffers which currently exist in an application.
    """
    def __init__(self, **args):
        self.deep_construct(BufferStates, {}, args)
    
    def known_buffer(self, buff_name):
        """returns the state cookie associated with a given buff_name

        **INPUTS**

        *STR buff_name* -- the name of the buffer

        **OUTPUTS**

        *BOOL* -- true if the buffer is known
        """
        debug.virtual('BufferStates.known_buffer')

    def known_buffers(self):
        """returns a list of the names of known buffers

        **INPUTS**

        *none*

        **OUTPUTS**

        *[STR]* -- list of names of buffers for which we have cookies
        """
        debug.virtual('BufferStates.known_buffers')

    def cookie(self, buff_name):
        """returns the state cookie associated with a given buff_name

        **INPUTS**

        *STR buff_name* -- the name of the buffer

        **OUTPUTS**

        *SourceBuffCookie* -- state cookie (see SourceBuff), or None if
        the buffer is unknown.  Note: this may be used temporarily but
        should not be stored permanently.  Also, note that 
        SourceBuffCookie is a dummy class.  The actual return type will 
        vary with the SourceBuff subclass.
        """ 
        debug.virtual('BufferStates.cookie')

    def valid_cookies(self, app, ignore_deleted = 0):
        """checks whether our state cookies are still valid
        If the state corresponding to a cookie has
        been lost, valid_cookies will return false.

        **INPUTS**

        *BOOL ignore_deleted* -- should we ignore buffers which no
        longer exist in the current state?

        **OUTPUTS**

        *BOOL* -- true if our cookies are valid
        """
        debug.virtual('BufferStates.valid_cookies')

    def rename_buffer_cbk(self, old_buff_name, new_buff_name):
        """callback which notifies us that the editor
        has renamed a buffer

        **INPUTS**

        *STR* old_buff_name -- old name of the buffer 

        *STR* new_buff_name -- new name of the buffer 

        **OUTPUTS**

        *none*
        """
        debug.virtual('BufferStates.rename_buffer_cbk')

    def compare_with_current(self, app, ignore_new = 1, ignore_deleted = 0):
        """compares the stored state to the current one.
        
        **INPUTS**

        *AppState app* -- the editor whose states should be compared

        *BOOL ignore_new* -- should we ignore new buffers (ones in the
        current state but not in the stored state)?

        *BOOL ignore_deleted* -- should we ignore buffers which no
        longer exist in the current state?

        **OUTPUTS**

        *BOOL* -- true if states are the same, false if they are not, or
        it cannot be determined due to expiration of cookies
        """
        debug.virtual('BufferStates.compare_with_current')

    def restore_state(self, app):
        """restores the editor to its stored state

        **NOTE:** restore_state never re-creates deleted buffers or
        modifies new ones. 
        
        **INPUTS**

        *AppState app* -- the editor whose states should be restored

        **OUTPUTS**

        *BOOL* -- true if restore was successful
        """
        debug.virtual('SourceBuff.restore_state')

class UnexpectedRestoreFailure(RuntimeError):
    """exception used internally by BufferStatesBasic.restore_state 
    to signal that restore failed on a particular buffer, and to 
    trigger an attempt to un-restore all the buffers previously 
    restored

    This exception should be caught by the restore_state method, 
    so it should never be seen outside that method.
    """
    def __init__(self, buff_name):
        """
        **INPUTS**

        *STR buff_name* -- name of the buffer which could not be
        restored
        """
        self.buff_name = buff_name
        RuntimeError.__init__(self, self.generate_message)

    def generate_message(self):
        warning = \
            'BufferStatesBasic.restore_state: unable to restore\n'
        warning = warning + \
            'state of buffer %s despite earlier check\n' % self.buff_name
        warning = warning + \
            'indicating that the cookie was valid\n'
        return warning
    
class BufferStatesBasic(Object):
    """implementation of BufferStates

    **INSTANCE ATTRIBUTES**

    *{STR: SourceBuffCookie} cookies* -- map from buffer names to
    cookies representing the state of the buffer
    """
    def __init__(self, app, buffers = None, **args):
        """
        **INPUTS**

        *AppState app* -- the editor whose state should be stored

        *[STR] buffers* -- a list of buffers whose states should be
        stored, or None to store all buffers
        """
        self.deep_construct(BufferStatesBasic,
                            {
                             'cookies': {}
                            },
                            args)
        if buffers is None:
# really, we don't want to get this from the editor:
# for storing the state before interpretation, we will already have
# synchronized with the editor.
# for storing the state after interpretation, we don't want to give the
# editor any chance to send updates.
            buffers = app.open_buffers_from_app()
        for buff_name in buffers:
            buffer = app.find_buff(buff_name)
            if buffer != None:
                self.cookies[buff_name] = buffer.store_current_state()

    def known_buffer(self, buff_name):
        """returns the state cookie associated with a given buff_name

        **INPUTS**

        *STR buff_name* -- the name of the buffer

        **OUTPUTS**

        *BOOL* -- true if the buffer is known
        """
        return self.cookies.has_key(buff_name)

    def known_buffers(self):
        """returns a list of the names of known buffers

        **INPUTS**

        *none*

        **OUTPUTS**

        *[STR]* -- list of names of buffers for which we have cookies
        """
        return self.cookies.keys()

    def cookie(self, buff_name):
        """returns the state cookie associated with a given buff_name

        **INPUTS**

        *STR buff_name* -- the name of the buffer

        **OUTPUTS**

        *SourceBuffCookie* -- state cookie (see SourceBuff), or None if
        the buffer is unknown.  Note: this may be used temporarily but
        should not be stored permanently.  Also, note that 
        SourceBuffCookie is a dummy class.  The actual return type will 
        vary with the SourceBuff subclass.
        """ 
        if self.known_buffer(buff_name):
            return self.cookies[buff_name]
        return None

    def valid_cookies(self, app, ignore_deleted = 0):
        """checks whether our state cookies are still valid
        If the state corresponding to a cookie has
        been lost, valid_cookies will return false.

        **INPUTS**
        
        *AppState app* -- the editor to which our cookies belong

        *BOOL ignore_deleted* -- should we ignore buffers which no
        longer exist in the current state?

        **OUTPUTS**

        *BOOL* -- true if our cookies are valid
        """
        for buff_name in self.known_buffers():
            buffer = app.find_buff(buff_name)
            if buffer is None:
                if ignore_deleted:
                    continue
                return 0
            if not buffer.valid_cookie(self.cookies[buff_name]):
                return 0
        return 1

    def rename_buffer_cbk(self, old_buff_name, new_buff_name):
        """callback which notifies us that the editor
        has renamed a buffer

        **INPUTS**

        *STR* old_buff_name -- old name of the buffer 

        *STR* new_buff_name -- new name of the buffer 

        **OUTPUTS**

        *none*
        """
        if old_buff_name == new_buff_name:
            return
        try:
            self.cookies[new_buff_name] = self.cookies[old_buff_name]
            del self.cookies[old_buff_name]
        except KeyError:
            pass

    def compare_with_current(self, app, ignore_new = 1, ignore_deleted = 0):
        """compares the stored state to the current one.
        
        **INPUTS**

        *AppState app* -- the editor whose states should be compared

        *BOOL ignore_new* -- should we ignore new buffers (ones in the
        current state but not in the stored state)?

        *BOOL ignore_deleted* -- should we ignore buffers which no
        longer exist in the current state?

        **OUTPUTS**

        *BOOL* -- true if states are the same, false if they are not, or
        it cannot be determined due to expiration of cookies
        """

        if not ignore_new:
            current_buffers = app.open_buffers_from_app()
            for buff_name in current_buffers:
                if not self.known_buffer(buff_name):
                    return 0

        for buff_name in self.known_buffers():
            buffer = app.find_buff(buff_name)
            if buffer is None:
                if ignore_deleted:
                    continue
                return 0
            if not buffer.compare_with_current(self.cookies[buff_name]):
                return 0
        return 1

    def restore_state(self, app):
        """restores the editor to its stored state

        **NOTE:** restore_state never re-creates deleted buffers or
        modifies new ones. 
        
        **INPUTS**

        *AppState app* -- the editor whose states should be restored

        **OUTPUTS**

        *BOOL* -- true if restore was successful
        """
# we have to check all our cookies first, so that we don't restore some
# buffers before realizing that others can't be restored,
# leaving the editor in a mixed up state
        if not self.valid_cookies(app, ignore_deleted = 1):
            return 0

        debug.trace('BufferStatesBasic.restore_state',
                    'cookies valid, proceeding to restore')
        temporary_cookies = {}
        try:
            for buff_name in self.known_buffers():
                buffer = app.find_buff(buff_name)
                if buffer is None:
# when restoring, always ignore deleted buffers
                    continue
                temporary_cookies[buff_name] = buffer.store_current_state()
                debug.trace('BufferStatesBasic.restore_state',
                    'restoring %s' % buff_name)
                if not buffer.restore_state(self.cookies[buff_name]):
                    raise UnexpectedRestoreFailure(buff_name = buff_name)
            return 1
        except UnexpectedRestoreFailure, e:
            failed_to_fix = []
            for buff_name, cookie in self.temporary_cookies.items():
                if buff_name == e.buff_name:
                    continue
                buffer = app.find_buff(buff_name)
                if buffer is None:
# when restoring, always ignore deleted buffers
                    continue
# here, ignore errors (we want to un-restore the rest of the buffers,
# and besides, what else can we do but try)
                if not buffer.restore_state(temporary_cookies[buff_name]):
                    failed_to_fix.append(buff_name)
            warning = e.generate_message()
            debug.critical_warning(warning)
            if len(failed_to_fix) != 0:
                failed = 'Failed to un-restore the following buffers:\n'
                for buff_name in failed_to_fix:
                    failed = failed + '%s\n' % buff_name
                debug.critical_warning(failed_to_fix)
            return 0
        
class StateStack(Object):
    """Abstract interface for storing a stack of
    BufferStates representing the state of an editor's buffers before
    interpretation of the most recent dictation utterances

    **NOTE:** To maintain the integrity of the StateStack, before_interp
    MUST be called before every dictation utterance which is stored in
    the utterance stack, after_interp MUST be called after the utterance
    and before any other updates (besides those in direct response to
    the interpretation) from the editor are processed, and no other
    methods of StateStack may be called between the calls to
    before_interp and after_interp.
    """
    def __init__(self, **args):
        self.deep_construct(StateStack, {}, args)
    
    def before_interp(self, app, initial_buffer = None):
        """method which must be called before interpretation of a
        dictation utterance to store editor state (or compare with the
        state stored after the previous utterance).

        This method will compare the state after the most recent dictation 
        utterance to the current state.  If they do not match,
        before_interp will clear the stack.  Then, it will push the 
        current state onto the stack.

        After this method returns, the top of the stack will be the 
        editor state before the utterance is interpreted.

        **NOTE:** To maintain the integrity of the StateStack, before_interp
        MUST be called before every dictation utterance which is stored in
        the utterance stack, after_interp MUST be called after the utterance
        and before any other updates (besides those in direct response to
        the interpretation) from the editor are processed, and no other
        methods of StateStack may be called between the calls to
        before_interp and after_interp.
            
        **INPUTS**

        *AppState app* -- the editor into which the user is dictating

        *STR initial_buffer* -- the name of the initial buffer which was
        active at recognition-starting

        **OUTPUTS**

        *none*
        """
        debug.virtual('StateStack.before_interp')

    def after_interp(self, app, initial_buffer = None):
        """method which must be called after interpretation of a
        dictation utterance to store editor state.

        This method will store the current state, but not on the stack.

        **NOTE:** To maintain the integrity of the StateStack, before_interp
        MUST be called before every dictation utterance which is stored in
        the utterance stack, after_interp MUST be called after the utterance
        and before any other updates (besides those in direct response to
        the interpretation) from the editor are processed, and no other
        methods of StateStack may be called between the calls to
        before_interp and after_interp.
        
        **INPUTS**

        *AppState app* -- the editor into which the user is dictating

        *STR initial_buffer* -- the name of the initial buffer which was
        active at recognition-starting

        **OUTPUTS**

        *none*
        """
        debug.virtual('StateStack.after_interp')

    def safe_depth(self, app):
        """returns the number of entries in the stack which can be
        safely restored

        **INPUTS**

        *AppState app* -- the editor 

        **OUTPUTS**

        *INT* -- the depth in the state stack to which we can
        safely restore the editor
        """
        debug.virtual('StateStack.safe_depth')

    def undo_manual_changes(self, app):
        """restores the editor to its state just after the most recent 
        dictated utterance, but prior to any subsequent manual changes.
        (Any new buffers will not be removed, nor will buffers deleted
        since the utterance be restored).

        **NOTE:** use this method with extreme caution, as the
        StateStack provides no means to redo these changes, and the 
        user may not expect manual changes to vanish.

        **NOTE:** This method must not 
        be called between before_interp and after_interp.

        **INPUTS**

        *AppState app* -- the editor 

        **OUTPUTS**

        *BOOL* -- true if we successfully restored to that state
        """
        debug.virtual('StateStack.undo_manual_changes')

    def can_restore(self, app, n):
        """can we safely restore the editor to its nth most recent
        stored state (popping n entries off our stack)?

        **NOTE:** This method must not 
        be called between before_interp and after_interp.

        **INPUTS**

        *AppState app* -- the editor 

        *INT n* -- the depth in the editor state stack to which we are 
        trying to restore the state (n = 1 refers to the top entry)

        **OUTPUTS**

        *BOOL* -- true if we can safely restore to that state
        """
        debug.virtual('StateStack.can_restore')

    def pop(self, app, n):
        """restores the editor to its nth most recent stored state, if
        this can be done safely, popping n entries off our stack.

        **NOTE:** This method must not 
        be called between before_interp and after_interp.

        **INPUTS**

        *AppState app* -- the editor 

        *INT n* -- the depth in the editor state stack to which we are 
        trying to restore the state (n = 1 refers to the top entry)

        *BOOL* -- true if we sucessfully restored the editor to that state
        """
        debug.virtual('StateStack.pop')

    def rename_buffer_cbk(self, old_buff_name, new_buff_name):
        """callback which notifies us that the editor
        has renamed a buffer

        **INPUTS**

        *STR* old_buff_name -- old name of the buffer 

        *STR* new_buff_name -- new name of the buffer 

        **OUTPUTS**

        *none*
        """
        debug.virtual('StateStack.rename_buffer_cbk')

class StateStackBasic(StateStack):
    """implementation of StateStack using BufferStatesBasic

    **INSTANCE ATTRIBUTES**

    *[BufferStatesBasic] states* -- the stack of stored editor states

    *BufferStatesBasic after_utterance* -- the state of the editor after
    the most recent utterance

    *INT max_depth* -- maximum depth of the stack

    *BOOL ignore_new* -- should we ignore new buffers (ones in the
    current state but not in the stored state) when comparing states,
    and simply restore the states of the stored buffers?

    *BOOL ignore_deleted* -- should we ignore buffers which no
    longer exist in the current state, and simply restore the states of
    the buffers which still exist?
    """
    def __init__(self, max_depth, ignore_new = 1, ignore_deleted = 0, **args):
        """
        **INPUTS**

        *INT max_depth* -- maximum depth of the stack, or -1 to allow an
        unlimited stack

        *BOOL ignore_new* -- should we ignore new buffers (ones in the
        current state but not in the stored state) when comparing states,
        and simply restore the states of the stored buffers?

        *BOOL ignore_deleted* -- should we ignore buffers which no
        longer exist in the current state, and simply restore the states of
        the buffers which still exist?
        """
        self.deep_construct(StateStackBasic, 
                            {
                             'states': [],
                             'after_utterance': None,
                             'max_depth': max_depth,
                             'ignore_new': ignore_new,
                             'ignore_deleted': ignore_deleted
                            }, args)

    def before_interp(self, app, initial_buffer = None):
        """method which must be called before interpretation of a
        dictation utterance to store editor state (or compare with the
        state stored after the previous utterance).

        This method will compare the state after the most recent dictation 
        utterance to the current state.  If they do not match,
        before_interp will clear the stack.  Then, it will push the 
        current state onto the stack.

        After this method returns, the top of the stack will be the 
        editor state before the utterance is interpreted.

        **NOTE:** To maintain the integrity of the StateStack, before_interp
        MUST be called before every dictation utterance which is stored in
        the utterance stack, after_interp MUST be called after the utterance
        and before any other updates (besides those in direct response to
        the interpretation) from the editor are processed, and no other
        methods of StateStack may be called between the calls to
        before_interp and after_interp.
            
        **INPUTS**

        *AppState app* -- the editor into which the user is dictating

        *STR initial_buffer* -- the name of the initial buffer which was
        active at recognition-starting

        **OUTPUTS**

        *none*
        """
        if self.after_utterance and \
            not self.after_utterance.compare_with_current(app, 
                ignore_new = self.ignore_new,
                ignore_deleted = self.ignore_deleted):
# if the current state doesn't match that after the (previous) most
# recent utterance, then the rest of the stack is invalid, so clear it
            self.states = []
        self.after_utterance = None
        current = BufferStatesBasic(app)
        self._push(current)

    def _push(self, state):
        """private method to push a state onto the stack, removing an
        element from the bottom if the depth exceeds max_depth

        **INPUTS**

        *BufferStateBasic state* -- the state to push onto the stack

        **OUTPUTS**

        *none*
        """
        self.states.append(state)
        if self.max_depth > 0 and len(self.states) > self.max_depth:
            del self.states[0]

    def after_interp(self, app, initial_buffer = None):
        """method which must be called after interpretation of a
        dictation utterance to store editor state.

        This method will store the current state, but not on the stack.

        **NOTE:** To maintain the integrity of the StateStack, before_interp
        MUST be called before every dictation utterance which is stored in
        the utterance stack, after_interp MUST be called after the utterance
        and before any other updates (besides those in direct response to
        the interpretation) from the editor are processed, and no other
        methods of StateStack may be called between the calls to
        before_interp and after_interp.
        
        **INPUTS**

        *AppState app* -- the editor into which the user is dictating

        *STR initial_buffer* -- the name of the initial buffer which was
        active at recognition-starting

        **OUTPUTS**

        *none*
        """
        current = BufferStatesBasic(app)
        self.after_utterance = current

    def safe_depth(self, app):
        """returns the number of entries in the stack which can be
        safely restored

        **INPUTS**

        *AppState app* -- the editor 

        **OUTPUTS**

        *INT* -- the depth in the state stack to which we can
        safely restore the editor
        """
        if len(self.states) == 0:
            return 0
        if self.after_utterance is None:
            return 0
        same = self.after_utterance.compare_with_current(app, 
            ignore_new = self.ignore_new, 
            ignore_deleted = self.ignore_deleted)
        if not same:
            return 0
# in this implementation, we clear the stack whenever the state before
# the next dictation utterance doesn't match the state after
# the previous utterance.  Therefore, the only thing left to check is
# whether the states in the stack have valid cookies
        for n in range(1, len(self.states) + 1):
            if not self.states[-n].valid_cookies(app, 
                ignore_deleted = self.ignore_deleted):
# if the cookies aren't valid, we might as well delete those states
                del self.states[0:-(n-1)]
                return n-1
        return len(self.states)

    def undo_manual_changes(self, app):
        """restores the editor to its state just after the most recent 
        dictated utterance, but prior to any subsequent manual changes.
        (Any new buffers will not be removed, nor will buffers deleted
        since the utterance be restored).

        **NOTE:** use this method with extreme caution, as the
        StateStack provides no means to redo these changes, and the 
        user may not expect manual changes to vanish.

        **NOTE:** This method must not 
        be called between before_interp and after_interp.

        **INPUTS**

        *AppState app* -- the editor 

        **OUTPUTS**

        *BOOL* -- true if we successfully restored to that state
        """
        if self.after_utterance is None:
            return 0
        return self.after_utterance.restore_state(app)

    def can_restore(self, app, n):
        """can we safely restore the editor to its nth most recent
        stored state (popping n entries off our stack)?

        **NOTE:** This method must not 
        be called between before_interp and after_interp.

        **INPUTS**

        *AppState app* -- the editor 

        *INT n* -- the depth in the editor state stack to which we are 
        trying to restore the state (n = 1 refers to the top entry)

        **OUTPUTS**

        *BOOL* -- true if we can safely restore to that state
        """
        if n < 1:
            return 0
        if len(self.states) < n:
            return 0
        safe = self.safe_depth(app)
        if safe >= n:
            return 1
        return 0

    def pop(self, app, n):
        """restores the editor to its nth most recent stored state, if
        this can be done safely, popping n - 1 entries off our stack.

        **NOTE:** This method must not 
        be called between before_interp and after_interp.

        **INPUTS**

        *AppState app* -- the editor 

        *INT n* -- the depth in the editor state stack to which we are 
        trying to restore the state (n = 1 refers to the top entry)

        *BOOL* -- true if we sucessfully restored the editor to that state
        """
        debug.trace('StateStack.pop', 'called with n = %d' % n)
        if not self.can_restore(app, n):
            debug.trace('StateStack.pop', 'unable to restore')
            return 0
        temporary = BufferStatesBasic(app)
        if not self.undo_manual_changes(app):
            warning = \
                'StateStack.pop: unexpected failure to restore state\n'
            debug.critical_warning(warning)
            temporary.restore_state(app)
            return 0
        for i in range(1, n+1):
            debug.trace('StateStack.pop', 'popping %d' % i)
            if not self.states[-i].restore_state(app):
# since we checked cookies in can_restore, this shouldn't happen, but
# if it does, un-restore the state before returning 0 to signal failure
                warning = \
                    'StateStack.pop: unexpected failure to restore state\n'
                debug.critical_warning(warning)
                temporary.restore_state(app)
                return 0
        self.after_utterance = self.states[-n]
        del self.states[-n:]
        return 1

    def rename_buffer_cbk(self, old_buff_name, new_buff_name):
        """callback which notifies us that the editor
        has renamed a buffer

        **INPUTS**

        *STR* old_buff_name -- old name of the buffer 

        *STR* new_buff_name -- new name of the buffer 

        **OUTPUTS**

        *none*
        """
        for state in self.states:
            state.rename_buffer_cbk(old_buff_name, new_buff_name)

class ResMgrBasic(ResMgrStd):
    """implementation of ResMgrStd providing services necessary for
    basic correction.

    **INSTANCE ATTRIBUTES**

    *INT max_utterances* -- the maximum number of recent dictation utterances 
    to store

    *[SpokenUtterance] utterances* -- queue of recent utterances, sorted with
    most recent last

    *[STR] initial_buffers* -- queue of names of initial buffers 
    corresponding to the utterances

    *StateStackBasic states* -- stack representing the state of the editor 
    application before/after recent utterances
    """
    def __init__(self, max_utterances = 30, **args):
        self.deep_construct(ResMgrBasic,
                            {
                             'max_utterances': max_utterances,
                             'utterances': [],
                             'initial_buffers': [],
                             'states': StateStackBasic(max_utterances)
                            },
                            args)
        
    def store(self, result, initial_buffer):
        """store the result, along with the editor state before and 
        after interpretation

        **INPUTS**

        *SpokenUtterance result* -- a SpokenUtterance object
        representing the recognition results

        **OUTPUTS**

        *none*
        """
        debug.trace('ResMgrBasic.store', 
            'storing an utterance (already have %d)' % len(self.utterances))
        if len(self.utterances) >= self.max_utterances:
            debug.trace('ResMgrBasic.store', 'removing the oldest')
            del self.utterances[0]
            del self.initial_buffers[0]
        self.utterances.append(result)
        self.initial_buffers.append(initial_buffer)

    def interpret_dictation(self, result, initial_buffer = None):
        """interpret the result of recognition by a dictation grammar,
        and store the relevant information to allow for correction.

        **INPUTS**

        *SpokenUtterance result* -- a SpokenUtterance object
        representing the recognition results

        *STR initial_buffer* -- the name of the initial buffer which was
        active at recognition-starting

        **OUTPUTS**

        *none*
        """
        debug.trace('ResMgrBasic.interpret_dictation', 'about to interpret')
        app = self.editor()
        ResMgrStd._std_interp(self, result, 
            app, 
            initial_buffer = initial_buffer, 
            before = self.states.before_interp,
            after = self.states.after_interp)
        self.store(result, initial_buffer = initial_buffer)

    def rename_buffer_cbk(self, old_buff_name, new_buff_name):
        """callback which notifies us that the given editor
        instance has renamed a buffer

        **INPUTS**

        *STR* old_buff_name -- old name of the buffer 

        *STR* new_buff_name -- new name of the buffer 

        **OUTPUTS**

        *none*
        """
        self.states.rename_buffer_cbk(old_buff_name, new_buff_name)
        for i in range(len(self.initial_buffers)):
            if self.initial_buffer[i] == old_buff_name:
                self.initial_buffer[i] = new_buff_name


    def stored_utterances(self):
        """tells how many dictated utterances have been stored

        **INPUTS**

        *none*

        **OUTPUTS**

        *INT* -- number of utterances which can be retrieved with
        recent_dictation
        """
        return len(self.utterances)

    def recent_dictation(self, n = None):
        """returns a list of SpokenUtterance objects

        **Note:** additional dictation into the editor will increment
        the indices of specific utterances, so the mediator must not
        allow dictation into the editor between the call to 
        recent_dictation to get the utterances and the call to 
        reinterpret_recent.

        **INPUTS**

        *INT n* -- the number of utterances to return, or None to return 
        all available utterances.

        **OUTPUTS**

        *[(SpokenUtterance, BOOL)]* -- the n most recent dictation 
        utterances (or all available if < n), sorted most recent last, 
        with corresponding flags indicating if the utterance can be 
        undone and re-interpreted, or None if no utterances are stored.

        Note:  These utterances should not be stored permanently, nor
        should they be modified except as part of the correction
        process.  Also, the status of whether a given utterance can be
        re-interpreted may change if the user makes other changes to the 
        buffer during
        """
        available = self.stored_utterances()
        if available == 0:
            return None
        if n == None:
            m = available
        else:
            m = min(n, available)
        safe = self.states.safe_depth(self.editor())
        debug.trace('ResMgrBasic.recent_dictation', 'safe depth = %d' % safe)
        utterances = []
        for i in range(m, 0, -1):
            utterances.append((self.utterances[-i], i <= safe))
        return utterances
   
    def scratch_recent(self, n = 1):
        """undo the effect of the most recent n utterances, if possible.

        **INPUTS**

        *INT n* -- number of utterances to undo

        **OUTPUTS**

        *INT* -- number of utterances actually undone
        """
        debug.trace('ResMgrBasic.scratch_recent', 
            'attempting to scratch n = %d' % n)
        safe = self.states.safe_depth(self.editor())
        if safe < 1:
            return 0
        m = min(safe, n)
        app = self.editor()
        success = self.states.pop(app, m)
        if success:
            del self.utterances[-m:]
            return m
        return 0
    
    def reinterpret_recent(self, changed):
        """undo the effect of one or more recent utterances, if
        possible, and reinterpret these utterances (and possibly any
        intervening utterances), making the appropriate changes to the
        editor buffers.

        **Note:** this method does not perform adaption of the changed
        utterances.  The caller should do that itself.

        **Note:** additional dictation into the editor will increment
        the indices of specific utterances, so the mediator must not
        allow dictation into the editor between the call to 
        recent_dictation to get the utterances and the call to 
        reinterpret_recent.

        **INPUTS**

        *[INT] changed* -- the indices into the stack of recent
        utterances of those utterances which were corrected by the user

        **NOTE:** particular implementations of ResMgr may reinterpret 
        all utterances subsequent to the oldest changed utterance

        **OUTPUTS**

        *[INT]* -- the indices of the utterances actually reinterpreted
        (including intervening ones), sorted with the oldest first, or 
        None if no utterances could be reinterpreted
        """
        n = max(changed)
        debug.trace('ResMgrBasic.reinterpret_recent', 
            'max changed = %d' % n)
        app = self.editor()
        n = min(n, self.stored_utterances())
        debug.trace('ResMgrBasic.reinterpret_recent', 
            'max changed and stored = %d\n' % n)
        m = self.states.safe_depth(self.editor())
        debug.trace('ResMgrBasic.reinterpret_recent', 
            'safe depth = %d' % m)
        m = min(m, n)
        debug.trace('ResMgrBasic.reinterpret_recent', 
            'so popping %d' % m)
        if not self.states.pop(app, m):
            return None
        to_do = self.utterances[-m:]
        buffers = self.initial_buffers[-m:]
        del self.utterances[-m:]
        del self.initial_buffers[-m:]
        debug.trace('ResMgrBasic.reinterpret_recent', 
            'about to reinterpret %s' % repr(to_do))
        for i in range(len(to_do)):
            debug.trace('ResMgrBasic.reinterpret_recent', 
                'reinterpreting %d' % (m - i))
            utterance = to_do[i]
            debug.trace('ResMgrBasic.reinterpret_recent', 
                'spoken_forms %s' % repr(utterance.spoken_forms()))
            self.interpret_dictation(utterance,
                initial_buffer = buffers[i])
        return range(m, 0, -1)

    def can_reinterpret(self, n):
        """can we safely reinterpret the nth most recent utterance

        **INPUTS**

        *INT n* -- the depth in the editor state stack of the utterance
        to be reinterpreted

        **OUTPUTS**

        *BOOL* -- true if we can safely reinterpret that utterance
        """
        app = self.editor()
        if n <= self.stored_utterances() and \
            n <= self.states.safe_depth(app):
            return 1
        return 0
   
# defaults for vim - otherwise ignore
# vim:sw=4
