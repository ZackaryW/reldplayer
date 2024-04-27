from contextlib import contextmanager
import inspect
from time import sleep
import typing

from reldplayer.com.rawconsole import RawConsole
from ..com.config import Config


class Synchronizer:
    __dictionary: typing.Dict[str, typing.Tuple[typing.List[int], None | int]] = {}
    __lastSyncKey: str | None = None
    __currentSyncKey: str | None = None

    __get_config__: Config
    __get_rawconsole__: RawConsole

    @property
    def syncCount(self) -> int:
        if self.__currentSyncKey is None:
            return 0
        return len(self.__dictionary[self.__currentSyncKey])

    def set(
        self,
        key: str,
        value: typing.Optional[typing.List[int]] = None,
        setPrimary: int = -1,
        active: bool = True,
    ):
        """
        set a profile of synchronizer and activate
        """

        if key in self.__dictionary and value is None:
            self.__currentSyncKey = key
            return

        assert value

        if key in self.__dictionary:
            raise KeyError("Key already exists")
        self.__dictionary[key] = (value, setPrimary if setPrimary in value else None)
        if active:
            self.__currentSyncKey = key

    def setq(self, value: typing.List[int], setPrimary: int = -1, active: bool = True):
        """
        ignore the default profile saving logic and just activate the input value
        """
        key = "__some_internal_rand_key______"
        if key in self.__dictionary:
            self.__dictionary.pop(key)
        self.set(key, value, setPrimary, active)

    def get(self, key: str) -> typing.List[int]:
        """
        get a profile of synchronizer
        """
        if key not in self.__dictionary:
            raise KeyError("Key doesn't exist")
        return self.__dictionary[key][0]

    def getPrimary(self, key: str) -> typing.Optional[int]:
        if key not in self.__dictionary:
            raise KeyError("Key doesn't exist")
        return self.__dictionary[key][1]

    def getTuple(
        self, key: str
    ) -> typing.Tuple[typing.List[int], typing.Optional[int]]:
        if key not in self.__dictionary:
            raise KeyError("Key doesn't exist")
        return self.__dictionary[key]

    @contextmanager
    def tempSync(self, key: str):
        """
        temproarily set a profile of synchronizer and restore after the block
        """
        previousSync = self.__currentSyncKey
        if key not in self.__dictionary:
            raise KeyError("Key doesn't exist")
        self.__currentSyncKey = key
        try:
            yield
        finally:
            self.__currentSyncKey = previousSync

    @property
    def syncToggle(self) -> bool:
        return self.__currentSyncKey is not None

    @syncToggle.setter
    def syncToggle(self, value: bool):
        self.__currentSyncKey = None if value else self.__lastSyncKey

    @property
    def currentSync(self) -> typing.List[int]:
        if self.__currentSyncKey is None:
            return []
        return self.__dictionary[self.__currentSyncKey][0]

    @property
    def currentActives(self) -> typing.List[int]:
        return [
            x["id"]
            for x in self.__get_rawconsole__.list2()
            if x["top_window_handle"] != 0
        ]

    @property
    def currentPrimary(self) -> typing.Optional[int]:
        if self.__currentSyncKey is None:
            return self.currentActives[0] if self.currentActives else None
        res = self.__dictionary[self.__currentSyncKey][1]
        if res is None and len(self.__dictionary[self.__currentSyncKey][0]) == 1:
            return self.__dictionary[self.__currentSyncKey][0][0]
        return res

    @contextmanager
    def disableSync(self):
        previousSync = self.__currentSyncKey
        self.__currentSyncKey = None
        try:
            yield
        finally:
            self.__currentSyncKey = previousSync

    def __setattr__(self, name: str, value: typing.Any) -> None:
        """
        setup last sync key for each current sync assignment
        """
        if name == "__currentSyncKey":
            self.__lastSyncKey = value
        super().__setattr__(name, value)

    def _wrapOver(self, func, callingKey: str = "mnq_name"):
        """
        takes a function and wraps it so that it can repeatly be called
        """
        if self.__currentSyncKey is None:
            return func
        # check mnq_name in signature
        if callingKey not in inspect.signature(func).parameters:
            return func

        if func.__name__ in ["copy", "add"]:
            raise RuntimeError("copy and add are not supported")

        def wrapper(*args, **kwargs):
            assert self.__currentSyncKey in self.__dictionary, "Key doesn't exist"
            for id in self.get(self.__currentSyncKey):
                func(*args, **kwargs, mnq_name=id)
                if self.__get_config__.SYNC_DELAY > 0:
                    sleep(self.__get_config__.SYNC_DELAY)

        return wrapper
