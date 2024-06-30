from mongoengine import DynamicDocument, ReferenceField, StringField, ListField, BooleanField, DictField
from enum import Enum

from pydantic import BaseModel

from models.character import Character
from models.room import Room


class PortalDirection(Enum):
    FROM = '_from'
    TO = '_to'


class Portal(DynamicDocument):
    meta = {'collection': 'portals'}

    owner = ReferenceField(Character, required=True, db_field='_ownerId')

    from_room = ReferenceField(Room, required=True, db_field='_fromId')  # The Entrance of the portal
    to_room = ReferenceField(Room, required=True, db_field='_toId')  # The Exit of the portal

    name = StringField(required=True)

    alias_to = ListField(StringField(), db_field='aliasTo')
    description_to = StringField(db_field='descriptionTo')

    alias_from = ListField(StringField(), db_field='aliasFrom')
    description_from = StringField(db_field='descriptionFrom')

    visible = BooleanField(default=True)
    reversible = BooleanField(default=False)

    properties = DictField()


class PortalCreateDTO(BaseModel):
    name: str
    owner: str
    from_room: str
    to_room: str
    alias_to: list[str] = []
    description_to: str | None = None
    alias_from: list[str] = []
    description_from: str | None = None
    visible: bool = True
    reversible: bool = True


class PortalUpdateDTO(BaseModel):
    name: str | None = None
    owner: str
    from_room: str | None = None
    to_room: str | None = None
    alias_to: list[str] = []
    description_to: str | None = None
    alias_from: list[str] = []
    description_from: str | None = None
    visible: bool | None = None
    reversible: bool | None = None
