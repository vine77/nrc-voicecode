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
        self.before_interp(initial_buffer = initial_buffer)
        interp = self.interpreter()
        words = result.words()
        app = self.recog_mgr.app_instance(self.name)
        interp.interpret_command_tuple(words, app, 
            initial_buffer = initial_buffer)
        self.after_interp()
        app.print_buff_if_necessary(buff_name = self.buff_name)


    def before_interp(self, initial_buffer = None):
        """hook for any additional pre-interpretation processing needed by
        a subclass (e.g. to store buffer states to allow correction)
        
        **INPUTS**

        *STR initial_buffer* -- the name of the initial buffer which was
        active at recognition-starting

        **OUTPUTS**

        *none*
        """
        pass

    def after_interp(self):
        """hook for any additional post-interpretation processing needed by
        a subclass (e.g. to store buffer states to allow correction)
        
        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        pass

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
   

class StateInfo(Object):
    """Abstract interface for storing, comparing, and restoring the
    state of an editor application

    """
    def __init__(self, **args):
        self.deep_construct(StateInfo,
                            args)


class ResMgrBasic(ResMgr):
    """implementation of ResMgrStd providing services necessary for
    basic correction.

    **INSTANCE ATTRIBUTES**

    *INT max_utterances* -- the maximum number of recent dictation utterances 
    to store

    *[SpokenUtterance] utterances* -- queue of recent utterances, sorted with
    most recent last

    *[StateInfo] before* -- queue of StateInfo objects representing the 
    application state before interpretation of the corresponding utterance 
    in utterances

    *[StateInfo] after* -- queue of StateInfo objects representing the 
    application state after interpretation of the corresponding utterance 
    in utterances

    *StateInfo temp_before* -- temporary StateInfo object for 
    application state before the utterance currently being interpreted

    *StateInfo temp_after* -- temporary StateInfo object for 
    application state after the utterance currently being interpreted
    """
    def __init__(self, max_utterances = 30, **args):
        self.deep_construct(ResMgrBasic,
                            {
                             'max_utterances': max_utterances,
                             'utterances': [],
                             'before': [],
                             'after': [],
                             'temp_before': None,
                             'temp_after': None
                            },
                            args)
        
    def store(self, result):
        """store the result, along with the editor state before and 
        after interpretation

        **INPUTS**

        *SpokenUtterance result* -- a SpokenUtterance object
        representing the recognition results

        **OUTPUTS**

        *none*
        """
        if len(self.utterances) >= self.max_utterances:
            del self.utterances[0]
            del self.before[0]
            del self.after[0]
        self.utterances.append(result)
        self.before.append(self.temp_before)
        self.after.append(self.temp_after)

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
        self.clear_temp_states()
        ResMgrStd.interpret_dictation(self, result, 
            initial_buffer = initial_buffer)
        self.store(result)
        self.clear_temp_states()

    def clear_temp_states(self):
        """clear the temporary application states after they've been 
        stored to the queues
        
        **INPUTS**
        
        *none*

        **OUTPUTS**

        *none*
        """
        self.temp_before = None
        self.temp_after = None

    def before_interp(self, initial_buffer = None):
        """hook for any additional pre-interpretation processing needed by
        a subclass (e.g. to store buffer states to allow correction)
        
        **INPUTS**

        *STR initial_buffer* -- the name of the initial buffer which was
        active at recognition-starting

        **OUTPUTS**

        *none*
        """
        app = self.recog_mgr.app_instance(self.name)

    def after_interp(self):
        """hook for any additional post-interpretation processing needed by
        a subclass (e.g. to store buffer states to allow correction)
        
        **INPUTS**

        *none*

        **OUTPUTS**

        *none*
        """
        pass

    def rename_buffer_cbk(self, old_buff_name, new_buff_name):
        """callback which notifies us that the given editor
        instance has renamed a buffer

	**INPUTS**

	*STR* old_buff_name -- old name of the buffer 

	*STR* new_buff_name -- new name of the buffer 

	**OUTPUTS**

	*none*
	"""
        for state in self.before:
            state.rename_buffer_cbk(old_buff_name, new_buff_name)
        for state in self.after:
            state.rename_buffer_cbk(old_buff_name, new_buff_name)
   
