import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys
import urllib2,urllib
import extract
import downloader
import re
import common as Common
import installer

#Community Builds
Community_List = ""
AddonData = xbmc.translatePath('special://userdata/addon_data')
addon_id = 'plugin.program.jogosEmuladores'
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
ADDON = xbmcaddon.Addon(id=addon_id)
AddonTitle="[COLOR ghostwhite]Project X[/COLOR] [COLOR lightsteelblue]Wizard[/COLOR]"
MaintTitle="[COLOR ghostwhite]Project X[/COLOR] [COLOR lightsteelblue]Maintenance Tools[/COLOR]"
BASEURL = "www.projectxwizard.com"

#######################################################################
#						Community Builds
#######################################################################

def COMMUNITY():

	link = Common.OPEN_URL(Community_List).replace('\n','').replace('\r','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)"').findall(link)
	for name,url,iconimage,fanart in match:
		Common.addDir("[COLOR cyan]" + name + " [/COLOR]",url,93,iconimage,fanart,'')
	
	Common.addItem('[COLOR white]HOW TO ADD YOUR BUILDS TO THE LIST![/COLOR]',BASEURL,17,ICON,FANART,'')

def SHOWCOMMUNITYBUILDS(url):
	
	link = Common.OPEN_URL(url).replace('\n','').replace('\r','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)"').findall(link)
	for name,url,iconimage,fanart in match:
		Common.addDir(name,url,99,iconimage,fanart," ")


#######################################################################
#                       Community
#######################################################################
def CommunityBuilds():
    
    dialog = xbmcgui.Dialog()
    dialog.ok(AddonTitle, "[COLOR white]If you would like your build to be hosted by[/COLOR]", "[COLOR ghostwhite]PROJECT X[/COLOR] [COLOR lightsteelblue]WIZARD[/COLOR]  [COLOR white]please visit:[/COLOR]", "[COLOR yellow]http://tvsupertuga.forum-gratuito.com [/COLOR]")

############################
###GET PARAMS###############
############################

url=None
name=None
mode=None
iconimage=None
fanart=None
description=None


#######################################################################
#						Which mode to select
#######################################################################

if mode==17:
        CommunityBuilds()

elif mode==18:
        CommunityUpdateNotice()
		
elif mode==85:
        print "############   ATTEMPT TO KILL XBMC/KODI   #################"
        Common.killxbmc()

elif mode==87:
        COMMUNITY()
		
elif mode==99:
        installer.INSTALLCOM(name,url,description)

elif mode==93:
        SHOWCOMMUNITYBUILDS(url)
