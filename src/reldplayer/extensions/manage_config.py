import os
import typing
import zrcl4.json as json

from reldplayer.core.player import Player
from reldplayer.internal.model_config import LeidiansConfig
from reldplayer.internal.model_mps import SMP, KeyboardMapping
from reldplayer.internal.model_profile_config import LeidianConfig


class ManageConfig:
    def __init__(self, player: Player):
        self.__player = player

    def get_default_config(self) -> LeidiansConfig:
        data = json.read_json(
            os.path.join(self.__player._config.vms_folder, "config", "leidians.config")
        )
        return data

    def save_default_config(self, data: LeidiansConfig):
        json.write_json(
            os.path.join(self.__player._config.vms_folder, "config", "leidians.config"),
            data,
        )

    def get_config(self, id: int = None) -> LeidianConfig:
        if id is None:
            if not self.__player._ctx.selected:
                raise ValueError("no selection")
            id = self.__player._ctx.selected[0]

        cfgpath = os.path.join(
            self.__player._config.vms_folder, "config", f"leidian{id}.config"
        )
        if not os.path.exists(cfgpath):
            raise ValueError(f"config not found: {cfgpath}")

        data = json.read_json(cfgpath)
        return json.parse_dotted_dict(data)

    def save_config(self, *args, id: int = None, data: LeidianConfig = None):
        if len(args) == 1 and isinstance(args[0], dict):
            data = args[0]
        elif len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], dict):
            id = args[0]
            data = args[1]
        elif len(args) == 0:
            pass
        else:
            raise ValueError("invalid args")

        if id is None:
            if not self.__player._ctx.selected:
                raise ValueError("no selection")
            id = self.__player._ctx.selected[0]

        cfgpath = os.path.join(
            self.__player._config.vms_folder, "config", f"leidian{id}.config"
        )
        flatten = json.flatten_nested_dict(data)
        json.write_json(cfgpath, flatten)

    def list_smps(self, type: typing.Literal["customize", "recommended"]):
        path = (
            self.__player._config.customize_configs_folder
            if type == "customize"
            else self.__player._config.recommend_configs_folder
        )

        return [
            os.path.splitext(os.path.basename(x))[0]
            for x in os.listdir(path)
            if os.path.splitext(x)[1] == ".smp"
        ]

    def get_smp(
        self, name: str, fromloc: typing.Literal["customize", "recommended"]
    ) -> SMP:
        path = (
            self.__player._config.customize_configs_folder
            if fromloc == "customize"
            else self.__player._config.recommend_configs_folder
        )
        return json.read_json(os.path.join(path, f"{name}.smp"))

    def save_smp(
        self, name: str, fromloc: typing.Literal["customize", "recommended"], data: SMP
    ):
        path = (
            self.__player._config.customize_configs_folder
            if fromloc == "customize"
            else self.__player._config.recommend_configs_folder
        )
        json.write_json(os.path.join(path, f"{name}.smp"), data)

    def list_keyboard_mapping(self, type: typing.Literal["customize", "recommended"]):
        path = (
            self.__player._config.customize_configs_folder
            if type == "customize"
            else self.__player._config.recommend_configs_folder
        )
        return [
            os.path.splitext(os.path.basename(x))[0]
            for x in os.listdir(path)
            if os.path.splitext(x)[1] == ".kmp"
        ]

    def get_keyboard_mapping(
        self, name: str, fromloc: typing.Literal["customize", "recommended"]
    ) -> KeyboardMapping:
        path = (
            self.__player._config.customize_configs_folder
            if fromloc == "customize"
            else self.__player._config.recommend_configs_folder
        )
        data = json.read_json(os.path.join(path, f"{name}.kmp"))
        return KeyboardMapping.from_dict(data)

    def save_keyboard_mapping(
        self,
        name: str,
        fromloc: typing.Literal["customize", "recommended"],
        data: KeyboardMapping,
    ):
        path = (
            self.__player._config.customize_configs_folder
            if fromloc == "customize"
            else self.__player._config.recommend_configs_folder
        )
        json.write_json(os.path.join(path, f"{name}.kmp"), data.to_dict())
