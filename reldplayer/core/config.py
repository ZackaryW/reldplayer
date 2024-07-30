from dataclasses import field as _field, dataclass
import os
import typing
from zrcl4.json import touch_json, read_json, write_json


class PlayerConfigMeta(type):
    _instances = {}

    def __call__(self, path: str, **kwds):
        if path not in self._instances:
            self._instances[path] = super(PlayerConfigMeta, self).__call__(path, **kwds)
        return self._instances[path]


config_store_path = os.path.join(os.path.expanduser("~"), ".reldplayer")
os.makedirs(config_store_path, exist_ok=True)
if not os.path.exists(os.path.join(config_store_path, "config.json")):
    touch_json(os.path.join(config_store_path, "config.json"))
config_store: dict = read_json(os.path.join(config_store_path, "config.json"))


@dataclass
class PlayerConfig(metaclass=PlayerConfigMeta):
    path: str

    window_auto_restriction: bool = True
    window_auto_primary_onlys: typing.List[str] = _field(
        default_factory=lambda: [
            "volumeMax",
            "installApkDialog",
            "sharedFolder",
            "fullscreen",
            "synchronizer",
            "operationRecorder",
        ]
    )

    custom_vms_folder: str = None
    custom_customiza_configs_folder: str = None
    custom_recommend_configs_folder: str = None
    custom_operation_records_folder: str = None

    SYNC_DELAY: float = 1.2

    @property
    def vms_folder(self) -> str:
        if self.custom_vms_folder:
            return self.custom_vms_folder

        return os.path.join(self.path, "vms")

    @property
    def customize_configs_folder(self) -> str:
        if self.custom_customiza_configs_folder:
            return self.custom_customiza_configs_folder
        return os.path.join(self.vms_folder, "customizeConfigs")

    @property
    def recommend_configs_folder(self) -> str:
        if self.custom_recommend_configs_folder:
            return self.custom_recommend_configs_folder
        return os.path.join(self.vms_folder, "recommendConfigs")

    @property
    def operation_records_folder(self) -> str:
        if self.custom_operation_records_folder:
            return self.custom_operation_records_folder
        return os.path.join(self.vms_folder, "operationRecords")

    def _todict(self):
        ret = {}
        for name, field in self.__dataclass_fields__.items():
            if name == "path":
                continue
            if not hasattr(self, name):
                continue
            val = getattr(self, name)
            if val == field.default:
                continue
            elif name == "window_auto_primary_onlys" and val == [
                "volumeMax",
                "installApkDialog",
                "sharedFolder",
                "fullscreen",
                "synchronizer",
                "operationRecorder",
            ]:
                continue
            ret[name] = val

        return ret

    def _update(self):
        global config_store
        config_store[self.path] = self._todict()
        write_json(os.path.join(config_store_path, "config.json"), config_store)

    def __post_init__(self):
        self.__everything_inited = True
        self._update()

    def __setattr__(self, name: str, value) -> None:
        if name.startswith("_"):
            return super().__setattr__(name, value)

        if not hasattr(self, "__everything_inited"):
            return super().__setattr__(name, value)

        super().__setattr__(name, value)
        self._update()

    @classmethod
    def from_default_install(cls):
        if os.path.exists("C:\\Program Files\\LDPlayer"):
            return cls.from_path("C:\\Program Files\\LDPlayer")

        if os.path.exists("C:\\Program Files (x86)\\LDPlayer"):
            return cls.from_path("C:\\Program Files (x86)\\LDPlayer")

    @classmethod
    def from_process(cls):
        import psutil
        from psutil import AccessDenied

        for proc in psutil.process_iter():
            if proc.name() in ["dnplayer.exe", "dnmultiplayer.exe"]:
                try:
                    return cls.from_path(os.path.dirname(proc.cmdline()[0]))
                except AccessDenied:
                    return None

    @classmethod
    def from_path(cls, path: str):
        if not os.path.exists(path):
            return None

        path = os.path.abspath(path)
        # check if path ldconsole.exe exists
        if not os.path.exists(os.path.join(path, "ldconsole.exe")):
            return None

        if path in config_store:
            return cls(**config_store[path], path=path)

        return cls(path=path)

    @classmethod
    def auto(cls, allowDefault: bool = True):
        if ret := cls.from_default_install():
            return ret

        if ret := cls.from_process():
            return ret

        if allowDefault and len(config_store) > 0:
            path = list(config_store.keys())[0]
            return cls(**config_store[path], path=path)

        return None

    @staticmethod
    def openConfig():
        os.startfile(os.path.join(config_store_path, "config.json"))

    @staticmethod
    def purgeConfig():
        global config_store
        config_store = {}
        write_json(os.path.join(config_store_path, "config.json"), config_store)
