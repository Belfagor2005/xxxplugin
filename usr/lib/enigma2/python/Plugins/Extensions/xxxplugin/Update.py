#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
PY3 = sys.version_info.major >= 3
print("Update.py")


def upd_done():
    from os import popen, system
    system('rm -rf /tmp/xxxplugin.tar')
    cmd01 = "wget http://patbuweb.com/adultlive/xxxplugin.tar -O /tmp/xxxplugin.tar ; tar -xvf /tmp/xxxplugin.tar -C /"
    cmd02 = "wget --no-check-certificate -U 'Enigma2 - xxxplugin Plugin' -c 'http://patbuweb.com/adultlive/xxxplugin.tar' -O '/tmp/xxxplugin.tar'; tar -xvf /tmp/xxxplugin.tar -C /"
    cmd22 = 'find /usr/bin -name "wget"'
    res = popen(cmd22).read()
    if 'wget' not in res.lower():
        if os.path.exists('/etc/opkg'):
            cmd23 = 'opkg update && opkg install wget'
        else:
            cmd23 = 'apt-get update && apt-get install wget'
        popen(cmd23)
    try:
        popen(cmd02)
    except:
        popen(cmd01)
    system('rm -rf /tmp/xxxplugin.tar')
    return
