from dataclasses import dataclass
import typing


@dataclass
class PlayerCtx:
    selected: typing.List[int] = None

    @property
    def primary(self) -> int:
        if not self.selected:
            return None
        return self.selected[0]
