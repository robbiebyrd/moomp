from pathlib import Path

from models.room import Room
from services.room import RoomService
from templates.utils.text.graphics import TextGraphicsRenderer

renderer = TextGraphicsRenderer()
ct = renderer.colorize

from random import randrange
from typing import List

from Cheetah.Template import Template

from models.character import Character
from templates.text import BaseTextTemplate
from templates.utils.text.graphics import TextGraphicsRenderer
from utils.db import connect_db

ren = TextGraphicsRenderer()
connect_db()


class RoomTextTemplate(BaseTextTemplate):
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
    def get(cls,
            room: Room,
            character: Character,
            colors: list[str] = None,
            color_groups: list[list[str]] = None):
        default_color_groups = list(ren.color_groups.get('colors').values())
        default_colors = default_color_groups[randrange(len(default_color_groups))]

        exits = RoomService.exits_and_aliases(character.room.id, False)
        here = RoomService.here(room.id)

        objs = list(map(lambda x: x.name, here.get("objects")))
        characters = list(
            filter(
                lambda s: s is not None,
                map(lambda x: x.name if x.id != character.id else None, here.get("characters")),
            )
        )
        return str(
            Template(
                cls.load(cls._cwd('room')).replace('\n', ren.nl),
                searchList={
                    'room': room,
                    'exits': exits,
                    'char': character,
                    'objs': objs,
                    'chars': characters,
                    'ren': ren,
                    'color_list': color_groups or default_color_groups,
                    'colors': colors or default_colors,
                },
            )
        )
