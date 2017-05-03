# -*- coding: cp1252 -*-
import os
import sys
import shutil
import win32con
import threading

import wx

from time     import sleep, time

from LED      import LED
from LogFile  import logfile

from ILX import *
from ChannelFrame import *

class Frame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title,
                          style = wx.CAPTION|wx.MINIMIZE_BOX|wx.CLOSE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL)

        ##Start ILX (channel 14)
        self.ILX = ILX_Lightwave("GPIB0::14::INSTR")
        self._programmed = self.ILX.programmed()

        ##Main panel
        self.p = wx.Panel(self, wx.ID_ANY)

        ##Creating sizer
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.p.grid = wx.GridBagSizer(hgap = 0, vgap = 0)

        ## Channels
        self.channels = []
        for i in xrange(8):
            ## ChannelFrames
            self.p.ch = ChannelFrame(self.p)
            self.p.ch.Configure("Channel {}".format(1+i), 10000 + 10*(1+i), self.SetOnOff)
            self.channels.append(self.p.ch)
            self.p.grid.Add(self.p.ch, pos = (i // 4,i % 4), flag = wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border = 5)
            ## Hotkeys
            try:
                self.RegisterHotKey(hotkeyId = 10000 + 10*(1+i), modifiers = win32con.MOD_CONTROL, keycode = win32con.VK_F1+i)
                self.RegisterHotKey(hotkeyId = 10001 + 10*(1+i), modifiers = 0,                    keycode = win32con.VK_F1+i)
            except:
                self.RegisterHotKey(hotkeyId = 10000 + 10*(1+i), modifiers = win32con.MOD_CONTROL, virtualKeyCode = win32con.VK_F1+i)
                self.RegisterHotKey(hotkeyId = 10001 + 10*(1+i), modifiers = 0,                    virtualKeyCode = win32con.VK_F1+i)
            self.Bind(wx.EVT_HOTKEY, self.SetOnOff, id=10000 + 10*(1+i))
            self.Bind(wx.EVT_HOTKEY, self.SetOnOff, id=10001 + 10*(1+i))

        ##Button
        self.p.buttonUpdateChanges = wx.Button(self.p, label = "&Update Changes", size = (150,22))
        self.p.grid.Add(self.p.buttonUpdateChanges, pos = (2,3), flag = wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, border = 0)
        self.p.Bind(wx.EVT_BUTTON, self.SetUpdate, self.p.buttonUpdateChanges)

        ##Setting main sizers
        self.sizer.Add(self.p, 1, wx.EXPAND | wx.ALL, 0)

        ##Setting sizer
        self.p.SetSizerAndFit(self.p.grid)
        self.SetSizerAndFit(self.sizer)

        ##Update Values
        self.GetUpdate()

        ##Show
        self.Centre()
        self.Show(True)


    def SetLocal(self):
        self.ILX.set_local()


    def SetOnOff(self, event):
        if self._programmed:
            buttonId = event.GetId() - 10000
            statusOnOff = buttonId % 10
            channel = buttonId // 10
            self.ILX.set_status(statusOnOff, channel)
            self.Update(channel)
            self.SetLocal()


    def Update(self, channel):
        if self._programmed:
            if self.ILX.get_status(channel) == "ON":
                ledstatus  = 2
            else:
                ledstatus  = 0
            power      = self.ILX.get_power(channel)
            wavelength = self.ILX.get_wavelength(channel)

            self.channels[channel-1].Update(ledstatus, power, wavelength)
            self.SetLocal()


    def GetUpdate(self):
        if self._programmed:
            for i, j in enumerate(self.channels):
                if self.ILX.get_status(i+1) == "ON":
                    ledstatus  = 2
                else:
                    ledstatus  = 0
                power      = self.ILX.get_power(i+1)
                wavelength = self.ILX.get_wavelength(i+1)

                j.Update(ledstatus, power, wavelength)

            self.SetLocal()


    def SetUpdate(self, event):
        if self._programmed:
            for i, j in enumerate(self.channels):
                PWR, WVL = j.GetValues()

                self.ILX.set_power(float(PWR), i+1)
                self.ILX.set_wavelength(float(WVL), i+1)

            self.SetLocal()


if __name__ == '__main__':
    app = wx.App(False)
    frame = Frame(None, 'Mainframe 1 - ILX Lightwave 7900B System')
    app.MainLoop()

