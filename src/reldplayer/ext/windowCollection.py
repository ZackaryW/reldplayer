from functools import cached_property
from reldplayer.ext.window import LDWindow
import typing



class _Layout:
    def __init__(self, c: "LDWindowCollection"):
        self.__c = c

    def grid(
        self,
        rows: int,
        cols: int,
        *,
        maxwidth: float | None = None,
        maxheight: float | None = None,
        minwidth: float | None = None,
        minheight: float | None = None,
        monitor: int = 0,
        sleepTime: float = 0.2,
    ):
        from reldplayer.utils import grid_orientation

        grid_orientation(
            [x.wnd for x in self.__c],
            rows,
            cols,
            maxwidth=maxwidth,
            maxheight=maxheight,
            minwidth=minwidth,
            minheight=minheight,
            monitor=monitor,
            sleepTime=sleepTime,
        )


class LDWindowCollection(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert all(isinstance(x, LDWindow) for x in self)

    def __setitem__(self, index, value):
        assert isinstance(value, LDWindow)
        super().__setitem__(index, value)

    def append(self, value):
        assert isinstance(value, LDWindow)
        super().append(value)

    def extend(self, value):
        assert all(isinstance(x, LDWindow) for x in value)
        super().extend(value)

    def insert(self, index, value):
        assert isinstance(value, LDWindow)
        super().insert(index, value)

    def __iter__(self) -> typing.Iterator[LDWindow]:
        return super().__iter__()

    @cached_property
    def LAYOUT(self):
        return _Layout(self)


def asCollection(iter: typing.Iterable[LDWindow]) -> LDWindowCollection:
    return LDWindowCollection(iter)
