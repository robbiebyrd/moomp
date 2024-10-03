import json
import os
from math import ceil

from colored import Style as Sty
from colored import fore

from templates.utils.text.color import TextColors


class BaseTextTemplate:
    NEWLINE = "\r\n"
    LINE_RULE = "─" * 20
    LINE_RULE_NEWLINE = LINE_RULE + NEWLINE
    ROWS = 43
    COLUMNS = 80


class TextGraphics(BaseTextTemplate):
    def __init__(self, settings_filename: str = 'text.json'):
        data = json.load(open(f'{os.path.dirname(os.path.realpath(__file__))}/{settings_filename}'))
        default_theme = data['themes']['default']
        color_groups = data['groups']
        graphics = data['graphics']
        escape_code_prefixes = data['escape_codes']['prefixes']
        escape_code_colors = data['escape_codes']['colors']
        settings = data['settings']

        colors_by_brightness = color_groups.get('brightness')
        self.graphics_box = graphics['box'].get(settings['graphics']['box'])
        self.space_char = graphics.get('space')

    @classmethod
    def get_colors_array(cls, colors: list | None, length: int):
        colors = TextColors.colors_by_brightness.get("pastel") if colors is None else colors
        colors = [colors] if type(colors) is not list else colors
        colors = [item for sublist in map(lambda c: [c] * ceil(length / len(colors)), colors) for item in sublist]

        return colors[:length]

    def box(
            self,
            text_content: str | list[str],
            colors: list[str] | None = None,
            center: bool = False,
            min_width: int | None = None,
            max_width: int | None = None,
            h_padding: int = 1,
            v_padding: int = 0,
    ):
        left_top, right_top, left_bottom, right_bottom, horizontal, vertical = self.graphics_box[:6]

        content = [text_content] if type(text_content) is not list or text_content == "" else text_content

        max_line_length = max(map(len, content)) or self.COLUMNS

        if min_width and max_line_length < min_width:
            max_line_length = min_width
        if max_width and max_line_length > max_width:
            max_line_length = max_width

        for i in range(v_padding):
            content.insert(0, "")
            content.append("")

        colors = self.get_colors_array(colors, len(content) + (v_padding * 2))

        formatted_content = "".join(
            [
                "".join(
                    [
                        fore(colors[i]) if True else "",
                        vertical,
                        Sty.reset,
                        self.space_char * h_padding,
                        (
                            content_line.center(max_line_length)
                            if center
                            else content_line.ljust(max_line_length, self.space_char)
                        ),
                        self.space_char * h_padding,
                        fore(colors[i]) if True else "",
                        vertical,
                        Sty.reset,
                        self.NEWLINE,
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
                self.NEWLINE,
            ]
        )
        footer_graf = "".join(
            [fore(colors[-1]), left_bottom, horizontal * (max_line_length + (h_padding * 2)), right_bottom, Sty.reset]
        )

        return header_graf + formatted_content + footer_graf
