import json

from middleware.updater import unpack_topic
from models.character import Character
from services.session import TextSession
from templates.text import BaseTextTemplate as Btt
from utils.colors import ct
from utils.db import connect_db

connect_db()


def on_message(mqtt, session: TextSession, msg):
    if msg.topic.startswith("/Speech/"):
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
