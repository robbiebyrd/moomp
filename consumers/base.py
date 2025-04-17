from abc import ABC, abstractmethod
from typing import List

from paho.mqtt import client as mqtt_client

import consumers
from services.session import Session
from utils.system import import_modules


class BaseConsumer(ABC):

    @classmethod
    @abstractmethod
    def on_message(cls, mqtt: mqtt_client, session: Session, msg: mqtt_client.MQTTMessage) -> str | None:
        pass

    @classmethod
    @abstractmethod
    def validate_topic(cls, instance_id: str, topic: str) -> bool:
        pass


def route_message(mqtt: mqtt_client, session: Session, msg: mqtt_client.MQTTMessage):
    for module in get_consumer_modules():
        if module.validate_topic(session.instance.id, msg.topic):
            module.on_message(mqtt, session, msg)


def get_consumer_modules() -> List[BaseConsumer]:
    return import_modules(consumers.__all__, "on_message", "consumers.", "Consumer")
