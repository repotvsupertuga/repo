import xbmcaddon
import base64
base = 'Wl1RmtmSrdzL3Fmcv02bj5ibpJWZ0NXYw9yL6MHc0RHa'
tam = len(base)
basedem = base[::-1]
MainBase = base64.b64decode(basedem)
addon = xbmcaddon.Addon('script.module.mikafilmes.addon')
