import json

from middleware.updater import unpack_topic
from models.character import Character
from services.session import TextSession
from templates.text import BaseTextTemplate as Btt
from utils.colors import ct
from utils.db import connect_db

connect_db()


class SpeechConsumer:

    def __init__(self):
        self._connection = connect_db()

    @classmethod
    def on_message(cls, mqtt, session: TextSession, msg):
        [_, room_id, speaker_id] = list(unpack_topic("/Speech/+/Room/+/Speaker/+", msg.topic))
        if room_id and speaker_id:
            speaker = Character.objects(id=speaker_id).first()
            payload = json.loads(msg.payload)
            prefix = payload.get("prefix")
            msg = ct(payload.get('message'), *session.colors.get('chat'))
            session.writer.write(
                (
                    f"You {prefix[0]} {msg}{Btt.NEWLINE}"
                    if speaker.id == session.character.id
                    else f"{speaker.name} {prefix[1]} {msg}{Btt.NEWLINE}"
                ),
            )

    @classmethod
    def validate_topic(cls, topic: str) -> bool:
        return True if topic.startswith('/Speech/') else False
