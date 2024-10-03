import json
import os

from utils.colors import find_closest


class TextColors:
    escape_code_prefixes: dict
    escape_code_colors: dict
    escape_code_styles: dict
    default_theme: dict
    color_groups: dict

    def __init__(self, escape_code_prefixes=None, escape_code_colors=None, escape_code_styles=None,
                 default_theme=None, color_groups=None):
        color_settings = json.load(open(f'{os.path.dirname(os.path.realpath(__file__))}/text.json'))
        self.escape_code_prefixes = escape_code_prefixes or color_settings['escape_codes']['prefixes']
        self.escape_code_colors = escape_code_colors or color_settings['escape_codes']['colors']
        self.escape_code_styles = escape_code_styles or color_settings['escape_codes']['styles']
        self.default_theme = default_theme or color_settings['themes']['default']
        self.color_groups = color_groups or color_settings['groups']

    def wrap_escape_code(self, code: str | list[str]) -> str:
        if isinstance(code, str):
            code = [code]
        return self.escape_code_prefixes.get('escape') + "".join(code) + self.escape_code_styles.get('end')

    def color(self, color_name: str, background_color: bool = False):
        color_list = self.escape_code_colors.keys()

        if color_name not in color_list:
            color_name = find_closest(color_name, list(color_list))

        return self.wrap_escape_code([
            self.escape_code_prefixes.get("foreground" if background_color else "background"),
            self.escape_code_colors[color_name]
        ])
