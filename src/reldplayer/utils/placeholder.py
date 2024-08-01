from reldplayer.batch_window import LDBatchWindow
from . import grid_orientation as _g


def grid_orientation(
    ldbw: LDBatchWindow,
    monitor: int = 0,
    col: int = 0,
    row: int = 0,
    colrow: str = None,
    sleepTime: float = 0.2,
):
    windows = [ldw.window for ldw in ldbw.windows]
    if colrow is not None:
        col, row = colrow.split(",")
    return _g(windows, monitor=monitor, col=col, row=row, sleepTime=sleepTime)
