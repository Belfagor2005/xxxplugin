#!/usr/bin/python
# -*- coding: utf-8 -*-

from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
import gettext
import os
from enigma import getDesktop
global skin_path

PluginLanguageDomain = 'xxxplugin'
PluginLanguagePath = 'Extensions/xxxplugin/locale'
THISPLUG = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/".format('xxxplugin'))
skin_path = THISPLUG + '/res/skins/hd/'
screenwidth = getDesktop(0).size()
isDreamOS = False


if os.path.exists("/var/lib/dpkg/status"):
    isDreamOS = True
if screenwidth.width() == 2560:
    skin_path = THISPLUG + 'res/skins/uhd/'
elif screenwidth.width() == 1920:
    skin_path = THISPLUG + 'res/skins/fhd/'
else:
    skin_path = THISPLUG + 'res/skins/hd/'


def localeInit():
    if isDreamOS:  # check if opendreambox image
        lang = language.getLanguage()[:2]  # getLanguage returns e.g. "fi_FI" for "language_country"
        os.environ["LANGUAGE"] = lang  # Enigma doesn't set this (or LC_ALL, LC_MESSAGES, LANG). gettext needs it!
    gettext.bindtextdomain(PluginLanguageDomain, resolveFilename(SCOPE_PLUGINS, PluginLanguagePath))


if isDreamOS:  # check if DreamOS image
    _ = lambda txt: gettext.dgettext(PluginLanguageDomain, txt) if txt else ""
else:
    def _(txt):
        if gettext.dgettext(PluginLanguageDomain, txt):
            return gettext.dgettext(PluginLanguageDomain, txt)
        else:
            print(("[%s] fallback to default translation for %s" % (PluginLanguageDomain, txt)))
            return gettext.gettext(txt)
localeInit()
language.addCallback(localeInit)

