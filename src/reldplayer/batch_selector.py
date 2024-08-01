import typing
from pyldplayer._internal.model.list2meta import List2Meta
import re
from reldplayer._internal.console_dispatch import ConsoleDispatchCls
from reldplayer.quick import Console

_default_mapping_functions = {
    "between_id": lambda a, x, y: x <= a["id"] <= y,
    "active": lambda a: a["top_window_handle"] != 0,
    "name_pattern": lambda a, q: re.search(q, str(a["name"])),
}


class LDBatchSelector(ConsoleDispatchCls):
    def __init__(self, string: str, limit: int = -1):
        self.__query_string = string
        self.__query_limit = limit
        super().__init__()

    def __dispatch__(self):
        self.__selected = [
            matched
            for matched in self.match(
                self.__console.list2(), self.__query_string, self.__query_limit
            )
        ]

    def __alternative_init__(self):
        console = Console.auto()
        if not console.path:
            self.__selected = None
        else:
            self.__console = console
            self.__dispatch__()

    @property
    def selectedMeta(self):
        return [
            meta for meta in self.__console.list2() if meta["id"] in self.__selected
        ]

    @property
    def selectedIDs(self) -> typing.List[int]:
        return self.__selected

    @staticmethod
    def match(
        list2s: typing.List[List2Meta], querystr: str, limit: int = -1, var: str = "a"
    ):
        counter = 0
        stripped_querystr = querystr.replace(" ", "")
        for i in _default_mapping_functions:
            if i in querystr and f"{i}({var}" not in stripped_querystr:
                querystr = querystr.replace(f"{i}(", f"{i}({var},")

        for meta in list2s:
            if not eval(querystr, {var: meta, **_default_mapping_functions}):
                continue
            counter += 1
            yield meta["id"]

            if counter > limit and limit > 0:
                break
