import typing
import pygetwindow as gw
from reldplayer.main import ReLDPlayer
from reldplayer.utils.screen import gridOrientation

class WndMgr:
    def __init__(self, ldplayer : ReLDPlayer) -> None:
        self.__player = ldplayer
        self.__rawcon = self.__player.rawconsole

    def getWnd(self, name : str = None, id : int = None):
        idict = self.__rawcon.get(name or id)
        if not idict:
            return -1
        if idict["top_window_handle"] == 0:
            return -2
        
        for w in gw.getAllWindows():
            w : gw.Window
            if w._hWnd == idict["top_window_handle"]:
                return w

    def batchGetWnd(self, query : typing.Union[str, list])-> typing.Dict[str, gw.Window]:
        ret = {}
        if isinstance(query, str):
            matched = self.__rawcon.query(query)
        else:
            matched = [
                item for item in self.__rawcon.list2() if item["name"] in query or item["id"] in query
            ]

        for w in gw.getAllWindows():
            w : gw.Window
            for i in matched:
                if w._hWnd == i["top_window_handle"]:
                    ret[i["name"]] = w
    
        return ret

    @property
    def allOpenedWnds(self):
        ret = {}

        instances = [w for w in self.__rawcon.list2()
                if w["top_window_handle"] != 0    
        ]
        
        for instance in instances:
            ret[instance["name"]] = gw.Window(instance["top_window_handle"])
        
        return ret
    
    @property
    def appliedWnds(self):
        return self.batchGetWnd(self.__player.currentApplied)

    def resize(self, width : float =None, height : float = None, scope =None):
        if scope is None:
            scope = self.batchGetWnd(self.__player.currentApplied).values()

        for w in scope:
            newwidth = width if width is not None else w.width
            newheight = height if height is not None else w.height
            w.resizeTo(newwidth, newheight)

    def gridOrientation(
        self, 
        row : int, 
        col : int, 
        maxwidth : float = None,
        maxheight : float = None,
        minwidth : float = None,
        minheight : float = None,
        monitor : int = 0,
        scope = None
    ):
        if scope is None:
            scope: typing.dict_values[str, gw.Win32Window] = self.batchGetWnd(self.__player.currentApplied).values()  

        return gridOrientation(
            scope, row, col, maxwidth, maxheight, minwidth, minheight, monitor
        )


    def quickGrid(self, gridStr : str, monitor = 0, scope = None):
        return self.gridOrientation(
            *[int(x) for x in gridStr.split("X")], scope=scope, monitor=monitor
        )
    
    