from wxPython.wx import *

class MyFrame(wxFrame):
  def __init__(self, parent, ID, title):
    wxFrame.__init__(self, parent, ID, title, wxDefaultPosition,
    wxSize(80, 120))

    menu=wxMenu()
    menu.Append(101,"E&xit","Terminate")

    menuBar=wxMenuBar()
    menuBar.Append(menu,"&File");

    self.SetMenuBar(menuBar)
    EVT_MENU(self,101,self.QuitNow)
    button = wxButton(self, 102, "Push me", wxDefaultPosition, wxDefaultSize)
    button2 = wxButton(self, 103, "Pull you", wxDefaultPosition, wxDefaultSize)
    EVT_BUTTON(self, 102, self.on_push)
    EVT_BUTTON(self, 103, self.on_pull)
    s = wxBoxSizer(wxHORIZONTAL)
    s.Add(button, 0, wxEXPAND | wxALL)
    s.Add(button2, 0, wxEXPAND | wxALL)
    self.SetAutoLayout(true)
    self.SetSizer(s)
#    b = button.GetSize()
#    print b
#    s.SetItemMinSize(button, b[0], b[1])
#    b = button2.GetSize()
#    print b
#    s.SetItemMinSize(button2, b[0], b[1])
    s.Fit(self)
    s.SetSizeHints(self)

  def on_push(self, event):
    t = Correction(self)
    answer = t.ShowModal()
  def on_pull(self, event):
    t = CorrectionB(self)
    answer = t.ShowModal()

  def QuitNow(self, event):
    self.Close(true)

class Correction(wxDialog):
  def __init__(self, parent):
    wxDialog.__init__(self, parent, wxNewId(), "Correction", wxDefaultPosition, (600, 400))
    s = wxBoxSizer(wxVERTICAL)
    text = wxTextCtrl(self, wxNewId(), "Miss Recognized text here", 
      wxDefaultPosition, wxDefaultSize)
    s.Add(text, 0, wxEXPAND | wxALL)
    choice_sizer = wxBoxSizer(wxHORIZONTAL)
    number_sizer = wxBoxSizer(wxVERTICAL)
    ID_CHOICES = wxNewId()
    choices = ["Miss Recognized text here",
               "misrecognized texture",
               "Ms. Recognized texture",
               "misrecognized text ear",
               "misrecognized text here"]
    choice_list = wxListBox(self, ID_CHOICES, wxDefaultPosition,
      wxDefaultSize, choices, wxLB_SINGLE)
    ID_NUMBERS = 200
    for i in range(1, 10):
      st = wxStaticText(self, ID_NUMBERS + i, "&%d" % i,
        wxDefaultPosition, wxDefaultSize)
      number_sizer.Add(st, 0)
    choice_sizer.Add(number_sizer, 0)
    choice_sizer.Add(choice_list, 1, wxEXPAND | wxALL)
    choice_list.SetSelection(1, 0)
    s.Add(choice_sizer, 1, wxEXPAND | wxALL)
    b_sizer = wxBoxSizer(wxHORIZONTAL)
    okb = wxButton(self, wxID_OK, "OK", wxDefaultPosition, wxDefaultSize)
    cancelb = wxButton(self, wxID_CANCEL, "Cancel", wxDefaultPosition, wxDefaultSize)
    b_sizer.Add(okb, 0, 0)
    b_sizer.Add(cancelb, 0, 0)
    s.Add(b_sizer, 0, wxEXPAND | wxALL)
    okb.SetDefault()



    self.SetAutoLayout(true)
    self.SetSizer(s)
    self.Layout()
    
class CorrectionB(wxDialog):
  def __init__(self, parent):
    wxDialog.__init__(self, parent, wxNewId(), "Correction", wxDefaultPosition, (600, 400))
    s = wxBoxSizer(wxVERTICAL)
    text = wxTextCtrl(self, wxNewId(), "Miss Recognized text here", 
      wxDefaultPosition, wxDefaultSize)
    s.Add(text, 0, wxEXPAND | wxALL)
    middle_sizer = wxFlexGridSizer(2, 2, 5, 5)
# two rows, two columns, 5 pixels between rows and columns
    number_sizer = wxBoxSizer(wxVERTICAL)
    ID_CHOICES = wxNewId()
    choices = ["Miss Recognized text here",
               "misrecognized texture",
               "Ms. Recognized texture",
               "misrecognized text ear",
               "misrecognized text here"]
    choice_list = wxListBox(self, ID_CHOICES, wxDefaultPosition,
      wxDefaultSize, choices, wxLB_SINGLE)
    ID_NUMBERS = 200
    for i in range(1, 10):
      st = wxStaticText(self, ID_NUMBERS + i, "&%d" % i,
        wxDefaultPosition, wxDefaultSize)
      number_sizer.Add(st, 0)
    middle_sizer.AddMany([(0, 0), #spacer
                          (text, 0, wxEXPAND),
                          (number_sizer, 0, wxEXPAND),
                          (choice_list, 0, wxEXPAND)])
    middle_sizer.AddGrowableRow(1)
    middle_sizer.AddGrowableCol(1)
    choice_list.SetSelection(1, 0)
    s.Add(middle_sizer, 1, wxEXPAND | wxALL)
    b_sizer = wxBoxSizer(wxHORIZONTAL)
    okb = wxButton(self, wxID_OK, "OK", wxDefaultPosition, wxDefaultSize)
    cancelb = wxButton(self, wxID_CANCEL, "Cancel", wxDefaultPosition, wxDefaultSize)
    b_sizer.Add(okb, 0, 0)
    b_sizer.Add(cancelb, 0, 0)
    s.Add(b_sizer, 0, wxEXPAND | wxALL)
    okb.SetDefault()



    self.SetAutoLayout(true)
    self.SetSizer(s)
    self.Layout()
    
    

class application(wxApp):
  def OnInit(self):
    frame = MyFrame(NULL, -1, "Hello, world")
    frame.Show(true)
#    frame.SetSize(frame.GetSizer().GetMinSize())
    self.SetTopWindow(frame)
    return true

def run():
  app=application(0)
  app.MainLoop()


if __name__ =='__main__':
  run()
