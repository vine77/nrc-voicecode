import wx
import TestCaseWithHelpers
from wxWindowsWithHelpers import *
import debug


class wxListCtrlTestDlg(wxDialogWithHelpers):
    def __init__(self):
        wxDialogWithHelpers.__init__(self, None, wx.NewId(), "Testing wxListCtrlWithHelpers", (1, 1),
                          (600, 400),
                          style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
                          
        self.button = wxButtonWithHelpers(self, wx.NewId(), "Button", wx.DefaultPosition, 
                               wx.DefaultSize)
        wx.EVT_BUTTON(self, self.button.GetId(), self.on_button)
        
        self.button_was_clicked = False

        self.list = \
            wxListCtrlWithHelpers(self, wx.NewId(), 
                                                       style = wx.LC_REPORT | wx.LC_HRULES | wx.LC_SINGLE_SEL)

        self.list.InsertColumn(0,"This is Col #1")
        self.list.InsertColumn(1,"This is Col #2")
        self.list.InsertColumn(2,"This is Col #3")

        self.list.InsertStringItem(0, "item 0-0")
        self.list.SetStringItem(0,1,"item 0-1")
        self.list.SetStringItem(0,2,"item 0-2")

        self.list.InsertStringItem(1, "item 1-0")
        self.list.SetStringItem(1,1,"item 1-1")
        self.list.SetStringItem(1,2, "item 1-2")
        
        wx.EVT_LIST_ITEM_SELECTED(self.list, self.list.GetId(), self.on_list_ctrl_selected)
        wx.EVT_LIST_ITEM_ACTIVATED(self.list, self.list.GetId(), self.on_list_ctrl_item_activated)
        wx.EVT_CHAR(self.list, self.on_list_char)
        
        self.list_ctrl_item_selected = None
        self.last_key_pressed = {}
        self.last_item_selected = {}
        self.last_list_item_activated = None
        
    def on_button(self, event):
        self.button_was_clicked = True

    def on_list_ctrl_selected(self, event):
        self.list_ctrl_item_selected = event

    def on_list_ctrl_item_activated(self, event):
        self.last_list_item_activated = event.GetIndex()
        
    def on_list_char(self, event):
        self.last_key_pressed[self.list] = event.GetKeyCode()
        
    def last_key_pressed_for_widget(self, widget):
        last_key = None
        if self.last_key_pressed.has_key(widget):
           last_key = self.last_key_pressed[widget]
        return last_key

    def last_item_selected_for_widget(self, widget):
        last_item = None
        if self.last_item_selected.has_key(widget):
           last_item = self.last_item_selected[widget]
        return last_item

class wxButtonWithHelpersTest(TestCaseWithHelpers.TestCaseWithHelpers):
   def __init__(self, name):
      TestCaseWithHelpers.TestCaseWithHelpers.__init__(self, name)

   def setUp(self):
      self.dlg = wxListCtrlTestDlg()       

   def tearDown(self):
      self.dlg.Destroy()

   def test_button_Click(self):
      self.assert_(not self.dlg.button_was_clicked,
                   "button started out as being clicked.")
      self.dlg.button.Click()
      self.assert_(self.dlg.button_was_clicked,
                   "button was not clicked.")


class wxListCtrlWithHelpersTest(TestCaseWithHelpers.TestCaseWithHelpers):
        
    def __init__(self, name):
       TestCaseWithHelpers.TestCaseWithHelpers.__init__(self, name)
       
    def setUp(self):
       self.dlg = wxListCtrlTestDlg()       

    def tearDown(self):
       self.dlg.Destroy()

    def test_NumberOfColumns(self):
       self.assert_equal(3, self.dlg.list.NumberOfColumns(),
                          "Number of columns was wrong.", )

    def test_NumberOfRows(self):
       self.assert_equal(self.dlg.list.NumberOfRows(), 2,
                          "Number of rows was wrong.")
       
    def test_AllCellsContentsString(self):
       self.assert_sequences_have_same_content([['item 0-0', 'item 0-1', 'item 0-2'], ['item 1-0', 'item 1-1', 'item 1-2']], 
                                               self.dlg.list.AllCellsContentsString(),
                                               "Cells of the list were wrong.")
                                               
    def test_Select(self):
       self.dlg.list.Select(1)
       self.assert_(self.dlg.list_ctrl_item_selected != None,
                    "Selection of a list ctrl item did not invoke appropriate callback method.")
           
    # AD: Reactivate this test when we upgrade to wx.Python 2.5 (ActivateNth does
    #     not work with wx.Python < 2.5)         
    def ___test_ActivateNth(self):
       self.assert_equal(None,
                          self.dlg.last_list_item_activated,
                          "List started out with an activated item")                          
       self.dlg.list.ActivateNth(1)
       self.assert_equal(1,
                          self.dlg.last_list_item_activated,
                          "Activating an element of the list did not invoke proper event handler")                          
## this test doesn't work onto the migration to wx ( from wxPython) that is
## it seems the SendKeys function is not used in voicecode presently
##    def test_SendKey(self):
##       self.assert_(self.dlg.last_key_pressed_for_widget(self.dlg.list) == None, 
##                   "List control already had a key pressed into it from the start.")
##       self.dlg.list.SendKey(wx.WXK_DOWN)
##       self.assert_(self.dlg.last_key_pressed_for_widget(self.dlg.list) != None, 
##                   "Pressing a key on list item did not invoke appropriate event handler.")
##       self.assert_equal(wx.WXK_DOWN, self.dlg.last_key_pressed_for_widget(self.dlg.list), 
##                    "Wrong key received by event handler.")
##    
       
class wxDialogWithHelpersTest(TestCaseWithHelpers.TestCaseWithHelpers):
        
    def __init__(self, name):
       TestCaseWithHelpers.TestCaseWithHelpers.__init__(self, name)
       
    def setUp(self):
       self.dlg = wxListCtrlTestDlg()       

    def tearDown(self):
       self.dlg.Destroy()
    