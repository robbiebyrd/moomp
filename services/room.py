from mongoengine.queryset.visitor import Q

from models.character import Character
from models.object import Object
from models.portal import Portal, PortalUpdateDTO
from models.room import Room, RoomUpdateDTO, RoomCreateDTO
from services.portal import PortalService
from utils.db import connect_db


class RoomService:

    def __init__(self):
        self._connection = connect_db()

    @staticmethod
    def get_by_id(room_id: str):
        return Room.objects(id=room_id).first()

    @staticmethod
    def get_by_name(room_name: str):
        return Room.objects(name=room_name).first()

    @staticmethod
    def remove(room_id: str):
        if char := Room.objects(id=room_id).first():
            return char.delete()

    @staticmethod
    def create(room: RoomCreateDTO):
        if Room.objects(name=room.name).first():
            raise ValueError("room exists")

        room_obj = Room(**room.model_dump(exclude_none=True)).save()
        return room_obj

    @classmethod
    def exits(cls, room_id: str):
        return PortalService.get_by_room(room_id)

    @classmethod
    def here(cls, room_id: str, show_offline: bool = False, show_hidden: bool = False):
        objects_query = (Q(room=room_id) & Q(visible=True)) if show_hidden else Q(room=room_id)
        characters_query = (
                Q(room=room_id)
                & (Q(online=True) if not show_offline else None)
                & (Q(visible=True) if not show_offline else None)
        )
        return {"objects": Object.objects(objects_query), "characters": Character.objects(characters_query)}

    @classmethod
    def update(cls, room: RoomUpdateDTO):
        this_room = cls.get_by_id(room.id)
        this_room.update(**room.model_dump(exclude_none=True))

    @classmethod
    def update_property(cls, room_id: str, properties: dict):
        this_room = cls.get_by_id(room_id)
        this_room.properties.update(**properties)
        this_room.save()

    @staticmethod
    def connect(room_id: str, portal: PortalUpdateDTO):
        if portal.name is None or portal.owner is None or portal.to_room is None:
            return False
        owner = Character.objects(name=portal.owner).first()
        to_room = Room.objects(id=portal.to_room).first()
        p = Portal(
            name=portal.name,
            owner=str(owner.id),
            from_room=room_id,
            to_room=str(to_room.id),
            reversible=portal.reversible,
        )
        p.save()
        return p.id

    @classmethod
    def dig(cls, room_id: str, new_room: RoomCreateDTO | str, portal: PortalUpdateDTO):
        if portal.name is None:
            raise ValueError("the portal name is required")

        portal.from_room = Room.objects(id=room_id).first()

        if type(new_room) is str:
            portal.to_room = cls.get_by_id(new_room).id
        elif type(new_room) is RoomCreateDTO:
            portal.to_room = cls.create(new_room).id
        else:
            raise ValueError("new_room must be str or RoomCreateDTO")

        portal = Portal(**portal.model_dump(exclude_none=True))
        portal.save()
        return portal

    @classmethod
    def to_text(cls, room_id: str):
        this_room = Room.objects(id=room_id).first()
        return f"""{this_room.name}\r\n
        {this_room.description}\r\n
        
        """
