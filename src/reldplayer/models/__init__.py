from typing import TypedDict, Union, Literal

class InstanceDict(TypedDict):
    id : int
    name : str
    top_window_handle : int 
    bind_window_handle : int
    android_started_int : int
    pid : int
    pid_of_vbox : int

    
class ConsoleInterface:
    def quit(self, mnq_name: str = None, mnq_idx: int = None):
        pass

    def quitall(self):
        pass

    def launch(self, mnq_name: str = None, mnq_idx: int = None):
        pass

    def reboot(self, mnq_name: str = None, mnq_idx: int = None):
        pass

    def list(self):
        pass

    def runninglist(self):
        pass

    def isrunning(self, mnq_name: str = None, mnq_idx: int = None):
        pass

    def list2(self):
        pass
    
    def add(self, mnq_name: str = None):
        pass

    def copy(self, mnq_name: str = None, mnq_idx: int = None, to: str = None):
        pass

    def remove(self, mnq_name: str = None, mnq_idx: int = None):
        pass

    def rename(self, mnq_name: str = None, mnq_idx: int = None, title: str = None):
        pass

    def modify(self, mnq_name: str = None, mnq_idx: int = None, resolution: str = None, cpu: Literal[1,2,3,4] = None, memory: Literal[256, 512,768,1024, 2048, 4096, 8192] = None, manufacturer: str = None, model: str = None, pnumber: int = None, imei: Union[Literal["auto"], str] = None, imsi: Union[Literal["auto"], str] = None, simserial: Union[Literal["auto"], str] = None, androidid: Union[Literal["auto"], str] = None, mac: Union[Literal["auto"], str] = None, autorotate: bool = None, lockwindow: bool = None, root: bool = None):
        pass

    def installapp(self, mnq_name: str = None, mnq_idx: int = None, apk_file_name: str = None):
        pass

    def uninstallapp(self, mnq_name: str = None, mnq_idx: int = None, apk_package_name: str = None):
        pass

    def runapp(self, mnq_name: str = None, mnq_idx: int = None, apk_package_name: str = None):
        pass

    def killapp(self, mnq_name: str = None, mnq_idx: int = None, apk_package_name: str = None):
        pass

    def locate(self, mnq_name: str = None, mnq_idx: int = None, lng: float = None, lat: float = None):
        pass

    def adb(self, mnq_name: str = None, mnq_idx: int = None, cmd_str: str = None):
        pass

    def setprop(self, mnq_name: str = None, mnq_idx: int = None, key: str = None, value: str = None):
        pass

    def getprop(self, mnq_name: str = None, mnq_idx: int = None, key: str = None):
        pass

    def downcpu(self, mnq_name: str = None, mnq_idx: int = None, rate: int = None):
        pass

    def backup(self, mnq_name: str = None, mnq_idx: int = None, filepath: str = None):
        pass

    def restore(self, mnq_name: str = None, mnq_idx: int = None, filepath: str = None):
        pass

    def action(self, mnq_name: str = None, mnq_idx: int = None, name: str = None, value: str = None):
        pass

    def scan(self, mnq_name: str = None, mnq_idx: int = None, filepath: str = None):
        pass

    def sortWnd(self):
        pass

    def zoomIn(self):
        pass

    def zoomOut(self):
        pass

    def rock(self):
        pass

    def pull(self, mnq_name: str = None, mnq_idx: int = None, remote: str = None, local: str = None):
        pass
    
    def push(self, mnq_name: str = None, mnq_idx: int = None, remote: str = None, local: str = None):
        pass

    def backupapp(self, mnq_name: str = None, mnq_idx: int = None, apk_package_name: str = None, filepath: str = None):
        pass

    def restoreapp(self, mnq_name: str = None, mnq_idx: int = None, apk_package_name: str = None, filepath: str = None):
        pass

    def globalsetting(self, fps: int = None, audio: bool = None, fastplay: bool = None, cleanmode: bool = None):
        pass

    def launchex(self, mnq_name: str = None, mnq_idx: int = None, apk_package_name: str = None):
        pass

    def operatelist(self, mnq_name: str = None, mnq_idx: int = None):
        pass

    def operateinfo(self, mnq_name: str = None, mnq_idx: int = None, filepath: str = None):
        pass

    def operaterecord(self, mnq_name: str = None, mnq_idx: int = None, jsonstring: str = None):
        pass
