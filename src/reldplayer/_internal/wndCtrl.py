from functools import cached_property
from typing import Any

try:
    import pyautogui as pg
except ImportError:  # noqa
    pg = None


class WndCtrlCom:
    """
    A base class that provides window control functionality through keyboard shortcuts.

    This class implements common window control operations like volume control, screenshots,
    and other features by simulating keyboard shortcuts using pyautogui.

    Attributes:
        wnd: The window object to control. Must be implemented by subclasses.

    Methods:
        volumeup(): Increases the volume using Ctrl + +
        volumedown(): Decreases the volume using Ctrl + -
        volumeMute(): Mutes the volume by pressing Ctrl + - multiple times
        screenshot(): Takes a screenshot using Ctrl + 0
        shake(): Shakes the window using Ctrl + 6
        virtualGps(): Opens virtual GPS using Ctrl + 7

    Note:
        This class requires pyautogui to be installed. Methods will raise RuntimeError
        if pyautogui is not available.
    """

    def _focus(self):
        try:
            self.wnd.activate()
        except Exception:
            pass

    @cached_property
    def __methods(self):
        return [name for name in dir(WndCtrlCom) if not name.startswith("_")]

    def __getattribute__(self, name: str) -> Any:
        if name.startswith("_"):
            return super().__getattribute__(name)
        if name in self.__methods:
            if pg is None:
                raise RuntimeError("pyautogui is not installed")
            assert self.wnd, "wnd is not set"
            self._focus()
            return getattr(self, name)
        return super().__getattribute__(name)

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
