# -*- coding: utf-8 -*-

import xbmcaddon,os,xbmc,xbmcgui,urllib,urllib2,re,xbmcplugin,sys
import traceback
import logging,shutil
import HTMLParser,time
from shutil import copyfile

_plugin_name_='plugin.program.tvsupertugamanutencao'
__debuging__="DEBUG_MODE"
__USERAGENT__ = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
__settings__ = xbmcaddon.Addon(id=_plugin_name_)
addonName = __settings__.getAddonInfo("name")
addonIcon = __settings__.getAddonInfo('icon')
__language__ = __settings__.getLocalizedString
#__cachePeriod__ = __settings__.getSetting("cache")
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')
__DEBUG__ = __settings__.getSetting("DEBUG") == "true"
__addon__ = xbmcaddon.Addon()
ADDON=xbmcaddon.Addon(id=_plugin_name_)
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
sys.modules["__main__"].dbg = True
__USERAGENT__ = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
#cacheServer = StorageServer.StorageServer("plugin.video.Ebs_RSS", __cachePeriod__)  # (Your plugin name, Cache time in hours)
AddonID = _plugin_name_
Addon = xbmcaddon.Addon(AddonID)
localizedString = Addon.getLocalizedString 
user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
LIB_PATH = xbmc.translatePath( os.path.join( __PLUGIN_PATH__, 'resources', 'mail' ) )
sys.path.append (LIB_PATH)
import mail_file
if not os.path.exists(user_dataDir):
     os.makedirs(user_dataDir)

if not os.path.exists(user_dataDir): # check if folder doesnt exist 
     os.makedirs(user_dataDir) # create if it doesnt
download_list = user_dataDir + 'download_list.txt' # define watched as the path to txt file to store data 


def get_params():
        param=[]
        if len(sys.argv)>=2:
          paramstring=sys.argv[2]
          if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param     
		
#################################################################################################################

#                               NEED BELOW CHANGED



def addDir(contentType, name, url, mode, iconimage='DefaultFolder.png', elementId='', summary='', fanart='',isRealFolder=True):
        try:
           
            u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + name + "&module=" + urllib.quote_plus(elementId)
            liz = xbmcgui.ListItem(clean(contentType, name), iconImage=iconimage, thumbnailImage=iconimage)
            liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote(clean(contentType, name)), "Plot": urllib.unquote(summary)})
            if not fanart == '':
                liz.setProperty("Fanart_Image", fanart)
               
            ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isRealFolder)
            if __DEBUG__:
                 
                print "added directory success:" + clean(contentType, name) + " url=" + clean('utf-8',u)
            return ok
        except Exception as e:
            print "WALLA exception in addDir"
            print e
            raise
     
def addDir2_2(name,url,mode,iconimage,fanart,description):

        uinstall_package=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        

        
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        
       # xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
        
   
        return ok
###############################################################################################################        

def addDir3(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        
        return ok

def addDir2(name,url,mode,iconimage,fanart,description):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Audio", infoLabels={ "Title": name } )
    if not fanart == '':
                liz.setProperty("Fanart_Image", fanart)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok

def main_menu():
     
     addDir3("[COLOR blue]Install addon list[/COLOR]",'plugin.',6,__PLUGIN_PATH__ + "\\resources\\install.png",__PLUGIN_PATH__ + "\\resources\\install.png","Install addon list")
     addDir3("[COLOR darkgoldenrod]Remove addons[/COLOR]",'plugin.',25,__PLUGIN_PATH__ + "\\resources\\remove.png",__PLUGIN_PATH__ + "\\resources\\remove.png","Remove addons")
     addDir3("[COLOR darkgoldenrod]Remove all addons[/COLOR]",'plugin.',5,__PLUGIN_PATH__ + "\\resources\\remove2.jpg",__PLUGIN_PATH__ + "\\resources\\remove2.jpg","Remove all addons")
     addDir3("[COLOR skyblue]Remove Repo[/COLOR]",'repository.',25,__PLUGIN_PATH__ + "\\resources\\remove3.png",__PLUGIN_PATH__ + "\\resources\\remove3.png","Remove Repo")
     addDir3("[COLOR skyblue]Remove all Repos[/COLOR]",'repository.',5,__PLUGIN_PATH__ + "\\resources\\remove4.png",__PLUGIN_PATH__ + "\\resources\\remove4.png","Remove all Repos")
     
     addDir3("[COLOR slateblue]Maintenance[/COLOR]","www.nothing.com",4,__PLUGIN_PATH__ + "\\resources\\Maintenance.jpg",__PLUGIN_PATH__ + "\\resources\\Maintenance.jpg","Maintenance")
     addDir2('[COLOR teal]View Kodi Log[/COLOR]','url',31,__PLUGIN_PATH__ + "\\resources\\log.jpg",__PLUGIN_PATH__ + "\\resources\\log.jpg",'View Kodi Log')
     addDir2('[COLOR teal]Mail Me Kodi Log[/COLOR]','ME',32,__PLUGIN_PATH__ + "\\resources\\mail-image.jpg",__PLUGIN_PATH__ + "\\resources\\mail-image.jpg",'Mail Kodi Log')
     addDir2('[COLOR teal]Mail Someone Kodi Log[/COLOR]','someone',32,__PLUGIN_PATH__ + "\\resources\\Mail_image2.jpg",__PLUGIN_PATH__ + "\\resources\\Mail_image2.jpg",'Mail Kodi Log')
def clear_caches():
        addDir2('Clear temp movie files','url',65,__PLUGIN_PATH__ + "\\resources\\temp.jpg",__PLUGIN_PATH__ + "\\resources\\temp.jpg",'Clear temp movie files')
        addDir2('Clear cache','url',3,__PLUGIN_PATH__ + "\\resources\\temp2.png",__PLUGIN_PATH__ + "\\resources\\temp2.png",'Clear cache')
        addDir2('Clear old backups','url',2,__PLUGIN_PATH__ + "\\resources\\temp3.jpg",__PLUGIN_PATH__ + "\\resources\\temp3.jpg",'Clear old backups')
        addDir2('Clear Log','url',1,__PLUGIN_PATH__ + "\\resources\\temp4.jpg",__PLUGIN_PATH__ + "\\resources\\temp4.jpg",'Clear Log')

############################################################        LYB          ###############################################################    
    
def loglocation(): 
    versionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
    if versionNumber < 12:
        if xbmc.getCondVisibility('system.platform.osx'):
            if xbmc.getCondVisibility('system.platform.atv2'):
                log_path = '/var/mobile/Library/Preferences'
            else:
                log_path = os.path.join(os.path.expanduser('~'), 'Library/Logs')
        elif xbmc.getCondVisibility('system.platform.ios'):
            log_path = '/var/mobile/Library/Preferences'
        elif xbmc.getCondVisibility('system.platform.windows'):
            log_path = xbmc.translatePath('special://home')
            log = os.path.join(log_path, 'xbmc.log')
        elif xbmc.getCondVisibility('system.platform.linux'):
            log_path = xbmc.translatePath('special://home/temp')
        else:
            log_path = xbmc.translatePath('special://logpath')
    elif versionNumber > 11:
        log_path = xbmc.translatePath('special://logpath')
        log = os.path.join(log_path, 'xbmc.log')
    return log_path
	
def cleandb():
    dialog = xbmcgui.Dialog()
    image_select=['video','music']
    library= image_select[xbmcgui.Dialog().select('Which Version ?', image_select)]
    xbmc.executebuiltin( 'CleanLibrary(%s)'%library ) 
    dialog = xbmcgui.Dialog()
    dialog.ok("Kodi  Maintenance", '','ALL DONE !! :)', "[COLOR yellow]Brought To You By Kodi  Maintenance[/COLOR]")
            
    ############################################################        STANDARD CACHE          ###############################################################  
  
def deletecachefiles(url):
    print '############################################################       DELETING STANDARD CACHE             ###############################################################'
    xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'), 'cache')
    if os.path.exists(xbmc_cache_path)==True:    
        for root, dirs, files in os.walk(xbmc_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete XBMC Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'), 'temp')
    if os.path.exists(xbmc_cache_path)==True:    
        for root, dirs, files in os.walk(xbmc_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete XBMC Temp Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass            
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'Other'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'LocalAndRental'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
              # Set path to Cydia Archives cache files
                             

    # Set path to What th Furk cache files
    wtf_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/cache'), '')
    if os.path.exists(wtf_cache_path)==True:    
        for root, dirs, files in os.walk(wtf_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete WTF Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                # Set path to 4oD cache files
    channel4_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.4od/cache'), '')
    if os.path.exists(channel4_cache_path)==True:    
        for root, dirs, files in os.walk(channel4_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete 4oD Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                # Set path to BBC iPlayer cache files
    iplayer_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache'), '')
    if os.path.exists(iplayer_cache_path)==True:    
        for root, dirs, files in os.walk(iplayer_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete BBC iPlayer Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                
                # Set path to Simple Downloader cache files
    downloader_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/script.module.simple.downloader'), '')
    if os.path.exists(downloader_cache_path)==True:    
        for root, dirs, files in os.walk(downloader_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Simple Downloader Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                # Set path to ITV cache files
    itv_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.itv/Images'), '')
    if os.path.exists(itv_cache_path)==True:    
        for root, dirs, files in os.walk(itv_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ITV Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
    dialog = xbmcgui.Dialog()
    dialog.ok("Kodi  Maintenance", "       Thats It All Done Please Come Visit Again", "          [COLOR yellow]Brought To You By Kodi  Maintenance[/COLOR]")
############################################################        DELETING CRASH LOGS          ###############################################################    
        
def DeleteCrashLogs(url):  
    print '############################################################       DELETING CRASH LOGS             ###############################################################'
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Delete Old Crash Logs", '', "Do you want to delete them?"):
        path=loglocation()
        import glob
        for infile in glob.glob(os.path.join(path, 'xbmc_crashlog*.*')):
             File=infile
             print infile
             os.remove(infile)
    dialog = xbmcgui.Dialog()
    dialog.ok("Kodi  Maintenance", "Please Reboot XBMC To Take Effect !!", "[COLOR yellow]Brought To You By Kodi  Maintenance[/COLOR]")
            
            
   
############################################################        PACKAGES          ###############################################################    
          
def DeletePackages(url):
    print '############################################################       DELETING PACKAGES             ###############################################################'
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))

    try:    
        for root, dirs, files in os.walk(packages_cache_path):
            file_count = 0
            file_count += len(files)
            
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Package Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                            
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                    dialog = xbmcgui.Dialog()
                    dialog.ok("Kodi  Maintenance", "       Thats It All Done Please Come Visit Again", "          [COLOR yellow]Brought To You By Kodi  Maintenance[/COLOR]")
    except: 
        logging.warning("ERROR")
        dialog = xbmcgui.Dialog()
        dialog.ok("Kodi  Maintenance", "Bloody Packages Wont Delete Can Some Developer", "Sort It!!    [COLOR yellow]Brought To You By Kodi  Maintenance[/COLOR]")
        
    ############################################################       REMOVE ADDON             ###############################################################'
def findaddon(url,name):  
    print '############################################################       REMOVE ADDON             ###############################################################'
    pluginpath = xbmc.translatePath(os.path.join('special://home/addons',''))
    import glob
    for file in glob.glob(os.path.join(pluginpath, url+'*')):
        name=str(file).replace(pluginpath,'').replace('plugin.','').replace('audio.','').replace('video.','').replace('skin.','').replace('repository.','')
        iconimage=(os.path.join(file,'icon.png'))
        fanart=(os.path.join(file,'fanart.jpg'))
        addDir2(name,file,26,iconimage,fanart,'')
        setView('movies', 'SUB') 

     
def removeanything(url):   
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Remove", '', "Do you want to Remove"):
        for root, dirs, files in os.walk(url):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        os.rmdir(url)
        xbmc.executebuiltin('Container.Refresh')        
def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )

def findaddon_all(url,name):  
    print '############################################################       REMOVE ADDON             ###############################################################'

    pluginpath = xbmc.translatePath(os.path.join('special://home/addons',''))
    import glob
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Remove ALL ???", '', "Do you want to Remove???"):
     dp = xbmcgui.DialogProgress()
     dp.create("Removing Addons", "Please Wait", '', "")
     dp.update(0)
     for file in glob.glob(os.path.join(pluginpath, url+'*')):
        
        file_name=file[file.rfind('\\')+1:]

        
        if file_name != 'plugin.program.tvsupertugamanutencao':
         
          dp.update(0, "Please Wait...", file_name+'-Removing', '')
          if dp.iscanceled(): 
              dp.close()
              break
          removeanything_all(file)

          
        setView('movies', 'SUB') 
    xbmc.executebuiltin('Container.Refresh')
    sys.exit()
def removeanything_all(url): 
        
        for root, dirs, files in os.walk(url):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        if os.path.isdir(url):
          os.rmdir(url)
        else:
          os.remove(url)
          
        
def remove_all_addons(url,name):
    findaddon_all(url,name)

def multi_addons_menu():
      pluginpath = xbmc.translatePath(os.path.join('special://home/addons','plugin.program.tvsupertugamanutencao'))
   
      addDir3('Demo List',pluginpath+'\Startup_list.txt',8,"https://cdn0.iconfinder.com/data/icons/presentation-training-seminar/400/Popular-17-512.png","http://www.gamepur.com/files/images/2014/FH2-KeyArt-Horizontal-v2-CMYK-jpg.jpg","Addon List")
      if os.path.exists(download_list):
       file = open(download_list, "r") 
       for f in file.readlines():
         
         name=''
         icon=''
         fanart=''
         read_text=read_txt_files(f)
         if read_text!='ERROR' :
           for line in read_text:
             if((line.split('=')[0])=='list name'):
               name=line.split('=')[1].rstrip('\r\n')
             if((line.split('=')[0])=='icon'):
               icon=line.split('=')[1].rstrip('\r\n')
             if((line.split('=')[0])=='fanart'):
               fanart=line.split('=')[1].rstrip('\r\n')
           if len(name)>0 and len(icon)>0 and len(fanart)>0:

             addDir3(name,f,8,icon,fanart,"Addon List")
      addDir2("Add Addons List",'plugin.',7,__PLUGIN_PATH__ + "\\resources\\add_list.png",__PLUGIN_PATH__ + "\\resources\\add_list.png","Add Addons List txt File")
      addDir2("Remove addons List",'plugin',28,__PLUGIN_PATH__ + "\\resources\\remove_list.jpg",__PLUGIN_PATH__ + "\\resources\\remove_list.jpg",'Remove addon list')
      addDir2("Help",'plugin',29,__PLUGIN_PATH__ + "\\resources\\help.jpg",__PLUGIN_PATH__ + "\\resources\\help.jpg",'Create your own list file')
def add_file_location():
      text_entered=''
      keyboard = xbmc.Keyboard(text_entered, 'Enter list file location')
      keyboard.doModal()
      if keyboard.isConfirmed():
         text_entered = (keyboard.getText())
      if len(text_entered)>3:
        print_text_file = open(download_list,"a") # sets it to append to watched.txt
        print_text_file.write(text_entered+'\n') # writes the url in a form easy to regex above 
        print_text_file.close # closes file
      xbmc.executebuiltin('Container.Refresh')
      sys.exit()
def read_txt_files(target_url):
  try:
 
   target_url=target_url.rstrip('\r\n')
   if os.path.isfile(target_url):
    
    f=open(target_url, 'r') 
   else:
    f = urllib2.urlopen(target_url)
   return f.readlines()
  except:
    print 'ERROR: defname'
    #traceback.print_exc()
    return 'ERROR'
def add_keyboard():
	new = '"locale.keyboardlayouts"'
	value='["English QWERTY|Hebrew QWERTY"]'
	query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":%s}, "id":1}' % (new)

	response = xbmc.executeJSONRPC(query)
	
	
	query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (new, value)

	xbmc.executeJSONRPC(query)

	xbmc.executebuiltin('SendClick(11)')
		
	return False
def swapUS(value):
	new = '"addons.unknownsources"'
	
	query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":%s}, "id":1}' % (new)

	response = xbmc.executeJSONRPC(query)

	if 'false' in response:
		query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (new, value)

		xbmc.executeJSONRPC(query)

		xbmc.executebuiltin('SendClick(11)')
		
	return False
def change_language(wanted_language):
          
        
        language = xbmc.getLanguage()
        
        if (wanted_language!=language):
          xbmc.executebuiltin('xbmc.SetGUILanguage('+wanted_language+')')
        add_keyboard()
		  
		  
def add_addon_list(url):
     
     addDir2("[B][COLOR coral]Install All[/COLOR][/B]",url,10,__PLUGIN_PATH__ + "\\resources\\easyinstall1.png",__PLUGIN_PATH__ + "\\resources\\easyinstall1.png","Install All Addons")
     f =read_txt_files(url)
    # mail_message()
     
     if f!='ERROR':
      for file in f:

       if 'unknownsources' in file and file[0]!="#":
      
         setting=file.split('=')[1]
         
         swapUS(setting.rstrip('\r\n'))

       if '$' in file and file[0]!="#":
        
        file_name=file.split("$")
        
        file_name[2]=file_name[2].replace('%24','$')

        if os.path.exists(xbmc.translatePath("special://home/addons/") + file_name[2].rstrip('\r\n')):
           file_name[1]='*'+file_name[1]
        else:
          file_name[1]='[COLOR red][B]'+file_name[1]+'[/B][/COLOR]'
        addDir2(file_name[1],file,9,__PLUGIN_PATH__ + "\\resources\\images.jpg",__PLUGIN_PATH__ + "\\resources\\images.jpg","Install Addon")
       if (file.split('=')[0]=='language') and file[0]!="#":
        addDir2('language='+file.split('=')[1].title().rstrip('\r\n'),file.split('=')[1].title().rstrip('\r\n'),27,__PLUGIN_PATH__ + "\\resources\\lang.jpg",__PLUGIN_PATH__ + "\\resources\\lang.jpg","Install language")
       if (file.split('=')[0]=='splash'):
         addDir2('splash',file.split('=')[1].rstrip('\r\n'),30,__PLUGIN_PATH__ + "\\resources\\splash.png",__PLUGIN_PATH__ + "\\resources\\splash.png","Install language")

     
def change_splash(name,url,message):
      
          if os.path.exists(xbmc.translatePath("special://home/addons/") + name+'png'):
                copyfile(url,xbmc.translatePath("special://home/addons/") + name+'png' ) 
          else:
                f = open(xbmc.translatePath('special://home/media/')+'splash.png','wb')
                f.write(urllib.urlopen(url).read())
                f.close()
          if message=='True':
              dialog = xbmcgui.Dialog()
              dialog.ok("Kodi Maintenance", '','Splash screen Changed', "")
def dis_or_enable_addon(addon_id, enable="true"):
    import json
    addon = '"%s"' % addon_id
    if xbmc.getCondVisibility("System.HasAddon(%s)" % addon_id) and enable == "true":
        logging.warning('already Enabled')
        return xbmc.log("### Skipped %s, reason = allready enabled" % addon_id)
    elif not xbmc.getCondVisibility("System.HasAddon(%s)" % addon_id) and enable == "false":
        return xbmc.log("### Skipped %s, reason = not installed" % addon_id)
    else:
        do_json = '{"jsonrpc":"2.0","id":1,"method":"Addons.SetAddonEnabled","params":{"addonid":%s,"enabled":%s}}' % (addon, enable)
        query = xbmc.executeJSONRPC(do_json)
        response = json.loads(query)
        if enable == "true":
            xbmc.log("### Enabled %s, response = %s" % (addon_id, response))
        else:
            xbmc.log("### Disabled %s, response = %s" % (addon_id, response))
    return xbmc.executebuiltin('Container.Update(%s)' % xbmc.getInfoLabel('Container.FolderPath'))
	
def install_package(url,with_massage):
    extension=url.split("$")

    
    if not os.path.exists(xbmc.translatePath("special://home/addons/") + extension[2].rstrip('\r\n').replace('%24','$')):


      logging.warning(extension)
      downloader_is(extension[0],extension[1],with_massage)
      
      

      dis_or_enable_addon(extension[2].rstrip('\r\n'))
      time.sleep(10)
      xbmc.executebuiltin('SendClick(yesnodialog,11)')
      if 'skin_change' in extension[1]:

  
       SkinToUse = Addon.getSetting("SkinToUse")
       time.sleep(2)
       xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
       time.sleep(2)
       xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"'+extension[2].rstrip('\r\n')+'"}}')
       xbmc.executebuiltin('SendClick(11)')
       if os.path.exists(xbmc.translatePath(os.path.join('special://home'))+'\\userdata\\addon_data\\skin.phenomenal\settings.xml'):
            file=open(xbmc.translatePath(os.path.join('special://home'))+'\\userdata\\addon_data\\skin.phenomenal\settings.xml','r')
            skin_setting=file.read()
            skin_setting=skin_setting.replace('<setting id="Disable_Splash" type="bool">false</setting>','<setting id="Disable_Splash" type="bool">true</setting>')
            file=open(xbmc.translatePath(os.path.join('special://home'))+'\\userdata\\addon_data\\skin.phenomenal\settings.xml','w')
            file.write(skin_setting)
            file.close()
    elif with_massage=='yes':
      dialog = xbmcgui.Dialog()
      choice=dialog.yesno("Kodi Maintenance", '','[B][COLOR red]Already Installed[/COLOR][/B]', "Install again Any way?")
      if    choice :
        downloader_is(extension[0],extension[1],'false')
        dis_or_enable_addon(extension[2].rstrip('\r\n'))
    
       
def OKmsg(title, line1, line2="", line3=""):
	xbmcgui.Dialog().ok(title, line1, line2, line3)
def downloader_is (url,name,with_massage ) :
 import downloader,extract   
 i1iIIII = xbmc . getInfoLabel ( "System.ProfileName" )
 I1 = xbmc . translatePath ( os . path . join ( 'special://home' , '' ) )
 O0OoOoo00o = xbmcgui . Dialog ( )
 if name.find('repo')< 0 and with_massage=='yes':
     choice = O0OoOoo00o . yesno ( "XBMC ISRAEL" , "Yes to install" ,name)
 else:
     choice=True
 if    choice :
  iiI1iIiI = xbmc . translatePath ( os . path . join ( 'special://home/addons' , 'packages' ) )
  iiiI11 = xbmcgui . DialogProgress ( )
  iiiI11 . create ( "XBMC ISRAEL" , "Downloading " +name, '' , 'Please Wait' )
  OOooO = os . path . join ( iiI1iIiI , 'isr.zip' )
  try :
     os . remove ( OOooO )
  except :
      pass
  downloader . download ( url , OOooO ,name, iiiI11 )
  II111iiii = xbmc . translatePath ( os . path . join ( 'special://home' , 'addons' ) )
  iiiI11 . update ( 0 , name , "Extracting Zip Please Wait" )

  extract . all ( OOooO , II111iiii , iiiI11 )
  iiiI11 . update ( 0 , name , "Downloading" )
  iiiI11 . update ( 0 , name , "Extracting Zip Please Wait" )
  xbmc . executebuiltin ( 'UpdateLocalAddons ' )
  xbmc . executebuiltin ( "UpdateAddonRepos" )


def install_all_package(url):
  dp=xbmcgui.Dialog()
  choice = dp . yesno ( "XBMC ISRAEL" , "Install all addons?" )
  if choice :

     f =read_txt_files(url)


     for file in f:
      if (file.split('=')[0]=='language'):
        xbmc.executebuiltin('xbmc.SetGUILanguage('+file.split('=')[1].title().rstrip('\r\n')+')')
        
      else:
       #file_name=file.split("$")
       if '$' in file and file[0]!="#":
         install_package(file,'no')
         
       if 'skin' in file[0]:

          SkinToUse = Addon.getSetting("SkinToUse")
          time.sleep(2)
          xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
          time.sleep(2)
          xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"'+extension[2].rstrip('\r\n')+'"}}')
          xbmc.executebuiltin('SendClick(11)')
          if os.path.exists(xbmc.translatePath(os.path.join('special://home'))+'\\userdata\\addon_data\\skin.phenomenal\settings.xml'):
            file.open(xbmc.translatePath(os.path.join('special://home'))+'\\userdata\\addon_data\\skin.phenomenal\settings.xml','r')
            skin_setting=file.read()
            skin_setting=skin_setting.replace('<setting id="Disable_Splash" type="bool">false</setting>','<setting id="Disable_Splash" type="bool">true</setting>')
            file.open(xbmc.translatePath(os.path.join('special://home'))+'\\userdata\\addon_data\\skin.phenomenal\settings.xml','w')
            file.write(skin_setting)
            file.close()
       if (file.split('=')[0]=='splash'):
          change_splash('splash', file.split('=')[1].rstrip('\r\n'),'False')
         
 
     dialog = xbmcgui.Dialog()
     dialog.ok("Kodi Maintenance", '','ALL Done.', "")
def remove_everything(url):
     findaddon_all_everything(url,'a')

def findaddon_all_everything(url,name):  
    print '############################################################       REMOVE ADDON             ###############################################################'

    pluginpath = xbmc.translatePath(os.path.join('special://home/addons',''))
    import glob
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Remove ALL ???", '', "Do you want to Remove???"):
     dp = xbmcgui.DialogProgress()
     dp.create("Removing Addons", "Pleas Wait", '', "")
     dp.update(0)
     for file in glob.glob(os.path.join(pluginpath, '*')):
        
        file_name=file[file.rfind('\\')+1:]

        
        if file_name != 'plugin.program.tvsupertugamanutencao' and file_name!='packages' and 'skin' not in file_name:

          dp.update(0, "Pleas Wait...", file_name+'-Removing', '')
          if dp.iscanceled(): 
              dp.close()
              break
          removeanything_all(file)
      

          
        setView('movies', 'SUB') 
    xbmc.executebuiltin('Container.Refresh')
    sys.exit()

def remove_addon_list(): 
    dialog=xbmcgui.Dialog()
   
    if os.path.exists(download_list):
       version_select=[]
       select=[]
       file = open(download_list, "r") 
       for f in file.readlines():
         
         
         read_text=read_txt_files(f)
         
         if read_text!='ERROR':
          version_select.append(f)
          select.append(f)
    version_select.append('Cancel')
    select.append('Cancel')
    selected_value=(version_select[xbmcgui.Dialog().select('Please Choose Your Build', select)])
    if selected_value!='Cancel':
       dialog = xbmcgui.Dialog()
       if dialog.yesno("Remove Addon list" , "Remove " + selected_value+'?', "Are you Sure?"):
         f = open(download_list,"r+")
         d = f.readlines()
         f.seek(0)
         for i in d:
           if i != selected_value:
             f.write(i)
         f.truncate()
         f.close()
    xbmc.executebuiltin('Container.Refresh')   
    #return version_select[xbmcgui.Dialog().select('Please Choose Your Build', select)]
	
def mail_message():
	import smtplib

	SERVER = "localhost"

	FROM = "ebs111@gmail.com"
	TO = ["ebs111@gmail.com"] # must be a list

	SUBJECT = "Hello!"

	TEXT = "This message was sent with Python's smtplib."

	# Prepare actual message

	message = """\From: %so: %sSubject: %s%s""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

	# Send the mail

	fromaddr = FROM
	toaddrs  = TO
	msg =message 

	msg = msg.format(fromaddr =fromaddr, toaddr = toaddrs[0])
	# The actual mail send
	server = smtplib.SMTP('gmail-smtp-in.l.google.com:25')
	server.starttls()
	server.ehlo("example.com")
	server.mail(fromaddr)
	server.rcpt(toaddrs[0])
	server.data(msg)
	server.quit()  
def Readme():
   help_file = xbmc.translatePath(os.path.join('special://home/addons','plugin.program.tvsupertugamanutencao'))+'\help.txt'
   file = open(help_file, "r") 
   showText('List File Help',file.read())
   file.close()
   sys.exit()
def showText(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            retry -= 1
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            return
        except:
            pass
def View_log():
    logfile=loglocation()+'kodi.log'

    file = open(logfile, "r") 
    file_text=file.read()
    file_text=file_text.replace('ERROR','[B][COLOR red]ERROR[/COLOR][/B]')
    file_text=file_text.replace('WARNING','[B][COLOR blue]WARNING[/COLOR][/B]')
    file_text=file_text.replace('NOTICE','[B][COLOR burlywood]NOTICE[/COLOR][/B]')
    showText('Log File',file_text)
def Mail_log(url):

     if ADDON.getSetting('email')=='':
        Show_Dialog('','You Need To Enter Your Email Details','')
        ADDON.openSettings()
        mail_file.EmailLog(url) 
     else:
        if url=='someone':
          mail_file.EmailLog('')
        else:
          mail_file.EmailLog('ME')
def Show_Dialog(line1,line2,line3):
    dialog = xbmcgui.Dialog()
    dialog.ok('.Kodi Log Emailer', line1,line2,line3)
params=get_params()

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
   
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        main_menu()


 
elif mode==1:
        DeleteCrashLogs(url)
elif mode==2:
        DeletePackages(url) 
elif mode==3:
        deletecachefiles(url)
elif mode==4:
        clear_caches()
elif mode==5:
        remove_all_addons(url,name)
elif mode==6:
        multi_addons_menu()
elif mode==7:
        add_file_location()
elif mode==8:
        add_addon_list(url)
elif mode==9:
        install_package(url,'yes')
elif mode==10:
        install_all_package(url)
elif mode==11:
        remove_everything(url)
elif mode==25:
        findaddon(url,name)
elif mode==26:
        removeanything(url)
elif mode==27:
        change_language(url)
elif mode==28:
        remove_addon_list()
elif mode==29:
        Readme()
elif mode==30:
        change_splash(name,url,'True')
elif mode==31:
        View_log()
elif mode==32:
        Mail_log(url)
elif mode==65:
        cleandb()       



if len(sys.argv)>0:

 xbmcplugin.endOfDirectory(int(sys.argv[1]))
