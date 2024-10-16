import re

from templates.utils.text.color import ColorTextRenderer
from utils.color import get_colors_array, hex_color_complimentary


class TextGraphicsRenderer(ColorTextRenderer):
    colors: list

    def __init__(self, config_file: str | None = None):
        super().__init__(config_file)

        self.colors = self.color_groups.get("brightness").get('darkest')
        self.graphics_box = self.config.text.box[self.config.settings.graphics.box]

    def box(
            self,
            text_content: str | list[str],
            colors: list[str] | None = None,
            center: bool = True,
            min_width: int | None = 1,
            max_width: int | None = None,
            h_padding: int = 2,
            v_padding: int = 0,
    ):

        if max_width is None:
            max_width = self.config.text.columns

        left_top, right_top, left_bottom, right_bottom, horizontal, vertical = self.graphics_box[:6]

        content = [text_content] if type(text_content) is str or text_content == "" else text_content

        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        max_line_length = int(max(map(len, [ansi_escape.sub('', c) for c in content])))

        max_line_length = min(max_line_length, max_width)
        max_line_length = max(max_line_length, min_width)

        for _ in range(v_padding):
            content.insert(0, "")
            content.append("")

        colors = get_colors_array(len(content) + 2 + (v_padding * 2), colors)

        for i, c in enumerate(content):
            content[i] = c.center(max_line_length, ' ')

        formatted_content = "".join(
            [
                "".join(
                    [
                        self.ct(vertical, colors[i]),
                        self.style('reset'),
                        self.sp * h_padding,
                        content_line.center(max_line_length, self.sp)
                        if center
                        else content_line.ljust(max_line_length, self.sp)
                        ,
                        self.sp * h_padding,
                        self.ct(vertical, colors[i]),
                        self.style('reset'),
                        self.nl,
                    ]
                )
                for i, content_line in enumerate(content)
            ]
        )

        header_graf = "".join(
            [
                self.ct(left_top, colors[0]),
                self.ct(horizontal * (max_line_length + (h_padding * 2)), colors[0]),
                self.ct(right_top, colors[0]),
                self.nl,
            ]
        )
        footer_graf = "".join(
            [
                self.ct(left_bottom, colors[-1]),
                self.ct(horizontal * (max_line_length + (h_padding * 2)), colors[-1]),
                self.ct(right_bottom, colors[-1]),
            ]
        )

        return header_graf + formatted_content + footer_graf

    def list(
            self,
            options: list[str],
            colors: list[str],
            padding: int = 1,
            horizontal: bool = True):

        if not options:
            return ""

        colors = get_colors_array(len(options), colors)
        if horizontal:
            return "".join(
                f"""{self.sp * padding if i != 0 else ''}{self.colorize(option, [colors[i], hex_color_complimentary(colors[i])])}{self.sp * padding if i < len(options) else ''}"""
                for i, option in enumerate(options)
            )

        max_length = int(max(map(len, options)) + (padding * 2))

        return "".join(
            f"{self.nl}"
            f"{self.colorize(f"{self.sp * padding}{option.ljust(max_length)}{self.sp * padding}", [colors[i], hex_color_complimentary(colors[i])])}"
            for i, option in enumerate(options)) + self.nl
