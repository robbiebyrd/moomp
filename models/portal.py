from datetime import datetime
from enum import Enum

from mongoengine import (
    Document,
    ReferenceField,
    StringField,
    ListField,
    BooleanField,
    DictField,
    SequenceField, DateTimeField,
)
from pydantic import BaseModel

from models.character import Character
from models.room import Room


class PortalDirection(Enum):
    FROM = "_from"
    TO = "_to"


class Portal(Document):
    meta = {"collection": "portals"}
    cId = SequenceField(db_field="c")
    created_at = DateTimeField(required=True, default=datetime.now)

    owner = ReferenceField(Character, required=True, db_field="_ownerId")

    from_room = ReferenceField(Room, required=True, db_field="_fromId")
    to_room = ReferenceField(Room, required=True, db_field="_toId")  # The Exit of the portal

    name = StringField(required=True)

    alias_to = ListField(StringField(), db_field="aliasTo")
    description_to = StringField(db_field="descriptionTo")

    alias_from = ListField(StringField(), db_field="aliasFrom")
    description_from = StringField(db_field="descriptionFrom")

    visible = BooleanField(default=True)
    reversible = BooleanField(default=False)

    properties = DictField()


class PortalCreateDTO(BaseModel):
    """
    A Data Transfer Object class for creatina a new Portal between Rooms.

    Attributes:
        name (str): Name of the portal.
        owner (str): User ID of the owner of the portal.
        from_room (str): ID of the 'from' room of the portal.
        to_room (str): ID of the 'to' room of the portal.
        alias_to (list[str], optional): Alias names for the 'to' direction of the portal. Defaults to empty list.
        description_to (str, optional): Description for the 'to' direction of the portal. Defaults to None.
        alias_from (list[str], optional): Alias names for the 'from' direction of the portal. Defaults to empty list.
        description_from (str, optional): Description for the 'from' direction of the portal. Defaults to None.
        visible (bool, optional): A flag indicating whether the portal is visible to others. Defaults to True.
        reversible (bool, optional): A flag indicating whether the portal is reversible. Defaults to True.
    """

    name: str
    owner: str
    from_room: str
    to_room: str | None = None
    alias_to: list[str] = []
    description_to: str | None = None
    alias_from: list[str] = []
    description_from: str | None = None
    visible: bool = True
    reversible: bool = False


class PortalUpdateDTO(BaseModel):
    """
    A Data Transfer Object class for updating a new Portal between Rooms.

    Attributes:
        name (str, optional): Name of the portal.
        owner (str, optional): User ID of the owner of the portal.
        from_room (str, optional): ID of the 'from' room of the portal.
        to_room (str, optional): ID of the 'to' room of the portal.
        alias_to (list[str], optional): Alias names for the 'to' direction of the portal. Defaults to empty list.
        description_to (str, optional): Description for the 'to' direction of the portal. Defaults to None.
        alias_from (list[str], optional): Alias names for the 'from' direction of the portal. Defaults to empty list.
        description_from (str, optional): Description for the 'from' direction of the portal. Defaults to None.
        visible (bool, optional): A flag indicating whether the portal is visible to others. Defaults to True.
        reversible (bool, optional): A flag indicating whether the portal is reversible. Defaults to True.
    """

    name: str | None = None
    owner: str | None = None
    from_room: str | None = None
    to_room: str | None = None
    alias_to: list[str] = []
    description_to: str | None = None
    alias_from: list[str] = []
    description_from: str | None = None
    visible: bool | None = None
    reversible: bool | None = None
