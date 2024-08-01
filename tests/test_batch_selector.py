import os
from reldplayer.batch_selector import LDBatchSelector
from reldplayer.quick import Console, Global

def test_batch_selector_1():
    Global(os.environ["LDCONSOLE_PATH"])
    LDBatchSelector.console = (c:=Console.auto())
    assert isinstance(c, Console)
    selector : LDBatchSelector = LDBatchSelector("between_id(1, 10) and not active() and name_pattern('arknights*')")
    assert len(selector.selectedIDs) == 2

