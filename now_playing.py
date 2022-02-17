#!/usr/bin/env python
# title             : now_playing.py
# description       : Now Playing is an OBS script that will update a Text Source
#                   : with the current song that Media Player are playing. Only for MAC OS
# author            : Yanxin1
# date              : 2022 01 13
# version           : 0.1
# usage             : python now_playing.py
# dependencies      : - Python 3.6 (https://www.python.org/)
#                   : - biplist
# notes             : Follow this step for this script to work:
#                   : Python:
#                   :   1. Install python (v3.6 and 64 bits, this is important)
#                   :   2. Install biplist (use pip)
#                   : OBS:
#                   :   1. Create a GDI+ Text Source with the name of your choice
#                   :   2. Go to Tools › Scripts
#                   :   3. Click the "+" button and add this script
#                   :   5. Set the same source name as the one you just created
#                   :   6. Check "Enable"
#                   :   7. Click the "Python Settings" rab
#                   :   8. Select your python install path
#                   :
# python_version    : 3.6+
# ==============================================================================

import obspython as obs
import os, time, datetime, codecs, json
from biplist import *

class plistManager(object):
    """docstring for ClassName"""
    # def __init__(self, arg):
    # super(ClassName, self).__init__()
    # self.arg = arg

    # plist 路径
    def filePaht(self):
        # 获取系统桌面路径
        # 系统路径
        osPath = os.path.expanduser('~')
        # 网易云路径
        subPath = "Library/Containers/com.netease.163music/Data/Documents/storage/file_storage/webdata/file"
        pathstr = os.path.join(osPath,subPath)
        return  pathstr
    # plist 名字
    def plistName(self):
        checkfile ='history'
        return  checkfile

    # 切换目录  目录
    def changePath(self,pathstr):
        os.chdir(pathstr)
        ls = os.getcwd()
        # print ("当前目录是 : ", pathstr)
        return

    # 读取plist
    def readPlistFromName(self,name):
        try:
            plist = readPlist(name)

            return  plist
            pass
        except Exception as e:
            raise e
            return

working = True
enabled = True
check_frequency = 3000
display_text = '♫ %artist - %title '
debug_mode = False

source_name = ''
plm = plistManager()
plm.changePath(plm.filePaht())

def script_defaults(settings):
    global debug_mode
    if debug_mode: print("Calling defaults")

    global enabled
    global source_name
    global display_text
    global check_frequency

    obs.obs_data_set_default_bool(settings, "enabled", enabled)
    obs.obs_data_set_default_int(settings, "check_frequency", check_frequency)
    obs.obs_data_set_default_string(settings, "display_text", display_text)
    obs.obs_data_set_default_string(settings, "source_name", source_name)

def script_description():
    global debug_mode
    if debug_mode: print("Calling description")

    return "<b>Music Now Playing</b>" + \
        "<hr>" + \
        "Display current song as a text on your screen." + \
        "<br/>" + \
        "Available placeholders: " + \
        "<br/>" + \
        "<code>♫ %artist</code>, <code>%title</code>" + \
        "<hr>"

def script_load(settings):
    global debug_mode
    if debug_mode: print("[CS] Loaded script.")

def script_properties():
    global debug_mode
    if debug_mode: print("[CS] Loaded properties.")

    props = obs.obs_properties_create()
    obs.obs_properties_add_bool(props, "enabled", "Enabled")
    obs.obs_properties_add_bool(props, "debug_mode", "Debug Mode")
    obs.obs_properties_add_int(props, "check_frequency", "Check frequency", 150, 100000, 100 )
    obs.obs_properties_add_text(props, "display_text", "Display text", obs.OBS_TEXT_DEFAULT )
    obs.obs_properties_add_text(props, "source_name", "Text source", obs.OBS_TEXT_DEFAULT )
    return props

def script_save(settings):
    global debug_mode
    if debug_mode: print("[CS] Saved properties.")

    script_update(settings)

def script_unload():
    global debug_mode
    if debug_mode: print("[CS] Unloaded script.")

    obs.timer_remove(get_song_info)

def script_update(settings):
    global debug_mode
    if debug_mode: print("[CS] Updated properties.")

    global enabled
    global display_text
    global check_frequency
    global source_name

    if obs.obs_data_get_bool(settings, "enabled") is True:
        if (not enabled):
            if debug_mode: print("[CS] Enabled song timer.")

        enabled = True
        if debug_mode: print("[CS] timer add.")
        obs.timer_add(get_song_info, check_frequency)
    else:
        if (enabled):
            if debug_mode: print("[CS] Disabled song timer.")

        enabled = False
        if debug_mode: print("[CS] timer remove.")
        obs.timer_remove(get_song_info)

    debug_mode = obs.obs_data_get_bool(settings, "debug_mode")
    display_text = obs.obs_data_get_string(settings, "display_text")
    source_name = obs.obs_data_get_string(settings, "source_name")
    check_frequency = obs.obs_data_get_int(settings, "check_frequency")

def update_song(artist = "", song = ""):
    global debug_mode
    global display_text
    global source_name

    now_playing = ""
    if(artist != "" or song != ""):
        now_playing = display_text.replace('%artist', artist).replace('%title', song)

    settings = obs.obs_data_create()
    obs.obs_data_set_string(settings, "text", now_playing)
    source = obs.obs_get_source_by_name(source_name)
    obs.obs_source_update(source, settings)
    obs.obs_data_release(settings)
    obs.obs_source_release(source)
    if debug_mode: print("[CS] Now Playing : " + artist + " / " + song)

def get_song_info():
    global debug_mode
    global plm

    plist = plm.readPlistFromName(plm.plistName())
    playing = json.loads(plist['$objects'][1])[0]['track']
    artists = []
    for artist in playing['artists']:
        artists.append(artist['name'])
    try:
        update_song(' / '.join(artists), playing['name'])
    except:
        update_song()


