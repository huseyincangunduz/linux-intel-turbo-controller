#! /usr/bin/python3
import subprocess
from ast import Str
from asyncore import read
from operator import eq
import os
from xmlrpc.client import Boolean
from numpy import void
import wx
import wx.adv
import sys


def is_root():
    return os.geteuid() == 0


def getPrivileges():
    if (not is_root()):
        environment = os.environ.copy()

        tala = subprocess.run(['pkexec', sys.executable] +
                              [sys.argv[0]], env=environment)
        if (tala.returncode != 1):
            wx.MessageBox("Doğrulama başarısız")
        exit()


def ReadFile(path: str) -> str:
    f = open(path, "r")
    return f.read()


def TurboIsOpen() -> Boolean:
    content: str = ReadFile("/sys/devices/system/cpu/intel_pstate/no_turbo")
    return eq(content.strip(), "0")


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


def GetAdminPrivileges():
    wx.MessageBox("Ver yetkiyi gör etkiyi, okuma dışındaki bir çok işlem için admin yetkisi gerekiyor, sorry. şimdi btci ile muhattap olmak zorundasın... çok yazık 👨‍❤‍💋‍👨")
    # args = ['sudo', sys.executable] + sys.argv + [os.environ]
    # os.execlpe('sudo', *args)


def SetTurboState(state: Boolean) -> void:
    if (not is_root()):
        GetAdminPrivileges()
        # return
    file = open("/sys/devices/system/cpu/intel_pstate/no_turbo", "r+")
    print("Şu anki durum: " + file.read())
    file.truncate()
    if state:
        file.write("0")
    else:
        file.write("1")
    file.close()


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self):
        super(TaskBarIcon, self).__init__()
        self.set_icon()
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.toggle_turbo)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Turbo aç', self.enable_turbo)
        create_menu_item(menu, 'Turbo kapat', self.disable_turbo)
        menu.AppendSeparator()
        create_menu_item(menu, 'Çıkış', self.on_exit)
        return menu

    def enable_turbo(self, event):
        SetTurboState(True)
        self.set_icon()

    def disable_turbo(self, event):
        SetTurboState(False)
        self.set_icon()

    def toggle_turbo(self, event):
        SetTurboState(not TurboIsOpen())
        self.set_icon()

    def set_icon(self):
        turboIkon = "./closed.png"
        if (TurboIsOpen()):
            turboIkon = "./open.png"

        icon = wx.Icon(wx.Bitmap(turboIkon))
        self.SetIcon(icon, "Turbocu")

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        exit()


class App(wx.App):
    def OnInit(self):
        getPrivileges()
        frame = wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon()
        return True


app = App()
# app.MainLoop()
# SetTurboState(True)
# print(TurboIsOpen())
app.MainLoop()
