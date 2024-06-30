import importlib
from abc import ABC, abstractmethod
from typing import List

import commands


class Command(ABC):
    command_prefixes: List[str]

    @classmethod
    @abstractmethod
    async def telnet(cls, reader, writer, mqtt_client, command: str, session: "TextSession") -> str | None:
        pass

    @classmethod
    def get_command_prefix(cls, command):
        for prefix in cls.command_prefixes:
            if command.lower().startswith(prefix):
                return (command[:len(prefix)]
                        .strip())

    @classmethod
    def get_arguments(cls, command):
        for prefix in cls.command_prefixes:
            if command.lower().startswith(prefix):
                return (command[len(prefix):]
                        .strip())

    @classmethod
    def parse_args(cls, args):
        parsed_arguments = args.split(' ', 1)
        for arg_wrapper in ['"', "'"]:
            if arg_wrapper in args:
                parsed_arguments = [line for line in [line.strip() for line in args.split(arg_wrapper)] if line]
        return list(filter(lambda item: item != "", parsed_arguments))

    @classmethod
    def parse_command_verb_and_target(cls, command: str):
        useless_prepositions = ["at"]
        command_alias = command.split()[0]
        target = command.split()[1:]

        if len(target) > 0 and target[0] in useless_prepositions:
            target = target[1:]

        if len(target) == 0:
            return command_alias, None

        return command_alias, " ".join(target)


def get_command_modules() -> List[Command]:
    command_modules = []
    for module_path in commands.__all__:
        module = getattr(importlib.import_module("commands." + module_path), module_path.title() + "Command")
        if hasattr(module, "telnet"):
            command_modules.append(module)
    return command_modules
