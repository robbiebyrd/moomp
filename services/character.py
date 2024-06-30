from middleware.updater import notify_modified, notify_deleted
from models.character import Character, CharacterCreateDTO, CharacterUpdateDTO
from models.portal import Portal, PortalDirection
from utils.db import connect_db
from mongoengine import signals
from mongoengine.queryset.visitor import Q


class CharacterService:

    def __init__(self, character: Character):
        self._character = character
        self._connection = connect_db()

    @staticmethod
    def get_by_username(username: str) -> Character:
        return Character.objects(name=username).first()

    @staticmethod
    def new(username: str):
        return CharacterService(CharacterService.get_by_username(username))

    @staticmethod
    def register(user: CharacterCreateDTO):
        if Character.objects(name=user.name).first():
            raise ValueError('character exists')

        character = Character(**user.model_dump()).save()
        return character

    @staticmethod
    def remove(username: str):
        if char := Character.objects(name=username).first():
            return char.delete()

    def get(self):
        return self._character

    def where(self):
        return self._character['room']

    def rename(self, username: str):
        self._character.name = username
        self._character.save()

    def update(self, user: CharacterUpdateDTO):
        self._character.update(**user.model_dump(exclude_none=True))

    def update_property(self, properties: dict):
        self._character.properties.update(**properties)
        self._character.save()

    def refresh(self):
        self._character = Character.objects(name=self._character.name).first()

    def move(self, direction: str):
        portals = Portal.objects(Q(from_id=self.where().id) | Q(to_id=self.where().id) & Q(reversible=True))
        print(portals)
        return

    def warp(self, portal: Portal, direction: PortalDirection = PortalDirection.TO):
        return


signals.post_save.connect(notify_modified, sender=Character)
signals.post_delete.connect(notify_deleted, sender=Character)
