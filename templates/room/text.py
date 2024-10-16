from functools import partial
from operator import is_not
from pathlib import Path
from random import randrange

from Cheetah.Template import Template

from models.character import Character
from models.room import Room
from services.room import RoomService
from templates.text import BaseTextTemplate
from utils.db import connect_db

connect_db()


class RoomTextTemplate(BaseTextTemplate):

    @staticmethod
    def _get_template_path(filename: str):
        return f"/{Path(f'./{__file__}').parent}/{filename}.templ"

    def get(self,
            room: Room,
            character: Character,
            colors: list[str] = None,
            color_groups: list[list[str]] = None):
        default_color_groups = list(self._session.ren.color_groups.get('colors').values())
        default_colors = default_color_groups[randrange(len(default_color_groups))]

        exits = RoomService.exits_and_aliases(character.room.id, False)
        here = RoomService.here(room.id)
        objs = list(map(lambda x: x.name, here.get("objects")))
        characters = list(filter(
            partial(is_not, None),
            map(lambda x: x.name if x.id != character.id else None, here.get("characters"))
        ))

        return str(
            Template(
                self.load(self._get_template_path('room')).replace('\n', self._session.ren.nl),
                searchList={
                    'room': room,
                    'exits': exits,
                    'char': character,
                    'objs': objs,
                    'chars': characters,
                    'ren': self._session.ren,
                    'color_list': color_groups or default_color_groups,
                    'colors': colors or default_colors,
                },
            )
        )
