from itertools import chain

from mongoengine.queryset.visitor import Q

from models.character import Character
from models.object import Object
from models.portal import Portal, PortalUpdateDTO
from models.room import Room, RoomUpdateDTO, RoomCreateDTO
from services.portal import PortalService
from utils.db import connect_db

connect_db()


class RoomService:

    @staticmethod
    def get_by_id(room_id: str):
        return Room.objects(id=room_id).first()

    @staticmethod
    def get_by_cid(c_id: int):
        return Room.objects(cId=c_id).first()

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

        return Room(**room.model_dump(exclude_none=True)).save()

    @classmethod
    def exits(cls, room_id: str):
        return PortalService.get_by_room(room_id)

    @classmethod
    def here(cls, room_id: str, show_offline: bool = False, show_hidden: bool = False):
        objects_query = (
            (Q(room=room_id) & Q(visible=True)) if show_hidden else Q(room=room_id)
        )
        characters_query = (
            Q(room=room_id)
            & (None if show_offline else Q(online=True))
            & (None if show_offline else Q(visible=True))
        )
        return {
            "objects": Object.objects(objects_query),
            "characters": Character.objects(characters_query),
            "exits": cls.exits(room_id),
        }

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
    def exits_and_aliases(
        cls,
        room_id: str,
        lowercase: bool = True,
        filter_duplicates: bool = True,
        include_name: bool = True,
    ):
        room = Room.objects(id=room_id).first()
        exits = []

        for exit_item in RoomService.exits(room_id=room.id):
            exits = exits + list(chain(*cls.exits_with_aliases(room.id).values()))
            if include_name:
                exits.append(exit_item.name)

        if lowercase:
            exits = [x.lower() for x in exits]
        if filter_duplicates:
            exits = list(set(exits))

        return exits

    @classmethod
    def exits_with_aliases(cls, room_id: str):
        room = Room.objects(id=room_id).first()
        return {
            exit_item.name: (
                exit_item.alias_from
                if exit_item.to_room.id == room.id
                else exit_item.alias_to
            )
            for exit_item in RoomService.exits(room_id=room.id)
        }

    @classmethod
    def resolve_alias(cls, room_id: str, direction: str):
        room = Room.objects(id=room_id).first()
        portals = PortalService.get_by_room(room.id)
        direction = direction.lower()

        for portal in portals:
            if (
                direction in [x.lower() for x in portal.alias_to]
                and portal.to_room.id != room_id
            ):  # and
                return True, portal, portal.to_room
            elif (
                direction in [x.lower() for x in portal.alias_from]
                and portal.reversible is True
                and portal.from_room.id != room_id
            ):
                return False, portal, portal.from_room
            elif direction.lower() == portal.name.lower():
                return (
                    True,
                    portal,
                    (
                        portal.to_room
                        if room_id == portal.from_room.id
                        else portal.from_room
                    ),
                )

        return False, None, room
