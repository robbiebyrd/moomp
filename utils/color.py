import math
from enum import Enum
from math import ceil


class ColorEncodingTypes(Enum):
    RGB = 1
    HEX = 2
    NAME = 3


def find_closest_hex_color(hex_color: str, hex_colors: list[str]) -> str:
    """Find the closest hex color from a list of colors.

    This function calculates the Euclidean distance between the input color and a list of colors,
    returning the hex color that is closest to the input color.

    Args:
        hex_color (str): The input color in hex format (e.g., '#RRGGBB').
        hex_colors (list[str]): A list of hex colors to compare against.

    Returns:
        str: The closest hex color from the provided list.
    """
    input_color = tuple(int(hex_color.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
    distances = [
        math.sqrt(
            sum(
                (int(c.lstrip("#")[i : i + 2], 16) - a) ** 2
                for i, a in enumerate(input_color)
            )
        )
        for c in hex_colors
    ]
    return hex_colors[distances.index(min(distances))]


def hex_color_inverse(hex_color: str):
    """Calculate the inverse of a hex color.

    This function computes the inverse color of the provided hex color by subtracting each RGB component
    from 255, resulting in a new hex color that is the complementary color.

    Args:
        hex_color (str): The input hex color string (e.g., '#RRGGBB').

    Returns:
        str: The inverse hex color string.
    """
    hex_color = hex_string_cleaner(hex_color)
    return "#" + "".join(
        [hex(255 - int(hex_color[i : i + 2], 16))[2:].zfill(2) for i in range(1, 6, 2)]
    )


def hex_color_complimentary(hex_color: str):
    """Calculate the complementary color of a given hex color.

    This function takes a hex color, converts it to its RGB components, and computes the complementary color
    by inverting each RGB component. The result is returned as a hex color string.

    Args:
        hex_color (str): The input hex color string (e.g., '#RRGGBB').

    Returns:
        str: The complementary hex color string.
    """
    r, g, b = hex_color_to_rgb(hex_color)
    r, g, b = r ^ 255, g ^ 255, b ^ 255
    return rgb_color_to_hex(r, g, b)


def hex_string_cleaner(hex_color: str):
    """Clean a hex color string by removing the leading hash symbol.

    Args:
        hex_color (str): The input hex color string (e.g., '#RRGGBB').

    Returns:
        str: The cleaned hex color string without the leading hash.
    """
    return hex_color[1:] if hex_color.startswith("#") else hex_color


def hex_color_to_rgb(hex_color: str):
    """Convert a hex color string to its RGB components.

    Args:
        hex_color (str): The input hex color string (e.g., '#RRGGBB').

    Returns:
        tuple: A tuple containing the RGB components as integers (r, g, b).
    """
    hex_color = hex_string_cleaner(hex_color)
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def rgb_color_to_hex(r, g, b):
    """Convert RGB components to a hex color string.

    Args:
        r (int): The red component (0-255).
        g (int): The green component (0-255).
        b (int): The blue component (0-255).

    Returns:
        str: The corresponding hex color string (e.g., '#RRGGBB').
    """

    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def color_kind(color):
    if isinstance(color, list | tuple) and len(list(color)) == 3:
        return ColorEncodingTypes.RGB
    elif isinstance(color, str) and color.startswith("#") and 3 <= len(color[1:]) <= 6:
        return ColorEncodingTypes.HEX
    elif isinstance(color, str):
        return ColorEncodingTypes.NAME
    else:
        return None


def get_colors_array(length: int, colors: list | None = None) -> list[str]:
    colors = [colors] if type(colors) is not list else colors
    colors = [
        item
        for sublist in map(lambda c: [c] * ceil(length / len(colors)), colors)
        for item in sublist
    ]

    return colors[:length]
