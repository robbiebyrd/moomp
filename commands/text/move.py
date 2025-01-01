from commands.text.base import Command
from services.character import CharacterService
from services.room import RoomService
from services.session import TextSession
from templates.room.text import RoomTextTemplate


class MoveCommand(Command):
    command_prefixes = ["go ", "walk ", "move ", "@move "]

    @classmethod
    async def do(cls, command: str, session: TextSession) -> bool:
        if command in RoomService.exits_and_aliases(session.character.room.id):
            CharacterService.move(session, direction=command)
            session.character.reload()
            return True
        else:
            return False

    @classmethod
    async def telnet(
        cls, reader, writer, mqtt_client, command: str, session: "TextSession"
    ):
        command = cls.get_arguments(command)
        if len(command) != 0 and await cls.do(command, session):
            writer.write(
                RoomTextTemplate(session).get(session.character.room, session.character)
            )
        else:
            writer.write(f"I can't go that way.{session.ren.nl}")
