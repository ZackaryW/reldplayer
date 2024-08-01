from typing import Any
from pyldplayer import Console


class ConsoleDispatchCls:
    console: Console

    def __init__(self):
        try:
            self.__console = self.console
            self.__dispatch__()
        except:  # noqa
            self.__alternative_init__()

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "console":
            if not isinstance(value, Console):
                raise TypeError("console must be a Console object")

            self.__console = value
            self.__dispatch__()
        else:
            super().__setattr__(name, value)

    def __dispatch__(self):
        pass

    def __alternative_init__(self):
        pass

    def __getattribute__(self, name: str) -> Any:
        if name.startswith("__"):
            return super().__getattribute__(name)

        if name.startswith(f"_{self.__class__.__name__}__") and hasattr(
            self, f"_ConsoleDispatchCls__{name.split("__", 1)[1]}"
        ):
            return super().__getattribute__(
                f"_ConsoleDispatchCls__{name.split("__", 1)[1]}"
            )

        return super().__getattribute__(name)
