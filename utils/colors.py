import math
from enum import StrEnum

from colored import Fore as Fg, Back as Bg, Style as Sty, stylize


def find_closest(color: str, colors: list[str]) -> str:
    input_color = tuple(int(color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
    distances = [math.sqrt(sum((int(c.lstrip('#')[i:i + 2], 16) - a) ** 2 for i, a in enumerate(input_color))) for c in
                 colors]
    return colors[distances.index(min(distances))]


def hex_color_inverse(hex_color: str):
    hex_color = hex_string_cleaner(hex_color)
    return "#" + "".join([hex(255 - int(hex_color[i: i + 2], 16))[2:].zfill(2) for i in range(1, 6, 2)])


def hex_color_complimentary(hex_color: str):
    r, g, b = hex_color_to_rgb(hex_color)
    r, g, b = r ^ 255, g ^ 255, b ^ 255
    return rgb_color_to_hex(r, g, b)


def hex_string_cleaner(hex_color: str):
    return hex_color[1:] if hex_color.startswith("#") else hex_color


def hex_color_to_rgb(hex_color: str):
    hex_color = hex_string_cleaner(hex_color)
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def rgb_color_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


class ColorType(StrEnum):
    BACKGROUND = "bg"
    FOREGROUND = "fg"


def text_color(hex_color, color_type: ColorType = ColorType.FOREGROUND):
    hex_color = hex_string_cleaner(hex_color)
    match color_type:
        case ColorType.BACKGROUND:
            return Bg.rgb(*hex_color_to_rgb(hex_color))
        case _:
            return Fg.rgb(*hex_color_to_rgb(hex_color))


def colorize_text(text: str, fg_color: str | None = None, bg_color: str | None = None):
    colors = []
    if fg_color:
        colors.append(f"{text_color(fg_color)}")
    if bg_color:
        colors.append(f"{text_color(bg_color, ColorType.BACKGROUND)}")
    return stylize(text, "".join(colors)) + Sty.reset


ct = colorize_text
