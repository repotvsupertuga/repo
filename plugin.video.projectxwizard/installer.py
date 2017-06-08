import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys
import urllib2,urllib
import time
import downloader
import common as Common
import wipe
import zipfile
import hashlib

AddonTitle="[COLOR ghostwhite]Project X[/COLOR] [COLOR lightsteelblue]Wizard[/COLOR]"
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
CHECKVERSION  =  os.path.join(USERDATA,'version.txt')

############################
###INSTALL BUILD############
############################

def INSTALL(name,url,description):

	#Check is the packages folder exists, if not create it.
	path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
	if not os.path.exists(path):
		os.makedirs(path)

	wipeme = 0

	if name == "SKYLEX":
		wipeme = 1
		choice = xbmcgui.Dialog().yesno(AddonTitle, 'SKYLEX was designed for low end machines like Firesticks.','Recomended: Single Core CPU | 1GB RAM or more','[I][COLOR lightsteelblue]Would you like to download this build now?[/I][/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
		if choice == 0:
			sys.exit(1)

	if name == "TUGAPOWER":
		wipeme = 1
		choice = xbmcgui.Dialog().yesno(AddonTitle, 'TUGAPOWER was designed for high end machines like Firesticks Amazon Fire TV & Nvidia Shield.','Recomended: Single Core CPU | 1GB RAM or more','[I][COLOR lightsteelblue]Would you like to download this build now?[/I][/COLOR]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
		if choice == 0:
			sys.exit(1)

	if name == "300":
		wipeme = 1
		name = "300"
		choice = xbmcgui.Dialog().yesno(AddonTitle, '300 was designed for mid-level machines like MX8 & T8.','Recomended: Single Core CPU | 1GB RAM or more','[I][COLOR lightsteelblue]Would you like to download this build now?[/I][/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
		if choice == 0:
			sys.exit(1)

	if name == "FUTURAMA":
		wipeme = 1
		choice = xbmcgui.Dialog().yesno(AddonTitle, 'FUTURAMA was designed for mid-level machines like MX8 & T8.','Recomended: Single Core CPU | 1GB RAM or more','[I][COLOR lightsteelblue]Would you like to download this build now?[/I][/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
		if choice == 0:
			sys.exit(1)
			
	if name == "EURO 2016":
		wipeme = 1
		choice = xbmcgui.Dialog().yesno(AddonTitle, 'EURO 2016 was designed for mid-level machines like MX8 & T8.','Recomended: Single Core CPU | 1GB RAM or more','[I][COLOR lightsteelblue]Would you like to download this build now?[/I][/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
		if choice == 0:
			sys.exit(1)
			
	if name == "SONAR":
		wipeme = 1
		choice = xbmcgui.Dialog().yesno(AddonTitle, 'Sonaer is a BETA build that needs testing.','Recomended: Dual Core CPU | 2GB RAM or more','[I][COLOR lightsteelblue]Would you like to download this build now?[/I][/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
		if choice == 0:
			sys.exit(1)
	
	if name == "XXX ADDON EXPANSION PACK":
		if not os.path.exists(CHECKVERSION):
			dialog = xbmcgui.Dialog()
			dialog.ok(AddonTitle,'Sorry, you are not using a Project X Build.','This pack is only available for Project X Build users.')
			sys.exit(1)
			
	if name == "EMBER":
		wipeme = 1
		choice = xbmcgui.Dialog().yesno(AddonTitle, 'Ember is a BETA build that needs testing.','Recomended: Dual Core CPU | 2GB RAM or more','[I][COLOR lightsteelblue]Would you like to download this build now?[/I][/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
		if choice == 0:
			sys.exit(1)
	
	if name == "EMBER FOR FIRESTICKS":
		wipeme = 1
		choice = xbmcgui.Dialog().yesno(AddonTitle, 'Ember is a BETA build that needs testing.','Recomended: Amazon Fire Stick','[I][COLOR lightsteelblue]Would you like to download this build now?[/I][/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
		if choice == 0:
			sys.exit(1)

	if wipeme == 1:
		wipe.WIPERESTORE()

	path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
	if not os.path.exists(path):
		os.makedirs(path)
	buildname = name
	dp = xbmcgui.DialogProgress()
	dp.create(AddonTitle,"","","build: " + buildname)
	name = "build"
	lib=os.path.join(path, name+'.zip')
	
	try:
		os.remove(lib)
	except:
		pass
	
	downloader.download(url, lib, dp)
	addonfolder = xbmc.translatePath(os.path.join('special://','home'))
	time.sleep(2)
	dp.update(0,"","Extracting Zip Please Wait","")
	unzip(lib,addonfolder,dp)
	dialog = xbmcgui.Dialog()
	time.sleep(1)
	try:
		os.remove(lib)
	except:
		pass
	dialog.ok(AddonTitle, "To save changes you now need to force close Kodi, Press OK to force close Kodi")
	time.sleep(2)
	Common.killxbmc()
	
def INSTALLCOM(name,url,description):
	
	wipe.WIPERESTORE()
	#Check is the packages folder exists, if not create it.
	path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
	if not os.path.exists(path):
		os.makedirs(path)
	buildname = "[COLOR orangered]" + name + "[/COLOR]"
	dp = xbmcgui.DialogProgress()
	dp.create(AddonTitle,"","","build: " + buildname)
	name = "build"
	lib=os.path.join(path, name+'.zip')
	
	try:
		os.remove(lib)
	except:
		pass
	
	downloader.download(url, lib, dp)
	addonfolder = xbmc.translatePath(os.path.join('special://','home'))
	time.sleep(2)
	dp.update(0,"","Extracting build...","")
	unzip(lib,addonfolder,dp)
	dialog = xbmcgui.Dialog()
	time.sleep(1)
	try:
		os.remove(lib)
	except:
		pass
	dialog.ok(AddonTitle, "To save changes you now need to force close Kodi, Press OK to force close Kodi")
	time.sleep(2)
	Common.killxbmc()
	
def unzip(_in, _out, dp):
	__in = zipfile.ZipFile(_in,  'r')
	
	nofiles = float(len(__in.infolist()))
	count   = 0
	
	try:
		for item in __in.infolist():
			count += 1
			update = (count / nofiles) * 100
			
			if dp.iscanceled():
				dialog = xbmcgui.Dialog()
				dialog.ok(AddonTitle, 'Extraction was cancelled.')
				
				sys.exit()
				dp.close()
			
			try:
				dp.update(int(update))
				__in.extract(item, _out)
			
			except Exception, e:
				print str(e)

	except Exception, e:
		print str(e)
		return False
		
	return True