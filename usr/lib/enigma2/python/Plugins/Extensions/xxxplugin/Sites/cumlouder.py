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
import os
import re
import six
import ssl
import sys
import unicodedata
from Plugins.Extensions.xxxplugin.plugin import rvList, Playstream1
from Plugins.Extensions.xxxplugin.plugin import showlist, rvoneListEntry
from Plugins.Extensions.xxxplugin.plugin import show_
from Plugins.Extensions.xxxplugin.lib import Utils
from Plugins.Extensions.xxxplugin.lib import html_conv
from Plugins.Extensions.xxxplugin import _, skin_path
PY3 = sys.version_info.major >= 3
print('Py3: ', PY3)


if sys.version_info >= (2, 7, 9):
    try:
        sslContext = ssl._create_unverified_context()
    except:
        sslContext = None

currversion = '1.0'
title_plug = 'Cumlouder '
desc_plugin = ('..:: Cumlouder by Lululla %s ::.. ' % currversion)
PLUGIN_PATH = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('xxxplugin'))
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
print(current)
print(parent)
pluglogo = os.path.join(PLUGIN_PATH, 'pic/cumlouder.png')
stripurl = 'aHR0cHM6Ly93d3cuY3VtbG91ZGVyLmNvbQ'
_session = None
Path_Movies = '/tmp/'
global search
search = False


if PY3:
    PY3 = True
    unicode = str
else:
    str = str


def normalize(title):
    try:
        try:
            return title.decode('ascii').encode("utf-8")
        except:
            pass

        return str(''.join(c for c in unicodedata.normalize('NFKD', unicode(title.decode('utf-8'))) if unicodedata.category(c) != 'Mn'))
    except:
        return html_conv.html_unescape(title)


Panel_list = [
    ('Cumlouder Girls'),
    ('Cumlouder Channels'),
    ('Cumlouder More Videos'),
    ('Cumlouder Categories'),
    ('SEARCH'),
    ]


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
        self['name'].setText(str(auswahl))

    def search_text(self, name, url):
        from Screens.VirtualKeyBoard import VirtualKeyBoard
        self.namex = name
        self.urlx = url
        self.session.openWithCallback(self.filterChannels,
                                      VirtualKeyBoard, title=_(
                                       "Filter this category..."
                                      ), text='')

    def filterChannels(self, result):
        if result:
            global search
            name = str(result)
            url = self.urlx + str(result) + '/'
            try:
                search = True
                self.session.open(cumlouder5, name, url)
            except:
                return
        else:
            self.resetSearch()

    def resetSearch(self):
        global search
        search = False

    def ok(self):
        self.keyNumberGlobalCB(self['menulist'].getSelectedIndex())

    def keyNumberGlobalCB(self, idx):
        global namex, lnk
        namex = ''
        sel = self.menu_list[idx]
        if sel == 'SEARCH':
            namex = sel.upper()
            lnk = 'https://www.cumlouder.com/search/?q='
            self.search_text(namex, lnk)
        if sel == ("Cumlouder Girls"):
            namex = "girls"
            lnk = 'https://www.cumlouder.com/girls/'
            self.session.open(cumlouder, namex, lnk)

        elif sel == ("Cumlouder Categories"):
            namex = "categories"
            lnk = 'https://www.cumlouder.com/categories/'
            self.session.open(cumlouder, namex, lnk)

        elif sel == ("Cumlouder Channels"):
            namex = "channels"
            lnk = 'https://www.cumlouder.com/channels/videos/'
            self.session.open(cumlouder2, namex, lnk)
        elif sel == ("Cumlouder More Videos"):
            namex = "videos"
            lnk = 'https://www.cumlouder.com/porn/'
            self.session.open(cumlouder2, namex, lnk)

        else:
            return

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


class cumlouder5(Screen):
    def __init__(self, session, name, url):
        self.session = session
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'defaultListScreen.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.menulist = []
        self.loading_ok = False
        self.count = 0
        self.loading = 0
        self['menulist'] = rvList([])
        self['red'] = Label(_('Back'))
        # self['green'] = Label(_('Export'))
        self['title'] = Label('+18')
        self['name'] = Label('')
        self['poster'] = Pixmap()
        self['text'] = Label('Only for Adult by Lululla')
        self.name = name
        self.url = url
        self.currentList = 'menulist'
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'DirectionActions',
                                     'MovieSelectionActions'], {'cancel': self.exit,
                                                                'ok': self.ok,
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
        try:
            pages = 100
            i = 1
            while i < pages:
                page = str(i)
                if "search" in self.url.lower():
                    pp = str(page) + "?"
                else:
                    pp = str(page) + "/?"
                url1 = self.url.replace("?", pp)
                name = "Page " + page
                i += 1
                self.names.append(name)
                self.urls.append(url1)
            self['name'].setText(_('Please select ...'))
            showlist(self.names, self['menulist'])
        except Exception as e:
            print(e)
            self['name'].setText(_('Nothing ... Retry'))

    def ok(self):
        name = self['menulist'].getCurrent()[0][0]
        url = self['menulist'].getCurrent()[0][1]
        self.play_that_shit(url, name)

    def play_that_shit(self, name, url):
        self.session.open(cumlouder3, name, url)

    def exit(self):
        self.close()


class cumlouder(Screen):
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
                                                                'green': self.ok,
                                                                'cancel': self.exit,
                                                                'red': self.exit}, -1)
        self.timer = eTimer()
        if Utils.DreamOS():
            self.timer_conn = self.timer.timeout.connect(self.cat)
        else:
            self.timer.callback.append(self.cat)
        self.timer.start(600, True)

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

            if "girls" in self.name.lower():
                regexcat = 'a girl-url="(.*?)".*?href="(.*?)".*?data-src="(.*?)"'
            else:
                regexcat = 'a tag-url="(.*?)".*?href="(.*?)".*?data-src="(.*?)"'

            match = re.compile(regexcat, re.DOTALL).findall(content)
            for name, url, pic in match:
                name = normalize(name)
                name = html_conv.html_unescape(name)
                url = "https://www.cumlouder.com" + str(url)
                pic = pic
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
        try:
            name = self['menulist'].getCurrent()[0][0]
            url = self['menulist'].getCurrent()[0][1]
            self.play_that_shit(url, name)
        except Exception as e:
            print(e)

    def play_that_shit(self, url, name):
        self.session.open(cumlouder2, str(name), str(url))

    def exit(self):
        self.close()


class cumlouder2(Screen):
    def __init__(self, session, name, url):
        self.session = session
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'defaultListScreen.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.menulist = []
        self.loading_ok = False
        self.count = 0
        self.loading = 0
        self.name = name
        self.url = url
        self['menulist'] = rvList([])
        self['red'] = Label(_('Back'))
        self['title'] = Label('+18')
        self['name'] = Label('')
        self['poster'] = Pixmap()
        self['text'] = Label('Only for Adult by Lululla')
        self.currentList = 'menulist'
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
        try:
            pages = 100
            i = 1
            while i < pages:
                page = str(i)
                url1 = self.url + page
                name = "Page " + page
                i += 1
                self.names.append(name)
                self.urls.append(url1)
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
        self.session.open(cumlouder3, name, url)

    def exit(self):
        global search
        search = False
        self.close()


class cumlouder3(Screen):
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
                                                                'green': self.ok,
                                                                'cancel': self.exit,
                                                                'red': self.exit}, -1)
        self.timer = eTimer()
        if Utils.DreamOS():
            self.timer_conn = self.timer.timeout.connect(self.cat)
        else:
            self.timer.callback.append(self.cat)
        self.timer.start(600, True)

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
            regexcat = 'a class="muestra-escena" href="(.*?)".*?data-src="(.*?)".*?alt="(.*?)"'
            match = re.compile(regexcat, re.DOTALL).findall(content)
            for url, pic, name in match:
                name = name
                url = "https://www.cumlouder.com" + url
                pic = pic
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
        try:
            name = self['menulist'].getCurrent()[0][0]
            url = self['menulist'].getCurrent()[0][1]
            self.play_that_shit(url, name)
        except Exception as e:
            print(e)

    def play_that_shit(self, url, name):
        self.session.open(cumlouder4, str(name), str(url))

    def exit(self):
        global search
        search = False
        self.close()


class cumlouder4(Screen):
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
                                                                'green': self.ok,
                                                                'cancel': self.exit,
                                                                'red': self.exit}, -1)
        self.timer = eTimer()
        if Utils.DreamOS():
            self.timer_conn = self.timer.timeout.connect(self.cat)
        else:
            self.timer.callback.append(self.cat)
        self.timer.start(600, True)

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
            regexcat = 'source src="(.*?)"'
            match = re.compile(regexcat, re.DOTALL).findall(content)

            url = match[0]
            url = url.replace("&amp;", "&")
            name = self.name
            # for url, name in match:
                # name = name
                # url = "https://www.hd-easyporn.com" + url
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
        try:
            name = self['menulist'].getCurrent()[0][0]
            url = self['menulist'].getCurrent()[0][1]
            self.play_that_shit(url, name)
        except Exception as e:
            print(e)

    def play_that_shit(self, url, name):
        self.session.open(Playstream1, str(name), str(url))

    def exit(self):
        global search
        search = False
        self.close()
