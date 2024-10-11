from templates.utils.text.config import TextPrefixes, TextStyles
from templates.utils.text.text import BaseTextRenderer


class StyleTextRenderer(BaseTextRenderer):
    escape_code_prefixes: TextPrefixes
    escape_code_styles: TextStyles

    def __init__(self, config_file=None, escape_code_prefixes=None, escape_code_styles=None):
        super().__init__(config_file)
        self.escape_code_prefixes = escape_code_prefixes or self.config.escape_codes.prefixes
        self.escape_code_styles = escape_code_styles or self.config.escape_codes.styles

    def wrap_escape_code(self, code: str | list[str]) -> str:
        code = [code] if isinstance(code, str) else code
        return self.escape_code_prefixes.escape + "".join(code) + self.escape_code_prefixes.end

    def get_style_code(self, style):
        return self.escape_code_styles.model_dump().get(style)

    def style(self, styles: str | list[str]):
        styles = [styles] if isinstance(styles, str) else styles
        return "".join([self.wrap_escape_code(self.get_style_code(style)) for style in styles])

    def stylize(self, message: str, styles: [str]):
        return self.style(styles) + message + self.reset()

    def reset(self):
        return self.wrap_escape_code(self.escape_code_styles.reset)
