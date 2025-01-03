from commands.text.base import Command
from models.room import Room
from services.character import CharacterService
from services.session import TextSession
from templates.room.text import RoomTextTemplate
from templates.utils.text.graphics import TextGraphicsRenderer

ren = TextGraphicsRenderer()


class WarpCommand(Command):
    command_prefixes = ["warp "]

    @classmethod
    async def do(cls, session: TextSession, room_cid: int) -> bool:
        if Room.objects(cId=room_cid).first():
            CharacterService.warp(session, room_cid=str(room_cid))
            session.character.reload()
            return True
        else:
            return False

    @classmethod
    async def telnet(
        cls, reader, writer, mqtt_client, command: str, session: "TextSession"
    ):
        command = cls.get_arguments(command)

        if command.startswith("#"):
            command = command[1:]

        try:
            room_cid = int(command)
        except ValueError:
            room_cid = None

        if len(command) != 0 and await cls.do(session, room_cid):
            writer.write(
                RoomTextTemplate(session).get(session.character.room, session.character)
            )
        else:
            writer.write(f"I can't warp to that room.{ren.nl}")
