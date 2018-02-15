# -*- coding: utf-8 -*-
#------------------------------------------------------------
# mntek
#------------------------------------------------------------
# Licença: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Baseado no código do addon youtube
#------------------------------------------------------------

import xbmc, xbmcaddon, xbmcplugin, os, sys, plugintools

from addon.common.addon import Addon

addonID = 'plugin.video.mntek'
addon   = Addon(addonID, sys.argv)
local   = xbmcaddon.Addon(id=addonID)
icon    = local.getAddonInfo('icon')
base    = 'plugin://plugin.video.youtube/'

icon01 = 'http://i.cubeupload.com/9pZDdZ.png'
icon02 = 'http://i.cubeupload.com/jkHnxD.png'
icon03 = 'http://i.cubeupload.com/inJpUo.png'
icon04 = 'http://i.cubeupload.com/7cW2sR.png'
def run():
    plugintools.log("mntek.run")
    
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

def main_list(params):
		plugintools.log("mntek ===> " + repr(params))

		plugintools.add_item(title = "Dicas para Kodi"                       , url = base + "playlist/PLbcICQBwGu7W8UAB3AdAA4wevk--oPO6U/"                   , thumbnail = icon01, folder = True)
		plugintools.add_item(title = "Dicas para Android"               , url = base + "playlist/PLbcICQBwGu7XhEyAsVG7PgttoAJRXFrWh/", thumbnail = icon02, folder = True)
		plugintools.add_item(title = "Dicas para Windows"                     , url = base + "playlist/PLbcICQBwGu7U7uI1UxIWpoAvWFLI7nPYj/", thumbnail = icon03, folder = True)
		plugintools.add_item(title = "Unboxings/Reviews"                     , url = base + "playlist/PLbcICQBwGu7VzQSwt0rRrm8nrzdOylDhg/", thumbnail = icon04, folder = True)
		
		
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		xbmc.executebuiltin('Container.SetViewMode()')
		
run()
