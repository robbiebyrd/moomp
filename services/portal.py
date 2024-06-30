from models.portal import Portal, PortalDirection, PortalUpdateDTO
from utils.db import connect_db
from middleware.updater import notify_modified, notify_deleted
from mongoengine import signals
from mongoengine.queryset.visitor import Q

class PortalService:

    def __init__(self, portal: Portal):
        self._portal = portal
        self._connection = connect_db()

    @staticmethod
    def new(portal_id: str) -> 'PortalService':
        return PortalService(PortalService.get_by_id(portal_id))

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

    def get(self):
        return self._portal

    def rename(self, portal_name: str):
        self._portal.name = portal_name
        self._portal.save()

    def update(self, portal: PortalUpdateDTO):
        self._portal.update(**portal.model_dump(exclude_none=True))
        self.refresh()

    def update_property(self, properties: dict):
        self._portal.properties.update(**properties)
        self._portal.save()

    def refresh(self):
        self._portal = Portal.objects(name=self._portal.name).first()


signals.post_save.connect(notify_modified, sender=Portal)
signals.post_delete.connect(notify_deleted, sender=Portal)
