from commands.base import Command
from models.room import Room
from services.character import CharacterService
from services.session import TextSession
from templates.room.text import RoomTextTemplate
from templates.utils.text.graphics import TextGraphicsRenderer

ren = TextGraphicsRenderer()


class WarpCommand(Command):
    command_prefixes = ["warp "]

    @classmethod
    async def do(cls, room_cid: str, session: TextSession) -> bool:
        if Room.objects(cId=room_cid).first():
            CharacterService.warp(session.character.id, room_cid=room_cid)
            session.character.reload()
            return True
        else:
            return False

    @classmethod
    async def telnet(
        cls, reader, writer, mqtt_client, command: str, session: "TextSession"
    ):
        command = cls.get_arguments(command)

        try:
            room_cid = int(command)
        except ValueError:
            room_cid = None

        if len(command) != 0 and await cls.do(room_cid, session):
            writer.write(
                RoomTextTemplate(session).get(session.character.room, session.character)
            )
        else:
            writer.write(f"I can't warp to that room.{ren.nl}")
