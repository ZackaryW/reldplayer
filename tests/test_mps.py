

from reldplayer.core.player import Player, PlayerConfig
from zrcl4.typing import is_valid_typeddict

from reldplayer.internal.model_mps import SMP, KeyboardMapping


def test_smp_1():
    x = Player(PlayerConfig.auto())
    smps = x.manage_config.list_smps("customize")
    smps2 = x.manage_config.list_smps("recommended")
    assert len(smps) > 0 or len(smps2) > 0, "no smp found"
    smps = smps if len(smps) > 0 else smps2
    smp = x.manage_config.get_smp(smps[0], "customize")

    assert is_valid_typeddict(smp, SMP)

def test_kmp_1():
    x = Player(PlayerConfig.auto())
    kmps = x.manage_config.list_keyboard_mapping("customize")
    kmps2 = x.manage_config.list_keyboard_mapping("recommended")
    assert len(kmps) > 0 or len(kmps2) > 0, "no kmp found"
    kmps = kmps if len(kmps) > 0 else kmps2
    kmp = x.manage_config.get_keyboard_mapping(kmps[0], "customize")

    assert isinstance(kmp, KeyboardMapping)