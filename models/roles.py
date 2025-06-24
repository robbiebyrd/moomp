from datetime import datetime

from mongoengine import (
    DynamicDocument,
    StringField,
    SequenceField,
    DateTimeField,
    ReferenceField,
)


class Role(DynamicDocument):
    meta = {"collection": "roles"}
    cId = SequenceField(db_field="c")
    created_at = DateTimeField(required=True, default=datetime.now)

    parent = ReferenceField("self", db_field="_parentId")

    name = StringField(required=True)
    description = StringField(required=True)
    shortname = StringField(required=False)
