from mongoengine.queryset.visitor import Q

from models.portal import Portal, PortalUpdateDTO, PortalCreateDTO


class PortalService:

    @staticmethod
    def create(portal: PortalCreateDTO):
        portal_obj = Portal(**portal.model_dump(exclude_none=True)).save()
        return portal_obj

    @staticmethod
    def get_by_id(portal_id: str) -> Portal:
        return Portal.objects(id=portal_id).first()

    @staticmethod
    def get_by_room(room_id: str) -> [Portal]:
        query = Q(from_room=room_id) | Q(to_room=room_id, reversible=True)
        return Portal.objects(query)

    @staticmethod
    def remove(portal_id: str):
        if portal := Portal.objects(id=portal_id).first():
            return portal.delete()

    @classmethod
    def update(cls, portal_id: str, portal: PortalUpdateDTO):
        p = cls.get_by_id(portal_id)
        p.update(**portal.model_dump(exclude_none=True))
        return p

    @classmethod
    def update_property(cls, portal_id: str, properties: dict):
        p = cls.get_by_id(portal_id)
        p.properties.update(**properties)
        p.save()
        return p.properties
