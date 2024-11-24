from pyldplayer.coms.appattr import LDAppAttr
from reldplayer.overloads.load import pyldplayer_curr_load, lookup_path_via_proc


LDAppAttr._registerDefaultMethodOverload(pyldplayer_curr_load)
LDAppAttr._registerDefaultMethodOverload(lookup_path_via_proc)

__all__ = ["undone_overloads"]


def undone_overloads():
    try:
        LDAppAttr._defaultMethodOverloads.remove(pyldplayer_curr_load)
    except ValueError:
        pass
    try:
        LDAppAttr._defaultMethodOverloads.remove(lookup_path_via_proc)
    except ValueError:
        pass
