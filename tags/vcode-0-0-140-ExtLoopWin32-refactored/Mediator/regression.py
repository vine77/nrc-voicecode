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

import debug
import Object
import mediator
import sim_commands
import MediatorObject
import NewMediatorObject
import CmdInterp
import EdSim

"""Classes and methods used to set up the MediatorObject or 
NewMediatorObject for the next new regression test
"""

class PersistentConfig(Object.Object):
    """abstract base class which hides the details of MediatorObject 
    and command initialization for regression tests which use a
    persistent MediatorObject.  
    """
    def __init__(self, **args):
        self.deep_construct(PersistentConfig, {}, args)

    def init_simulator_regression(symdict_pickle_fname=None):
        """re-initialize the mediator, using the same editor application

	**NOTE:**  This method must also ensure that the namespace in
	which the regression test definitions are/will be run with
	execfile contains an object called commands with the
	sim_commands commands as attributes.  commands can be a
	reference to the sim_commands module, if a global old
	MediatorObject is used, or an object with methods.

	**INPUTS**

	STR *symdict_pickle_fname=None* -- Name of the file containing the
	persistent version of the symbols dictionnary.

	**OUTPUTS**

	*none*
	"""
        debug.virtual('PersistentConfig.init_simulator_regression')

    def execute_command(self, command):
        """execute a command in the proper namespace, trapping any
	exceptions and printing the traceback

	**INPUTS**

	*STR command*

	**OUTPUTS**

	*none*
	"""
        debug.virtual('PersistentConfig.execute_command')

class PersistentConfigOldMediator(Object.Object):
    """implementation of PersistentConfig which calls 
    init_simulator_regression from the mediator module to create a 
    global MediatorObject in mediator.the_mediator

    **INSTANCE ATTRIBUTES**

    *{STR:ANY} names* -- the namespace dictionary in which the
    regression test definitions file, tests_def, has been (or will be) 
    run with execfile
    """
    def __init__(self, names, **args):
        """**INPUTS**

	*{STR:ANY} names* -- the namespace dictionary in which the
	regression test definitions file, tests_def, has been (or will be) 
	run with execfile
	"""
        self.deep_construct(PersistentConfigOldMediator, 
                            {
                             'names': names
                            }, args)
        self.names['init_simulator_regression'] = \
            self.init_simulator_regression

    def init_simulator_regression(self, symdict_pickle_fname=None):
        """re-initialize the mediator, using the same editor application

	**INPUTS**

	STR *symdict_pickle_fname=None* -- Name of the file containing the
	persistent version of the symbols dictionnary.

	**OUTPUTS**

	*none*
	"""
        mediator.init_simulator_regression(symdict_pickle_fname = \
            symdict_pickle_fname)
        self.names['commands'] = sim_commands
    
    def execute_command(self, command):
        """execute a command in the proper namespace, trapping any
	exceptions and printing the traceback

	**INPUTS**

	*STR command*

	**OUTPUTS**

	*none*
	"""
# right now, this method doesn't detect quit_flag, because neither
# does mediator.execute_command
        try:
            exec command in sim_commands.__dict__, sim_commands.command_space
            #	  exec command in sim_commands and command_space
        except Exception, err:
            traceback.print_exc()

class PersistentConfigNewMediator(Object.Object):
    """implementation of PersistentConfig which resets a pre-existing
    NewMediatorObject

    **INSTANCE ATTRIBUTES**

    *NewMediatorObject mediator* -- the existing mediator, which will be
    reset by the init_simulator_regression method

    *{STR:ANY} names* -- the namespace dictionary in which the
    regression test definitions file, tests_def, has been (or will be) 
    run with execfile

    *STR editor_name* -- the name of the editor being used for those
    regression tests using a persistent editor 
    """
    def __init__(self, mediator, editor_name, names, **args):
        """**INPUTS**

	*{STR:ANY} names* -- the namespace dictionary in which the
	regression test definitions file, tests_def, has been (or will be) 
	run with execfile

        *NewMediatorObject mediator* -- the existing mediator, which will be
        reset by the init_simulator_regression method

        *STR editor_name* -- the name of the editor being used for those
        regression tests using a persistent editor 
	"""
        self.deep_construct(PersistentConfigNewMediator, 
                            {
                             'mediator': mediator,
                             'names': names,
                             'editor_name': editor_name
                            }, args)

    def init_simulator_regression(symdict_pickle_fname=None):
        """re-initialize the mediator, using the same editor application

	**NOTE:**  This method must also ensure that the namespace in
	which the regression test definitions are/will be run with
	execfile contains an object called commands with the
	sim_commands commands as attributes.  commands can be a
	reference to the sim_commands module, if a global old
	MediatorObject is used, or an object with methods.

	**INPUTS**

	STR *symdict_pickle_fname=None* -- Name of the file containing the
	persistent version of the symbols dictionnary.

	**OUTPUTS**

	*none*
	"""
        self.mediator.reset(symdict_pickle_fname = symdict_pickle_fname)
        editor = self.mediator.editor_instance(self.editor_name)
        interp = self.mediator.interpreter()
        commands = sim_commands.SimCmdsObj(editor, interp, self.names)
        commands.bind_methods(self.names)
        self.names['commands'] = commands

    def execute_command(self, command):
        """execute a command in the proper namespace, trapping any
	exceptions and printing the traceback

	**INPUTS**

	*STR command*

	**OUTPUTS**

	*none*
	"""
# right now, this method doesn't detect quit_flag, because neither
# does mediator.execute_command
        try:
            exec command in self.names
        except Exception, err:
            traceback.print_exc()

class TempConfig(Object.Object):
    """abstract base class which hides the details of the internal
    structure of a temporary MediatorObject from regression tests
    which create their own MediatorObject.  
    """
    def __init__(self, **args):
        self.deep_construct(TempConfig, {}, args)

    def mediator(self):
        """returns a reference to the TempConfig's MediatorObject or
	NewMediatorObject 
	"""
        debug.virtual('TempConfig.mediator')

    def interpreter(self):
        """returns a reference to the MediatorObject's CmdInterp object
	"""
        debug.virtual('TempConfig.interpreter')

    def editor(self):
        """returns a reference to the MediatorObject's internal 
	AppState (usually EdSim) editor 
	"""
        debug.virtual('TempConfig.editor')

    def quit(self):
        """cleanup the underlying MediatorObject
	"""
        debug.virtual('TempConfig.quit')


class TempConfigFactory(Object.Object):
    """abstract base class which hides the details of MediatorObject 
    and command initialization for regression tests which create their
    own MediatorObject.  
    """
    def __init__(self, **args):
        self.deep_construct(TempConfigFactory, {}, args)

    def new_config(self, editor = None):
        """create a new TempConfig object

	**INPUTS**

	*AppState editor* -- the internal test editor to use, or None to
	create a new EdSim instance
	"""
        debug.virtual('TempConfigFactory.new_config')

class TempConfigOldMediator(Object.Object):
    """implementation of TempConfig using old MediatorObject 

    **INSTANCE ATTRIBUTES**

    *MediatorObject the_mediator* -- the temporary MediatorObject
    """
    def __init__(self, mediator, **args):
        self.deep_construct(TempConfigOldMediator, 
                            {
                             'the_mediator': mediator
                            }, args)

    def mediator(self):
        """returns a reference to the TempConfigOldMediator's MediatorObject or
	NewMediatorObject 
	"""
        return self.the_mediator

    def interpreter(self):
        """returns a reference to the MediatorObject's CmdInterp object
	"""
        return self.the_mediator.interp

    def editor(self):
        """returns a reference to the MediatorObject's internal 
	AppState (usually EdSim) editor 
	"""
        return self.the_mediator.app

    def quit(self):
        """cleanup the underlying MediatorObject
	"""
        self.the_mediator.quit(clean_sr_voc = 0, save_speech_files=0, 
            disconnect=0)
        self.the_mediator = None

class TempConfigOldMediatorFactory(Object.Object):
    """implementation of TempConfigFactory for the old MediatorObject
    """
    def __init__(self, **args):
        self.deep_construct(TempConfigOldMediatorFactory, {}, args)

    def new_config(self, editor = None, skip_config = 0):
        """create a new TempConfig object

	**INPUTS**

	*AppState editor* -- the internal test editor to use, or None to
	create a new EdSim instance

	*BOOL skip_config* -- flag allowing you to create a
	MediatorObject without configuring it 

	**OUTPUTS**

	*TempConfigOldMediator* --  the TempConfigOldOldMediator object
	"""
        if editor == None:
            app = EdSim.EdSim()
        else:
            app = editor
        a_mediator = MediatorObject.MediatorObject(app = app, 
            interp = CmdInterp.CmdInterp())
#        print a_mediator
        if not skip_config:
            a_mediator.configure()
        return TempConfigOldMediator(mediator = a_mediator)

class TempConfigNewMediator(Object.Object):
    """implementation of TempConfigFactory using NewMediatorObject

    **INSTANCE ATTRIBUTES**

    *NewMediatorObject the_mediator* -- the temporary NewMediatorObject

    *AppState the_editor* -- the editor used for tests with this
    mediator
    """
    def __init__(self, mediator, editor, **args):
        self.deep_construct(TempConfigNewMediator, 
                            {
                             'the_mediator': mediator,
                             'the_editor': editor
                            }, args)

    def mediator(self):
        """returns a reference to the TempConfig's MediatorObject or
	NewMediatorObject 
	"""
        return self.the_mediator

    def interpreter(self):
        """returns a reference to the MediatorObject's CmdInterp object
	"""
        return self.the_mediator.interpreter()

    def editor(self):
        """returns a reference to the MediatorObject's internal 
	AppState (usually EdSim) editor 
	"""
        return self.the_editor

    def quit(self):
        """cleanup the underlying MediatorObject
	"""
        self.the_editor = None
        self.the_mediator.quit(clean_sr_voc = 0, save_speech_files=0, 
            disconnect=0)
        self.the_mediator = None

class TempConfigNewMediatorFactory(Object.Object):
    """implementation of TempConfigFactory using NewMediatorObject
    """
    def __init__(self, **args):
        self.deep_construct(TempConfigNewMediatorFactory, {}, args)

    def new_config(self, editor = None, skip_config = 0):
        """create a new TempConfig object

	**INPUTS**

	*AppState editor* -- the internal test editor to use, or None to
	create a new EdSim instance

	*BOOL skip_config* -- flag allowing you to create a
	MediatorObject without configuring it 

	**OUTPUTS**

	*TempConfigNewMediator* --  the TempConfigNewMediator object
	"""
        a_mediator = NewMediatorObject.NewMediatorObject()
        if not skip_config:
            a_mediator.configure()
        if editor == None:
            app = EdSim.EdSim()
        else:
            app = editor
        a_mediator.new_editor(app)
        return TempConfigNewMediator(mediator = a_mediator, editor = app)


# defaults for vim - otherwise ignore
# vim:sw=4
