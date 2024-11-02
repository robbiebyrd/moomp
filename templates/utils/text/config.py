from typing import List, Union

from pydantic import BaseModel


class TextGraphicsSettings(BaseModel, extra="allow"):
    box: str


class ConfigTextSettings(BaseModel, extra="allow"):
    theme: str
    graphics: TextGraphicsSettings


class ConfigTextTheme(BaseModel, extra="allow"):
    error: list[str]
    input: list[str]
    inputActive: list[str]
    chat: list[str]
    chatSelf: list[str]


class ConfigTextBase(BaseModel, extra="allow"):
    rows: int
    columns: int
    newline: str
    line_rule: List[Union[int, str]]
    space: str
    box: dict[str, str]


class ConfigTextStyles(BaseModel, extra="allow"):
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


class ConfigTextPrefixes(BaseModel, extra="allow"):
    escape: str
    end: str
    foreground: str
    background: str
    underline: str


type ConfigTextColorList = dict[str, str]


class ConfigTextEscapeCodes(BaseModel, extra="allow"):
    styles: ConfigTextStyles
    prefixes: ConfigTextPrefixes
    colors: dict[str, dict[str, ConfigTextColorList]]


class ConfigText(BaseModel, extra="allow"):
    settings: ConfigTextSettings
    themes: dict[str, ConfigTextTheme]
    groups: dict[str, dict[str, list[str]]]
    text: ConfigTextBase
    escape_codes: ConfigTextEscapeCodes
