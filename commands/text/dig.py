from commands.text.base import Command
from models.portal import PortalCreateDTO
from models.room import RoomCreateDTO
from services.portal import PortalService
from services.room import RoomService
from services.session import TextSession


class DigCommand(Command):
    command_prefixes = ["@dig "]
    minimum_args = 3

    @classmethod
    async def telnet(
        cls, reader, writer, mqtt_client, command: str, session: "TextSession"
    ):
        args = cls.parse_args(cls.get_arguments(command))

        directions = args[1].split(" ", -1)

        if len(directions) != 3:
            writer.write("I need the name of the room to build, a name for the portal and the direction aliases to "
                         "dig.")
            return

        room_to_build = RoomCreateDTO(
            owner=str(session.character.id),
            name=args[0],
            description=args[0],
        )

        if new_room := RoomService.create(room_to_build):
            path_to_dig = PortalService.create(
                PortalCreateDTO(
                    name=directions[0],
                    to_room=str(new_room.id),
                    from_room=str(session.character.room.id),
                    alias_from=[directions[1]],
                    alias_to=[directions[2]],
                    owner=str(session.character.id),
                    reversible=True
                )
            )
            writer.write(f"Created new rom and path {room_to_build.name}, {path_to_dig.name}.")
            return

        writer.write(f"I could not create room {room_to_build.name}.")
