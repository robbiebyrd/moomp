from mongoengine import (
    Document,
    ReferenceField,
    StringField,
    BooleanField,
    DictField,
    SequenceField,
)
from pydantic import BaseModel

from models.account import Account
from models.room import Room


class Character(Document):
    meta = {"collection": "characters"}

    cId = SequenceField()
    account = ReferenceField(Account, db_field="_accountId")

    # The "location" of the current user.
    room = ReferenceField(Room, db_field="_roomId")

    name = StringField(required=True, regex="^[a-zA-Z0-9]{1,100}$")
    display = StringField(required=True)

    online = BooleanField(default=False)

    description = StringField()

    properties = DictField()

    visible = BooleanField()


class CharacterCreateDTO(BaseModel):
    name: str
    display: str
    visible: bool = True


class CharacterUpdateDTO(BaseModel):
    display: str | None = None
    visible: bool | None = None
