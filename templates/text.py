from math import ceil

from colored import Style as Sty
from colored import fore

from templates.colors.text import TextColors


class BaseTextTemplate:
    NEWLINE = "\r\n"
    LINE_RULE = "─" * 20
    LINE_RULE_NEWLINE = LINE_RULE + NEWLINE
    ROWS = 43
    COLUMNS = 80


class TextGraphics(BaseTextTemplate):
    # left_top, right_top, left_bottom, right_bottom, horizontal, vertical,
    # top t, right t, left t, bottom t, block, underline
    GRAPHICS_BOX_STANDARD = ["┌", "┐", "└", "┘", "─", "│", "┬", "┤", "├", "┴", "█", "▁"]
    GRAPHICS_BOX_ROUNDED = ["╭", "╮", "╰", "╯", "─", "│", "┬", "┤", "├", "┴", "█", "▁"]
    GRAPHICS_BOX_BOLD = ["┏", "┓", "┗", "┛", "━", "┃", "┳", "┫", "┣", "┻", "█", "▁"]
    GRAPHICS_BOX_DOUBLE_OUTLINE = ["╔", "╗", "╚", "╝", "═", "║", "╦", "╣", "╠", "╩", "█", "▁"]
    SPACING_CHAR = " "
    _graphics_box: list[str] = GRAPHICS_BOX_STANDARD

    def __init__(self, graphics_box=None, spacing_char: str = SPACING_CHAR):
        if graphics_box is not None:
            self._graphics_box = graphics_box
        if spacing_char is None:
            spacing_char = self.SPACING_CHAR
        self.SPACING_CHAR = spacing_char

    @classmethod
    def get_colors_array(cls, colors: list | None, length: int):
        colors = TextColors.colors_by_brightness.get("pastel") if colors is None else colors
        colors = [colors] if type(colors) is not list else colors
        colors = [item for sublist in map(lambda c: [c] * ceil(length / len(colors)), colors) for item in sublist]

        return colors[:length]

    @classmethod
    def box(
            cls,
            text_content: str | list[str],
            colors: list[str] | None = None,
            center: bool = False,
            min_width: int | None = None,
            max_width: int | None = None,
            h_padding: int = 1,
            v_padding: int = 0,
    ):
        left_top, right_top, left_bottom, right_bottom, horizontal, vertical = cls._graphics_box[:6]

        content = [text_content] if type(text_content) is not list or text_content == "" else text_content

        max_line_length = max(map(len, content)) or cls.COLUMNS

        if min_width and max_line_length < min_width:
            max_line_length = min_width
        if max_width and max_line_length > max_width:
            max_line_length = max_width

        for i in range(v_padding):
            content.insert(0, "")
            content.append("")

        colors = cls.get_colors_array(colors, len(content) + (v_padding * 2))

        formatted_content = "".join(
            [
                "".join(
                    [
                        fore(colors[i]) if True else "",
                        vertical,
                        Sty.reset,
                        cls.SPACING_CHAR * h_padding,
                        (
                            content_line.center(max_line_length)
                            if center
                            else content_line.ljust(max_line_length, cls.SPACING_CHAR)
                        ),
                        cls.SPACING_CHAR * h_padding,
                        fore(colors[i]) if True else "",
                        vertical,
                        Sty.reset,
                        cls.NEWLINE,
                    ]
                )
                for i, content_line in enumerate(content)
            ]
        )

        header_graf = "".join(
            [
                fore(colors[0]),
                left_top,
                horizontal * (max_line_length + (h_padding * 2)),
                right_top,
                Sty.reset,
                cls.NEWLINE,
            ]
        )
        footer_graf = "".join(
            [fore(colors[-1]), left_bottom, horizontal * (max_line_length + (h_padding * 2)), right_bottom, Sty.reset]
        )

        return header_graf + formatted_content + footer_graf
