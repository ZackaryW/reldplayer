from types import MappingProxyType
import typing
import pygetwindow as gw
from reldplayer._internal.wndCtrl import WndCtrlCom
from pyldplayer.model.list2meta import List2Meta


class LDWindowMeta(type):
    _matches: typing.ClassVar[typing.Dict[int, "LDWindow"]] = {}

    def __call__(cls, meta: List2Meta):
        id = meta["id"]
        if id in cls._matches:
            windowobj = cls._matches[id]
            pmeta = windowobj.meta
            if meta["pid"] == -1 and meta["top_window_handle"] == 0:
                obj = cls._matches.pop(id)
                del obj
                return None

            try:
                if pmeta == meta and windowobj.wnd._hWnd == meta["top_window_handle"]:
                    return windowobj
            except gw.PyGetWindowException:
                pass

            # need to refresh windowobj
            windowobj.refresh(meta)
            return windowobj

        newobj = super().__call__(meta)
        newobj.refresh(meta)
        cls._matches[id] = newobj
        return newobj


class LDWindow(WndCtrlCom, metaclass=LDWindowMeta):
    """
    A class that represents a window and provides control functionality.
    """

    def __init__(self, meta: LDWindowMeta):
        WndCtrlCom.__init__(self)
        self.__meta = meta

    @property
    def wnd(self) -> gw.Win32Window:
        return self.__wnd

    @property
    def meta(self) -> List2Meta:
        return MappingProxyType(self.__meta)

    def refresh(self, meta: List2Meta):
        assert meta["id"] == self.__meta["id"], "id mismatch"

        for wnd in gw.getAllWindows():
            wnd: gw.Win32Window
            if not wnd.title or not wnd.height or not wnd.width:
                continue

            if wnd._hWnd == meta["top_window_handle"]:
                self.__wnd = wnd
                break

        self.__meta = meta
