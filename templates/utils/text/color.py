import contextlib
from enum import StrEnum

from pydantic_extra_types.color import Color

from templates.utils.text.config import ConfigTextColorList, ConfigTextTheme
from templates.utils.text.style import StyleTextRenderer
from utils.color import (
    rgb_color_to_hex,
    find_closest_hex_color,
    ColorEncodingTypes,
    color_kind,
)


class ColorType(StrEnum):
    BACKGROUND = "bg"
    FOREGROUND = "fg"


class ColorTextRenderer(StyleTextRenderer):
    escape_code_colors: dict[str, ConfigTextColorList]
    color_theme: ConfigTextTheme
    color_groups: dict[str, dict[str, list[str]]]

    def __init__(
        self,
        config_file=None,
        escape_code_prefixes=None,
        escape_code_colors=None,
        escape_code_styles=None,
        color_theme: str = None,
        color_groups=None,
    ):
        super().__init__(config_file)

        self.escape_code_prefixes = (
            escape_code_prefixes or self.config.escape_codes.prefixes
        )
        self.escape_code_colors = (
            escape_code_colors or self.config.escape_codes.colors["256"]
        )
        self.escape_code_styles = escape_code_styles or self.config.escape_codes.styles
        self.color_theme = self.config.themes[color_theme or "default"]
        self.color_groups = color_groups or self.config.groups
        self.ct = self.colorize

    def wrap_escape_code(self, code: str | list[str]) -> str:
        code = [code] if isinstance(code, str) else code
        return self.enc(
            str(self.escape_code_prefixes.escape)
            + "".join(code)
            + str(self.escape_code_prefixes.end)
        )

    def color(self, color_name: str, background_color: bool = False):
        return self.wrap_escape_code(
            [
                (
                    self.escape_code_prefixes.background
                    if background_color
                    else self.escape_code_prefixes.foreground
                ),
                self.get_color_code(color_name) or "",
            ]
        )

    def named_color_to_hex(self, color: str):
        if self.escape_code_colors["names"].get(color, None) is not None:
            if (hex_color := self.escape_code_colors["names"].get(color)) is not None:
                if keys := [
                    k
                    for k, v in self.escape_code_colors["hex"].items()
                    if v == hex_color
                ]:
                    return keys[0]

        with contextlib.suppress(Exception):
            return Color(color).as_hex("long")

    def get_color_code(self, color: str) -> str | None:
        match color_kind(color):
            case ColorEncodingTypes.NAME:
                color = self.named_color_to_hex(color)
            case ColorEncodingTypes.RGB:
                color = rgb_color_to_hex(*color)
            case _:
                color = Color(color).as_hex("long")

        if color is None:
            return None

        hex_color_list = [
            c
            for c in list(self.escape_code_colors["hex"].keys())
            if c not in list(self.color_groups["colors"]["grayscale"])
        ]

        if color not in hex_color_list:
            color = find_closest_hex_color(color, hex_color_list)

        return self.escape_code_colors["hex"].get(color, None)

    def colorize(self, message: str, color_name: str | list[str]):
        colors = ""
        if isinstance(color_name, str):
            colors = self.color(color_name)
        if isinstance(color_name, list):
            if len(color_name) == 2:
                colors = "".join(
                    [self.color(color_name[0]), self.color(color_name[1], True)]
                )
            elif len(color_name) > 0:
                colors = self.color(color_name[0])
        return colors + message + self.reset()
