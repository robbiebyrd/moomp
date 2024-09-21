import json
import os

from colored import fore, back
from colored.library import Library


class TextColors:
    colors = json.load(open(os.path.dirname(os.path.realpath(__file__)) + '/text.json'))

    colors_by_brightness = colors.get('brightness')

    color_styles = {
        "error": ["#ffafd7", "#5f0000"],
        "input": ["#b2b2b2"],
        "inputActive": ["#000000", "#b2b2b2"],
        "chat": ["afffff"],
    }

    @classmethod
    def fgc(cls, color_name: str):
        return cls.get_color(color_name)

    @classmethod
    def bgc(cls, color_name: str):
        return cls.get_color(color_name, background_color=True)

    @classmethod
    def get_color(
            cls,
            color_name: str,
            background_color: bool = False,
    ):
        if Library.COLORS.get(color_name):
            if background_color:
                return back(color_name)
            else:
                return fore(color_name)
