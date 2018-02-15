# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Seal Music Live Acts
#------------------------------------------------------------
# Licença: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Baseado no código do addon youtube
#------------------------------------------------------------

import xbmc, xbmcaddon, xbmcplugin, os, sys, plugintools
from addon.common.addon import Addon

addonID = 'plugin.video.sealmusic'
addon   = Addon(addonID, sys.argv)
local   = xbmcaddon.Addon(id=addonID)
icon    = local.getAddonInfo('icon')
base    = 'plugin://plugin.video.youtube/'

fan01 = 'special://home/addons/plugin.video.sealmusic/resources/fan01.png'
icon = 'special://home/addons/plugin.video.sealmusic/resources/icon.png'
icon00 = 'special://home/addons/plugin.video.sealmusic/resources/icon00.png'
icon01 = 'special://home/addons/plugin.video.sealmusic/resources/icon01.png'
icon02 = 'special://home/addons/plugin.video.sealmusic/resources/icon02.png'
icon03 = 'special://home/addons/plugin.video.sealmusic/resources/icon03.png'
icon04 = 'special://home/addons/plugin.video.sealmusic/resources/icon04.png'
icon05 = 'special://home/addons/plugin.video.sealmusic/resources/icon05.png'
icon06 = 'special://home/addons/plugin.video.sealmusic/resources/icon06.png'
icon07 = 'special://home/addons/plugin.video.sealmusic/resources/icon07.png'
icon08 = 'special://home/addons/plugin.video.sealmusic/resources/icon08.png'
icon09 = 'special://home/addons/plugin.video.sealmusic/resources/icon09.png'



def run():
    plugintools.log("jami.run")
    params = plugintools.get_params()
    if params.get("action") is None: main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    plugintools.close_item_list()

def main_list(params):
	plugintools.log("jami ===> " + repr(params))
	
	plugintools.add_item(title = "NATIONAL LIVE ACTS", url =  base + "playlist/PLvD9-mRSTbHZghAOFEnjHMhOF3Sum33vt/", thumbnail = icon01, fanart = fan01, folder = True)
	plugintools.add_item(title = "INTERNATIONAL LIVE ACTS", url = base + "playlist/PLvD9-mRSTbHY05jsahTVIWbewcvXysUmy/", thumbnail = icon02, fanart = fan01, folder = True)
	plugintools.add_item(title = "DANCE MUSIC LIVE ACTS", url = base + "playlist/PLvD9-mRSTbHadR5sKn9ijYiJOyiRIE9y5/", thumbnail = icon03, fanart = fan01, folder = True)
	plugintools.add_item(title = "ACOUSTIC LIVE ACTS", url = base + "playlist/PLvD9-mRSTbHYlCpk-rkTqhfZqz8UNY8sR/", thumbnail = icon04, fanart = fan01, folder = True)
	plugintools.add_item(title = "BRASIL LIVE ACTS", url = base + "playlist/PLvD9-mRSTbHb8wCpD29YIyIyKtFgmkY-x/", thumbnail = icon05, fanart = fan01, folder = True)
	plugintools.add_item(title = "ACUSTICOS AO VIVO", url = base + "playlist/PLvD9-mRSTbHaa2VlyR_t5gIGaOBIBOZ6O/", thumbnail = icon06, fanart = fan01, folder = True)	
	plugintools.add_item(title = "", url = base + "", thumbnail = icon07, fanart = fan01, folder = False)
	plugintools.add_item(title = "", url = base + "", thumbnail = icon08, fanart = fan01, folder = False)
	plugintools.add_item(title = "", url = base + "", thumbnail = icon09, fanart = fan01, folder = False)

	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin('Container.SetViewMode(500)')
	
run()
