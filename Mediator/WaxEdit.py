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
import TextBufferWX

class WaxEdit:
    """base class for of new GUI interface to the mediator simulation

    **CLASS ATTRIBUTES**

    *none*

    **INSTANCE ATTRIBUTES**

    *none*
    """
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
