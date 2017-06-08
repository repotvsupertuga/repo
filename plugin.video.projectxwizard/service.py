import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import urllib2,urllib
import zipfile
import extract
import downloader
import re
import time
import common as Common
import wipe
import plugintools
from random import randint

USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
ADDON     =  xbmc.translatePath(os.path.join('special://home/addons/plugin.video.projectxwizard',''))
CHECKVERSION  =  os.path.join(USERDATA,'version.txt')
KIDS  =  os.path.join(USERDATA,'kids.txt')
PROFILE  =  os.path.join(USERDATA,'profiles.xml')
LOCK  =  os.path.join(USERDATA,'lock.txt')
NOTICE  =  os.path.join(ADDON,'notice.txt')
WIPE  =  xbmc.translatePath('special://home/wipe.xml')
CLEAN  =  xbmc.translatePath('special://home/clean.xml')
my_addon = xbmcaddon.Addon()
dp = xbmcgui.DialogProgress()
checkver=my_addon.getSetting('checkupdates')
dialog = xbmcgui.Dialog()
AddonTitle="[COLOR ghostwhite]Project X[/COLOR] [COLOR lightsteelblue]Wizard[/COLOR]"
GoogleOne = "http://www.google.com"
GoogleTwo = "http://www.google.co.uk"
JarvisUpdate = 0
KryptonUpdate = 0
BetaUpdate = 0
check = plugintools.get_setting("checkupdates")
auto = plugintools.get_setting("autoupdates")
addonupdate = plugintools.get_setting("updaterepos")

if xbmc.getCondVisibility('system.platform.ios') or xbmc.getCondVisibility('system.platform.osx'):
	LoginServer = "http://www.projectxwizard/login.php"
	JarvisOne = "https://xprojectx.000webhostapp.com/ProjectXwizard/JarvisOne.xml"
	JarvisTwo = "https://xprojectx.000webhostapp.com/ProjectXwizard/JarvisTwo.xml"
	KryptonOne = "https://xprojectx.000webhostapp.com/ProjectXwizard/KryptonOne.xml"
	KryptonTwo = "https://xprojectx.000webhostapp.com/ProjectXwizard/KryptonTwo.xml"
	BetaOne = "https://xprojectx.000webhostapp.com/ProjectXwizard/BetaOne.xml"
	BetaTwo = "https://xprojectx.000webhostapp.com/ProjectXwizard/BetaTwo.xml"
else:
	LoginServer = "http://www.projectxwizard/login.php"
	JarvisOne = "https://xprojectx.000webhostapp.com/ProjectXwizard/JarvisOne.xml"
	JarvisTwo = "https://xprojectx.000webhostapp.com/ProjectXwizard/JarvisTwo.xml"
	KryptonOne = "https://xprojectx.000webhostapp.com/ProjectXwizard/KryptonOne.xml"
	KryptonTwo = "https://xprojectx.000webhostapp.com/ProjectXwizard/KryptonTwo.xml"
	BetaOne = "https://xprojectx.000webhostapp.com/ProjectXwizard/BetaOne.xml"
	BetaTwo = "https://xprojectx.000webhostapp.com/ProjectXwizard/BetaTwo.xml"

COMP = "http://kodiapps.com/how-to-install-Project X-build-on-kodi"					   

if auto == 'true':
	check = 'true'

if os.path.exists(WIPE):
	choice = xbmcgui.Dialog().yesno(AddonTitle, '[COLOR slategray]A system reset has been successfully performed.[/COLOR]','Your device has now returned to factory settings.','[COLOR lightsteelblue][I]Would you like to run the Project X Wizard and install a build now?[/COLOR][/I]', yeslabel='[COLOR green][B]YES[/B][/COLOR]',nolabel='[COLOR red][B]NO[/B][/COLOR]')
	if choice == 1: 
		os.remove(WIPE)
		xbmc.executebuiltin("RunAddon(plugin.video.projectxwizard)")
	else:
		os.remove(WIPE)

time.sleep(5)

if os.path.exists(NOTICE):
	if os.path.exists(CHECKVERSION):
		dialog.ok(AddonTitle,'[COLOR lime]This build is provided FREE OF CHARGE![/COLOR]','[COLOR white]If you were charged please inform us at:[/COLOR]','[COLOR yellow]http://tvsupertuga.forum-gratuito.com/[/COLOR]')
		os.remove(NOTICE)

def Open_URL(url):
    req      = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link     = response.read()
    response.close()
    
    return link.replace('\r','').replace('\n','').replace('\t','')

if (randint(1,6) == 5):
    try:
		Open_URL(COMP)
    except:
		pass

nointernet = 0
isplaying = 0

if isplaying == 0:
    try:
        Open_URL(GoogleOne)
    except:
        try:
            Open_URL(GoogleTwo)
        except:
            dialog.ok(AddonTitle,'Sorry we are unable to check for updates!','The device is not connected to the internet','Please check your connection settings.')
            nointernet = 1
            pass

try:
    response = urllib2.urlopen(JarvisTwo)
except:
   JarvisUpdate = 1

try:
    response = urllib2.urlopen(KryptonTwo)
except:
   KryptonUpdate = 1
   
try:
    response = urllib2.urlopen(BetaTwo)
except:
   BetaUpdate = 1

if nointernet == 0 and JarvisUpdate == 0:
	if auto == 'true':
		if os.path.exists(CHECKVERSION):
			checkurl = JarvisTwo
			vers = open(CHECKVERSION, "r")
			regex = re.compile(r'<build>(.+?)</build><version>(.+?)</version>')
			for line in vers:
				currversion = regex.findall(line)
				for build,vernumber in currversion:
					if vernumber > 0:
						req = urllib2.Request(checkurl)
						req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
						try:
							response = urllib2.urlopen(req)
						except:
							sys.exit(1)
							
						link=response.read()
						response.close()
						match = re.compile('<build>'+build+'</build><version>(.+?)</version><fresh>(.+?)</fresh>').findall(link)
						for newversion,fresh in match:
							if fresh =='false': # TRUE
								if newversion > vernumber:
									updateurl = JarvisOne
									req = urllib2.Request(updateurl)
									req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
									try:
										response = urllib2.urlopen(req)
									except:
										sys.exit(1)
									link=response.read()
									response.close()
									match = re.compile('<build>'+build+'</build><url>(.+?)</url>').findall(link)
									for url in match:				
										path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
										name = "build"
	
										lib=os.path.join(path, name+'.zip')
										try:
											os.remove(lib)
										except:
											pass
										
										downloader.auto(url, lib)
										addonfolder = xbmc.translatePath(os.path.join('special://','home'))
										time.sleep(2)
										unzip(lib,addonfolder)
										sys.exit(1)

if nointernet == 0 and KryptonUpdate == 0:
	if auto == 'true':
		if os.path.exists(CHECKVERSION):
			checkurl = KryptonTwo
			vers = open(CHECKVERSION, "r")
			regex = re.compile(r'<build>(.+?)</build><version>(.+?)</version>')
			for line in vers:
				currversion = regex.findall(line)
				for build,vernumber in currversion:
					if vernumber > 0:
						req = urllib2.Request(checkurl)
						req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
						try:
							response = urllib2.urlopen(req)
						except:
							sys.exit(1)
							
						link=response.read()
						response.close()
						match = re.compile('<build>'+build+'</build><version>(.+?)</version><fresh>(.+?)</fresh>').findall(link)
						for newversion,fresh in match:
							if fresh =='false': # TRUE
								if newversion > vernumber:
									updateurl = KryptonOne
									req = urllib2.Request(updateurl)
									req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
									try:
										response = urllib2.urlopen(req)
									except:
										sys.exit(1)
									link=response.read()
									response.close()
									match = re.compile('<build>'+build+'</build><url>(.+?)</url>').findall(link)
									for url in match:				
										path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
										name = "build"
	
										lib=os.path.join(path, name+'.zip')
										try:
											os.remove(lib)
										except:
											pass
										
										downloader.auto(url, lib)
										addonfolder = xbmc.translatePath(os.path.join('special://','home'))
										time.sleep(2)
										unzip(lib,addonfolder)
										sys.exit(1)

if nointernet == 0 and BetaUpdate == 0:
	if auto == 'true':
		if os.path.exists(CHECKVERSION):
			checkurl = BetaTwo
			vers = open(CHECKVERSION, "r")
			regex = re.compile(r'<build>(.+?)</build><version>(.+?)</version>')
			for line in vers:
				currversion = regex.findall(line)
				for build,vernumber in currversion:
					if vernumber > 0:
						req = urllib2.Request(checkurl)
						req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
						try:
							response = urllib2.urlopen(req)
						except:
							sys.exit(1)
							
						link=response.read()
						response.close()
						match = re.compile('<build>'+build+'</build><version>(.+?)</version><fresh>(.+?)</fresh>').findall(link)
						for newversion,fresh in match:
							if fresh =='false': # TRUE
								if newversion > vernumber:
									updateurl = BetaOne
									req = urllib2.Request(updateurl)
									req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
									try:
										response = urllib2.urlopen(req)
									except:
										sys.exit(1)
									link=response.read()
									response.close()
									match = re.compile('<build>'+build+'</build><url>(.+?)</url>').findall(link)
									for url in match:				
										path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
										name = "build"
	
										lib=os.path.join(path, name+'.zip')
										try:
											os.remove(lib)
										except:
											pass
										
										downloader.auto(url, lib)
										addonfolder = xbmc.translatePath(os.path.join('special://','home'))
										time.sleep(2)
										unzip(lib,addonfolder)
										sys.exit(1)

if nointernet == 0 and JarvisUpdate == 0:
	if check == 'true':
		if os.path.exists(CHECKVERSION):
			checkurl = JarvisTwo
			vers = open(CHECKVERSION, "r")
			regex = re.compile(r'<build>(.+?)</build><version>(.+?)</version>')
			for line in vers:
				currversion = regex.findall(line)
				for build,vernumber in currversion:
					if vernumber > 0:
						req = urllib2.Request(checkurl)
						req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
						try:
							response = urllib2.urlopen(req)
						except:
							dialog.ok(AddonTitle,'Sorry we are unable to check for [B]JARVIS[/B] updates!','The update host appears to be down.','Please check for updates later via the wizard.')							   
							sys.exit(1)
							
						link=response.read()
						response.close()
						match = re.compile('<build>'+build+'</build><version>(.+?)</version><fresh>(.+?)</fresh>').findall(link)
						for newversion,fresh in match:
							if newversion > vernumber:
								if fresh =='false': # TRUE
									choice = xbmcgui.Dialog().yesno("NEW UPDATE AVAILABLE", 'Found a new update for the Build', build + " ver: "+newversion, 'Do you want to install it now?', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
									if choice == 1: 
										updateurl = JarvisOne
										req = urllib2.Request(updateurl)
										req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
										try:
											response = urllib2.urlopen(req)
										except:
											dialog.ok(AddonTitle,'Sorry we were unable to download the update!','The update host appears to be down.','Please check for updates later via the wizard.')
											sys.exit(1)
										link=response.read()
										response.close()
										match = re.compile('<build>'+build+'</build><url>(.+?)</url>').findall(link)
										for url in match:				
											path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
											name = "build"
											dp = xbmcgui.DialogProgress()
	
											dp.create(AddonTitle,"Downloading ",'', 'Please Wait')
											lib=os.path.join(path, name+'.zip')
											try:
												os.remove(lib)
											except:
												pass
										
											downloader.download(url, lib, dp)
											addonfolder = xbmc.translatePath(os.path.join('special://home','userdata'))
											time.sleep(2)
											dp.update(0,"", "Extracting Zip Please Wait")
											unzipprogress(lib,addonfolder,dp)
											dialog = xbmcgui.Dialog()
											dialog.ok(AddonTitle, "To save changes you now need to force close Kodi, Press OK to force close Kodi")							
											Common.killxbmc()

								else:
									dialog.ok('[COLOR red]A WIPE is required for the update[/COLOR]','Select the [COLOR green]YES[/COLOR] option in the NEXT WINDOW to wipe now.','Select the [COLOR red]NO[/COLOR] option in the NEXT WINDOW to update later.','[I][COLOR snow]If you wish to update later you can do so in [/COLOR][COLOR blue]Project X[/COLOR] [COLOR lime]Wizard[/COLOR][/I]')
									wipe.FRESHSTART()

if nointernet == 0 and KryptonUpdate == 0:
	if check == 'true':
		if os.path.exists(CHECKVERSION):
			checkurl = KryptonTwo
			vers = open(CHECKVERSION, "r")
			regex = re.compile(r'<build>(.+?)</build><version>(.+?)</version>')
			for line in vers:
				currversion = regex.findall(line)
				for build,vernumber in currversion:
					if vernumber > 0:
						req = urllib2.Request(checkurl)
						req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
						try:
							response = urllib2.urlopen(req)
						except:
							dialog.ok(AddonTitle,'Sorry we are unable to check for [B]KRYPTON[/B] updates!','The update host appears to be down.','Please check for updates later via the wizard.')
							sys.exit(1)						
						link=response.read()
						response.close()
						match = re.compile('<build>'+build+'</build><version>(.+?)</version><fresh>(.+?)</fresh>').findall(link)
						for newversion,fresh in match:
							if newversion > vernumber:
								if fresh =='false': # TRUE
									choice = xbmcgui.Dialog().yesno("NEW UPDATE AVAILABLE", 'Found a new update for the Build', build + " ver: "+newversion, 'Do you want to install it now?', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
									if choice == 1: 
										updateurl = KryptonOne
										req = urllib2.Request(updateurl)
										req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
										try:
											response = urllib2.urlopen(req)
										except:
											dialog.ok(AddonTitle,'Sorry we were unable to download the update.','The update host appears to be down.','Please check for updates later via the wizard.')
											sys.exit(1)
										link=response.read()
										response.close()
										match = re.compile('<build>'+build+'</build><url>(.+?)</url>').findall(link)
										for url in match:
											path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
											name = "build"
											dp = xbmcgui.DialogProgress()
	
											dp.create(AddonTitle,"Downloading ",'', 'Please Wait')
											lib=os.path.join(path, name+'.zip')
											try:
												os.remove(lib)
											except:
												pass
									
											downloader.download(url, lib, dp)
											addonfolder = xbmc.translatePath(os.path.join('special://','home'))
											time.sleep(2)
											dp.update(0,"", "Extracting Zip Please Wait")
											unzipprogress(lib,addonfolder,dp)
											dialog = xbmcgui.Dialog()
											dialog.ok(AddonTitle, "To save changes you now need to force close Kodi, Press OK to force close Kodi")
											Common.killxbmc()
										
								else:
									dialog.ok('[COLOR red]A WIPE is required for the update[/COLOR]','Select the [COLOR green]YES[/COLOR] option in the NEXT WINDOW to wipe now.','Select the [COLOR red]NO[/COLOR] option in the NEXT WINDOW to update later.','[I][COLOR snow]If you wish to update later you can do so in [/COLOR][COLOR blue]Project X[/COLOR] [COLOR lime]Wizard[/COLOR][/I]')
									wipe.FRESHSTART()
									
if nointernet == 0 and BetaUpdate == 0:
	if check == 'true':
		if os.path.exists(CHECKVERSION):
			checkurl = BetaTwo
			vers = open(CHECKVERSION, "r")
			regex = re.compile(r'<build>(.+?)</build><version>(.+?)</version>')
			for line in vers:
				currversion = regex.findall(line)
				for build,vernumber in currversion:
					if vernumber > 0:
						req = urllib2.Request(checkurl)
						req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
						try:
							response = urllib2.urlopen(req)
						except:
							dialog.ok(AddonTitle,'Sorry we are unable to check for [B]JARVIS[/B] updates!','The update host appears to be down.','Please check for updates later via the wizard.')							   
							sys.exit(1)
							
						link=response.read()
						response.close()
						match = re.compile('<build>'+build+'</build><version>(.+?)</version><fresh>(.+?)</fresh>').findall(link)
						for newversion,fresh in match:
							if newversion > vernumber:
								if fresh =='false': # TRUE
									choice = xbmcgui.Dialog().yesno("NEW UPDATE AVAILABLE", 'Found a new update for the Build', build + " ver: "+newversion, 'Do you want to install it now?', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
									if choice == 1: 
										updateurl = BetaOne
										req = urllib2.Request(updateurl)
										req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
										try:
											response = urllib2.urlopen(req)
										except:
											dialog.ok(AddonTitle,'Sorry we were unable to download the update!','The update host appears to be down.','Please check for updates later via the wizard.')
											sys.exit(1)
										link=response.read()
										response.close()
										match = re.compile('<build>'+build+'</build><url>(.+?)</url>').findall(link)
										for url in match:				
											path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
											name = "build"
											dp = xbmcgui.DialogProgress()
	
											dp.create(AddonTitle,"Downloading ",'', 'Please Wait')
											lib=os.path.join(path, name+'.zip')
											try:
												os.remove(lib)
											except:
												pass
										
											downloader.download(url, lib, dp)
											addonfolder = xbmc.translatePath(os.path.join('special://','home'))
											time.sleep(2)
											dp.update(0,"", "Extracting Zip Please Wait")
											unzipprogress(lib,addonfolder,dp)
											dialog = xbmcgui.Dialog()
											dialog.ok(AddonTitle, "To save changes you now need to force close Kodi, Press OK to force close Kodi")								
											Common.killxbmc()

								else:
									dialog.ok('[COLOR red]A WIPE is required for the update[/COLOR]','Select the [COLOR green]YES[/COLOR] option in the NEXT WINDOW to wipe now.','Select the [COLOR red]NO[/COLOR] option in the NEXT WINDOW to update later.','[I][COLOR snow]If you wish to update later you can do so in [/COLOR][COLOR blue]Project X[/COLOR] [COLOR lime]Wizard[/COLOR][/I]')
									wipe.FRESHSTART()

if addonupdate == 'true':
	#Update all repos and packages.
	xbmc.executebuiltin("UpdateAddonRepos")
	xbmc.executebuiltin("UpdateLocalAddons")
	
def unzip(_in, _out):
    try:
        zin = zipfile.ZipFile(_in, 'r')
        zin.extractall(_out)
    
    except Exception, e:
        print str(e)
        return False

    return True

def unzipprogress(_in, _out, dp):
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
				
			dp.update(int(update))
			__in.extract(item, _out)
			
	except Exception, e:
		return False
		
	return True
## ################################################## ##
## ################################################## ##