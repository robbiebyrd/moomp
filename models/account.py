from datetime import datetime

from mongoengine import (
    Document,
    ReferenceField,
    StringField,
    SequenceField,
    DateTimeField,
)
from mongoengine import (
    EmailField,
)
from pydantic import BaseModel

from models.instance import Instance


class Account(Document):
    meta = {
        "collection": "accounts",
        "indexes": [
            "$email",
            ("instance", "+email"),  # compound index
        ],
    }

    cId = SequenceField(db_field="c")

    created_at = DateTimeField(required=True, default=datetime.now)

    email = EmailField(required=True)
    password = StringField(required=True)

    instance = ReferenceField(Instance, required=True, db_field="_instanceId")


class AccountCreateDTO(BaseModel):
    email: str
    password: str
    instance_id: str


class AccountUpdateDTO(BaseModel):
    email: str | None = None


class AccountPasswordUpdateDTO(BaseModel):
    email: str
    current_password: str
    new_password: str
