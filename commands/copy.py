from commands.base import Command
from models.object import Object
from services.session import TextSession


class CopyCommand(Command):
    command_prefixes = ["@copy "]
    args = 2

    @classmethod
    async def telnet(
        cls, reader, writer, mqtt_client, command: str, session: "TextSession"
    ):

        args = cls.parse_args(cls.get_arguments(command))

        if len(args) != cls.args:
            writer.write(
                "I need the name of the object to copy and a new name to give it."
            )
            return

        object_to_copy_name, object_new_name = args
        object_to_copy = Object.objects(name=object_to_copy_name).first()
        if object_to_copy is None:
            writer.write(f"I could not find an object named '{object_to_copy_name}'.")
        else:
            new_object = Object.objects.create(
                name=object_new_name,
                parent=object_to_copy.parent,
                owner=session.character.id,
                description=object_to_copy.description,
                room=session.character.room.id,
                properties=object_to_copy.properties,
            )

            writer.write(f"You create {new_object.name} with ID {new_object.id}.")
