# -*- coding: utf-8 -*-

'''
    Football Today Addon
    Copyright (C) 2014 lambda

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
'''

import urllib,urllib2,re,os,threading,datetime,time,base64,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
from operator import itemgetter
try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database
try:
    import CommonFunctions as common
except:
    import commonfunctionsdummy as common
try:
    import json
except:
    import simplejson as json


action              = None
language            = xbmcaddon.Addon().getLocalizedString
setSetting          = xbmcaddon.Addon().setSetting
getSetting          = xbmcaddon.Addon().getSetting
addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
addonDesc           = language(30450).encode("utf-8")
dataPath            = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile")).decode("utf-8")
addonIcon           = os.path.join(addonPath,'icon.png')
addonArt            = os.path.join(addonPath,'resources/art')
addonFanart         = os.path.join(addonPath,'fanart.jpg')
addonNext           = os.path.join(addonPath,'resources/art/videos_next.png')
addonSettings       = os.path.join(dataPath,'settings.db')
addonCache          = os.path.join(dataPath,'cache.db')


class main:
    def __init__(self):
        global action
        index().container_data()
        params = {}
        splitparams = sys.argv[2][sys.argv[2].find('?') + 1:].split('&')
        for param in splitparams:
            if (len(param) > 0):
                splitparam = param.split('=')
                key = splitparam[0]
                try:    value = splitparam[1].encode("utf-8")
                except: value = splitparam[1]
                params[key] = value

        try:        action = urllib.unquote_plus(params["action"])
        except:     action = None
        try:        url = urllib.unquote_plus(params["url"])
        except:     url = None
        try:        meta = urllib.unquote_plus(params["meta"])
        except:     meta = None
        try:        query = urllib.unquote_plus(params["query"])
        except:     query = None


        if action == None:                          root().get()
        elif action == 'cache_clear_list':          index().cache_clear_list()
        elif action == 'item_play':                 contextMenu().item_play()
        elif action == 'item_random_play':          contextMenu().item_random_play()
        elif action == 'item_queue':                contextMenu().item_queue()
        elif action == 'playlist_open':             contextMenu().playlist_open()
        elif action == 'settings_open':             contextMenu().settings_open()
        elif action == 'view_videos':               contextMenu().view('videos')
        elif action == 'videos':                    videos().get(url)
        elif action == 'videos_games':              videos().root('lfv_games')
        elif action == 'videos_highlights':         videos().root('lfv_highlights')
        elif action == 'videos_premierleague':      videos().root('lfv_premierleague')
        elif action == 'videos_laliga':             videos().root('lfv_laliga')
        elif action == 'videos_bundesliga':         videos().root('lfv_bundesliga')
        elif action == 'videos_seriea':             videos().root('lfv_seriea')
        elif action == 'videos_ligue1':             videos().root('lfv_ligue1')
        elif action == 'videos_eredivisie':         videos().root('lfv_eredivisie')
        elif action == 'videos_primeiraliga':       videos().root('lfv_primeiraliga')
        elif action == 'videos_uefachampionleague': videos().root('lfv_uefachampionleague')
        elif action == 'videos_uefaeuropaleague':   videos().root('lfv_uefaeuropaleague')
        elif action == 'videos_copalibertadores':   videos().root('lfv_copalibertadores')
        elif action == 'videos_search':             videos().search(query)
        elif action == 'videos_parts':              videoparts().get(url, meta)
        elif action == 'play':                      resolver().run(url)

class getUrl(object):
    def __init__(self, url, close=True, proxy=None, post=None, mobile=False, referer=None, cookie=None, output='', timeout='10'):
        if not proxy == None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
            opener = urllib2.install_opener(opener)
        if not post == None:
            request = urllib2.Request(url, post)
        else:
            request = urllib2.Request(url,None)
        if mobile == True:
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
        else:
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0')
        if not referer == None:
            request.add_header('Referer', referer)
        if not cookie == None:
            request.add_header('cookie', cookie)
        response = urllib2.urlopen(request, timeout=int(timeout))
        if output == 'cookie':
            result = str(response.headers.get('Set-Cookie'))
        elif output == 'geturl':
            result = response.geturl()
        else:
            result = response.read()
        if close == True:
            response.close()
        self.result = result

class uniqueList(object):
    def __init__(self, list):
        uniqueSet = set()
        uniqueList = []
        for n in list:
            if n not in uniqueSet:
                uniqueSet.add(n)
                uniqueList.append(n)
        self.list = uniqueList

class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)

class player(xbmc.Player):
    def __init__ (self):
        xbmc.Player.__init__(self)

    def run(self, url):
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

    def onPlayBackStarted(self):
        return

    def onPlayBackEnded(self):
        return

    def onPlayBackStopped(self):
        return

class index:
    def infoDialog(self, str, header=addonName):
        try: xbmcgui.Dialog().notification(header, str, addonIcon, 3000, sound=False)
        except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % (header, str, addonIcon))

    def okDialog(self, str1, str2, header=addonName):
        xbmcgui.Dialog().ok(header, str1, str2)

    def selectDialog(self, list, header=addonName):
        select = xbmcgui.Dialog().select(header, list)
        return select

    def yesnoDialog(self, str1, str2, header=addonName, str3='', str4=''):
        answer = xbmcgui.Dialog().yesno(header, str1, str2, '', str4, str3)
        return answer

    def getProperty(self, str):
        property = xbmcgui.Window(10000).getProperty(str)
        return property

    def setProperty(self, str1, str2):
        xbmcgui.Window(10000).setProperty(str1, str2)

    def clearProperty(self, str):
        xbmcgui.Window(10000).clearProperty(str)

    def addon_status(self, id):
        check = xbmcaddon.Addon(id=id).getAddonInfo("name")
        if not check == addonName: return True

    def container_refresh(self):
        xbmc.executebuiltin('Container.Refresh')

    def container_data(self):
        if not xbmcvfs.exists(dataPath):
            xbmcvfs.mkdir(dataPath)

    def container_view(self, content, viewDict):
        try:
            skin = xbmc.getSkinDir()
            record = (skin, content)
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM views WHERE skin = '%s' AND view_type = '%s'" % (record[0], record[1]))
            view = dbcur.fetchone()
            view = view[2]
            if view == None: raise Exception()
            xbmc.executebuiltin('Container.SetViewMode(%s)' % str(view))
        except:
            try:
                id = str(viewDict[skin])
                xbmc.executebuiltin('Container.SetViewMode(%s)' % id)
            except:
                pass

    def cache(self, function, timeout, *args):
        try:
            response = None

            f = repr(function)
            f = re.sub('.+\smethod\s|.+function\s|\sat\s.+|\sof\s.+', '', f)

            import hashlib
            a = hashlib.md5()
            for i in args: a.update(str(i))
            a = str(a.hexdigest())
        except:
            pass

        try:
            dbcon = database.connect(addonCache)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM rel_list WHERE func = '%s' AND args = '%s'" % (f, a))
            match = dbcur.fetchone()

            response = eval(match[2].encode('utf-8'))

            t1 = int(re.sub('[^0-9]', '', str(match[3])))
            t2 = int(datetime.datetime.now().strftime("%Y%m%d%H%M"))
            update = abs(t2 - t1) >= int(timeout*60)
            if update == False:
                return response
        except:
            pass

        try:
            r = function(*args)
            if (r == None or r == []) and not response == None:
                return response
            elif (r == None or r == []):
                return r
        except:
            return

        try:
            r = repr(r)
            t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            dbcur.execute("CREATE TABLE IF NOT EXISTS rel_list (""func TEXT, ""args TEXT, ""response TEXT, ""added TEXT, ""UNIQUE(func, args)"");")
            dbcur.execute("DELETE FROM rel_list WHERE func = '%s' AND args = '%s'" % (f, a))
            dbcur.execute("INSERT INTO rel_list Values (?, ?, ?, ?)", (f, a, r, t))
            dbcon.commit()
        except:
            pass

        try:
            return eval(r.encode('utf-8'))
        except:
            pass

    def cache_clear_list(self):
        try:
            dbcon = database.connect(addonCache)
            dbcur = dbcon.cursor()
            dbcur.execute("DROP TABLE IF EXISTS rel_list")
            dbcur.execute("VACUUM")
            dbcon.commit()

            index().infoDialog(language(30303).encode("utf-8"))
        except:
            pass

    def rootList(self, rootList):
        if rootList == None or len(rootList) == 0: return

        total = len(rootList)
        for i in rootList:
            try:
                try: name = language(i['name']).encode("utf-8")
                except: name = i['name']

                image = '%s/%s' % (addonArt, i['image'])

                root = i['action']
                u = '%s?action=%s' % (sys.argv[0], root)
                try: u += '&url=%s' % urllib.quote_plus(i['url'])
                except: pass
                if u == '': raise Exception()

                cm = []

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo(type="Video", infoLabels={"title": name, "plot": addonDesc})
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

    def videoList(self, videoList):
        if videoList == None or len(videoList) == 0: return

        total = len(videoList)
        for i in videoList:
            try:
                name, url, image, date, genre, plot, title, show = i['name'], i['url'], i['image'], i['date'], i['genre'], i['plot'], i['title'], i['show']

                try: fanart = i['fanart']
                except: fanart = '0'

                meta = {'name': name, 'title': title, 'studio': show, 'premiered': date, 'genre': genre, 'plot': plot, 'image': image, 'fanart': fanart}

                sysmeta = urllib.quote_plus(json.dumps(meta))
                sysurl = urllib.quote_plus(url)

                if fanart == '0': fanart = addonFanart
                if image == '0': image = addonFanart
                if show == '0': meta.update({'studio': addonName})
                if plot == '0': meta.update({'plot': addonDesc})
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')

                u = '%s?action=videos_parts&url=%s&meta=%s' % (sys.argv[0], sysurl, sysmeta)

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=view_videos)' % (sys.argv[0])))
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.setProperty("IsPlayable", "true")
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

        try:
            next = videoList[0]['next']
            if next == '': raise Exception()
            name, url, image = language(30361).encode("utf-8"), next, addonNext
            u = '%s?action=videos&url=%s' % (sys.argv[0], urllib.quote_plus(url))
            item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
            item.setInfo( type="Video", infoLabels={"title": name, "plot": addonDesc})
            item.setProperty("Fanart_Image", addonFanart)
            item.addContextMenuItems([], replaceItems=False)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)
        except:
            pass

        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(episodes)'):
                return index().container_view('videos', {'skin.confluence' : 504})
            xbmc.sleep(100)

    def videopartList(self, videopartList):
        if videopartList == None or len(videopartList) == 0: return

        total = len(videopartList)
        for i in videopartList:
            try:
                name, url = i['name'], i['url']
                meta = json.loads(i['meta'])
                image, fanart, show, plot = meta['image'], meta['fanart'], meta['studio'], meta['plot']

                sysurl = urllib.quote_plus(url)

                if fanart == '0': fanart = addonFanart
                if image == '0': image = addonFanart
                if show == '0': meta.update({'studio': addonName})
                if plot == '0': meta.update({'plot': addonDesc})
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')

                u = '%s?action=play&url=%s' % (sys.argv[0], sysurl)

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=view_videos)' % (sys.argv[0])))
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.setProperty("IsPlayable", "true")
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(episodes)'):
                return index().container_view('videos', {'skin.confluence' : 504})
            xbmc.sleep(100)

class contextMenu:
    def item_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.unshuffle()
        xbmc.Player().play(playlist)

    def item_random_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.shuffle()
        xbmc.Player().play(playlist)

    def item_queue(self):
        xbmc.executebuiltin('Action(Queue)')

    def playlist_open(self):
        xbmc.executebuiltin('ActivateWindow(VideoPlaylist)')

    def settings_open(self, id=addonId):
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % id)

    def view(self, content):
        try:
            skin = xbmc.getSkinDir()
            skinPath = xbmc.translatePath('special://skin/')
            xml = os.path.join(skinPath,'addon.xml')
            file = xbmcvfs.File(xml)
            read = file.read().replace('\n','')
            file.close()
            try: src = re.compile('defaultresolution="(.+?)"').findall(read)[0]
            except: src = re.compile('<res.+?folder="(.+?)"').findall(read)[0]
            src = os.path.join(skinPath, src)
            src = os.path.join(src, 'MyVideoNav.xml')
            file = xbmcvfs.File(src)
            read = file.read().replace('\n','')
            file.close()
            views = re.compile('<views>(.+?)</views>').findall(read)[0]
            views = [int(x) for x in views.split(',')]
            for view in views:
                label = xbmc.getInfoLabel('Control.GetLabel(%s)' % (view))
                if not (label == '' or label == None): break
            record = (skin, content, str(view))
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS views (""skin TEXT, ""view_type TEXT, ""view_id TEXT, ""UNIQUE(skin, view_type)"");")
            dbcur.execute("DELETE FROM views WHERE skin = '%s' AND view_type = '%s'" % (record[0], record[1]))
            dbcur.execute("INSERT INTO views Values (?, ?, ?)", record)
            dbcon.commit()
            viewName = xbmc.getInfoLabel('Container.Viewmode')
            index().infoDialog('%s%s%s' % (language(30301).encode("utf-8"), viewName, language(30302).encode("utf-8")))
        except:
            return

class root:
    def get(self):
        rootList = []
        rootList.append({'name': 30501, 'image': 'videos_games.png', 'action': 'videos_games'})
        rootList.append({'name': 30502, 'image': 'videos_highlights.png', 'action': 'videos_highlights'})
        rootList.append({'name': 30503, 'image': 'videos_search.png', 'action': 'videos_search'})
        rootList.append({'name': 'Premier League', 'image': 'videos_premierleague.png', 'action': 'videos_premierleague'})
        rootList.append({'name': 'La Liga', 'image': 'videos_laliga.png', 'action': 'videos_laliga'})
        rootList.append({'name': 'Bundesliga', 'image': 'videos_bundesliga.png', 'action': 'videos_bundesliga'})
        rootList.append({'name': 'Serie A', 'image': 'videos_seriea.png', 'action': 'videos_seriea'})
        rootList.append({'name': 'Ligue 1', 'image': 'videos_ligue1.png', 'action': 'videos_ligue1'})
        rootList.append({'name': 'Eredivisie', 'image': 'videos_eredivisie.png', 'action': 'videos_eredivisie'})
        rootList.append({'name': 'Primeira Liga', 'image': 'videos_primeiraliga.png', 'action': 'videos_primeiraliga'})
        rootList.append({'name': 'UEFA Champions League', 'image': 'videos_uefachampionleague.png', 'action': 'videos_uefachampionleague'})
        rootList.append({'name': 'UEFA Europa League', 'image': 'videos_uefaeuropaleague.png', 'action': 'videos_uefaeuropaleague'})
        rootList.append({'name': 'Copa Libertadores', 'image': 'videos_copalibertadores.png', 'action': 'videos_copalibertadores'})
        index().rootList(rootList)

class link:
    def __init__(self):
        self.lfv_base = 'http://livefootballvideo.com'
        self.lfv_search = 'http://www.google.com/cse?cx=partner-pub-9069051203647610:8413886168&sa=Search&ie=UTF-8&nojs=1&ref=livefootballvideo.com/&q=%s'
        self.lfv_games = 'http://livefootballvideo.com/fullmatch/'
        self.lfv_highlights = 'http://livefootballvideo.com/highlights/'
        self.lfv_premierleague = 'http://livefootballvideo.com/competitions/premier-league/'
        self.lfv_laliga = 'http://livefootballvideo.com/competitions/la-liga/'
        self.lfv_bundesliga = 'http://livefootballvideo.com/competitions/bundesliga/'
        self.lfv_seriea = 'http://livefootballvideo.com/competitions/serie-a/'
        self.lfv_ligue1 = 'http://livefootballvideo.com/competitions/ligue-1/'
        self.lfv_eredivisie = 'http://livefootballvideo.com/competitions/eredivisie/'
        self.lfv_primeiraliga = 'http://livefootballvideo.com/competitions/primeira-liga/'
        self.lfv_uefachampionleague = 'http://livefootballvideo.com/competitions/uefa-champions-league/'
        self.lfv_uefaeuropaleague = 'http://livefootballvideo.com/competitions/uefa-europa-league/'
        self.lfv_copalibertadores = 'http://livefootballvideo.com/competitions/copa-libertadores/'
        self.quality = getSetting("quality")

class videos:
    def __init__(self):
        self.list = []

    def root(self, url):
        url = getattr(link(), url)
        if '/highlights/' in url: self.list = index().cache(self.lfv_list2, 1, url)
        else: self.list = index().cache(self.lfv_list, 1, url)
        index().videoList(self.list)

    def get(self, url):
        if '/highlights/' in url: self.list = index().cache(self.lfv_list2, 1, url)
        else: self.list = index().cache(self.lfv_list, 1, url)
        index().videoList(self.list)

    def search(self, query=None):
        if query == None:
            self.query = common.getUserInput(language(30362).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query == None or self.query == ''):
            self.query = link().lfv_search % urllib.quote_plus(self.query)
            self.list = self.lfv_list3(self.query)
            index().videoList(self.list)

    def lfv_list(self, url):
        try:
            result = getUrl(url, timeout='30').result
            result = re.sub('<li\s.+?>','<li>', result)
            videos = common.parseDOM(result, "li")
        except:
            return

        try:
            next = common.parseDOM(result, "div", attrs = { "class": "wp-pagenavi" })
            if len(next) > 1: next = next[1]
            else: next = next[0]
            next = common.parseDOM(next, "a", ret="href", attrs = { "class": "nextpostslink" })[0]
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for video in videos:
            try:
                title = common.parseDOM(video, "a", ret="title")[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                date = common.parseDOM(video, "p")[-1]
                date = re.findall('(\d+)[/](\d+)[/](\d+)', date, re.I)[0]
                date = '%s-%s-%s' % ('%04d' % int(date[2]), '%02d' % int(date[0]), '%02d' % int(date[1]))

                name = '%s (%s)' % (title, date)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(video, "a", ret="href")[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(video, "img", ret="src")[0]
                if not image.startswith('http'): image = '0'
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                try: show = re.compile('/(fullmatch|highlights)/.+?/(.+?)/').findall(url)[0][1]
                except: show = '0'
                show = show.replace('-', ' ').upper()
                show = common.replaceHTMLCodes(show)
                show = show.encode('utf-8')

                plot = '%s\n%s' % (title, date)
                if not show == '0': plot = '%s\n%s' % (show, plot)
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': date, 'genre': 'Sports', 'plot': plot, 'title': title, 'show': show, 'next': next})
            except:
                pass

        return self.list

    def lfv_list2(self, url):
        try:
            result = getUrl(url, timeout='30').result
            result = re.sub('<li\s.+?>','<li>', result)
            videos = common.parseDOM(result, "li")
        except:
            return

        try:
            next = common.parseDOM(result, "div", attrs = { "class": "wp-pagenavi" })
            if len(next) > 1: next = next[1]
            else: next = next[0]
            next = common.parseDOM(next, "a", ret="href", attrs = { "class": "nextpostslink" })[0]
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for video in videos:
            try:
                home = common.parseDOM(video, "div", attrs = { "class": "team.+?" })[0]
                home = home.split("&nbsp;")[0]
                away = common.parseDOM(video, "div", attrs = { "class": "team.+?" })[-1]
                away = away.split("&nbsp;")[-1]
                title = '%s vs %s' % (home, away)
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                date = common.parseDOM(video, "span", attrs = { "class": "starttime.+?" })[0]
                date = common.replaceHTMLCodes(date)
                date = date.encode('utf-8')

                name = '%s (%s)' % (title, date)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(video, "a", ret="href", attrs = { "class": "playvideo" })[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try: show = re.compile('/(fullmatch|highlights)/.+?/(.+?)/').findall(url)[0][1]
                except: show = '0'
                show = show.replace('-', ' ').upper()
                show = common.replaceHTMLCodes(show)
                show = show.encode('utf-8')

                plot = '%s\n%s' % (title, date)
                if not show == '0': plot = '%s\n%s' % (show, plot)
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': '0', 'date': date, 'genre': 'Sports', 'plot': plot, 'title': title, 'show': show, 'next': next})
            except:
                pass

        return self.list

    def lfv_list3(self, url):
        try:
            result = getUrl(url, timeout='30').result
            videos = common.parseDOM(result, "h2")
        except:
            return
        for video in videos:
            try:
                name = common.parseDOM(video, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = re.sub('<b>|</b>|&\sAll\sGoals|\sDownload', '', name).strip()
                name = re.sub('\s\d+\s-\s\d+\s', ' vs ', name)
                name = name.encode('utf-8')

                url = common.parseDOM(video, "a", ret="href")[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                if not ('/fullmatch/' in url or '/highlights/' in url): raise Exception()

                try: show = re.compile('/(fullmatch|highlights)/.+?/(.+?)/').findall(url)[0][1]
                except: show = '0'
                show = show.replace('-', ' ').upper()
                show = common.replaceHTMLCodes(show)
                show = show.encode('utf-8')

                plot = name.replace('-', '\n')
                if not show == '0': plot = '%s\n%s' % (show, plot)
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': '0', 'date': '0', 'genre': 'Sports', 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

class videoparts:
    def __init__(self):
        self.list = []

    def get(self, url, meta=''):
        if '/highlights/' in url: self.list = self.lfv_list2(url, meta)
        else: self.list = self.lfv_list(url, meta)
        index().videopartList(self.list)

    def lfv_list(self, url, meta):
        try:
            result = getUrl(url, timeout='30').result
            result = result.replace('<object', '<iframe').replace(' data=', ' src=')

            title = common.parseDOM(result, "h1", attrs = { "class": "title" })[0]
            title = title.split(':', 1)[-1].split('>', 1)[-1].split('<', 1)[0].strip()

            videos = common.parseDOM(result, "div", attrs = { "id": "fullvideo" })[0]
            videos = common.parseDOM(videos, "div", attrs = { "class": "et-learn-more.+?" })
        except:
            return

        for video in videos:
            try:
                lang = common.parseDOM(video, "span")[0]
                lang = lang.split("-")[-1].strip()

                if 'proxy.link=lfv*' in video:
                    import gkdecrypter
                    parts = re.compile('proxy[.]link=lfv[*](.+?)&').findall(video)
                    parts = uniqueList(parts).list
                    parts = [gkdecrypter.decrypter(198,128).decrypt(i,base64.urlsafe_b64decode('Y0ZNSENPOUhQeHdXbkR4cWJQVlU='),'ECB').split('\0')[0] for i in parts]
                elif 'data-config=' in video:
                    parts = re.findall('data-config=\"(.+)\"', video, re.I)
                    parts = [i for i in parts if any(i.startswith(x) for x in resolver().hostList)]
                else:
                    video = video.replace('"//', '"http://').replace("'//", '"http://')
                    parts = re.findall('[\'|\"](http://.+?)[\'|\"]', video, re.I)
                    parts = [i for i in parts if any(i.startswith(x) for x in resolver().hostList)]

                count = 0
                for url in parts:
                    count = count + 1

                    name = '%s (%s) %s' % (title, str(count), lang)
                    name = common.replaceHTMLCodes(name)
                    name = name.encode('utf-8')

                    url = common.replaceHTMLCodes(url)
                    if url.startswith('//') : url = 'http:' + url
                    if not any(url.startswith(i) for i in resolver().hostList): continue
                    url = url.encode('utf-8')

                    self.list.append({'name': name, 'url': url, 'meta': meta})
            except:
                pass

        return self.list

    def lfv_list2(self, url, meta):
        try:
            result = getUrl(url, timeout='30').result

            title = common.parseDOM(result, "h1", attrs = { "class": "title" })[0]
            title = title.split(':', 1)[-1].split('>', 1)[-1].split('<', 1)[0].strip()

            videos = result.replace('"//', '"http://').replace("'//", '"http://')
            videos = re.findall('[\'|\"](http://.+?)[\'|\"]', videos, re.I)
            videos = uniqueList(videos).list
            videos = [i for i in videos if any(i.startswith(x) for x in resolver().hostList)]
            videos = [i for i in videos if not i.endswith('.js')]
        except:
            return

        for video in videos:
            try:
                name = title
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = video
                url = common.replaceHTMLCodes(url)
                if url.startswith('//') : url = 'http:' + url
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'meta': meta})
            except:
                pass

        return self.list

class resolver:
    def __init__(self):
        self.vk_base = 'http://vk.com'
        self.mailru_base = 'http://videoapi.my.mail.ru'
        self.mailru_base2 = 'http://api.video.mail.ru'
        self.dailymotion_base = 'http://www.dailymotion.com'
        self.facebook_base = 'http://www.facebook.com/video'
        #self.playwire_base = 'http://cdn.playwire.com'
        self.playwire_base = 'http://config.playwire.com'
        self.youtube_base = 'http://www.youtube.com'
        self.rutube_base = 'http://rutube.ru'
        self.videa_base = 'http://videa.hu'
        self.sapo_base = 'http://videos.sapo.pt'
        self.hostList = self.host_list()

    def run(self, url):
        try:
            #print url
            if url.startswith(self.vk_base): url = self.vk(url)
            elif url.startswith(self.mailru_base): url = self.mailru(url)
            elif url.startswith(self.mailru_base2): url = self.mailru(url)
            elif url.startswith(self.dailymotion_base): url = self.dailymotion(url)
            elif url.startswith(self.facebook_base): url = self.facebook(url)
            elif url.startswith(self.playwire_base): url = self.playwire(url)
            elif url.startswith(self.youtube_base): url = self.youtube(url)
            elif url.startswith(self.rutube_base): url = self.rutube(url)
            elif url.startswith(self.videa_base): url = self.videa(url)
            elif url.startswith(self.sapo_base): url = self.sapo(url)

            if url == None: raise Exception()
            player().run(url)
            return url
        except:
            index().infoDialog(language(30304).encode("utf-8"))
            return

    def host_list(self):
        return [self.vk_base, self.mailru_base, self.mailru_base2, self.dailymotion_base, self.facebook_base, self.playwire_base, self.youtube_base, self.rutube_base, self.videa_base, self.sapo_base]

    def vk(self, url):
        try:
            if not 'hash' in url: url = self.vk_private(url)

            url = url.replace('http://', 'https://')
            result = getUrl(url).result

            hd = re.compile('url(1080|720)=(.+?)&').findall(result)
            sd = re.compile('url(540|480|360)=(.+?)&').findall(result)
            if len(hd) == 0 or not link().quality == 'true': hd = sd

            url = hd[-1][1]
            return url
        except:
            return

    def vk_private(self, url):
        try:
            urln = 'http://livefootballvideo.com/playerF/vkru/plugins/plugins_vk.php'
            oid, vid = re.compile('\/video(.*)_(.*)').findall(url)[0]

            post = {'getacc':'true'}
            result = getUrl(urln, post=urllib.urlencode(post)).result
            result = result.replace('\n','')

            username, pwd = re.compile('u=(.*)&p=(.*)&').findall(result)[0]
            ipostfield = "pass=%s&email=%s&act=login&captcha_sid=&captcha_key=&role=al_frame&_origin=http://vk.com&expire=" % (pwd, username)

            post = {'icookie':'remixlang=3',
                    'ipostfield':ipostfield,
    				'ihttpheader':'true',
    				'iagent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
    				'isslverify':'true',
    				'iheader':'true',
    				'url':'https://login.vk.com/?act=login',
    				'ipost':'true'
    				}
            result = getUrl(urln, post=urllib.urlencode(post)).result
            result = result.replace('\n','')

            h, s, l, p, hash = re.compile('Set-Cookie: h=(.*?)\;.*?Set-Cookie:\ss=(.*?);.*?Set-Cookie:\sl=(.*?);.*?Set-Cookie:\sp=(.*?);.*?Location.*?hash=(.*)').findall(result)[0]
            icookiePost = "h=%s; s=%s; p=%s; l=%s; remixlang=3" % (h,s,p,l)
            if hash[len(hash)-1] == '\r': hash = hash[:-1]
            urlPost = 'http://vk.com/login.php?act=slogin&to=&s=%s&__q_hash=%s' % (s,hash)

            post = {'icookie':icookiePost,
    				'url':urlPost,
    				'iagent':'	Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
    				'ihttpheader':'true',
    				'iheader':'true'
    				}
            result = getUrl(urln, post=urllib.urlencode(post)).result
            result = result.replace('\n','')

            remixId = re.compile('remixsid=(.*?);').findall(result)[0]
            icookiePost = "remixlang=3; remixsid=%s" % (remixId)
            ipostFieldPost = "vid=%s&act=video_embed_box&al=1&oid=%s" % (vid,oid)

            post = {'icookie':icookiePost,
    				'ipostfield':ipostFieldPost,
    				'ihttpheader':'true',
    				'iagent':'	Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
    				'iheader':'true',
    				'url':'http://vk.com/al_video.php'
    				}
            result = getUrl(urln, post=urllib.urlencode(post)).result
            result = result.replace('\n','')

            url = re.compile('iframe src=&quot;(.*?)";').findall(result)[0]
            return url
        except:
            return

    def mailru(self, url):
        try:
            url = url.replace('/my.mail.ru/video/', '/api.video.mail.ru/videos/embed/')
            url = url.replace('/videoapi.my.mail.ru/', '/api.video.mail.ru/')
            result = getUrl(url).result

            url = re.compile('metadataUrl":"(.+?)"').findall(result)[0]
            cookie = getUrl(url, output='cookie').result
            result = getUrl(url).result
            result = json.loads(result)
            result = result['videos']

            hd = [i for i in result if (i['key'] == '1080p' or i ['key'] == '720p')]
            sd = [i for i in result if not (i['key'] == '1080p' or i ['key'] == '720p')]
            if len(hd) == 0 or not link().quality == 'true': hd = sd

            url = hd[-1]['url']
            url += "|Cookie=%s" % urllib.quote(cookie)
            return url
        except:
            return

    def dailymotion(self, url):
        try:
            url = url.replace('dailymotion.com/video/', 'dailymotion.com/embed/video/')

            result = getUrl(url).result

            hd = re.compile('"stream_h264_hd_url":"(.+?)"').findall(result)
            sd = re.compile('"stream_h264_hq_url":"(.+?)"').findall(result)
            sd += re.compile('"stream_h264_url":"(.+?)"').findall(result)
            sd += re.compile('"stream_h264_ld_url":"(.+?)"').findall(result)
            if len(hd) == 0 or not link().quality == 'true': hd = sd

            url = hd[0]
            url = urllib.unquote(url).decode('utf-8').replace('\\/', '/')
            return url
        except:
            return

    def facebook(self, url):
        try:
            result = getUrl(url).result
            url = re.compile('"params","(.+?)"').findall(result)[0]
            url = re.sub(r'\\(.)', r'\1', urllib.unquote_plus(url.decode('unicode_escape')))
            url = re.compile('_src":"(.+?)"').findall(url)[0]
            return url
        except:
            return

    def playwire(self, url):
        try:
            result = getUrl(url).result
            result = json.loads(result)['content']['media']['f4m']
            result = getUrl(result).result
            baseURL = common.parseDOM(result, "baseURL")[0]
            media = common.parseDOM(result, "media", ret="url")[0]
            url = '%s/%s' % (baseURL, media)
            return url
        except:
            return

    def youtube(self, url):
        try:
            url = url.split("?v=")[-1].split("/")[-1].split("?")[0]
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
            return url
        except:
            return

    def rutube(self, url):
        try:
            result = getUrl(url).result
            url = re.compile('"m3u8": "(.+?)"').findall(result)[0]
            return url
        except:
            return

    def videa(self, url):
        try:
            url = url.rsplit("v=", 1)[-1].rsplit("-", 1)[-1]
            if url.startswith('http://'): raise Exception()
            url = 'http://videa.hu/flvplayer_get_video_xml.php?v=%s' % url

            result = getUrl(url).result
            url = re.compile('video_url="(.+?)"').findall(result)[0]
            if url.startswith('//'): url = 'http:' + url

            return url
        except:
            return

    def sapo(self, url):
        try:
            id = url.split("file=")[-1].split("sapo.pt/")[-1].split("/")[0]
            url = '%s/%s/rss2' % (self.sapo_base, id)

            result = getUrl(url).result
            url = common.parseDOM(result, "media:content", ret="url")[0]
            url = '%s%s/mov' % (url.split(id)[0], id)
            url = getUrl(url, output='geturl').result

            return url
        except:
            return

main()