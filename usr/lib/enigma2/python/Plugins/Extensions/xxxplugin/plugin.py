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
from Components.AVSwitch import AVSwitch
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
from enigma import eListboxPythonMultiContent, eServiceReference, eTimer, gFont, iPlayableService, loadPNG, RT_HALIGN_LEFT, RT_VALIGN_CENTER
from itertools import cycle, islice
from os.path import splitext
from Plugins.Plugin import PluginDescriptor
from PIL import Image, ImageFile, ImageChops
from Screens.InfoBarGenerics import InfoBarMenu, InfoBarSubtitleSupport, InfoBarNotifications, InfoBarSeek, InfoBarAudioSelection
from Screens.LocationBox import LocationBox
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Tools.Directories import SCOPE_PLUGINS, resolveFilename
from Tools.Downloader import downloadWithProgress
from enigma import getDesktop
from requests import get, exceptions
from requests.exceptions import HTTPError
from twisted.internet.reactor import callInThread
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
    currversion = '1.8'
    version_file = os.path.join(THISPLUG, 'version')
    if os.path.exists(version_file):
        try:
            fp = open(version_file, 'r').readlines()
            for line in fp:
                if 'version' in line:
                    currversion = line.split('=')[1].strip()
        except:
            pass
    return (currversion)


global defpic, dblank
_firstStartxxxplugin = True
_session = None

currversion = getversioninfo()
Version = currversion + ' - 12.07.2023'
title_plug = '..:: XXX Revolution V. %s ::..' % Version
folder_path = "/tmp/xxxplugin/"
name_plug = 'XXX Revolution'
piccons = os.path.join(THISPLUG, 'res/img/')
# piconinter = os.path.join(piccons, 'inter.png')
# piconlive = os.path.join(piccons, 'tv.png')
# piconmovie = os.path.join(piccons, 'cinema.png')
# piconsearch = os.path.join(piccons, 'search.png')
# piconseries = os.path.join(piccons, 'series.png')
# pixmaps = os.path.join(piccons, 'backg.png')
# nextpng = 'next.png'
# prevpng = 'prev.png'
res_plugin_path = os.path.join(THISPLUG, 'res/')
pngx = os.path.join(res_plugin_path, 'pics/setting2.png')


if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# screenwidth = getDesktop(0).size()
if screenwidth.width() == 2560:
    defpic = THISPLUG + '/res/pics/no_work.png'
    dblank = THISPLUG + '/res/pics/backg2.png'

elif screenwidth.width() == 1920:
    defpic = THISPLUG + '/res/pics/no_work.png'
    dblank = THISPLUG + '/res/pics/backg2.png'
else:
    defpic = THISPLUG + '/res/pics/no_work.png'
    dblank = THISPLUG + '/res/pics/backg2.png'


# # https twisted client hack #
# try:
    # from twisted.internet import ssl
    # from twisted.internet._sslverify import ClientTLSOptions
    # sslverify = True
# except:
    # sslverify = False

# if sslverify:
    # class SNIFactory(ssl.ClientContextFactory):
        # def __init__(self, hostname=None):
            # self.hostname = hostname

        # def getContext(self):
            # ctx = self._contextFactory(self.method)
            # if self.hostname:
                # ClientTLSOptions(self.hostname, ctx)
            # return ctx


# def piconlocal(name):

    # pngs = [
        # ["tv", "movie"],
        # ["commedia", "commedia"],
        # ["comedy", "commedia"],
        # ["thriller", "thriller"],
        # ["family", "family"],
        # ["famiglia", "family"],
        # ["azione", "azione"],
        # ["dramma", "dramma"],
        # ["drama", "dramma"],
        # ["western", "western"],
        # ["biografico", "biografico"],
        # ["storia", "biografico"],
        # ["documentario", "biografico"],
        # ["romantico", "romantico"],
        # ["romance", "romantico"],
        # ["horror", "horror"],
        # ["musica", "musical"],
        # ["show", "musical"],
        # ["guerra", "guerra"],
        # ["bambini", "bambini"],
        # ["bianco", "bianconero"],
        # ["tutto", "toto"],
        # ["cartoni", "cartoni"],
        # ["bud", "budterence"],
        # ["documentary", "documentary"],
        # ["crime", "crime"],
        # ["mystery", "mistery"],
        # ["mistero", "mistery"],
        # ["giallo", "mistery"],
        # ["fiction", "fiction"],
        # ["adventure", "mistery"],
        # ["action", "azione"],
        # ["007", "007"],
        # ["sport", "sport"],
        # ["teatr", "teatro"],
        # ["variet", "teatro"],
        # ["giallo", "teatro"],
        # ["extra", "extra"],
        # ["sexy", "fantasy"],
        # ["erotic", "fantasy"],
        # ["animazione", "bambini"],
        # ["search", "search"],

        # ["abruzzo", "regioni/abruzzo"],
        # ["basilicata", "regioni/basilicata"],
        # ["calabria", "regioni/calabria"],
        # ["campania", "regioni/campania"],
        # ["emilia", "regioni/emiliaromagna"],
        # ["friuli", "regioni/friuliveneziagiulia"],
        # ["lazio", "regioni/lazio"],
        # ["liguria", "regioni/liguria"],
        # ["lombardia", "regioni/lombardia"],
        # ["marche", "regioni/marche"],
        # ["molise", "regioni/molise"],
        # ["piemonte", "regioni/piemonte"],
        # ["puglia", "regioni/puglia"],
        # ["sardegna", "regioni/sardegna"],
        # ["sicilia", "regioni/sicilia"],
        # ["toscana", "regioni/toscana"],
        # ["trentino", "regioni/trentino"],
        # ["umbria", "regioni/umbria"],
        # ["veneto", "regioni/veneto"],
        # ["aosta", "regioni/valledaosta"],

        # ["mediaset", "mediaset"],
        # ["nazionali", "nazionali"],
        # ["news", "news"],

        # ["rai", "rai"],
        # ["webcam", "relaxweb"],
        # ["relax", "relaxweb"],
        # ["vecchi", "vecchi"],
        # ["muto", "vecchi"],
        # ["'italiani", "movie"],

        # ["fantascienza", "fantascienza"],
        # ["fantasy", "fantasy"],
        # ["fantasia", "fantasia"],
        # ["film", "movie"],
        # ["samsung", "samsung"],
        # ["plutotv", "plutotv"]
    # ]

    # for png in pngs:
        # piconlocal = 'backg.png'
        # if png[0] in str(name).lower():
            # piconlocal = str(png[1]) + ".png"
            # break

    # if 'prev' in name.lower():
        # piconlocal = prevpng
    # elif 'next' in name.lower():
        # piconlocal = nextpng

    # print('>>>>>>>> ' + str(piccons) + str(piconlocal))
    # path = os.path.join(piccons, piconlocal)
    # return str(path)


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


mdpchoices = [
        ("4097", _("IPTV(4097)")),
        ("1", _("Dvb(1)")),
        ("8193", _("eServiceUri(8193)")),
    ]

if os.path.exists("/usr/bin/gstplayer"):
    mdpchoices.append(("5001", _("Gstreamer(5001)")))

if os.path.exists("/usr/bin/exteplayer3"):
    mdpchoices.append(("5002", _("Exteplayer3(5002)")))

if os.path.exists("/usr/bin/apt-get"):
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
    if os.path.exists("/usr/bin/apt-get"):
        cfg.movie = ConfigDirectory(default='/media/hdd/movie')


global Path_Movies, Path_Cache

Path_Movies = str(cfg.movie.value)
Path_Cache = str(cfg.cachefold.value)
print('Path Movies: ', Path_Movies)
print('Path Cache: ', Path_Cache)


def returnIMDB(text_clear):
    TMDB = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('TMDB'))
    IMDb = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('IMDb'))
    if os.path.exists(TMDB):
        try:
            from Plugins.Extensions.TMBD.plugin import TMBD
            text = html_conv.html_unescape(text_clear)
            _session.open(TMBD.tmdbScreen, text, 0)
        except Exception as e:
            print("[XCF] Tmdb: ", e)
        return True
    elif os.path.exists(IMDb):
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
    print('[tivustream][threadGetPage] url, file, key, args, kwargs', url, "   ", file, "   ", key, "   ", args, "   ", kwargs)
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
        print('[tivustream][threadGetPage] Http error: ', httperror)
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
        ext = str(os.path.splitext(url)[-1])
        picf = os.path.join(picfold, str(name + ext))
        tpicf = os.path.join(tmpfold, str(name + ext))

        if os.path.exists(picf):
            if ('stagione') in str(name.lower()):
                cmd = "rm " + picf
                os.system(cmd)

            cmd = "cp " + picf + " " + tmpfold
            print("In getpics fileExists(picf) cmd =", cmd)
            os.system(cmd)

        # test remove this
        # if os.path.exists(tpicf):
            # cmd = "rm " + tpicf
            # os.system(cmd)

        if not os.path.exists(picf):
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

        if not os.path.exists(tpicf):
            cmd = "cp " + defpic + " " + tpicf
            os.system(cmd)

        if os.path.exists(tpicf):
            try:
                size = [150, 220]
                if screenwidth.width() == 2560:
                    size = [294, 440]
                elif screenwidth.width() == 1920:
                    size = [220, 330]
                else:
                    size = [150, 220]

                file_name, file_extension = os.path.splitext(tpicf)
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


class xxxpluginmain(Screen):
    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self["menu"] = List(self.list)
        self["menu"] = rvList([])
        title = _(name_plug)
        self["title"] = Button(title)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = ActionMap(["MenuActions", "DirectionActions", "ColorActions", "OkCancelActions"], {
            "ok": self.okClicked,
            "cancel": self.close,
            "red": self.close,
            "green": self.okClicked
        }, -1)

        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onLayoutFinish.append(self.startSession)

    def startSession(self):
        self.names = []
        self.urls = []
        self.infos = []
        self.menu = [
            [_("About"), _("Information Us"), ""],
            [_("Config"), _("Setup Plugin"), ""],
            [_("Live TV"), _("Live TV Stream"), "https://tivustream.website/urls/e2live"],
            [_("Film"), _("Film and Movie"), "https://tivustream.website/urls/e2movie"],
            [_("Serie"), _("Series"), "https://tivustream.website/urls/e2series"],
            [_("Search"), _("Search your Movie"), "https://tivustream.website/php_filter/kodi19/kodi19.php?mode=movie&query="],
        ]

        self.session.open(AnimMain, name_plug, "Main", self.menu)

    def okClicked(self):
        pass

    def cancel(self):
        self.session.nav.playService(self.srefInit)
        self.close()


class AnimMain(Screen):
    def __init__(self, session, menuTitle, nextmodule, menu):
        Screen.__init__(self, session)
        self.session = session
        global _session
        _session = session
        skin = os.path.join(skin_path, 'AnimMain.xml')
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.menu = menu
        self.nextmodule = nextmodule
        self.pos = []
        self["title"] = Button(menuTitle)
        self["pointer"] = Pixmap()
        self["info"] = Label()
        self["label1"] = StaticText()
        self["label2"] = StaticText()
        self["label3"] = StaticText()
        self["label4"] = StaticText()
        self["label5"] = StaticText()
        self["actions"] = ActionMap(["MenuActions", "DirectionActions", "ColorActions", "OkCancelActions"], {
            "ok": self.okbuttonClick,
            "cancel": self.cancel,
            "left": self.key_left,
            "right": self.key_right,
            "red": self.cancel,
            "green": self.okbuttonClick,
            "menu": self.closeRecursive,
        }, -1)

        self.nop = len(self.menu)
        self.index = 0
        self.onShown.append(self.openTest)

    def key_menu(self):
        return

    def info(self):
        self.inf = " "
        try:
            self.inf = self.nextlink[1]
        except:
            pass
        if self.inf:
            try:
                self["info"].setText(self.inf)
            except:
                self["info"].setText('')
        print("In AnimMain infos nextlink[1] =", self.inf)

    def cancel(self):
        self.close()

    def openTest(self):
        nextname = islice(cycle(self.menu), self.index, None)
        menu1 = next(nextname)
        menu2 = next(nextname)
        menu3 = next(nextname)
        menu4 = next(nextname)
        menu5 = next(nextname)
        self["label1"].setText(menu1[0])
        self["label2"].setText(menu2[0])
        self["label3"].setText(menu3[0])
        self["label4"].setText(menu4[0])
        self["label5"].setText(menu5[0])

        self.nextlink = menu3
        if screenwidth.width() == 2560:
            dpointer = os.path.join(res_plugin_path, "pics/pointerFHD.png")
            self["pointer"].instance.setPixmapFromFile(dpointer)
        elif screenwidth.width() == 1920:
            dpointer = os.path.join(res_plugin_path, "pics/pointerFHD.png")
            self["pointer"].instance.setPixmapFromFile(dpointer)
        else:
            dpointer = os.path.join(res_plugin_path, "pics/pointerHD.png")
            self["pointer"].instance.setPixmapFromFile(dpointer)
        self.info()

    def key_left(self):
        self.index -= 1
        if self.index < 0:
            self.index = self.nop - 1
        self.openTest()

    def key_right(self):
        self.index += 1
        if self.index > self.nop - 1:
            self.index = 0
        self.openTest()

    def closeRecursive(self):
        self.close(True)

    def okbuttonClick(self):
        name = self.nextlink[0]
        url = self.nextlink[2]
        if self.nextlink[0] == _("About"):
            self.session.open(Abouttvr)

        elif self.nextlink[0] == _("Config"):
            self.session.open(ConfigEx)

        elif self.nextlink[0] == _("Live TV") or self.nextlink[0] == _("Film") or self.nextlink[0] == _("Serie"):
            try:
                vid2 = Main(self.session, name, url)
                vid2.startSession()
            except:
                pass

        elif self.nextlink[0] == _("Search"):
            self.search_text()

    def search_text(self):
        self.namex = self.nextlink[0]
        self.urlx = self.nextlink[2]
        self.session.openWithCallback(self.filterChannels, VirtualKeyBoard, title=_("Filter this category..."), text='')

    def filterChannels(self, result):
        if result:
            name = str(result)
            url = self.urlx + str(result)
            try:
                vid2 = nextVideos4(self.session, name, url)
                vid2.startSession()
            except:
                return
        else:
            self.resetSearch()

    def resetSearch(self):
        global search
        search = False
        return


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
        if os.path.exists('/var/lib/dpkg/status'):
            skin = os.path.join(skin_path, 'ConfigOs.xml')
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = _("SETUP PLUGIN")
        self.onChangedEntry = []
        self.list = []
        ConfigListScreen.__init__(self, self.list, session=self.session, on_change=self.changedEntry)
        self['key_red'] = Label(_('Exit'))
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
    # def __init__(self, session, name, url):
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
        self["actions"] = ActionMap(["WizardActions", "InputActions", "ColorActions", 'ButtonSetupActions', "DirectionActions"], {
            "ok": self.okClicked,
            "back": self.close,
            "red": self.close,
            "green": self.okClicked
        }, -1)
        # self.name = name
        # self.url = url
        self.onLayoutFinish.append(self.startSession)

    def startSession(self):
        self.names = []
        self.urls = []
        self.pics = []
        # self.infos = []
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
                    if file.endswith('.py'):
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
                        # else:
                        # name = file.replace('.py','')
                        name, ext = file.split(".")  # [-1]
                        desc = 'XXX %s' % name
                        url = THISPLUG + "Sites/%s.py" % name
                        pic = os.path.join(piccons, '%s.png' % name)
                        self.names.append(name)
                        self.urls.append(url)
                        self.pics.append(pic)
                        i += 1
                        print(name +'\n'+desc+'\n'+url+'\n'+pic)


        except Exception as e:
            print(e)

        title = name_plug
        # if _("Live") in self.name:
            # nextmodule = "Videos3"
        # elif _("Film") in self.name:
            # nextmodule = "Videos4"
        # elif _("Serie") in self.name:
            # nextmodule = "Videos1"

        if cfg.thumb.value == "True":
            # print("In Main Going in GridMain")
            # menuTitle, nextmodule, names, urls, infos, pics=[]
            self.session.open(GridMain, title, self.names, self.urls, pics=self.pics)
        """
        else:
            self.session.open(AnimMain, title, nextmodule, self.menu)
            """

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
            self.pos.append([180, 80])
            self.pos.append([658, 80])
            self.pos.append([1134, 80])
            self.pos.append([1610, 80])
            self.pos.append([2084, 80])
            self.pos.append([180, 720])
            self.pos.append([658, 720])
            self.pos.append([1134, 720])
            self.pos.append([1610, 720])
            self.pos.append([2084, 720])

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
        self["actions"] = ActionMap(["OkCancelActions", "EPGSelectActions", "MenuActions", "DirectionActions", "NumberActions"], {
            "ok": self.okClicked,
            "epg": self.showIMDB,
            "info": self.showIMDB,
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

    def cancel(self):
        self.close()

    def exit(self):
        self.close()

    def showIMDB(self):
        idx = self.index
        text_clear = self.names[idx]
        if returnIMDB(text_clear):
            print('show imdb/tmdb')

    # def info(self):
        # itype = self.index
        # self.inf = self.infos[itype]
        # # self.inf = ''
        # try:
            # self.inf = self.infos[itype]
        # except:
            # pass
        # if self.inf:
            # try:
                # self["info"].setText(self.inf)
                # # print('infos: ', self.inf)
            # except:
                # self["info"].setText('')
                # # print('except info')
        # print("In GridMain infos =", self.inf)

    def paintFrame(self):
        # print("In paintFrame self.index, self.minentry, self.maxentry =", self.index, self.minentry, self.maxentry)
        # print("In paintFrame self.ipage = ", self.ipage)
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
            '''
            print("i, idx =", i, idx)
            print("self.names[idx] B=", self.names[idx])
            print("idx, self.pics[idx]", idx, self.pics[idx])
            print("pic =", pic)
            '''
            if os.path.exists(pic):
                print("pic path exists")
            else:
                print("pic path not exists")
            picd = defpic
            file_name, file_extension = os.path.splitext(pic)
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
        # print("self.minentry, self.index =", self.minentry, self.index)
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
        # print("keyup self.index, self.minentry = ", self.index, self.minentry)
        self.index = self.index - 5
        # print("keyup self.index, self.minentry 2 = ", self.index, self.minentry)
        # print("keyup self.ipage = ", self.ipage)
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
        # print("keydown self.index, self.maxentry = ", self.index, self.maxentry)
        self.index = self.index + 5
        # print("keydown self.index, self.maxentry 2= ", self.index, self.maxentry)
        # print("keydown self.ipage = ", self.ipage)
        if self.index > (self.maxentry):
            if self.ipage < self.npage:
                self.ipage = self.ipage + 1
                self.openTest()
            elif self.ipage == self.npage:
                self.index = 0
                self.ipage = 1
                self.openTest()
            else:
                # print("keydown self.index, self.maxentry 3= ", self.index, self.maxentry)
                self.index = 0
            self.paintFrame()
        else:
            self.paintFrame()

    def okClicked(self):
        itype = self.index
        name = self.names[itype]
        url = self.urls[itype]
        # inf = self.infos[itype]
        print("In GridMain name =", name)
        print("In GridMain url =", url)
        # print("In GridMain self.nextmodule =", self.nextmodule)
        # if name == _("Config"):
            # self.session.open(ConfigEx)
        # elif name == _("About"):
            # self.session.open(Abouttvr)
        # elif _('Search') in str(name):
            # global search
            # search = True
            # # print('Search go movie: ', search)
            # self.search_text(name, url)
        # try:
            # vid2 = nextVideos1(self.session, name, url)
            # vid2.startSession()

        if PY3:
              modl = name.lower()
              import importlib.util
              spec = importlib.util.spec_from_file_location(modl, url)
              foo = importlib.util.module_from_spec(spec)
              spec.loader.exec_module(foo)
              print("In GridMain Going in PY3")
              # foo.main(self.session)
              self.session.open(foo.main)
        else:
              modl = name.lower()
              import imp
              foo = imp.load_source(modl, url)
              print("In GridMain Going in PY2")
              # foo.main(self.session)
              # foo.main(self.updateMenuList)
              self.session.open(foo.main)
        # except:
            # pass

    # def search_text(self, name, url):
        # self.namex = name
        # self.urlx = url
        # self.session.openWithCallback(self.filterChannels, VirtualKeyBoard, title=_("Filter this category..."), text=name)

    # def filterChannels(self, result):
        # if result:
            # name = str(result)
            # url = self.urlx + str(result)
            # try:
                # vid2 = nextVideos4(self.session, name, url)
                # vid2.startSession()
            # except:
                # return
        # else:
            # self.resetSearch()

    # def resetSearch(self):
        # global search
        # search = False
        # return


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
        global _session
        _session = session
        skin = os.path.join(skin_path, 'Playstream1.xml')
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Select Player Stream')
        self.list = []
        self['list'] = rvList([])
        self['info'] = Label()
        self['info'].setText(name)
        self['key_red'] = Button(_('Exit'))
        self['key_green'] = Button(_('Select'))
        self['progress'] = ProgressBar()
        self['progresstext'] = StaticText()
        self["progress"].hide()
        self.downloading = False
        self['actions'] = ActionMap(['MoviePlayerActions', 'MovieSelectionActions', 'ColorActions', 'DirectionActions', 'ButtonSetupActions', 'OkCancelActions'], {
            'red': self.cancel,
            'green': self.okClicked,
            'back': self.cancel,
            'cancel': self.cancel,
            'leavePlayer': self.cancel,
            'rec': self.runRec,
            'instantRecord': self.runRec,
            'ShortRecord': self.runRec,
            'ok': self.okClicked
        }, -2)

        self.name1 = name
        self.url = url
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onLayoutFinish.append(self.openTest)
        return

    def runRec(self):
        self.namem3u = self.name1
        self.urlm3u = self.url
        if self.downloading is True:
            self.session.open(MessageBox, _('You are already downloading!!!'), MessageBox.TYPE_INFO, timeout=5)
            return
        else:
            if '.mp4' or '.mkv' or '.flv' or '.avi' in self.urlm3u:
                self.session.openWithCallback(self.download_m3u, MessageBox, _("DOWNLOAD VIDEO?\n%s" % self.namem3u), type=MessageBox.TYPE_YESNO, timeout=10, default=False)
            else:
                self.downloading = False
                self.session.open(MessageBox, _('Only VOD Movie allowed or not .ext Filtered!!!'), MessageBox.TYPE_INFO, timeout=5)

    def download_m3u(self, result):
        if result:
            # if 'm3u8' not in self.urlm3u:
            path = urlparse(self.urlm3u).path
            ext = splitext(path)[1]
            if ext != '.mp4' or ext != '.mkv' or ext != '.avi' or ext != '.flv':  # or ext != 'm3u8':
                ext = '.mp4'
            fileTitle = re.sub(r'[\<\>\:\"\/\\\|\?\*\[\]]', '_', self.namem3u)
            fileTitle = re.sub(r' ', '_', fileTitle)
            fileTitle = re.sub(r'_+', '_', fileTitle)
            fileTitle = fileTitle.replace("(", "_").replace(")", "_").replace("#", "").replace("+", "_").replace("\'", "_").replace("'", "_").replace("!", "_").replace("&", "_")
            fileTitle = fileTitle.replace(" ", "_").replace(":", "").replace("[", "").replace("]", "").replace("!", "_").replace("&", "_")
            fileTitle = fileTitle.lower() + ext
            self.in_tmp = os.path.join(Path_Movies, fileTitle)
            self.downloading = True
            self.download = downloadWithProgress(self.urlm3u, self.in_tmp)
            self.download.addProgress(self.downloadProgress)
            self.download.start().addCallback(self.check).addErrback(self.showError)
            # else:
                # self.downloading = False
                # self.session.open(MessageBox, _('Download Failed!!!'), MessageBox.TYPE_INFO, timeout=5)
        else:
            self.downloading = False

    def downloadProgress(self, recvbytes, totalbytes):
        self["progress"].show()
        self['progress'].value = int(100 * recvbytes / float(totalbytes))
        self['progresstext'].text = '%d of %d kBytes (%.2f%%)' % (recvbytes / 1024, totalbytes / 1024, 100 * recvbytes / float(totalbytes))

    def check(self, fplug):
        checkfile = self.in_tmp
        if os.path.exists(checkfile):
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
        self.names.append('Download Now')
        self.urls.append(url)
        self.names.append('Play HLS')
        self.urls.append(url)
        self.names.append('Play TS')
        self.urls.append(url)
        self.names.append('Streamlink')
        self.urls.append(url)
        showlist(self.names, self['list'])

    def okClicked(self):
        idx = self['list'].getSelectionIndex()
        if idx is not None or idx != -1:
            self.name = self.names[idx]
            self.url = self.urls[idx]
            if "youtube" in str(self.url):
                desc = self.name
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
                self.session.open(Playstream2, self.name, self.url, desc)

            if idx == 0:
                print('In playVideo url D=', self.url)
                self.play()

            elif idx == 1:
                print('In playVideo url D=', self.url)
                self.runRec()

            elif idx == 2:
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
                self.play()
            else:
                if idx == 4:
                    print('In playVideo url D=', self.url)
                    self.play2()
            return

    def playfile(self, serverint):
        self.serverList[serverint].play(self.session, self.url, self.name)

    def play(self):
        desc = self.name
        url = self.url
        name = self.name1
        self.session.open(Playstream2, name, url, desc)
        self.close()

    def play2(self):
        if Utils.isStreamlinkAvailable():
            desc = self.name
            name = self.name1
            url = self.url
            url = url.replace(':', '%3a')
            ref = '5002:0:1:0:0:0:0:0:0:0:' + 'http%3a//127.0.0.1%3a8088/' + str(url)
            sref = eServiceReference(ref)
            print('SREF: ', sref)
            sref.setName(self.name1)
            self.session.open(Playstream2, name, sref, desc)
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


class Playstream2(Screen, InfoBarMenu, InfoBarBase, InfoBarSeek, InfoBarNotifications, InfoBarAudioSelection, TvInfoBarShowHide, InfoBarSubtitleSupport):
    STATE_IDLE = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    ENABLE_RESUME_SUPPORT = True
    ALLOW_SUSPEND = True
    screen_timeout = 4000

    def __init__(self, session, name, url, desc):
        global streaml, _session
        _session = session
        streaml = False
        Screen.__init__(self, session)
        self.session = session
        self.skinName = 'MoviePlayer'
        InfoBarMenu.__init__(self)
        InfoBarNotifications.__init__(self)
        InfoBarBase.__init__(self, steal_current_service=True)
        TvInfoBarShowHide.__init__(self)
        InfoBarSubtitleSupport.__init__(self)
        InfoBarAudioSelection.__init__(self)
        try:
            self.init_aspect = int(self.getAspect())
        except:
            self.init_aspect = 0
        self.new_aspect = self.init_aspect
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
        self.service = None
        self.allowPiP = False
        self.desc = desc
        self.url = url
        self.name = name
        self.state = self.STATE_PLAYING
        self['actions'] = ActionMap(['WizardActions', 'MoviePlayerActions', 'MovieSelectionActions', 'MediaPlayerActions', 'EPGSelectActions', 'MediaPlayerSeekActions', 'ColorActions',
                                     'ButtonSetupActions', 'InfobarShowHideActions', 'InfobarActions', 'InfobarSeekActions'], {
            'leavePlayer': self.cancel,
            'epg': self.showIMDB,
            'info': self.showIMDB,
            # 'info': self.cicleStreamType,
            'tv': self.cicleStreamType,
            'stop': self.leavePlayer,
            'cancel': self.cancel,
            'back': self.cancel
        }, -1)
        InfoBarSeek.__init__(self, actionmap='InfobarSeekActions')
        # self.onLayoutFinish.append(self.cicleStreamType)
        # self.onClose.append(self.cancel)
        # self.onClose.append(self.__onClose)
        if '8088' in str(self.url):
            self.onFirstExecBegin.append(self.slinkPlay)
        else:
            self.onFirstExecBegin.append(self.cicleStreamType)
        return

    def getAspect(self):
        return AVSwitch().getAspectRatioSetting()

    def getAspectString(self, aspectnum):
        return {
            0: '4:3 Letterbox',
            1: '4:3 PanScan',
            2: '16:9',
            3: '16:9 always',
            4: '16:10 Letterbox',
            5: '16:10 PanScan',
            6: '16:9 Letterbox'
        }[aspectnum]

    def setAspect(self, aspect):
        map = {
            0: '4_3_letterbox',
            1: '4_3_panscan',
            2: '16_9',
            3: '16_9_always',
            4: '16_10_letterbox',
            5: '16_10_panscan',
            6: '16_9_letterbox'
        }
        config.av.aspectratio.setValue(map[aspect])
        try:
            AVSwitch().setAspectRatio(aspect)
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
        text_clear = self.name
        if returnIMDB(text_clear):
            print('show imdb/tmdb')

    def slinkPlay(self):
        ref = str(self.url)
        ref = ref.replace(':', '%3a').replace(' ', '%20')
        print('final reference 1:   ', ref)
        ref = "{0}:{1}".format(ref, self.name)
        sref = eServiceReference(ref)
        sref.setName(self.name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def openPlay(self, servicetype, url):
        url = url.replace(':', '%3a').replace(' ', '%20')
        ref = str(servicetype) + ':0:1:0:0:0:0:0:0:0:' + str(url)  # + ':' + self.name
        if streaml is True:
            ref = str(servicetype) + ':0:1:0:0:0:0:0:0:0:http%3a//127.0.0.1%3a8088/' + str(url) + ':' + self.name
        print('final reference 2:   ', ref)
        sref = eServiceReference(ref)
        sref.setName(self.name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def cicleStreamType(self):
        global streaml
        # streaml = False
        from itertools import cycle, islice
        self.servicetype = str(cfg.services.value)
        print('servicetype1: ', self.servicetype)
        url = str(self.url)
        if str(splitext(url)[-1]) == ".m3u8":
            if self.servicetype == "1":
                self.servicetype = "4097"
        currentindex = 0
        streamtypelist = ["4097"]
        """
        # if "youtube" in str(self.url):
            # self.mbox = self.session.open(MessageBox, _('For Stream Youtube coming soon!'), MessageBox.TYPE_INFO, timeout=5)
            # return
        # if Utils.isStreamlinkAvailable():
            # streamtypelist.append("5002")  # ref = '5002:0:1:0:0:0:0:0:0:0:http%3a//127.0.0.1%3a8088/' + url
            # streaml = True
        # elif os.path.exists("/usr/bin/gstplayer"):
            # streamtypelist.append("5001")
        # if os.path.exists("/usr/bin/exteplayer3"):
            # streamtypelist.append("5002")
            """
        if os.path.exists("/usr/bin/apt-get"):
            streamtypelist.append("8193")
        for index, item in enumerate(streamtypelist, start=0):
            if str(item) == str(self.servicetype):
                currentindex = index
                break
        nextStreamType = islice(cycle(streamtypelist), currentindex + 1, None)
        self.servicetype = str(next(nextStreamType))
        print('servicetype2: ', self.servicetype)
        self.openPlay(self.servicetype, url)

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
        if os.path.exists('/tmp/hls.avi'):
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


# class AutoStartTimerxxxplugin:

    # def __init__(self, session):
        # self.session = session
        # global _firstStartxxxplugin
        # if _firstStartxxxplugin:
            # self.runUpdate()

    # def runUpdate(self):
        # print("*** running update ***")
        # try:
            # from . import Update
            # Update.upd_done()
            # _firstStartxxxplugin = False
        # except Exception as e:
            # print('error _firstStartxxxplugin', e)


# def autostart(reason, session=None, **kwargs):
    # global autoStartTimerxxxplugin
    # global _firstStartxxxplugin
    # if reason == 0:
        # if session is not None:
            # _firstStartxxxplugin = True
            # autoStartTimerxxxplugin = AutoStartTimerxxxplugin(session)
    # return


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
    result = [PluginDescriptor(name=name_plug, description=title_plug, where=PluginDescriptor.WHERE_PLUGINMENU, icon=icona, fnc=main)]
    result.append(extDescriptor)
    return result
