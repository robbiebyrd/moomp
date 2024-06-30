from mongoengine import DynamicDocument, ReferenceField, StringField, BooleanField, DictField
from pydantic import BaseModel


class Character(DynamicDocument):
    meta = {'collection': 'characters'}

    # The "location" of the current user.
    room = ReferenceField('Room', db_field='_roomId')

    name = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)

    display = StringField(required=True)
    description = StringField()

    properties = DictField()

    visible = BooleanField()


class CharacterCreateDTO(BaseModel):
    name: str
    email: str
    password: str
    display: str
    visible: bool = False


class CharacterUpdateDTO(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    display: str | None = None
    visible: bool | None = None
