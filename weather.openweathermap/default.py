# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with XBMC; see the file COPYING. If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html

import os, sys, socket, urllib2, time
# in Frodo import crashes when refreshing weather info

try:
    from PIL import Image
except: pass


#from xml.dom import minidom
from datetime import datetime
import xbmc, xbmcgui, xbmcaddon, xbmcvfs
if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson

__addon__      = xbmcaddon.Addon()
__addonname__  = __addon__.getAddonInfo('name')
__addonid__    = __addon__.getAddonInfo('id')
__version__    = __addon__.getAddonInfo('version')
__cwd__        = __addon__.getAddonInfo('path')
__resource__   = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'lib' ).encode("utf-8") ).decode("utf-8")
__settings__   = xbmcaddon.Addon(id=str(__addonid__))

sys.path.append(__resource__)

from utilities import *

# API Description can be found here: http://openweathermap.org/API#forecast
# Other Background tiles: http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
# API key is APPID=d5f83afb38a84ae215195678dd09952f
LOC_URL          = 'http://api.openweathermap.org/data/2.5/find?q=%s&type=like&mode=json&APPID=d5f83afb38a84ae215195678dd09952f'
API_URL_FORECAST = 'http://api.openweathermap.org/data/2.5/forecast/daily?id=%s&units=metric&cnt=11&mode=json&lang=%s&APPID=d5f83afb38a84ae215195678dd09952f'
API_URL_HOURLY   = 'http://api.openweathermap.org/data/2.5/forecast?id=%s&units=metric&cnt=11&mode=json&lang=%s&APPID=d5f83afb38a84ae215195678dd09952f'
API_URL_NOW      = 'http://api.openweathermap.org/data/2.5/weather?id=%s&units=metric&mode=json&lang=%s&APPID=d5f83afb38a84ae215195678dd09952f'
TILE_URL_OSM     = 'http://%s.tile.openstreetmap.org/%s/%s/%s.png' # % (a|b|c, zoom, x, y)
TILE_URL_OCM     = 'http://%s.tile.opencyclemap.org/cycle/%s/%s/%s.png' # % (a|b|c, zoom, x, y)
TILE_URL_MQ      = 'http://otile%s.mqcdn.com/tiles/1.0.0/osm/%s/%s/%s.jpg' # % (1|2|3|4, zoom, x, y)
TILE_URL_MQOA    = 'http://otile%s.mqcdn.com/tiles/1.0.0/sat/%s/%s/%s.jpg' # % (1|2|3|4, zoom, x, y)
TILE_URL_OWM     = 'http://undefined.tile.openweathermap.org/map/%s/%s/%s/%s.png' # % (clouds|precipitation|rain|pressure|wind|temp|snow, zoom, x, y)
TIME_FORMAT      = xbmc.getRegion('time').replace('%H%H','%H').replace(':%S','') #Workaround get Region doubles %H
WEATHER_ICON     = xbmc.translatePath('special://temp/weather/%s.png').decode("utf-8")
WEATHER_WINDOW   = xbmcgui.Window(12600)
MAXDAYS          = 6

#get user unit settings
if __addon__.getSetting('UnitTemperature') == '1':
    TEMPUNIT = unicode(u'\u00b0C')
elif __addon__.getSetting('UnitTemperature') == '2':
    TEMPUNIT = unicode(u'\u00b0F')
elif __addon__.getSetting('UnitTemperature') == '3':
    TEMPUNIT = 'K'
else: #fallback to system standard
    TEMPUNIT = unicode(xbmc.getRegion('tempunit'),encoding='utf-8')
    
if __addon__.getSetting('UnitWindSpeed') == '1':
    SPEEDUNIT = 'm/s'
elif __addon__.getSetting('UnitWindSpeed') == '2':
    SPEEDUNIT = 'km/h'
elif __addon__.getSetting('UnitWindSpeed') == '3':
    SPEEDUNIT = 'mph'
elif __addon__.getSetting('UnitWindSpeed') == '4':
    SPEEDUNIT = 'kn'
elif __addon__.getSetting('UnitWindSpeed') == '5':
    SPEEDUNIT = 'bft'
else: 
    SPEEDUNIT = xbmc.getRegion('speedunit')    
    
socket.setdefaulttimeout(10)

def log(txt):
    if isinstance (txt,str):
        txt = txt.decode("utf-8")
    message = u'%s: %s' % (__addonid__, txt)
    xbmc.log(msg=message.encode("utf-8"), level=xbmc.LOGDEBUG)
    #xbmc.log(msg=message.encode("utf-8"))

def set_property(name, value):
    WEATHER_WINDOW.setProperty(name, value)
    
def get_property(name):
    return WEATHER_WINDOW.getProperty(name)

def refresh_locations():
    locations = 0
    for count in range(1, 4):
        loc_name = __addon__.getSetting('Location%s' % count)
        if loc_name != '':
            locations += 1
        set_property('Location%s' % count, loc_name)
    set_property('Locations', str(locations))
    log('available locations: %s' % str(locations))

def location(loc):
    items  = []
    locs   = []
    locids = []
    log('searching for location: %s' % loc)
    query = find_location(loc)
    log('location data: %s' % query)
    data = parse_data(query)

    if data != '' and data.has_key('list') and data['list'][0]['sys']['country'] != '':
        for item in data['list']:
            listitem   = item['name'] + ' (' + item['sys']['country'] + ')'
            location   = item['name'] + ' (' + item['sys']['country'] + ')'
            locationid = str(item['id'])
            items.append(listitem)
            locs.append(location)
            locids.append(locationid)
    return items, locs, locids

def find_location(loc):
    url = LOC_URL % loc
    try:
        req = urllib2.urlopen(url)
        response = req.read()
        req.close()
    except:
        response = ''
    return response

def parse_data(reply):
    try:
        data = simplejson.loads(reply)
    except:
        log('failed to parse weather data')
        data = ''
    return data
    
# this function is used to recieve a language code compatible with openweathermap API
def get_api_lang():
# xbmc.getLanguage(xbmc.ISO_639_1, False) is not supported by older versions than gotham, i leave it for later use
#    lang = xbmc.getLanguage(xbmc.ISO_639_1, False)
#    if lang == 'zh': # for chinese, additional info is required
#        lang = xbmc.getLanguage(xbmc.ISO_639_1, True).replace('-', '_')

    default = 'en'
    lang = LANGUAGES.get(xbmc.getLanguage(), default)
    log('Language: ' + lang)
    return lang

def forecast(loc,locid):
    log('weather location: %s' % locid)
    retry = 0
    fc = ''
    while (retry < 6) and (not xbmc.abortRequested):
        now = get_weather(locid)
        if now != '':
            retry = 6
        else:
            retry += 1
            xbmc.sleep(10000)
            log('weather now download failed')
    log('now data: %s' % now)
    
    retry = 0
    while (retry < 6) and (not xbmc.abortRequested):
        fc = get_forecast(locid)
        if fc != '':
            retry = 6
        else:
            retry += 1
            xbmc.sleep(10000)
            log('weather forecast download failed')
    log('forecast data: %s' % fc)

    retry = 0
    while (retry < 6) and (not xbmc.abortRequested):
        hd = get_hourly(locid)
        if hd != '':
            retry = 6
        else:
            retry += 1
            xbmc.sleep(10000)
            log('weather hourly forecast download failed')
    log('hourly data: %s' % hd)      
    
    if now != '' and fc != '' and hd != '':
        properties(now,fc,hd,loc)
    else:
        clear()

def get_weather(locid):
    LANG_SHORT = get_api_lang()
    url = API_URL_NOW % (locid, LANG_SHORT)
    log('API URL now: ' + url)
    try:
        req = urllib2.urlopen(url)
        response = req.read()
        req.close()
    except:
        response = ''
    return response
    
def get_forecast(locid):
    LANG_SHORT = get_api_lang()
    url = API_URL_FORECAST % (locid, LANG_SHORT)
    log('API URL forecast: ' + url)
    try:
        req = urllib2.urlopen(url)
        response = req.read()
        req.close()
    except:
        response = ''
    return response

def get_hourly(locid):
    LANG_SHORT = get_api_lang()
    url = API_URL_HOURLY % (locid, LANG_SHORT)
    log('API URL hourly: ' + url)
    try:
        req = urllib2.urlopen(url)
        response = req.read()
        req.close()
    except:
        response = ''
    return response
    
def download_tile(url, filename):
    response = ''
    data = ''
    hfile = ''
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        data = response.read()
        response.close()
        log('Image downloaded from ' + url)
    except:
        data = ''
        log('Image download failed from ' + url)

    if data != '':
        try:
            hfile = open(filename, 'wb')
            hfile.write(data)
            hfile.close()
            log('Saved image ' + filename)
        except:
            log('Failed to save image ' + filename)

def create_marker(x, y, filename):
  try:
    blankfile = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'images', 'blank.png' ).encode("utf-8") ).decode("utf-8")
    markerfile = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'images', 'marker.png' ).encode("utf-8") ).decode("utf-8")
    blank = Image.open(blankfile)
    image = Image.open(filename)
    marker = Image.open(markerfile)
    width, height = marker.size
    x = int(x - width/2)
    y = int(y - height/2)
    blank.paste(image, (0,0))
    blank.paste(marker, (x,y), mask=marker)
    blank.save(filename.replace('.png','_m.png').replace('.jpg','_m.png'))
  except: pass
    
def clear():
    set_property('Current.Condition'            , 'N/A')
    set_property('Current.Temperature'          , '0')
    set_property('Current.Wind'                 , '0')
    set_property('Current.WindGust'             , '0')
    set_property('Current.WindDirection'        , 'N/A')
    set_property('Current.Humidity'             , '0')
    set_property('Current.FeelsLike'            , '0')
    set_property('Current.UVIndex'              , '0')
    set_property('Current.DewPoint'             , '0')
    set_property('Current.OutlookIcon'          , 'na.png')
    set_property('Current.FanartCode'           , 'na')
    set_property('Current.CloudCover'           , '0')
    set_property('Current.PrecipitationSnow'    , 'N/A')
    set_property('Current.PrecipitationRain'    , 'N/A')
    set_property('Today.Sunrise'                , 'N/A')
    set_property('Today.Sunset'                 , 'N/A')
    set_property('Today.AvgHighTemperature'     , '0')
    set_property('Today.AvgLowTemperature'      , '0')
    set_property('Map.Location'                 , 'na.png')
    set_property('Map.Rain'                     , 'na.png')
    set_property('Map.Temperature'              , 'na.png')
    set_property('Map.Clouds'                   , 'na.png')
    set_property('Map.Wind'                     , 'na.png')
    set_property('Map.Snow'                     , 'na.png')
    set_property('Map.Pressure'                 , 'na.png')
    set_property('Map.Precipitation'            , 'na.png')
    set_property('Map.ColorDiffuse'             , 'FFFFFFFF')
    for count in range (0, MAXDAYS + 1):
        set_property('Day%i.Title'       % count, 'N/A')
        set_property('Day%i.HighTemp'    % count, '0')
        set_property('Day%i.LowTemp'     % count, '0')
        set_property('Day%i.Outlook'     % count, 'N/A')
        set_property('Day%i.OutlookIcon' % count, 'na.png')
        set_property('Day%i.FanartCode'  % count, 'na')
        set_property('Day%i.CloudCover'  % count, '0')
        set_property('Day%i.Wind'        % count, '0')
        set_property('Day%i.Winddirection'  % count, 'N/A')
        
def properties(data_now, data_forecast, data_hourly, loc):
    # now section
    now = parse_data(data_now)
    
    windgust = ''
    if now != '' and now['wind'].has_key('gust'):
        windgust = str(calc_mstokmh(float(now['wind']['gust'])))

    if now != '' and now.has_key('rain'):
        if now['rain'].has_key('1h'):
            PrecipitationRain = unicode(now['rain']['1h']) + unicode(u'mm/1 ') + unicode(xbmc.getLocalizedString(12392))
        elif now['rain'].has_key('3h'):
            PrecipitationRain = unicode(now['rain']['3h']) + unicode(u'mm/3 ') + unicode(xbmc.getLocalizedString(12392))
        else:
            PrecipitationRain = unicode(now['rain']) + unicode(u'mm/24 ') + unicode(xbmc.getLocalizedString(12392)) #Default value unknown so far
    else: #no data provided
        PrecipitationRain = unicode(u'0mm/24 ') + unicode(xbmc.getLocalizedString(12392))
        
    if now != '' and now.has_key('snow'):
        if now['snow'].has_key('1h'):
            PrecipitationSnow = unicode(now['snow']['1h']) + unicode(u'mm/1 ') + unicode(xbmc.getLocalizedString(12392))
        elif now['snow'].has_key('3h'):
            PrecipitationSnow = unicode(now['snow']['3h']) + unicode('mm/3 ') + unicode(xbmc.getLocalizedString(12392))
        else:
            PrecipitationSnow = unicode(now['snow']) + unicode('mm/24 ') + unicode(xbmc.getLocalizedString(12392)) #Default value unknown so far
    else: #no data provided
        PrecipitationSnow = unicode(u'0mm/24 ') + unicode(xbmc.getLocalizedString(12392))
    
    # prevent crash if unknown weather codes are used
    default = 'na'
    weather_code = WEATHER_CODES.get(str(now['weather'][0]['id']), default)
        
    if now != '' and now.has_key('weather') and now.has_key('main') and now.has_key('wind') :
        set_property('Current.Location'             , loc)
        set_property('Current.Condition'            , now['weather'][0]['description'])
        set_property('Current.Temperature'          , str(round(float(now['main']['temp']))))
        set_property('Current.TempUserUnit'         , str(convert_unit(1, now['main']['temp'], TEMPUNIT)))
        set_property('Current.Wind'                 , str(calc_mstokmh(float(now['wind']['speed']))))
        set_property('Current.WindUserUnit'         , xbmc.getLocalizedString(434) % (winddir(now['wind']['deg'], 1), convert_unit(2, now['wind']['speed'], SPEEDUNIT), SPEEDUNIT))
        set_property('Current.WindGust'             , windgust)
        set_property('Current.WindDirection'        , winddir(now['wind']['deg'], 0)) # autotranslated
        #set_property('Current.WindChill'           , wind[0].attributes['chill'].value)
        set_property('Current.Humidity'             , str(now['main']['humidity']))
        #set_property('Current.Visibility'          , atmosphere[0].attributes['visibility'].value)
        set_property('Current.Pressure'             , str(now['main']['pressure']))
        set_property('Current.FeelsLike'            , feelslike(float(now['main']['temp']), calc_mstokmh(float(now['wind']['speed']))))
        set_property('Current.FeelsLikeUserUnit'    , str(convert_unit(1, float(feelslike(float(now['main']['temp']), calc_mstokmh(float(now['wind']['speed'])))), TEMPUNIT)))
        set_property('Current.DewPoint'             , dewpoint(int(round(float(now['main']['temp']))), int(now['main']['humidity'])))
        set_property('Current.DewPointUserUnit'     , str(convert_unit(1, float(dewpoint(int(round(float(now['main']['temp']))), int(now['main']['humidity']))), TEMPUNIT)))
        set_property('Current.UVIndex'              , '')
        set_property('Current.OutlookIcon'          , WEATHER_ICON % weather_code)
        set_property('Current.FanartCode'           , weather_code)
        set_property('Current.CloudCover'           , str(now['clouds']['all']) + '%') # in %
        set_property('Current.PrecipitationSnow'    , PrecipitationSnow) # in mm / x hours
        set_property('Current.PrecipitationRain'    , PrecipitationRain) # in mm / x hours
        set_property('Today.Sunrise'                , datetime.fromtimestamp(int(now['sys']['sunrise'])).strftime(TIME_FORMAT).lstrip('0'))
        set_property('Today.Sunset'                 , datetime.fromtimestamp(int(now['sys']['sunset'])).strftime(TIME_FORMAT).lstrip('0'))
        set_property('Today.AvgHighTemperature'     , str(round(float(now['main']['temp_max']))))
        set_property('Today.AvgLowTemperature'      , str(round(float(now['main']['temp_min']))))
        
    #forecast section
    fc_json = parse_data(data_forecast)
    if fc_json != '' and fc_json.has_key('list'):
        count = -1
        #skip the first entry because its today
        for item in fc_json['list'][1:]:
            count += 1
            set_property('Day%i.Title'       % count, datetime.fromtimestamp(int(item['dt'])).strftime('%A'))
            set_property('Day%i.HighTemp'    % count, str(item['temp']['max']))
            set_property('Day%i.LowTemp'     % count, str(item['temp']['min']))
            set_property('Day%i.Outlook'     % count, item['weather'][0]['description'])
            set_property('Day%i.OutlookIcon' % count, WEATHER_ICON % WEATHER_CODES[str(item['weather'][0]['id'])])
            set_property('Day%i.FanartCode'  % count, WEATHER_CODES[str(item['weather'][0]['id'])])
            set_property('Day%i.CloudCover'  % count, str(item['clouds']))
            set_property('Day%i.Wind'        % count, str(item['speed']))
            set_property('Day%i.Winddirection'  % count, winddir(int(item['deg']), 2))
            if count == MAXDAYS:
                break
    
    # this is done for skin modification - daily data
    set_property('Daily.IsFetched', 'true')
    if fc_json != '' and fc_json.has_key('list'):
        count = -1
        for item in fc_json['list']:
            
            if item.has_key('rain'):
                Precip = str(item['rain']) + ' mm'
            else:
                Precip = '0 mm'
        
            odatetime = datetime.fromtimestamp(int(item['dt']))
            count += 1
            set_property('Daily.%i.ShortDay'       % count, WEEKDAY[odatetime.strftime('%a')]) # note formatstring %u (weekday as int) leads to formatstring error
            set_property('Daily.%i.ShortDate'      % count, odatetime.strftime('%d') + ' ' + MONTH[int(odatetime.strftime('%m'))])
            set_property('Daily.%i.HighTemperature'    % count, str(convert_unit(1, item['temp']['max'], TEMPUNIT)) + ' ' + TEMPUNIT)
            set_property('Daily.%i.LowTemperature'     % count, str(convert_unit(1, item['temp']['min'], TEMPUNIT)) + ' ' + TEMPUNIT)
            set_property('Daily.%i.Outlook'     % count, item['weather'][0]['description'])
            set_property('Daily.%i.OutlookIcon' % count, WEATHER_ICON % WEATHER_CODES[str(item['weather'][0]['id'])])
            set_property('Daily.%i.FanartCode'  % count, WEATHER_CODES[str(item['weather'][0]['id'])])
            set_property('Daily.%i.CloudCover'  % count, str(item['clouds']))
            set_property('Daily.%i.WindSpeed'   % count, str(convert_unit(2, item['speed'], SPEEDUNIT))  + ' ' + SPEEDUNIT)
            set_property('Daily.%i.Winddirection'  % count, winddir(int(item['deg']), 2))
            set_property('Daily.%i.Precipitation'  % count, Precip)

    # this is done for skin modification - hourly data
    set_property('Hourly.IsFetched', 'true')
    hd_json = parse_data(data_hourly)
    if hd_json != '' and hd_json.has_key('list'):
        count = 0
        maxcount = int(hd_json['cnt']);
        log('Hourly Data Sets ' + str(maxcount));
        
        if maxcount > 12:
            maxcount = 12
        
        for item in hd_json['list']:
            
            #if item.has_key('rain'):
            #    Precip = str(item['rain']) + ' mm'
            #else:
            #    Precip = '0 mm'
        
            odatetime = datetime.fromtimestamp(int(item['dt']))
            count += 1
            set_property('Hourly.%i.Time'       % count, odatetime.strftime('%H') + ':00')
            set_property('Hourly.%i.ShortDate'      % count, odatetime.strftime('%d') + ' ' + MONTH[int(odatetime.strftime('%m'))])
            set_property('Hourly.%i.Temperature'    % count, str(convert_unit(1, item['main']['temp'], TEMPUNIT)) + ' ' + TEMPUNIT)
            set_property('Hourly.%i.FeelsLike'     % count, str(convert_unit(1, float(feelslike(float(item['main']['temp']), calc_mstokmh(float(item['wind']['speed'])))), TEMPUNIT)) + ' ' + TEMPUNIT)
            set_property('Hourly.%i.Humidity'  % count, str(item['main']['humidity']) + '%')
            set_property('Hourly.%i.Outlook'     % count, item['weather'][0]['description'])
            set_property('Hourly.%i.OutlookIcon' % count, WEATHER_ICON % WEATHER_CODES[str(item['weather'][0]['id'])])
            #set_property('Hourly.%i.FanartCode'  % count, WEATHER_CODES[str(item['weather'][0]['id'])])
            set_property('Hourly.%i.WindSpeed'   % count, str(convert_unit(2, item['wind']['speed'], SPEEDUNIT))  + ' ' + SPEEDUNIT)
            set_property('Hourly.%i.Winddirection'  % count, winddir(int(item['wind']['deg']), 2))
            #set_property('Hourly.%i.Precipitation'  % count, Precip)

            if count == maxcount:
                break
    
    #Download Maps
    zoom = int(__addon__.getSetting('Zoom'))
    # Workaround: MapQuest Open Aerial supports only 11 zoom levels
    if int(zoom) > 11 and __addon__.getSetting('BackgroundProvider') == '3':
        zoom = 11
        log('Zoomlevel fallback to 11 because if MapQuest Open Aerial')
    
    lon = float(now['coord']['lon'])
    lat = float(now['coord']['lat'])
    log('Lon: ' + str(lon) + ' Lat: ' + str(lat))
    tile = deg2num(lat, lon, zoom)
    log('Tile-X: ' + tile['x'] + ' Tile-Y: ' + tile['y'] + ' Tile-Xpx: ' + tile['xpx'] + ' Tile-Ypx: ' + tile['ypx'])
    update_time = 21600 # Allow only downloading every 6 hours to prevent too much server load
    
    # Create nessesary folder
    mapdir = xbmc.translatePath('special://profile/addon_data/%s/%s' % (__addonid__, now['id']))
    if not xbmcvfs.exists(mapdir):
        xbmcvfs.mkdir(mapdir)
        log('Location directory %s created' % now['id'])
        
    # Download Background Tile
    MapProvider = __addon__.getSetting('BackgroundProvider')
    log('Map Provider: ' + MapProvider)
    if MapProvider == '1': #OpenCycleMap
        filename = xbmc.translatePath('special://profile/addon_data/%s/%s/%s_%s_ocm.png' % (__addonid__, now['id'], zoom, 'location'))
        url = TILE_URL_OCM % ('a', zoom, tile['x'], tile['y'])
    elif MapProvider == '2': #MapQuest
        filename = xbmc.translatePath('special://profile/addon_data/%s/%s/%s_%s_mq.jpg' % (__addonid__, now['id'], zoom, 'location'))
        url = TILE_URL_MQ % ('1', zoom, tile['x'], tile['y'])
    elif MapProvider == '3': #MapQuest Open Aerial
        filename = xbmc.translatePath('special://profile/addon_data/%s/%s/%s_%s_mqoa.jpg' % (__addonid__, now['id'], zoom, 'location'))
        url = TILE_URL_MQOA % ('1', zoom, tile['x'], tile['y'])
    else: #use openstreetmap as default
        filename = xbmc.translatePath('special://profile/addon_data/%s/%s/%s_%s_osm.png' % (__addonid__, now['id'], zoom, 'location'))
        url = TILE_URL_OSM % ('a', zoom, tile['x'], tile['y'])

    if not xbmcvfs.exists(filename):      
        download_tile(url, filename)
    
    if __addon__.getSetting('AddMarker') == 'true':
        if not xbmcvfs.exists(filename.replace('.png','_m.png').replace('.jpg','_m.png')):
            create_marker(int(tile['xpx']), int(tile['ypx']), filename)
        set_property('Map.Location', filename.replace('.png','_m.png').replace('.jpg','_m.png'))
        #set_property('Current.OutlookIcon', filename.replace('.png','_m.png')) # Test Code
    else:
        set_property('Map.Location', filename)
        #set_property('Current.OutlookIcon', filename) # Test Code
        
    if __addon__.getSetting('TempMap') == 'true':
        # Download Temperature Tile from openweathermap
        filename = xbmc.translatePath('special://profile/addon_data/%s/%s/%s_%s.png' % (__addonid__, now['id'], zoom, 'temp'))
        if not xbmcvfs.exists(filename) or int(time.time()) - int(os.stat(filename).st_mtime) > update_time:
            xbmcvfs.delete(filename)
            url = TILE_URL_OWM % ('temp', zoom, tile['x'], tile['y']) # % (clouds|precipitation|rain|pressure|wind|temp|snow, zoom, x, y)
            download_tile(url, filename)
        set_property('Map.Temperature', filename)
        set_property('Map.Weathermap', filename)
        set_property('Map.Text', xbmc.getLocalizedString(33035) + ": " + xbmc.getLocalizedString(401))
    else:
        set_property('Map.Temperature', '')

    if __addon__.getSetting('RainMap') == 'true':
        # Download Rain Tile from openweathermap
        filename = xbmc.translatePath('special://profile/addon_data/%s/%s/%s_%s.png' % (__addonid__, now['id'], zoom, 'rain'))
        if not xbmcvfs.exists(filename) or int(time.time()) - int(os.stat(filename).st_mtime) > update_time:    
            xbmcvfs.delete(filename)
            url = TILE_URL_OWM % ('rain', zoom, tile['x'], tile['y']) # % (clouds|precipitation|rain|pressure|wind|temp|snow, zoom, x, y)
            download_tile(url, filename)
        set_property('Map.Rain', filename)
        if get_property('Map.Weathermap') == '':
            set_property('Map.Weathermap', filename)
            set_property('Map.Text', xbmc.getLocalizedString(33035) + ": " + xbmc.getLocalizedString(376))
    else:
        set_property('Map.Rain', '')
    
    if __addon__.getSetting('CloudsMap') == 'true':    
        # Download Clouds Tile from openweathermap
        filename = xbmc.translatePath('special://profile/addon_data/%s/%s/%s_%s.png' % (__addonid__, now['id'], zoom, 'clouds'))
        if not xbmcvfs.exists(filename) or int(time.time()) - int(os.stat(filename).st_mtime) > update_time:
            xbmcvfs.delete(filename)
            url = TILE_URL_OWM % ('clouds', zoom, tile['x'], tile['y']) # % (clouds|precipitation|rain|pressure|wind|temp|snow, zoom, x, y)
            download_tile(url, filename)
        set_property('Map.Clouds', filename)
        if get_property('Map.Weathermap') == '':
            set_property('Map.Weathermap', filename)
            set_property('Map.Text', xbmc.getLocalizedString(33035) + ": " + xbmc.getLocalizedString(387))
    else:
        set_property('Map.Clouds', '')
        
    if __addon__.getSetting('SnowMap') == 'true':
        # Download Snow Tile from openweathermap
        filename = xbmc.translatePath('special://profile/addon_data/%s/%s/%s_%s.png' % (__addonid__, now['id'], zoom, 'snow'))
        if not xbmcvfs.exists(filename) or int(time.time()) - int(os.stat(filename).st_mtime) > update_time:
            xbmcvfs.delete(filename)
            url = TILE_URL_OWM % ('snow', zoom, tile['x'], tile['y']) # % (clouds|precipitation|rain|pressure|wind|temp|snow, zoom, x, y)
            download_tile(url, filename)
        set_property('Map.Snow', filename)
        if get_property('Map.Weathermap') == '':
            set_property('Map.Weathermap', filename)
            set_property('Map.Text', xbmc.getLocalizedString(33035) + ": " + xbmc.getLocalizedString(375))
    else:
        set_property('Map.Snow', '')

    if __addon__.getSetting('WindMap') == 'true':
        # Download Wind Tile from openweathermap
        filename = xbmc.translatePath('special://profile/addon_data/%s/%s/%s_%s.png' % (__addonid__, now['id'], zoom, 'wind'))
        if not xbmcvfs.exists(filename) or int(time.time()) - int(os.stat(filename).st_mtime) > update_time:
            xbmcvfs.delete(filename)
            url = TILE_URL_OWM % ('wind', zoom, tile['x'], tile['y']) # % (clouds|precipitation|rain|pressure|wind|temp|snow, zoom, x, y)
            download_tile(url, filename)
        set_property('Map.Wind', filename)
        if get_property('Map.Weathermap') == '':
            set_property('Map.Weathermap', filename)
            set_property('Map.Text', xbmc.getLocalizedString(33035) + ": " + xbmc.getLocalizedString(383))
    else:
        set_property('Map.Wind', '')

    if __addon__.getSetting('PressureMap') == 'true':
        # Download Pressure Tile from openweathermap
        filename = xbmc.translatePath('special://profile/addon_data/%s/%s/%s_%s.png' % (__addonid__, now['id'], zoom, 'pressure'))
        if not xbmcvfs.exists(filename) or int(time.time()) - int(os.stat(filename).st_mtime) > update_time:
            xbmcvfs.delete(filename)
            url = TILE_URL_OWM % ('pressure', zoom, tile['x'], tile['y']) # % (clouds|precipitation|rain|pressure|wind|temp|snow, zoom, x, y)
            download_tile(url, filename)
        set_property('Map.Pressure', filename)
        if get_property('Map.Weathermap') == '':
            set_property('Map.Weathermap', filename)
            set_property('Map.Text', xbmc.getLocalizedString(33035) + ": Pressure")
    else:
        set_property('Map.Pressure', '')
        
    if __addon__.getSetting('PrecipitationMap') == 'true':
        # Download Precipitation Tile from openweathermap
        filename = xbmc.translatePath('special://profile/addon_data/%s/%s/%s_%s.png' % (__addonid__, now['id'], zoom, 'precipitation'))
        if not xbmcvfs.exists(filename) or int(time.time()) - int(os.stat(filename).st_mtime) > update_time:
            xbmcvfs.delete(filename)
            url = TILE_URL_OWM % ('precipitation', zoom, tile['x'], tile['y']) # % (clouds|precipitation|rain|pressure|wind|temp|snow, zoom, x, y)
            download_tile(url, filename)
        set_property('Map.Precipitation', filename)
        if get_property('Map.Weathermap') == '':
            set_property('Map.Weathermap', filename)
            set_property('Map.Text', xbmc.getLocalizedString(33035) + ": " + xbmc.getLocalizedString(33021))
    else:
        set_property('Map.Precipitation', '')

    # calculate transparency
    colordiffuse = hex(255 - int(float(__addon__.getSetting('OverlayTransparency')) / 100 * 255)) + 'FFFFFF'
    log('ColorDiffuse: ' + colordiffuse)
    set_property('Map.ColorDiffuse', colordiffuse)
    
log('version %s started: %s' % (__version__, sys.argv))

set_property('WeatherProvider', __addonname__)
set_property('WeatherProviderLogo', xbmc.translatePath(os.path.join(__cwd__, 'resources', 'banner.png')))
set_property('TempUserUnit', TEMPUNIT)
set_property('SpeedUserUnit', SPEEDUNIT)
log('Temp unit: ' + TEMPUNIT)
log('Speed unit: ' + SPEEDUNIT)
xbmc.translatePath( os.path.join( __cwd__, 'resources', 'lib' ).encode("utf-8") ).decode("utf-8")
set_property('ScriptSwitchMap', xbmc.translatePath( os.path.join( __cwd__, 'resources', 'lib', 'switch_map.py' ).encode("utf-8") ).decode("utf-8"))
set_property('Alerts.Count', '')

if sys.argv[1].startswith('Location'):
    keyboard = xbmc.Keyboard('', xbmc.getLocalizedString(14024), False)
    keyboard.doModal()
    if (keyboard.isConfirmed() and keyboard.getText() != ''):
        text = keyboard.getText()
        items, locs, locids = location(text)
        dialog = xbmcgui.Dialog()
        if locs != []:
            selected = dialog.select(xbmc.getLocalizedString(396), items)
            if selected != -1:
                __addon__.setSetting(sys.argv[1], locs[selected])
                __addon__.setSetting(sys.argv[1] + 'id', locids[selected])
                log('selected location: %s' % locs[selected])
        else:
            dialog.ok(__addonname__, xbmc.getLocalizedString(284))
else:
    location = __addon__.getSetting('Location%s' % sys.argv[1])
    locationid = __addon__.getSetting('Location%sid' % sys.argv[1])
    if (locationid == '') and (sys.argv[1] != '1'):
        location = __addon__.getSetting('Location1')
        locationid = __addon__.getSetting('Location1id')
        log('trying location 1 instead')
    if not locationid == '':
        forecast(location, locationid)
    else:
        log('no location found, opening setting window')
        __settings__.openSettings()
        location = __addon__.getSetting('Location1')
        locationid = __addon__.getSetting('Location1id')
        if not locationid == '':
            forecast(location, locationid)
        else:
            clear()
    refresh_locations()

log('finished')
