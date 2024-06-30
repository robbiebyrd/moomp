from models.character import Character
from models.portal import Portal, PortalUpdateDTO, PortalCreateDTO
from models.room import Room, RoomUpdateDTO, RoomCreateDTO
from utils.db import connect_db
from middleware.updater import notify_modified, notify_deleted
from mongoengine import signals


class RoomService:

    def __init__(self, room: Room):
        self._room = room
        self._connection = connect_db()

    @staticmethod
    def new(room_id: str | Room):
        if type(room_id) is Room:
            return RoomService(room_id)

        return RoomService(RoomService.get_by_id(room_id))

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
            raise ValueError('room exists')

        room_obj = Room(**room.model_dump()).save()
        return room_obj

    def get(self):
        return self._room

    def rename(self, room_name: str):
        self._room.name = room_name
        self._room.save()

    def update(self, room: RoomUpdateDTO):
        self._room.update(**room.model_dump(exclude_none=True))
        self.refresh()

    def update_property(self, properties: dict):
        self._room.properties.update(**properties)
        self._room.save()

    def refresh(self):
        self._room = Room.objects(name=self._room.name).first()

    def connect(self, to_room_id: str, name: str, owner: Character | str, reversible: bool = False, ):
        if owner is str:
            owner = Character.objects(name=owner).first()
        portal = Portal(name=name,
                        owner=owner,
                        from_room=self._room.id,
                        to_room=to_room_id,
                        reversible=reversible)
        portal.save()
        return portal.id

    def dig(self, new_room: RoomCreateDTO | str, portal: PortalCreateDTO):
        if portal.name is None:
            raise ValueError('the portal name is required')

        portal.from_room = self.get()

        if type(new_room) is str:
            portal.to_room = self.get_by_id(new_room).id
        elif type(new_room) is RoomCreateDTO:
            portal.to_room = self.create(new_room).id
        else:
            raise ValueError('new_room must be str or RoomCreateDTO')

        portal = Portal(**portal.model_dump(exclude_none=True))
        portal.save()


signals.post_save.connect(notify_modified, sender=Room)
signals.post_delete.connect(notify_deleted, sender=Room)
