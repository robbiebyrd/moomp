from commands.base import Command
from services.room import RoomService
from services.session import TextSession
from templates.character.text import CharacterTextTemplate
from templates.object.text import ObjectTextTemplate
from templates.portal.text import PortalTextTemplate
from templates.room.text import RoomTextTemplate
from templates.utils.text.color import ColorTextRenderer

renderer = ColorTextRenderer()


class LookCommand(Command):
    command_prefixes = ["look", "me"]

    @classmethod
    async def telnet(cls, reader, writer, mqtt_client, command: str, session: TextSession):
        command, target = ('look', 'me') if command == "me" else cls.parse_command_verb_and_target(command)

        here = RoomService.here(session.character.room.id)

        objs = here.get("objects")
        characters = list(
            filter(
                lambda s: s is not None,
                map(lambda x: x if x.id != session.character.id else None, here.get("characters")),
            )
        )
        exits = RoomService.exits_and_aliases(session.character.room.id)

        if len(command) == 0 or target is None:
            writer.write(f"You stare off, gazing into nothing.{renderer.nl}")

        elif target.lower() in ["me", session.character.name.lower()]:
            writer.write(CharacterTextTemplate.get(session.character))

        elif target.lower() in ["here", "around", session.character.room.name.lower()]:
            writer.write(RoomTextTemplate.get(session.character.room, session.character))

        elif target.lower() in ["in", "inside", "into"]:
            # TODO: Do something to an object here
            a = 1


        elif target.lower() in list(map(lambda x: x.name.lower(), characters)):
            for char in characters:
                if char.name.lower() == target.lower():
                    writer.write(CharacterTextTemplate.get(char))

        elif target.lower() in list(map(lambda x: x.name.lower(), objs)):
            for obj in objs:
                if obj.name.lower() == target.lower():
                    writer.write(ObjectTextTemplate.get(obj))

        elif target.lower() in exits:
            to, portal, room = RoomService.resolve_alias(session.character.room.id, target.lower())
            writer.write(PortalTextTemplate.get(portal, room, to))
