from colored import fore

from templates.utils.text.color import ColorTextRenderer
from utils.color import get_colors_array, hex_color_complimentary


class TextGraphicsRenderer(ColorTextRenderer):
    colors: list

    def __init__(self, config_file: str | None = None):
        super().__init__(config_file)

        self.colors = self.color_groups.get("brightness").get('regular')
        self.graphics_box = self.config.text.box[self.config.settings.graphics.box]

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

        max_line_length = max(map(len, content)) or self.col

        if min_width and max_line_length < min_width:
            max_line_length = min_width
        if max_width and max_line_length > max_width:
            max_line_length = max_width

        for _ in range(v_padding):
            content.insert(0, "")
            content.append("")

        colors = get_colors_array(len(content) + (v_padding * 2), colors)

        formatted_content = "".join(
            [
                "".join(
                    [
                        fore(colors[i]) if True else "",
                        vertical,
                        self.style('reset'),
                        self.sp * h_padding,
                        (
                            content_line.center(max_line_length)
                            if center
                            else content_line.ljust(max_line_length, self.sp)
                        ),
                        self.sp * h_padding,
                        fore(colors[i]) if True else "",
                        vertical,
                        self.style('reset'),
                        self.nl,
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
                self.style('reset'),
                self.nl,
            ]
        )
        footer_graf = "".join(
            [
                fore(colors[-1]),
                left_bottom,
                horizontal * (max_line_length + (h_padding * 2)),
                right_bottom,
                self.style('reset'),
            ]
        )

        return header_graf + formatted_content + footer_graf

    def list(
            self,
            options: list[str],
            colors: list[str],
            padding: int = 1,
            horizontal: bool = True):

        colors = get_colors_array(len(options), colors)
        max_length = max(map(len, options)) + (padding * 2)

        if horizontal:
            return "".join(
                f"""{self.sp * padding if i != 0 else ''}{self.colorize(option, [colors[i], hex_color_complimentary(colors[i])])}{self.sp * padding if i < len(options) else ''}"""
                for i, option in enumerate(options)
            )

        return "".join(
            f"""{self.nl}{self.colorize((self.sp * padding) + option.ljust(max_length) + (self.sp * padding), [colors[i], hex_color_complimentary(colors[i])])}"""
            for i, option in enumerate(options)) + self.nl
