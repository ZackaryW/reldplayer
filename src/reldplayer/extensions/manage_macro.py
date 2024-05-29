import os
import typing
from reldplayer.core.player import Player
from reldplayer.internal.model_record import OperationRecord, ReturnInfo
from zrcl4.json import read_json, write_json
from dataclasses import asdict


class ManageMacro:
    def __init__(self, player: Player):
        self.__player = player

    def list_records(self, native: bool = False):
        if native:
            return [x["file"][:-7] for x in self.__player.raw_console.operatelist(0)]

        files = [
            x[:-7]
            for x in os.listdir(self.__player._config.operation_records_folder)
            if x.endswith(".record")
        ]

        return files

    def get_record(
        self, name: str, native: bool = False
    ) -> typing.Union[ReturnInfo, OperationRecord]:
        if native:
            return self.__player.raw_console.operateinfo(
                0,
                filepath=name + ".record",
            )
        else:
            data = read_json(
                os.path.join(
                    self.__player._config.operation_records_folder, name + ".record"
                )
            )

            return OperationRecord(**data)

    def save_record(self, name: str, data: OperationRecord):
        if not os.path.exists(self.__player._config.operation_records_folder):
            os.makedirs(self.__player._config.operation_records_folder)

        write_json(
            os.path.join(
                self.__player._config.operation_records_folder, name + ".record"
            ),
            asdict(data),
        )
