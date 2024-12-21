from commands.base import Command
from models.room import Room
from services.character import CharacterService
from services.session import TextSession, renderer


class WaypointCommand(Command):
    command_prefixes = ["waypoint ", "waypoints"]
    command_format = ["waypoint <nickname>"]

    @classmethod
    async def telnet(
        cls, reader, writer, mqtt_client, command: str, session: TextSession
    ):
        command, command_prefix = cls.get_arguments(command), cls.get_command_prefix(command)
        if command_prefix.strip() == "waypoints":
            if waypoints := session.character.properties.get(
                "waypoints", {}
            ).items():
                for waypoint in waypoints:
                    room = Room.objects.get(id=waypoint[1])
                    writer.write(f"{str(waypoint[0])}: {room.name}{renderer.nl}")
            return

        elif not command.strip().lower():
            writer.write(f"You must give your waypoint a name.{renderer.nl}")
            return

        props = session.character.properties.get("waypoints", {})
        props[command] = session.character.room.id
        CharacterService.update_property(session, session.character.id, {"waypoints": props})
        writer.write(f"Your waypoint {command} has been set.{renderer.nl}")
