from models.character import Character
from models.object import Object, ObjectUpdateDTO, ObjectCreateDTO
from models.room import Room


class ObjectService:
    @staticmethod
    def get_by_id(obj_id: str):
        return Object.objects(id=obj_id).first()

    @staticmethod
    def get_by_owner(character_id: str, show_invisible: bool = False):
        owner = Character.objects(id=character_id).first()
        if not owner:
            return None
        return Object.objects(owner=owner, visible=show_invisible)

    @staticmethod
    def get_by_holder(character_id: str, show_invisible: bool = False):
        holder = Character.objects(id=character_id).first()
        if not holder:
            return None
        return Object.objects(holder=holder, visible=show_invisible)

    @staticmethod
    def get_by_room(room_id: str, show_invisible: bool = False):
        room = Room.objects(id=room_id).first()
        if not room:
            return None
        return Object.objects(room=room, visible=show_invisible)

    @staticmethod
    def remove(obj_id: str):
        if obj := Object.objects(id=obj_id).first():
            return obj.delete()

    @staticmethod
    def create(obj: ObjectCreateDTO):
        new_obj = Object(**obj.model_dump(exclude_none=True)).save()
        return new_obj

    @staticmethod
    def update(obj: ObjectUpdateDTO):
        new_obj = ObjectService.get_by_id(obj.id)
        new_obj.update(**obj.model_dump(exclude_none=True)).save()
        return new_obj

    @classmethod
    def update_property(cls, obj_id: str, properties: dict):
        obj = cls.get_by_id(obj_id)
        obj.properties.update(**properties)
        obj.save()
