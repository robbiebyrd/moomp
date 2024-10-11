from typing import List

from models.character import Character
from models.object import Object
from templates.utils.text.color import ColorTextRenderer

renderer = ColorTextRenderer()


class CharacterText:
    @classmethod
    def get_list(cls, characters: List[Character], colors: List[str]):
        text = ""

        chars = [char.name for char in characters]
        text += f"{renderer.nl}Characters: " + " ".join(chars) if chars else ""
        return text

    @classmethod
    def get(cls, character: Character):
        header = f"You are: {character.name}{renderer.nl}"
        header += (character.description + renderer.nl) if character.description else ""
        inventory_text = f"Inventory: {", ".join([x.name for x in Object.objects(holder=character)])}{renderer.nl}"
        where = f"In Room: {character.room.name}{renderer.nl}"

        return "".join(
            [
                renderer.lrn,
                header,
                where,
                inventory_text,
                renderer.lrn,
            ]
        )
