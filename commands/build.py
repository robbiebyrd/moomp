from commands.base import Command
from models.room import RoomCreateDTO
from services.room import RoomService
from services.session import TextSession


class BuildCommand(Command):
    command_prefixes = ["@build ", "@dig "]
    minimum_args = 1

    @classmethod
    async def telnet(
        cls, reader, writer, mqtt_client, command: str, session: "TextSession"
    ):
        command_prefix = str(cls.get_command_prefix(command))
        args = cls.parse_args(cls.get_arguments(command))

        if len(args) != cls.minimum_args:
            writer.write("I need the name of the room to build.")
            return

        if len(args) == 1:
            args = [args[0], args[0]]

        room_to_build = RoomCreateDTO(
            owner=session.character.id,
            name=args[0],
            description=args[1],
        )
        RoomService.create(room_to_build)

        match command_prefix:
            case "@build":
                pass
            case "@dig":
                pass
