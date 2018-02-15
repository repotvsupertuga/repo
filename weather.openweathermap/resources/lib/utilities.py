import math
import xbmc, xbmcaddon
__addon__ = xbmcaddon.Addon()

DAYS = { 'Mon': xbmc.getLocalizedString( 11 ),
         'Tue': xbmc.getLocalizedString( 12 ),
         'Wed': xbmc.getLocalizedString( 13 ),
         'Thu': xbmc.getLocalizedString( 14 ),
         'Fri': xbmc.getLocalizedString( 15 ),
         'Sat': xbmc.getLocalizedString( 16 ),
         'Sun': xbmc.getLocalizedString( 17 )}

# definition at http://openweathermap.org/wiki/API/Weather_Condition_Codes
# xbmc weather icons: http://forum.xbmc.org/showthread.php?tid=62261         
WEATHER_CODES = { '200' : '4',    # thunderstorm with light rain 
                  '201' : '3',    # thunderstorm with rain 
                  '202' : '3',    # thunderstorm with heavy rain 
                  '210' : '37',   # light thunderstorm 
                  '211' : '37',   # thunderstorm 
                  '212' : '37',   # heavy thunderstorm 
                  '221' : '37',   # ragged thunderstorm 
                  '230' : '4',    # thunderstorm with light drizzle 
                  '231' : '4',    # thunderstorm with drizzle 
                  '232' : '4',    # thunderstorm with heavy drizzle
                  '300' : '11',   # light intensity drizzle
                  '301' : '11',   # drizzle 
                  '302' : '11',   # heavy intensity drizzle 
                  '310' : '12',   # light intensity drizzle rain
                  '311' : '12',   # drizzle rain 
                  '312' : '12',   # heavy intensity drizzle rain
                  '321' : '10',   # shower drizzle 
                  '500' : '11',   # light rain 
                  '501' : '11',   # moderate rain 
                  '502' : '12',   # heavy intensity rain 
                  '503' : '18',   # very heavy rain 
                  '504' : '18',   # extreme rain 
                  '511' : '5',    # freezing rain 
                  '520' : '11',   # light intensity shower rain 
                  '521' : '11',   # shower rain 
                  '522' : '12',   # heavy intensity shower rain
                  '600' : '7',    # light snow 
                  '601' : '7',    # snow 
                  '602' : '7',    # heavy snow
                  '611' : '5',    # sleet 
                  '621' : '7',    # shower snow
                  '701' : '21',   # mist 
                  '711' : '22',   # smoke 
                  '721' : '21',   # haze 
                  '731' : '19',   # Sand/Dust Whirls
                  '741' : '20',   # Fog
                  '800' : '32',   # sky is clear 
                  '801' : '34',   # few clouds 
                  '802' : '28',   # scattered clouds
                  '803' : '26',   # broken clouds 
                  '804' : '26',   # overcast clouds
                  '900' : '0',    # tornado 
                  '901' : '35',   # tropical storm
                  '902' : '0',    # hurricane 
                  '903' : '25',   # cold 
                  '904' : '36',   # hot 
                  '905' : '23',   # windy 
                  '906' : '6'     # hail
                  }
                  
LANGUAGES   =  {'English' : 'en', 
                'Russian' : 'ru',
                'Italian' : 'it',
                'Spanish' : 'sp',
                'Ukrainian': 'ua',
                'German' : 'de',
                'Portuguese' : 'pt' ,
                'Romanian' : 'ro',
                'Polish' : 'pl',
                'Finnish' : 'fi',
                'Dutch' : 'nl',
                'French' : 'fr',
                'Bulgarian' : 'bg',
                'Swedish' : 'se',
                'Chinese (Traditional)' : 'zh_tw',
                'Chinese (Simple)' : 'zh_cn',
                'Turkish' : 'tr'
                }

MONTH = { 1  : xbmc.getLocalizedString(51),
          2  : xbmc.getLocalizedString(52),
          3  : xbmc.getLocalizedString(53),
          4  : xbmc.getLocalizedString(54),
          5  : xbmc.getLocalizedString(55),
          6  : xbmc.getLocalizedString(56),
          7  : xbmc.getLocalizedString(57),
          8  : xbmc.getLocalizedString(58),
          9  : xbmc.getLocalizedString(59),
          10 : xbmc.getLocalizedString(60),
          11 : xbmc.getLocalizedString(61),
          12 : xbmc.getLocalizedString(62)}

WEEKDAY = { 'Mon'  : xbmc.getLocalizedString(41),
            'Tue'  : xbmc.getLocalizedString(42),
            'Wed'  : xbmc.getLocalizedString(43),
            'Thu'  : xbmc.getLocalizedString(44),
            'Fri'  : xbmc.getLocalizedString(45),
            'Sat'  : xbmc.getLocalizedString(46),
            'Sun'  : xbmc.getLocalizedString(47)}
            
def mstobft(ms):
    if (ms < 0.3):
        return 0
    elif (ms >= 0.3) and (ms < 1.6):
        return 1
    elif (ms >= 1.6) and (ms < 3.4):
        return 2
    elif (ms >= 3.4) and (ms < 5.5):
        return 3
    elif (ms >= 5.5) and (ms < 8.0):
        return 4
    elif (ms >= 8.0) and (ms < 10.8):
        return 5
    elif (ms >= 10.8) and (ms < 13.9):
        return 6
    elif (ms >= 13.9) and (ms < 17.2):
        return 7
    elif (ms >= 17.2) and (ms < 20.8):
        return 8
    elif (ms >= 20.8) and (ms < 24.5):
        return 9
    elif (ms >= 24.5) and (ms < 28.5):
        return 10
    elif (ms >= 28.5) and (ms < 32.7):
        return 11
    elif (ms >= 32.7):
        return 12
    return ''
            
def convert_unit(unittype, input, target):
    #input value for temperature must be in C; input value for speed must be in m/s
    if unittype == 1: #temperature
        if 'C' in target:
            return int(round(input))
        if 'F' in target:
            return int(round(float(input * 1.8 + 32)))
        if 'K' in target:
            return int(round(float(input + 273.15)))
    elif unittype == 2: #speed units
        if target == "m/s":
            return int(round(input))
        if target == "km/h":
            return int(round(input * 3.6))
        if target == "mph":
            return int(round(input * 2.236))
        if target == "kn":
            return int(round(input * 1.944))
        if target == "bft":
            return mstobft(input)
        return 'na'
    return 'na'

        
def winddir(deg, format=0):
    long = __addon__.getLocalizedString(32196) + ' '
    if deg >= 12 and deg <= 34:
        wind = 'NNE'
        long = long + __addon__.getLocalizedString(32180)
        short = xbmc.getLocalizedString(72)
    elif deg >= 35 and deg <= 56:
        wind = 'NE'
        long = long + __addon__.getLocalizedString(32181)
        short = xbmc.getLocalizedString(73)
    elif deg >= 57 and deg <= 79:
        wind = 'ENE'
        long = long + __addon__.getLocalizedString(32182)
        short = xbmc.getLocalizedString(74)
    elif deg >= 80 and deg <= 101:
        wind = 'E'
        long = long + __addon__.getLocalizedString(32183)
        short = xbmc.getLocalizedString(75)
    elif deg >= 102 and deg <= 124:
        wind = 'ESE'
        long = long + __addon__.getLocalizedString(32184)
        short = xbmc.getLocalizedString(76)
    elif deg >= 125 and deg <= 146:
        wind = 'SE'
        long = long + __addon__.getLocalizedString(32185)
        short = xbmc.getLocalizedString(77)
    elif deg >= 147 and deg <= 169:
        wind = 'SSE'
        long = long + __addon__.getLocalizedString(32186)
        short = xbmc.getLocalizedString(78)
    elif deg >= 170 and deg <= 191:
        wind = 'S'
        long = long + __addon__.getLocalizedString(32187)
        short = xbmc.getLocalizedString(79)
    elif deg >= 192 and deg <= 214:
        wind = 'SSW'
        long = long + __addon__.getLocalizedString(32188)
        short = xbmc.getLocalizedString(80)
    elif deg >= 215 and deg <= 236:
        wind = 'SW'
        long = long + __addon__.getLocalizedString(32189)
        short = xbmc.getLocalizedString(81)
    elif deg >= 237 and deg <= 259:
        wind = 'WSW'
        long = long + __addon__.getLocalizedString(32190)
        short = xbmc.getLocalizedString(82)
    elif deg >= 260 and deg <= 281:
        wind = 'W'
        long = long + __addon__.getLocalizedString(32191)
        short = xbmc.getLocalizedString(83)
    elif deg >= 282 and deg <= 304:
        wind = 'WNW'
        long = long + __addon__.getLocalizedString(32192)
        short = xbmc.getLocalizedString(84)
    elif deg >= 305 and deg <= 326:
        wind = 'NW'
        long = long + __addon__.getLocalizedString(32193)
        short = xbmc.getLocalizedString(85)
    elif deg >= 327 and deg <= 349:
        wind = 'NNW'
        long = long + __addon__.getLocalizedString(32194)
        short = xbmc.getLocalizedString(86)
    else:
        wind = 'N'
        long = long + __addon__.getLocalizedString(32195)
        short = xbmc.getLocalizedString(71)
    
    if format == 0:   # short form, untranslated
        return wind
    elif format == 1: # short form, translated
        return short
    else:             # long form, translated
        return long 
    
# calculate x, y maptile and pixel coordinates
def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    
    # calc x, y value for tile url
    fxtile = float((lon_deg + 180.0) / 360.0 * n)
    fytile = float((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    
    xtile = str(int(fxtile))
    ytile = str(int(fytile))
    
    # calc x, y Pixel value in the tile
    xpx = str(int((fxtile - float(xtile)) * 256))
    ypx = str(int((fytile - float(ytile)) * 256))
    return {'x':xtile, 'y':ytile, 'xpx': xpx, 'ypx': ypx}
    
def calc_mstokmh(speed):
    return speed * 3.6

#### thanks to FrostBox @ http://forum.xbmc.org/showthread.php?p=937168#post937168

def feelslike( T=10, V=25 ):
    """ The formula to calculate the equivalent temperature related to the wind chill is:
        T(REF) = 13.12 + 0.6215 * T - 11.37 * V**0.16 + 0.3965 * T * V**0.16
        Or:
        T(REF): is the equivalent temperature in degrees Celsius
        V: is the wind speed in km/h measured at 10m height
        T: is the temperature of the air in degrees Celsius
        source: http://zpag.tripod.com/Meteo/eolien.htm
        
        getFeelsLike( tCelsius, windspeed )
    """
    FeelsLike = T
    # Wind speeds of 4 mph or less, the wind chill temperature is the same as the actual air temperature.
    if round( ( V + .0 ) / 1.609344 ) > 4:
        FeelsLike = ( 13.12 + ( 0.6215 * T ) - ( 11.37 * V**0.16 ) + ( 0.3965 * T * V**0.16 ) )
    return str( round( FeelsLike ) )


def dewpoint( Tc=0, RH=93, minRH=( 0, 0.075 )[ 0 ] ):
    """ Dewpoint from relative humidity and temperature
        If you know the relative humidity and the air temperature,
        and want to calculate the dewpoint, the formulas are as follows.
        
        getDewPoint( tCelsius, humidity )
    """
    #First, if your air temperature is in degrees Fahrenheit, then you must convert it to degrees Celsius by using the Fahrenheit to Celsius formula.
    # Tc = 5.0 / 9.0 * ( Tf - 32.0 )
    #The next step is to obtain the saturation vapor pressure(Es) using this formula as before when air temperature is known.
    Es = 6.11 * 10.0**( 7.5 * Tc / ( 237.7 + Tc ) )
    #The next step is to use the saturation vapor pressure and the relative humidity to compute the actual vapor pressure(E) of the air. This can be done with the following formula.
    #RH=relative humidity of air expressed as a percent. or except minimum(.075) humidity to abort error with math.log.
    RH = RH or minRH #0.075
    E = ( RH * Es ) / 100
    #Note: math.log( ) means to take the natural log of the variable in the parentheses
    #Now you are ready to use the following formula to obtain the dewpoint temperature.
    try:
        DewPoint = ( -430.22 + 237.7 * math.log( E ) ) / ( -math.log( E ) + 19.08 )
    except ValueError:
        #math domain error, because RH = 0%
        #return "N/A"
        DewPoint = 0 #minRH
    #Note: Due to the rounding of decimal places, your answer may be slightly different from the above answer, but it should be within two degrees.
    return str( int( DewPoint ) )
