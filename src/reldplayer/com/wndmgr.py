from .._internal.i import InstanceMeta
from ..com.sync import Synchronizer
from ..com.rawconsole import RawConsole
import typing
import pygetwindow as gw
from zro2.typing import is_valid_typeddict
from zro2.pygetwindow import grid_orientation as _grid_orientation
from PIL.Image import Image


class GridOrient(typing.TypedDict, total=False):
    row: int
    col: int
    maxwidth: float | None
    maxheight: float | None
    minwidth: float | None
    minheight: float | None
    monitor: int
    sleepTime: float


class WndMgr:
    __get_rawconsole__: RawConsole
    __get_synchronizer__: Synchronizer

    __internal_wnd_mapping: typing.Dict[int, gw.Window] = {}

    @typing.overload
    def getWnd(self, instance: int) -> gw.Window: ...

    @typing.overload
    def getWnd(self, instance: InstanceMeta) -> gw.Window: ...

    def getWnd(self, instance: typing.Union[InstanceMeta, int]) -> gw.Window | None:
        if isinstance(instance, dict) and is_valid_typeddict(instance, InstanceMeta):
            wndid = instance["top_window_handle"]
        elif isinstance(instance, int):
            insmeta = self.__get_rawconsole__.get(instance)  # type: ignore
            if not insmeta:
                raise ValueError(f"instance {instance} not found")
            wndid = insmeta["top_window_handle"]
        else:
            raise TypeError(f"instance should be dict or int, not {type(instance)}")

        if wndid == 0:
            return None

        for sid, snd in self.__internal_wnd_mapping.items():
            if sid == wndid and snd.isActive:
                return snd

        for awnd in gw.getAllWindows():
            if awnd._hWnd == wndid:
                self.__internal_wnd_mapping[wndid] = awnd
                return awnd

        return None

    def getAllActiveWnds(self):
        list2meta = self.__get_rawconsole__.list2()
        return [self.getWnd(i) for i in list2meta if i["top_window_handle"] != 0]

    def getAllActiveIds(self):
        return [
            i["id"]
            for i in self.__get_rawconsole__.list2()
            if i["top_window_handle"] != 0
        ]

    def getWndsOfInterest(self, id: int | typing.List[int] | None = None):
        if id:
            scope = [id] if isinstance(id, int) else id
        elif self.__get_synchronizer__.currentSync:
            scope = self.__get_synchronizer__.currentSync
        else:
            scope = self.getAllActiveIds()

        return [self.getWnd(i) for i in scope]

    def resize(
        self,
        id: int | typing.List[int] | None = None,
        width: float | None = None,
        height: float | None = None,
    ):
        for wnd in self.getWndsOfInterest(id):
            if not wnd:
                continue

            wnd.resize(width if width else wnd.width, height if height else wnd.height)

    def gridOrientation(
        self,
        id: int | typing.List[int] | None = None,
        gridStr: str | None = None,
        **gridCfg: typing.Unpack[GridOrient],
    ):
        scope = self.getWndsOfInterest(id)
        if gridCfg is None:
            gridCfg = {}

        if gridStr:
            row, col = gridStr.split("X")
            gridCfg["row"] = int(row)
            gridCfg["col"] = int(col)

        return _grid_orientation(scope, **gridCfg)

    def screenshotGenerator(self, id: int | typing.List[int] | None = None):
        import pyscreeze

        scope = self.getWndsOfInterest(id)
        for wnd in scope:
            if not wnd:
                continue
            res = pyscreeze.screenshot(
                region=(int(wnd.left), int(wnd.top), int(wnd.width), int(wnd.height))
            )

            yield res, wnd

    def screenshot(
        self, id: int | typing.List[int] | None = None
    ) -> typing.Union[Image, typing.List[Image]]:
        res = []
        for img, wnd in self.screenshotGenerator(id):
            img: Image
            res.append(img)
        return res if len(res) > 1 else res[0]

