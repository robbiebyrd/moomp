from commands.base import Command
from models.object import Object
from services.session import TextSession
from templates.text import BaseTextTemplate as Btt


class TakeCommand(Command):
    positive_command_prefixes = ["take ", "pick up ", "drop ", "put down "]
    negative_command_prefixes = ["take ", "pick up ", "drop ", "put down "]
    command_prefixes = list(set(positive_command_prefixes + negative_command_prefixes))

    @classmethod
    async def take(cls, command: str, session: TextSession) -> bool:
        obj = Object.objects(name=command, room=session.character.room).first()

        if obj is not None:
            obj.room = None
            obj.holder = session.character
            obj.save()
            return True

        return False

    @classmethod
    async def drop(cls, command: str, session: TextSession) -> bool:
        obj = Object.objects(name=command, holder=session.character).first()

        if obj is not None:
            obj.room = session.character.room
            obj.holder = None
            obj.save()
            return True

        return False

    @classmethod
    async def telnet(cls, reader, writer, mqtt_client, command: str, session: "TextSession"):
        command, command_prefix = cls.get_arguments(command), cls.get_command_prefix(command)

        if len(command) == 0:
            writer.write(f"I can't take that.{Btt.NEWLINE}")

        if command_prefix == "take":
            if await cls.take(command, session):
                writer.write(f"You took '{command}'.{Btt.NEWLINE}")
            else:
                writer.write(f"I can't take '{command}'.{Btt.NEWLINE}")
        elif command_prefix == "drop":
            if await cls.drop(command, session):
                writer.write(f"You drop '{command}'.{Btt.NEWLINE}")
            else:
                writer.write(f"You can't drop '{command}' because you don't have it.{Btt.NEWLINE}")
