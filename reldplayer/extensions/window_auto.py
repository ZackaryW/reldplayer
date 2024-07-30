from time import sleep
from typing import Any
from reldplayer.core.player import Player
import pygetwindow as gw
from zrcl4.pygetwindow import activate_wnd
import pyautogui as pg


class WindowAuto:

    def __init__(self, player: Player):
        self.__player = player

    def __getattribute__(self, name: str) -> Any:
        if name.startswith("_") or not self.__player._ctx:
            return super().__getattribute__(name)

        sfunc = super().__getattribute__(name)
        if not callable(sfunc):
            return sfunc

        if (
            self.__player._config.window_auto_restriction
            and name in self.__player._config.window_auto_primary_onlys
        ):
            targets = [self.__player.manage_window.get_window()]
        else:
            targets = list(self.__player.manage_window.get_windows().values())

        for target in targets:
            target: gw.Win32Window
            activate_wnd(target)
            sfunc()
            sleep(self.__player._config.SYNC_DELAY)

    # ANCHOR actual implementations
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
