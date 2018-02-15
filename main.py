import wx
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

import data_loading as dl
import data_processing as dp
import optimization as optim
import time

class MainFrame(wx.Frame):

    def __init__(self, parent, title):
        #wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(900, 657))
        super(MainFrame, self).__init__(parent, title = title, size=(800,600))
        self.FILENAME = 'CC-2.txt'
        self.DISTANCE = 'cie1976'
        self.initUI()
        self.Centre()
        self.Show(True)

    def initUI(self):

        self.createMenu()
        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        fgs = wx.FlexGridSizer(rows=1, cols=2, vgap=5, hgap=5)
        vbox_left = wx.BoxSizer(wx.VERTICAL)
        vbox_right = wx.BoxSizer(wx.VERTICAL)

        font = wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')

        st1 = wx.StaticText(panel, label='Choose data:')
        vbox_left.Add(st1, flag=wx.RIGHT, border=8)

        self.rb_xyz = wx.CheckBox(panel, label = 'XYZ graphs',pos = (100,100))
        vbox_left.Add(self.rb_xyz, flag=wx.RIGHT | wx.BOTTOM | wx.TOP, border=10)

        lblList = ['Blue (CC-2)', 'Green (GZC-9)', 'Red (0C-14)']
        self.rbox = wx.RadioBox(panel, label = 'Glass color', pos = (80,10), choices = lblList, majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        vbox_left.Add(self.rbox, flag=wx.RIGHT | wx.BOTTOM, border=15)

        self.to_rgb_btn = wx.Button(panel, -1, label='To RGB', pos = (80,10), name='to_rgb')
        vbox_left.Add(self.to_rgb_btn, flag=wx.RIGHT | wx.BOTTOM, border=15)

        self.non_optim_text = wx.StaticText(panel, label='Non-optimized color')
        self.non_optim_text.SetFont(font)
        vbox_left.Add(self.non_optim_text, flag=wx.CENTER | wx.BOTTOM, border=15)

        self.color = wx.TextCtrl(panel, pos=(300, 0), size=(350, 200))
        self.color.SetFont(font)
        vbox_left.Add(self.color, flag=wx.RIGHT | wx.BOTTOM, border=15)

        self.optimize_btn = wx.Button(panel, -1, label='Optimize color', pos=(80, 10), name='optimize')
        vbox_left.Add(self.optimize_btn, flag=wx.RIGHT | wx.BOTTOM, border=15)

        LOAD_FILE_ID = wx.NewId()
        self.Bind(wx.EVT_MENU, self.loadFile, id=LOAD_FILE_ID)

        #RIGHT PANEL

        st2 = wx.StaticText(panel, label='Show input data:')
        vbox_right.Add(st2, flag=wx.RIGHT, border=15)

        self.show_graph_btn = wx.Button(panel, -1, label='Show graphs', pos=(80, 10), name='show_graphs')
        vbox_right.Add(self.show_graph_btn, flag=wx.RIGHT | wx.BOTTOM, border=15)

        self.show_cube_btn = wx.Button(panel, -1, label='Show cube', pos=(80, 10), name='show_cube')
        vbox_right.Add(self.show_cube_btn, flag=wx.RIGHT | wx.BOTTOM, border=15)

        lblList2 = ['CIE 1976', 'CIE 1994', 'CIE 2000']
        self.distance = wx.RadioBox(panel, label='Metric of the distance', pos=(80,10), choices=lblList2, majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        vbox_right.Add(self.distance, flag=wx.LEFT | wx.BOTTOM, border=15)

        self.optim_text = wx.StaticText(panel, label='Optimized color')
        self.optim_text.SetFont(font)
        vbox_right.Add(self.optim_text, flag=wx.CENTER | wx.BOTTOM, border=10)

        self.color_optimized = wx.TextCtrl(panel, pos=(300, 0), size=(350, 200))
        self.color_optimized.SetFont(font)
        vbox_right.Add(self.color_optimized, flag=wx.RIGHT | wx.BOTTOM, border=15)

        fgs.AddMany([(vbox_left), (vbox_right)])
        hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)

        self.Bind(wx.EVT_CHECKBOX, self.onChecked)
        self.Bind(wx.EVT_BUTTON, self.OnClicked)
        self.rbox.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.distance.Bind(wx.EVT_RADIOBOX, self.onDistanceRadioBox)

        panel.SetSizer(hbox)

    def onRadioBox(self,e):
        if self.rbox.GetSelection() == 0: #CC-2 choice
            self.FILENAME = 'CC-2.txt'
        elif self.rbox.GetSelection() == 1:
            self.FILENAME = 'GZC-9.txt'
        elif self.rbox.GetSelection() == 2:
            self.FILENAME = 'OC-14.txt'

    def onDistanceRadioBox(self, e):
        if self.distance.GetSelection() == 0:
            self.DISTANCE = 'cie1976'
        elif self.distance.GetSelection() == 1:
            self.DISTANCE = 'cie1994'
        elif self.distance.GetSelection() == 2:
            self.DISTANCE = 'cie2000'
        elif self.distance.GetSelection() == 3:
            self.DISTANCE = 'cmc'


    def onChecked(self, e):
        cb = e.GetEventObject()
        print(cb.GetLabel(),' is clicked',cb.GetValue())

    def OnClicked(self, event):
        label = event.GetEventObject().GetLabel()
        name = event.GetEventObject().GetName()
        if name == 'show_graphs':
            if self.rb_xyz.GetValue() == True:
                wave_length, x, y, z = dl.load_xyz_csv()
                plt.plot(wave_length, z, wave_length, y, wave_length, x)
                plt.xlabel('Wavelength(nm)')
                plt.axis([350, 850, 0, 2.1])
                plt.grid(True)
                plt.title('The CIE standard observer color matching functions')
                plt.show()
            data = dl.load_txt(self.FILENAME)
            func = interp1d(data[:,0], data[:,1], kind='slinear')
            dp.plot_data(data, [], 'Wavelength(nm)', '', '', func)
        elif name == 'to_rgb':
            data = dl.load_txt(self.FILENAME)
            func = interp1d(data[:,0], data[:,1], kind='slinear') #interpolation of the data
            R, G, B = dp.plot_to_xyz(func)
            print ("LAB: ", dp.rgb_to_lab(R,G,B))
            self.color.SetBackgroundColour(wx.Colour(R * 255.0, G * 255.0, B * 255.0))
            self.Refresh()
        elif name == 'show_cube':
            #dp.get_rgb_cube_surface()
            dp.get_rgb_points()
        elif name == 'optimize':
            data = dl.load_txt(self.FILENAME)
            print("FILENAME: ", self.FILENAME)
            print("DISTANCE: ", self.DISTANCE)
            func = interp1d(data[:, 0], data[:, 1], kind='slinear')  # interpolation of the data
            R, G, B = dp.plot_to_xyz(func)
            self.color.SetBackgroundColour(wx.Colour(R * 255.0, G * 255.0, B * 255.0))
            self.color.SetValue(str(int(R * 255)) + " " + str(int(G * 255)) + " " + str(int(B * 255)))
            self.Refresh()
            print("LAB: ", dp.rgb_to_lab(R, G, B))
            R_optim, G_optim, B_optim = optim.steepest_descend((R, G, B), self.DISTANCE, self)
            print((int(R_optim * 255), int(G_optim * 255), int(B_optim * 255)))
            self.color_optimized.SetBackgroundColour((int(R_optim * 255), int(G_optim * 255), int(B_optim * 255)))
            self.color_optimized.SetValue(str(int(R_optim * 255)) + " " + str(int(G_optim * 255)) + " " + str(int(B_optim * 255)))
            self.Refresh()
            print("RGB: ", (R, G, B), "RGB_optimized: ", (R_optim, G_optim, B_optim))
            print("RGB: ", (R * 255, G * 255, B * 255), "RGB_optimized: ", (R_optim * 255, G_optim * 255, B_optim * 255))

    def createMenu(self):
        menubar = wx.MenuBar()
        file = wx.Menu()
        help = wx.Menu()
        file.Append(101, '&Open\tCtrl+O', 'Open a new document')
        file.AppendSeparator()
        quit = wx.MenuItem(file, 105, '&Quit\tCtrl+Q', 'Quit the Application')
        file.Append(quit)
        menubar.Append(file, '&File')
        menubar.Append(help, '&Help')
        self.SetMenuBar(menubar)
        self.CreateStatusBar()
        self.Centre()
        self.Bind(wx.EVT_MENU, self.onQuit, id=105)
        self.Bind(wx.EVT_MENU, self.loadFile, id=101)

    def loadFile(self, event):
        dlg = wx.FileDialog(self, "Open", "", "", "*.txt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.FILENAME = dlg.GetPath()
        dlg.Destroy()

    def onQuit(self, event):
        self.Close()


if __name__ == '__main__':

    app = wx.App()
    MainFrame(None, title='Chromaticity modeling of an object')
    app.MainLoop()
