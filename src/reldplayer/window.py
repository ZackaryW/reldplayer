import typing
import psutil
from pyldplayer._internal.model.list2meta import List2Meta
import pygetwindow
from reldplayer._internal.auto_window import AutoWindow
from reldplayer._internal.console_dispatch import ConsoleDispatchCls
from reldplayer.utils import activate_wnd, get_pid_from_hwnd
from reldplayer.quick import Console

_autoWndClsMethods = [
    x
    for x in dir(AutoWindow)
    if not x.startswith("_") and callable(getattr(AutoWindow, x))
]


class LDWindowMeta(type):
    _instances = {}
    _associated = {}

    def __call__(
        self, window: pygetwindow.Win32Window, list2meta: List2Meta
    ) -> typing.Any:
        if (window.title, window._hWnd) not in self._instances:
            self._instances[(window.title, window._hWnd)] = super().__call__(window)
            self._associated[(window.title, window._hWnd)] = list2meta
        return self._instances[(window.title, window._hWnd)]


class LDWindow(AutoWindow, metaclass=LDWindowMeta):
    def __getattribute__(self, name: str) -> typing.Any:
        if name in _autoWndClsMethods:
            activate_wnd(self.__window)
        return super().__getattribute__(name)

    def __del__(self):
        self.__class__._instances.pop(self.__hashAttr, None)
        self.__class__._associated.pop(self.__hashAttr, None)

    def __init__(self, window: pygetwindow.Win32Window) -> None:
        self.__window = window
        self.__hashAttr = (window.title, window._hWnd)

    def __hash__(self) -> int:
        return hash(self.__hashAttr)

    @property
    def window(self):
        return self.__window


class LDWindowCollection(ConsoleDispatchCls):
    def __alternative_init__(self):
        try:
            self.__console = Console.auto()
        except:  # noqa
            pass

    @classmethod
    def __check_cache(cls, meta2: List2Meta):
        for attr, meta in LDWindowMeta._associated.items():
            if meta == meta2:
                return LDWindowMeta._instances[attr]

        return None

    def __get_with_target_meta(self, meta: List2Meta):
        if ccres := self.__check_cache(meta):
            return ccres

        hwnds: typing.List[pygetwindow.Win32Window] = pygetwindow.getWindowsWithTitle(
            meta["name"]
        )
        if len(hwnds) == 1:
            return LDWindow(hwnds[0], meta)

        for hwnd in hwnds:
            pid = get_pid_from_hwnd(hwnd._hWnd)
            if not pid:
                continue

            proc = psutil.Process(pid)
            if "dnplayer.exe" in proc.exe():
                return LDWindow(hwnd, meta)

    def get(self, id: typing.Union[str, int, List2Meta], skip_list2_check: bool = True):
        if not self.__console:
            raise Exception("console not set")

        if isinstance(id, dict):
            if skip_list2_check:
                return self.__get_with_target_meta(id)
            id = id["id"]

        for meta in self.__console.list2():
            if not (meta["id"] == id or meta["name"] == id):
                continue

            if not meta["top_window_handle"]:
                return None

            return self.__get_with_target_meta(meta)
