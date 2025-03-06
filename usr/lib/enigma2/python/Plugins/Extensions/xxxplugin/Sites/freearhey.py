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
import codecs
import os
import re
import six
import ssl
import sys
from Plugins.Extensions.xxxplugin import (_, skin_path)
from Plugins.Extensions.xxxplugin.lib import Utils
from Plugins.Extensions.xxxplugin.plugin import (
	rvList,
	Playstream1,
	# Playstream2,
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
title_plug = 'freearhey '
desc_plugin = ('..:: freearhey by Lululla %s ::.. ' % currversion)
PLUGIN_PATH = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('xxxplugin'))
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
print(current)
print(parent)
pluglogo = os.path.join(PLUGIN_PATH, 'pic/freearhey.png')
stripurl = 'aHR0cHM6Ly9pcHR2LW9yZy5naXRodWIuaW8vaXB0di9jYXRlZ29yaWVzL3h4eC5tM3U='
referer = 'https://github.com/iptv-org/iptv'
_session = None
Path_Movies = '/tmp/'
PY3 = sys.version_info.major >= 3


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
		self.onLayoutFinish.append(self.updateMenuList)

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
		for x in self.cat_list:
			del self.cat_list[0]
		items = []
		try:
			url = Utils.b64decoder(stripurl)
			content = Utils.getUrl2(url, referer)
			if six.PY3:
				content = six.ensure_str(content)
			regexcat = '#EXTINF.*?title="(.+?)".*?,(.+?)\\n(.+?)\\n'
			match = re.compile(regexcat, re.DOTALL).findall(content)
			for country, name, url in match:
				if ".m3u8" not in url:
					continue
				url = url.replace(" ", "").replace("\\n", "").replace('\r', '')
				name = name.replace('\r', '')
				name = country + ' | ' + name
				item = name + "###" + url + '\n'
				items.append(item)
			items.sort()
			for item in items:
				name = item.split('###')[0]
				url = item.split('###')[1]
				name = name.capitalize()
				self.cat_list.append(show_(name, url))
			self['menulist'].l.setList(self.cat_list)
			auswahl = self['menulist'].getCurrent()[0][0]
			self['name'].setText(str(auswahl))
		except Exception as e:
			print('exception error ', str(e))

	def ok(self):
		name = self['menulist'].getCurrent()[0][0]
		url = self['menulist'].getCurrent()[0][1]
		self.play_that_shit(url, name)

	def play_that_shit(self, url, name):
		self.session.open(Playstream1, str(name), str(url))

	def exit(self):
		self.close()
