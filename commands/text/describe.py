from commands.text.base import Command
from services.room import RoomService
from services.session import TextSession


class DescribeCommand(Command):
    command_prefixes = ["@describe "]

    @classmethod
    async def telnet(
        cls, reader, writer, mqtt_client, command: str, session: "TextSession"
    ):
        args = cls.parse_args(cls.get_arguments(command))

        if args[0] == "here":
            if room_rename := RoomService.describe(session.character.room.id, args[1]):
                writer.write(f"You gave this room a new description: {room_rename.description}.")
                return
