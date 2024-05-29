from typing import TypedDict
from dataclasses import dataclass, field, asdict
from typing import List, Union


class SMP(TypedDict):
    reduceInertia: bool
    keyboardShowGreet: bool
    joystickShowGreet: bool
    keyboardFirstGreet: bool
    joystickFirstGreet: bool
    keyboardShowHints: bool
    joystickShowHints: bool
    keyboardIgnoreVersion: int
    joystickIgnoreVersion: int
    noticeTimes: int
    noticeHash: int
    resolutionRelatives: dict


@dataclass
class Point:
    x: int
    y: int


@dataclass
class CurvePoint:
    x: int
    y: int
    timing: int


@dataclass
class ResolutionPattern:
    width: int
    height: int


@dataclass
class BaseKeyboardData:
    key: int
    secondKey: int
    extraData: str = ""
    description: str = ""
    moreDescription: str = ""
    hintVisible: bool = True
    hintOffset: Point = field(default_factory=lambda: Point(x=0, y=0))


@dataclass
class KeyboardCurveData(BaseKeyboardData):
    curve: List[CurvePoint] = field(default_factory=list)


@dataclass
class KeyboardPointData(BaseKeyboardData):
    point: Point = field(default_factory=lambda: Point(x=0, y=0))
    type: int = 0
    downDuration: int = 0
    upDuration: int = 0
    downDurationEx: int = 0
    upDurationEx: int = 0


@dataclass
class KeyboardEntry:
    class_name: str
    data: Union[KeyboardCurveData, KeyboardPointData]

    @classmethod
    def from_dict(cls, data: dict) -> "KeyboardEntry":
        # Rename 'class' to 'class_name' if present
        if "class" in data:
            data["class_name"] = data.pop("class")
        if "curve" in data["data"]:
            data["data"] = KeyboardCurveData(**data["data"])
        else:
            data["data"] = KeyboardPointData(**data["data"])
        return cls(**data)

    def to_dict(self) -> dict:
        """Converts the KeyboardEntry object to a dictionary, handling any necessary field renames for external use."""
        result = asdict(self)
        result["class"] = result.pop("class_name")
        return result


@dataclass
class ConfigInfo:
    version: int = 0
    versionMessage: str = ""
    packageNameType: int = 0
    packageNamePattern: str = ""
    resolutionType: int = 0
    resolutionPattern: ResolutionPattern = field(
        default_factory=lambda: ResolutionPattern(width=0, height=0)
    )
    priority: int = 0
    search: str = ""


@dataclass
class KeyboardConfig:
    mouseCenter: Point = field(default_factory=lambda: Point(x=0, y=0))
    mouseScrollType: int = 0
    discType: int = 0
    advertising: bool = False
    advertiseDuration: int = 0
    advertiseText: str = ""
    cancelPoint: Point = field(default_factory=lambda: Point(x=0, y=0))
    cancelKey: int = 0
    cancelMode: int = 0
    cursor: str = "defaultCursor"
    extraData: str = ""


@dataclass
class KeyboardMapping:
    configInfo: ConfigInfo
    keyboardConfig: KeyboardConfig
    keyboardMappings: List[KeyboardEntry] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "KeyboardMapping":
        configInfo = ConfigInfo(**data["configInfo"])
        keyboardConfig = KeyboardConfig(**data["keyboardConfig"])
        keyboardMappings = [
            KeyboardEntry.from_dict(entry) for entry in data["keyboardMappings"]
        ]
        return cls(
            keyboardMappings=keyboardMappings,
            configInfo=configInfo,
            keyboardConfig=keyboardConfig,
        )

    def to_dict(self) -> dict:
        configInfo = asdict(self.configInfo)
        keyboardConfig = asdict(self.keyboardConfig)
        keyboardMappings = [entry.to_dict() for entry in self.keyboardMappings]
        return {
            "configInfo": configInfo,
            "keyboardConfig": keyboardConfig,
            "keyboardMappings": keyboardMappings,
        }
