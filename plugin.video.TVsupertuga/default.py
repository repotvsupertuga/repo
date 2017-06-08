import urlparse,sys,re
import urllib, urllib2
from urlparse import parse_qsl
import requests
import xml.etree.ElementTree as ET
import xbmcaddon, os



params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

action = params.get('action')

content = params.get('content')

name = params.get('name')

url = params.get('url')

image = params.get('image')

fanart = params.get('fanart')

addonPath = xbmcaddon.Addon().getAddonInfo("path")


def getVersion():
	req = urllib.urlopen("http://bit.ly/penospathjoinaddonPathpenospathjoinaddonPath").read()
	print "req.version = " + req 
	if req == None:
		return 0
	else:
		return int(req)

def update():
	from resources.lib.indexers import TVsupertuga
	print "TVsupertuga.version = " + str(TVsupertuga.version)
	print "gitTVsupertuga.version = " + str(getVersion())
	if TVsupertuga.version < getVersion():
		req = urllib.urlopen("http://bit.ly/gitTVsupertugagetVersiongitTVsupertugagetVersion").read()
		print "code got, updating NOW"
		if req == None:
			print "Something went wrong!"
		else:
			print "TVsupertugafile.path = " + os.path.join(addonPath, "resources", "lib", "indexers", "TVsupertuga.py")
			with open(os.path.join(addonPath, "resources", "lib", "indexers", "TVsupertuga.py"), "wb") as filewriter:
				filewriter.write(req)

update()
if action == None:
	from resources.lib.indexers import TVsupertuga
	TVsupertuga.indexer().root()

elif action == 'directory':
	from resources.lib.indexers import TVsupertuga
	TVsupertuga.indexer().get(url)

elif action == 'qdirectory':
	from resources.lib.indexers import TVsupertuga
	TVsupertuga.indexer().getq(url)

elif action == 'xdirectory':
	from resources.lib.indexers import TVsupertuga
	TVsupertuga.indexer().getx(url)

elif action == 'developer':
	from resources.lib.indexers import TVsupertuga
	TVsupertuga.indexer().developer()

elif action == 'tvtuner':
	from resources.lib.indexers import TVsupertuga
	TVsupertuga.indexer().tvtuner(url)

elif 'youtube' in str(action):
	from resources.lib.indexers import TVsupertuga
	TVsupertuga.indexer().youtube(url, action)

elif action == 'play':
	from resources.lib.indexers import TVsupertuga
	TVsupertuga.player().play(url, content)

elif action == 'browser':
	from resources.lib.indexers import TVsupertuga
	TVsupertuga.resolver().browser(url)

elif action == 'search':
	from resources.lib.indexers import TVsupertuga
	TVsupertuga.indexer().search()

elif action == 'addSearch':
	from resources.lib.indexers import TVsupertuga
	TVsupertuga.indexer().addSearch(url)

elif action == 'delSearch':
	from resources.lib.indexers import TVsupertuga
	TVsupertuga.indexer().delSearch()

elif action == 'queueItem':
	from resources.lib.modules import control
	control.queueItem()

elif action == 'openSettings':
	from resources.lib.modules import control
	control.openSettings()

elif action == 'urlresolverSettings':
	from resources.lib.modules import control
	control.openSettings(id='script.module.urlresolver')

elif action == 'addView':
	from resources.lib.modules import views
	views.addView(content)

elif action == 'downloader':
	from resources.lib.modules import downloader
	downloader.downloader()

elif action == 'addDownload':
	from resources.lib.modules import downloader
	downloader.addDownload(name,url,image)

elif action == 'removeDownload':
	from resources.lib.modules import downloader
	downloader.removeDownload(url)

elif action == 'startDownload':
	from resources.lib.modules import downloader
	downloader.startDownload()

elif action == 'startDownloadThread':
	from resources.lib.modules import downloader
	downloader.startDownloadThread()

elif action == 'stopDownload':
	from resources.lib.modules import downloader
	downloader.stopDownload()

elif action == 'statusDownload':
	from resources.lib.modules import downloader
	downloader.statusDownload()

elif action == 'trailer':
	from resources.lib.modules import trailer
	trailer.trailer().play(name)

elif action == 'clearCache':
	from resources.lib.modules import cache
	cache.clear()