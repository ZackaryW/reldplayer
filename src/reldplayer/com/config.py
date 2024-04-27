from dataclasses import dataclass
import os
import typing

# following are methods to get the path of ldconsole.exe


def strategy_1():
    # try to get the instance by checking psutil
    if os.path.exists("C:\\Program Files\\LDPlayer"):
        return "C:\\Program Files\\LDPlayer"

    if os.path.exists("C:\\Program Files (x86)\\LDPlayer"):
        return "C:\\Program Files (x86)\\LDPlayer"


def strategy_2():
    import psutil

    for proc in psutil.process_iter():
        if proc.name() in ["dnplayer.exe", "dnmultiplayer.exe"]:
            return os.path.dirname(proc.cmdline()[0])


class ConfigMeta(type):
    """
    ensures only one config is created for each path
    """

    _instances: typing.Dict[str, "Config"] = {}

    def __call__(cls, path: str):
        if path not in cls._instances:
            cls._instances[path] = super().__call__(path)
        return cls._instances[path]


@dataclass(slots=True)
class Config(metaclass=ConfigMeta):
    # ANCHOR config options
    path: str

    SYNC_DELAY: float = 2.5

    INSTANCE_GUI_PRIMARY_ONLYS = [
        "volumeup",
        "volumedown",
        "volumemax",
        "installapkdialog",
        "sharedfolder",
        "fullscreen",
        "operationrecorder",
        "synchronizer",
    ]

    def __hash__(self) -> int:
        return hash(self.path)

    @classmethod
    def create(cls, path: typing.Optional[str] = None):
        if path and path in cls._instances:
            return cls._instances[path]
        elif path:
            return cls(path)

        res = strategy_1()
        if res:
            return cls(res)

        res = strategy_2()
        if res:
            return cls(res)

        if os.environ.get("LDPLAYER_PATH", None):
            return cls(os.environ["LDPLAYER_PATH"])

        raise RuntimeError("cannot find a valid LDPlayer instance")
