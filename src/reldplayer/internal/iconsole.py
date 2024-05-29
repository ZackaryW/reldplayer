import typing

from reldplayer.internal.typedicts import InstanceMeta


class IConsole:
    def quit(self, mnq_name: str | None = None, mnq_idx: int | None = None): ...
    def quitall(self) -> None: ...
    def launch(self, mnq_name: str | None = None, mnq_idx: int | None = None): ...
    def reboot(self, mnq_name: str | None = None, mnq_idx: int | None = None): ...
    def list(self): ...
    def runninglist(self): ...
    def isrunning(self, mnq_name: str | None = None, mnq_idx: int | None = None): ...
    def list2(self) -> typing.List[InstanceMeta]: ...
    def add(self, mnq_name: str | None = None): ...
    def copy(
        self,
        mnq_name: str | None = None,
        mnq_idx: int | None = None,
        to: str | None = None,
    ): ...
    def remove(self, mnq_name: str | None = None, mnq_idx: int | None = None): ...
    def rename(
        self,
        mnq_name: str | None = None,
        mnq_idx: int | None = None,
        title: str | None = None,
    ): ...
    def modify(
        self,
        mnq_name: str | None | None = None,
        mnq_idx: int | None | None = None,
        resolution: str | None = None,
        cpu: typing.Literal[1, 2, 3, 4] | None = None,
        memory: typing.Literal[256, 512, 768, 1024, 2048, 4096, 8192] | None = None,
        manufacturer: str | None = None,
        model: str | None = None,
        pnumber: int | None = None,
        imei: typing.Literal["auto"] | str | None = None,
        imsi: typing.Literal["auto"] | str | None = None,
        simserial: typing.Literal["auto"] | str | None = None,
        androidid: typing.Literal["auto"] | str | None = None,
        mac: typing.Literal["auto"] | str | None = None,
        autorotate: bool | None = None,
        lockwindow: bool | None = None,
        root: bool | None = None,
    ): ...
    def installapp(
        self,
        mnq_name: str | None = None,
        mnq_idx: int | None = None,
        apk_file_name: str | None = None,
    ): ...
    def uninstallapp(
        self,
        mnq_name: str | None = None,
        mnq_idx: int | None = None,
        apk_package_name: str | None = None,
    ): ...
    def runapp(
        self,
        mnq_name: str | None = None,
        mnq_idx: int | None = None,
        apk_package_name: str | None = None,
    ): ...
    def killapp(
        self,
        mnq_name: str | None = None,
        mnq_idx: int | None = None,
        apk_package_name: str | None = None,
    ): ...
    def locate(
        self,
        mnq_name: str | None = None,
        mnq_idx: int | None = None,
        lng: float | None = None,
        lat: float | None = None,
    ): ...
    def adb(
        self,
        mnq_name: str | None = None,
        mnq_idx: int | None = None,
        cmd_str: str | None = None,
    ): ...
    def setprop(
        self,
        mnq_name: str | None = None,
        mnq_idx: int | None = None,
        key: str | None = None,
        value: str | None = None,
    ): ...
    def getprop(
        self,
        mnq_name: str | None = None,
        mnq_idx: int | None = None,
        key: str | None = None,
    ): ...
    def downcpu(
        self,
        mnq_name: str | None = None,
        mnq_idx: int | None = None,
        rate: int | None = None,
    ): ...
    def backup(
        self,
        mnq_name: str | None = None,
        mnq_idx: int | None = None,
        filepath: str | None = None,
    ): ...
    def restore(
        self,
        mnq_name: str | None = None,
        mnq_idx: int | None = None,
        filepath: str | None = None,
    ): ...
    def action(
        self,
        mnq_name: str | None = None,
        mnq_idx: int | None = None,
        name: str | None = None,
        value: str | None = None,
    ): ...
    def scan(
        self,
        mnq_name: str | None = None,
        mnq_idx: int | None = None,
        filepath: str | None = None,
    ): ...
    def sortWnd(self) -> None: ...
    def zoomIn(self) -> None: ...
    def zoomOut(self) -> None: ...
    def rock(self) -> None: ...
    def pull(
        self,
        mnq_name: str | None = None,
        mnq_idx: int | None = None,
        remote: str | None = None,
        local: str | None = None,
    ): ...
    def push(
        self,
        mnq_name: str | None = None,
        mnq_idx: int | None = None,
        remote: str | None = None,
        local: str | None = None,
    ): ...
    def backupapp(
        self,
        mnq_name: str | None = None,
        mnq_idx: int | None = None,
        apk_package_name: str | None = None,
        filepath: str | None = None,
    ): ...
    def restoreapp(
        self,
        mnq_name: str | None = None,
        mnq_idx: int | None = None,
        apk_package_name: str | None = None,
        filepath: str | None = None,
    ): ...
    def globalsetting(
        self,
        fps: int | None = None,
        audio: bool | None = None,
        fastplay: bool | None = None,
        cleanmode: bool | None = None,
    ): ...
    def launchex(
        self,
        mnq_name: str | None = None,
        mnq_idx: int | None = None,
        apk_package_name: str | None = None,
    ): ...
    def operatelist(self, mnq_name: str | None = None, mnq_idx: int | None = None): ...
    def operateinfo(
        self,
        mnq_name: str | None = None,
        mnq_idx: int | None = None,
        filepath: str | None = None,
    ): ...
    def operaterecord(
        self,
        mnq_name: str | None = None,
        mnq_idx: int | None = None,
        jsonstring: str | None = None,
    ): ...


class IConsole2:
    def quit(self): ...
    def quitall(self) -> None: ...
    def launch(self): ...
    def reboot(self): ...
    def list(self): ...
    def runninglist(self): ...
    def isrunning(self): ...
    def list2(self) -> typing.List[InstanceMeta]: ...
    def add(self, mnq_name: str | None = None): ...
    def copy(self, to: str | None = None): ...
    def remove(self): ...
    def rename(self, title: str | None = None): ...
    def modify(
        self,
        mnq_name: str | None | None = None,
        mnq_idx: int | None | None = None,
        resolution: str | None = None,
        cpu: typing.Literal[1, 2, 3, 4] | None = None,
        memory: typing.Literal[256, 512, 768, 1024, 2048, 4096, 8192] | None = None,
        manufacturer: str | None = None,
        model: str | None = None,
        pnumber: int | None = None,
        imei: typing.Literal["auto"] | str | None = None,
        imsi: typing.Literal["auto"] | str | None = None,
        simserial: typing.Literal["auto"] | str | None = None,
        androidid: typing.Literal["auto"] | str | None = None,
        mac: typing.Literal["auto"] | str | None = None,
        autorotate: bool | None = None,
        lockwindow: bool | None = None,
        root: bool | None = None,
    ): ...
    def installapp(self, apk_file_name: str | None = None): ...
    def uninstallapp(self, apk_package_name: str | None = None): ...
    def runapp(self, apk_package_name: str | None = None): ...
    def killapp(self, apk_package_name: str | None = None): ...
    def locate(self, lng: float | None = None, lat: float | None = None): ...
    def adb(self, cmd_str: str | None = None): ...
    def setprop(self, key: str | None = None, value: str | None = None): ...
    def getprop(self, key: str | None = None): ...
    def downcpu(self, rate: int | None = None): ...
    def backup(self, filepath: str | None = None): ...
    def restore(self, filepath: str | None = None): ...
    def action(self, name: str | None = None, value: str | None = None): ...
    def scan(self, filepath: str | None = None): ...
    def sortWnd(self) -> None: ...
    def zoomIn(self) -> None: ...
    def zoomOut(self) -> None: ...
    def rock(self) -> None: ...
    def pull(self, remote: str | None = None, local: str | None = None): ...
    def push(self, remote: str | None = None, local: str | None = None): ...
    def backupapp(
        self, apk_package_name: str | None = None, filepath: str | None = None
    ): ...
    def restoreapp(
        self, apk_package_name: str | None = None, filepath: str | None = None
    ): ...
    def globalsetting(
        self,
        fps: int | None = None,
        audio: bool | None = None,
        fastplay: bool | None = None,
        cleanmode: bool | None = None,
    ): ...
    def launchex(self, apk_package_name: str | None = None): ...


list_of_id_funcs = [
    "operaterecord",
    "operateinfo",
    "operatelist",
    "launchex",
    "restoreapp",
    "backupapp",
    "push",
    "pull",
    "scan",
    "action",
    "restore",
    "backup",
    "downcpu",
    "getprop",
    "setprop",
    "adb",
    "locate",
    "runapp",
    "killapp",
    "uninstallapp",
    "installapp",
    "modify",
    "rename",
    "remove",
    "copy",
    "reboot",
    "launch",
    "quit",
]
