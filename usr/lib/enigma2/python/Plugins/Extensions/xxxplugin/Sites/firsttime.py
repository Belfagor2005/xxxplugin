#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
*        coded by Lululla & PCD        *
*             skin by MMark            *
*             26/03/2023               *
*       Skin by MMark                  *
****************************************
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
from Plugins.Extensions.xxxplugin.plugin import rvList, Playstream1, Playstream2
from Plugins.Extensions.xxxplugin.plugin import showlist, rvoneListEntry
from Plugins.Extensions.xxxplugin.plugin import show_
from Plugins.Extensions.xxxplugin.lib import Utils
from Plugins.Extensions.xxxplugin.lib import html_conv
from Plugins.Extensions.xxxplugin import _, skin_path
# print("wapbold.py skin_path =", skin_path)
PY3 = sys.version_info.major >= 3
print('Py3: ', PY3)


if sys.version_info >= (2, 7, 9):
    try:
        sslContext = ssl._create_unverified_context()
    except:
        sslContext = None

currversion = '1.0'
title_plug = 'Firsttime'
desc_plugin = ('..:: Firsttime by Lululla %s ::.. ' % currversion)
PLUGIN_PATH = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('xxxplugin'))
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
print(current)
print(parent)
pluglogo = os.path.join(PLUGIN_PATH, 'pic/firsttime.png')
stripurl = 'aHR0cHM6Ly93d3cuZmlyc3RhbmFsdmlkZW9zLmNvbS8'
_session = None
Path_Movies = '/tmp/'
global search
search = False


if PY3:
    PY3 = True
    unicode = str
else:
    str = str


Panel_list = [
    ('Popular'),
    ('Top-Rated'),
    ('Latest'),
    ('Featured-Videos'),
    ('Categories'),
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
        self['title'] = Label('')
        self['title'].setText(title_plug)
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
            # pcd fix
            result = str(result).replace(" ", "+")
            # url = self.urlx + str(result) + '/'
            url = self.urlx + result + '/'
            #
            try:
                search = True
#                print("wapbold.py going in getVideos name = ", name)
#                print("wapbold.py going in getVideos url = ", url)
                self.session.open(getVideos, name, url)
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
        if sel == 'Categories':
            namex = sel.upper()
            lnk = 'https://www.firstanalvideos.com/categories/'
            self.session.open(getCats, namex, lnk)
        if sel == ("Popular"):
            namex = "Popular"
            lnk = 'https://www.firstanalvideos.com/most-popular/'
            self.session.open(getPage, namex, lnk)
        if sel == ("Top-Rated"):
            namex = "Top-Rated"
            lnk = 'https://www.firstanalvideos.com/top-rated/'
            self.session.open(getPage, namex, lnk)
        if sel == ("Latest"):
            namex = "Latest"
            lnk = 'https://www.firstanalvideos.com/latest-updates/'
            self.session.open(getPage, namex, lnk)
        if sel == ("Featured-Videos"):
            namex = "Featured-Videos"
            lnk = 'https://www.firstanalvideos.com/latest-updates/'
            self.session.open(getPage, namex, lnk)

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


class getPage(Screen):
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
        self['title'] = Label('')
        self['title'].setText(title_plug)
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
        self.cat_list = []
        name = self.name
        # url = self.url
        try:
            pages = 60
            i = 1
            while i < pages:
                page = str(i)
                # https://www.firstanalvideos.com/latest-updates/3/
                # print("getPage self.name =", self.name)
                url1 = self.url + str(page) + "/"
                #
                name = "Page " + page
                i += 1
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
            self['name'].setText(_('Nothing ... Retry'))

    def ok(self):
        name = self['menulist'].getCurrent()[0][0]
        url = self['menulist'].getCurrent()[0][1]
        # print("getPage self.url =", self.url)
        # print("getPage url =", url)
        self.session.open(getVideos, name, url)

    def exit(self):
        global search
        search = False
        self.close()


class getVideos(Screen):
    def __init__(self, session, name, url):
        self.session = session
        print("getVideos url 3=", url)
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'defaultListScreen.xml')
        print("getVideos skin =", skin)

        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        print("getVideos self.skin =", self.skin)

        self.menulist = []
        self['menulist'] = rvList([])
        self['red'] = Label(_('Back'))
        # self['green'] = Label(_('Export'))
        self['title'] = Label('')
        self['title'].setText(title_plug)
        self['name'] = Label('')
        self['text'] = Label('Only for Adult by Lululla')
        self['poster'] = Pixmap()
        self.name = name
        self.url = url
        # print("getVideos self.url 2")
        # print("getVideos self.url 1=", self.url)
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
            # print("getVideos self.url =", self.url)
            content = Utils.getUrl(self.url)
            if six.PY3:
                content = six.ensure_str(content)
            # print("getVideos content =", content)
            regexcat = '<div class="list_content">.*?href="(.*?)".*?img src="(.*?)" alt="(.*?)"'
            match = re.compile(regexcat, re.DOTALL).findall(content)
            # print("getVideos match =", match)
            for url, pic, name in match:
                name = name
                url = url
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
            self.playVideo(url, name)
        except Exception as e:
            print(e)

    def playVideo(self, url, name):
        # print("Here in playVideo url 1=", url)
        content = Utils.getUrl(url)
        regexvideo = "video_url: '(.*?)'"
        match = re.compile(regexvideo, re.DOTALL).findall(content)
        # print( "Here in playVideo match 1=", match)
        url1 = match[0]
        self.play(url1)

    def play(self, url):
        name = self.name
        self.session.open(Playstream2, name, url)

    def exit(self):
        self.close()


class getCats(Screen):
    def __init__(self, session, name, url):
        self.session = session
        # print("getCats url 3=", url)
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'defaultListScreen.xml')
#        print("getCats skin =", skin)

        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
#        print("getVideos self.skin =", self.skin)

        self.menulist = []
        self['menulist'] = rvList([])
        self['red'] = Label(_('Back'))
        # self['green'] = Label(_('Export'))
        self['title'] = Label('')
        self['title'].setText(title_plug)
        self['name'] = Label('')
        self['text'] = Label('Only for Adult by Lululla')
        self['poster'] = Pixmap()
        self.name = name
        self.url = url
        # print("getVideos self.url 2")
        # print("getVideos self.url 1=", self.url)
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
            # print("getVideos self.url =", self.url)
            content = Utils.getUrl(self.url)
            if six.PY3:
                content = six.ensure_str(content)
            # print("getVideos content =", content)
            regexcat = '<div class="list_content">.*?href="(.*?)".*?img src="(.*?)".*?alt="(.*?)"'
            match = re.compile(regexcat, re.DOTALL).findall(content)
            # print("getVideos match =", match)
            for url, pic, name in match:
                if "picture" in name.lower():
                    continue
                else:
                    name = name
                    url = url
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
            self.session.open(getPage, name, url)
        except Exception as e:
            print(e)


    def exit(self):
        self.close()
