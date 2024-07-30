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
        *key: typing.List[typing.Union[int, str, list, Query]],
    ):
        """
        used to set up the PlayerCtx.selected

        to query all instances with 'ark' in name
        >>> x.select(Query("'ark' in x['name']"))

        to select instances but set the last as primary
        >>> x.select([1,2,3,[4]])
        """

        currStats = self.raw_console.list2()
        primary = None
        valid_entries = []
        primary_set = False

        def _query(key):
            if isinstance(key, Query):
                return self.query_ids(key.qstring)

            for x in currStats:
                if (
                    isinstance(key, str)
                    and x["name"] == key
                    or isinstance(key, int)
                    and x["id"] == key
                ):
                    return x["id"]
            return None

        def handle_result(res, set_as_primary):
            nonlocal primary, primary_set
            if res is None:
                return
            if set_as_primary:
                if primary_set:
                    raise ValueError("Only one primary can be set")
                primary = res
                primary_set = True
            else:
                if isinstance(res, int):
                    valid_entries.append(res)
                else:
                    valid_entries.extend(res if isinstance(res, list) else [res])

        for item in key:
            set_as_primary = False
            if isinstance(item, list):
                if len(item) != 1:
                    raise ValueError("Invalid query format for setting primary")
                item = item[0]
                set_as_primary = True

            res = _query(item)
            handle_result(res, set_as_primary)

        deduped = (
            list(set(valid_entries))
            if all(isinstance(x, int) for x in valid_entries)
            else valid_entries
        )
        self._ctx.selected = (
            [primary] + [entry for entry in deduped if entry != primary]
            if primary is not None
            else deduped
        )

        return self

    def query_meta(self, evalkey: str, limit: int = -1):
        """
        you may query an instance based on the `InstanceMeta` attributes
        """
        funcstr = "lambda x : {}".format(evalkey)
        func = eval(funcstr)
        currStats = self.raw_console.list2()
        for x in currStats:
            x["selected"] = self._ctx.selected and int(x["id"]) in self._ctx.selected
        if limit != 1:
            ret = []
        for x in currStats:
            if func(x):
                if limit == 1:
                    return x
                ret.append(x)
            if limit > 0 and len(ret) >= limit:
                break
        return ret

    def query_ids(
        self, evalkey: str, limit: int = -1
    ) -> typing.Union[int, typing.List[int]]:
        if limit == 1:
            res = self.query_meta(evalkey, 1)
            return res["id"] if res else None
        else:
            return [x["id"] for x in self.query_meta(evalkey, limit)]

    def select_actives(self):
        """
        select all active instances
        """
        currStats = self.raw_console.list2()
        self._ctx.selected = [
            int(x["id"]) for x in currStats if x["top_window_handle"] != 0
        ]

    def select_all(self):
        """
        select all instances
        """

        currStats = self.raw_console.list2()
        self._ctx.selected = [int(x["id"]) for x in currStats]

    def select_inactives(self):
        """
        select non active instances
        """
        currStats = self.raw_console.list2()
        self._ctx.selected = [
            int(x["id"]) for x in currStats if x["top_window_handle"] == 0
        ]

    @cached_property
    def raw_console(self):
        """
        get a rawconsole that supports all commands from ldconsole.exe
        """

        from reldplayer.extensions.console import Console

        r = Console(self, True)
        return r

    @cached_property
    def console(self) -> IConsole2:
        """
        this console builds on top of rawconsole and can batch run commands based on the selected instances
        """
        from reldplayer.extensions.console import Console

        r = Console(self)
        return r

    @cached_property
    def manage_macro(self):
        """
        manage operation records
        """

        from reldplayer.extensions.manage_macro import ManageMacro

        return ManageMacro(self)

    @cached_property
    def manage_window(self):
        """
        get pygetwindow.PyWin32Window instances of the instances
        """
        from reldplayer.extensions.manage_window import ManageWindow

        return ManageWindow(self)

    @cached_property
    def manage_config(self):
        """
        manage configs located in vms
        """
        from reldplayer.extensions.manage_config import ManageConfig

        return ManageConfig(self)
