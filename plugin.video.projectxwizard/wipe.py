import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import re
import time
import common as Common
import shutil

thumbnailPath = xbmc.translatePath('special://userdata/Thumbnails');
cachePath = os.path.join(xbmc.translatePath('special://home'), 'cache')
tempPath = xbmc.translatePath('special://temp')
addonPath = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.projectxwizard')
mediaPath = os.path.join(addonPath, 'resources/art')
databasePath = xbmc.translatePath('special://userdata/Database')
AddonData = xbmc.translatePath('special://userdata/addon_data')
addon_id = 'plugin.video.projectxwizard'
ADDON = xbmcaddon.Addon(id=addon_id)
AddonID='plugin.video.projectxwizard'
AddonTitle="[COLOR ghostwhite]Project X[/COLOR] [COLOR lightsteelblue]Wizard[/COLOR]"
MaintTitle="[COLOR ghostwhite]Project X[/COLOR] [COLOR lightsteelblue]Wizard[/COLOR]"
dialog       =  xbmcgui.Dialog()
HOME         =  xbmc.translatePath('special://home/')
dp           =  xbmcgui.DialogProgress()
U = ADDON.getSetting('User')
USB          =  xbmc.translatePath(os.path.join(HOME,'backupdir'))
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
ART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
VERSION = "1.19"
DBPATH = xbmc.translatePath('special://userdata/Database')
TNPATH = xbmc.translatePath('special://userdata/Thumbnails');
PATH = "Project X Wizard"            
BASEURL = "http://www/projectxwizard.com"
H = 'http://'
skin         =  xbmc.getSkinDir()
EXCLUDES     = ['Database','cache','temp','backupdir','plugin.video.projectxwizard','repository.tdbegley.official',"kodi.log","kodi.log.old","spmc.log","spmc.log.old"]

ARTPATH      =  '' + os.sep
UPDATEPATH     =  xbmc.translatePath(os.path.join('special://home/addons',''))
UPDATEADPATH	=  xbmc.translatePath(os.path.join('special://home/userdata/addon_data',''))
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
MEDIA        =  xbmc.translatePath(os.path.join('special://home/media',''))
AUTOEXEC     =  xbmc.translatePath(os.path.join(USERDATA,'autoexec.py'))
AUTOEXECBAK  =  xbmc.translatePath(os.path.join(USERDATA,'autoexec_bak.py'))
ADDON_DATA   =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
PLAYLISTS    =  xbmc.translatePath(os.path.join(USERDATA,'playlists'))
DATABASE     =  xbmc.translatePath(os.path.join(USERDATA,'Database'))
ADDONS       =  xbmc.translatePath(os.path.join('special://home','addons',''))
CBADDONPATH  =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'default.py'))
GUISETTINGS  =  os.path.join(USERDATA,'guisettings.xml')
GUI          =  xbmc.translatePath(os.path.join(USERDATA,'guisettings.xml'))
GUIFIX       =  xbmc.translatePath(os.path.join(USERDATA,'guifix.xml'))
INSTALL      =  xbmc.translatePath(os.path.join(USERDATA,'install.xml'))
FAVS         =  xbmc.translatePath(os.path.join(USERDATA,'favourites.xml'))
SOURCE       =  xbmc.translatePath(os.path.join(USERDATA,'sources.xml'))
ADVANCED     =  xbmc.translatePath(os.path.join(USERDATA,'advancedsettings.xml'))
PROFILES     =  xbmc.translatePath(os.path.join(USERDATA,'profiles.xml'))
RSS          =  xbmc.translatePath(os.path.join(USERDATA,'RssFeeds.xml'))
KEYMAPS      =  xbmc.translatePath(os.path.join(USERDATA,'keymaps','keyboard.xml'))
WIPE 		 =  xbmc.translatePath('special://home/wipe.xml')
MARKER          =  xbmc.translatePath(os.path.join(USERDATA,'MARKER.txt'))
CLEAN 		 =  xbmc.translatePath('special://home/clean.xml')
FRESH        = 0
notifyart    =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'resources/'))
skin         =  xbmc.getSkinDir()
userdatafolder = xbmc.translatePath(os.path.join(ADDON_DATA,AddonID))
zip = 'special://home/addons/plugin.video.projectxwizard'
urlbase      =  'None'
mastercopy   =  ADDON.getSetting('mastercopy')
dialog = xbmcgui.Dialog()
urlupdate =  ""
updatename =  "projectx_update"
CHECKVERSION  =  os.path.join(USERDATA,'version.txt')
my_addon = xbmcaddon.Addon()
dp = xbmcgui.DialogProgress()
checkver=my_addon.getSetting('checkupdates')
dialog = xbmcgui.Dialog()

def FRESHSTART():
    if FRESH == 1:
        dialog.ok(AddonTitle,'Please switch to the default Confluence skin','before performing a wipe.','')
        xbmc.executebuiltin("ActivateWindow(appearancesettings)")
        return
    else:
        choice2 = xbmcgui.Dialog().yesno("[COLOR=red]ABSOLUTELY CERTAIN?!!![/COLOR]", 'Are you absolutely certain you want to wipe this install?', '', 'Everything EXCLUDING THIS WIZARD & YOUR BACKUPS will be completely wiped!', yeslabel='[COLOR=green]Yes[/COLOR]',nolabel='[COLOR=red]No[/COLOR]')
    if choice2 == 0:
        return
    elif choice2 == 1:
	dp.create(AddonTitle,"Wiping Install",'Wiping Now.............', 'Please Wait')
        try:
            for root, dirs, files in os.walk(HOME,topdown=True):
                dirs[:] = [d for d in dirs if d not in EXCLUDES]
                for name in files:
                    try:
                        os.remove(os.path.join(root,name))
                        os.rmdir(os.path.join(root,name))
                    except: pass
                        
                for name in dirs:
                    try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                    except: pass
        except: pass
	
	dp.create(AddonTitle,"Wiping Install",'Removing empty folders.', 'Please Wait')
    Common.REMOVE_EMPTY_FOLDERS()
    Common.REMOVE_EMPTY_FOLDERS()
    Common.REMOVE_EMPTY_FOLDERS()
    Common.REMOVE_EMPTY_FOLDERS()
    Common.REMOVE_EMPTY_FOLDERS()
    Common.REMOVE_EMPTY_FOLDERS()
    Common.REMOVE_EMPTY_FOLDERS()
    Common.REMOVE_EMPTY_FOLDERS()
    open(WIPE, "a")
	
    dialog.ok(AddonTitle,'Wipe Successful, please restart XBMC/Kodi for changes to take effect.','','')
    Common.killxbmc()

def WIPERESTORE():

    dp.create(AddonTitle,"Wiping Install",'Wiping Now.............', 'Please Wait')
    try:
        for root, dirs, files in os.walk(HOME,topdown=True):
            dirs[:] = [d for d in dirs if d not in EXCLUDES]
            for name in files:
                try:
                    os.remove(os.path.join(root,name))
                    os.rmdir(os.path.join(root,name))
                except: pass
                        
            for name in dirs:
                try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                except: pass
    except: pass

    dp.create(AddonTitle,"Wiping Install",'Removing empty folders.', 'Please Wait')
    Common.REMOVE_EMPTY_FOLDERS()
    Common.REMOVE_EMPTY_FOLDERS()
    Common.REMOVE_EMPTY_FOLDERS()
    Common.REMOVE_EMPTY_FOLDERS()
    Common.REMOVE_EMPTY_FOLDERS()
    Common.REMOVE_EMPTY_FOLDERS()
    Common.REMOVE_EMPTY_FOLDERS()
    Common.REMOVE_EMPTY_FOLDERS()

    if os.path.exists(DATABASE):
		try:
			shutil.rmtree(DATABASE)
		except:
			pass