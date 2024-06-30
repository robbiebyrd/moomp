from mongoengine import DynamicDocument, ReferenceField, StringField, BooleanField, DictField
from pydantic import BaseModel

from models.character import Character


class Room(DynamicDocument):
    meta = {'collection': 'rooms'}

    owner = ReferenceField(Character, required=True, db_field='_ownerId')
    parent = ReferenceField('self', db_field='_parentId')

    name = StringField(required=True, unique=True)
    description = StringField()

    visible = BooleanField()

    properties = DictField()


class RoomCreateDTO(BaseModel):
    owner: str
    name: str
    description: str
    parent_id: str | None = None
    visible: bool | None = True


class RoomUpdateDTO(BaseModel):
    owner: str | None = None
    parent_id: str | None = None
    name: str | None = None
    description: str | None = None
    visible: bool | None = None
