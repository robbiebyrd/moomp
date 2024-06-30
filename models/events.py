from datetime import datetime

from mongoengine import (
    DynamicDocument,
    StringField,
    SequenceField,
    DateTimeField,
    GenericReferenceField,
)


class Event(DynamicDocument):
    meta = {"collection": "events"}

    cId = SequenceField()

    created_at = DateTimeField(required=True, default=datetime.now)

    event = StringField(required=True)

    ref_document = GenericReferenceField(required=True)
    ref_operator = GenericReferenceField(required=False)
