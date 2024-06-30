from commands.base import Command
from services.character import CharacterService
from services.session import TextSession
from services.telnet import TelnetService
from templates.room.text import RoomText


class MoveCommand(Command):
    command_prefixes = ["go ", "walk ", "move ", "_move "]

    @classmethod
    async def do(cls, command: str, session: TextSession) -> bool:
        if command in RoomText.get_exit_aliases(session.character.room, True, True):
            CharacterService.move(session.character.id, direction=command)
            session.character.reload()
            return True
        else:
            return False

    @classmethod
    async def telnet(cls, reader, writer, mqtt_client, command: str, session: "TextSession"):
        ts = TelnetService(reader, writer, session)
        command = cls.get_arguments(command)
        if len(command) == 0:
            ts.write_line("I can't go that way.")

        if await cls.do(command, session):
            ts.write_line(RoomText.get(session.character.room, session.character))
            return

        ts.write_line("I can't go that way.")
