from functools import cached_property
import json
from time import sleep
from zrcl4.subprocess import exec_command as _exec, query, query_raw
import typing
import os

from reldplayer.core.ctx import PlayerCtx
from reldplayer.core.config import PlayerConfig
from reldplayer.internal.iconsole import IConsole, list_of_id_funcs
from reldplayer.internal.typedicts import InstanceMeta


class Console(IConsole):

    def __init__(self, player, rawconsole: bool = False):
        self.__rawconsole = rawconsole
        self.__player = player

    @property
    def __config(self) -> PlayerConfig:
        return self.__player._config

    @property
    def __ctx(self) -> PlayerCtx:
        if self.__rawconsole:
            return None
        return self.__player._ctx

    @cached_property
    def __ldconsole__(self):
        return os.path.join(self.__config.path, "ldconsole.exe")

    def __argument_id(
        self,
        mnq_name: typing.Optional[str],
        mnq_idx: typing.Optional[int],
        arglist: list,
    ):
        if mnq_name is None and mnq_idx is None:
            raise ValueError("mnq_name and mnq_idx cannot both be None")

        if isinstance(mnq_name, int):
            arglist.extend(["--index", str(mnq_name)])
        elif mnq_name is not None:
            arglist.extend(["--name", mnq_name])
        else:
            arglist.extend(["--index", str(mnq_idx)])

    def __argument_check_range(self, value: int, low: int, high: int):
        if value < low or value > high:
            raise ValueError(f"value must be between {low} and {high}")

    def _exec(self, cmd: str, *args):
        _exec(self.__ldconsole__, cmd, *args)

    def _query(self, cmd: str, *args, **kwargs):
        return query(self.__ldconsole__, cmd, *args, **kwargs)

    def _query_raw(self, cmd: str, *args):
        return query_raw(self.__ldconsole__, cmd, *args)

    # commands
    def quit(   
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        self._exec("quit", *arglist)

    def quitall(self):
        self._exec("quitall")

    def launch(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        self._exec("launch", *arglist)

    def reboot(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        self._exec("reboot", *arglist)

    def list(self):
        return self._query("list")

    def runninglist(self):
        return self._query("runninglist")

    def isrunning(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        return self._query("isrunning", *arglist) == "running"

    def list2(self) -> typing.List[InstanceMeta]:
        raw = self._query("list2", to_list=True)
        assert isinstance(raw, list)
        ret = []
        for item in raw:
            item: str
            splitted = item.split(",")

            ret.append(
                InstanceMeta(
                    id=int(splitted[0]),
                    name=splitted[1],
                    top_window_handle=int(splitted[2]),
                    bind_window_handle=int(splitted[3]),
                    android_started_int=int(splitted[4]),
                    pid=int(splitted[5]),
                    pid_of_vbox=int(splitted[6]),
                )
            )

        return ret

    def add(self, mnq_name: typing.Optional[str] = None):
        arglist = ["--name", mnq_name] if mnq_name is not None else []
        self._exec("add", *arglist)

    def copy(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
        to: typing.Optional[str] = None,
    ):
        if not mnq_name and not mnq_idx:
            raise ValueError("mnq_name and mnq_idx cannot both be None")
        arglist = (
            ["--from", mnq_name]
            if mnq_name is not None
            else ["--from", str(mnq_idx), "--to", to]
        )

        if to is not None:
            arglist = ["--name", to] + arglist

        self._exec("copy", *arglist)

    def remove(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        self._exec("remove", *arglist)

    def rename(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
        title: typing.Optional[str] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        if title is not None:
            arglist.extend(["--title", title])
        self._exec("rename", *arglist)

    def modify(
        self,
        mnq_name: typing.Optional[typing.Optional[str]] = None,
        mnq_idx: typing.Optional[typing.Optional[int]] = None,
        resolution: typing.Optional[str] = None,
        cpu: typing.Optional[typing.Literal[1, 2, 3, 4]] = None,
        memory: typing.Optional[
            typing.Literal[256, 512, 768, 1024, 2048, 4096, 8192]
        ] = None,
        manufacturer: typing.Optional[str] = None,
        model: typing.Optional[str] = None,
        pnumber: typing.Optional[int] = None,
        imei: typing.Optional[typing.Union[typing.Literal["auto"], str]] = None,
        imsi: typing.Optional[typing.Union[typing.Literal["auto"], str]] = None,
        simserial: typing.Optional[typing.Union[typing.Literal["auto"], str]] = None,
        androidid: typing.Optional[typing.Union[typing.Literal["auto"], str]] = None,
        mac: typing.Optional[typing.Union[typing.Literal["auto"], str]] = None,
        autorotate: typing.Optional[bool] = None,
        lockwindow: typing.Optional[bool] = None,
        root: typing.Optional[bool] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        if resolution is not None:
            arglist.extend(["--resolution", resolution])
        if cpu is not None:
            arglist.extend(["--cpu", str(cpu)])
        if memory is not None:
            arglist.extend(["--memory", str(memory)])
        if manufacturer is not None:
            arglist.extend(["--manufacturer", manufacturer])
        if model is not None:
            arglist.extend(["--model", model])
        if pnumber is not None:
            arglist.extend(["--pnumber", str(pnumber)])
        if imei is not None:
            arglist.extend(["--imei", str(imei)])
        if imsi is not None:
            arglist.extend(["--imsi", str(imsi)])
        if simserial is not None:
            arglist.extend(["--simserial", str(simserial)])
        if androidid is not None:
            arglist.extend(["--androidid", str(androidid)])
        if mac is not None:
            arglist.extend(["--mac", str(mac)])
        if autorotate is not None:
            arglist.extend(["--autorotate", 1 if autorotate else 0])
        if lockwindow is not None:
            arglist.extend(["--lockwindow", 1 if lockwindow else 0])
        if root is not None:
            arglist.extend(["--root", 1 if root else 0])
        self._exec("modify", *arglist)

    def installapp(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
        apk_file_name: typing.Optional[str] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        arglist.extend(["--filename", apk_file_name])
        self._exec("installapp", *arglist)

    def uninstallapp(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
        apk_package_name: typing.Optional[str] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        arglist.extend(["--packagename", apk_package_name])
        self._exec("uninstallapp", *arglist)

    def runapp(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
        apk_package_name: typing.Optional[str] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        arglist.extend(["--packagename", apk_package_name])
        self._exec("runapp", *arglist)

    def killapp(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
        apk_package_name: typing.Optional[str] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        arglist.extend(["--packagename", apk_package_name])
        self._exec("killapp", *arglist)

    def locate(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
        lng: typing.Optional[float] = None,
        lat: typing.Optional[float] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        arglist.extend(["--LLI", f"{str(lat)},{str(lng)}"])
        self._exec("locate", *arglist)

    def adb(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
        cmd_str: typing.Optional[str] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        arglist.extend(["--command", cmd_str])
        self._exec("adb", *arglist)

    def setprop(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
        key: typing.Optional[str] = None,
        value: typing.Optional[str] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        arglist.extend(["--key", key, "--value", value])
        self._exec("setprop", *arglist)

    def getprop(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
        key: typing.Optional[str] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        if key is not None:
            arglist.extend(["--key", key])
        self._exec("getprop", *arglist)

    def downcpu(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
        rate: typing.Optional[int] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        if rate is None:
            rate = 100
        self.__argument_check_range(rate, 0, 100)
        arglist.extend(["--rate", str(rate)])
        self._exec("downcpu", *arglist)

    def backup(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
        filepath: typing.Optional[str] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        arglist.extend(["--file", filepath])
        self._exec("backup", *arglist)

    def restore(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
        filepath: typing.Optional[str] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        arglist.extend(["--file", filepath])
        self._exec("restore", *arglist)

    def action(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
        name: typing.Optional[str] = None,
        value: typing.Optional[str] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        arglist.extend(["--name", name, "--value", value])
        self._exec("action", *arglist)

    def scan(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
        filepath: typing.Optional[str] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        arglist.extend(["--file", filepath])
        self._exec("scan", *arglist)

    def sortWnd(self):
        self._exec("sortWnd")

    def zoomIn(self):
        self._exec("zoomIn")

    def zoomOut(self):
        self._exec("zoomOut")

    def rock(self):
        self._exec("rock")

    def pull(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
        remote: typing.Optional[str] = None,
        local: typing.Optional[str] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        arglist.extend(["--remote", remote, "--local", local])
        self._exec("pull", *arglist)

    def push(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
        remote: typing.Optional[str] = None,
        local: typing.Optional[str] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        arglist.extend(["--remote", remote, "--local", local])
        self._exec("push", *arglist)

    def backupapp(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
        apk_package_name: typing.Optional[str] = None,
        filepath: typing.Optional[str] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        arglist.extend(["--packagename", apk_package_name, "--file", filepath])
        self._exec("backupapp", *arglist)

    def restoreapp(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
        apk_package_name: typing.Optional[str] = None,
        filepath: typing.Optional[str] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        arglist.extend(["--packagename", apk_package_name, "--file", filepath])
        self._exec("restoreapp", *arglist)

    def globalsetting(
        self,
        fps: typing.Optional[int] = None,
        audio: typing.Optional[bool] = None,
        fastplay: typing.Optional[bool] = None,
        cleanmode: typing.Optional[bool] = None,
    ):
        arglist = []
        if fps is not None:
            arglist.extend(["--fps", str(fps)])
        if audio is not None:
            arglist.extend(["--audio", 1 if audio else 0])
        if fastplay is not None:
            arglist.extend(["--fastplay", 1 if fastplay else 0])
        if cleanmode is not None:
            arglist.extend(["--cleanmode", 1 if cleanmode else 0])
        self._exec("globalsetting", *arglist)

    def launchex(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
        apk_package_name: typing.Optional[str] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        arglist.extend(["--packagename", apk_package_name])
        self._exec("launchex", *arglist)

    def operatelist(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        raw = self._query("operatelist", *arglist)
        return json.loads(raw)

    def operateinfo(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
        filepath: typing.Optional[str] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        arglist.extend(["--file", filepath])
        raw = self._query("operateinfo", *arglist)
        assert isinstance(raw, str)
        return json.loads(raw)

    def operaterecord(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
        jsonstring: typing.Optional[str] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        arglist.extend(["--content", jsonstring])
        self._exec("operaterecord", *arglist)

    def __getattribute__(self, name: str) -> typing.Any:
        if (
            name.startswith("_")
            or not self.__ctx
            or name not in list_of_id_funcs
            or not self.__ctx.selected
        ):
            return super().__getattribute__(name)

        func = super().__getattribute__(name)

        def wrapper(*args, **kwargs):

            for idx in self.__ctx.selected:
                func(mnq_idx=idx, *args, **kwargs)
                sleep(self.__config.SYNC_DELAY)

        return wrapper
