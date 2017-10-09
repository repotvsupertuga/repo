"""
   GOmovies.sc | Stream TVsupertuga
   Copyright (C) 2017 Mister-X

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,sys,xbmc,xbmcaddon,os,urlparse,base64,net,requests
from t0mm0.common.addon import Addon
from metahandler import metahandlers
from resources.lib import utils
from resources.cloudflare import cloudflare

net = net.Net()
addon_id = utils.addon_id
addDir = utils.addDir
addLink = utils.addLink
selfAddon = utils.selfAddon
addon = utils.addon
fanart = utils.fanart
icon = utils.addon
next = utils.next
art = utils.art
name = utils.name
mode = utils.mode
url = utils.url
iconimage = utils.iconimage
site = utils.site
setView = utils.setView

BASEURL = 'https://gomovies.sc'

datapath= xbmc.translatePath(selfAddon.getAddonInfo('profile'))
try:os.mkdir(datapath)
except:pass
file_var = open(xbmc.translatePath(os.path.join(datapath, 'cookie.lwp')), "a")
cookie_file = os.path.join(os.path.join(datapath,''), 'cookie.lwp')

def MAIN():
    addDir('Search',BASEURL,510,art+'search.png',fanart)
    addDir('Movies','http://ignorme',506,art+'movies.png',fanart)
    addDir('TV Shows','http://ignorme',507,art+'tvshows.png',fanart)
    addDir('Genres',BASEURL,511,art+'genres.png',fanart)
    addDir('Country',BASEURL,512,art+'country.png',fanart)		
    xbmc.executebuiltin('Container.SetViewMode(50)')
	
def MOVIES():
    addDir('Popular',BASEURL+'/movie/filter/movies/favorite/all/all/all/all/',503,art+'popular.png',fanart)
    addDir('Most Viewed',BASEURL+'/movie/filter/movies/view/all/all/all/all/',503,art+'most.png',fanart)
    addDir('Recently Added',BASEURL+'/movie/filter/movies/latest/all/all/all/all/',503,art+'recently.png',fanart)
    addDir('All Movies',BASEURL+'/movies/',503,art+'movies.png',fanart)
    addDir('Best Ratings',BASEURL+'/movie/filter/movies/rating/all/all/all/all/',503,art+'best.png',fanart)	
    addDir('Top iMDB',BASEURL+'/movie/filter/movies/imdb_mark/all/all/all/all/',503,art+'imdb.png',fanart)		
    xbmc.executebuiltin('Container.SetViewMode(50)')

def TVSHOWS():
    addDir('Popular',BASEURL+'/movie/filter/seasons/favorite/all/all/all/all/',503,art+'popular.png',fanart)
    addDir('Most Viewed',BASEURL+'/movie/filter/seasons/view/all/all/all/all/',503,art+'most.png',fanart)
    addDir('Latest Added',BASEURL+'/movie/filter/seasons/latest/all/all/all/all/',503,art+'recently.png',fanart)
    addDir('All TV Shows',BASEURL+'/tv-series/',503,art+'movies.png',fanart)
    addDir('Best Ratings',BASEURL+'/movie/filter/seasons/rating/all/all/all/all/',503,art+'best.png',fanart)	
    addDir('Top iMDB',BASEURL+'/movie/filter/seasons/imdb_mark/all/all/all/all/',503,art+'imdb.png',fanart)		
    xbmc.executebuiltin('Container.SetViewMode(50)')
	
def GETMOVIES(url):
	link = open_url(url)
	match=re.compile('<a href="([^"]+)" class="ml-mask jt" data-url="[^"]+" data-hasqtip="[^"]+" oldtitle="([^"]+)" title="[^"]+" aria-describedby="qtip-[^"]+">[^"]+<span class="mli-.+?">([^"]+)</span>[^"]+<img class="thumb mli-thumb lazy" title="[^"]+" alt="[^"]+" data-original="([^"]+)"',re.DOTALL).findall(link)
	for url, name, info, img in match:
			try:
				if '/movie/' in url:
					url = url + '1/watching/'
					name = name.replace('&#8217;','\'').replace('#038;','').replace('\\xc3\\xa9','e').replace('&#8211;','-').replace('&amp;', '&')
					name = name + ':' + ' ' + ' ' + '[B][COLOR dodgerblue](' + info + ')[/COLOR][/B]'
					addDir(name,url,513,img,fanart)
				elif '/tv/' in url:
					url = url + '1-1/watching/'
					name = name.replace('&#8217;','\'').replace('#038;','').replace('\\xc3\\xa9','e').replace('&#8211;','-').replace('&amp;', '&')
					info = info.replace('<i>', ' ').replace('</i>', ' ').replace('Eps','EPS')
					name = name + ':' + ' ' + ' ' + '[B][COLOR dodgerblue](' + info + ')[/COLOR][/B]'
					addDir(name,url,509,img,fanart)					
			except:pass
	try:
		np=re.compile('<a href="([^"]+)">Next[^"]+</a>', re.DOTALL | re.IGNORECASE).findall(link)[0]
		name = '[COLOR dodgerblue]' + 'Next Page >>' + '[/COLOR]'
		addDir(name,np,503,next,fanart)
	except:pass
	xbmc.executebuiltin('Container.SetViewMode(50)')

def GETEPISODE(url):
    link = open_url(url)
    match = re.compile('<a title="([^"]+)" data-.+?="(.+?)".+?data-server="(.+?)"', re.DOTALL).findall(link)
    for name, url, server in match:
        try:
			if 'openload' in url:
				name = '[COLOR dodgerblue]Server ' + server + ': [/COLOR]' + " " + name
				addLink(name,url,505,iconimage,fanart)
			elif 'estream' in url:
				name = '[COLOR dodgerblue]Server ' + server + ': [/COLOR]' + " " + name
				addLink(name,url,505,iconimage,fanart) 
			else:
				name = '[COLOR dodgerblue]Server ' + server + ': [/COLOR]' + " " + name
				addLink(name,url,508,iconimage,fanart) 						
        except:pass
    xbmc.executebuiltin('Container.SetViewMode(50)')

def GENRES(url):
    link = open_url(url)
    match = re.compile('<a href="https://gomovies.sc/genre(.+?)" title="(.+?)"', re.DOTALL).findall(link)
    for url, name in match:
        try:
			url = BASEURL + '/genre' + url
			addDir(name,url,503,iconimage,fanart)				
        except:pass
    xbmc.executebuiltin('Container.SetViewMode(50)')

def COUNTRY(url):
    link = open_url(url)
    match = re.compile('<a href="https://gomovies.sc/country(.+?)" title="(.+?)"', re.DOTALL).findall(link)
    for url, name in match:
        try:
			url = BASEURL + '/country' + url
			addDir(name,url,503,iconimage,fanart)				
        except:pass
    xbmc.executebuiltin('Container.SetViewMode(50)')

def GETSOURCE2(url):
    link = open_url(url)
    match = re.compile('file: "(.+?)", label: "(.+?)"', re.DOTALL).findall(link)
    for url, name in match:
        try:
			name = "GoogleVideo: " + "[COLOR dodgerblue](" + name + ")[/COLOR]"
			addLink(name,url,505,iconimage,fanart)				
        except:pass
    xbmc.executebuiltin('Container.SetViewMode(50)')
	
def GETSOURCE(url):
    link = open_url(url)
    match = re.compile('<div class="les-content">\n.+?<a title="(.+?)" .+? data-(.+?)="(.+?)"', re.DOTALL).findall(link)
    for quality, name, url in match:
        try:
			if 'drive' in name:
				name = name.replace('drive','GoogleVideo')
				addLink(name,url,508,iconimage,fanart)
			else:
				name = name.replace('openload','OpenLoad.co').replace('estream','EStream.com')
				addLink(name,url,505,iconimage,fanart)				
        except:pass
    xbmc.executebuiltin('Container.SetViewMode(50)')
	
def SEARCH(url):
    search_entered = ''
    keyboard = xbmc.Keyboard(search_entered, 'Search GOmovies.sc')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ', '+')
    if len(search_entered) > 1:
        url = url + '/search-query/' + search_entered
        progress = xbmcgui.DialogProgress()
        GETMOVIES(url)

def resolve(name, url, iconimage):
    progress = xbmcgui.DialogProgress()
    progress.create('Stream TVsupertuga', 'Opening Stream For:')
    progress.update(10, '', name, '')
    url = urlresolver.resolve(url)
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title': name})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
    xbmc.Player().play(url, liz, False)
	
def GOOGLE(name,url,iconimage):
	progress = xbmcgui.DialogProgress()
	progress.create('Stream TVsupertuga', 'Opening Stream For:')
	progress.update(10, "", name, "" )
        link = open_url(url)
        stream_url=re.compile('.+?file.+?"(.+?)"').findall(link)
        try:
            for url in stream_url:
					url = url.replace('https:\/\/','https://')
					url = url.replace('\/','/')
					url = urlresolver.resolve(url)
					liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
					ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
					xbmc.Player ().play(url, liz, False)
        except:pass	
		
def open_url(url):
        try:
                net.set_cookies(cookie_file)
                link = net.http_GET(url).content
                link = cleanHex(link)
                return link
        except:
                from resources.cloudflare import cloudflare
                cloudflare.createCookie(url,cookie_file,'Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0')
                net.set_cookies(cookie_file)
                link = net.http_GET(url).content
                link = cleanHex(link)
                return link	

def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    try :return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))
    except:return re.sub("(?i)&#\w+;", fixup, text.encode("ascii", "ignore").encode('utf-8'))		