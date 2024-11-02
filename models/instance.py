from datetime import datetime

from mongoengine import (
    Document,
    StringField,
    SequenceField,
    ReferenceField,
    DictField,
    DateTimeField
)


class Instance(Document):
    meta = {"collection": "instances"}
    cId = SequenceField(db_field="c")

    parent = ReferenceField("self", db_field="_parentId", required=False)

    name = StringField(required=True)
    description = StringField()
    created_at = DateTimeField(required=True, default=datetime.now)

    properties = DictField()
