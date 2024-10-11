from typing import List, Union

from pydantic import BaseModel


class TextGraphicsSettings(BaseModel, extra='allow'):
    box: str


class TextSettings(BaseModel, extra='allow'):
    theme: str
    graphics: TextGraphicsSettings


class TextTheme(BaseModel, extra='allow'):
    error: list[str]
    input: list[str]
    inputActive: list[str]
    chat: list[str]
    chatSelf: list[str]


class TextText(BaseModel, extra='allow'):
    rows: int
    columns: int
    newline: str
    line_rule: List[Union[int, str]]
    space: str
    box: dict[str, str]


class TextStyles(BaseModel, extra='allow'):
    bold: str
    dim: str
    italic: str
    underline: str
    blink: str
    reverse: str
    hidden: str
    strikeout: str
    reset: str
    reset_bold: str
    reset_dim: str
    reset_underline: str
    reset_blink: str
    reset_reverse: str
    reset_hidden: str
    reset_underline_color: str


class TextPrefixes(BaseModel, extra='allow'):
    escape: str
    end: str
    foreground: str
    background: str
    underline: str


type TextColorList = dict[str, str]


class TextEscapeCodes(BaseModel, extra='allow'):
    styles: TextStyles
    prefixes: TextPrefixes
    colors: dict[str, dict[str, TextColorList]]


class ConfigText(BaseModel, extra='allow'):
    settings: TextSettings
    themes: dict[str, TextTheme]
    groups: dict[str, dict[str, list[str]]]
    text: TextText
    escape_codes: TextEscapeCodes
