from datetime import datetime
from enum import Enum

from mongoengine import (
    Document,
    ReferenceField,
    StringField,
    DictField,
    SequenceField,
    ListField,
    DateTimeField,
    EmbeddedDocument,
    EnumField,
    EmbeddedDocumentField,
)
from pydantic import BaseModel, Field

from utils.types import SCRIPT_OBJECT_TYPES

ScriptTypes = Enum("ScriptTypes", [x._class_name for x in SCRIPT_OBJECT_TYPES])


class ScriptType(EmbeddedDocument):
    type = EnumField(ScriptTypes)
    script = StringField(required=True)
    topics = ListField(default=[])


class Script(Document):
    meta = {"collection": "scripts"}
    cId = SequenceField(db_field="c")

    name = StringField(unique_with="owner")

    owner = ReferenceField("Character", required=True, db_field="_ownerId")
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)

    scripts = ListField(EmbeddedDocumentField(ScriptType))

    properties = DictField()


class SpeechCreateDTO(BaseModel):
    speaker: str
    message: str
    created_at: datetime | None = None
    listeners: list[str] | None = None
    rooms: list[str] | None = None
    properties: dict | None = Field(default={})
