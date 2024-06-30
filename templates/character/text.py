from typing import List

from models.character import Character
from models.object import Object
from templates.text import BaseTextTemplate as Btt


class CharacterText:
    @classmethod
    def get_list(cls, characters: List[Character], colors: List[str]):
        text = ""

        chars = []
        for i, char in enumerate(characters):
            chars.append(char.name)

        text += f"{Btt.NEWLINE}Characters: " + " ".join(chars) if len(chars) > 0 else ""
        return []

    @classmethod
    def get(cls, character: Character):
        header = f"{character.name}{Btt.NEWLINE}"
        header += (character.description + Btt.NEWLINE) if character.description else ""
        inventory_text = f"Inventory: {", ".join([x.name for x in Object.objects(holder=character)])}{Btt.NEWLINE}"
        where = f"In Room: {character.room.name}{Btt.NEWLINE}"

        return "".join(
            [
                Btt.LINE_RULE_NEWLINE,
                header,
                where,
                inventory_text,
                Btt.LINE_RULE,
            ]
        )
