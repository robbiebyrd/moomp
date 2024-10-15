from pathlib import Path
from random import randrange
from typing import List

from Cheetah.Template import Template

from models.character import Character
from templates.text import BaseTextTemplate
from templates.utils.text.graphics import TextGraphicsRenderer
from utils.db import connect_db

ren = TextGraphicsRenderer()
connect_db()


class CharacterTextTemplate(BaseTextTemplate):
    @classmethod
    def get_list(cls, characters: List[Character], colors: List[str]):
        text = ""

        chars = [char.name for char in characters]
        text += f"{ren.nl}Characters: " + " ".join(chars) if chars else ""
        return text

    @staticmethod
    def _cwd(filename: str):
        return f"/{Path(f'./{__file__}').parent}/{filename}.templ"

    @classmethod
    def get(cls, character: Character):
        color_groups = list(ren.color_groups.get('colors').values())
        colors = color_groups[randrange(len(color_groups))]

        return str(
            Template(
                cls.load(cls._cwd('character')).replace('\n', ren.nl),
                searchList={
                    'character': character,
                    'ren': ren,
                    'color_list': color_groups,
                    'colors': colors,
                },
            )
        )
