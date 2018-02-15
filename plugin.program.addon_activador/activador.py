#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmc, xbmcgui, os
from sqlite3 import dbapi2 as db_lib

conn =db_lib.connect(os.path.join(xbmc.translatePath('special://profile/Database'),'Addons27.db'))
conn.text_factory = str

def get_kodi_version():
    try:
	    return float(xbmc.getInfoLabel('System.BuildVersion').split('-')[0])
    except:
	    return float(xbmc.getInfoLabel('System.BuildVersion').split('.')[0])

def check_updates():
    xbmc.executebuiltin('XBMC.UpdateLocalAddons()')
    xbmc.executebuiltin('XBMC.UpdateAddonRepos()')

def set_all_enable():
    conn.executemany('update installed set enabled=1 WHERE addonID = (?)',((val,) for val in os.listdir(xbmc.translatePath(os.path.join('special://home','addons')))))
    conn.commit()
		
if get_kodi_version() > 16.9 :

    dp = xbmcgui.DialogProgress()
    dp.create('Activar os add-ons!','Por favor aguarde ...','')
    dp.update(0)

    check_updates()
    xbmc.sleep(2000)
    dp.update(30)

    set_all_enable()
    xbmc.sleep(2000)
    dp.update(60)

    check_updates()
    xbmc.sleep(2000)
    dp.update(100)

    xbmc.sleep(2000)
    dp.close()
	
    xbmcgui.Dialog().ok('FEITO!', 'Todos os addons encontrados foram ativados!' )
else:
    xbmcgui.Dialog().ok('AVISO!', 'Apenas para uso com as versões Kodi 17.0 +!' )