from typing import NotRequired, TypedDict


class WindowsPosition(TypedDict):
    x: int
    y: int


class LeidiansConfig(TypedDict):
    nextCheckupdateTime: int
    hasPluginLast: bool
    strp: str
    lastZoneArea: str
    lastZoneName: str
    vipMode: bool
    isBaseboard: bool
    lastIP: NotRequired[str]
    noiceUserRed: bool
    isFirstInstallApk: bool
    cloneFromSmallDisk: bool
    languageId: str
    mulTab: bool
    exitFullscreenEsc: bool
    disableMouseRightOpt: bool
    nextUpdateTime: int
    ignoreVersion: str
    framesPerSecond: int
    reduceAudio: bool
    displayMode: bool
    vmdkFastMode: bool
    windowsAlignType: int
    windowsRowCount: int
    windowsAutoSize: bool
    sortwndnotoutscreen: bool
    moreScreenSortInSame: bool
    windowsOrigin: WindowsPosition
    windowsOffset: WindowsPosition
    batchStartInterval: int
    batchNewCount: int
    batchCloneCount: int
    windowsRecordPos: bool
    multiPlayerSort: int
    isSSD: bool
    fromInstall: bool
    productLanguageId: str
    channelOpenId: str
    channelLastOpenId: str
    operaRecordFirstDo: bool
    remoteEntranceVersion: int
