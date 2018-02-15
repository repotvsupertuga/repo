# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PT DocS HD
#------------------------------------------------------------
# Licença: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Baseado no código do addon youtube
#-----------------------------------------------------------

import xbmc, xbmcaddon, xbmcplugin, os, sys, plugintools
from addon.common.addon import Addon

addonID = 'plugin.video.pt.docs.hd'
addon   = Addon(addonID, sys.argv)
local   = xbmcaddon.Addon(id=addonID)
icon    = local.getAddonInfo('icon')
base    = 'plugin://plugin.video.youtube/'

fan01 = 'special://home/addons/plugin.video.pt.docs.hd/resources/fan01.jpg'
iconAA = 'special://home/addons/plugin.video.pt.docs.hd/resources/iconAA.png'
icon01 = 'special://home/addons/plugin.video.pt.docs.hd/resources/icon01.png'
icon02 = 'special://home/addons/plugin.video.pt.docs.hd/resources/icon02.png'
icon03 = 'special://home/addons/plugin.video.pt.docs.hd/resources/icon03.png'
icon04 = 'special://home/addons/plugin.video.pt.docs.hd/resources/icon04.png'
icon05 = 'special://home/addons/plugin.video.pt.docs.hd/resources/icon05.png'
icon06 = 'special://home/addons/plugin.video.pt.docs.hd/resources/icon06.png'
icon07 = 'special://home/addons/plugin.video.pt.docs.hd/resources/icon07.png'
icon08 = 'special://home/addons/plugin.video.pt.docs.hd/resources/icon08.png'
icon09 = 'special://home/addons/plugin.video.pt.docs.hd/resources/icon09.png'
icon10 = 'special://home/addons/plugin.video.pt.docs.hd/resources/icon10.png'
icon11 = 'special://home/addons/plugin.video.pt.docs.hd/resources/icon11.png'
icon12 = 'special://home/addons/plugin.video.pt.docs.hd/resources/icon12.png'
iconAB = 'special://home/addons/plugin.video.pt.docs.hd/resources/iconAB.png'
iconAC = 'special://home/addons/plugin.video.pt.docs.hd/resources/iconAC.png'
iconAD = 'special://home/addons/plugin.video.pt.docs.hd/resources/iconAD.png'
iconAE = 'special://home/addons/plugin.video.pt.docs.hd/resources/iconAE.png'








def run():
    plugintools.log("pt.docs.hd.run")
    params = plugintools.get_params()
    if params.get("action") is None: main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    plugintools.close_item_list()

def main_list(params):
	plugintools.log("pt.docs.hd ===> " + repr(params))
	plugintools.add_item(title = "[ KODI Video Tutoriais ]", url = base + "channel/UCb6fo8oH9phPpNjzNjc8MOg/", thumbnail = iconAA, fanart = fan01, folder = True)
	plugintools.add_item(title = "[ O Povo - A Terra ]", url = base + "playlist/PLAg4T2da6qWzR4wzIK8r9H8S_kR1PIvDX/", thumbnail = icon01, fanart = fan01, folder = True)
	plugintools.add_item(title = "[ Pré-História - Origens ]", url = base + "playlist/PLAg4T2da6qWyDld8XLVstbH4ATeId6d6E/", thumbnail = icon02, fanart = fan01, folder = True)
	plugintools.add_item(title = "[ Civilizações - Impérios ]", url = base + "playlist/PLAg4T2da6qWx4B6j1zPpgbyI-ROEzVeDZ/", thumbnail = icon03, fanart = fan01, folder = True)
	plugintools.add_item(title = "[ Cultos - Seitas ]", url = base + "playlist/PLAg4T2da6qWxPpEjq9KWuGe6vF-DWbAiE/", thumbnail = icon04, fanart = fan01, folder = True)
	plugintools.add_item(title = "[ Atletas - Hooligans ]", url = base + "playlist/PLAg4T2da6qWxlyw4HD5t6bOt9n03nIHGa/", thumbnail = icon05, fanart = fan01, folder = True)
	plugintools.add_item(title = "[ Biografias - Bandas ]", url = base + "playlist/PLAg4T2da6qWzUkstE50-E3rRnLCW9nX2Q/", thumbnail = icon06, fanart = fan01, folder = True)
	plugintools.add_item(title = "[ Informática - Jogos ]", url = base + "playlist/PLAg4T2da6qWxPRExPKACw5RP3GWWYIkDJ/", thumbnail = icon07, fanart = fan01, folder = True)
	plugintools.add_item(title = "[ Tendências - Paranóias ]", url = base + "playlist/PLAg4T2da6qWxSswYqS6gi4XYZ3qlz5Azo/", thumbnail = icon08, fanart = fan01, folder = True)
	plugintools.add_item(title = "[ Gangues - Prisões ]", url = base + "playlist/PLAg4T2da6qWxPpEjq9KWuGe6vF-DWbAiE/", thumbnail = icon09, fanart = fan01, folder = True)
	plugintools.add_item(title = "[ Eventos - Predadores ]", url = base + "playlist/PLAg4T2da6qWz9L4bxdK0jg4d01r50eM6P/", thumbnail = icon10, fanart = fan01, folder = True)
	plugintools.add_item(title = "[ Cosmos - Planetas ]", url = base + "playlist/PLAg4T2da6qWzckdBwDHweyF6hqds1NtAL/" , thumbnail = icon11, fanart = fan01, folder = True)	
	plugintools.add_item(title = "[ Vários ]", url = base + "playlist/PLAg4T2da6qWyEKYtDwim653ZYa7PYueK9/", thumbnail = icon12, fanart = fan01, folder = True)
	plugintools.add_item(title = "[ Toda a Verdade 480p ]", url = base + "playlist/PLAg4T2da6qWyXpuxGw_pmo43zAm-jRImD/", thumbnail = iconAB, fanart = fan01, folder = True)
	plugintools.add_item(title = "[ Acredite ou não ]", url = base + "channel/UCunqx90PNIv30uOgn0m4CTg/", thumbnail = iconAC, fanart = fan01, folder = True)
	plugintools.add_item(title = "[ Revolução Ciêntifica ]", url = base + "channel/UCPLBXvobTRvDjPy41y9hG8g/", thumbnail = iconAD, fanart = fan01, folder = True)
	plugintools.add_item(title = "[ Sem Legendas ]", url = base + "channel/UCn8zNIfYAQNdrFRrr8oibKw/", thumbnail = iconAE, fanart = fan01, folder = True)
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin('Container.SetViewMode(500)')
	
run()
