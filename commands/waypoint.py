from commands.base import Command
from services.character import CharacterService
from services.session import TextSession


class WaypointCommand(Command):
    command_prefixes = ["waypoint ", "waypoints "]
    command_format = ["waypoint <nickname>"]

    @classmethod
    async def telnet(
        cls, reader, writer, mqtt_client, command: str, session: TextSession
    ):
        command = "".join(command.split()[:1])
        command_properties = " ".join(command.split()[1:])
        if command == "waypoints":
            # TODO: Need to return the list of waypoints
            pass

        if len(command_properties.strip().lower()) == 0:
            writer.write("You must give your waypoint a name.")
            return

        props = session.character.properties.get("waypoints", {})
        props[command_properties] = session.character.room.id
        CharacterService.update_property(session.character.id, {"waypoints": props})
        writer.write(f"Your waypoint {command_properties} has been set.")
