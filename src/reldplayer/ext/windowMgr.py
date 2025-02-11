import typing
from pyldplayer import LDAppAttr, LDConsole
from reldplayer.ext.window import LDWindow
from pyldplayer.utils.query import QueryObj


class LDWindowMgr:
    def __init__(self, appattr: LDAppAttr = None):
        self.__console = LDConsole(appattr)

    def get(self, id: int = None, name: str = None):
        assert id is not None or name is not None, "id or name must be provided"

        for wnd in self.activeWnds():
            if id is not None and wnd.meta["id"] == id:
                return wnd
            if name is not None and wnd.meta["title"] == name:
                return wnd
        return None

    def gets(self, obj: typing.Any):
        """
        Get windows matching the given query object.

        Args:
            obj (Any): Query to match windows against. Can be:
                - str: Match window name (supports wildcards)
                - int: Match window ID
                - tuple: Match range of IDs
                - list: Match multiple IDs or names
                - QueryObj: Custom query object
                - Cond: Condition expression

        Examples:
            QueryObj("ldplayer-1")  # Match exact name
            QueryObj("ldplayer-*")  # Pattern match with wildcard
            QueryObj((0,5))         # Match IDs 0-5
            QueryObj([1,3,5])       # Match IDs 1, 3 or 5
            QueryObj(Cond("id < 5")) # Match condition
            QueryObj([1, "ldplayer-1", "*l]) # Match ID 1 or name "ldplayer-1" or regex

        Yields:
            LDWindow: Window objects matching the query
        """
        qobj = QueryObj.parse(obj)
        for wnd in self.activeWnds():
            if qobj.validate(wnd.meta):
                yield wnd

    def activeWnds(self):
        for meta in self.__console.list2():
            if meta["pid"] != -1 and meta["top_window_handle"] != 0:
                yield LDWindow(meta)
