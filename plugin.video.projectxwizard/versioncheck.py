import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs

AddonTitle="[COLOR ghostwhite]Project X[/COLOR] [COLOR lightsteelblue]Wizard[/COLOR]"
dialog=xbmcgui.Dialog()

#---------------------------------------------------------------------------------------------------
#Report back with the version of Kodi installed
def XBMC_Version():
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
	
    if version >= 16:
		dialog=xbmcgui.Dialog()
		dialog.ok(AddonTitle, "[COLOR green][B]CONGRATULATIONS![/B][/COLOR]","Your version is: Kodi %s" % version + " " + codename, "You can install a Project X Build on this system!")
    else:
		dialog=xbmcgui.Dialog()
		dialog.ok(AddonTitle, "[COLOR red][B]SORRY![/B][/COLOR]","Your version is: Kodi %s" % version, "You cannot install a Project X Build on this system!")

#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#Report back with the version of Kodi installed
def BUILD_Version():
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])

    if version >= 11.0 and version <= 11.9:
		codename = 'Eden'
		dialog.ok(AddonTitle, "[COLOR yellow][B]Which should I choose? - Jarvis or Krypton?![/B][/COLOR]","Your system is running : Kodi Version %s" % version + " " + codename, "Sorry no builds can be inatalled on this system! Please update your Kodi installation to 16 Jarvis or 17 Krypton to use a Project X Build.")
    if version >= 12.0 and version <= 12.9:
		codename = 'Frodo'
		dialog.ok(AddonTitle, "[COLOR yellow][B]Which should I choose? - Jarvis or Krypton?![/B][/COLOR]","Your system is running : Kodi Version %s" % version + " " + codename, "Sorry no builds can be inatalled on this system! Please update your Kodi installation to 16 Jarvis or 17 Krypton to use a Project X Build.")
    if version >= 13.0 and version <= 13.9:
		codename = 'Gotham'
		dialog.ok(AddonTitle, "[COLOR yellow][B]Which should I choose? - Jarvis or Krypton?![/B][/COLOR]","Your system is running : Kodi Version %s" % version + " " + codename, "Sorry no builds can be inatalled on this system! Please update your Kodi installation to 16 Jarvis or 17 Krypton to use a Project X Build.")
    if version >= 14.0 and version <= 14.9:
		codename = 'Helix'
		dialog.ok(AddonTitle, "[COLOR yellow][B]Which should I choose? - Jarvis or Krypton?![/B][/COLOR]","Your system is running : Kodi Version %s" % version + " " + codename, "Sorry no builds can be inatalled on this system! Please update your Kodi installation to 16 Jarvis or 17 Krypton to use a Project X Build.")
    if version >= 15.0 and version <= 15.9:
		codename = 'Isengard'
		dialog.ok(AddonTitle, "[COLOR yellow][B]Which should I choose? - Jarvis or Krypton?![/B][/COLOR]","Your system is running : Kodi Version %s" % version + " " + codename, "Sorry no builds can be inatalled on this system! Please update your Kodi installation to 16 Jarvis or 17 Krypton to use a Project X Build.")
    if version >= 16.0 and version <= 16.9:
		codename = 'Jarvis'
		dialog.ok(AddonTitle, "[COLOR yellow]Which should I choose? [/COLOR][COLOR white]- Jarvis or Krypton?[/COLOR]","Your system is running : Kodi Version %s" % version + " " + codename, "You should install a [B][COLOR lime]Jarvis[/B][/COLOR] build on this system!")
    if version >= 17.0 and version <= 17.9:
		codename = 'Krypton'
		dialog.ok(AddonTitle, "[COLOR yellow]Which should I choose? - Jarvis or Krypton?[/COLOR]","Your system is running : Kodi Version %s" % version + " " + codename, "You should install a [B][COLOR lime]Krypton[/B][/COLOR] build on this system!")

#---------------------------------------------------------------------------------------------------