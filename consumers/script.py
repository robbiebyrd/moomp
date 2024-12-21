from middleware.updater import unpack_topic
from services.session import TextSession
from templates.utils.text.color import ColorTextRenderer
from utils.db import connect_db

connect_db()
renderer = ColorTextRenderer()
ct = renderer.colorize


class ScriptConsumer:

    def __init__(self):
        self._connection = connect_db()

    @classmethod
    def on_message(cls, mqtt, session: TextSession, msg):
        [_, room_id, speaker_id] = list(
            unpack_topic(f"{session.instance.id}/Speech/+/Room/+/Speaker/+", msg.topic)
        )

    @classmethod
    def validate_topic(cls, instance_id: str, topic: str) -> bool:
        return bool(topic.startswith(f"/{instance_id}/Speech/"))
