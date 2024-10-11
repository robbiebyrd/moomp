from datetime import datetime

import paho.mqtt.client
from telnetlib3 import TelnetWriterUnicode, TelnetReaderUnicode

from models.character import Character
from models.instance import Instance
from templates.utils.text.color import ColorTextRenderer

renderer = ColorTextRenderer()


class Session:
    character: Character
    instance: Instance
    created: datetime = datetime.now()
    message_topics: [str] = []
    mqtt_client: paho.mqtt.client


class TextSession(Session):
    input_history: list[(str, datetime)] = []
    size: [int, int] = [renderer.row, renderer.col]
    colors: dict[str, list[str]] = renderer.color_theme
    reader: TelnetReaderUnicode = None
    writer: TelnetWriterUnicode = None
