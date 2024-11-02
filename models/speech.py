from datetime import datetime

from mongoengine import (
    Document,
    ReferenceField,
    StringField,
    DictField,
    SequenceField,
    ListField,
    DateTimeField,
)
from pydantic import BaseModel


class Speech(Document):
    meta = {"collection": "speech"}
    cId = SequenceField(db_field="c")

    speaker = ReferenceField("Character", required=True, db_field="_ownerId")
    created_at = DateTimeField(required=True, default=datetime.now)

    message = StringField(required=True)
    prefix = ListField(required=True, default=["say", "says"])

    # The characters being spoken to.
    listeners = ListField(
        ReferenceField("Character", db_field="_characterIds"), required=False
    )

    # The rooms where the message can be heard.
    rooms = ListField(ReferenceField("Room", db_field="_roomIds"), required=False)

    properties = DictField()


class SpeechCreateDTO(BaseModel):
    speaker: str
    message: str
    created_at: datetime | None = None
    listeners: list[str] | None = None
    rooms: list[str] | None = None
    properties: dict | None = {}
