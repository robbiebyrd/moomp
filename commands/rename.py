from commands.base import Command
from services.character import CharacterService
from services.session import TextSession


class RenameCommand(Command):
    command_prefixes = ["@rename "]

    @classmethod
    async def telnet(
        cls, reader, writer, mqtt_client, command: str, session: "TextSession"
    ):

        for prefix in cls.command_prefixes:
            if command.lower().startswith(prefix):
                command = command[len(prefix) :]
                break

        command = command.strip().split()

        if command[0] == "me":
            CharacterService.rename(session.character.id, command[1])
