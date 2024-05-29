import typing

import pyscreeze
from reldplayer.core.player import Player
import pygetwindow as gw
from zrcl4.pygetwindow import grid_orientation as _grid_orientation


class GridOrient(typing.TypedDict, total=False):
    row: int
    col: int
    maxwidth: float | None
    maxheight: float | None
    minwidth: float | None
    minheight: float | None
    monitor: int
    sleepTime: float


class ManageWindow:
    def __init__(self, player: Player):
        self.__player = player

    def active_instances(self):
        return [
            x for x in self.__player.raw_console.list2() if x["top_window_handle"] != 0
        ]

    def _get_window_handles(self, *ids):
        active_instances = self.active_instances()
        active_hwnds = {x["top_window_handle"]: x for x in active_instances}

        for wnd in gw.getAllWindows():
            wnd: gw.Win32Window
            if wnd.width <= 0 or wnd.height <= 0:
                continue

            if wnd._hWnd in active_hwnds:
                yield active_hwnds[wnd._hWnd], wnd

    def get_window(self, id: int = None):
        if id is None:
            id = self.__player._ctx.primary

        if id is None:
            raise ValueError("no selection")

        for _, wnd in self._get_window_handles(id):
            return wnd

    def get_windows(
        self, selected: typing.List[int] = None
    ) -> typing.Dict[int, gw.Win32Window]:
        if selected is None:
            selected = self.__player._ctx.selected

        ret = {}
        for meta, wnd in self._get_window_handles(*selected):
            ret[meta["id"]] = wnd

        return ret

    def gridOrientation(
        self,
        id: int | typing.List[int] | None = None,
        gridStr: str | None = None,
        **gridCfg: typing.Unpack[GridOrient],
    ):
        if isinstance(id, int):
            scope = [self.get_window(id)]
        else:
            scope = list(self.get_windows(id).values())

        if gridCfg is None:
            gridCfg = {}

        if gridStr:
            row, col = gridStr.split("X")
            gridCfg["row"] = int(row)
            gridCfg["col"] = int(col)

        return _grid_orientation(scope, **gridCfg)

    def screenshot(self, id: int | typing.List[int] | None = None):
        if isinstance(id, int):
            wnd = [self.get_window(id)]
        else:
            wnd = list(self.get_windows(id).values())

        for wnd in wnd:
            yield pyscreeze._screenshot_win32(
                region=(wnd.left, wnd.top, wnd.width, wnd.height), allScreens=True
            )
