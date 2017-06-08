import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys
import shutil
import urllib2,urllib
import re
import extract
import time
import downloader
import plugintools
import zipfile
import ntpath
import common as Common
from os import listdir
from os.path import isfile, join
import parameters
import wipe

base = 'http://tvsupertuga.forum-gratuito.com/'
dp           =  xbmcgui.DialogProgress()
AddonTitle="[COLOR ghostwhite]Project X[/COLOR] [COLOR lightsteelblue]Wizard[/COLOR]"
AddonID ='plugin.video.projectxwizard'
selfAddon = xbmcaddon.Addon(id=AddonID)
backupfull = selfAddon.getSetting('backup_database')
backupaddons = selfAddon.getSetting('backup_addon_data')
ADDON_DATA   =  xbmc.translatePath(os.path.join('special://','home'))
PACKAGES = xbmc.translatePath(os.path.join('special://home/addons/' + 'packages'))
dialog = xbmcgui.Dialog()  
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID, 'icon.png'))
mastercopy   =  selfAddon.getSetting('mastercopy')
HOME         =  xbmc.translatePath('special://home/')
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
zip = plugintools.get_setting("zip")
USB          =  xbmc.translatePath(os.path.join(zip))
HOME         =  xbmc.translatePath('special://home/')

params=parameters.get_params()

def _get_keyboard( default="", heading="", hidden=False ):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        return unicode( keyboard.getText(), "utf-8" )
    return default

def Backup():
    guisuccess=1
    if not os.path.exists(USB):
        os.makedirs(USB)
    if os.path.exists(PACKAGES):
        shutil.rmtree(PACKAGES)
    vq = _get_keyboard( heading="Enter a name for this backup" )
    if ( not vq ): return False, 0
    title = urllib.quote_plus(vq)
    backup_zip = xbmc.translatePath(os.path.join(USB,title+'.zip'))
    exclude_dirs =  ['plugin.video.projectxwizard','repository.tdbegley.official','backupdir','cache', 'system', 'Thumbnails']
    exclude_files = ["spmc.log","spmc.old.log","xbmc.log","xbmc.old.log","kodi.log","kodi.old.log","Textures13.db"]
    message_header = "Creating full backup..."
    message_header2 = "Creating full backup..."
    message1 = "Archiving..."
    message2 = ""
    message3 = "Please Wait"
    FIX_SPECIAL(USERDATA)
    ARCHIVE_CB(HOME, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
    time.sleep(1)
    dialog.ok("[COLOR green][B]SUCCESS![/B][/COLOR]", 'The backup was completed successfully!.',"Backup Location: ",'[COLOR=yellow]'+backup_zip+'[/COLOR]')

def ARCHIVE_CB(sourcefile, destfile, message_header, message1, message2, message3, exclude_dirs, exclude_files):
    zipobj = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(sourcefile)
    for_progress = []
    ITEM =[]
    dp.create(message_header, message1, message2, message3)
    for base, dirs, files in os.walk(sourcefile):
        for file in files:
            ITEM.append(file)
    N_ITEM =len(ITEM)
    for base, dirs, files in os.walk(sourcefile):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        files[:] = [f for f in files if f not in exclude_files]
        for file in files:
            for_progress.append(file) 
            progress = len(for_progress) / float(N_ITEM) * 100  
            dp.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
            fn = os.path.join(base, file)
            if not 'temp' in dirs:
                if not 'plugin.video.projectxwizard' in dirs:
                   import time
                   FORCE= '01/01/1980'
                   FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                   if FILE_DATE > FORCE:
                       zipobj.write(fn, fn[rootlen:])  
    zipobj.close()
    dp.close()

def FIX_SPECIAL(HOME):
    HOME         =  xbmc.translatePath('special://home')
    dialog = xbmcgui.Dialog()
    dp.create(AddonTitle,"Renaming paths...",'', 'Please Wait')
    for root, dirs, files in os.walk(HOME):  #Search all xml files and replace physical with special
        for file in files:
            if file.endswith(".xml"):
                 dp.update(0,"Fixing","[COLOR yellow]" + file + "[/COLOR]", "Please wait.....")
                 a=open((os.path.join(root, file))).read()
                 b=a.replace(HOME, 'special://home/')
                 f = open((os.path.join(root, file)), mode='w')
                 f.write(str(b))
                 f.close()
				
def Restore():
	addonfolder = xbmc.translatePath(os.path.join('special://','home'))
	for file in os.listdir(USB):
		if file.endswith(".zip"):
			url =  xbmc.translatePath(os.path.join(USB,file))
			Common.addItem(file,url,100,ICON,ICON,'')
		

def READ_ZIP(url):

	if dialog.yesno(AddonTitle,"[COLOR yellow]" + url + "[/COLOR]","Do you want to restore this backup?"):
		wipe.WIPERESTORE()
	
		zin    = zipfile.ZipFile(url,  'r')
		nFiles = float(len(zin.infolist()))
		count  = 0

		try:
			for item in zin.infolist():
				dp.create(AddonTitle,"Extracting Backup","[COLOR yellow]" + url + "[/COLOR]","Please Wait...")
				count += 1
				update = count / nFiles * 100
				dp.update(int(update))
				try:
					zin.extract(item, HOME)
				except Exception, e:
					print str(e)
		except Exception, e:
			print str(e)
			return False
		dialog.ok(AddonTitle,'Restore Successful, please restart XBMC/Kodi for changes to take effect.','','')
		Common.killxbmc()
		return True
		
def ListBackDel():
	addonfolder = xbmc.translatePath(os.path.join('special://','home'))
	for file in os.listdir(USB):
		if file.endswith(".zip"):
			url =  xbmc.translatePath(os.path.join(USB,file))
			Common.addDir(file,url,101,ICON,ICON,'')
			
def DeleteBackup(url):
	if dialog.yesno(AddonTitle,"[COLOR yellow]" + url + "[/COLOR]","Do you want to delete this backup?"):
		os.remove(url)
		dialog.ok(AddonTitle,"[COLOR yellow]" + url + "[/COLOR]","Successfully deleted.")
		
def DeleteAllBackups():
	if dialog.yesno(AddonTitle,"Do you want to delete all backups?"):
		shutil.rmtree(USB)
		os.makedirs(USB)
		dialog.ok(AddonTitle,"All backups successfully deleted.")


##############################    END    #########################################

#######################################################################
#						Which mode to select
#######################################################################

url=None
name=None
mode=None
iconimage=None
fanart=None
description=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass

if mode==100:
	READ_ZIP(url)
	
elif mode==101:
	DeleteBackup(url)