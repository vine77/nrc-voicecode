from wxPython.wx import *
import TestCaseWithHelpers
import wxWindowsWithHelpers
import debug


class wxListCtrlTestDlg(wxDialog):
    def __init__(self):
        wxDialog.__init__(self, None, wxNewId(), "Testing wxListCtrlWithHelpers", (1, 1),
                          (600, 400),
                          style = wxDEFAULT_DIALOG_STYLE | wxRESIZE_BORDER)

        self.list = \
            wxWindowsWithHelpers.wxListCtrlWithHelpers(self, wxNewId(), 
                                                       style = wxLC_REPORT | wxLC_HRULES | wxLC_SINGLE_SEL)

        self.list.InsertColumn(0,"This is Col #1")
        self.list.InsertColumn(1,"This is Col #2")
        self.list.InsertColumn(2,"This is Col #3")

        self.list.InsertStringItem(0, "item 0-0")
        self.list.SetStringItem(0,1,"item 0-1")
        self.list.SetStringItem(0,2,"item 0-2")

        self.list.InsertStringItem(1, "item 1-0")
        self.list.SetStringItem(1,1,"item 1-1")
        self.list.SetStringItem(1,2, "item 1-2")


class wxListCtrlWithHelpersTest(TestCaseWithHelpers.TestCaseWithHelpers):
        
    def __init__(self, name):
       TestCaseWithHelpers.TestCaseWithHelpers.__init__(self, name)
       
    def setUp(self):
       self.dlg = wxListCtrlTestDlg()       

    def test_NumberOfColumns(self):
       self.assert_equals(3, self.dlg.list.NumberOfColumns(),
                          "Number of columns was wrong.", )

    def test_NumberOfRows(self):
       self.assert_equals(self.dlg.list.NumberOfRows(),
                          "Number of rows was wrong.", 2)
       
    def test_AllCellsContentsString(self):
       self.assert_sequences_have_same_content([['item 0-0', 'item 0-1', 'item 0-2'], ['item 1-0', 'item 1-1', 'item 1-2']], 
                                               self.dlg.list.AllCellsContentsString(),
                                               "Cells of the list were wrong.")
                                               
                                                   
    def tearDown(self):
       self.dlg.Destroy()
       