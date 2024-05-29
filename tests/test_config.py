from reldplayer import Player, PlayerConfig
#from zrcl4.typing import is_valid_typeddict

from reldplayer.internal.model_config import LeidiansConfig
from reldplayer.internal.model_profile_config import LeidianConfig

def test_config_1():
    x = Player(PlayerConfig.auto())
    l1 = x.manage_config.get_default_config()
    l2 = x.manage_config.get_config(0)
    assert isinstance(l1, dict)
    assert isinstance(l2, dict)

    assert all(x in l1 for x in LeidiansConfig.__annotations__.keys() if x != "lastIP")
    assert all(x in  LeidianConfig.__annotations__.keys() for x in l2)

    #assert is_valid_typeddict(l1, LeidiansConfig)
    #assert is_valid_typeddict(l2, LeidianConfig)