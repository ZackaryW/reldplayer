
from functools import cached_property
import typing
from .com.config import Config
from ._internal.i import IConsole

class _BaseAdapter:
    def __init__(self, __reldplayer : 'Reldplayer'):
        self.__reldplayer = __reldplayer

    @property
    def __host__(self):
        return self.__reldplayer

    @property
    def __get_wndmgr__(self):
        return self.__reldplayer.wndmgr
    
    @property
    def __get_rawconsole__(self):
        return self.__reldplayer.rawconsole
    
    @property
    def __get_console__(self):
        return self.__reldplayer.console
    
    @property
    def __get_synchronizer__(self):
        return self.__reldplayer.synchronizer
    
    @property
    def __get_metamgr__(self):
        return self.__reldplayer.metamgr
    
    @property
    def __get_config__(self):
        return self.__reldplayer.config


class ReMeta(type):
    _instances : typing.Dict[Config, 'Reldplayer'] = {}

    def __call__(cls, config : Config):
        if not config:
            config = Config.create()
        
        if config not in cls._instances:
            cls._instances[config] = super().__call__(config)

        return cls._instances[config]

class Reldplayer(metaclass=ReMeta):
    def __init__(self, config : Config):
        self.__config = config

    @property
    def config(self):
        """
        configurations
        """
        return self.__config

    @cached_property
    def rawconsole(self):
        """
        basic wrapper for ldconsole.exe
        """
        from reldplayer.com.rawconsole import RawConsole as _RawConsole
        class RawConsole(_BaseAdapter, _RawConsole):
            pass
        return RawConsole(self)

    @cached_property
    def console(self):
        """
        console capable of leveraging synchronizer
        """
        class Console(_BaseAdapter, IConsole):
            def __getattribute__(self, name: str) -> typing.Any:
                if name.startswith("_") or name not in dir(IConsole):
                    return super().__getattribute__(name)
                
                return self.__get_synchronizer__._wrapOver(getattr(self.__get_rawconsole__, name))
        return Console(self)

    @cached_property
    def synchronizer(self):
        """
        setting up syncing actions for multiple instances
        """
        from reldplayer.com.sync import Synchronizer as _Synchronizer

        class Synchronizer(_Synchronizer, _BaseAdapter):
            pass
        return Synchronizer(self)
    
    @cached_property
    def wndmgr(self):
        """
        manages instance windows
        - able to locate the instance window
        - resize and sort the windows according to needs
        """
        from reldplayer.com.wndmgr import WndMgr as _WndMgr
        class WndMgr(_BaseAdapter, _WndMgr):
            pass

        return WndMgr(self)
    
    @cached_property
    def metamgr(self):
        raise NotImplementedError
        class MetaMgr(_BaseAdapter):
            pass
        return MetaMgr(self)
    
    @cached_property
    def instanceQuick(self):
        from reldplayer.com.instanceQuick import InstanceQuick as _InstanceQuick
        class InstanceQuick(_BaseAdapter, _InstanceQuick):
            pass
        return InstanceQuick(self)
    
    
