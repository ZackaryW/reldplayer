import typing
from reldplayer._internal.auto_window import AutoWindow
from reldplayer.batch_selector import LDBatchSelector
from reldplayer.window import LDWindow, LDWindowCollection, _autoWndClsMethods


class LDBatchWindow(AutoWindow):
    def __init__(self, selector: LDBatchSelector):
        self.__selector = None
        self.selector = selector

    @property
    def selector(self):
        return self.__selector

    @selector.setter
    def selector(self, selector: LDBatchSelector):
        self.__selector = selector
        wndc = LDWindowCollection()
        wndc._LDWindowCollection__console = self.selector._LDBatchSelector__console
        self.__wndc = wndc

    @property
    def windows(self) -> typing.Generator[LDWindow, None, None]:
        for id in self.__selector.selectedIDs:
            
            res = self.__wndc.get(id)
            if res:
                yield res


def _setup(method: str):
    def wrapper(self: LDBatchWindow, *args, **kwargs):
        ids = self.__selector.selectedIDs
        for id in ids:
            item = self.__wndc.get(id)
            if not item:
                continue
            getattr(item, method)(*args, **kwargs)

    return wrapper


for method in _autoWndClsMethods:
    setattr(LDBatchWindow, method, _setup(method))
