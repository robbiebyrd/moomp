from middleware.updater import notify_and_create_event
from models.character import Character, CharacterCreateDTO, CharacterUpdateDTO
from models.room import Room
from services.room import RoomService
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

        return Character(**user.model_dump(exclude_none=True)).save()

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
    def move(cls, character_id: str, direction: str) -> None:
        character = Character.objects(id=character_id).first()
        exiting_room = character.room

        _, _, entering_room = RoomService.resolve_alias(character.room.id, direction)

        if entering_room is None:
            return

        character.room = entering_room

        notify_and_create_event("Room", exiting_room, "Exited", character)
        notify_and_create_event("Room", character.room, "Entered", character)

        character.save()

    @classmethod
    def warp(cls, character_id: str, room_id: str):
        character = Character.objects(id=character_id).first()
        room = Room.objects(id=room_id).first()

        character.room = room
        character.save()

# async def register(self):
#     while True:
#         email_input = await self.input_line("Email Address: ")
#         already_emails = Character.objects(email=email_input)
#         if len(already_emails) > 0:
#             session.writer.write("That email address is already taken, please try another one.")
#             continue
#         break
#
#     while True:
#         character_name_input = await self.input_line("Username: ", required=True, on_new_line=True)
#         already_character_name = Character.objects(name=character_name_input)
#         if len(already_character_name) > 0:
#             session.writer.write("That character name is already taken, please try another one.")
#             continue
#         break
#
#     password_input = await self.input_line("Password: ", mask_character="*")
#     display_name_input = await self.input_line("Display Name: ")
#
#     char = CharacterService.register(
#         user=CharacterCreateDTO(
#             name=character_name_input,
#             display=display_name_input,
#             password=password_input,
#             email=email_input,
#         )
#     )
#     return char
