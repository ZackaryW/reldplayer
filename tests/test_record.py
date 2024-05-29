from reldplayer import Player, PlayerConfig
from reldplayer.internal.model_record import OperationRecord

def test_record_fetch():
    x = Player(PlayerConfig.auto())
    re = x.manage_macro.list_records()
    re1 = x.manage_macro.list_records(True)

    re2 = x.manage_macro.get_record(re[0], native=True)
    re3 = x.manage_macro.get_record(re[0], native=False)

    assert re == re1
    assert isinstance(re2, dict)
    assert isinstance(re3, OperationRecord)
    assert re2["info"] == re3.recordInfo