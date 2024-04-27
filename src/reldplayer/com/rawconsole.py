from functools import cached_property
import os
import subprocess
import typing

from .._internal.i import IConsole, InstanceMeta
from ..com.config import Config


class RawConsole(IConsole):
    __get_config__: Config

    @cached_property
    def __ldconsole__(self):
        return os.path.join(self.__get_config__.path, "ldconsole.exe")

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

    # ANCHOR subporcess
    def _exec(self, *args):
        """
        Execute a subprocess with the given arguments.

        Args:
            *args: Variable length argument list.

        Returns:
            None
        """
        subprocess.Popen(  # noqa
            [self.__ldconsole__, *(str(arg) for arg in args)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.DETACHED_PROCESS
            | subprocess.CREATE_NEW_PROCESS_GROUP
            | subprocess.CREATE_BREAKAWAY_FROM_JOB,
        )

    def _queryRaw(self, *args, timeout: int = 5):
        """
        Executes a raw query using the specified arguments and a timeout.

        Args:
            *args: Any additional arguments for the query.
            timeout (int): The maximum time to wait for the query to complete (default is 5).

        Returns:
            bytes: The output of the query execution.
        """
        try:
            if not len(args):
                queryed = [self.__ldconsole__]
            else:
                queryed = [self.__ldconsole__, *(str(arg) for arg in args)]

            proc: subprocess.CompletedProcess = subprocess.run(
                queryed, capture_output=True, timeout=timeout
            )
            comm: bytes = proc.stdout

        except subprocess.TimeoutExpired as e:
            raise e
        except subprocess.CalledProcessError as e:
            raise e

        return comm

    def _query(
        self,
        *args,
        timeout: int = 5,
        raw: bool = False,
        decodeOrder: typing.List[str] = ["utf-8", "gbk"],
        toList: bool = False,
        stripNullLines: bool = False,
    ):
        """
        Perform a query with optional parameters for timeout, raw output, return context, decoding order, conversion to list, and stripping null lines.

        Args:
            *args: Variable length argument list.
            timeout (int): Timeout duration in seconds (default is 5).
            raw (bool): Flag to indicate whether to return raw output (default is False).
            decodeOrder (List[str]): List of encoding orders to decode raw output (default is ["utf-8", "gbk"]).
            toList (bool): Flag to indicate whether to convert the output to a list (default is False).
            stripNullLines (bool): Flag to indicate whether to strip null lines from the output (default is False).

        Returns:
            str: The processed query output
        """
        rawProcess = self._queryRaw(*args, timeout=timeout)

        if raw:
            return rawProcess

        for decoder in decodeOrder:
            try:
                decoded = rawProcess.decode(decoder)
            except:  # noqa
                continue

            ret = decoded

        if toList:
            ret = ret.strip().split("\r\n")

            if stripNullLines:
                ret = list(filter(None, ret))
                ret = list(map(lambda x: x.strip(), ret))

        return ret

    # ANCHOR commands
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
        raw = self._query("list2", toList=True)
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
        self._query("operatelist", *arglist)

    def operateinfo(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
        filepath: typing.Optional[str] = None,
    ):
        arglist = []
        self.__argument_id(mnq_name, mnq_idx, arglist)
        arglist.extend(["--file", filepath])
        self._query("operateinfo", *arglist)

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

    #
    def get(
        self,
        mnq_name: typing.Optional[str] = None,
        mnq_idx: typing.Optional[int] = None,
    ):
        if isinstance(mnq_name, int):
            mnq_idx = mnq_name
        for item in self.list2():
            if item["name"] == mnq_name or item["id"] == mnq_idx:
                return item

    def query(self, qrystr: str, returnIds: bool = False):
        evalfunc = eval(f"lambda q : {qrystr}")
        matched = []

        for item in self.list2():
            if evalfunc(item):
                matched.append(item)

        if returnIds:
            return [item["id"] for item in matched]
        else:
            return matched
