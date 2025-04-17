from commands.text.base import Command
from services.character import CharacterService
from services.room import RoomService
from services.session import TextSession


class RenameCommand(Command):
    command_prefixes = ["@rename "]

    @classmethod
    async def telnet(
        cls, reader, writer, mqtt_client, command: str, session: "TextSession"
    ):
        args = cls.parse_args(cls.get_arguments(command))

        if args[0] == "me":
            if character_rename := CharacterService.rename(session.character.id, args[1]):
                writer.write(f"You renamed your character to {character_rename.name}.")
                return

        if args[0] == "alias":
            CharacterService.rename(session.character.id, args[1])
            writer.write(f"You changed your character alias to {args[1]}.")
            return

        if args[0] == "here":
            if room_rename := RoomService.rename(session.character.room.id, args[1]):
                writer.write(f"You renamed this room to {room_rename.name}.")
                return
