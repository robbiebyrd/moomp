from mongoengine import (
    Document,
    ReferenceField,
    StringField,
    BooleanField,
    DictField,
    SequenceField,
)
from pydantic import BaseModel


class Room(Document):
    meta = {"collection": "rooms"}

    cId = SequenceField()

    owner = ReferenceField("Character", required=True, db_field="_ownerId")
    parent = ReferenceField("self", db_field="_parentId")

    name = StringField(required=True, unique=True)
    description = StringField()

    visible = BooleanField()

    properties = DictField()


class RoomCreateDTO(BaseModel):
    """
    A Data Transfer Object class for creating a Room.

    Attributes:
        owner (str): The ID of the owner of the room.
        name (str): Name of the room.
        description (str): Description of the room.
        parent_id (str, optional): ID of the parent room if the room is a sub-room. Defaults to None.
        visible (bool, optional): A flag indicating whether the room is visible to others. Defaults to True.
    """

    owner: str
    name: str
    description: str = "An empty room."
    parent_id: str | None = None
    visible: bool | None = True


class RoomUpdateDTO(BaseModel):
    """
    A Data Transfer Object class for updating a Room.

    Attributes:
        id (str): The ID of the room to update.
        owner (str, optional): The ID of the owner of the room.
        parent_id (str, optional): ID of the parent room if the room is a sub-room. Defaults to None.
        name (str, optional): Name of the room. Defaults to None.
        description (str, optional): Description of the room. Defaults to None.
        visible (bool, optional): A flag indicating whether the room is visible to others. Defaults to None.
    """

    id: str
    owner: str | None = None
    parent_id: str | None = None
    name: str | None = None
    description: str | None = None
    visible: bool | None = None
