from middleware.updater import unpack_topic
from services.character import CharacterService
from services.room import RoomService
from services.session import TextSession
from templates.utils.text.color import ColorTextRenderer
from utils.db import connect_db

connect_db()
renderer = ColorTextRenderer()
ct = renderer.colorize


class RoomConsumer:

    def __init__(self):
        self._connection = connect_db()

    @classmethod
    def on_message(cls, mqtt, session: TextSession, msg):
        [room_id, operator, entrant_id] = list(
            unpack_topic("/Room/+/+/Character/+", msg.topic)
        )

        room = RoomService.get_by_id(room_id)
        entrant = CharacterService.get_by_id(entrant_id)

        if (
            room
            and entrant
            and (
                room.id == session.character.room.id
                and entrant.id != session.character.id
            )
        ):
            session.writer.write(
                f"{renderer.ct(message=entrant.name, color_name=session.ren.color_theme.chat)} {operator}"
                f" {room.name}.{renderer.nl}"
            )

    @staticmethod
    def validate_topic(topic: str) -> bool:
        return bool(topic.startswith("/Room/"))
