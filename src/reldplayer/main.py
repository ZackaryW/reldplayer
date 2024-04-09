from functools import cached_property
import os
from time import sleep

class ReLDPlayerFactory:
    def __init__(self) -> None:
        self.__instance = None

    def __strategy_1(self):
        # try to get the instance by checking psutil
        if os.path.exists("C:\Program Files\LDPlayer"):
            return "C:\Program Files\LDPlayer"
        
        if os.path.exists("C:\Program Files (x86)\LDPlayer"):
            return "C:\Program Files (x86)\LDPlayer"

    def __strategy_2(self):
        

    def __get__(self, obj, objtype):
        if self.__instance is not None:
            return self.__instance
        
        counter = 1
        while True:
            if not hasattr(self, f"__strategy_{counter}"):
                break
            path = getattr(self, f"__strategy_{counter}")()
            if path:
                self.__instance = ReLDPlayer(path)
                break
            counter += 1

        if not self.__instance:
            raise RuntimeError("LDPlayer not found")

        return self.__instance
    


class ReLDPlayer:
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