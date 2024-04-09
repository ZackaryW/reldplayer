from functools import cache
from time import sleep
from typing import Any
from reldplayer.models import ConsoleInterface
import inspect

class Console(ConsoleInterface):
    def __init__(self, ldplayer):
        from reldplayer.main import ReLDPlayer
        self.__host : ReLDPlayer = ldplayer

    def __getattribute__(self, __name: str) -> Any:
        if __name.startswith("_") or __name not in dir(ConsoleInterface):
            return super().__getattribute__(__name)
    
        if len(self.__host.currentApplied) == 0:
            return getattr(self.__host.rawconsole, __name)
        
        if not self.__isBatchable(__name):
            return getattr(self.__host.rawconsole, __name)

        def runner(*args, **kwargs):
            combined_query = {}
            for i in self.__host.currentApplied:
                res = self.__host.rawconsole.__getattribute__(__name)(i, *args, **kwargs)
                sleep(0.2)
                if res is None:
                    continue
                combined_query[i] = res

        return runner
    
    @cache
    def __isBatchable(self, __name : str):
        if not inspect.ismethod(getattr(self.__host.rawconsole, __name)):
            return False
        
        # check if args include mnq_name and mnq_idx
        if len((params := inspect.signature(getattr(self.__host.rawconsole, __name)).parameters)) < 2:
            return False
        
        if "mnq_name" in params and "mnq_idx" in params:
            return True
        
        return False
        
