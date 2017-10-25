import wx
import matplotlib.pyplot as plt
import numpy as np

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        #wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(900, 657))
        super(MainFrame, self).__init__(parent, title = title, size=(1000,500))
        self.initUI()
        self.Centre()
        self.Show(True)

    def initUI(self):
        panel = wx.Panel(self)
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        fgs = wx.FlexGridSizer(rows=1, cols=2, vgap=5, hgap=5)
        vbox_left = wx.BoxSizer(wx.VERTICAL)
        vbox_right = wx.BoxSizer(wx.VERTICAL)

        st1 = wx.StaticText(panel, label='Choose data:')
        st1.SetFont(font)
        vbox_left.Add(st1, flag=wx.RIGHT, border=8)

        self.rb_xyz = wx.CheckBox(panel, label = 'XYZ graphs',pos = (100,100))
        vbox_left.Add(self.rb_xyz, flag=wx.RIGHT | wx.BOTTOM | wx.TOP, border=10)

        lblList = ['Blue', 'Green', 'Red']
        self.rbox = wx.RadioBox(panel, label = 'Glass color', pos = (80,10), choices = lblList, majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        vbox_left.Add(self.rbox, flag=wx.RIGHT | wx.BOTTOM, border=15)

        self.show_graph_btn = wx.Button(panel, -1, label='Show graphs', pos = (80,10), name='show_graphs')
        vbox_left.Add(self.show_graph_btn, flag=wx.RIGHT | wx.BOTTOM, border=15)

        #RIGHT PANEL

        '''self.figure = Figure(figsize=(5,5))
        self.axe = self.figure.add_subplot(111)
        self.canvas_xyz = FigureCanvas(self, -1, self.figure)

        vbox_right.Add(self.canvas_xyz, flag=wx.RIGHT | wx.BOTTOM | wx.TOP, border=10)'''

        fgs.AddMany([(vbox_right), (vbox_left)])
        hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        #hbox.Add(vbox_left, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        #hbox.Add(vbox_right, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        self.Bind(wx.EVT_CHECKBOX, self.onChecked)
        self.Bind(wx.EVT_BUTTON, self.OnClicked)
        self.rbox.Bind(wx.EVT_RADIOBOX, self.onRadioBox)

        panel.SetSizer(hbox)

    def onRadioBox(self,e):
        print self.rbox.GetStringSelection(),' is clicked from Radio Box'

    def onChecked(self, e):
        cb = e.GetEventObject()
        print cb.GetLabel(),' is clicked',cb.GetValue()

    def OnClicked(self, event):
        label = event.GetEventObject().GetLabel()
        name = event.GetEventObject().GetName()
        if name == 'show_graphs':
            if self.rb_xyz.GetValue() == True:
                print ''
                #show xyz graph
            print 'DRAW GRAPHS'
        print "Label of pressed button = ",label, " My btn name: ", name


if __name__ == '__main__':

    app = wx.App()
    MainFrame(None, title='Chromaticity modeling of an object')
    app.MainLoop()
