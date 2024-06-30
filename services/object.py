from models.object import Object, ObjectUpdateDTO, ObjectCreateDTO


class ObjectService:

    @staticmethod
    def get_by_id(obj_id: str):
        return Object.objects(id=obj_id).first()

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
