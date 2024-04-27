from contextlib import contextmanager
from functools import cache
import functools
import inspect
from typing import Any
import pyscreeze
from ..com.config import Config
from ..com.sync import Synchronizer
from ..com.wndmgr import WndMgr
from zro2.pygetwindow import activate_wnd
import pyautogui as pg
import pygetwindow as gw


class InstanceQuick:
    __get_wndmgr__: WndMgr
    __get_config__: Config
    __get_synchronizer__: Synchronizer

    __ignore_counter: int = 0

    @property
    def __ignore_constraint(self):
        return self.__ignore_counter > 0

    @contextmanager
    def ignorePrimaryRestriction(self):
        try:
            self.__ignore_counter += 1
            yield
        finally:
            self.__ignore_counter -= 1

    def __loopover(self, name: str):
        currPrimary = self.__get_synchronizer__.currentPrimary
        if (
            currPrimary is None
            or name.lower() not in self.__get_config__.INSTANCE_GUI_PRIMARY_ONLYS
            or self.__ignore_constraint
        ):
            yield from self.__get_wndmgr__.getWndsOfInterest()
        else:
            primaryWnd = self.__get_wndmgr__.getWnd(currPrimary)  # type: ignore
            yield primaryWnd

    @cache
    def __checkFuncNeedWnd(self, func):
        return "wnd" in inspect.signature(func).parameters

    def __getattribute__(self, name: str) -> Any:
        if name.startswith("_"):
            return super().__getattribute__(name)

        if name in ["ignorePrimaryRestriction"]:
            return super().__getattribute__(name)

        def _wrapOver(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                prepedArgs = inspect.getcallargs(func, *args, **kwargs)
                if "wnd" in prepedArgs and prepedArgs["wnd"] is not None:
                    return func(*args, **kwargs)

                for wnd in self.__loopover(name):
                    activate_wnd(wnd)
                    if self.__checkFuncNeedWnd(func):
                        kwargs["wnd"] = wnd
                    res = func(*args, **kwargs)
                    if res is not None:
                        return res

            return wrapper

        f = super().__getattribute__(name)
        return _wrapOver(f)

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

    def fullscreen(self, wnd: gw.Window | None = None):
        pg.press("f11")

    def operationRecorder(self):
        with pg.hold("ctrl"):
            pg.press("8")

    def synchronizer(self):
        with pg.hold("ctrl"):
            pg.press("9")

    # OTHERS
    @contextmanager
    def settings(self, wnd: gw.Window | None = None):
        try:
            from .._internal.b64 import setting_icon
            from .._internal.utils import base64_to_image

            assert wnd is not None
            img = base64_to_image(setting_icon)
            res = pyscreeze.locateOnScreen(
                img,
                region=(wnd.left, wnd.top, wnd.width, wnd.height),  # type: ignore
            )  # type: ignore

            wnd.maximize()
            from reldplayer.submod.setting_gui import SettingGUi

            if not res:
                return None

            pg.moveTo(pyscreeze.center(res))
            pg.click()
            yield SettingGUi(wnd)
        finally:
            pass