from datetime import datetime
from enum import Enum
from typing import List

from mongoengine import (
    Document,
    ReferenceField,
    StringField,
    DictField,
    SequenceField,
    ListField,
    DateTimeField,
    EmbeddedDocument,
    EmbeddedDocumentListField,
)
from pydantic import BaseModel

from utils.types import SCRIPT_OBJECT_TYPES

ScriptTypesList = [x._class_name for x in SCRIPT_OBJECT_TYPES]
ScriptTypes = Enum("ScriptTypes", ScriptTypesList)


class ScriptType(EmbeddedDocument):
    script = StringField(required=True)
    topics = ListField(default=[])


class Script(Document):
    meta = {"collection": "scripts"}
    cId = SequenceField(db_field="c")

    name = StringField(unique_with="owner")

    owner = ReferenceField("Character", required=True, db_field="_ownerId")
    instance = ReferenceField("Instance", required=True, db_field="_instanceId")
    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)

    scripts = EmbeddedDocumentListField(ScriptType)

    properties = DictField()


class ScriptTypeDto(BaseModel):
    type: str
    script: str
    topics: List[str]


class ScriptCreateDTO(BaseModel):
    name: str
    owner: str
    created_at: datetime | None = None
    scripts: list[ScriptTypeDto] | None = None
    properties: dict


def ref_to_topic(
    instance_id: str,
    obj_id: str | None,
    collection: ScriptTypes,
    ml_wildcard: bool = False,
) -> [str]:

    # All subscribable topics must start with the instance ID.
    prefix = f"/{instance_id}"

    # If the specific object ID is provided, display it; else use a wildcard.
    if obj_id is None:
        obj_id = "+"

    # Add the Document Type to the topic
    prefix += f"/{collection}/{obj_id}"

    # Return either the bare topic or the topic and it's wildcard, if requested in ml_wildcard
    return [f"{prefix}", f"{prefix}/#"] if ml_wildcard else [prefix]
