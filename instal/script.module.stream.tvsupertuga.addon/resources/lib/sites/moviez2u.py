"""
   Moviez2U.com | Stream TVsupertuga
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

BASEURL = 'http://www.moviez2u.com'

def MAIN():
    addDir('Search', BASEURL, 454, art + 'search.png', fanart)
    addDir('Movies', 'http://ignorme', 451, art + 'movies.png', fanart)
    addDir('TV Shows', 'http://ignorme', 452, art + 'tvshows.png', fanart)
    xbmc.executebuiltin('Container.SetViewMode(50)')


def MOVIES():
    addDir('Featured', BASEURL + '/genre/featured/', 482, art + 'featured.png', fanart)
    addDir('Popular', BASEURL + '/genre/popular-movies/', 482, art + 'popular.png', fanart)
    addDir('Trending', BASEURL + '/trending/?get=movies', 482, art + 'trending.png', fanart)
    addDir('All Movies', BASEURL + '/movies/', 482, art + 'movies.png', fanart)
    addDir('Best Ratings', BASEURL + '/ratings/?get=movies', 482, art + 'best.png', fanart)
    addDir('Genres', BASEURL, 453, art + 'genres.png', fanart)
    xbmc.executebuiltin('Container.SetViewMode(50)')


def TVSHOWS():
    addDir('Trending', BASEURL + '/trending/?get=tv', 485, art + 'trending.png', fanart)
    addDir('All TV Shows', BASEURL + '/tvshows/', 485, art + 'tvshows.png', fanart)
    addDir('Best Ratings', BASEURL + '/ratings/?get=tv', 485, art + 'best.png', fanart)
    xbmc.executebuiltin('Container.SetViewMode(50)')


def GETMOVIES(url):
    link = open_url(url)
    match = re.compile('<div class="poster">[^"]+<a href="([^"]+)"><img src="([^"]+)" alt="([^"]+) Full.+?"></a>[^"]+<div class="rating"><span class="icon-star2"></span>([^"]+)</div>[^"]+<span class="quality">([^"]+)</span>', re.DOTALL).findall(link)
    for url, img, name, rating, quality in match:
        try:
            name = name.replace('&#8217;', "'").replace('#038;', '').replace('\\xc3\\xa9', 'e').replace('&#8211;', '-')
            name = name + ':' + ' ' + ' ' + '[COLOR dodgerblue]' + quality + '[/COLOR]' + ' ' + '|' + ' ' + 'Rating:[COLOR dodgerblue]' + ' ' + rating + '[/COLOR]'
            addDir(name, url, 484, img, fanart)
        except:
            pass

    try:
        np = re.compile('<link rel="next" href="(.+?)"', re.DOTALL | re.IGNORECASE).findall(link)[0]
        name = '[COLOR dodgerblue]' + 'Next Page >>' + '[/COLOR]'
        addDir(name, np, 485, next, fanart)
    except:
        pass

    xbmc.executebuiltin('Container.SetViewMode(50)')


def GETTVSHOWS(url):
    link = open_url(url)
    match = re.compile('<div class="poster">[^"]+<a href="([^"]+)"><img src="([^"]+)" alt="([^"]+)"></a>', re.DOTALL).findall(link)
    for url, img, name in match:
        try:
            name = name.replace('&#8217;', "'").replace('#038;', '').replace('\\xc3\\xa9', 'e').replace('&#8211;', '-')
            addDir(name, url, 486, img, fanart)
        except:
            pass

    try:
        np = re.compile('<link rel="next" href="(.+?)"', re.DOTALL | re.IGNORECASE).findall(link)[0]
        name = '[COLOR dodgerblue]' + 'Next Page >>' + '[/COLOR]'
        addDir(name, np, 482, next, fanart)
    except:
        pass

    xbmc.executebuiltin('Container.SetViewMode(50)')


def GETEPISODE(url):
    link = open_url(url)
    match = re.compile('<li>[^"]+<div class="imagen"><a href="([^"]+)"><img src="([^"]+)"></a></div>[^"]+<div class="numerando">([^"]+) - ([^"]+)</div>[^"]+<div class="episodiotitle">[^"]+<a href=".+?">([^"]+)</a>', re.DOTALL).findall(link)
    for url, img, season, episode, name in match:
        try:
            name = 'Season: ' + '[COLOR dodgerblue]' + ' ' + season + '[/COLOR]' + ' ' + '|' + ' ' + ' ' + 'Episode:[COLOR dodgerblue]' + ' ' + episode + '[/COLOR]' + ':   ' + name
            addDir(name, url, 484, img, fanart)
        except:
            pass

    xbmc.executebuiltin('Container.SetViewMode(50)')


def GENRES(url):
    link = open_url(url)
    match = re.compile('<li class="cat-item cat-item.+?"><a href="(.+?)" >(.+?)</a> <i>(.+?)</i>', re.DOTALL).findall(link)
    for url, name, total in match:
        try:
            if '&amp;' in name:
                pass
            elif 'Popular' in name:
                pass
            elif 'Featured' in name:
                pass
            else:
                name = name.replace('&#8217;', "'").replace('#038;', '').replace('\\xc3\\xa9', 'e').replace('&#8211;', '-').replace('&#215;', 'x')
                name = name + ':' + ' ' + ' ' + '[B][COLOR dodgerblue](' + ' ' + total + ')[/COLOR][/B]'
                addDir(name, url, 482, iconimage, fanart)
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
                addLink(name, url, 483, iconimage, fanart)
            elif 'google' in url:
                name = 'GoogleVideo'
                url = url.replace('/preview', '')
                addLink(name, url, 483, iconimage, fanart)
        except:
            pass

    xbmc.executebuiltin('Container.SetViewMode(50)')


def SEARCH(url):
    search_entered = ''
    keyboard = xbmc.Keyboard(search_entered, 'Search Moviez2U.com')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ', '+')
    if len(search_entered) > 1:
        url = url + '/?s=' + search_entered
        progress = xbmcgui.DialogProgress()
        GETSEARCH(url)


def GETSEARCH(url):
    link = open_url(url)
    match = re.compile('<div class="thumbnail animation-2">[^"]+<a href="([^"]+)">[^"]+<img src="([^"]+)" alt="([^"]+)"', re.DOTALL).findall(link)
    for url, img, name in match:
        try:
            if '/episodes/' in url:
                name = name.replace('&#8217;', "'").replace('#038;', '').replace('\\xc3\\xa9', 'e').replace('&#8211;', '-').replace('&#215;', 'x')
                addDir(name, url, 484, img, fanart)
            elif '/movies/' in url:
                name = name.replace('&#8217;', "'").replace('#038;', '').replace('\\xc3\\xa9', 'e').replace('&#8211;', '-').replace('&#215;', 'x')
                addDir(name, url, 484, img, fanart)
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