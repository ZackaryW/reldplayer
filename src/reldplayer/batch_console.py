from time import sleep
from pyldplayer._internal.iconsole import IConsole
from reldplayer.quick import Console
import inspect
from reldplayer.batch_selector import LDBatchSelector

_all_methods = [
    method
    for method in dir(IConsole)
    if callable((methodobj := getattr(IConsole, method))) and not method.startswith("_")
]

_batchable_methods = [
    method
    for method in _all_methods
    if "name" in (params := inspect.signature(methodobj).parameters)
    and "index" in params
]


class LDBatchConsole(IConsole):
    INTERVAL_BETWEEN_EACH_TRIGGER: int = 2
    NON_BATCHABLEs = set(_all_methods) - set(_batchable_methods)

    def __init__(self, selector: LDBatchSelector):
        self.__selector = selector
        self.__console = self.__selector._LDBatchSelector__console
        assert isinstance(self.__console, Console), "Uninited selector"

    @property
    def wrappedConsole(self):
        return self.__console


def batchable_method(method: str):
    def wrapper(self: LDBatchConsole, *args, **kwargs):
        func = getattr(self._LDBatchConsole__console, method)

        params = inspect.signature(func).bind(*args, **kwargs).arguments

        if any(k in params for k in ("name", "index")):
            return func(*args, **kwargs)

        for instance in self._LDBatchConsole__selector.selectedIDs:
            func(instance, *args, **kwargs)
            sleep(self.INTERVAL_BETWEEN_EACH_TRIGGER)

    return wrapper


for method in _batchable_methods:
    setattr(LDBatchConsole, method, batchable_method(method))
