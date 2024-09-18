from datetime import datetime
from enum import Enum

from mongoengine import (
    Document,
    ReferenceField,
    StringField,
    DictField,
    SequenceField,
    ListField,
    DateTimeField, EmbeddedDocument, EnumField, EmbeddedDocumentField,
)
from pydantic import BaseModel

import models

ScriptTypes = Enum('ScriptTypes', models.__all__)


class ScriptType(EmbeddedDocument):
    type: EnumField(ScriptTypes)
    script: StringField()


class Script(Document):
    meta = {"collection": "scripts"}

    cId = SequenceField()

    owner = ReferenceField("Character", required=True, db_field="_ownerId")
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)

    scripts = ListField(EmbeddedDocumentField(ScriptType))

    accounts = ListField(ReferenceField("Account"), db_field="_accountIds")
    characters = ListField(ReferenceField("Character"), db_field="_characterIds")
    objects = ListField(ReferenceField("Object"), db_field="_objectIds")
    portals = ListField(ReferenceField("Portal"), db_field="_portalIds")
    rooms = ListField(ReferenceField("Room"), db_field="_roomIds")
    topics = ListField(StringField())

    properties = DictField()


class SpeechCreateDTO(BaseModel):
    speaker: str
    message: str
    created_at: datetime | None = None
    listeners: list[str] | None = None
    rooms: list[str] | None = None
    properties: dict | None = {}
