
from reldplayer.quick import Global
from reldplayer import grid_orientation, LDBatchSelector, LDBatchWindow

Global()
selector : LDBatchSelector = LDBatchSelector(
    '{your query}'
)
bw = LDBatchWindow(selector)
grid_orientation(bw, monitor=2, row=2, col=2)