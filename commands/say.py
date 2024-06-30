import json
import os

import paho.mqtt.publish as publish
from pluralizer import Pluralizer

from commands.base import Command
from models.speech import Speech
from services.portal import PortalService
from services.telnet import TelnetService
from services.telnet import TextSession


class SayCommand(Command):
    command_prefixes = ["say ", "speak ", '"', "'", "shout ", "scream ", "yell ", "emote "]
    private_message_command_prefixes = []

    @classmethod
    async def notify(cls, document: Speech, session: "TextSession"):
        # Make a shallow copy of the document object for filtering.
        doc = json.loads(document.to_json())

        messages = ([
                        {
                            "topic": f"/Speech/{document.id}/Room/{room.id}/Speaker/{session.character.id}",
                            "payload": json.dumps(doc)
                        } for room in document.rooms
                    ] + [
                        {
                            "topic": f"/Speech/{document.id}/Listener/{listener.id}/Speaker/{session.character.id}",
                            "payload": json.dumps(doc)
                        } for listener in document.listeners
                    ]
                    )

        publish.multiple(messages,
                         hostname=os.environ.get("MQTT_HOST"),
                         port=int(os.environ.get("MQTT_PORT")),
                         )

    @classmethod
    async def telnet(cls, reader, writer, mqtt_client, command: str, session: "TextSession"):
        prefix = cls.get_command_prefix(command)
        if not command.startswith("'") or not command.startswith('"'):
            command = cls.get_arguments(command)

        command.strip()

        def check_char(cmd, chars: list[str]):
            for char in chars:
                if cmd.startswith(char):
                    cmd = cmd[len(char):]
                if cmd.endswith(char):
                    cmd = cmd[: -len(char)]
            return cmd

        command = check_char(command, ['"', "'"]).strip()

        hear_rooms = [session.character.room]
        pluralizer = Pluralizer()

        match prefix:
            case "shout" | "scream" | "yell":
                for portal in PortalService.get_by_room(session.character.room.id):
                    if portal.from_room == session.character.room:
                        hear_rooms.append(portal.to_room)
                    elif portal.to_room == session.character.room and portal.reversible == True:
                        hear_rooms.append(portal.from_room)
                speech = Speech.objects.create(
                    speaker=session.character,
                    message=command,
                    rooms=hear_rooms,
                    prefix=[prefix, pluralizer.pluralize(prefix, 2, False)]
                )
                await cls.notify(speech, session)
            case _:
                if len(command) == 0:
                    TelnetService.write_line(writer, "You mumble incoherently.")
                else:
                    speech = Speech.objects.create(
                        speaker=session.character,
                        message=command,
                        rooms=[session.character.room],
                    )
                    await cls.notify(speech, session)
