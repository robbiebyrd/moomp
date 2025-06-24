from commands.text.base import Command
from services.room import RoomService
from services.session import TextSession


class HideCommand(Command):
    command_prefixes = ["@hide "]

    @classmethod
    async def telnet(
        cls, reader, writer, mqtt_client, command: str, session: "TextSession"
    ):
        args = cls.parse_args(cls.get_arguments(command))

        if args[0] == "here":
            room = session.character.room
            if args[1].startswith("y"):
                RoomService.hide(room.id, True)
                writer.write(f"You hid room {room.name}.")
            elif args[1].startswith("n"):
                RoomService.hide(room.id, False)
                writer.write(f"You made room {room.name} visible.")
            else:
                RoomService.hide(room.id, not session.character.room.hidden)
                writer.write(f"You made room {room.name} {'not hidden' if room.hidden else 'hidden'}.")
            return

        writer.write(f"Could not hide {args[0]}.")
