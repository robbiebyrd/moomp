import re

from middleware.updater import unpack_topic
from services.character import CharacterService
from services.room import RoomService
from services.session import TextSession
from utils.db import connect_db

connect_db()


class RoomConsumer:
    allowed_operators = [
        "Entered",
        "Exited",
        "TeleportedIn",
        "TeleportedOut",
        "LoggedIn",
        "LoggedOut",
    ]

    @classmethod
    def on_message(cls, mqtt, session: TextSession, msg):
        [room_id, operator, entrant_id] = list(
            unpack_topic(f"/{session.instance.id}/Room/+/+/Character/+", msg.topic)
        )

        if operator not in cls.allowed_operators:
            return

        if entrant_id == str(session.character.id) or room_id != str(
            session.character.room.id
        ):
            return

        room = RoomService.get_by_id(room_id)
        entrant = CharacterService.get_by_id(entrant_id)

        if not (room and entrant):
            return

        match operator:
            case "Entered" | "Exited":
                session.writer.write(
                    f"{session.ren.ct(message=entrant.name, color_name=session.ren.color_theme.chat)}"
                    f" {operator.lower()} {room.name}.{session.ren.nl}"
                )
            case "TeleportedIn" | "TeleportedOut" | "LoggedIn" | "LoggedOut":
                operator = re.sub(r"(\w)([A-Z])", r"\1 \2", operator)
                session.writer.write(
                    f"{session.ren.ct(message=entrant.name, color_name=session.ren.color_theme.chat)}"
                    f" {operator.lower()}.{session.ren.nl}"
                )

    @staticmethod
    def validate_topic(instance_id: str, topic: str) -> bool:
        return bool(topic.startswith(f"/{instance_id}/Room/"))
