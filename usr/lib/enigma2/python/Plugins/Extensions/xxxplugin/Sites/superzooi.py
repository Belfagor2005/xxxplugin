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
from Tools.Directories import (SCOPE_PLUGINS, resolveFilename)
from enigma import eTimer
import codecs
import os
import re
import six
import ssl
import sys
import unicodedata
from Plugins.Extensions.xxxplugin import (_, skin_path)
from Plugins.Extensions.xxxplugin.lib import (Utils, html_conv)
from Plugins.Extensions.xxxplugin.plugin import (
        rvList,
        Playstream1,
        Playstream2,
        showlist,
        rvoneListEntry,
        show_,
)
PY3 = sys.version_info.major >= 3
print('Py3: ', PY3)
if sys.version_info >= (2, 7, 9):
    try:
        sslContext = ssl._create_unverified_context()
    except:
        sslContext = None

currversion = '1.0'
title_plug = 'superzooi '
desc_plugin = ('..:: superzooi by Lululla %s ::.. ' % currversion)
PLUGIN_PATH = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('xxxplugin'))
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
referer = 'https://www.superzooi.com/'
print(current)
print(parent)
pluglogo = os.path.join(PLUGIN_PATH, 'pic/superzooi.png')
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
 ('CATEGORIES'),  # 5
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
        self['title'] = Label('')
        self['title'].setText(title_plug)
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
            url = self.urlx + str(result)
            try:
                search = True
                self.session.open(superzooi2, str(name), str(url))
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
        lnk = 'https://www.superzooi.com/'
        sel = self.menu_list[idx]
        if sel == ("CATEGORIES"):
            namex = "categories"
            lnk = 'http://superzooi.com/categories/'
            self.session.open(categories, namex, lnk)

        if sel == 'SEARCH':
            namex = sel.upper()
            lnk = 'http://superzooi.com/search/video/'
            self.search_text(namex, lnk)

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


class categories(Screen):
    def __init__(self, session, name, url):
        self.session = session
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'defaultListScreen.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.menulist = []
        self['menulist'] = rvList([])
        self['red'] = Label(_('Back'))
        self['title'] = Label('')
        self['title'].setText(title_plug)
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
            regexcat2 = '<li class="category span.*?<a href="(.*?)"><img src="(.*?)".*?a href.*?">(.*?)<'
            match2 = re.compile(regexcat2, re.DOTALL).findall(content)
            for url, pic, name in match2:
                url1 = "http://superzooi.com" + url
                self.cat_list.append(show_(name, url1))
                self['menulist'].l.setList(self.cat_list)
                self['menulist'].moveToIndex(0)
            if len(self.cat_list) < 0:
                return
            else:
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
        self.session.open(superzooi2, str(name), str(url))

    def exit(self):
        self.close()


class superzooi2(Screen):
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
        url = self.url
        try:
            pages = 100
            i = 1
            while i < pages:
                if 'superzooi.com/search/video' in self.url:
                    if i == 1:
                        i = ''
                        url1 = self.url + str(i)  # + "/"
                    else:
                        url1 = self.url + '/' + str(i) + "/"
                    print('is search url', url1)
                else:
                    url1 = self.url + '/recent/' + str(i) + "/"

                name = "Page " + str(i)
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
        print('pages url: ', url)
        self.session.open(superzooi3, name, url)

    def exit(self):
        global search
        search = False
        self.close()


class superzooi3(Screen):
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
        self['title'] = Label('')
        self['title'].setText(title_plug)
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
            regexvideo = 'li class="span3".*?a href="(.*?)".*?title="(.*?)"'
            match = re.compile(regexvideo, re.DOTALL).findall(content)
            for url, name in match:
                url1 = "http://superzooi.com" + str(url)
                self.cat_list.append(show_(name, url1))
            self['menulist'].l.setList(self.cat_list)
            self['menulist'].moveToIndex(0)
            if len(self.cat_list) < 0:
                return
            else:
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
        print("superzooi3 = ", url)
        self.session.open(superzooi4, str(name), str(url))

    def exit(self):
        self.close()


class superzooi4(Screen):
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
        self['title'] = Label('')
        self['title'].setText(title_plug)
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
            regexvideo = 'player-embed">.*?src="https://embed.heavy(.*?)"'
            match = re.compile(regexvideo, re.DOTALL).findall(content)
            url = "http://embed.heavy" + match[0]
            reference = "http://superzooi.com/"
            content2 = Utils.getUrl2(url, reference)
            if six.PY3:
                content2 = six.ensure_str(content)
            regexvideo = 'type="video/mp4" src="(.*?)"'
            match2 = re.compile(regexvideo, re.DOTALL).findall(content2)
            url = match2[0]
            name = self.name
            self.cat_list.append(show_(name, url))
            self['menulist'].l.setList(self.cat_list)
            self['menulist'].moveToIndex(0)
            if len(self.cat_list) < 0:
                return
            else:
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
