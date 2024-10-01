from abc import ABC, abstractmethod
from typing import List

import commands
from utils.system import import_modules


class Command(ABC):
    command_prefixes: List[str]

    errors = {
        "not_enough_arguments": "You must give the command some arguments.",
        "unknown_command": "That is not a valid command.",
        "not_a_character": "You must be in a character to use that command.",
        "not_in_room": "You must be in the room to use that command.",
        "not_enough_permissions": "You do not have the permissions to use that command.",
        "not_a_number": "You must give a number.",
        "not_a_valid_object": "That is not a valid object.",
        "not_a_valid_room": "That is not a valid room.",
        "not_a_valid_character": "That is not a valid character.",
    }

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
    return import_modules(commands.__all__,
                          'telnet',
                          "commands.",
                          "Command")
