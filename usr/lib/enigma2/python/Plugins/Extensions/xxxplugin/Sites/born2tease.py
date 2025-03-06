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
from Plugins.Extensions.xxxplugin.lib import (Utils, html_conv)
from Plugins.Extensions.xxxplugin import (_, skin_path)
from Plugins.Extensions.xxxplugin.plugin import (
	rvList,
	Playstream1,
	# showlist,
	# rvoneListEntry,
	show_,
)

PY3 = sys.version_info.major >= 3


if sys.version_info >= (2, 7, 9):
	try:
		sslContext = ssl._create_unverified_context()
	except:
		sslContext = None

currversion = '1.0'
title_plug = 'Born2tease '
desc_plugin = ('..:: Born2tease by Lululla %s ::.. ' % currversion)
PLUGIN_PATH = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('xxxplugin'))
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
print(current)
print(parent)
pluglogo = os.path.join(PLUGIN_PATH, 'pic/born2tease.png')
stripurl = 'aHR0cHM6Ly9ib3JuMnRlYXNlLm5ldC9tb2RlbHMuaHRtbA=='
_session = None
Path_Movies = '/tmp/'

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
			url = Utils.b64decoder(stripurl)
			content = Utils.getUrl(url)
			if six.PY3:
				content = six.ensure_str(content)
			regexcat = 'div id="videothumbs2">(.*?)<.*?<a href="(.*?)"'
			match = re.compile(regexcat, re.DOTALL).findall(content)
			for name, url in match:
				name = normalize(name)
				name = html_conv.html_unescape(name)
				url1 = url.replace("videos", "allvideos")
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

	def play_that_shit(self, name, url):
		self.session.open(born2tease3, url, name)

	def exit(self):
		self.close()


class born2tease3(Screen):
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
		self['poster'] = Pixmap()
		self['text'] = Label('Only for Adult by Lululla')
		self.currentList = 'menulist'
		self.loading_ok = False
		self.count = 0
		self.loading = 0
		self.name = name
		self.url = url
		self['actions'] = ActionMap(
			['OkCancelActions',
			 'ColorActions',
			 'DirectionActions',
			 'MovieSelectionActions'],
			{
				'up': self.up,
				'down': self.down,
				'left': self.left,
				'right': self.right,
				'ok': self.ok,
				'green': self.ok,
				'cancel': self.exit,
				'red': self.exit
			},
			-1
		)
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
			start = 10
			n1 = self.url.find("/", start)
			n2 = self.url.find("/", (n1 + 1))
			site = self.url[:(n2 + 1)]
			content = Utils.getUrl(self.url)
			if six.PY3:
				content = six.ensure_str(content)
			regexcat = 'div id="videothumbs2.*?<a href="(.*?)"><img src="(.*?)" alt="(.*?)"'
			match = re.compile(regexcat, re.DOTALL).findall(content)

			for url, pic, name in match:
				if 'http' in url:
					url1 = url.replace("../", "")
					pass
				else:
					url1 = site + str(url).replace("../", "")
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
		self.session.open(born2tease4, name, url)

	def exit(self):
		global search
		search = False
		self.close()


class born2tease4(Screen):
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
		self['actions'] = ActionMap(
			['OkCancelActions',
			 'ColorActions',
			 'DirectionActions',
			 'MovieSelectionActions'],
			{
				'up': self.up,
				'down': self.down,
				'left': self.left,
				'right': self.right,
				'ok': self.ok,
				'green': self.ok,
				'cancel': self.exit,
				'red': self.exit
			},
			-1
		)
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
			start = 10
			n1 = self.url.find("/", start)
			n2 = self.url.find("/", (n1 + 1))
			site = self.url[:(n2 + 1)]
			regexcat = '<video src="(.*?)"'
			match = re.compile(regexcat, re.DOTALL).findall(content)
			for url in match:
				url1 = site + str(url).replace('.mp4/', '.mp4')
				name = self.name
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
		self.session.open(Playstream1, str(name), str(url))

	def exit(self):
		global search
		search = False
		self.close()
