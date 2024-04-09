
from reldplayer.utils.screen import activatewnd
from .wndMgr import WndMgr
import pyautogui as pg

class AutoGui:
    def __init__(self, wndMgr : WndMgr) -> None:
        self.__wndMgr = wndMgr
        self.__primary = None
        self.__primaryLifetime = -1

    def primaryOnly(self):
        if self.__primaryLifetime < 0:
            self.__primaryLifetime = 1
        else:
            self.__primaryLifetime +=1

    def __getScope(self):
        
        if self.__primaryLifetime > 0:
            self.__primaryLifetime -= 1
            return [self.__primary]
        else:
            return self.__wndMgr.appliedWnds.values()

    def setPrimary(self, name : str = None, id : int = None):
        res = self.__wndMgr.getWnd(name, id)
        if isinstance(res, int):
            raise ValueError(f"cannot find window with id {res}, result: {res}")
        self.__primary = res
        return self

    def volumeup(self):
        for wnd in self.__getScope():
            activatewnd(wnd)
            with pg.hold("ctrl"):
                pg.press("+")
            yield wnd

    def volumedown(self):
        for wnd in self.__getScope():
            activatewnd(wnd)
            with pg.hold("ctrl"):
                pg.press("-")
            yield wnd

    def volumeMute(self):
        for wnd in self.__getScope():
            activatewnd(wnd)
            with pg.hold("ctrl"):
                for _ in range(20):
                    pg.press("-")
            yield wnd
            
    def volumeMax(self):
        for wnd in self.__getScope():
            activatewnd(wnd)
            with pg.hold("ctrl"):
                for _ in range(20):
                    pg.press("+")
            yield wnd

    def installApkDialog(self):
        for wnd in self.__getScope():
            activatewnd(wnd)
            with pg.hold("ctrl"):
                pg.press("i")
            yield wnd

    def builtinScreenshot(self):
        for wnd in self.__getScope():
            activatewnd(wnd)
            with pg.hold("ctrl"):
                pg.press("0")
            yield wnd

    def screenshot(self):
        for wnd in self.__getScope():
            activatewnd(wnd)
            screenshot = pg.screenshot(region=(wnd.left, wnd.top, wnd.width, wnd.height))
            yield wnd, screenshot

    def shake(self):
        for wnd in self.__getScope():
            activatewnd(wnd)
            with pg.hold("ctrl"):
                pg.press("6")
            yield wnd

    def sharedFolder(self):
        for wnd in self.__getScope():
            activatewnd(wnd)
            with pg.hold("ctrl"):
                pg.press("5")
            yield wnd

    def virtualGps(self):
        for wnd in self.__getScope():
            activatewnd(wnd)
            with pg.hold("ctrl"):
                pg.press("7")
            yield wnd

    # ANCHOR primary only
    def fullscreen(self):
        if self.__primary is None:
            raise Exception("no primary window")
        
        activatewnd(self.__primary)
        pg.press("f11")

    def operationRecorder(self):
        if self.__primary is None:
            raise Exception("no primary window")
        
        activatewnd(self.__primary)
        with pg.hold("ctrl"):
            pg.press("8")

    def synchronizer(self, host = None):
        if host is None:
            host = self.__primary

        assert host, "primary not set and host not provided"

        """if children is None:
            children  = self.__wndMgr.appliedWnds.values()"""

        activatewnd(host)
        with pg.hold("ctrl"):
            pg.press("9")
            


    

        

    
        
    