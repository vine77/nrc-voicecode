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

"""A SourceBuff that delegates a series of methods to supporting services."""


import sb_services, SourceBuff

class SourceBuffWithServices(SourceBuff.SourceBuff):

   def __init__(self, srv_sim_kbd_and_mouse_edits = sb_services.SB_ServiceSimulateKbdAndMouseEditsWindowsStyle(),
                      **attrs):
        self.deep_construct(SourceBuffWithServices,
                            {'srv_sim_kbd_and_mouse_edits': srv_sim_kbd_and_mouse_edits},
                            attrs
                            )


###################################################################
# Methods for simulating user kbd and mouse input. Those methods
# are only used by the regression test, in order to test mixed mode
# (i.e. voice + mouse + kbd) editing scenarios.
###################################################################
    
   def set_selection_by_kbd(self, start, end):
      self.srv_sim_kbd_and_mouse_edits.simulate_set_selection_by_kbd(start, end)
        
   def move_cursor_by_kbd(self, direction, num_steps):
      self.srv_sim_kbd_and_mouse_edits.simulate_set_selection_by_kbd(direction, num_steps)
        
   def type_text(self, text):
      self.srv_sim_kbd_and_mouse_edits.simulate_set_selection_by_kbd(text)

    
   def set_selection_by_kbd(self, start, end):
       self.srv_sim_kbd_and_mouse_edits.simulate_set_selection_by_kbd(start, end)
       
   def move_cursor_by_kbd(self, direction, num_steps):
       self.srv_sim_kbd_and_mouse_edits.simulate_move_cursor_by_kbd(direction, num_steps)
        
   def type_text(self, text):
       self.srv_sim_kbd_and_mouse_edits.simulate_type_text(text)
        
