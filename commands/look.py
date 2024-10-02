from commands.base import Command
from services.session import TextSession
from templates.character.text import CharacterText
from templates.room.text import RoomText
from templates.text import BaseTextTemplate as Btt


class LookCommand(Command):
    command_prefixes = ["look", "me"]

    @classmethod
    async def telnet(cls, reader, writer, mqtt_client, command: str, session: TextSession):
        command, target = cls.parse_command_verb_and_target(command)
        if command == "me":
            command, target = 'look', 'me'

        if len(command) == 0 or target is None:
            writer.write("You stare off, gazing into nothing." + Btt.NEWLINE)
            return
        else:
            if target.lower() == "me":
                # Describe the room the current character
                writer.write(CharacterText.get(session.character))
                return

            if target.lower() in ["here", "around"]:
                # Describe the room the character is currently in
                writer.write(RoomText.get(session.character.room, session.character))
                return

            if target.lower() in ["in", "inside", "into"]:
                # TODO: Do something to an object here
                a = 1
                return
