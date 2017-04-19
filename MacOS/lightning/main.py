#-*- coding: UTF-8 -*-

import wx
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

import engine


def DefaultUpdate(event):
    engine._DefaultUpdate()

def UpdateAll(event):
    engine._UpdateAll()


def Search(event):
    str = SearchTXT.GetValue()
    if('' == str):
        dlg = wx.MessageBox(message='without input', style=wx.YES|wx.ICON_WARNING)
    else:
        result = engine._Search(''.join(str.split()))
        if({} == result):
            SearchTXT.Clear()
            dlg = wx.MessageBox(message='no result', style=wx.YES | wx.ICON_WARNING)
        else:
            ResultTXT.Clear()
            str = ''
            for i in result:
                str += i
                str += ' ---------------->> '
                for j in result[i]:
                    str = str + j + ' '
                str += '\n'
            ResultTXT.SetValue(str)


app = wx.App()
win = wx.Frame(None,title='Lightning',size=(1000,600))
bkg = wx.Panel(win)

DefaultUpdataBTN = wx.Button(bkg,label='default update')
DefaultUpdataBTN.Bind(wx.EVT_BUTTON,DefaultUpdate)

AllUpdateBTN = wx.Button(bkg,label='update all')
AllUpdateBTN.Bind(wx.EVT_BUTTON,UpdateAll)

SearchBTN = wx.Button(bkg,label='search')
SearchBTN.Bind(wx.EVT_BUTTON,Search)
SearchTXT = wx.TextCtrl(bkg)

ResultTXT = wx.TextCtrl(bkg,style=(wx.TE_MULTILINE | wx.VSCROLL | wx.TE_RICH2 | wx.TE_READONLY))

h_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
h_box_sizer.Add(DefaultUpdataBTN, proportion=1, flag= wx.ALL | wx.ALL, border=2)
h_box_sizer.Add(AllUpdateBTN,proportion=1, flag= wx.ALL, border=2)

h_box_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
h_box_sizer1.Add(SearchTXT,proportion=1, flag=wx.EXPAND | wx.ALL, border=2)
h_box_sizer1.Add(SearchBTN,proportion=0, flag= wx.ALL, border=2)

v_box_sizer = wx.BoxSizer(wx.VERTICAL)
v_box_sizer.Add(h_box_sizer, proportion=0, flag=wx.EXPAND)
v_box_sizer.Add(h_box_sizer1,proportion=0, flag=wx.EXPAND)
v_box_sizer.Add(ResultTXT, proportion=1, flag=wx.EXPAND, border=5)

bkg.SetSizer(v_box_sizer)

engine.init()
win.Show()
app.MainLoop()
