import pyautogui as pg


class AutoWindow:
    def volumeup(self):
        with pg.hold("ctrl"):
            pg.press("+")

    def volumedown(self):
        with pg.hold("ctrl"):
            pg.press("-")

    def volumeMute(self):
        with pg.hold("ctrl"):
            for _ in range(20):
                pg.press("-")

    def screenshot(self):
        with pg.hold("ctrl"):
            pg.press("0")

    def shake(self):
        with pg.hold("ctrl"):
            pg.press("6")

    def virtualGps(self):
        with pg.hold("ctrl"):
            pg.press("7")

    # ANCHOR primary only
    def volumeMax(self):
        with pg.hold("ctrl"):
            for _ in range(20):
                pg.press("+")

    def installApkDialog(self):
        with pg.hold("ctrl"):
            pg.press("i")

    def sharedFolder(self):
        with pg.hold("ctrl"):
            pg.press("5")

    def fullscreen(self):
        pg.press("f11")

    def operationRecorder(self):
        with pg.hold("ctrl"):
            pg.press("8")

    def synchronizer(self):
        with pg.hold("ctrl"):
            pg.press("9")
