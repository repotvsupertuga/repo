import xbmcaddon

__plugin__ = 'PornoMix'
__author__ = 'TVsupertuga'
__credits__ = 'TVsupertuga'

addon = xbmcaddon.Addon(id='plugin.video.pornomix')
rootDir = addon.getAddonInfo('path')
if rootDir.endswith(';'):
    rootDir = rootDir[:-1]

class Main:
    def __init__(self):
        self.pDialog = None
        self.run()

    def run(self):
        import videodevil
        videodevil.Main()

Main()
