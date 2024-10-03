from datetime import datetime

from telnetlib3 import TelnetWriterUnicode, TelnetReaderUnicode

from models.character import Character
from models.instance import Instance
from templates.utils.text.color import TextColors
from templates.utils.text.graphics import BaseTextTemplate as Btt


class Session:
    character: Character
    instance: Instance
    created: datetime = datetime.now()
    message_topics: [str] = []


class TextSession(Session):
    input_history: list[(str, datetime)] = []
    size: [int, int] = [Btt.ROWS, Btt.COLUMNS]
    colors: dict[str, list[str]] = TextColors().default_theme
    reader: TelnetReaderUnicode = None
    writer: TelnetWriterUnicode = None
