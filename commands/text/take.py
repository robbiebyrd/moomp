from commands.text.base import Command
from middleware.updater import notify_and_create_event
from models.object import Object
from services.session import TextSession


class TakeCommand(Command):
    positive_command_prefixes = ["take", "pick up"]
    negative_command_prefixes = ["drop", "put down"]
    command_prefixes = list(set(positive_command_prefixes + negative_command_prefixes))

    responses = {
        "success": "You took '{command}'.{nl}",
        "error_no_subject": "I can't take that.{nl}",
        "error_drop_no_subject": "I can't drop that.{nl}",
        "error": "I can't take '{command}'.{nl}",
        "success_drop": "You drop '{command}'.{nl}",
        "error_drop_possession": "You can't drop '{command}' because you don't have it.{nl}",
    }

    @classmethod
    def get(cls, command: str, session: TextSession, operation: str):
        args =  {}

        match operation:
            case "drop":
                args["holder"] = session.character
            case "take":
                args["room"] = session.character.room

        if command.startswith("#"):
            args["cId"] = command[1:]
        else:
            args["name"] = command

        return Object.objects(**args).first()

    @classmethod
    async def take(cls, command: str, session: TextSession) -> bool:
        if obj := cls.get(command, session, "take"):
            obj.room = None
            obj.holder = session.character
            obj.save()
            await cls.notify(obj, "taken", session)
            return True

        return False

    @classmethod
    async def drop(cls, command: str, session: TextSession) -> bool:
        if obj := cls.get(command, session, "drop"):
            obj.room = session.character.room
            obj.holder = None
            obj.save()
            await cls.notify(obj, "dropped", session)
            return True

        return False

    @classmethod
    async def notify(cls, obj: Object, operation: str, session: "TextSession"):
        notify_and_create_event(
            instance=session.instance,
            document_type="Object",
            document=obj,
            document_operation=operation.title(),
            operator_type="Character",
            operator=session.character,
        )


    @classmethod
    async def telnet(cls, reader, writer, mqtt_client, command: str, session: "TextSession"):
        command, command_prefix = cls.get_arguments(command), cls.get_command_prefix(command)
        if command_prefix in cls.positive_command_prefixes:
            if len(command.strip()) == 0:
                writer.write(cls.responses.get("error_no_subject").format(nl=session.ren.nl))
                return
            if await cls.take(command, session):
                writer.write(cls.responses.get("success").format(command=command, nl=session.ren.nl))
            else:
                writer.write(cls.responses.get("error").format(command=command, nl=session.ren.nl))
        elif command_prefix in cls.negative_command_prefixes:
            if len(command.strip()) == 0:
                writer.write(cls.responses.get("error_drop_no_subject").format(nl=session.ren.nl))
            if await cls.drop(command, session):
                writer.write(cls.responses.get("success_drop").format(command=command, nl=session.ren.nl))
            else:
                writer.write(cls.responses.get("error_drop_possession").format(command=command, nl=session.ren.nl))
