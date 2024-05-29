import copy
from functools import cached_property
import typing
from reldplayer.core.ctx import PlayerCtx
from reldplayer.core.config import PlayerConfig
from reldplayer.internal.iconsole import IConsole2
from reldplayer.objs.query import Query


class Player:
    """
    All in one player class for interactions
    """

    _config: PlayerConfig
    _ctx: PlayerCtx

    def __init__(self, config: PlayerConfig, initCtx: bool = True):
        if config is None:
            raise ValueError("config cannot be None")
        self._config = config
        if initCtx:
            self._ctx = PlayerCtx()

    def __getitem__(
        self,
        key: typing.Union[int, str, typing.List[typing.Union[int, str, list]], Query],
    ):
        if isinstance(key, list) and len(key) == 1:
            return self.copy().select(key[0])
        return self.select(key)

    def copy(self):
        """
        creates a copy with identical PlayerConfig
        """

        player = Player(self._config, False)
        player._ctx = copy.copy(self._ctx)

        player.__dict__["raw_console"] = self.raw_console

        return player

    def select(
        self,
        key: typing.Union[int, str, typing.List[typing.Union[int, str, list]], Query],
    ):
        """
        used to set up the PlayerCtx.selected
        """
        currStats = self.raw_console.list2()
        currIds = [int(x["id"]) for x in currStats]

        def locate_id(key):
            if isinstance(key, int) and key in currIds:
                return key
            elif isinstance(key, str):
                for x in currStats:
                    if x.name == key:
                        return x["id"]
            raise ValueError(f"key {key} not found")

        if not isinstance(key, (list, tuple)):
            self._ctx.selected = [locate_id(key)]
            return

        as_primary = None
        results = set()
        for item in key:
            if isinstance(item, list):
                if as_primary:
                    raise ValueError("only one primary can be set")
                id = locate_id(item[0])
                as_primary = id
            else:
                results.add(locate_id(item))

        self._ctx.selected = as_primary + list(results) if as_primary else list(results)

    def query_instance(self, evalkey: str):
        funcstr = "lambda x : {}".format(evalkey)
        func = eval(funcstr)
        currStats = self.raw_console.list2()
        for x in currStats:
            x["selected"] = int(x["id"]) in self._ctx.selected
        for x in currStats:
            if func(x):
                return x

    def select_actives(self):
        """
        select all active windows
        """
        currStats = self.raw_console.list2()
        self._ctx.selected = [
            int(x["id"]) for x in currStats if x["top_window_handle"] != 0
        ]

    def select_all(self):
        currStats = self.raw_console.list2()
        self._ctx.selected = [int(x["id"]) for x in currStats]

    def select_inactives(self):
        currStats = self.raw_console.list2()
        self._ctx.selected = [
            int(x["id"]) for x in currStats if x["top_window_handle"] == 0
        ]

    @cached_property
    def raw_console(self):
        from reldplayer.extensions.console import Console

        r = Console(self, True)
        return r

    @cached_property
    def console(self) -> IConsole2:
        from reldplayer.extensions.console import Console

        r = Console(self)
        return r

    @cached_property
    def manage_macro(self):
        from reldplayer.extensions.manage_macro import ManageMacro

        return ManageMacro(self)

    @cached_property
    def manage_window(self):
        from reldplayer.extensions.manage_window import ManageWindow

        return ManageWindow(self)

    @cached_property
    def manage_config(self):
        from reldplayer.extensions.manage_config import ManageConfig

        return ManageConfig(self)
