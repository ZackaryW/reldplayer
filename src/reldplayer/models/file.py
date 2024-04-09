
from typing import List, Optional, TypedDict
import typing
from pydantic import BaseModel, Field, dataclasses

class WidthHeight(TypedDict):
    width: int
    height: int 

class Hotkey(TypedDict):
    modifiers: int
    key : int

class XY(TypedDict):
    x: int
    y: int

class CurveItem(TypedDict):
    x: int
    y: int
    timing: int


class Data(BaseModel):
    type: Optional[int] = None
    origin: Optional[XY] = None
    radius: Optional[int] = None
    leftKey: Optional[int] = None
    upKey: Optional[int] = None
    rightKey: Optional[int] = None
    downKey: Optional[int] = None
    description: str
    moreDescription: str
    extraData: str
    hintVisible: bool
    hintOffset: XY
    key: Optional[int] = None
    secondKey: Optional[int] = None
    macros: Optional[str] = None
    curve: Optional[List[CurveItem]] = None
    point: Optional[XY] = None
    downDuration: Optional[int] = None
    upDuration: Optional[int] = None
    downDurationEx: Optional[int] = None
    upDurationEx: Optional[int] = None
    mode: Optional[int] = None
    sensitivity: Optional[int] = None
    sensitivity_y: Optional[int] = None
    sensitivityex_x: Optional[float] = None
    sensitivityex_y: Optional[float] = None

class KeyboardMapping(BaseModel):
    class_: str = Field(..., alias='class')
    data: Data

class ConfigInfo(BaseModel):
    version: int
    versionMessage: str
    packageNameType: int
    packageNamePattern: str
    resolutionType: int
    resolutionPattern: WidthHeight
    priority: int
    search: str

class KeyboardConfig(BaseModel):
    mouseCenter: XY
    mouseScrollType: int
    discType: int
    advertising: bool
    advertiseDuration: int
    advertiseText: str
    cancelPoint: XY
    cancelKey: int
    cancelMode: int
    cursor: str
    extraData: str

class KMP(BaseModel):
    keyboardMappings: List[KeyboardMapping]
    configInfo: ConfigInfo
    keyboardConfig: KeyboardConfig


class PropertySettings(BaseModel):
    phoneIMEI: Optional[str] = None
    phoneIMSI: Optional[str] = None
    phoneSimSerial: Optional[str] = None
    phoneAndroidId: Optional[str] = None
    phoneModel: Optional[str] = None
    phoneManufacturer: Optional[str] = None
    macAddress: Optional[str] = None
    phoneNumber: Optional[str] = None

class StatusSettings(BaseModel):
    sharedApplications: Optional[str] = None
    sharedPictures: Optional[str] = None
    sharedMisc: Optional[str] = None
    playerName: Optional[str] = None
    closeOption: Optional[int] = None

class BasicSettings(BaseModel):
    left: Optional[int] = None
    top: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    realHeigh: Optional[int] = None
    realWidth: Optional[int] = None
    networkEnable: Optional[bool] = None
    isForstStart: Optional[bool] = None
    mulFsAddSize: Optional[int] = None
    mulFsAutoSize: Optional[int] = None
    verticalSync: Optional[bool] = None
    fsAutoSize: Optional[int] = None
    noiceHypeVOpen: Optional[bool] = None
    autoRun: Optional[bool] = None
    rootMode: Optional[bool] = None
    heightFrameRate: Optional[bool] = None
    adbDebug: Optional[int] = None
    autoRotate: Optional[bool] = None
    isForceLandscape: Optional[bool] = None
    standaloneSysVmdk: Optional[bool] = None
    lockWindow: Optional[bool] = None
    disableMouseFastOpt: Optional[bool] = None
    cjztdisableMouseFastOpt_new: Optional[int] = None
    HDRQuality: Optional[int] = None
    qjcjdisableMouseFast: Optional[int] = None
    fps: Optional[int] = None
    astc: Optional[bool] = None
    videoQuality: Optional[int] = None

class NetworkSettings(BaseModel):
    networkEnable: Optional[bool] = None
    networkSwitching: Optional[bool] = None
    networkStatic: Optional[bool] = None
    networkAddress: Optional[str] = None
    networkGateway: Optional[str] = None
    networkSubnetMask: Optional[str] = None
    networkDNS1: Optional[str] = None
    networkDNS2: Optional[str] = None
    networkInterface: Optional[str] = None

class AdvancedSettings(BaseModel):
    resolution: Optional[WidthHeight] = None
    resolutionDpi: Optional[int] = None
    cpuCount: Optional[int] = None
    memorySize: Optional[int] = None
    micphoneName: Optional[str] = None
    speakerName: Optional[str] = None

class HotkeySettings(BaseModel):
    backKey: Optional[Hotkey] = None
    homeKey: Optional[Hotkey] = None
    appSwitchKey: Optional[Hotkey] = None
    menuKey: Optional[Hotkey] = None
    zoomInKey: Optional[Hotkey] = None
    zoomOutKey: Optional[Hotkey] = None
    bossKey: Optional[Hotkey] = None
    shakeKey: Optional[Hotkey] = None
    operationRecordKey: Optional[Hotkey] = None
    fullScreenKey: Optional[Hotkey] = None
    showMappingKey: Optional[Hotkey] = None
    videoRecordKey: Optional[Hotkey] = None
    mappingRecordKey: Optional[Hotkey] = None
    keyboardModelKey: Optional[Hotkey] = None

class LeidianCfg(BaseModel):
    propertySettings: Optional['PropertySettings'] = None
    statusSettings: Optional['StatusSettings'] = None
    basicSettings: Optional['BasicSettings'] = None
    networkSettings: Optional['NetworkSettings'] = None
    advancedSettings: Optional['AdvancedSettings'] = None
    hotkeySettings: Optional['HotkeySettings'] = None

class WindowsOrigin(BaseModel):
    x: int
    y: int


class WindowsOffset(BaseModel):
    x: int
    y: int

class LeidiansCfg(BaseModel):
    languageId: Optional[str] = None
    productLanguageId: Optional[str] = None
    channelOpenId: Optional[str] = None
    channelLastOpenId: Optional[str] = None
    reduceAudio: Optional[bool] = None
    isSSD: Optional[bool] = None
    fromInstall: Optional[bool] = None
    strp: Optional[str] = None
    lastZoneArea: Optional[str] = None
    lastZoneName: Optional[str] = None
    vipMode: Optional[bool] = None
    hyperOptime: Optional[str] = None
    isBaseboard: Optional[bool] = None
    basicSettings_lastIP: Optional[str] = Field(None, alias='basicSettings.lastIP')
    nextCheckupdateTime: Optional[int] = None
    noiceUserRed: Optional[bool] = None
    isFirstInstallApk: Optional[bool] = None
    hasPluginLast: Optional[bool] = None
    cloneFromSmallDisk: Optional[bool] = None
    framesPerSecond: Optional[int] = None
    displayMode: Optional[bool] = None
    vmdkFastMode: Optional[bool] = None
    windowsAlignType: Optional[int] = None
    windowsRowCount: Optional[int] = None
    windowsAutoSize: Optional[bool] = None
    sortwndnotoutscreen: Optional[bool] = None
    moreScreenSortInSame: Optional[bool] = None
    windowsOrigin: Optional[WindowsOrigin] = None
    windowsOffset: Optional[WindowsOffset] = None
    batchStartInterval: Optional[int] = None
    batchNewCount: Optional[int] = None
    batchCloneCount: Optional[int] = None
    windowsRecordPos: Optional[bool] = None
    mulTab: Optional[bool] = None
    exitFullscreenEsc: Optional[bool] = None
    disableMouseRightOpt: Optional[bool] = None
    remoteEntranceVersion: Optional[int] = None
    multiPlayerSort: Optional[int] = None
    operaterSort: Optional[int] = None


@dataclasses.dataclass(slots=True)
class SMP:
    reduceInertia: bool = True
    keyboardShowGreet: bool = True
    joystickShowGreet: bool = True
    keyboardFirstGreet: bool = True
    joystickFirstGreet: bool = True
    keyboardShowHints: bool = True
    joystickShowHints: bool = True
    keyboardIgnoreVersion : int =0
    joystickIgnoreVersion: int = 0
    noticeTimes : int = 0
    noticeHash : int = 0
    resolutionRelatives : typing.Dict[str ,dict] = Field(default_factory=dict)