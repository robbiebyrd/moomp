from middleware.updater import notify_and_create_event, notify
from models.account import Account
from models.character import Character, CharacterCreateDTO, CharacterUpdateDTO
from models.room import Room
from services.room import RoomService
from utils.db import connect_db

connect_db()


class CharacterService:

    def __init__(self, character: Character):
        self._character = character

    def context(self):
        return (
            self._character,
            self._character.inventory,
            self._character.room,
            Character.objects(room=self._character.room, online=True),
            self._character.account,
            RoomService.exits(self._character.room.id),
        )

    @staticmethod
    def get_by_id(user_id: str) -> Character:
        return Character.objects(id=user_id).first()

    @staticmethod
    def get_by_username(username: str) -> Character:
        return Character.objects(name=username).first()

    @staticmethod
    def register(character: CharacterCreateDTO):
        if Character.objects(name=character.name).first():
            raise ValueError("character exists")

        account_dto = character.model_dump(exclude_none=True)
        account_dto["account"] = Account.objects(id=character.account_id).first()
        del account_dto["account_id"]

        return Character(**account_dto).save()

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
        characters = Character.objects(name=new_username).all()
        if len(characters) != 0:
            return None

        character = Character.objects(id=character_id).first()
        character.name = new_username
        character.save()
        notify(character.account.instance.id, "Character", character, "Renamed")
        return character

    @classmethod
    def rename_display(cls, character_id: str, new_display_name: str):
        character = Character.objects(id=character_id).first()
        character.display = new_display_name
        character.save()
        return character

    def update(self, user: CharacterUpdateDTO):
        self._character.update(**user.model_dump(exclude_none=True))

    @classmethod
    def update_property(cls, session, character_id: str, properties: dict):
        character = Character.objects(id=character_id).first()
        character.properties.update(**properties)
        character.save()
        notify(session.instance, "Character", character, "Updated")

    def refresh(self):
        self._character = Character.objects(name=self._character.name).first()

    @classmethod
    def move(cls, session, direction: str) -> None:
        character = Character.objects(id=session.character.id).first()
        exiting_room = character.room

        _, _, entering_room = RoomService.resolve_alias(
            room_id=character.room.id, direction=direction
        )

        if entering_room is None:
            return

        character.room = entering_room
        character.save()

        cls.notify_move(session, exiting_room, ["Entered", "Exited"])

    @classmethod
    def warp(cls, session, room_cid: str):
        character = Character.objects(id=session.character.id).first()
        room_cid = room_cid.removeprefix("#")
        room = Room.objects(cId=room_cid).first()
        exiting_room = character.room

        character.room = room
        character.save()

        cls.notify_move(session, exiting_room, ["TeleportedIn", "TeleportedOut"])

    @classmethod
    def notify_move(cls, session, exiting_room: Room, action=None):
        if action is None:
            action = ["Entered", "Exited"]

        def create_event(
            document_type, document, document_operation, operator_type, operator
        ):
            notify_and_create_event(
                instance=session.instance,
                document_type=document_type,
                document=document,
                document_operation=document_operation,
                operator_type=operator_type,
                operator=operator,
            )

        events = [
            ("Room", session.character.room, action[0], "Character", session.character),
            ("Character", session.character, action[0], "Room", session.character.room),
            ("Room", exiting_room, action[1], "Character", session.character),
            ("Character", session.character, action[1], "Room", exiting_room),
        ]

        for event in events:
            create_event(*event)
