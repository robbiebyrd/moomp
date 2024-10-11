from commands.base import Command
from models.object import Object
from services.session import TextSession
from templates.utils.text.color import ColorTextRenderer

renderer = ColorTextRenderer()


class TakeCommand(Command):
    positive_command_prefixes = ["take", "pick up"]
    negative_command_prefixes = ["drop", "put down"]
    command_prefixes = list(set(positive_command_prefixes + negative_command_prefixes))

    error_messages = {
        'success': "You took '{command}'.{nl}",
        'error_no_subject': "I can't take that.{nl}",
        'error_drop_no_subject': "I can't drop that.{nl}",
        'error': "I can't take '{command}'.{nl}",
        'success_drop': "You drop '{command}'.{nl}",
        'error_drop_possession': "You can't drop '{command}' because you don't have it.{nl}"
    }

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

        if command_prefix in cls.positive_command_prefixes:
            if len(command.strip()) == 0:
                writer.write(cls.error_messages.get('error_no_subject').format(nl=renderer.nl))

            elif await cls.take(command, session):
                writer.write(cls.error_messages.get('success').format(command=command, nl=renderer.nl))
            else:
                writer.write(cls.error_messages.get('error').format(command=command, nl=renderer.nl))
        elif command_prefix in cls.negative_command_prefixes:
            if len(command.strip()) == 0:
                writer.write(cls.error_messages.get('error_drop_no_subject').format(nl=renderer.nl))

            if await cls.drop(command, session):
                writer.write(cls.error_messages.get('success_drop').format(command=command, nl=renderer.nl))
            else:
                writer.write(cls.error_messages.get('error_drop_possession').format(command=command, nl=renderer.nl))
