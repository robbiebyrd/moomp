from pathlib import Path
from random import randrange

from Cheetah.Template import Template

from models.object import Object
from templates.text import BaseTextTemplate
from utils.db import connect_db

connect_db()


class ObjectTextTemplate(BaseTextTemplate):
    @staticmethod
    def _cwd(filename: str):
        return f"/{Path(f'./{__file__}').parent}/{filename}.templ"

    def get(
            self,
            obj: Object,
            colors: list[str] = None,
            color_groups: list[list[str]] = None,
    ):
        default_color_groups = list(self._session.ren.color_groups.get("colors").values())
        default_colors = default_color_groups[randrange(len(default_color_groups))]

        return str(
            Template(
                self.load(self._cwd("object")).replace("\n", self._session.ren.nl),
                searchList={
                    "obj": obj,
                    "ren": self._session.ren,
                    "color_list": color_groups or default_color_groups,
                    "colors": colors or default_colors,
                },
            )
        )
