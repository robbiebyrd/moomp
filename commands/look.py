from functools import partial
from operator import is_not

from commands.base import Command
from services.room import RoomService
from services.session import TextSession
from templates.character.text import CharacterTextTemplate
from templates.object.text import ObjectTextTemplate
from templates.portal.text import PortalTextTemplate
from templates.room.text import RoomTextTemplate


class LookCommand(Command):
    command_prefixes = ["look", "me"]

    @classmethod
    async def telnet(
        cls, reader, writer, mqtt_client, command: str, session: TextSession
    ):
        command, target = (
            ("look", "me")
            if command == "me"
            else cls.parse_command_verb_and_target(command)
        )

        here = RoomService.here(session.character.room.id)

        characters = list(
            filter(
                partial(is_not, None),
                map(
                    lambda x: x if x.id != session.character.id else None,
                    here.get("characters"),
                ),
            )
        )

        if len(command) == 0 or target is None:
            writer.write(f"You stare off, gazing into nothing.{session.ren.nl}")
            return

        if target.lower() in ["me", session.character.name.lower()]:
            writer.write(CharacterTextTemplate(session).get(session.character))
            return

        if target.lower() in ["here", "around", session.character.room.name.lower()]:
            writer.write(
                RoomTextTemplate(session).get(session.character.room, session.character)
            )
            return

        for char in characters:
            if char.name.lower() == target.lower():
                writer.write(CharacterTextTemplate(session).get(char))
                return

        for obj in here.get("objects"):
            if obj.name.lower() == target.lower():
                writer.write(ObjectTextTemplate(session).get(obj))
                return

        for inv in session.character.inventory():
            if inv.name.lower() == target.lower():
                writer.write(ObjectTextTemplate(session).get(inv))
                return

        if target.lower() in RoomService.exits_and_aliases(session.character.room.id):
            to, portal, room = RoomService.resolve_alias(
                session.character.room.id, target.lower()
            )
            writer.write(PortalTextTemplate(session).get(portal, room, to))
            return
