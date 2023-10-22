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
from Components.Label import Label
from Components.Pixmap import Pixmap
from Screens.Screen import Screen
from Tools.Directories import SCOPE_PLUGINS
from Tools.Directories import resolveFilename
from enigma import eTimer
import codecs
import json
import os
import re
import six
import ssl
import sys
from Plugins.Extensions.xxxplugin.plugin import rvList, Playstream1
from Plugins.Extensions.xxxplugin.plugin import showlist
from Plugins.Extensions.xxxplugin.plugin import show_
from Plugins.Extensions.xxxplugin.lib import Utils
from Plugins.Extensions.xxxplugin import _, skin_path
PY3 = sys.version_info.major >= 3

if sys.version_info >= (2, 7, 9):
    try:
        sslContext = ssl._create_unverified_context()
    except:
        sslContext = None

currversion = '1.0'
title_plug = 'empflix2 '
desc_plugin = ('..:: empflix by Lululla %s ::.. ' % currversion)
PLUGIN_PATH = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('xxxplugin'))
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
print(current)
print(parent)
pluglogo = os.path.join(PLUGIN_PATH, 'pic/empflix.png')
referer = 'https://www.empflix.com/'
stripurl = 'https://www.empflix.com/categories'
_session = None
Path_Movies = '/tmp/'


if PY3:
    PY3 = True
    unicode = str
else:
    str = str
class main(Screen):
    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'defaultListScreen.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
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
        self.timer = eTimer()
        if Utils.DreamOS():
            self.timer_conn = self.timer.timeout.connect(self.updateMenuList)
        else:
            self.timer.callback.append(self.updateMenuList)
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

    def updateMenuList(self):
        self.cat_list = []
        try:
            url = stripurl
            content = Utils.getUrl2(url, referer)
            if six.PY3:
                content = six.ensure_str(content)
            regexcat = r'class="col-6.+?href="([^"]+)">\s*<img.+?src="([^"]+).+?title">([^<]+)'
            match = re.compile(regexcat, re.DOTALL).findall(content)
            for url, pic, name in match:
                url1 = url
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
        name = self['menulist'].getCurrent()[0][0]
        url = self['menulist'].getCurrent()[0][1]
        self.play_that_shit(url, name)

    def play_that_shit(self, url, name):
        self.session.open(empflix3, name, url)

    def exit(self):
        self.close()


class empflix3(Screen):
    def __init__(self, session, name, url):
        self.session = session
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'defaultListScreen.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
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
                                                                'green': self.ok,
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
            content = Utils.getUrl2(self.url, referer)
            if six.PY3:
                content = six.ensure_str(content)
            regexcat = r'data-vid="([^"]+).+?src="([^"]+)"\s*alt="([^"]+).+?tion">([^<]+)'
            match = re.compile(regexcat, re.DOTALL).findall(content)
            for url, pic, name, tmp in match:
                name = name + '( ' + tmp + ' )'
                url1 = 'https://player.empflix.com/ajax/video-player/' + url
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
        try:
            name = self['menulist'].getCurrent()[0][0]
            url = self['menulist'].getCurrent()[0][1]
            self.play_that_shit(url, name)
        except Exception as e:
            print(e)

    def play_that_shit(self, url, name):
        if 'https://www.empflix.com/' in url:
            self.session.open(empflix5, str(name), str(url))
        else:
            self.session.open(empflix5, str(name), str(url))

    def exit(self):
        global search
        search = False
        self.close()


class empflix4(Screen):
    def __init__(self, session, name, url):
        self.session = session
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'defaultListScreen.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
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
            pages = 100
            i = 1
            while i < pages:
                url1 = url + str(i)
                name = "Page " + str(i)
                i += 1
                self.urls.append(url1)
                self.names.append(name)
            self['name'].setText(_('Please select ...'))
            showlist(self.names, self['menulist'])
        except Exception as e:
            print(e)
            self['name'].setText(_('Nothing ... Retry'))

    def ok(self):
        i = len(self.names)
        if i < 0:
            return
        idx = self["menulist"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]
        self.session.open(empflix5, name, url)

    def exit(self):
        global search
        search = False
        self.close()


class empflix5(Screen):
    def __init__(self, session, name, url):
        self.session = session
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'defaultListScreen.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
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
                                                                'green': self.ok,
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
            content2 = json.loads(content).get('html')
            match = re.compile(r'source\s*src="([^"]+)').findall(content2)
            url1 = (match[0] + '|Referer=https://www.empflix.com/')
            self.cat_list.append(show_(self.name, url1))
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
        try:
            name = self['menulist'].getCurrent()[0][0]
            url = self['menulist'].getCurrent()[0][1]
            self.play_that_shit(url, name)
        except Exception as e:
            print(e)

    def play_that_shit(self, url, name):
        self.session.open(Playstream1, str(name), str(url))

    def exit(self):
        self.close()
