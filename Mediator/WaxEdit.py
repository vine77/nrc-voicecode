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

"""base class for of new GUI interface to the mediator simulation"""


import debug
import sys
# import TextBufferWX

class WaxEdit:
    """base class for of new GUI interface to the mediator simulation

    **CLASS ATTRIBUTES**

    *none*

    **INSTANCE ATTRIBUTES**

    *none*
    """
    def mic_change(self, state):
	"""function to receive microphone state change callbacks

	**INPUTS**

	*STR* state -- new state ('on', 'off', 'sleeping', 'disabled')

	**OUTPUTS**

	*none*
	"""
        pass
# no-op by default, can be overridden

    def is_active(self):
	"""indicates whether the editor frame is active

	**INPUTS**

	*none*

	**OUTPUTS**

	*BOOL* -- true if frame window is active
	"""
	debug.virtual('WaxEdit.is_active')

    def editor_has_focus(self):
	"""indicates whether the editor window has the focus

	**INPUTS**

	*none*

	**OUTPUTS**
	*BOOL* -- true if editor window has the focus
	"""
	debug.virtual('WaxEdit.editor_has_focus')


    def editor_buffer(self):
	"""returns a reference to the TextBufferWX embedded in the GUI

	**INPUTS**

	*none*

	**OUTPUTS**

	*TextBufferWX* -- the TextBufferWX
	"""
	debug.virtual('WaxEdit.editor_buffer')


    def open_file_in_buffer(self, name):
	"""opens a new file in the existing TextBufferWX

	**INPUTS**

	*none*

	**OUTPUTS**

	*BOOL* -- true on success (otherwise the existing file is left
	there)
	"""
	debug.virtual('WaxEdit.open_file_in_buffer')

    def save_file(self, full_path, no_prompt = 0):
	"""Saves the file in the existing TextBufferWX

	**INPUTS**

	*STR full_path* -- path name of file to save

	*BOOL no_prompt* -- if true, don't prompt before overwriting
	an existing file.

	**OUTPUTS**

	*BOOL* -- true on success (otherwise the existing file is left
	there)
	"""
	debug.virtual('WaxEdit.save_file')

    def set_title_string(self, title_string):
        """sets the title string which is included in the full title 
	displayed in the title bar

	**INPUTS**

	*STR* title_string -- string to include as part of the title

	**OUTPUTS**

	*none*
	"""
	debug.virtual('WaxEdit.set_title_string')
  
    def set_name(self, name):
        """sets the filename to name (usually indicated in the title bar)

	**INPUTS**

	*STR* name -- name of current file

	**OUTPUTS**

	*none*
	"""
	debug.virtual('WaxEdit.set_name')

    def run(self, app_control):
	"""starts the message loop.  Note: this function does not
	return until the GUI exits.

	**INPUTS**

	*AppStateWaxEdit app_control* -- reference to corresponding 
	AppState interface

	**OUTPUTS**

	*none*
	"""
	debug.virtual('WaxEdit.run')

