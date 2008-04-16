"""Use this simple program to experiment with wx.Python"""

import wx
class MainWindow(wx.Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent, wx.NewId(), title, size = ( 200,100),
                                     style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
       
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.items = [('a1', 'a2', 'a3', 'a4'), ('b1', 'b2' 'b3', 'b4')]
        self.list = wx.ListCtrl(self, wx.NewId(), wx.DefaultPosition,
            wx.DefaultSize, 
            style = wx.LC_REPORT | wx.LC_HRULES | wx.LC_SINGLE_SEL)
        
        self.list.InsertColumn(0, "")
        self.list.InsertColumn(1, "Written form")

        for ii in range(len(self.items)):
           self.list.InsertStringItem(ii, "%d" % (ii+1))
           self.list.SetStringItem(ii, 1, self.items[ii][0])
           self.list.SetStringItem(ii, 1, self.items[ii][1])

        self.list.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
        self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)

        self.list.ScrollList(0, len(self.items))
        main_sizer.Add(self.list, 1, wx.EXPAND | wx.ALL)
        
        wx.EVT_LIST_ITEM_ACTIVATED(self.list, self.list.GetId(), 
                                self.on_item_activated)
        wx.EVT_LIST_ITEM_SELECTED(self.list, self.list.GetId(), 
                               self.on_item_selected)
                               

        self.Show(True)
        
    def on_item_activated(self, event):
        print "-- on_item_activated: event=%s" % event
  
    def on_item_selected(self, event):
        print "-- on_item_selected: event=%s" % event

app = wx.PySimpleApp()
frame = MainWindow(None, -1, "Small editor")
app.MainLoop()