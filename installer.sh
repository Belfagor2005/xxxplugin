#!/bin/bash

##setup command=wget -q --no-check-certificate https://raw.githubusercontent.com/Belfagor2005/xxxplugin/main/installer.sh -O - | /bin/sh

######### Only This 2 lines to edit with new version ######
version='1.4'
changelog='\nRecode all file and sites'
##############################################################

TMPPATH=/tmp/xxxplugin-main
FILEPATH=/tmp/main.tar.gz

if [ ! -d /usr/lib64 ]; then
    PLUGINPATH=/usr/lib/enigma2/python/Plugins/Extensions/xxxplugin
else
    PLUGINPATH=/usr/lib64/enigma2/python/Plugins/Extensions/xxxplugin
fi

## check depends packges
if [ -f /var/lib/dpkg/status ]; then
    STATUS=/var/lib/dpkg/status
    OSTYPE=DreamOs
else
    STATUS=/var/lib/opkg/status
    OSTYPE=Dream
fi

echo ""
echo "Checking dependencies..."

## Check and install wget if needed
if [ ! -f /usr/bin/wget ]; then
    echo "Installing wget..."
    if [ $OSTYPE = "DreamOs" ]; then
        apt-get update && apt-get install wget -y
    else
        opkg update && opkg install wget
    fi
fi

## Check Python version
if python --version 2>&1 | grep -q '^Python 3\.'; then
    echo "Python3 detected"
    PYTHON=PY3
    Packagesix=python3-six
    Packagerequests=python3-requests
else
    echo "Python2 detected"
    PYTHON=PY2
    Packagerequests=python-requests
fi

## Check and install required packages
if [ $PYTHON = "PY3" ] && ! grep -qs "Package: $Packagesix" $STATUS; then
    echo "Installing $Packagesix..."
    if [ $OSTYPE = "DreamOs" ]; then
        apt-get install python3-six -y
    else
        opkg install python3-six
    fi
fi

if ! grep -qs "Package: $Packagerequests" $STATUS; then
    echo "Installing $Packagerequests..."
    if [ $OSTYPE = "DreamOs" ]; then
        apt-get install $Packagerequests -y
    else
        opkg install $Packagerequests
    fi
fi

## Cleanup previous installations
[ -r $TMPPATH ] && rm -rf $TMPPATH > /dev/null 2>&1
[ -r $FILEPATH ] && rm -f $FILEPATH > /dev/null 2>&1
[ -r $PLUGINPATH ] && rm -rf $PLUGINPATH > /dev/null 2>&1

## Download and install plugin
mkdir -p $TMPPATH
cd $TMPPATH
set -e

echo ""
if [ $OSTYPE = "DreamOs" ]; then
    echo "OE2.5/2.6 image detected"
else
    echo "OE2.0 image detected"
    echo "Installing additional dependencies..."
    opkg update && opkg install ffmpeg gstplayer exteplayer3 enigma2-plugin-systemplugins-serviceapp
fi

echo "Downloading plugin..."
wget --no-check-certificate -O $FILEPATH 'https://github.com/Belfagor2005/xxxplugin/archive/refs/heads/main.tar.gz'
tar -xzf $FILEPATH -C $TMPPATH
cp -r $TMPPATH/xxxplugin-main/usr /
set +e

## Verify installation
if [ ! -d $PLUGINPATH ]; then
    echo "ERROR: Plugin installation failed!"
    rm -rf $TMPPATH > /dev/null 2>&1
    rm -f $FILEPATH > /dev/null 2>&1
    exit 1
fi

## Cleanup
rm -rf $TMPPATH > /dev/null 2>&1
rm -f $FILEPATH > /dev/null 2>&1
sync

## Show installation info
FILE="/etc/image-version"
box_type=$(head -n 1 /etc/hostname 2>/dev/null || echo "Unknown")
distro_value=$(grep '^distro=' "$FILE" 2>/dev/null | awk -F '=' '{print $2}' || echo "Unknown")
distro_version=$(grep '^version=' "$FILE" 2>/dev/null | awk -F '=' '{print $2}' || echo "Unknown")
python_vers=$(python --version 2>&1 || echo "Python not found")

echo "#########################################################
#               INSTALLED SUCCESSFULLY                  #
#                developed by LULULLA                   #
#               https://corvoboys.org                   #
#########################################################
#           your Device will RESTART Now                #
#########################################################
^^^^^^^^^^Debug information:
BOX MODEL: $box_type
OO SYSTEM: $OSTYPE
PYTHON: $python_vers
IMAGE NAME: $distro_value
IMAGE VERSION: $distro_version"

sleep 5
killall -9 enigma2
exit 0