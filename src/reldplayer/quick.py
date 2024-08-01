import os
from typing import List
from pyldplayer import *  # noqa
import pyldplayer as _internal
from pyldplayer import Console as _Console
from pyldplayer._internal.model.list2meta import List2Meta

from reldplayer.utils.timely import timely


def Global(path: str = None):
    if "PYLDPLAYER_CURR" in os.environ:
        path = os.environ["PYLDPLAYER_CURR"]

    if not path and "PYLDPLAYER_PATH" in os.environ:
        path = os.environ["PYLDPLAYER_PATH"]

    try:
        return _internal.Global(path)
    except Exception:
        pass

    # try get using psutil


class Console(_Console):
    def __hash__(self):
        return hash(self.path._LDPath__path)

    @timely(1)
    def list2(self) -> List[List2Meta]:
        return super().list2()
