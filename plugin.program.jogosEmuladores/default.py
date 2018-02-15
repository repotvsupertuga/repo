import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import platform
import zipfile
import hashlib
import urllib2,urllib
import re
import glob
import time
import errno
import speedtest
import common as Common
import wipe
import versioncheck
import ServerStatus
import community
import installer
import update
import parameters
import maintenance
import plugintools
import backuprestore
import socket
import json

AddonTitle="[COLOR cyan]Jogos e[/COLOR] [COLOR lightsteelblue]Emuladores[/COLOR]"
AddonData = xbmc.translatePath('special://userdata/addon_data')
addon_id = 'plugin.program.jogosEmuladores'
ADDON = xbmcaddon.Addon(id=addon_id)
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
ART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))

if xbmc.getCondVisibility('system.platform.ios') or xbmc.getCondVisibility('system.platform.osx'):
	Repo = ""
	Addons = ""
	Website = ""
	Forum = ""
	Community = ""
	JarvisWiz = ""
	JarvisCheck = ""
	JarvisUpdate = ""
	KryptonWiz = ""
	KryptonCheck = ""
	KryptonUpdate = ""
	BetaWiz = ""
	BetaVIPWiz = ""
	BetaVIP = ""
	BetaKeys = ""
	SpeedTest = ""
	AdvancedSettings = "http://projectxwizard.net16.net/jogos/jogosEmuladores.xml"
	JarvisOne = ""
	JarvisTwo = ""
	KryptonOne = ""
	KryptonTwo = ""
	BASEURL = "http://www.tvsupertuga.com"
else:
	Repo = ""
	Addons = ""
	Website = ""
	Forum = ""
	Community = ""
	JarvisWiz = ""
	JarvisCheck = ""
	JarvisUpdate = ""
	KryptonWiz = ""
	KryptonCheck = ""
	KryptonUpdate = ""
	BetaWiz = ""
	BetaVIPWiz = ""
	BetaVIP = ""
	BetaKeys = ""
	SpeedTest = ""
	AdvancedSettings = "http://projectxwizard.net16.net/jogos/jogosEmuladores.xml"
	JarvisOne = ""
	JarvisTwo = ""
	KryptonOne = ""
	KryptonTwo = ""
	BASEURL = "http://www.tvsupertuga.com"

SpeedTestStatusMain = "[COLOR lime][B]ONLINE [/B][/COLOR]"
CommunityStatusMain = "[COLOR lime][B]ONLINE [/B][/COLOR]"
AdvancedSettingsMain = ""
JarvisWizStatusMain = "[COLOR lime][B]ONLINE [/B][/COLOR]"
KryptonWizStatusMain = "[COLOR lime][B]ONLINE [/B][/COLOR]"
JarvisUpdateStatusMain = "[COLOR lime][B]ONLINE [/B][/COLOR]"
KryptonUpdateStatusMain = "[COLOR lime][B]ONLINE [/B][/COLOR]"
RepoStatus = "[COLOR lime][B] . [/B][/COLOR]"
AddonsStatus = "[COLOR lime][B] . [/B][/COLOR]"
JarvisWizStatus = "[COLOR lime][B] . [/B][/COLOR]"
JarvisCheckStatus = "[COLOR lime][B] . [/B][/COLOR]"
JarvisUpdateStatus = "[COLOR lime][B] . [/B][/COLOR]"
KryptonWizStatus = "[COLOR lime][B] . [/B][/COLOR]"
KryptonCheckStatus = "[COLOR lime][B] . [/B][/COLOR]"
KryptonUpdateStatus = "[COLOR lime][B] . [/B][/COLOR]"
WebsiteStatus = "[COLOR lime][B] . [/B][/COLOR]"
ForumStatus = "[COLOR lime][B] . [/B][/COLOR]"
CommunityStatus = "[COLOR lime][B] . [/B][/COLOR]"
SpeedTestStatus = "[COLOR lime][B] . [/B][/COLOR]"
check = plugintools.get_setting("checkupdates")
auto = plugintools.get_setting("autoupdates")


try:
	response = urllib2.urlopen(JarvisWiz)
except:
	JarvisWizStatus = "[COLOR red][B] . [/B][/COLOR]"
	JarvisWizStatusMain = "[COLOR red][B]OFFLINE [/B][/COLOR]"
	
try:
	response = urllib2.urlopen(JarvisUpdate)
except:
	JarvisUpdateStatus = "[COLOR red][B] . [/B][/COLOR]"
	JarvisUpdateStatusMain = "[COLOR red][B]OFFLINE[/B][/COLOR]"

try:
	response = urllib2.urlopen(KryptonWiz)
except:
	KryptonWizStatus = "[COLOR red][B] . [/B][/COLOR]"
	KryptonWizStatusMain = "[COLOR red][B]OFFLINE[/B][/COLOR]"

try:
	response = urllib2.urlopen(KryptonUpdate)
except:
	KryptonUpdateStatus = "[COLOR red][B] . [/B][/COLOR]"
	KryptonUpdateStatusMain = "[COLOR red][B]OFFLINE[/B][/COLOR]"

try:
	response = urllib2.urlopen(Community)
except:
	CommunityStatus = "[COLOR red][B] . [/B][/COLOR]"
	CommunityStatusMain = "[COLOR red][B]OFFLINE [/B][/COLOR]"
	
try:
	response = urllib2.urlopen(SpeedTest)
except:
	SpeedTestStatus = "[COLOR red][B] . [/B][/COLOR]"
	SpeedTestStatusMain = "[COLOR red][B]OFFLINE [/B][/COLOR]"
	
try:
	response = urllib2.urlopen(AdvancedSettings)
except:
	AdvancedSettingsMain = "[COLOR red][B]OFFLINE[/B][/COLOR]"

xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
version=float(xbmc_version[:4])

if version >= 11.0 and version <= 11.9:
		codename = 'Eden'
if version >= 12.0 and version <= 12.9:
	codename = 'Frodo'
if version >= 13.0 and version <= 13.9:
	codename = 'Gotham'
if version >= 14.0 and version <= 14.9:
	codename = 'Helix'
if version >= 15.0 and version <= 15.9:
	codename = 'Isengard'
if version >= 16.0 and version <= 16.9:
	codename = 'Jarvis'
if version >= 17.0 and version <= 17.9:
	codename = 'Krypton'
	
params=parameters.get_params()

#######################################################################
#						ROOT MENU
#######################################################################

def INDEX():

  #if plugintools.get_setting("username")=="":
  #       settings(params)
		 
  #login_request =  login(LoginServer  , plugintools.get_setting("username") , plugintools.get_setting("password") )

  #if login_request!="ACCESS GRANTED":	

	Common.addDir('[COLOR cyan]INSTALADOR DE JOGOS[/COLOR]  ' + AdvancedSettingsMain,BASEURL,30,ICON,FANART,'')

  #else:
  #  plugintools.message(AddonTitle,"Invalid Login: Check Details Or Register On Our Forum","[COLOR yellow]http://www.tdbwizard.co.uk[/COLOR]")

def ACCOUNT():

  f = urllib.urlopen("http://www.canyouseeme.org/")
  html_doc = f.read()
  f.close()
  m = re.search('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',html_doc)
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
  user = plugintools.get_setting("username")

  key = base64.b64encode(plugintools.get_setting("beta"))
	
  if key=="d2F0ZXJtZWxsb24=":
    beta = "[COLOR lime]Yes[/COLOR]"
  else:
    beta = "[COLOR red]No[/COLOR]"
	
  if check=="true":
    a = "[COLOR lime]Yes[/COLOR]"
  else:
    a = "[COLOR red]No[/COLOR]"
	
  if auto=="true":
    b = "[COLOR lime]Yes[/COLOR]"
  else:
    b = "[COLOR red]No[/COLOR]"

  Common.addItem('[COLOR cyan]Version: [/COLOR][COLOR lime]%s' % version + " " + codename + "[/COLOR]",BASEURL,200,ICON,FANART,'')
  Common.addItem('[COLOR cyan]BETA Tester: [/COLOR]' + beta,BASEURL,200,ICON,FANART,'')
  Common.addItem('[COLOR cyan]Check For Updates: [/COLOR]' + a,BASEURL,200,ICON,FANART,'')
  Common.addItem('[COLOR cyan]Auto Updates: [/COLOR]' + b,BASEURL,200,ICON,FANART,'')
  Common.addItem('[COLOR cyan]Local IP: [/COLOR][COLOR yellow]' + s.getsockname()[0] + '[/COLOR]',BASEURL,200,ICON,FANART,'')
  Common.addItem('[COLOR cyan]External IP: [/COLOR][COLOR yellow]' + m.group(0) + '[/COLOR]',BASEURL,200,ICON,FANART,'')

# Settings dialog
def settings(params):
    plugintools.open_settings_dialog()
	
	
def login(server,username,password):
    # Service call
    service_url = server
    service_parameters = urllib.urlencode({'username':username,'password':password})
    body , response_headers = plugintools.read_body_and_headers( service_url , post=service_parameters )
    return body

#######################################################################
#						JARVIS OR KRYPTON SELECT
#######################################################################

def BUILDMENU():
 
	Jarvis = 0
	Krypton = 0
	Beta = 0
	updownj = "[B][COLOR lime]ONLINE[/B][/COLOR]"
	updownk = "[B][COLOR lime]ONLINE[/B][/COLOR]"
	updownb = "[B][COLOR lime]ONLINE[/B][/COLOR]"
	dialog = xbmcgui.Dialog()
	
	try:
	    response = urllib2.urlopen(JarvisWiz)
	except:
	    Jarvis = 1

	try:
	    response = urllib2.urlopen(KryptonWiz)
	except:
	    Krypton = 1
		
	try:
	    response = urllib2.urlopen(BetaWiz)
	except:
	    Beta = 1

	if Jarvis == 1:
		updownj = "[B][COLOR red]OFFLINE[/B][/COLOR]"
	
	if Krypton == 1:
		updownk = "[B][COLOR red]OFFLINE[/B][/COLOR]"

	if Beta == 1:
		updownb = "[B][COLOR red]OFFLINE[/B][/COLOR]"

	Common.addDir(updownj + ' - [COLOR cyan]JARVIS BUILDS[/COLOR]',BASEURL,19,ART+'SKYLEX XXL.png',ART+'SKYLEX XXL.png','')
	Common.addDir(updownk + ' - [COLOR cyan]KRYPTON BUILDS[/COLOR]',BASEURL,20,ART+'SONAR.png',ART+'SONAR.png','')
	Common.addDir(updownb + ' - [COLOR cyan]BETA BUILDS[/COLOR]',BASEURL,21,ART+'EMBER.png',ART+'EMBER.png','')
	Common.addItem('[COLOR powderblue]Which should I choose?[/COLOR]',BASEURL,44,ICON,FANART,'')

#######################################################################
#						JARVIS BUILDS MENU
#######################################################################

def BUILDMENU_JARVIS():
    
    accept = 0
    Jarvis = 0
    dialog = xbmcgui.Dialog()
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")

    if version >= 16.0 and version <= 16.9:
		accept = 1

    try:
        response = urllib2.urlopen(JarvisWiz)
    except:
        Jarvis = 1

    if accept == 1:	
        if Jarvis == 0:
	    	link = Common.OPEN_URL(JarvisWiz).replace('\n','').replace('\r','')
	    	match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
	    	for name,url,iconimage,fanart,description in match:
			Common.addDir(name,url,90,ART+name+'.png',ART+name+'.png',description)
        else:
	    	dialog.ok(AddonTitle,'Sorry we are unable to get the Jarvis Build list at this time.','The Jarvis host appears to be down.','[I][COLOR lightsteelblue]Plese try again later.[/COLOR][/I]')
    else:
    	dialog.ok(AddonTitle, "Sorry we are unable to process your request","[COLOR red][I][B]Error: You are not running Kodi Jarvis[/COLOR][/I][/B]","[I]Your are running: [COLOR lightsteelblue][B]Kodi " + codename + " Version:[COLOR cyan] %s" % version + "[/COLOR][/I][/B][/COLOR]")

#######################################################################
#						KRYPTON BUILDS MENU
#######################################################################

def BUILDMENU_KRYPTON():
    
    accept = 0
    Krypton = 0
    dialog = xbmcgui.Dialog()
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])

    if version >= 17.0 and version <= 17.9:
		accept = 1

    Krypton = 0
    dialog = xbmcgui.Dialog()

    try:
	    response = urllib2.urlopen(KryptonWiz)
    except:
	    Krypton = 1

    if accept == 1:	
		if Krypton == 0:
			link = Common.OPEN_URL(KryptonWiz).replace('\n','').replace('\r','')
			match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
			for name,url,iconimage,fanart,description in match:
				Common.addDir(name,url,90,ART+name+'.png',ART+name+'.png',description)
		else:
			dialog.ok(AddonTitle,'Sorry we are unable to get the Krypton Build list at this time.','The Krypton host appears to be down.','[I][COLOR lightsteelblue]Plese try again later.[/COLOR][/I]')
    else:
    	dialog.ok(AddonTitle, "Sorry we are unable to process your request","[COLOR red][I][B]Error: You are not running Kodi Krypton[/COLOR][/I][/B]","[I]Your are running: [COLOR lightsteelblue][B]Kodi " + codename + " Version:[COLOR cyan] %s" % version + "[/COLOR][/I][/B][/COLOR]")

#######################################################################
#						ADVANCED SETTINGS
#######################################################################

def BUILDMENU_BETA():
 
	key = base64.b64encode(plugintools.get_setting("beta"))

	link = Common.OPEN_URL(BetaKeys).replace('\n','').replace('\r','')
	match = re.compile('passkey="(.+?)"').findall(link)
	for passkey in match:
		if key==passkey:
			link = Common.OPEN_URL(BetaWiz).replace('\n','').replace('\r','')
			match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
			for name,url,iconimage,fanart,description in match:
				Common.addDir(name,url,90,ART+name+'.png',ART+name+'.png',description)
		else:
			link = Common.OPEN_URL(BetaVIP).replace('\n','').replace('\r','')
			match = re.compile('passkey="(.+?)"').findall(link)
			for passkey in match:
				if key==passkey:
					link = Common.OPEN_URL(BetaVIPWiz).replace('\n','').replace('\r','')
					match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
					for name,url,iconimage,fanart,description in match:
						Common.addDir(name,url,90,ART+name+'.png',ART+name+'.png',description)
				else:	
					plugintools.message(AddonTitle,"Invalid Key: Check Details","[COLOR yellow]https://www.facebook.com/groups/1735809796639007/")  
 
def ADVANCEDSETTINGS():
    
    link = Common.OPEN_URL(AdvancedSettings).replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        Common.addDir('[COLOR cyan]' + name + '[/COLOR]',url,90,ICON,FANART,description)

#######################################################################
#						MAINTENANCE MENU
#######################################################################
	
def maintMenu():

	Common.addDir('[COLOR cyan]Auto Clean Device[/COLOR]','url',31,os.path.join(ART, "icon.png"),ART+'maintwall.jpg','')
	Common.addItem('[COLOR cyan]Clear Cache[/COLOR]','url',1,os.path.join(ART, "icon.png"),ART+'maintwall.jpg','')
	Common.addItem('[COLOR cyan]Delete Thumbnails[/COLOR]','url',2,os.path.join(ART, "icon.png"),ART+'maintwall.jpg','')
	Common.addItem('[COLOR cyan]Purge Packages[/COLOR]','url',3,os.path.join(ART, "icon.png"),ART+'maintwall.jpg','')
	Common.addItem('[COLOR cyan]Convert Physical Paths To Special[/COLOR]','url',13,os.path.join(ART, "icon.png"),ART+'maintwall.jpg','')
	Common.addDir('[COLOR cyan]SYSTEM RESET [/COLOR][COLOR red](CAUTION)[/COLOR]','url',6,ICON,FANART,'')

#######################################################################
#						SPEEDTEST LIST
#######################################################################

def SPEEDTEST():
    
    link = Common.OPEN_URL(SpeedTest).replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        Common.addItem('[COLOR cyan]' + name + " | " + description + '[/COLOR]',url,15,ICON,ART+'speedfanart.jpg','')
		
#######################################################################
#						BACKUP MENU MENU
#######################################################################
	
def BACKUPMENU():

    Common.addItem('[COLOR cyan]Backup[/COLOR]','url',70,ICON,FANART,'')
    Common.addDir('[COLOR cyan]Restore[/COLOR]','url',71,ICON,FANART,'')
    Common.addDir('[COLOR cyan]Delete A Backup[/COLOR]','url',72,ICON,FANART,'')
    Common.addItem('[COLOR cyan]Delete All Backups[/COLOR]','url',73,ICON,FANART,'')
    Common.addItem('[COLOR cyan]Select Backup Location[/COLOR]','url',9,ICON,FANART,'')

#######################################################################
#                       Compatibility
#######################################################################
def NotCompatible():
    
    dialog = xbmcgui.Dialog()
    dialog.ok(AddonTitle, "[B][COLOR powderblue]Important Notice: [/COLOR][/B]",'[COLOR cyan]Project X Builds are not compatabile with any Kodi versions before 16 Jarvis.','Project X Builds will NOT work with Frodo, Gotham and Isengard versions of Kodi.[/COLOR]')

############################
###SET VIEW#################
############################

def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )

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

if mode==None or url==None or len(url)<1:
        INDEX()
		
elif mode==1:
		maintenance.clearCache()
        
elif mode==2:
		maintenance.deleteThumbnails()

elif mode==3:
		maintenance.purgePackages()

elif mode==4:
		ACCOUNT()
		
elif mode==5:
        maintMenu()

elif mode==6:        
		wipe.FRESHSTART()

elif mode==8:
        BACKUPMENU()
		
elif mode==9:
        settings(params)

elif mode==11:
        update.updatecheck()
		
elif mode==12:
        xbmc.executebuiltin("RunAddon(plugin.program.jogosEmuladores)")
		
elif mode==13:
        maintenance.Fix_Special(url)

elif mode==14:
        versioncheck.XBMC_Version()
		
elif mode==15:
        speedtest.runtest(url)
		
elif mode==16:
        SPEEDTEST()

elif mode==17:
       community.CommunityBuilds()

elif mode==18:
       community.CommunityUpdateNotice()

elif mode==19:
        BUILDMENU_JARVIS()

elif mode==20:
        BUILDMENU_KRYPTON()
		
elif mode==21:
        BUILDMENU_BETA()
		
elif mode==30:
		ADVANCEDSETTINGS()
		
elif mode==31:
		maintenance.autocleanask()

elif mode==44:
        versioncheck.BUILD_Version()

elif mode==45:
        NotCompatible()

elif mode==70:
        backuprestore.Backup()
		
elif mode==71:
        backuprestore.Restore()
	
elif mode==72:
        backuprestore.ListBackDel()
		
elif mode==73:
        backuprestore.DeleteAllBackups()
		
elif mode==85:
        print "############   ATTEMPT TO KILL XBMC/KODI   #################"
        Common.killxbmc()

elif mode==87:
       community.COMMUNITY()
		
elif mode==88:
        BUILDMENU()
	
elif mode==90:
        installer.INSTALL(name,url,description)
		
elif mode==92:
        ServerStatus.Check()
		
elif mode==93:
       community.SHOWCOMMUNITYBUILDS(url)
	   
elif mode==99:
		installer.INSTALLCOM(name,url,description)

xbmcplugin.endOfDirectory(int(sys.argv[1]))