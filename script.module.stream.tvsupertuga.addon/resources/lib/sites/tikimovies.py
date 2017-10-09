"""
   TikiMovies.com | Stream TVsupertuga
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
import urllib, urllib2, re, xbmcplugin, xbmcgui, urlresolver, sys, xbmc, xbmcaddon, os, urlparse, base64
from t0mm0.common.addon import Addon
from metahandler import metahandlers
from resources.lib import utils
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
open_url = utils.open_url

BASEURL = 'http://tikimovies.com'

def MAIN():
    addDir('Search', BASEURL, 489, art + 'search.png', fanart)
    addDir('Movies', 'http://ignorme', 493, art + 'movies.png', fanart)
    addDir('TV Shows', 'http://ignorme', 494, art + 'tvshows.png', fanart)
    xbmc.executebuiltin('Container.SetViewMode(50)')


def MOVIES():
    addDir('Trending', BASEURL + '/trending/?get=movies', 488, art + 'trending.png', fanart)
    addDir('All Movies', BASEURL + '/movies/', 488, art + 'movies.png', fanart)
    addDir('Best Ratings', BASEURL + '/ratings/?get=movies', 488, art + 'best.png', fanart)
    addDir('Genres', BASEURL, 500, art + 'genres.png', fanart)
    addDir('Release', BASEURL, 501, art + 'release.png', fanart)
    xbmc.executebuiltin('Container.SetViewMode(50)')


def TVSHOWS():
    addDir('Trending', BASEURL + '/trending/?get=tv', 495, art + 'trending.png', fanart)
    addDir('Recently Added Seasons', BASEURL + '/seasons/', 497, art + 'recently.png', fanart)
    addDir('Recently Added Episode', BASEURL + '/episodes/', 499, art + 'recently.png', fanart)
    addDir('All TV Shows', BASEURL + '/tvshows/', 495, art + 'movies.png', fanart)
    addDir('Best Ratings', BASEURL + '/ratings/?get=tv', 495, art + 'best.png', fanart)
    xbmc.executebuiltin('Container.SetViewMode(50)')


def GETMOVIES(url):
    link = open_url(url)
    match = re.compile('<div class="poster">[^"]+<a href="([^"]+)"><img src="([^"]+)" alt="([^"]+)"></a>[^"]+<div class="rating"><span class="icon-star2"></span> ([^"]+)</div>[^"]+<span class="quality">([^"]+)</span>', re.DOTALL).findall(link)
    for url, img, name, rating, quality in match:
        try:
            name = name.replace('&#8217;', "'").replace('#038;', '').replace('\\xc3\\xa9', 'e').replace('&#8211;', '-')
            name = name + ':' + ' ' + ' ' + '[COLOR dodgerblue]' + quality + '[/COLOR]' + ' ' + '|' + ' ' + 'Rating:[COLOR dodgerblue]' + ' ' + rating + '[/COLOR]'
            addDir(name, url, 490, img, fanart)
        except:
            pass

    nextpage = re.compile('<a href=([^"]+) class="inactive">(.+?)</a>', re.DOTALL).findall(link)
    for np, name in nextpage:
        try:
            np = np.replace("'", '')
            url = np
            name = '[COLOR dodgerblue]' + 'Page ' + name + ' >> [/COLOR]'
            addDir(name, url, 488, next, fanart)
        except:
            pass

    xbmc.executebuiltin('Container.SetViewMode(50)')


def GETTVSHOWS(url):
    link = open_url(url)
    match = re.compile('<div class="poster">\n<a href="([^"]+)"><img src="([^"]+)" alt="([^"]+)"></a>\n<div class="rating"><span class="icon-star2"></span>([^"]+)</div>', re.DOTALL).findall(link)
    for url, img, name, rating in match:
        try:
            name = name.replace('&#8217;', "'").replace('#038;', '').replace('\\xc3\\xa9', 'e').replace('&#8211;', '-')
            rating = rating.replace('</div>', '')
            name = name + ':' + ' ' + ' ' + 'Rating:[COLOR dodgerblue]' + ' ' + rating + '[/COLOR]'
            addDir(name, url, 496, img, fanart)
        except:
            pass

    xbmc.executebuiltin('Container.SetViewMode(50)')


def GETSEASONS(url):
    link = open_url(url)
    match = re.compile('<div class="poster">\n<img src="([^"]+)" alt="([^"]+)">\n<div class="season_m animation-1">\n<a href="([^"]+)"', re.DOTALL).findall(link)
    for img, name, url in match:
        try:
            name = name.replace('&#8217;', "'").replace('#038;', '').replace('\\xc3\\xa9', 'e').replace('&#8211;', '-')
            addDir(name, url, 498, img, fanart)
        except:
            pass
    nextpage = re.compile('<a href=([^"]+) class="inactive">(.+?)</a>', re.DOTALL).findall(link)
    for np, name in nextpage:
        try:
            np = np.replace("'", '')
            url = np
            name = '[COLOR dodgerblue]' + 'Page ' + name + ' >> [/COLOR]'
            addDir(name, url, 497, next, fanart)
        except:
            pass
    xbmc.executebuiltin('Container.SetViewMode(50)')


def GETEPISODE(url):
    link = open_url(url)
    match = re.compile('<li>\n<div class="imagen"><a href="([^"]+)"><img src="([^"]+)"></a></div>\n<div class="numerando">([^"]+) - ([^"]+)</div>\n<div class="episodiotitle">\n<a href=".+?">([^"]+)</a>', re.DOTALL).findall(link)
    for url, img, season, episode, name in match:
        try:
            name = 'Season: ' + '[COLOR dodgerblue]' + ' ' + season + '[/COLOR]' + ' ' + '|' + ' ' + ' ' + 'Episode:[COLOR dodgerblue]' + ' ' + episode + '[/COLOR]' + ':   ' + name
            addDir(name, url, 490, img, fanart)
        except:
            pass
    xbmc.executebuiltin('Container.SetViewMode(50)')


def GETEPISODE2(url):
    link = open_url(url)
    match = re.compile('<div class="imagen"><a href="([^"]+)"><img src="([^"]+)"></a></div>\n<div class="numerando">([^"]+)x([^"]+)</div>\n<div class="episodiotitle">\n<a href=".+?">([^"]+)</a>', re.DOTALL).findall(link)
    for url, img, season, episode, name in match:
        try:
            name = 'Season: ' + '[COLOR dodgerblue]' + ' ' + season + '[/COLOR]' + ' ' + '|' + ' ' + ' ' + 'Episode:[COLOR dodgerblue]' + ' ' + episode + '[/COLOR]' + ':   ' + name
            addDir(name, url, 490, img, fanart)
        except:
            pass
    xbmc.executebuiltin('Container.SetViewMode(50)')


def GETEPISODE3(url):
    link = open_url(url)
    match = re.compile('<div class="poster">\n<img src="([^"]+)" alt="([^"]+)">\n<div class="season_m animation-1">\n<a href="([^"]+)"', re.DOTALL).findall(link)
    for img, name, url in match:
        try:
            name = name.replace('&#8217;', "'").replace('#038;', '').replace('\\xc3\\xa9', 'e').replace('&#8211;', '-').replace('&#215;', 'x')
            addDir(name, url, 490, img, fanart)
        except:
            pass
    nextpage = re.compile('<a href=([^"]+) class="inactive">(.+?)</a>', re.DOTALL).findall(link)
    for np, name in nextpage:
        try:
            np = np.replace("'", '')
            url = np
            name = '[COLOR dodgerblue]' + 'Page ' + name + ' >> [/COLOR]'
            addDir(name, url, 499, next, fanart)
        except:
            pass
    xbmc.executebuiltin('Container.SetViewMode(50)')


def GENRES(url):
    link = open_url(url)
    match = re.compile('<li class="cat-item cat-item.+?"><a href="(.+?)">(.+?)</a> <i>(.+?)</i>', re.DOTALL).findall(link)
    for url, name, total in match:
        try:
            if '&amp;' in name:
                pass
            else:
                name = name.replace('&#8217;', "'").replace('#038;', '').replace('\\xc3\\xa9', 'e').replace('&#8211;', '-').replace('&#215;', 'x')
                name = name + ':' + ' ' + ' ' + '[B][COLOR dodgerblue](' + ' ' + total + ')[/COLOR][/B]'
                addDir(name, url, 488, iconimage, fanart)
        except:
            pass
    xbmc.executebuiltin('Container.SetViewMode(50)')


def RELEASE(url):
    link = open_url(url)
    match = re.compile('<li><a href="http://tikimovies.com/release(.+?)">(.+?)</a></li>', re.DOTALL).findall(link)
    for url, name in match:
        try:
            url = 'http://tikimovies.com/release' + url
            addDir(name, url, 488, iconimage, fanart)
        except:
            pass
    xbmc.executebuiltin('Container.SetViewMode(50)')


def GETSOURCE(url):
    link = open_url(url)
    match = re.compile('<iframe class="metaframe rptss" src="(.+?)"', re.DOTALL).findall(link)
    for url in match:
        try:
            if 'openload' in url:
                name = 'OpenLoad.co'
                addLink(name, url, 491, iconimage, fanart)
            elif 'google' in url:
                name = 'GoogleVideo'
                url = url.replace('/preview', '')
                addLink(name, url, 491, iconimage, fanart)
        except:
            pass
    xbmc.executebuiltin('Container.SetViewMode(50)')


def SEARCH(url):
    search_entered = ''
    keyboard = xbmc.Keyboard(search_entered, 'Search TikiMovies.com')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ', '+')
    if len(search_entered) > 1:
        url = url + '/?s=' + search_entered
        progress = xbmcgui.DialogProgress()
        GETSEARCH(url)


def GETSEARCH(url):
    link = open_url(url)
    match = re.compile('<a href="([^"]+)">\n<img src="([^"]+)" alt="([^"]+)"', re.DOTALL).findall(link)
    for url, img, name in match:
        try:
            if '/movies/' in url:
                addDir(name, url, 490, img, fanart)
            elif '/tvshows/' in url:
                addDir(name, url, 496, img, fanart)
        except:
            pass
    xbmc.executebuiltin('Container.SetViewMode(50)')


def resolve(name, url, iconimage):
    progress = xbmcgui.DialogProgress()
    progress.create('Stream TVsupertuga', 'Opening Stream For:')
    progress.update(10, '', name, '')
    url = urlresolver.resolve(url)
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title': name})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
    xbmc.Player().play(url, liz, False)


def GOOGLE(name, url, iconimage):
    progress = xbmcgui.DialogProgress()
    progress.create('Stream TVsupertuga', 'Opening Stream For:')
    progress.update(10, '', name, '')
    link = open_url(url)
    stream_url = re.compile('<iframe src="([^"]+)"').findall(link)
    try:
        for url in stream_url:
            url = urlresolver.resolve(url)
            liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
            liz.setInfo(type='Video', infoLabels={'Title': name})
            ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
            xbmc.Player().play(url, liz, False)

    except:
        pass