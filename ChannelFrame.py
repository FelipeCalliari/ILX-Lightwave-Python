# -*- coding: cp1252 -*-

import wx

from LED      import LED

class ChannelFrame(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        self.StaticBox = wx.StaticBox(self, -1, "Channel") 
        self.StaticBoxSizer = wx.StaticBoxSizer(self.StaticBox, wx.VERTICAL) 
        self.grid = wx.GridBagSizer(0, 0)

        self.On = wx.Button(self, -1,  "ON",  size = (58,22)) 
        self.Off = wx.Button(self, -1, "OFF", size = (58,22))

        self.Led = LED(self)
        self.Led.SetState(0)

        self.PWR = wx.StaticText(self, label = u"Power [dBm]:  ",     size = (120,20), style = wx.ALIGN_RIGHT)
        self.WVL = wx.StaticText(self, label = u"Wavelength [nm]:  ", size = (120,20), style = wx.ALIGN_RIGHT)

        self.txtPWR = wx.TextCtrl(self, size = (80,20), value = "")
        self.txtWVL = wx.TextCtrl(self, size = (80,20), value = "")

        self.grid.Add(self.On,     pos = (0,0), flag = wx.ALL|wx.ALIGN_CENTER_VERTICAL, border = 0)
        self.grid.Add(self.Off,    pos = (0,1), flag = wx.ALL|wx.ALIGN_CENTER_VERTICAL, border = 0)
        self.grid.Add(self.Led,    pos = (0,2), flag = wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border = 0)
        self.grid.Add(self.PWR,    pos = (1,0), flag = wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border = 0, span = (1,2))
        self.grid.Add(self.WVL,    pos = (2,0), flag = wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border = 0, span = (1,2))
        self.grid.Add(self.txtPWR, pos = (1,2), flag = wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border = 0)
        self.grid.Add(self.txtWVL, pos = (2,2), flag = wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border = 0)

        self.StaticBoxSizer.Add(self.grid, 0, wx.ALL|wx.LEFT, 0)
        self.SetSizerAndFit(self.StaticBoxSizer)

    def SetLabel(self, text):
        self.StaticBox.SetLabel(str(text))

    def SetChannelId(self, id):
        self.On.SetId(id+1)
        self.Off.SetId(id)

    def SetBind(self, handler):
        self.Bind(wx.EVT_BUTTON, handler, self.On)
        self.Bind(wx.EVT_BUTTON, handler, self.Off)

    def SetLed(self, colour):
        self.Led.SetState(colour)

    def Configure(self, text, id, handler, LedStatus = 0, txtPWR = "", txtWVL = ""):
        self.SetLabel(text)
        self.SetChannelId(id)
        self.SetBind(handler)
        self.Led.SetState(LedStatus)
        self.txtPWR.SetValue(str(txtPWR))
        self.txtWVL.SetValue(str(txtWVL))
        

    def Update(self, LedStatus, txtPWR, txtWVL):
        self.Led.SetState(LedStatus)
        self.txtPWR.SetValue(str(txtPWR))
        self.txtWVL.SetValue(str(txtWVL))

    def GetValues(self):
        PWR = self.txtPWR.GetValue()
        WVL = self.txtWVL.GetValue()
        return PWR, WVL

