from pathlib import Path
from random import randrange
from typing import List

from Cheetah.Template import Template

from models.character import Character
from templates.text import BaseTextTemplate
from utils.db import connect_db

connect_db()


class CharacterTextTemplate(BaseTextTemplate):
    def get_list(self, characters: List[Character], colors: List[str]):
        text = ""

        chars = [char.name for char in characters]
        text += f"{self._session.ren.nl}Characters: " + " ".join(chars) if chars else ""
        return text

    @staticmethod
    def _cwd(filename: str):
        return f"/{Path(f'./{__file__}').parent}/{filename}.templ"

    def get(self, character: Character):
        color_groups = list(self._session.ren.color_groups.get("colors").values())
        colors = color_groups[randrange(len(color_groups))]

        return str(
            Template(
                self.load(self._cwd("character")).replace("\n", self._session.ren.nl),
                searchList={
                    "character": character,
                    "ren": self._session.ren,
                    "color_list": color_groups,
                    "colors": colors,
                },
            )
        )
