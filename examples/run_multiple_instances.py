
from reldplayer.batch_selector import LDBatchSelector
from reldplayer.batch_console import LDBatchConsole
from reldplayer.quick import Global, Console

Global()
LDBatchSelector.console = (c:=Console.auto())
selector : LDBatchSelector = LDBatchSelector(
    "between_id(1, 10) and not active() and name_pattern({yourpattern})"
)
console = LDBatchConsole(selector)
console.launch()
