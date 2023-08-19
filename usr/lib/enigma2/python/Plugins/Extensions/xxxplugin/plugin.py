#!/usr/bin/python
# -*- coding: utf-8 -*-

# '''
# Info http://t.me/tivustream
# ****************************************
# *        coded by Lululla              *
# *          skin by MMark               *
# *             02/07/2023               *
# ****************************************
# '''

from __future__ import print_function
from . import _, skin_path, screenwidth
from .lib import Utils
from .lib import html_conv
try:
    from Components.AVSwitch import eAVSwitch
except Exception:
    from Components.AVSwitch import iAVSwitch as eAVSwitch
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.config import config, ConfigSubsection
from Components.config import ConfigSelection, getConfigListEntry
from Components.config import ConfigDirectory, ConfigYesNo
from Components.config import configfile, ConfigEnableDisable
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText
from Components.MultiContent import MultiContentEntryPixmapAlphaTest
from Components.Pixmap import Pixmap, MovingPixmap
from Components.ProgressBar import ProgressBar
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from enigma import eListboxPythonMultiContent, eServiceReference
from enigma import eTimer
from enigma import gFont
from enigma import iPlayableService
from enigma import loadPNG
from enigma import RT_HALIGN_LEFT, RT_VALIGN_CENTER
from os.path import splitext
from Plugins.Plugin import PluginDescriptor
from PIL import Image, ImageFile, ImageChops
from Screens.InfoBarGenerics import InfoBarSubtitleSupport
from Screens.InfoBarGenerics import InfoBarSeek, InfoBarAudioSelection
from Screens.LocationBox import LocationBox
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Tools.Downloader import downloadWithProgress
from requests import get, exceptions
from requests.exceptions import HTTPError
from twisted.internet.reactor import callInThread
from os.path import exists as file_exists
import os
import re
import requests
import sys
# import json
import six
ImageFile.LOAD_TRUNCATED_IMAGES = True
_session = None
THISPLUG = '/usr/lib/enigma2/python/Plugins/Extensions/xxxplugin/'
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


global defpic, dblank
# _firstStartxxxplugin = True
_session = None

currversion = getversioninfo()
Version = currversion + ' - 12.07.2023'
title_plug = '..:: XXX Revolution V. %s ::..' % Version
folder_path = "/tmp/xplugin/"
name_plug = 'XXX Revolution'
piccons = os.path.join(THISPLUG, 'res/img/')
res_plugin_path = os.path.join(THISPLUG, 'res/')
pngx = os.path.join(res_plugin_path, 'pics/setting2.png')

if not file_exists(folder_path):
    os.makedirs(folder_path)

# screenwidth = getDesktop(0).size()
if screenwidth.width() == 2560:
    defpic = THISPLUG + 'res/img/no_work.png'
    dblank = THISPLUG + 'res/img/undefinided.png'

elif screenwidth.width() == 1920:
    defpic = THISPLUG + 'res/img/no_work.png'
    dblank = THISPLUG + 'res/img/undefinided.png'
else:
    defpic = THISPLUG + 'res/img/no_work.png'
    dblank = THISPLUG + 'res/img/undefinided.png'


class rvList(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, False, eListboxPythonMultiContent)
        if screenwidth.width() == 2560:
            self.l.setItemHeight(60)
            textfont = int(42)
            self.l.setFont(0, gFont('Regular', textfont))
        elif screenwidth.width() == 1920:
            self.l.setItemHeight(50)
            textfont = int(30)
            self.l.setFont(0, gFont('Regular', textfont))
        else:
            self.l.setItemHeight(50)
            textfont = int(24)
            self.l.setFont(0, gFont('Regular', textfont))


def rvoneListEntry(name):
    res = [name]
    pngx = os.path.join(res_plugin_path, 'pics/setting2.png')
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
        icount += 1
        list.setList(plist)


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


mdpchoices = [
        ("4097", _("IPTV(4097)")),
        ("1", _("Dvb(1)")),
        ("8193", _("eServiceUri(8193)")),
    ]

if file_exists("/usr/bin/gstplayer"):
    mdpchoices.append(("5001", _("Gstreamer(5001)")))

if file_exists("/usr/bin/exteplayer3"):
    mdpchoices.append(("5002", _("Exteplayer3(5002)")))

if file_exists("/usr/bin/apt-get"):
    mdpchoices.append(("8193", _("DreamOS GStreamer(8193)")))

config.plugins.xxxplugin = ConfigSubsection()
cfg = config.plugins.xxxplugin
cfg.services = ConfigSelection(default='4097', choices=mdpchoices)
cfg.thumb = ConfigSelection(default="True", choices=[("True", _("yes")), ("False", _("no"))])
cfg.cachefold = ConfigDirectory("/media/hdd", False)
cfg.movie = ConfigDirectory("/media/hdd/movie")


try:
    from Components.UsageConfig import defaultMoviePath
    downloadpath = defaultMoviePath()
    cfg.movie = ConfigDirectory(default=downloadpath)
except:
    if file_exists("/usr/bin/apt-get"):
        cfg.movie = ConfigDirectory(default='/media/hdd/movie')


global Path_Movies, Path_Cache

Path_Movies = str(cfg.movie.value)
Path_Cache = str(cfg.cachefold.value)
print('Path Movies: ', Path_Movies)
print('Path Cache: ', Path_Cache)


def returnIMDB(text_clear):
    from Tools.Directories import SCOPE_PLUGINS, resolveFilename
    TMDB = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('TMDB'))
    IMDb = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('IMDb'))
    if file_exists(TMDB):
        try:
            from Plugins.Extensions.TMBD.plugin import TMBD
            text = html_conv.html_unescape(text_clear)
            _session.open(TMBD.tmdbScreen, text, 0)
        except Exception as e:
            print("[XCF] Tmdb: ", e)
        return True
    elif file_exists(IMDb):
        try:
            from Plugins.Extensions.IMDb.plugin import main as imdb
            text = html_conv.html_unescape(text_clear)
            imdb(_session, text)
        except Exception as e:
            print("[XCF] imdb: ", e)
        return True
    else:
        text_clear = html_conv.html_unescape(text_clear)
        _session.open(MessageBox, text_clear, MessageBox.TYPE_INFO)
        return True
    return False


def threadGetPage(url=None, file=None, key=None, success=None, fail=None, *args, **kwargs):
    print('[xxxplugin][threadGetPage] url, file, key, args, kwargs', url, "   ", file, "   ", key, "   ", args, "   ", kwargs)
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
    # from PIL import Image
    # global defpic
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
        # test remove this
        # if file_exists(tpicf):
            # cmd = "rm " + tpicf
            # os.system(cmd)
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
                        # if PY3:
                            # poster = poster.encode()
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
                                # print("Going in urlopen url =", url)
                                # p = Utils.gettUrl(url)
                                # with open(tpicf, 'wb') as f1:
                                    # f1.write(p)
                                try:
                                    with open(tpicf, 'wb') as f:
                                        f.write(requests.get(url, stream=True, allow_redirects=True).content)
                                    print('=============11111111=================\n')
                                except Exception as e:
                                    print("Error: Exception")
                                    print('===========2222222222=================\n')
                                    # if PY3:
                                        # poster = poster.encode()
                                    callInThread(threadGetPage, url=poster, file=tpicf, success=downloadPic, fail=downloadError)

                                    '''
                                    print(e)
                                    open(tpicf, 'wb').write(requests.get(poster, stream=True, allow_redirects=True).content)
                                    '''
                            except Exception as e:
                                print("Error: Exception 2")
                                print(e)

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
                    size = [220, 330]
                else:
                    size = [150, 220]

                file_name, file_extension = splitext(tpicf)
                try:
                    im = Image.open(tpicf).convert("RGBA")
                    # shrink if larger
                    try:
                        im.thumbnail(size, Image.Resampling.LANCZOS)
                    except:
                        im.thumbnail(size, Image.ANTIALIAS)
                    imagew, imageh = im.size
                    # enlarge if smaller
                    try:
                        if imagew < size[0]:
                            ratio = size[0] / imagew
                            try:
                                im = im.resize((int(imagew * ratio), int(imageh * ratio)), Image.Resampling.LANCZOS)
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
                        im.thumbnail(size, Image.Resampling.LANCZOS)
                    except:
                        im.thumbnail(size, Image.ANTIALIAS)
                    im.save(tpicf)
            except Exception as e:
                print("******* picon resize failed *******")
                print(e)
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


class Abouttvr(Screen):
    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        skin = os.path.join(skin_path, 'Abouttvr.xml')
        with open(skin, 'r') as f:
            self.skin = f.read()
        title = _(name_plug)
        self["title"] = Button(title)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = ActionMap(["WizardActions", "InputActions", "ColorActions", 'ButtonSetupActions', "DirectionActions"], {
            "ok": self.okClicked,
            "back": self.close,
            "cancel": self.cancel,
            "red": self.close,
            "green": self.okClicked
        }, -1)
        self.onLayoutFinish.append(self.startSession)

    def startSession(self):
        self['info'].setText(self.getinfo())

    def okClicked(self):
        Screen.close(self, False)

    def getinfo(self):
        continfo = _("==  WELCOME to WWW.TIVUSTREAM.COM ==\n")
        continfo += _("== SUPPORT ON: WWW.CORVOBOYS.ORG http://t.me/tivustream ==\n")
        continfo += _("== thank's to @PCD @KIDDAC @MMARK @LINUXSAT-SUPPORT.COM\n")
        continfo += _("========================================\n")
        continfo += _("DISCLAIMER:\n")
        continfo += _("The lists created at HOC contain addresses freely and freely found on\n")
        continfo += _("the net and not protected by subscription or subscription.\n")
        continfo += _("The structural reference server for projects released\n")
        continfo += _("is not a source of any stream/flow.\n")
        continfo += _("Absolutely PROHIBITED to use this lists without authorization\n")
        continfo += _("========================================\n")
        return continfo

    def keyLeft(self):
        self['list'].left()

    def keyRight(self):
        self['list'].right()

    def cancel(self):
        self.close()


class ConfigEx(ConfigListScreen, Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        skin = os.path.join(skin_path, 'Config.xml')
        if file_exists('/var/lib/dpkg/status'):
            skin = os.path.join(skin_path, 'ConfigOs.xml')
        with open(skin, 'r') as f:
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
        fold = os.path.join(str(cfg.cachefold.value), "xxxplugin/pic")
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
            if isinstance(self['config'].getCurrent()[1], ConfigEnableDisable) or isinstance(self['config'].getCurrent()[1], ConfigYesNo) or isinstance(self['config'].getCurrent()[1], ConfigSelection):
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
        self["menu"] = List(self.list)
        self["menu"] = rvList([])
        self["title"] = Button(name_plug)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = ActionMap(["WizardActions",
                                     "InputActions",
                                     "ColorActions",
                                     "ButtonSetupActions",
                                     "DirectionActions"], {
                                                            "ok": self.okClicked,
                                                            "back": self.close,
                                                            "red": self.close,
                                                            "green": self.okClicked,
                                                           }, -1)
        self.onLayoutFinish.append(self.startSession)

    def startSession(self):
        self.names = []
        self.urls = []
        self.pics = []
        # sort test
        items = []
        # sort test
        i = 0
        name = ""
        desc = ""
        pic = ""
        url = ""
        path = THISPLUG + "Sites"
        print('path= ', path)
        try:
            for root, dirs, files in os.walk(path):
                # print(files)
                for file in files:
                    if file.endswith('.py') and not file.endswith('.pyo') and not file.endswith('.pyc'):
                        print('name= ', file)
                        if "pycache" in file:
                            continue
                        if 'extractor' in file:
                            continue
                        if 'init' in file:
                            continue
                        if 'Utils' in file:
                            continue
                        if 'html_conv' in file:
                            continue
                        if 'no_work' in file:
                            continue
                        name, ext = file.split(".")  # [-1]
                        desc = 'XXX %s' % name
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
                    print(name + '\n' + desc + '\n' + url + '\n' + pic)
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
        with open(skin, 'r') as f:
            self.skin = f.read()
        title = menuTitle
        self.name = menuTitle
        self["title"] = Button(title)

        self.pos = []

        if screenwidth.width() == 2560:
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
            self.pos.append([122, 42])
            self.pos.append([478, 42])
            self.pos.append([834, 42])
            self.pos.append([1190, 42])
            self.pos.append([1546, 42])
            self.pos.append([122, 522])
            self.pos.append([478, 522])
            self.pos.append([834, 522])
            self.pos.append([1190, 522])
            self.pos.append([1546, 522])
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

        tmpfold = os.path.join(str(cfg.cachefold.value), "xxxplugin/tmp")
        picfold = os.path.join(str(cfg.cachefold.value), "xxxplugin/pic")

        picx = getpics(names, pics, tmpfold, picfold)
        print("In Gridmain pics = ", pics)

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
        i = 0
        while i < 20:
            self["label" + str(i + 1)] = StaticText()
            self["pixmap" + str(i + 1)] = Pixmap()
            i += 1
        # i = 0
        self.index = 0
        self.ipage = 1
        ln = len(self.names)
        self.npage = int(float(ln / 10)) + 1
        print("self.npage =", self.npage)
        self["actions"] = ActionMap(["OkCancelActions",
                                     "EPGSelectActions",
                                     "MenuActions",
                                     "DirectionActions",
                                     "NumberActions"], {
                                                        "ok": self.okClicked,
                                                        "epg": self.showIMDB,
                                                        "info": self.about,
                                                        "cancel": self.cancel,
                                                        "menu": self.configure,
                                                        "left": self.key_left,
                                                        "right": self.key_right,
                                                        "up": self.key_up,
                                                        "down": self.key_down
                                                       })

        print("Going in openTest")
        self.onLayoutFinish.append(self.openTest)

    def configure(self):
        self.session.open(ConfigEx)

    def about(self):
        self.session.open(Abouttvr)

    def cancel(self):
        self.close()

    def exit(self):
        self.close()

    def showIMDB(self):
        idx = self.index
        text_clear = self.names[idx]
        if returnIMDB(text_clear):
            print('show imdb/tmdb')

    def paintFrame(self):
        try:
            ifr = self.index - (10 * (self.ipage - 1))
            # print("ifr =", ifr)
            ipos = self.pos[ifr]
            # print("ipos =", ipos)
            self["frame"].moveTo(ipos[0], ipos[1], 1)
            self["frame"].startMoving()
            # self.info()
        except Exception as e:
            print('error  in paintframe: ', e)

    def openTest(self):
        print("self.index, openTest self.ipage, self.npage =", self.index, self.ipage, self.npage)
        if self.ipage < self.npage:
            self.maxentry = (10 * self.ipage) - 1
            self.minentry = (self.ipage - 1) * 10
            print("self.ipage , self.minentry, self.maxentry =", self.ipage, self.minentry, self.maxentry)

        elif self.ipage == self.npage:
            print("self.ipage , len(self.pics) =", self.ipage, len(self.pics))
            self.maxentry = len(self.pics) - 1
            self.minentry = (self.ipage - 1) * 10
            print("self.ipage , self.minentry, self.maxentry B=", self.ipage, self.minentry, self.maxentry)
            i1 = 0
            blpic = dblank
            while i1 < 12:
                self["label" + str(i1 + 1)].setText(" ")
                self["pixmap" + str(i1 + 1)].instance.setPixmapFromFile(blpic)
                i1 += 1
        print("len(self.pics), self.minentry, self.maxentry =", len(self.pics), self.minentry, self.maxentry)
        self.npics = len(self.pics)
        i = 0
        i1 = 0
        self.picnum = 0
        ln = self.maxentry - (self.minentry - 1)
        while i < ln:
            idx = self.minentry + i
            self["label" + str(i + 1)].setText(self.names[idx])
            pic = self.pics[idx]
            if file_exists(pic):
                print("pic path exists")
            else:
                print("pic path not exists")
            picd = defpic
            file_name, file_extension = splitext(pic)
            if file_extension != ".png":
                pic = str(file_name) + ".png"
            if self["pixmap" + str(i + 1)].instance:
                try:
                    self["pixmap" + str(i + 1)].instance.setPixmapFromFile(pic)  # ok
                except Exception as e:
                    print(e)
                    self["pixmap" + str(i + 1)].instance.setPixmapFromFile(picd)
            i += 1

        self.index = self.minentry
        self.paintFrame()

    def key_left(self):
        self.index -= 1
        if self.index < 0:
            self.index = self.maxentry
            self.key_up()
        else:
            self.paintFrame()

    def key_right(self):
        i = self.npics - 1
        if self.index == i:
            self.index = 0
            self.ipage = 1
            self.openTest()
        self.index += 1
        if self.index > self.maxentry:
            self.index = 0
            self.key_down()
        else:
            self.paintFrame()

    def key_up(self):
        self.index = self.index - 5
        if self.index < (self.minentry):
            if self.ipage > 1:
                self.ipage = self.ipage - 1
                self.openTest()
            elif self.ipage == 1:
                return
            else:
                self.index = 0
            self.paintFrame()
        else:
            self.paintFrame()

    def key_down(self):
        self.index = self.index + 5
        if self.index > (self.maxentry):
            if self.ipage < self.npage:
                self.ipage = self.ipage + 1
                self.openTest()
            elif self.ipage == self.npage:
                self.index = 0
                self.ipage = 1
                self.openTest()
            else:
                self.index = 0
            self.paintFrame()
        else:
            self.paintFrame()

    def okClicked(self):
        itype = self.index
        name = self.names[itype]
        url = self.urls[itype]
        if PY3:
            modl = name.lower()
            import importlib.util
            spec = importlib.util.spec_from_file_location(modl, url)
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            print("In GridMain Going in PY3")
            self.session.open(foo.main)
        else:
            modl = name.lower()
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
        with open(skin, 'r') as f:
            self.skin = f.read()
        f.close()
        self.setup_title = ('Select Player Stream')
        self.list = []
        self.name1 = name
        self.url = url
        self.desc = ''
        print('In Playstream1 self.url =', url)
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
        self.namem3u = self.name1
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
                if ext != '.mp4' or ext != '.mkv' or ext != '.avi' or ext != '.flv':  # or ext != 'm3u8':
                    ext = '.mp4'
                fileTitle = re.sub(r'[\<\>\:\"\/\\\|\?\*\[\]]', '_', self.namem3u)
                fileTitle = re.sub(r' ', '_', fileTitle)
                fileTitle = re.sub(r'_+', '_', fileTitle)
                fileTitle = fileTitle.replace("(", "_").replace(")", "_").replace("#", "").replace("+", "_").replace("\'", "_").replace("'", "_").replace("!", "_").replace("&", "_")
                fileTitle = fileTitle.lower() + ext
                self.in_tmp = Path_Movies + fileTitle
                self.downloading = True
                self.download = downloadWithProgress(self.urlm3u, self.in_tmp)
                self.download.addProgress(self.downloadProgress)
                self.download.start().addCallback(self.check).addErrback(self.showError)
            else:
                self.downloading = False
                self.session.open(MessageBox, _('Download Failed!!!'), MessageBox.TYPE_INFO, timeout=5)
        else:
            self.downloading = False

    def downloadProgress(self, recvbytes, totalbytes):
        self["progress"].show()
        self['progress'].value = int(100 * recvbytes / float(totalbytes))
        self['progresstext'].text = '%d of %d kBytes (%.2f%%)' % (recvbytes / 1024, totalbytes / 1024, 100 * recvbytes / float(totalbytes))

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
        print('iiiiii= ', i)
        if i < 0:
            return
        idx = self['list'].getSelectionIndex()
        self.name = self.names[idx]
        self.url = self.urls[idx]
        if "youtube" in str(self.url):
            # desc = self.desc
            try:
                from Plugins.Extensions.xxxplugin.youtube_dl import YoutubeDL
                '''
                ydl_opts = {'format': 'best'}
                ydl_opts = {'format': 'bestaudio/best'}
                '''
                ydl_opts = {'format': 'best'}
                ydl = YoutubeDL(ydl_opts)
                ydl.add_default_info_extractors()
                result = ydl.extract_info(self.url, download=False)
                self.url = result["url"]
            except:
                pass
            self.session.open(Playstream2, self.name, self.url)

        if idx == 0:
            self.name = self.names[idx]
            self.url = self.urls[idx]
            print('In playVideo url D=', self.url)
            self.play()

        if idx == 1:
            self.url = self.urls[idx]
            print('In playVideo url D=', self.url)
            self.runRec()

        elif idx == 2:
            print('In playVideo url B=', self.url)
            self.name = self.names[idx]
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
            print('hls cmd = ', cmd)
            os.system(cmd)
            os.system('sleep 3')
            self.url = '/tmp/hls.avi'
            self.name = self.names[idx]
            self.play()

        elif idx == 4:
            self.name = self.names[idx]
            self.url = self.urls[idx]
            print('In playVideo url D=', self.url)
            self.play2()

        elif idx == 5:
            try:
                url = self.url
                content = Utils.getUrlresp(url)
                if six.PY3:
                    content = six.ensure_str(content)
                print("content A =", content)

                from Plugins.Extensions.xxxplugin.youtube_dl import YoutubeDL
                '''
                ydl_opts = {'format': 'best'}
                ydl_opts = {'format': 'bestaudio/best'}
                '''
                ydl_opts = {'format': 'best'}
                ydl = YoutubeDL(ydl_opts)
                ydl.add_default_info_extractors()
                result = ydl.extract_info(content, download=False)
                self.url = result["url"]
            except:
                pass
            self.session.open(Playstream2, self.name, self.url)

        return

    def playfile(self, serverint):
        self.serverList[serverint].play(self.session, self.url, self.name)

    def play(self):
        url = self.url
        name = self.name1
        self.session.open(Playstream2, name, url)

    def play2(self):
        if Utils.isStreamlinkAvailable:
            name = self.name1
            url = self.url
            url = url.replace(':', '%3a')
            print('In revolution url =', url)
            ref = '5002:0:1:0:0:0:0:0:0:0:' + 'http%3a//127.0.0.1%3a8088/' + str(url)
            sref = eServiceReference(ref)
            print('SREF: ', sref)
            sref.setName(name)
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
        title = name
        streaml = False
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
        InfoBarBase.__init__(self, steal_current_service=True)
        TvInfoBarShowHide.__init__(self)
        InfoBarSeek.__init__(self, actionmap="InfobarSeekActions")
        InfoBarAudioSelection.__init__(self)
        InfoBarSubtitleSupport.__init__(self)
        # SubsSupport.__init__(self, searchSupport=True, embeddedSupport=True)
        # SubsSupportStatus.__init__(self)
        try:
            self.init_aspect = int(self.getAspect())
        except:
            self.init_aspect = 0
        self.new_aspect = self.init_aspect
        self.service = None
        self.url = url
        self.name = html_conv.html_unescape(name)
        self.state = self.STATE_PLAYING
        self['actions'] = ActionMap(['MoviePlayerActions',
                                     'MovieSelectionActions',
                                     'MediaPlayerActions',
                                     'EPGSelectActions',
                                     'MediaPlayerSeekActions',
                                     'ColorActions',
                                     'OkCancelActions',
                                     'InfobarShowHideActions',
                                     'InfobarActions',
                                     'InfobarSeekActions'], {'epg': self.showIMDB,
                                                             'info': self.showIMDB,
                                                             # 'info': self.cicleStreamType,
                                                             'tv': self.cicleStreamType,
                                                             'stop': self.leavePlayer,
                                                             'cancel': self.cancel,
                                                             'back': self.cancel}, -1)

        if '8088' in str(self.url):
            self.onFirstExecBegin.append(self.slinkPlay)
        else:
            self.onFirstExecBegin.append(self.cicleStreamType)

    def getAspect(self):
        return eAVSwitch().getAspectRatioSetting()

    def getAspectString(self, aspectnum):
        return {0: '4:3 Letterbox',
                1: '4:3 PanScan',
                2: '16:9',
                3: '16:9 always',
                4: '16:10 Letterbox',
                5: '16:10 PanScan',
                6: '16:9 Letterbox'}[aspectnum]

    def setAspect(self, aspect):
        map = {0: '4_3_letterbox',
               1: '4_3_panscan',
               2: '16_9',
               3: '16_9_always',
               4: '16_10_letterbox',
               5: '16_10_panscan',
               6: '16_9_letterbox'}
        config.av.aspectratio.setValue(map[aspect])
        try:
            eAVSwitch().setAspectRatio(aspect)
        except:
            pass

    def av(self):
        temp = int(self.getAspect())
        temp += 1
        if temp > 6:
            temp = 0
        self.new_aspect = temp
        self.setAspect(temp)

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
        sref.setName(name)
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
        sref.setName(name)
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
        # if file_exists("/usr/bin/apt-get"):
            # streamtypelist.append("8193")
        # for index, item in enumerate(streamtypelist, start=0):
            # if str(item) == str(self.servicetype):
                # currentindex = index
                # break
        # nextStreamType = islice(cycle(streamtypelist), currentindex + 1, None)
        # self.servicetype = str(next(nextStreamType))
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
        if not self.new_aspect == self.init_aspect:
            try:
                self.setAspect(self.init_aspect)
            except:
                pass
        self.close()

    def leavePlayer(self):
        self.close()


class AutoStartTimerxxxplugin:

    def __init__(self, session):
        self.session = session
        global _firstStartxxxplugin
        if _firstStartxxxplugin:
            self.runUpdate()

    def runUpdate(self):
        print("*** running update ***")
        try:
            from . import Update
            Update.upd_done()
            _firstStartxxxplugin = False
        except Exception as e:
            print('error _firstStartxxxplugin', e)


def autostart(reason, session=None, **kwargs):
    global autoStartTimerxplugin
    global _firstStartxxxplugin
    if reason == 0:
        if session is not None:
            _firstStartxxxplugin = True
            autoStartTimerxplugin = AutoStartTimerxxxplugin(session)
    return


def main(session, **kwargs):
    try:
        _session = session

        try:
            os.mkdir(os.path.join(str(cfg.cachefold.value), "xxxplugin"))
        except:
            pass

        try:
            os.mkdir(os.path.join(str(cfg.cachefold.value), "xxxplugin/vid"))
        except:
            pass

        try:
            os.mkdir(os.path.join(str(cfg.cachefold.value), "xxxplugin/pic"))
        except:
            pass

        try:
            os.mkdir(os.path.join(str(cfg.cachefold.value), "xxxplugin/tmp"))
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
    result = [PluginDescriptor(name=name_plug, description=title_plug, where=PluginDescriptor.WHERE_PLUGINMENU, icon=icona, fnc=main),
              PluginDescriptor(name=name_plug, description=title_plug, where=[PluginDescriptor.WHERE_SESSIONSTART], fnc=autostart)]
    result.append(extDescriptor)
    return result
