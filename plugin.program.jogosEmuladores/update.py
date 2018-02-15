import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import urllib2,urllib
import re
import glob
import extract
import downloader
import time
import common as Common
import wipe

AddonTitle="[COLOR ghostwhite]Project X[/COLOR] [COLOR lightsteelblue]Wizard[/COLOR]"
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
CHECKVERSION  =  os.path.join(USERDATA,'version.txt')
JarvisWiz = "http://projectxwizard.netne.net/ProjectXwizard/JarvisWiz.xml"
KryptonWiz = "http://projectxwizard.netne.net/ProjectXwizard/KryptonWiz.xml"
JarvisOne = "http://projectxwizard.netne.net/ProjectXwizard/JarvisOne.xml"
JarvisTwo = "http://projectxwizard.netne.net/ProjectXwizard/JarvisTwo.xml"
KryptonOne = "http://projectxwizard.netne.net/ProjectXwizard/KryptonOne.xml"
KryptonTwo = "http://projectxwizard.netne.net/ProjectXwizard/KryptonTwo.xml"
dp = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()

if xbmc.getCondVisibility('system.platform.ios') or xbmc.getCondVisibility('system.platform.osx'):
	JarvisWiz = "http://projectxwizard.netne.net/ProjectXwizard/JarvisWiz.xml"
	KryptonWiz = "http://projectxwizard.netne.net/ProjectXwizard/KryptonWiz.xml"
	BetaWiz = "http://projectxwizard.netne.net/ProjectXwizard/BetaWiz.xml"
	JarvisOne = "http://projectxwizard.netne.net/ProjectXwizard/JarvisOne.xml"
	JarvisTwo = "http://projectxwizard.netne.net/ProjectXwizard/JarvisTwo.xml"
	KryptonOne = "http://projectxwizard.netne.net/ProjectXwizard/KryptonOne.xml"
	KryptonTwo = "http://projectxwizard.netne.net/ProjectXwizard/KryptonTwo.xml"
	BetaOne = "http://projectxwizard.netne.net/ProjectXwizard/BetaOne.xml"
	BetaTwo = "http://projectxwizard.netne.net/ProjectXwizard/BetaTwo.xml"
else:
	JarvisWiz = "http://projectxwizard.netne.net/ProjectXwizard/JarvisWiz.xml"
	KryptonWiz = "http://projectxwizard.netne.net/ProjectXwizard/KryptonWiz.xml"
	BetaWiz = "http://projectxwizard.netne.net/ProjectXwizard/BetaWiz.xml"
	JarvisOne = "http://projectxwizard.netne.net/ProjectXwizard/JarvisOne.xml"
	JarvisTwo = "http://projectxwizard.netne.net/ProjectXwizard/JarvisTwo.xml"
	KryptonOne = "http://projectxwizard.netne.net/ProjectXwizard/KryptonOne.xml"
	KryptonTwo = "http://projectxwizard.netne.net/ProjectXwizard/KryptonTwo.xml"
	BetaOne = "http://projectxwizard.netne.net/ProjectXwizard/BetaOne.xml"
	BetaTwo = "http://projectxwizard.netne.net/ProjectXwizard/BetaTwo.xml"

############################
###CHECK FOR UPDATES########
############################

def updatecheck():

    dp.create(AddonTitle,"[COLOR ghostwhite]Checking all repositories for addon updates.[/COLOR]",'[COLOR yellow]This will take approximately 10 seconds.[/COLOR]', '[COLOR ghostwhite]Please wait...[/COLOR]') 
    xbmc.executebuiltin("UpdateAddonRepos")
    xbmc.executebuiltin("UpdateLocalAddons")
    time.sleep ( 10 )
    if not os.path.exists(CHECKVERSION):
		dialog.ok(AddonTitle,'[COLOR ghostwhite]All repositories have been checked for updates.[/COLOR]','[COLOR powderblue]All available addon updates have now been installed.[/COLOR]','')
		sys.exit(1)
    choice = xbmcgui.Dialog().yesno(AddonTitle,'[COLOR ghostwhite]All repositories have been checked for updates.[/COLOR]','[COLOR powderblue]All available addon updates have now been installed.[/COLOR]','[COLOR yellow]Check for build updates now?[/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
    if choice == 1:
        update()
    else:
    	sys.exit(1)

def update():

	JarvisUpdate = 0
	KryptonUpdate = 0
	BetaUpdate = 0
	dialog = xbmcgui.Dialog()

	try:
	    response = urllib2.urlopen(JarvisTwo)
	except:
	    JarvisUpdate = 1
	    dialog.ok(AddonTitle,'Sorry we are unable to check for [B]JARVIS[/B] updates!','The Jarvis update host appears to be down.','')

	try:
	    response = urllib2.urlopen(KryptonTwo)
	except:
	    KryptonUpdate = 1
	    dialog.ok(AddonTitle,'Sorry we are unable to check for [B]KRYPTON[/B] updates!','The update host appears to be down.','Please check for updates later via the wizard.')

	try:
	    response = urllib2.urlopen(BetaTwo)
	except:
	    BetaUpdate = 1
	    dialog.ok(AddonTitle,'Sorry we are unable to check for [B]BETA[/B] updates!','The update host appears to be down.','Please check for updates later via the wizard.')

#######################################################################
#						Check for Jarvis Updates
#######################################################################

	if JarvisUpdate == 0:
		dialog = xbmcgui.Dialog()
		checkurl = JarvisTwo
		vers = open(CHECKVERSION, "r")
		regex = re.compile(r'<build>(.+?)</build><version>(.+?)</version>')
		for line in vers:
			if JarvisUpdate == 0:
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
								choice = xbmcgui.Dialog().yesno("NEW UPDATE AVAILABLE", 'Found a new update for the Build', build + " ver: "+newversion, 'Do you want to install it now?', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
								if choice == 1: 
									if fresh =='false': # TRUE
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
											addonfolder = xbmc.translatePath(os.path.join('special://','home'))
											time.sleep(2)
											dp.update(0,"", "Extracting Zip Please Wait")
											print '======================================='
											print addonfolder
											print '======================================='
											extract.all(lib,addonfolder,dp)
											dialog.ok(AddonTitle, "To save changes you now need to force close Kodi, Press OK to force close Kodi")
										
											Common.killxbmc()
																		
									else:
										dialog.ok(AddonTitle,'[COLOR red]A WIPE (FACTORY RESET)[/COLOR] is required for the update... [COLOR red]WOULD YOU LIKE TO WIPE THE SYSTEM NOW?[/COLOR]','','')
										wipe.FRESHSTART()
							else:
								dialog.ok(AddonTitle,'[COLOR ghostwhite]Your build is up to date.[/COLOR]', "[COLOR ghostwhite]Current Build: [/COLOR][COLOR yellow]" + build + "[/COLOR]", "[COLOR ghostwhite]Current Version: [/COLOR][COLOR yellow]" + newversion + "[/COLOR]")

#######################################################################
#						Check for Krypton Updates
#######################################################################

	if KryptonUpdate == 0:
		dialog = xbmcgui.Dialog()
		checkurl = KryptonTwo
		vers = open(CHECKVERSION, "r")
		regex = re.compile(r'<build>(.+?)</build><version>(.+?)</version>')
		for line in vers:
			if KryptonUpdate == 0:
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
								choice = xbmcgui.Dialog().yesno("NEW UPDATE AVAILABLE", 'Found a new update for the Build', build + " ver: "+newversion, 'Do you want to install it now?', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
								if choice == 1: 
									if fresh =='false': # TRUE
										updateurl = KryptonOne
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
											print '======================================='
											print addonfolder
											print '======================================='
											extract.all(lib,addonfolder,dp)
											dialog.ok(AddonTitle, "To save changes you now need to force close Kodi, Press OK to force close Kodi")
										
											common.killxbmc()()
																		
									else:
										dialog.ok('[COLOR red]A WIPE is required for the update[/COLOR]','Select the [COLOR green]YES[/COLOR] option in the NEXT WINDOW to wipe now.','Select the [COLOR red]NO[/COLOR] option in the NEXT WINDOW to update later.','[I][COLOR powderblue]If you wish to update later you can do so in [/COLOR][COLOR ghostwhite]Project X[/COLOR] [COLOR lightsteelblue]Wizard[/COLOR][/I]')
										wipe.FRESHSTART()
							else:
								dialog.ok(AddonTitle,'[COLOR ghostwhite]Your build is up to date.[/COLOR]', "[COLOR ghostwhite]Current Build: [/COLOR][COLOR yellow]" + build + "[/COLOR]", "[COLOR ghostwhite]Current Version: [/COLOR][COLOR yellow]" + newversion + "[/COLOR]")
								
#######################################################################
#						Check for Beta Updates
#######################################################################

	if BetaUpdate == 0:
		dialog = xbmcgui.Dialog()
		checkurl = BetaTwo
		vers = open(CHECKVERSION, "r")
		regex = re.compile(r'<build>(.+?)</build><version>(.+?)</version>')
		for line in vers:
			if KryptonUpdate == 0:
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
								choice = xbmcgui.Dialog().yesno("NEW UPDATE AVAILABLE", 'Found a new update for the Build', build + " ver: "+newversion, 'Do you want to install it now?', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
								if choice == 1: 
									if fresh =='false': # TRUE
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
											print '======================================='
											print addonfolder
											print '======================================='
											extract.all(lib,addonfolder,dp)
											dialog.ok(AddonTitle, "To save changes you now need to force close Kodi, Press OK to force close Kodi")
										
											common.killxbmc()()
																		
									else:
										dialog.ok('[COLOR red]A WIPE is required for the update[/COLOR]','Select the [COLOR green]YES[/COLOR] option in the NEXT WINDOW to wipe now.','Select the [COLOR red]NO[/COLOR] option in the NEXT WINDOW to update later.','[I][COLOR powderblue]If you wish to update later you can do so in [/COLOR][COLOR ghostwhite]Project X[/COLOR] [COLOR lightsteelblue]Wizard[/COLOR][/I]')
										wipe.FRESHSTART()
							else:
								dialog.ok(AddonTitle,'[COLOR ghostwhite]Your build is up to date.[/COLOR]', "[COLOR ghostwhite]Current Build: [/COLOR][COLOR yellow]" + build + "[/COLOR]", "[COLOR ghostwhite]Current Version: [/COLOR][COLOR yellow]" + newversion + "[/COLOR]")