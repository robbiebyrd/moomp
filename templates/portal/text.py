from pathlib import Path

from models.portal import Portal
from models.room import Room
from templates.utils.text.graphics import TextGraphicsRenderer

renderer = TextGraphicsRenderer()
ct = renderer.colorize

from random import randrange

from Cheetah.Template import Template

from templates.text import BaseTextTemplate
from templates.utils.text.graphics import TextGraphicsRenderer
from utils.db import connect_db

ren = TextGraphicsRenderer()
connect_db()


class PortalTextTemplate(BaseTextTemplate):
    @staticmethod
    def _cwd(filename: str):
        return f"/{Path(f'./{__file__}').parent}/{filename}.templ"

    @classmethod
    def get(
            cls,
            portal: Portal,
            room: Room,
            to: bool,
            colors: list[str] = None,
            color_groups: list[list[str]] = None,
    ):
        default_color_groups = list(ren.color_groups.get("colors").values())
        default_colors = default_color_groups[randrange(len(default_color_groups))]

        return str(
            Template(
                cls.load(cls._cwd("portal")).replace("\n", ren.nl),
                searchList={
                    "portal": portal,
                    "room": room,
                    "to": to,
                    "ren": ren,
                    "color_list": color_groups or default_color_groups,
                    "colors": colors or default_colors,
                },
            )
        )
