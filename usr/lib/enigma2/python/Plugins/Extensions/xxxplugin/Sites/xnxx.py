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
from Components.Pixmap import Pixmap
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import SCOPE_PLUGINS
from Tools.Directories import resolveFilename
from enigma import eTimer
import os
import re
import six
import ssl
import sys
from Plugins.Extensions.xxxplugin.plugin import rvList, Playstream1  # , returnIMDB
from Plugins.Extensions.xxxplugin.plugin import showlist, rvoneListEntry
from Plugins.Extensions.xxxplugin.plugin import show_, cat_
from Plugins.Extensions.xxxplugin.lib import Utils
from Plugins.Extensions.xxxplugin.lib import html_conv
from Plugins.Extensions.xxxplugin import _, skin_path  # , screenwidth
PY3 = sys.version_info.major >= 3
print('Py3: ', PY3)


if sys.version_info >= (2, 7, 9):
    try:
        sslContext = ssl._create_unverified_context()
    except:
        sslContext = None

currversion = '1.0'
title_plug = 'xnxx '
desc_plugin = ('..:: xnxx by Lululla %s ::.. ' % currversion)
PLUGIN_PATH = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('xxxplugin'))
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
print(current)
print(parent)
pluglogo = os.path.join(PLUGIN_PATH, 'pic/xnxx.png')
stripurl = 'https://www.xnxx.com/tags'
caturl = 'https://www.xnxx.com/hits'
_session = None
Path_Movies = '/tmp/'
global search
search = False


Panel_list = [
        ("SEARCH"),
        ("TAGS"),
        ("HITS"),
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
                self.session.open(xnxx4, name, url)
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
        sel = self.menu_list[idx]
        if sel == ("TAGS"):
            lnk = (stripurl)
        if sel == ("HITS"):
            lnk = (caturl)
        namex = sel.upper()
        if sel == 'SEARCH':
            lnk = ("https://www.xnxx.com/search/")
            self.search_text(namex, lnk)
        else:
            if 'TAGS' in namex:
                print('tags select')
                self.session.open(xnxx1, namex, lnk)
            if 'HITS' in namex:
                print('hits select')
                self.session.open(xnxxplus2, namex, lnk)
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


class xnxx1(Screen):
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
            url = self.url
            content = Utils.getUrl(url)
            if six.PY3:
                content = six.ensure_str(content)
            regexcat = 'href="/search(.*?)">(.*?)</a><strong>(.*?)</strong'
            match = re.compile(regexcat, re.DOTALL).findall(content)
            for url, name, qty in match:
                url1 = "https://xnxx.com/search" + url
                name = name + ' - Videos N°' + qty
                self.cat_list.append(show_(name, url1))
            if len(self.cat_list) < 0:
                return
            else:
                self['menulist'].l.setList(self.cat_list)
                self['menulist'].moveToIndex(0)
                auswahl = self['menulist'].getCurrent()[0]
                self['name'].setText(str(auswahl))
        except Exception as e:
            print(e)

    def ok(self):
        name = self['menulist'].getCurrent()[0][0]
        url = self['menulist'].getCurrent()[0][1]
        self.play_that_shit(url, name)

    def play_that_shit(self, url, name):
        print('xnxx1 select url', url)
        self.session.open(xnxxplus2, name, url)

    def exit(self):
        self.close()


class xnxxplus2(Screen):
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
            i = 0
            while i < pages:
                page = i
                if page == 0:
                    url1 = url
                else:
                    url1 = url + str(page)
                name = "Page " + str(page)
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
        print('iiiiii= ', i)
        if i < 0:
            return
        idx = self["menulist"].getSelectionIndex()
        name = self.names[idx]
        url = self.urls[idx]

        if 'xnxx.com/hits' in url:
            print('xnxx.com/hits select url', url)
            self.session.open(xnxx4, name, url)
        else:
            print('xxnplus tags select url', url)
            self.session.open(xnxx2, name, url)

    def exit(self):
        self.close()


class xnxx2(Screen):
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
            url = self.url
            content = Utils.getUrl(url)
            if six.PY3:
                content = six.ensure_str(content)
            regexcat = '"thumb-under">.*?href="(.*?)".*?title="(.*?)"'
            match = re.compile(regexcat, re.DOTALL).findall(content)
            for url, name in match:
                url1 = "https://xnxx.com" + url
                name = name.upper()
                self.cat_list.append(show_(name, url1))
            if len(self.cat_list) < 0:
                return
            else:
                self['menulist'].l.setList(self.cat_list)
                self['menulist'].moveToIndex(0)
                auswahl = self['menulist'].getCurrent()[0]
                self['name'].setText(str(auswahl))
        except Exception as e:
            print(e)

    def ok(self):
        name = self['menulist'].getCurrent()[0][0]
        url = self['menulist'].getCurrent()[0][1]
        self.play_that_shit(url, name)

    def play_that_shit(self, url, name):
        print("xnxx2 select= ", url)
        self.session.open(xnxx3, name, url)

    def exit(self):
        self.close()


class xnxx3(Screen):
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
            regexcat = '"contentUrl": "(.*?)"'
            match = re.compile(regexcat, re.DOTALL).findall(content)
            for url in match:
                url1 = url
                name = self.name
                self.cat_list.append(show_(name, url1))

            if len(self.cat_list) < 0:
                return
            else:
                self['menulist'].l.setList(self.cat_list)
                self['menulist'].moveToIndex(0)
                auswahl = self['menulist'].getCurrent()[0]
                self['name'].setText(str(auswahl))
        except Exception as e:
            print(e)

    def ok(self):
        name = self['menulist'].getCurrent()[0][0]
        url = self['menulist'].getCurrent()[0][1]
        self.play_that_shit(url, name)

    def play_that_shit(self, url, name):
        print("xnxx3 select= ", url)
        # self.session.open(xnxx4, str(name), str(url))
        self.session.open(Playstream1, str(name), str(url))

    def exit(self):
        global search
        search = False
        self.close()


class xnxx4(Screen):
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
            print("content c =", content)
            # <div id="video_66859049" data-id="66859049" data-is-channel="1" class="thumb-block  with-uploader">
            # <div class="thumb-inside"><div class="thumb">
            # <a href="/search-video/eAE9UdFu2zAM_JVBz2oqUiIp5Qs2bCiKrnsY1kFwasMJ4MRBbDcphv37zn3Yi0Qe78ij9Mf9dFv32Xn3FfftdLsh_OK2qllKSMW7b277639mqbAIsTcSRli8KasFQ2BcYlHyJkmjBPGWWDiW4ikU6Ix8wmHFoteiVkQjODEoCQLhFLKI5wyJkIFDYmB7iyVTyuBE4qJoCHNGGRzJookJ05NZyooSgAxDkCcpGiHnENeijwFtdOXEEDiyrJyUEHoRNmyD6RqkYDHslZijEBoyYW2UOHFYRwAlUXgGgmERxvAIhZR-e_cDz_hy_3Zou_GO4hwuM4eX-90yzV1b57v-cBmm2g1DU_fjMLxfx7GtaTxR3V1fazMf664ZwGi77lybUzPUtjnXy7j0-zp1t9o3526qr8uxHk71OC4z4CsU47Xu5j5Yxvc9um3w7uHjfIadab40h34_r6WnD_Q70PDpvEzTO8BnpAT_WFNLxvejgcu2Id3EuCFS9_cftriKsA==/647518e0e1b131c146ab36e76925d8ba"
            # ><img src="https://static-cdn77.xnxx-cdn.com/img/lightbox/lightbox-blank.gif"
            # data-src="https://cdn77-pic.xnxx-cdn.com/videos/thumbs169xnxx/5b/ae/a2/5baea2cd9f572357437156d6dc511fc6-2/5baea2cd9f572357437156d6dc511fc6.17.jpg"
             # data-idcdn="10" data-videoid="66859049" id="pic_66859049" alt="" /></a></div></div><div class="uploader">
             # <a href="/porn-maker/anal-vids-trailers"><span class="name">Anal Vids Trailers</span></a></div><div class="thumb-under"><p>
             # <a href="/search-video/eAE9UdFu2zAM_JVBz2oqUiIp5Qs2bCiKrnsY1kFwasMJ4MRBbDcphv37zn3Yi0Qe78ij9Mf9dFv32Xn3FfftdLsh_OK2qllKSMW7b277639mqbAIsTcSRli8KasFQ2BcYlHyJkmjBPGWWDiW4ikU6Ix8wmHFoteiVkQjODEoCQLhFLKI5wyJkIFDYmB7iyVTyuBE4qJoCHNGGRzJookJ05NZyooSgAxDkCcpGiHnENeijwFtdOXEEDiyrJyUEHoRNmyD6RqkYDHslZijEBoyYW2UOHFYRwAlUXgGgmERxvAIhZR-e_cDz_hy_3Zou_GO4hwuM4eX-90yzV1b57v-cBmm2g1DU_fjMLxfx7GtaTxR3V1fazMf664ZwGi77lybUzPUtjnXy7j0-zp1t9o3526qr8uxHk71OC4z4CsU47Xu5j5Yxvc9um3w7uHjfIadab40h34_r6WnD_Q70PDpvEzTO8BnpAT_WFNLxvejgcu2Id3EuCFS9_cftriKsA==/647518e0e1b131c146ab36e76925d8ba"
             # title="Busted T-Girls, Ella Hollywood, 4on1, BWC, ATM, Balls Deep Anal, DAP, Rough Sex, Gapes, Cum in Mouth, Swallow BTG078"
            # >Busted T-Girls, Ella Hollywood, 4on1, BWC, ATM, Balls Deep Anal, DAP, Rough Sex, Gapes, Cum in Mouth, Swallow BTG078</a></p><p class="metadata"><span class="right">
            regexvideo = 'data-src="(.*?)".*?a href="(.*?)".*?title="(.*?)">'
            match = re.compile(regexvideo, re.DOTALL).findall(content)
            for pic, url, name in match:
                url1 = "https://xnxx.com" + url
                name = name.upper()
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
        print("xnxx4 select= ", url)
        self.session.open(xnxx3, str(name), str(url))

    def exit(self):
        global search
        search = False
        self.close()
