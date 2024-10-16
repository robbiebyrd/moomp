from datetime import datetime

import paho.mqtt.client
from telnetlib3 import TelnetWriterUnicode, TelnetReaderUnicode

from models.character import Character
from models.instance import Instance
from templates.utils.text.graphics import TextGraphicsRenderer

renderer = TextGraphicsRenderer()


class Session:
    character: Character
    instance: Instance
    created: datetime = datetime.now()
    message_topics: [str] = []
    mqtt_client: paho.mqtt.client


class TextSession(Session):
    input_history: list[(str, datetime)] = []
    size: [int, int] = None
    reader: TelnetReaderUnicode = None
    writer: TelnetWriterUnicode = None
    ren: TextGraphicsRenderer = None
