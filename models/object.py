from mongoengine import (
    Document,
    ReferenceField,
    StringField,
    DictField,
    SequenceField,
    BooleanField,
)
from pydantic import BaseModel, ValidationError

common_properties = {"locked": bool}


class Object(Document):
    meta = {"collection": "objects"}

    cId = SequenceField()

    parent = ReferenceField("self", db_field="_parentId")
    owner = ReferenceField("Character", required=True, db_field="_ownerId")

    name = StringField(required=True)

    description = StringField()
    visible = BooleanField(default=True)

    # The character holding the object. If set, the room_id should be empty.
    holder = ReferenceField("Character", db_field="_characterId")

    # The room containing the object. If set, the character_id should be empty.
    room = ReferenceField("Room", db_field="_roomId")

    properties = DictField()

    def clean(self):
        if self.holder is not None and self.room is not None:
            raise ValidationError("You cannot assign an object to both a room and a character.")


class ObjectCreateDTO(BaseModel):
    """
    A Data Transfer Object class for creating Objects.

    Attributes:
        name (str): Name of the object.
        parent (str): ID of the parent of the object.
        owner (str): User ID of the owner of the object.
        description (str): Description of the object.
        character (str): The ID of the Character holding the object; cannot be set with `room`.
        room (str): The ID of the Room the object is located in; cannot be set with `character`.
        properties (dict): Additional properties of the object.

    """

    name: str
    parent: str | None = None
    owner: str
    description: str
    character: str | None = None
    room: str | None = None
    properties: dict | None = {}


class ObjectUpdateDTO(BaseModel):
    """
    A Data Transfer Object class for updating Objects.

    Attributes:
        name (str, optional): Name of the object.
        parent (str, optional): ID of the parent of the object.
        owner (str, optional): User ID of the owner of the object.
        description (str, optional): Description of the object.
        character (str, optional): The ID of the Character holding the object; cannot be set with `room`.
        room (str, optional): The ID of the Room the object is located in; cannot be set with `character`.
        properties (dict, optional): Additional properties of the object.

    """

    name: str | None = None
    parent: str | None = None
    owner: str | None = None
    description: str | None = None
    character: str | None = None
    room: str | None = None
    properties: dict | None = None
