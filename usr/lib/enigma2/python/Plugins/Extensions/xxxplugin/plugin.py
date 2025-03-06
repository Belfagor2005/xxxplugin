#!/usr/bin/python
# -*- coding: utf-8 -*-

# '''
# Info http://t.me/tivustream
# ****************************************
# *        coded by Lululla              *
# *          skin by MMark               *
# *   start init 05/09/2024              *
# ****************************************
# '''

from __future__ import print_function
from . import _, skin_path, screenwidth, THISPLUG
from .lib import Utils, html_conv
from .lib.AspectManager import AspectManager
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import (MultiContentEntryPixmapAlphaTest, MultiContentEntryText)
from Components.Pixmap import Pixmap, MovingPixmap
from Components.ProgressBar import ProgressBar
from Components.ScrollLabel import ScrollLabel
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from Components.config import (
	ConfigDirectory,
	ConfigYesNo,
	ConfigSelection,
	getConfigListEntry,
	config,
	ConfigSubsection,
	configfile,
)
from PIL import Image, ImageFile  # , ImageChops
from Plugins.Plugin import PluginDescriptor
from Screens.InfoBarGenerics import (
	InfoBarSeek,
	InfoBarAudioSelection,
	InfoBarSubtitleSupport,
)
from Screens.LocationBox import LocationBox
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Tools.Downloader import downloadWithProgress
from enigma import (
	RT_HALIGN_LEFT,
	RT_VALIGN_CENTER,
	eListboxPythonMultiContent,
	eServiceReference,
	eTimer,
	gFont,
	iPlayableService,
	loadPNG,
)
from os.path import (splitext, exists as file_exists)
from twisted.internet.reactor import callInThread
import codecs
import os
import re
import requests
import sys
import shutil
import six


ImageFile.LOAD_TRUNCATED_IMAGES = True
_session = None

aspect_manager = AspectManager()


global defpic, dblank
global Path_Movies, Path_Cache

PY3 = sys.version_info.major >= 3
if PY3:
	from http.client import HTTPConnection
	from urllib.parse import urlparse
	PY3 = True
else:
	from httplib import HTTPConnection
	from urlparse import urlparse

HTTPConnection.debuglevel = 1


def getversioninfo():
	currversion = '1.0'
	version_file = os.path.join(THISPLUG, 'version')
	if file_exists(version_file):
		try:
			fp = open(version_file, 'r').readlines()
			for line in fp:
				if 'version' in line:
					currversion = line.split('=')[1].strip()
		except:
			pass
	return (currversion)


currversion = getversioninfo()
Version = currversion + ' - 05.03.2025'
title_plug = '..:: XXX Revolution V. %s ::..' % Version
folder_path = "/tmp/xxxplugin/"
name_plug = 'XXX Revolution'
piccons = os.path.join(THISPLUG, 'res/img/')
res_plugin_path = os.path.join(THISPLUG, 'res/')
pngx = os.path.join(res_plugin_path, 'pics/setting2.png')

if not file_exists(folder_path):
	os.makedirs(folder_path)
try:
	folder_path = sum([sum(map(lambda fname: os.path.getsize(os.path.join(folder_path, fname)), files)) for folder_p, folders, files in os.walk(folder_path)])
	posterpng = "%0.f" % (folder_path // (1024 * 1024.0))
	if posterpng >= "5":
		shutil.rmtree(folder_path)
except:
	pass


if screenwidth.width() == 2560:
	defpic = THISPLUG + 'res/img/no_work.png'

elif screenwidth.width() == 1920:
	defpic = THISPLUG + 'res/img/tvs.png'
else:
	defpic = THISPLUG + 'res/img/no_work.png'
dblank = THISPLUG + 'res/img/undefinided.png'


def get_screen_settings():
	"""Helper per configurazioni basate sulla risoluzione dello schermo."""
	if screenwidth.width() == 2560:
		return {
			"item_height": 60,
			"font_size": 42,
			"pixmap_size": (50, 50),
			"pixmap_pos": (5, 5),
			"text_pos": (90, 0),
			"text_size": (1200, 50),
		}
	elif screenwidth.width() == 1920:
		return {
			"item_height": 50,
			"font_size": 30,
			"pixmap_size": (40, 40),
			"pixmap_pos": (5, 5),
			"text_pos": (70, 0),
			"text_size": (1000, 50),
		}
	else:
		return {
			"item_height": 50,
			"font_size": 24,
			"pixmap_size": (40, 40),
			"pixmap_pos": (3, 10),
			"text_pos": (50, 0),
			"text_size": (500, 50),
		}


class rvList(MenuList):
	def __init__(self, list):
		screen_settings = get_screen_settings()
		MenuList.__init__(self, list, False, eListboxPythonMultiContent)
		self.l.setItemHeight(screen_settings["item_height"])
		self.l.setFont(0, gFont('Regular', screen_settings["font_size"]))


def rvoneListEntry(name):
	screen_settings = get_screen_settings()
	res = [name]
	pngx = os.path.join(res_plugin_path, 'pics/setting2.png')
	res.append(MultiContentEntryPixmapAlphaTest(
		pos=screen_settings["pixmap_pos"],
		size=screen_settings["pixmap_size"],
		png=loadPNG(pngx)
	))
	res.append(MultiContentEntryText(
		pos=screen_settings["text_pos"],
		size=screen_settings["text_size"],
		font=0,
		text=name,
		flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER
	))
	return res


def showlist(data, list_widget):
	plist = [rvoneListEntry(name) for name in data]
	list_widget.setList(plist)


def show_(name, link):
	screen_settings = get_screen_settings()
	res = [(name, link)]
	res.append(MultiContentEntryText(
		pos=(0, 0),
		size=screen_settings["text_size"],
		font=0,
		text=name,
		flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER
	))
	return res


mdpchoices = [
	("4097", ("IPTV(4097)")),
	("1", ("Dvb(1)")),
]
players = [
	("/usr/bin/gstplayer", ("5001", "Gstreamer(5001)")),
	("/usr/bin/exteplayer3", ("5002", "Exteplayer3(5002)")),
	("/usr/bin/apt-get", ("8193", "DreamOS GStreamer(8193)"))
]


mdpchoices.extend(choice for path, choice in players if file_exists(path))


config.plugins.xxxplugin = ConfigSubsection()
cfg = config.plugins.xxxplugin
cfg.services = ConfigSelection(default='4097', choices=mdpchoices)
cfg.thumb = ConfigSelection(default="True", choices=[("True", _("yes")), ("False", _("no"))])
cfg.movie = ConfigDirectory("/media/hdd/movie")
cfg.cachefold = ConfigDirectory("/media/hdd", False)

try:
	from Components.UsageConfig import defaultMoviePath
	downloadpath = defaultMoviePath()
	cfg.movie = ConfigDirectory(default=downloadpath)
	cfg.cachefold = ConfigDirectory(default=downloadpath)
except:
	if file_exists("/usr/bin/apt-get"):
		cfg.movie = ConfigDirectory(default='/media/hdd/movie')
		cfg.cachefold = ConfigDirectory(default='/media/hdd')

Path_Movies = str(cfg.movie.value) + '/'
Path_Cache = str(cfg.cachefold.value).replace('movie', 'xxxplugin')


def returnIMDB(text_clear):
	plugins = {
		"TMDB": ("TMBD", "tmdbScreen"),
		"tmdb": ("tmdb", "tmdbScreen"),
		"IMDb": ("IMDb", "main")
	}
	text = html_conv.html_unescape(text_clear)
	for plugin_name, (module_name, func_name) in plugins.items():
		plugin_path = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format(plugin_name))
		if os.path.exists(plugin_path):
			try:
				plugin_module = __import__("Plugins.Extensions.{}.plugin".format(module_name), fromlist=[func_name])
				plugin_function = getattr(plugin_module, func_name)
				_session.open(plugin_function, text, 0 if func_name == "tmdbScreen" else None)
				return True
			except Exception as e:
				print("[XCF] {} error: {}".format(plugin_name, str(e)))
				return False
	_session.open(MessageBox, text, MessageBox.TYPE_INFO)
	return False


def threadGetPage(url=None, file=None, key=None, success=None, fail=None, *args, **kwargs):
	print('[xxxplugin][threadGetPage] url, file, key, args, kwargs', url, "   ", file, "   ", key, "   ", args, "   ", kwargs)
	from requests import get, exceptions
	from requests.exceptions import HTTPError
	# from twisted.internet.reactor import callInThread
	try:
		url = url.rstrip('\r\n')
		url = url.rstrip()
		url = url.replace("%0A", "")
		response = get(url, verify=False)
		response.raise_for_status()
		if file is None:
			success(response.content)
		elif key is not None:
			success(response.content, file, key)
		else:
			success(response.content, file)
	except HTTPError as httperror:
		print('[xxxplugin][threadGetPage] Http error: ', httperror)
		# fail(error)  # E0602 undefined name 'error'
	except exceptions.RequestException as error:
		print(error)


def getpics(names, pics, tmpfold, picfold):
	pix = []
	if cfg.thumb.value == "False":
		npic = len(pics)
		i = 0
		while i < npic:
			pix.append(defpic)
			i += 1
		return pix
	cmd = "rm " + tmpfold + "/*"
	os.system(cmd)
	npic = len(pics)
	j = 0
	while j < npic:
		name = names[j]
		if name is None or name == '':
			name = "Video"
		url = pics[j]
		ext = str(splitext(url)[-1])
		picf = os.path.join(picfold, str(name + ext))
		tpicf = os.path.join(tmpfold, str(name + ext))

		if file_exists(picf):
			if ('stagione') in str(name.lower()):
				cmd = "rm " + picf
				os.system(cmd)

			cmd = "cp " + picf + " " + tmpfold
			print("In getpics fileExists(picf) cmd =", cmd)
			os.system(cmd)

		if not file_exists(picf):
			# if plugin_path in url:
			if THISPLUG in url:
				try:
					cmd = "cp " + url + " " + tpicf
					print("In getpics not fileExists(picf) cmd =", cmd)
					os.system(cmd)
				except:
					pass
			else:
				# now download image
				try:
					url = url.replace(" ", "%20").replace("ExQ", "=")
					url = url.replace("AxNxD", "&").replace("%0A", "")
					poster = Utils.checkRedirect(url)
					if poster:
						if "|" in url:
							n3 = url.find("|", 0)
							n1 = url.find("Referer", n3)
							n2 = url.find("=", n1)
							url = url[:n3]
							referer = url[n2:]
							p = Utils.getUrl2(url, referer)
							with open(tpicf, 'wb') as f1:
								f1.write(p)
						else:
							try:
								try:
									with open(tpicf, 'wb') as f:
										f.write(requests.get(url, stream=True, allow_redirects=True).content)
									print('=============11111111=================\n')
								except Exception as e:
									print("Error: Exception", e)
									callInThread(threadGetPage, url=poster, file=tpicf, success=downloadPic, fail=downloadError)
							except Exception as e:
								print("Error: Exception 2", e)

				except:
					cmd = "cp " + defpic + " " + tpicf
					os.system(cmd)
					print('cp defpic tpicf')

		if not file_exists(tpicf):
			cmd = "cp " + defpic + " " + tpicf
			os.system(cmd)

		if file_exists(tpicf):
			try:
				size = [150, 220]
				if screenwidth.width() == 2560:
					size = [294, 440]
				elif screenwidth.width() == 1920:
					size = [200, 200]
				else:
					size = [150, 220]

				file_name, file_extension = splitext(tpicf)
				try:
					im = Image.open(tpicf).convert("RGBA")
					# shrink if larger
					try:
						im.thumbnail(size, Image.LANCZOS)
					except:
						im.thumbnail(size, Image.ANTIALIAS)
					imagew, imageh = im.size
					# enlarge if smaller
					try:
						if imagew < size[0]:
							ratio = size[0] / imagew
							try:
								im = im.resize((int(imagew * ratio), int(imageh * ratio)), Image.LANCZOS)
							except:
								im = im.resize((int(imagew * ratio), int(imageh * ratio)), Image.ANTIALIAS)

							imagew, imageh = im.size
					except Exception as e:
						print(e)
					# # no work on PY3
					# # crop and center image
					# bg = Image.new("RGBA", size, (255, 255, 255, 0))
					# im_alpha = im.convert("RGBA").split()[-1]
					# bgwidth, bgheight = bg.size
					# bg_alpha = bg.convert("RGBA").split()[-1]
					# temp = Image.new("L", (bgwidth, bgheight), 0)
					# temp.paste(im_alpha, (int((bgwidth - imagew) / 2), int((bgheight - imageh) / 2)), im_alpha)
					# bg_alpha = ImageChops.screen(bg_alpha, temp)
					# bg.paste(im, (int((bgwidth - imagew) / 2), int((bgheight - imageh) / 2)))
					# im = bg
					im.save(file_name + ".png", "PNG")
				except Exception as e:
					print(e)
					im = Image.open(tpicf)
					try:
						im.thumbnail(size, Image.LANCZOS)
					except:
						im.thumbnail(size, Image.ANTIALIAS)
					im.save(tpicf)
			except Exception as e:
				print("******* picon resize failed *******", e)
				tpicf = defpic
		else:
			print("******* make picon failed *******")
			tpicf = defpic

		pix.append(j)
		pix[j] = picf
		j += 1

	cmd1 = "cp " + tmpfold + "/* " + picfold
	os.system(cmd1)

	cmd1 = "rm " + tmpfold + "/* &"
	os.system(cmd1)
	return pix


def downloadPic(output, poster):
	try:
		if output is not None:
			f = open(poster, 'wb')
			f.write(output)
			f.close()
	except Exception as e:
		print('downloadPic error ', e)
	return


def downloadError(output):
	print('output error ', output)
	pass


def savePoster(dwn_poster, url_poster):
	with open(dwn_poster, 'wb') as f:
		f.write(requests.get(url_poster, stream=True, allow_redirects=True).content)
		f.close()


class ConfigEx(ConfigListScreen, Screen):

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		skin = os.path.join(skin_path, 'Config.xml')
		if file_exists('/var/lib/dpkg/status'):
			skin = os.path.join(skin_path, 'ConfigOs.xml')
		with codecs.open(skin, "r", encoding="utf-8") as f:
			self.skin = f.read()
		self.setup_title = _("SETUP PLUGIN")
		self.onChangedEntry = []
		self.list = []
		ConfigListScreen.__init__(self, self.list, session=self.session, on_change=self.changedEntry)
		self['key_red'] = Label(_('Back'))
		self['key_green'] = Label(_('Save'))
		self['key_yellow'] = Button(_('Empty Cache'))
		self["description"] = Label('')
		self['actions'] = ActionMap(["SetupActions", "ColorActions", "VirtualKeyboardActions"], {
			'cancel': self.extnok,
			'yellow': self.cachedel,
			'green': self.save,
			'showVirtualKeyboard': self.KeyText,
			'ok': self.Ok_edit
		}, -2)

		self.createSetup()
		self.onLayoutFinish.append(self.layoutFinished)

		if self.setInfo not in self['config'].onSelectionChanged:
			self['config'].onSelectionChanged.append(self.setInfo)

	def layoutFinished(self):
		self.setTitle(self.setup_title)

	def VirtualKeyBoardCallback(self, callback=None):
		if callback is not None and len(callback):
			self["config"].getCurrent()[1].setValue(callback)
			self["config"].invalidate(self["config"].getCurrent())

	def KeyText(self):
		sel = self['config'].getCurrent()
		if sel:
			self.session.openWithCallback(self.VirtualKeyBoardCallback, VirtualKeyBoard, title=self['config'].getCurrent()[0], text=self['config'].getCurrent()[1].value)

	def cachedel(self):
		fold = os.path.join(Path_Cache, "pic")
		Utils.cachedel(fold)
		self.mbox = self.session.open(MessageBox, _('All cache fold empty!'), MessageBox.TYPE_INFO, timeout=5)

	def createSetup(self):
		self.editListEntry = None
		self.list = []
		self.list.append(getConfigListEntry(_('Services Player Reference type'), cfg.services, _("Configure Service Player Reference, Enigma restart required")))
		self.list.append(getConfigListEntry(_("Cache folder"), cfg.cachefold, _("Folder Cache Path (eg.: /media/hdd), Enigma restart required")))
		self.list.append(getConfigListEntry(_("Movie folder"), cfg.movie, _("Folder Movie Path (eg.: /media/hdd/movie), Enigma restart required")))
		# self.list.append(getConfigListEntry(_("Show thumbpic ?"), cfg.thumb, _("Show Thumbpics ? Enigma restart required")))
		self['config'].list = self.list
		self["config"].l.setList(self.list)
		self.setInfo()

	def setInfo(self):
		try:
			sel = self['config'].getCurrent()[2]
			if sel:
				# print('sel =: ', sel)
				self['description'].setText(str(sel))
			else:
				self['description'].setText(_('SELECT YOUR CHOICE'))
			return
		except Exception as e:
			print("Error ", e)

	def changedEntry(self):
		for x in self.onChangedEntry:
			x()
		try:
			if isinstance(self['config'].getCurrent()[1], ConfigYesNo) or isinstance(self['config'].getCurrent()[1], ConfigSelection):
				self.createSetup()
		except:
			pass

	def getCurrentEntry(self):
		return self['config'].getCurrent() and self['config'].getCurrent()[0] or ''

	def getCurrentValue(self):
		return self['config'].getCurrent() and str(self['config'].getCurrent()[1].getText()) or ''

	def createSummary(self):
		from Screens.Setup import SetupSummary
		return SetupSummary

	def Ok_edit(self):
		ConfigListScreen.keyOK(self)
		sel = self['config'].getCurrent()[1]
		if sel and sel == cfg.cachefold:
			self.setting = 'cachefold'
			self.openDirectoryBrowser(cfg.cachefold.value)
		if sel and sel == cfg.movie:
			self.setting = 'moviefold'
			self.openDirectoryBrowser(cfg.movie.value)
		else:
			pass

	def openDirectoryBrowser(self, path):
		try:
			self.session.openWithCallback(
				self.openDirectoryBrowserCB,
				LocationBox,
				windowTitle=_('Choose Directory:'),
				text=_('Choose Directory'),
				currDir=str(path),
				bookmarks=config.movielist.videodirs,
				autoAdd=False,
				editDir=True,
				inhibitDirs=['/bin', '/boot', '/dev', '/home', '/lib', '/proc', '/run', '/sbin', '/sys', '/var'],
				minFree=15
			)
		except Exception as e:
			print('openDirectoryBrowser get failed: ', e)

	def openDirectoryBrowserCB(self, path):
		if path is not None:
			if self.setting == 'cachefold':
				cfg.cachefold.setValue(path)
			if self.setting == 'moviefold':
				cfg.movie.setValue(path)
		return

	def save(self):
		if self['config'].isChanged():
			for x in self['config'].list:
				x[1].save()
			self.mbox = self.session.open(MessageBox, _('Settings saved correctly!'), MessageBox.TYPE_INFO, timeout=5)
			cfg.save()
			configfile.save()
		self.close()

	def extnok(self, answer=None):
		from Screens.MessageBox import MessageBox
		if answer is None:
			if self["config"].isChanged():
				self.session.openWithCallback(self.extnok, MessageBox, _("Really close without saving settings?"))
			else:
				self.close()
		elif answer:
			for x in self["config"].list:
				x[1].cancel()

			self.close()
		return


class Main(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		global _session
		_session = session
		self.list = []
		self["actions"] = ActionMap(
			["WizardActions", "InputActions", "ColorActions", "ButtonSetupActions", "DirectionActions"],
			{
				"ok": self.okClicked,
				"back": self.close,
				# "green": self.okClicked
				"red": self.close
			},
			-1
		)
		self.onLayoutFinish.append(self.startSession2)

	def startSession(self):
		self.session.openWithCallback(self.startSession2, startInit)

	def startSession2(self):
		self.names = []
		self.urls = []
		self.pics = []
		# sort test
		items = []
		# sort test
		i = 0
		name = ""
		# desc = ""
		pic = ""
		url = ""
		path = THISPLUG + "Sites"
		# print('path= ', path)
		try:
			def should_exclude(file):
				exclude_keywords = ['pycache', 'extractor', 'init', 'Utils', 'html_conv', 'no_work']
				return any(keyword in file for keyword in exclude_keywords)
			for root, dirs, files in os.walk(path):
				for file in files:
					if file.endswith('.py') and not file.endswith(('.pyo', '.pyc')):
						if should_exclude(file):
							continue

						name, ext = file.split(".")  # [-1]
						url = THISPLUG + "Sites/%s.py" % name
						pic = os.path.join(piccons, '%s.png' % name)
						if name not in self.names:
							# sort test
							item = name + "###" + url + "###" + pic
							items.append(item)
				items.sort()

				for item in items:
					name = item.split('###')[0]
					url = item.split('###')[1]
					pic = item.split('###')[2]
					# sort test
					self.names.append(name)
					self.urls.append(url)
					self.pics.append(pic)
					i += 1
					# print(name + '\n' + desc + '\n' + url + '\n' + pic)
		except Exception as e:
			print(e)
		title = name_plug
		if cfg.thumb.value == "True":
			self.session.open(GridMain, title, self.names, self.urls, pics=self.pics)

	def okClicked(self):
		pass


class GridMain(Screen):
	def __init__(self, session, menuTitle, names, urls, pics=[]):
		Screen.__init__(self, session)
		self.session = session
		global _session
		_session = session
		skin = os.path.join(skin_path, 'GridMain.xml')
		with codecs.open(skin, "r", encoding="utf-8") as f:
			self.skin = f.read()
		title = menuTitle
		self.name = menuTitle
		self["title"] = Button(title)

		self.pos = []

		if screenwidth.width() > 1920:
			self.pos.append([180, 90])
			self.pos.append([658, 90])
			self.pos.append([1134, 90])
			self.pos.append([1610, 90])
			self.pos.append([2084, 90])
			self.pos.append([180, 750])
			self.pos.append([658, 750])
			self.pos.append([1134, 750])
			self.pos.append([1610, 750])
			self.pos.append([2084, 750])

		elif screenwidth.width() == 1920:
			self.pos.append([154, 165])
			self.pos.append([513, 165])
			self.pos.append([869, 165])
			self.pos.append([1230, 165])
			self.pos.append([1580, 165])
			self.pos.append([154, 630])
			self.pos.append([513, 630])
			self.pos.append([869, 630])
			self.pos.append([1230, 630])
			self.pos.append([1580, 630])
		else:
			self.pos.append([81, 28])
			self.pos.append([319, 28])
			self.pos.append([556, 28])
			self.pos.append([793, 28])
			self.pos.append([1031, 28])
			self.pos.append([81, 348])
			self.pos.append([319, 348])
			self.pos.append([556, 348])
			self.pos.append([793, 348])
			self.pos.append([1031, 348])

		tmpfold = os.path.join(Path_Cache, "tmp")
		picfold = os.path.join(Path_Cache, "pic")

		picx = getpics(names, pics, tmpfold, picfold)
		# print("In Gridmain pics = ", pics)

		self.urls = urls
		self.pics = picx
		self.names = names
		# self.infos = infos
		self["info"] = Label()

		list = []
		list = names
		# list.sort()
		self["menu"] = List(list)
		for x in list:
			print("x in list =", x)
		self["frame"] = MovingPixmap()

		self.PIXMAPS_PER_PAGE = 10
		i = 0
		while i < self.PIXMAPS_PER_PAGE:
			self["label" + str(i + 1)] = StaticText()
			self["pixmap" + str(i + 1)] = Pixmap()
			i += 1

		self.npics = len(self.names)
		self.npage = int(float(self.npics // self.PIXMAPS_PER_PAGE)) + 1
		self.index = 0
		self.maxentry = len(list) - 1
		self.ipage = 1

		self["actions"] = ActionMap(
			["OkCancelActions",
			 "EPGSelectActions",
			 "MenuActions",
			 "DirectionActions",
			 "NumberActions"],
			{
				"ok": self.okClicked,
				"epg": self.showIMDB,
				"info": self.about,
				"cancel": self.cancel,
				"menu": self.configure,
				"left": self.key_left,
				"right": self.key_right,
				"up": self.key_up,
				"down": self.key_down
			}
		)

		self.onLayoutFinish.append(self.openTest)

	def paintFrame(self):
		try:
			if self.index > self.maxentry:
				self.index = self.minentry
			self.idx = self.index
			name = self.names[self.idx]
			self['info'].setText(str(name))
			ifr = self.index - (self.PIXMAPS_PER_PAGE * (self.ipage - 1))
			ipos = self.pos[ifr]
			self["frame"].moveTo(ipos[0], ipos[1], 1)
			self["frame"].startMoving()
		except Exception as e:
			print('Error in paintFrame: ', e)

	def openTest(self):
		if self.ipage < self.npage:
			self.maxentry = (self.PIXMAPS_PER_PAGE * self.ipage) - 1
			self.minentry = (self.ipage - 1) * self.PIXMAPS_PER_PAGE

		elif self.ipage == self.npage:
			self.maxentry = len(self.pics) - 1
			self.minentry = (self.ipage - 1) * self.PIXMAPS_PER_PAGE
			i1 = 0
			while i1 < self.PIXMAPS_PER_PAGE:
				self["label" + str(i1 + 1)].setText(" ")
				self["pixmap" + str(i1 + 1)].instance.setPixmapFromFile(dblank)
				i1 += 1
		self.npics = len(self.pics)
		i = 0
		i1 = 0
		self.picnum = 0
		ln = self.maxentry - (self.minentry - 1)
		while i < ln:
			idx = self.minentry + i
			# self["label" + str(i + 1)].setText(self.names[idx])  # this show label to bottom of png pixmap
			pic = self.pics[idx]
			if not os.path.exists(self.pics[idx]):
				pic = dblank
			self["pixmap" + str(i + 1)].instance.setPixmapFromFile(pic)
			i += 1
		self.index = self.minentry
		self.paintFrame()

	def key_left(self):
		# Decrement the index only if we are not at the first pixmap
		if self.index >= 0:
			self.index -= 1
		else:
			# If we are at the first pixmap, go back to the last pixmap of the last page
			self.ipage = self.npage
			self.index = self.npics - 1
		# Check if we need to change pages
		if self.index < self.minentry:
			self.ipage -= 1
			if self.ipage < 1:  # If we go beyond the first page
				self.ipage = self.npage
				self.index = self.npics - 1  # Back to the last pixmap of the last page
			self.openTest()
		else:
			self.paintFrame()

	def key_right(self):
		# Increment the index only if we are not at the last pixmap
		if self.index < self.npics - 1:
			self.index += 1
		else:
			# If we are at the last pixmap, go back to the first pixmap of the first page
			self.index = 0
			self.ipage = 1
			self.openTest()
		# Check if we need to change pages
		if self.index > self.maxentry:
			self.ipage += 1
			if self.ipage > self.npage:  # If we exceed the number of pages
				self.index = 0
				self.ipage = 1  # Back to first page
			self.openTest()
		else:
			self.paintFrame()

	def key_up(self):
		if self.index >= 5:
			self.index -= 5
		else:
			if self.ipage > 1:
				self.ipage -= 1
				self.index = self.maxentry  # Back to the last line of the previous page
				self.openTest()
			else:
				# If we are on the first page, go back to the last pixmap of the last page
				self.ipage = self.npage
				self.index = self.npics - 1
				self.openTest()
		self.paintFrame()

	def key_down(self):
		if self.index <= self.maxentry - 5:
			self.index += 5
		else:
			if self.ipage < self.npage:
				self.ipage += 1
				self.index = self.minentry  # Back to the top of the next page
				self.openTest()
			else:
				# If we are on the last page, go back to the first pixmap of the first page
				self.index = 0
				self.ipage = 1
				self.openTest()

		self.paintFrame()

	def configure(self):
		self.session.open(ConfigEx)

	def about(self):
		self.session.open(startInit)

	def cancel(self):
		self.close()

	def exit(self):
		self.close()

	def showIMDB(self):
		idx = self.index
		text_clear = self.names[idx]
		if returnIMDB(text_clear):
			print('show imdb/tmdb')

	def okClicked(self):
		itype = self.index
		name = self.names[itype]
		url = self.urls[itype]
		modl = name.lower()
		if PY3:
			import importlib.util
			spec = importlib.util.spec_from_file_location(modl, url)
			foo = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(foo)
			print("In GridMain Going in PY3")
		else:
			import imp
			foo = imp.load_source(modl, url)
			print("In GridMain Going in PY2")
		self.session.open(foo.main)


class TvInfoBarShowHide():
	""" InfoBar show/hide control, accepts toggleShow and hide actions, might start
	fancy animations. """
	STATE_HIDDEN = 0
	STATE_HIDING = 1
	STATE_SHOWING = 2
	STATE_SHOWN = 3
	skipToggleShow = False

	def __init__(self):
		self["ShowHideActions"] = ActionMap(["InfobarShowHideActions"], {
			"toggleShow": self.OkPressed,
			"hide": self.hide
		}, 0)

		self.__event_tracker = ServiceEventTracker(screen=self, eventmap={
			iPlayableService.evStart: self.serviceStarted
		})
		self.__state = self.STATE_SHOWN
		self.__locked = 0
		self.hideTimer = eTimer()
		try:
			self.hideTimer_conn = self.hideTimer.timeout.connect(self.doTimerHide)
		except:
			self.hideTimer.callback.append(self.doTimerHide)
		self.hideTimer.start(5000, True)
		self.onShow.append(self.__onShow)
		self.onHide.append(self.__onHide)

	def OkPressed(self):
		self.toggleShow()

	def toggleShow(self):
		if self.skipToggleShow:
			self.skipToggleShow = False
			return
		if self.__state == self.STATE_HIDDEN:
			self.show()
			self.hideTimer.stop()
		else:
			self.hide()
			self.startHideTimer()

	def serviceStarted(self):
		if self.execing:
			if config.usage.show_infobar_on_zap.value:
				self.doShow()

	def __onShow(self):
		self.__state = self.STATE_SHOWN
		self.startHideTimer()

	def startHideTimer(self):
		if self.__state == self.STATE_SHOWN and not self.__locked:
			self.hideTimer.stop()
			idx = config.usage.infobar_timeout.index
			if idx:
				self.hideTimer.start(idx * 1500, True)

	def __onHide(self):
		self.__state = self.STATE_HIDDEN

	def doShow(self):
		self.hideTimer.stop()
		self.show()
		self.startHideTimer()

	def doTimerHide(self):
		self.hideTimer.stop()
		if self.__state == self.STATE_SHOWN:
			self.hide()

	def lockShow(self):
		try:
			self.__locked += 1
		except:
			self.__locked = 0
		if self.execing:
			self.show()
			self.hideTimer.stop()
			self.skipToggleShow = False

	def unlockShow(self):
		try:
			self.__locked -= 1
		except:
			self.__locked = 0
		if self.__locked < 0:
			self.__locked = 0
		if self.execing:
			self.startHideTimer()

	def debug(obj, text=""):
		print(text + " %s\n" % obj)


class Playstream1(Screen):

	def __init__(self, session, name, url):
		Screen.__init__(self, session)
		self.session = session
		skin = os.path.join(skin_path, 'Playstream1.xml')
		with codecs.open(skin, "r", encoding="utf-8") as f:
			self.skin = f.read()
		f.close()
		self.setup_title = ('Select Player Stream')
		self.list = []
		self.name = name
		self.url = url
		self.desc = ''
		self.error_message = ""
		self.last_recvbytes = 0
		self.error_message = None
		self.download = None
		self.aborted = False
		# print('In Playstream1 self.url =', url)
		self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
		self['list'] = rvList([])
		self['info'] = Label()
		self['info'].setText(name)
		self['key_red'] = Button(_('Back'))
		self['key_green'] = Button(_('Select'))
		self['progress'] = ProgressBar()
		self['progresstext'] = StaticText()
		self["progress"].hide()
		self.downloading = False
		self['actions'] = ActionMap(['ColorActions',
									 'CancelActions',
									 'TimerEditActions',
									 'OkCancelActions',
									 'InfobarInstantRecord'], {'red': self.cancel,
															   'green': self.okClicked,
															   'back': self.cancel,
															   'cancel': self.cancel,
															   'rec': self.runRec,
															   'instantRecord': self.runRec,
															   'ShortRecord': self.runRec,
															   'ok': self.okClicked}, -2)
		self.onLayoutFinish.append(self.openTest)
		return

	def runRec(self):
		self.namem3u = self.name
		self.urlm3u = self.url
		if self.downloading is True:
			self.session.open(MessageBox, _('You are already downloading!!!'), MessageBox.TYPE_INFO, timeout=5)
			return
		else:
			if '.mp4' or '.mkv' or '.flv' or '.avi' in self.urlm3u:  # or 'm3u8':
				self.session.openWithCallback(self.download_m3u, MessageBox, _("DOWNLOAD VIDEO?\n%s" % self.namem3u), type=MessageBox.TYPE_YESNO, timeout=10, default=False)
			else:
				self.downloading = False
				self.session.open(MessageBox, _('Only VOD Movie allowed or not .ext Filtered!!!'), MessageBox.TYPE_INFO, timeout=5)

	def download_m3u(self, result):
		if result:
			if 'm3u8' not in self.urlm3u:
				path = urlparse(self.urlm3u).path
				ext = splitext(path)[1]
				if ext not in ['.mp4', '.mkv', '.avi', '.flv']:
					ext = '.mp4'
				# Sostituisco i caratteri indesiderati nel nome del file
				fileTitle = re.sub(r'[<>:"/\\|?*\[\]#()+\'!&]', '_', self.namem3u)  # Rimpiazzo tutti i caratteri indesiderati
				fileTitle = re.sub(r'\s+', '_', fileTitle)  # Rimpiazzo gli spazi con underscore
				fileTitle = re.sub(r'_+', '_', fileTitle)   # Riduco gli underscore consecutivi a uno solo
				# Converto il titolo in minuscolo e aggiungo l'estensione
				fileTitle = fileTitle.lower() + ext
				# Imposto il percorso del file
				self.in_tmp = Path_Movies + fileTitle
				self.downloading = True
				self.download = downloadWithProgress(self.urlm3u, self.in_tmp)
				self.download.addProgress(self.downloadProgress)
				self.download.start().addCallback(self.check).addErrback(self.download_failed)
			else:
				self.downloading = False
				self.session.open(MessageBox, _('Download Failed!!!'), MessageBox.TYPE_INFO, timeout=5)
		else:
			self.downloading = False

	def downloadProgress(self, recvbytes, totalbytes):
		self.last_recvbytes = recvbytes
		self["progress"].show()
		self['progress'].value = int(100 * self.last_recvbytes // float(totalbytes))
		self['progresstext'].text = '%d of %d kBytes (%.2f%%)' % (self.last_recvbytes // 1024, totalbytes // 1024, 100 * self.last_recvbytes // float(totalbytes))

	def check(self, fplug):
		checkfile = self.in_tmp
		if file_exists(checkfile):
			self.downloading = False
			self['progresstext'].text = ''
			self.progclear = 0
			self['progress'].setValue(self.progclear)
			self["progress"].hide()

	def showError(self, error):
		self.downloading = False
		self.session.open(MessageBox, _('Download Failed!!!'), MessageBox.TYPE_INFO, timeout=5)

	def download_failed(self, failure_instance=None, error_message=""):
		self.error_message = error_message
		if error_message == "" and failure_instance is not None:
			self.error_message = failure_instance.getErrorMessage()
		self.downloading = False
		self.session.open(MessageBox, _('Download Failed!!!'), MessageBox.TYPE_INFO, timeout=5)

	def abort(self):
		# print("aborting", self.url)
		if self.download:
			self.download.stop()
		self.aborted = True

	def download_finished(self, string=""):
		if self.aborted:
			self.finish(aborted=True)

	def openTest(self):
		url = self.url
		self.names = []
		self.urls = []
		self.names.append('Play Now')
		self.urls.append(url)
		self.names.append('Download Now-ATTENTION!')
		self.urls.append(url)
		self.names.append('Play HLS')
		self.urls.append(url)
		self.names.append('Play TS')
		self.urls.append(url)
		self.names.append('Streamlink')
		self.urls.append(url)
		self.names.append('YoutubeDl')
		self.urls.append(url)
		showlist(self.names, self['list'])

	def okClicked(self):
		i = len(self.names)
		if i < 0:
			return
		idx = self['list'].getSelectionIndex()
		self.name = self.name  # self.names[idx]
		self.url = self.urls[idx]

		if idx == 0:
			# self.name = self.names[idx]
			self.url = self.urls[idx]
			print('In playVideo url 0=', self.url)
			self.play()

		if idx == 1:
			self.url = self.urls[idx]
			print('In playVideo url 1=', self.url)
			self.runRec()

		elif idx == 2:
			print('In playVideo url B=', self.url)
			# self.name = self.names[idx]
			self.url = self.urls[idx]
			try:
				os.remove('/tmp/hls.avi')
			except:
				pass
			header = ''
			cmd = 'python "/usr/lib/enigma2/python/Plugins/Extensions/xxxplugin/lib/hlsclient.py" "' + self.url + '" "1" "' + header + '" + &'
			print('In playVideo cmd =', cmd)
			os.system(cmd)
			os.system('sleep 3')
			self.url = '/tmp/hls.avi'
			self.play()

		elif idx == 3:
			print('In playVideo url A=', self.url)
			url = self.url
			try:
				os.remove('/tmp/hls.avi')
			except:
				pass
			cmd = 'python "/usr/lib/enigma2/python/Plugins/Extensions/xxxplugin/lib/tsclient.py" "' + url + '" "1" + &'
			print('hls cmd 3= ', cmd)
			os.system(cmd)
			os.system('sleep 3')
			self.url = '/tmp/hls.avi'
			# self.name = self.names[idx]
			self.play()

		elif idx == 4:
			# self.name = self.names[idx]
			self.url = self.urls[idx]
			print('In playVideo url 4=', self.url)
			self.play2()

		elif idx == 5:
			try:
				url = self.url
				if 'embed' in url:
					url = url.replace('embed/', 'watch?v=').replace('?autoplay=1', '').replace('?autoplay=0', '')
				content = Utils.getUrlresp(url)
				if six.PY3:
					content = six.ensure_str(content)
				print("content A =", content)
				# from Plugins.Extensions.xxxplugin.youtube_dl import YoutubeDL
				# from Plugins.Extensions.xxxplugin import youtube_dl
				from .youtube_dl import YoutubeDL
				'''
				ydl_opts = {'format': 'best'}
				ydl_opts = {'format': 'bestaudio/best'}

				ydl_opts = {'format': 'best',
							'no_check_certificate': True,
							}
				'''
				ydl_opts = {'format': 'best'}
				ydl = YoutubeDL(ydl_opts)
				ydl.add_default_info_extractors()
				result = ydl.extract_info(url, download=False)
				self.url = result["url"]
				print("Here in Test url =", url)
				self.session.open(Playstream2, self.name, self.url)
			except:
				pass
		return

	def playfile(self, serverint):
		self.serverList[serverint].play(self.session, self.url, self.name)

	def play(self):
		url = self.url
		name = self.name
		self.session.open(Playstream2, name, url)

	def play2(self):
		if Utils.isStreamlinkAvailable:
			name = self.name
			url = self.url
			url = url.replace(':', '%3a')
			print('In revolution url =', url)
			ref = '5002:0:1:0:0:0:0:0:0:0:' + 'http%3a//127.0.0.1%3a8088/' + str(url)
			sref = eServiceReference(ref)
			print('SREF: ', sref)
			sref.setName(str(name))
			self.session.open(Playstream2, name, sref)
			self.close()
		else:
			self.session.open(MessageBox, _('Install Streamlink first'), MessageBox.TYPE_INFO, timeout=5)

	def cancel(self):
		try:
			self.session.nav.stopService()
			self.session.nav.playService(self.srefInit)
			self.close()
		except:
			pass
			self.close()


class Playstream2(Screen, InfoBarBase, TvInfoBarShowHide, InfoBarSeek, InfoBarAudioSelection, InfoBarSubtitleSupport):
	STATE_IDLE = 0
	STATE_PLAYING = 1
	STATE_PAUSED = 2
	ENABLE_RESUME_SUPPORT = True
	ALLOW_SUSPEND = True
	screen_timeout = 4000

	def __init__(self, session, name, url):
		global streaml, _session
		Screen.__init__(self, session)
		self.session = session
		_session = session
		self.skinName = 'MoviePlayer'
		# title = name
		streaml = False
		self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
		InfoBarBase.__init__(self, steal_current_service=True)
		TvInfoBarShowHide.__init__(self)
		InfoBarSeek.__init__(self, actionmap="InfobarSeekActions")
		InfoBarAudioSelection.__init__(self)
		InfoBarSubtitleSupport.__init__(self)
		# SubsSupport.__init__(self, searchSupport=True, embeddedSupport=True)
		# SubsSupportStatus.__init__(self)

		self.service = None
		self.url = url
		self.name = html_conv.html_unescape(name)
		self.state = self.STATE_PLAYING
		self['actions'] = ActionMap(
			['MoviePlayerActions',
			 'MovieSelectionActions',
			 'MediaPlayerActions',
			 'EPGSelectActions',
			 'MediaPlayerSeekActions',
			 'ColorActions',
			 'OkCancelActions',
			 'InfobarShowHideActions',
			 'InfobarActions',
			 'InfobarSeekActions'],
			{
				'epg': self.showIMDB,
				'info': self.showIMDB,
				# 'info': self.cicleStreamType,
				'tv': self.cicleStreamType,
				'stop': self.leavePlayer,
				'cancel': self.cancel,
				'back': self.cancel
			},
			-1
		)

		if 'youtube' in self.url:
			self.onFirstExecBegin.append(self.slinkPlay)
		elif '8088' in str(self.url):
			self.onFirstExecBegin.append(self.slinkPlay)
		else:
			self.onFirstExecBegin.append(self.cicleStreamType)
		return

	def showIMDB(self):
		try:
			text_clear = self.name
			if returnIMDB(text_clear):
				print('show imdb/tmdb')
		except Exception as ex:
			print(str(ex))
			print("Error: can't find Playstream2 in live_to_stream")

	def slinkPlay(self):
		url = self.url
		name = self.name
		ref = "{0}:{1}".format(url.replace(":", "%3a"), name.replace(":", "%3a"))
		print('final reference:   ', ref)
		sref = eServiceReference(ref)
		self.sref = sref
		sref.setName(str(name))
		self.session.nav.stopService()
		self.session.nav.playService(sref)

	def openPlay(self, servicetype, url):
		name = self.name
		ref = "{0}:0:1:0:0:0:0:0:0:0:{1}:{2}".format(servicetype, url.replace(":", "%3a"), name.replace(":", "%3a"))
		print('reference:   ', ref)
		if streaml is True:
			url = 'http://127.0.0.1:8088/' + str(url)
			ref = "{0}:0:1:0:0:0:0:0:0:0:{1}:{2}".format(servicetype, url.replace(":", "%3a"), name.replace(":", "%3a"))
			print('streaml reference:   ', ref)
		print('final reference:   ', ref)
		sref = eServiceReference(ref)
		self.sref = sref
		sref.setName(str(name))
		self.session.nav.stopService()
		self.session.nav.playService(sref)

	def cicleStreamType(self):
		# global streaml
		# from itertools import cycle, islice
		self.servicetype = str(cfg.services.value)
		print('servicetype1: ', self.servicetype)
		url = str(self.url)
		if str(splitext(url)[-1]) == ".m3u8":
			if self.servicetype == "1":
				self.servicetype = "4097"
		# currentindex = 0
		# streamtypelist = ["4097"]
		"""
		# if "youtube" in str(self.url):
			# self.mbox = self.session.open(MessageBox, _('For Stream Youtube coming soon!'), MessageBox.TYPE_INFO, timeout=5)
			# return
		# if Utils.isStreamlinkAvailable():
			# streamtypelist.append("5002")  # ref = '5002:0:1:0:0:0:0:0:0:0:http%3a//127.0.0.1%3a8088/' + url
			# streaml = True
		# elif file_exists("/usr/bin/gstplayer"):
			# streamtypelist.append("5001")
		# if file_exists("/usr/bin/exteplayer3"):
			# streamtypelist.append("5002")
			"""
		'''
		# if file_exists("/usr/bin/apt-get"):
			# streamtypelist.append("8193")
		# for index, item in enumerate(streamtypelist, start=0):
			# if str(item) == str(self.servicetype):
				# currentindex = index
				# break
		# nextStreamType = islice(cycle(streamtypelist), currentindex + 1, None)
		# self.servicetype = str(next(nextStreamType))
		'''
		print('servicetype2: ', self.servicetype)
		self.openPlay(self.servicetype, url)

	def up(self):
		pass

	def down(self):
		self.up()

	def doEofInternal(self, playing):
		self.close()

	def __evEOF(self):
		self.end = True

	def showVideoInfo(self):
		if self.shown:
			self.hideInfobar()
		if self.infoCallback is not None:
			self.infoCallback()
		return

	def showAfterSeek(self):
		if isinstance(self, TvInfoBarShowHide):
			self.doShow()

	def cancel(self):
		if file_exists('/tmp/hls.avi'):
			os.remove('/tmp/hls.avi')
		self.session.nav.stopService()
		self.session.nav.playService(self.srefInit)
		aspect_manager.restore_aspect()
		self.leavePlayer()

	def leavePlayer(self):
		self.close()


class startInit(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		global _session
		_session = session
		skin = os.path.join(skin_path, 'start.xml')
		with codecs.open(skin, "r", encoding="utf-8") as f:
			self.skin = f.read()
		info = 'Please Wait..'
		# self['info'] = Label('')
		self['text'] = ScrollLabel(info)
		self['actions'] = ActionMap(['OkCancelActions',
									 'ColorActions',
									 'DirectionActions'], {'cancel': self.close,
														   'red': self.close,
														   'ok': self.ok,
														   'up': self.Up,
														   'down': self.Down,
														   }, -1)

		self.timer = eTimer()
		if Utils.DreamOS():
			self.timer_conn = self.timer.timeout.connect(self.startSession)
		else:
			self.timer.callback.append(self.startSession)
		self.timer.start(100, 1)

	def ok(self):
		self.close()

	def Down(self):
		self['text'].pageDown()

	def Up(self):
		self['text'].pageUp()

	def getinfo(self):
		continfo = _("WELCOME TO XXXPLUGIN V.%s\n\n") % Version
		continfo += _("ATTENTION PLEASE: \n")
		continfo += _("This plugin contains adult content not\n")
		continfo += _("suitable for all readers.\n")
		continfo += _("If you are over 18 years old and wish to\n")
		continfo += _("use the aforementioned content.\n\n")
		continfo += _("For Support visit our social links go to\n")
		continfo += _("tivustream.com or corvoboys.org and ask\n")
		continfo += _("about this plugins.\n\n")
		continfo += _("Thank you with all my heart\n")
		continfo += _("Just for passion!!! @Lululla.\n\n")
		continfo += _("if you like what we do and how we do it\n")
		continfo += _("do we deserve a coffee.\n\n")
		continfo += _("QRCODE € 1,00\n")
		continfo += _("Donate now\n\n")
		continfo += _("=========     SUPPORT ON:   ============\n")
		continfo += _("+WWW.TIVUSTREAM.COM - WWW.CORVOBOYS.ORG+\n")
		continfo += _("http://t.me/tivustream\n\n")
		continfo += _("THANK'S TO:\n")
		continfo += _("@PCD\n@KIDDAC\n@MMARK\n@OKTUS\nand to: linuxsat-support forum")
		return continfo

	def startSession(self):
		try:
			self['text'].setText(self.getinfo())
		except:
			self['text'].setText(_('Error Report Issue!'))
		self.timer.startLongTimer(60)
		# self.timer.start(600, 1)
		# self.contdown()


def main(session, **kwargs):
	try:
		_session = session

		try:
			os.mkdir(os.path.join(Path_Cache, ""))
		except:
			pass

		try:
			os.mkdir(os.path.join(Path_Cache, "pic"))
		except:
			pass

		try:
			os.mkdir(os.path.join(Path_Cache, "tmp"))
		except:
			pass
		exo = Main(_session)
		exo.startSession()
	except:
		import traceback
		traceback.print_exc()
		pass


def Plugins(**kwargs):
	icona = 'icon.png'
	extDescriptor = PluginDescriptor(name=name_plug, description=_(title_plug), where=PluginDescriptor.WHERE_EXTENSIONSMENU, icon=icona, fnc=main)
	result = [PluginDescriptor(name=name_plug, description=title_plug, where=PluginDescriptor.WHERE_PLUGINMENU, icon=icona, fnc=main)]
	result.append(extDescriptor)
	return result
