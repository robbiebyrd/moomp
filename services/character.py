from middleware.updater import notify_and_create_event
from models.character import Character, CharacterCreateDTO, CharacterUpdateDTO
from models.room import Room
from services.authn import AuthNService
from services.portal import PortalService
from utils.db import connect_db


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
            raise ValueError("character exists")

        user.password = AuthNService.encrypt_password(user.password)

        character = Character(**user.model_dump(exclude_none=True)).save()
        return character

    @staticmethod
    def remove(username: str):
        if char := Character.objects(name=username).first():
            return char.delete()

    @classmethod
    def online(cls):
        return Character.objects.find(online=True)

    def get(self):
        return self._character

    def where(self):
        return self._character["room"]

    @classmethod
    def rename(cls, character_id: str, new_username: str):
        character = Character.objects(id=character_id).first()
        character.name = new_username
        character.save()
        return character

    def update(self, user: CharacterUpdateDTO):
        self._character.update(**user.model_dump(exclude_none=True))

    @classmethod
    def update_property(cls, character_id: str, properties: dict):
        character = Character.objects(id=character_id).first()
        character.properties.update(**properties)
        character.save()

    def refresh(self):
        self._character = Character.objects(name=self._character.name).first()

    @classmethod
    def move(cls, character_id: str, direction: str):
        character = Character.objects(id=character_id).first()
        portals = PortalService.get_by_room(character.room.id)
        direction = direction.lower()
        current_room = character.room

        for portal in portals:
            if direction in [x.lower() for x in portal.alias_to]:
                character.room = portal.from_room
                break
            elif direction in [x.lower() for x in portal.alias_from] and portal.reversible is True:
                character.room = portal.to_room
                break
        else:
            return

        notify_and_create_event("Room", current_room, "Exited", character)
        notify_and_create_event("Room", character.room, "Entered", character)

        character.save()

    @classmethod
    def warp(
            cls,
            character_id: str,
            room_id: str,
    ):
        character = Character.objects(id=character_id).first()
        room = Room.objects(id=room_id).first()

        character.room = room
        character.save()
