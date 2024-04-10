from functools import cached_property
import json
import os
from time import sleep

class ReLDPlayerFactory:

    def strategy_1(self):
        # try to get the instance by checking psutil
        if os.path.exists("C:\\Program Files\\LDPlayer"):
            return "C:\\Program Files\\LDPlayer"
        
        if os.path.exists("C:\\Program Files (x86)\\LDPlayer"):
            return "C:\\Program Files (x86)\\LDPlayer"

    def strategy_2(self):
        import psutil
        for proc in psutil.process_iter():
            if proc.name() in ["dnplayer.exe", "dnmultiplayer.exe"]:
                return os.path.dirname(proc.cmdline()[0])

    def __last_resort(self, objtype : type):
        for path in objtype._record:
            if path not in objtype._instances:
                return objtype(path)

    def __strategy_loop(self):
        counter = 1
        while True:
            if not hasattr(self, f"strategy_{counter}"):
                break
            path = getattr(self, f"strategy_{counter}")()
            if path:
                return ReLDPlayer(path)
                
            counter += 1

        return self.__last_resort(ReLDPlayer)

    def __get__(self, obj, objtype):
        try:
            res = self.__strategy_loop()
            if not res:
                raise
            return res
                
        except Exception:
            raise RuntimeError("cannot find a valid LDPlayer instance")

class ReLDPlayerMeta(type):
    _record = None
    _instances = {}
    __pkg_dir =  os.path.dirname(os.path.realpath(__file__))

    def __new__(self, name, bases, attrs):
        if self._record is None:
            if not os.path.exists(os.path.join(self.__pkg_dir, "reldplayer_records")):
                with open(os.path.join(self.__pkg_dir, "reldplayer_records"), "w") as f:
                    json.dump([], f)
                self._record = []
            else:
                with open(os.path.join(self.__pkg_dir, "reldplayer_records"), "r") as f:
                    self._record = json.load(f)

        return super().__new__(self, name, bases, attrs)

    def __call__(self, path : str):
        if not os.path.exists(path):
            raise RuntimeError(f"Not a valid path: {path}")
        path = os.path.abspath(path)
        if path not in self._record:
            self._record.append(path)
            with open(os.path.join(self.__pkg_dir, "reldplayer_records"), "w") as f:
                json.dump(self._record, f)

        if path not in self._instances:
            self._instances[path] = super().__call__(path)
        return self._instances[path]

class ReLDPlayer(metaclass=ReLDPlayerMeta):
    factory = ReLDPlayerFactory()

    def __init__(self, path : str):
        self.__path = path
        self.__batches = []

    def query(self, query : str, returnIds : bool = False):
        return self.rawconsole.query(query, returnIds)
    
    def getInstanceDict(self, mnq_name : str = None, mnq_idx : int = None):
        return self.rawconsole.get(mnq_name, mnq_idx)
    
    @property
    def path(self):
        return self.__path
    
    def waitTillBatchLoaded(self, timeout : int = 10):
        pending = list(self.currentApplied)
        counter = 0
        while True:
            last = pending[-1]
            
            if self.rawconsole.isrunning(last):
                pending.pop()
            else:
                sleep(1)
                counter += 1

            if counter > timeout:
                return 
            
            if len(pending) == 0:
                return
            

    @cached_property
    def rawconsole(self):
        from reldplayer.rawconsole import Rawconsole
        return Rawconsole(self.path+"\\ldconsole.exe")
    
    @property
    def currentApplied(self):
        return tuple(self.__batches)
    
    @currentApplied.setter
    def currentApplied(self, value : list):
        self.__batches.clear()
        for item in self.currentStatus:
            if item["id"] in value:
                self.__batches.append(item["id"])
            elif item["name"] in value:
                self.__batches.append(item["id"])
       

    @property
    def currentStatus(self):
        return self.rawconsole.list2()

    @cached_property
    def console(self):
        from reldplayer.console import Console
        return Console(self)
    
    @cached_property
    def wndMgr(self):
        from .wndMgr import WndMgr
        return WndMgr(self)
    
    @cached_property
    def metaMgr(self):
        pass
    
    @cached_property
    def autogui(self):
        from .autogui import AutoGui
        return AutoGui(self.wndMgr)