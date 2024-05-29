from dataclasses import dataclass, field
from typing import List, Optional, TypedDict


@dataclass
class Point:
    id: int
    x: int
    y: int
    state: Optional[int] = None  # Adding the 'state' attribute, making it optional


@dataclass
class Operation:
    timing: int
    operationId: str
    points: List[Point] = field(default_factory=list)


class RecordInfo(TypedDict):
    loopType: int
    loopTimes: int
    circleDuration: int
    loopInterval: int
    loopDuration: int
    accelerateTimes: int
    accelerateTimesEx: int
    recordName: str
    createTime: str
    playOnBoot: bool
    rebootTiming: int


class ReturnInfo(TypedDict):
    file: str
    info: RecordInfo


@dataclass
class OperationRecord:
    recordInfo: RecordInfo
    operations: List[Operation] = field(default_factory=list)
