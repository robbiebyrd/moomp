from datetime import datetime
from typing import Union

import paho.mqtt.client
from telnetlib3 import TelnetWriterUnicode, TelnetReaderUnicode

from models.character import Character
from models.instance import Instance
from templates.utils.text.graphics import TextGraphicsRenderer

renderer = TextGraphicsRenderer()


class Session:
    character: Character | None = None
    instance: Instance | None = None
    created: datetime = datetime.now()
    mqtt_client: Union[paho.mqtt.client, None]
    message_topics: [str] = []
    input_history: list[(str, datetime)] = []


class TextSession(Session):
    size: [int, int] = None
    reader: TelnetReaderUnicode = None
    writer: TelnetWriterUnicode = None
    ren: TextGraphicsRenderer = None
