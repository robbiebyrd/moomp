from datetime import datetime

from mongoengine import (
    Document,
    ReferenceField,
    StringField,
    BooleanField,
    DictField,
    SequenceField,
    DateTimeField,
)
from pydantic import BaseModel

from models.account import Account
from models.object import Object
from models.room import Room


class Character(Document):
    meta = {
        "collection": "characters",
        "indexes": [
            "$name",
            ("name", "+account"),
            {"fields": ["name"], "expireAfterSeconds": 3600},  # ttl index
        ],
    }
    cId = SequenceField(db_field="c")
    created_at = DateTimeField(required=True, default=datetime.now)

    name = StringField(required=True, regex="^[a-zA-Z0-9]{1,100}$", unique=True)
    display = StringField(required=True)
    description = StringField()

    online = BooleanField(default=False)
    visible = BooleanField(default=False)

    account = ReferenceField(Account, db_field="_accountId")
    room = ReferenceField(Room, db_field="_roomId")

    properties = DictField()

    @property
    def inventory(self):
        return Object.objects(holder=self)

    def clean(self):
        self.visible = bool(self.visible)
        self.online = bool(self.online)


class CharacterCreateDTO(BaseModel):
    account_id: str
    name: str
    display: str
    visible: bool | int = True


class CharacterUpdateDTO(BaseModel):
    display: str | None = None
    name: str | None = None
