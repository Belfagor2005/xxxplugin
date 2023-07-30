#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
*        coded by Lululla & PCD        *
*             skin by MMark            *
*             26/03/2023               *
*       Skin by MMark                  *
****************************************
# --------------------#
# Info http://t.me/tivustream
'''
from __future__ import print_function
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Label import Label
from Components.MultiContent import MultiContentEntryPixmapAlphaTest
from Components.MultiContent import MultiContentEntryText
from Components.Pixmap import Pixmap
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import SCOPE_PLUGINS
from Tools.Directories import resolveFilename
from enigma import RT_HALIGN_LEFT, RT_VALIGN_CENTER
from enigma import eTimer
from enigma import loadPNG
from os.path import exists as file_exists
import os
import re
import six
import ssl
import sys
from Plugins.Extensions.xxxplugin.plugin import rvList, Playstream1, returnIMDB
from Plugins.Extensions.xxxplugin.lib import Utils
from Plugins.Extensions.xxxplugin.lib import html_conv
from Plugins.Extensions.xxxplugin import _, skin_path, screenwidth
PY3 = sys.version_info.major >= 3
print('Py3: ', PY3)

try:
    import http.cookiejar as cookielib
    from urllib.parse import urlencode
    from urllib.parse import quote
    from urllib.parse import urlparse
    from urllib.request import Request
    from urllib.request import urlopen
    from urllib import request as urllib2
    PY3 = True
    unicode = str
    unichr = chr
    long = int
    xrange = range
except:
    import cookielib
    from urllib import urlencode
    from urllib import quote
    from urlparse import urlparse
    from urllib2 import Request
    from urllib2 import urlopen

if sys.version_info >= (2, 7, 9):
    try:
        sslContext = ssl._create_unverified_context()
    except:
        sslContext = None

currversion = '1.0'
title_plug = 'Hypnotube '
desc_plugin = ('..:: hypnotube by Lululla %s ::.. ' % currversion)
PLUGIN_PATH = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('xxxplugin'))
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
print(current)
print(parent)
pluglogo = os.path.join(PLUGIN_PATH, 'pic/hypnotube.png')
stripurl = "https://hypnotube.com/channels/"
_session = None
Path_Movies = '/tmp/'
global search
search = False


def show_(name, link):
    res = [(name, link)]
    if screenwidth.width() == 2560:
        res.append(MultiContentEntryText(pos=(0, 0), size=(1200, 50), font=0, text=name, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    elif screenwidth.width() == 1920:
        res.append(MultiContentEntryText(pos=(0, 0), size=(1000, 50), font=0, text=name, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryText(pos=(0, 0), size=(500, 50), font=0, text=name, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    return res


def cat_(letter, link):
    res = [(letter, link)]
    if screenwidth.width() == 2560:
        res.append(MultiContentEntryText(pos=(0, 0), size=(1200, 50), font=0, text=letter, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    elif screenwidth.width() == 1920:
        res.append(MultiContentEntryText(pos=(0, 0), size=(1000, 50), font=0, text=letter, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryText(pos=(0, 0), size=(500, 50), font=0, text=letter, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    return res


def rvoneListEntry(name):

    res = [name]
    pngx = os.path.join(PLUGIN_PATH, 'res/pics/key_yellow.png')
    if screenwidth.width() == 2560:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 5), size=(50, 50), png=loadPNG(pngx)))
        res.append(MultiContentEntryText(pos=(90, 0), size=(1200, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    elif screenwidth.width() == 1920:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 5), size=(40, 40), png=loadPNG(pngx)))
        res.append(MultiContentEntryText(pos=(70, 0), size=(1000, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(3, 10), size=(40, 40), png=loadPNG(pngx)))
        res.append(MultiContentEntryText(pos=(50, 0), size=(500, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    return res


def showlist(data, list):
    icount = 0
    plist = []
    for line in data:
        name = data[icount]
        plist.append(rvoneListEntry(name))
        icount = icount+1
        list.setList(plist)


Panel_list = [
    ("SEARCH"),
    ("HYPNOTUBE"),
    ]


class main(Screen):
    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'defaultListScreen.xml')
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.menulist = []
        self['menulist'] = rvList([])
        self['red'] = Label(_('Back'))
        # self['green'] = Label(_('Export'))
        self['title'] = Label('+18')
        self['name'] = Label('')
        self['text'] = Label('Only for Adult by Lululla')
        self['poster'] = Pixmap()
        self.currentList = 'menulist'
        self.loading_ok = False
        self.count = 0
        self.loading = 0
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'DirectionActions',
                                     'MovieSelectionActions'], {'up': self.up,
                                                                'down': self.down,
                                                                'left': self.left,
                                                                'right': self.right,
                                                                'ok': self.ok,
                                                                'green': self.ok,
                                                                'cancel': self.exit,
                                                                'red': self.exit}, -1)
        self.onLayoutFinish.append(self.updateMenuList)

    def updateMenuList(self):
        self.menu_list = []
        for x in self.menu_list:
            del self.menu_list[0]
        list = []
        idx = 0
        for x in Panel_list:
            list.append(rvoneListEntry(x))
            self.menu_list.append(x)
            idx += 1
        self['menulist'].setList(list)
        auswahl = self['menulist'].getCurrent()[0]
        print('auswahl: ', auswahl)

        self['name'].setText(str(auswahl))

    def search_text(self, name, url):
        from Screens.VirtualKeyBoard import VirtualKeyBoard
        self.namex = name
        self.urlx = url
        self.session.openWithCallback(self.filterChannels, VirtualKeyBoard, title=_("Filter this category..."), text='')

    def filterChannels(self, result):
        if result:
            global search
            name = str(result)
            url = self.urlx + name + '/'
            try:
                search = True
                self.session.open(hypnotubex, name, url)
            except:
                return
        else:
            self.resetSearch()

    def resetSearch(self):
        global search
        search = False
        return

    def ok(self):
        self.keyNumberGlobalCB(self['menulist'].getSelectedIndex())

    def keyNumberGlobalCB(self, idx):
        global namex, lnk
        namex = ''
        # lnk = b64decoder(stripurl)
        # if six.PY3:
            # url = six.ensure_str(lnk)
        sel = self.menu_list[idx]
        if sel == ("SEARCH"):
            lnk = ("https://hypnotube.com/search/")
            # lnk = ("https://www.hypnotube.com/video/search?q=")
        elif sel == ("HYPNOTUBE"):
            lnk = (stripurl)
        namex = sel.upper()
        if sel == 'SEARCH':
            self.search_text(namex, lnk)
        else:
            self.session.open(hypnotube1, namex, lnk)

    def up(self):
        self[self.currentList].up()
        auswahl = self['menulist'].getCurrent()[0]
        self['name'].setText(str(auswahl))

    def down(self):
        self[self.currentList].down()
        auswahl = self['menulist'].getCurrent()[0]
        self['name'].setText(str(auswahl))

    def left(self):
        self[self.currentList].pageUp()
        auswahl = self['menulist'].getCurrent()[0]
        self['name'].setText(str(auswahl))

    def right(self):
        self[self.currentList].pageDown()
        auswahl = self['menulist'].getCurrent()[0]
        self['name'].setText(str(auswahl))

    def exit(self):
        global search
        if search is True:
            search = False
            self.updateMenuList()
        else:
            self.close()


class hypnotubex(Screen):
    def __init__(self, session, name, url):
        self.session = session
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'defaultListScreen.xml')
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.menulist = []
        self['menulist'] = rvList([])
        self['red'] = Label(_('Back'))
        self['title'] = Label('+18')
        self['name'] = Label('')
        self['poster'] = Pixmap()
        self['text'] = Label('Only for Adult by Lululla')
        self.currentList = 'menulist'
        self.loading_ok = False
        self.count = 0
        self.loading = 0
        self.name = name
        self.url = url
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions'], {'ok': self.ok,
                                                       'cancel': self.exit,
                                                       'red': self.exit}, -1)
        self.timer = eTimer()
        if Utils.DreamOS():
            self.timer_conn = self.timer.timeout.connect(self._gotPageLoad)
        else:
            self.timer.callback.append(self._gotPageLoad)
        self.timer.start(500, True)

    def _gotPageLoad(self):
        self.names = []
        self.urls = []
        url = self.url
        try:
            pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            for page in pages:
                url1 = url + "page" + str(page) + ".html"
                name = "Page " + str(page)
                page += 1
                self.urls.append(url1)
                self.names.append(name)
            self['name'].setText(_('Please select ...'))
            showlist(self.names, self['menulist'])
        except Exception as e:
            print(e)
            self['name'].setText(_('Nothing ... Retry'))

    def ok(self):
        i = len(self.names)
        print('iiiiii= ', i)
        if i < 0:
            return
        idx = self["menulist"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        self.session.open(hypnotube2, name, url)

    def exit(self):
        global search
        search = False
        self.close()


class hypnotube1(Screen):
    def __init__(self, session, name, url):
        self.session = session
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'defaultListScreen.xml')
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.menulist = []
        self['menulist'] = rvList([])
        self['red'] = Label(_('Back'))
        # self['green'] = Label(_('Export'))
        self['title'] = Label('+18')
        self['name'] = Label('')
        self['text'] = Label('Only for Adult by Lululla')
        self['poster'] = Pixmap()
        self.name = name
        self.url = url
        self.currentList = 'menulist'
        self.loading_ok = False
        self.count = 0
        self.loading = 0
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'DirectionActions',
                                     'MovieSelectionActions'], {'up': self.up,
                                                                'down': self.down,
                                                                'left': self.left,
                                                                'right': self.right,
                                                                'ok': self.ok,
                                                                # 'green': self.message2,
                                                                'cancel': self.exit,
                                                                'red': self.exit}, -1)
        self.timer = eTimer()
        if Utils.DreamOS():
            self.timer_conn = self.timer.timeout.connect(self.cat)
        else:
            self.timer.callback.append(self.cat)
        self.timer.start(500, True)

    def up(self):
        self[self.currentList].up()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))

    def down(self):
        self[self.currentList].down()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))

    def left(self):
        self[self.currentList].pageUp()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))

    def right(self):
        self[self.currentList].pageDown()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))

    def cat(self):
        self.cat_list = []
        try:
            content = Utils.getUrl(self.url)
            if six.PY3:
                content = six.ensure_str(content)
            regexcat = 'li><a title=\'(.*?)\' href=\'(.*?)\''
            match = re.compile(regexcat, re.DOTALL).findall(content)
            for name, url in match:
                url1 = str(url)
                self.cat_list.append(show_(name, url1))
            if len(self.cat_list) < 0:
                return
            else:
                self['menulist'].l.setList(self.cat_list)
                self['menulist'].moveToIndex(0)
                auswahl = self['menulist'].getCurrent()[0][0]
                self['name'].setText(str(auswahl))
        except Exception as e:
            print(e)

    def ok(self):
        name = self['menulist'].getCurrent()[0]
        url = self['menulist'].getCurrent()[0][1]
        self.play_that_shit(url, name)

    def play_that_shit(self, url, name):
        self.session.open(hypnotubex, name, url)

    def exit(self):
        self.close()


class hypnotube2(Screen):
    def __init__(self, session, name, url):
        self.session = session
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'defaultListScreen.xml')
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.menulist = []
        self['menulist'] = rvList([])
        self['red'] = Label(_('Back'))
        # self['green'] = Label(_('Export'))
        self['title'] = Label('+18')
        self['name'] = Label('')
        self['poster'] = Pixmap()
        self['text'] = Label('Only for Adult by Lululla')
        self.currentList = 'menulist'
        self.loading_ok = False
        self.count = 0
        self.loading = 0
        self.name = name
        self.url = url
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'DirectionActions',
                                     'MovieSelectionActions'], {'up': self.up,
                                                                'down': self.down,
                                                                'left': self.left,
                                                                'right': self.right,
                                                                'ok': self.ok,
                                                                # 'green': self.message2,
                                                                'cancel': self.exit,
                                                                'red': self.exit}, -1)
        self.timer = eTimer()
        if Utils.DreamOS():
            self.timer_conn = self.timer.timeout.connect(self.cat)
        else:
            self.timer.callback.append(self.cat)
        self.timer.start(500, True)

    def up(self):
        self[self.currentList].up()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))

    def down(self):
        self[self.currentList].down()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))

    def left(self):
        self[self.currentList].pageUp()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))

    def right(self):
        self[self.currentList].pageDown()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))

    def cat(self):
        self.cat_list = []
        try:
            content = Utils.getUrl(self.url)
            if six.PY3:
                content = six.ensure_str(content)
            print("content A =", content)
            regexcat = '<div class="item-col col ".*?<a href="(.*?)" title="(.*?)"'  # .*?img data.*?src="(.*?)"'
            match = re.compile(regexcat, re.DOTALL).findall(content)
            for url, name in match:
                name = name.replace('"', '')
                self.cat_list.append(show_(name, url))
            if len(self.cat_list) < 0:
                return
            else:
                self['menulist'].l.setList(self.cat_list)
                self['menulist'].moveToIndex(0)
                auswahl = self['menulist'].getCurrent()[0][0]
                self['name'].setText(str(auswahl))
        except Exception as e:
            print(e)

    def ok(self):
        name = self['menulist'].getCurrent()[0][0]
        url = self['menulist'].getCurrent()[0][1]
        self.play_that_shit(url, name)

    def play_that_shit(self, url, name):
        self.session.open(hypnotube3, name, url)

    def exit(self):
        self.close()


class hypnotube3(Screen):
    def __init__(self, session, name, url):
        self.session = session
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'defaultListScreen.xml')
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.menulist = []
        self['menulist'] = rvList([])
        self['red'] = Label(_('Back'))
        # self['green'] = Label(_('Export'))
        self['title'] = Label('+18')
        self['name'] = Label('')
        self['text'] = Label('Only for Adult by Lululla')
        self['poster'] = Pixmap()
        self.name = name
        self.url = url
        self.currentList = 'menulist'
        self.loading_ok = False
        self.count = 0
        self.loading = 0
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'DirectionActions',
                                     'MovieSelectionActions'], {'up': self.up,
                                                                'down': self.down,
                                                                'left': self.left,
                                                                'right': self.right,
                                                                'ok': self.ok,
                                                                # 'green': self.message2,
                                                                'cancel': self.exit,
                                                                'red': self.exit}, -1)
        self.timer = eTimer()
        if Utils.DreamOS():
            self.timer_conn = self.timer.timeout.connect(self.cat)
        else:
            self.timer.callback.append(self.cat)
        self.timer.start(500, True)

    def up(self):
        self[self.currentList].up()
        auswahl = self['menulist'].getCurrent()[0]
        self['name'].setText(str(auswahl))

    def down(self):
        self[self.currentList].down()
        auswahl = self['menulist'].getCurrent()[0]
        self['name'].setText(str(auswahl))

    def left(self):
        self[self.currentList].pageUp()
        auswahl = self['menulist'].getCurrent()[0]
        self['name'].setText(str(auswahl))

    def right(self):
        self[self.currentList].pageDown()
        auswahl = self['menulist'].getCurrent()[0]
        self['name'].setText(str(auswahl))

    def cat(self):
        self.cat_list = []
        try:
            content = Utils.getUrl(self.url)
            if six.PY3:
                content = six.ensure_str(content)
            regexcat = '<source src="(.*?)".*?label=(.*?) res='
            match = re.compile(regexcat, re.DOTALL).findall(content)
            for url, name in match:
                url = url.replace('"', '')
                name = name.replace("'", "")
                name = str(self.name) + ' ' + str(name)
                self.cat_list.append(show_(name, url))
            if len(self.cat_list) < 0:
                return
            else:
                self['menulist'].l.setList(self.cat_list)
                self['menulist'].moveToIndex(0)
                auswahl = self['menulist'].getCurrent()[0][0]
                self['name'].setText(str(auswahl))
        except Exception as e:
            print(e)

    def ok(self):
        name = self['menulist'].getCurrent()[0][0]
        url = self['menulist'].getCurrent()[0][1]
        self.play_that_shit(url, name)

    def play_that_shit(self, url, name):
        self.session.open(Playstream1, str(name), str(url))

    def exit(self):
        self.close()
