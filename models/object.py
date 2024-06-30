from mongoengine import DynamicDocument, ReferenceField, StringField, DictField
from pydantic import BaseModel


class Object(DynamicDocument):
    meta = {'collection': 'objects'}

    parent = ReferenceField('self', db_field='_parentId')
    owner = ReferenceField('Character', required=True, db_field='_ownerId')

    name = StringField(required=True)

    description = StringField()

    # The character holding the object. If set, the room_id should be empty.
    character = ReferenceField('Character', db_field='_characterId')

    # The room containing the object. If set, the character_id should be empty.
    room = ReferenceField('Room', db_field='_roomId')

    properties = DictField()


class ObjectCreateDTO(BaseModel):
    name: str
    parent: str
    owner: str
    description: str
    character: str
    room: str
    properties: dict


class ObjectUpdateDTO(BaseModel):
    name: str | None = None
    parent: str | None = None
    owner: str | None = None
    description: str | None = None
    character: str | None = None
    room: str | None = None
    properties: dict | None = None
