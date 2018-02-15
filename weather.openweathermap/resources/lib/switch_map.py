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

import xbmc, xbmcgui

WEATHER_WINDOW   = xbmcgui.Window(12600)

def log(txt):
    if isinstance (txt,str):
        txt = txt.decode("utf-8")
    message = u'%s: %s' % ('weather.openweathermap Map Switch', txt)
    xbmc.log(msg=message.encode("utf-8"), level=xbmc.LOGDEBUG)
    #xbmc.log(msg=message.encode("utf-8"))

def set_property(name, value):
    WEATHER_WINDOW.setProperty(name, value)

def get_property(name):
    return WEATHER_WINDOW.getProperty(name)
    
def get_translation(num):
    if num == 0:
        return xbmc.getLocalizedString(33035) + ": " + xbmc.getLocalizedString(401)
    elif num == 1:
        return xbmc.getLocalizedString(33035) + ": " + xbmc.getLocalizedString(376)
    elif num == 2:
        return xbmc.getLocalizedString(33035) + ": " + xbmc.getLocalizedString(387)
    elif num == 3:
        return xbmc.getLocalizedString(33035) + ": " + xbmc.getLocalizedString(375)
    elif num == 4:
        return xbmc.getLocalizedString(33035) + ": " + xbmc.getLocalizedString(383)
    elif num == 5:
        return xbmc.getLocalizedString(33035) + ": Pressure" # not localized yet
    elif num == 6:
        return xbmc.getLocalizedString(33035) + ": " + xbmc.getLocalizedString(33021)

weathermaps = []
weathermaps.append(get_property('Map.Temperature')) 
weathermaps.append(get_property('Map.Rain')) 
weathermaps.append(get_property('Map.Clouds')) 
weathermaps.append(get_property('Map.Snow'))
weathermaps.append(get_property('Map.Wind'))
weathermaps.append(get_property('Map.Pressure'))
weathermaps.append(get_property('Map.Precipitation'))
            
def set_nextmap():
    for x in range(0,7):
        if get_property('Map.Weathermap') == weathermaps[x] and get_property('Map.Weathermap') != '':
            for y in range(x+1, 7):
                if weathermaps[y] != '':
                    set_property('Map.Weathermap', weathermaps[y])
                    set_property('Map.Text', get_translation(y))
                    return
            #start at the beginning
            for y in range(0, x):
                if weathermaps[y] != '':
                    set_property('Map.Weathermap', weathermaps[y])
                    set_property('Map.Text', get_translation(y))
                    return
                    
    # current map not found anymore -> happens if settings are changed
    for x in range(0,7):
        if weathermaps[x] != '':
            set_property('Map.Weathermap', weathermaps[x])
            set_property('Map.Text', get_translation(x))
            return
            
    # no map found -> no maps selected for download
    set_property('Map.Weathermap', '')
    set_property('Map.Text', xbmc.getLocalizedString(33035) + ": " + xbmc.getLocalizedString(36502))

set_nextmap()                    
log('openweathermap Switch map to: ' + get_property('Map.Weathermap'))
