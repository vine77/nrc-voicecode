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
# (C)2002, National Research Council of Canada
#
##############################################################################

"""Subclasses of various wxPython widgets with additional helper methods.

Among other things, those helper methods are useful for unit testing GUIs

"""

from wxPython.wx import *
import debug

class wxListCtrlWithHelpers(wxListCtrl):
    """A wxListCtrl subclass with helpers for finding more about the data
    that is displayed in it.
    """
    def __init__(self, frame, id, pos=wxDefaultPosition, size=wxDefaultSize, style=wxLC_REPORT | wxLC_HRULES | wxLC_SINGLE_SEL):
       wxListCtrl.__init__(self, frame, id, pos, size, style)
        
    def GetCellContentsString(self, row, column ):
       return self.GetItem(row, column).m_text
    
    def NumberOfColumns(self):
       num_cols = 0
       while(1):
          col = self.GetColumn(num_cols)
          if col:
             num_cols = num_cols + 1
          else:
             break
       return num_cols

    def NumberOfRows(self):
       return self.GetItemCount()
       
    def AllCellsContentsString(self):
       contents = []
       for row_num in range(self.NumberOfRows()):
          row = []
          for col_num in range(self.NumberOfColumns()):
             row.append(self.GetCellContentsString(row_num, col_num))
          contents.append(row)
       return contents
       
    def GetColumnContents(self, col_num):
       contents = []
       for row_num in range(self.NumberOfRows()):
          contents.append(self.GetCellContentsString(row_num, col_num))
       return contents
    
       
class MockListSelectionEvent(wxListEvent):
    def __init__(self, nth):
       wxListEvent.__init__(self)
       self.nth = nth

    def GetIndex(self):
       return self.nth
       
# defaults for vim - otherwise ignore
# vim:sw=4