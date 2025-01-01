import os

import paho.mqtt.client as mqtt_client

from consumers.base import get_consumer_modules
from models.instance import Instance
from services.session import TextSession, Session


class MQTTConsumer:
    instance: Instance
    mqttc: mqtt_client.Client
    consumer_session: Session

    def __init__(self, instance_name):
        self.instance = Instance.objects(name=instance_name).first()
        mqttc = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2)
        mqttc.on_message = self.on_message
        mqttc.connect(os.environ.get("MQTT_HOST"), int(os.environ.get("MQTT_PORT")), 60)
        mqttc.loop_start()

        self.mqtt_client = mqttc

    def serve(self):
        self.mqtt_client.subscribe("/#")

    def on_message(self, mqtt: mqtt_client, _, msg: mqtt_client.MQTTMessage):
        fake_session = TextSession()
        fake_session.instance = self.instance
        for module in get_consumer_modules():
            if module.validate_topic(self.instance.id, msg.topic):
                module.on_message(mqtt, fake_session, msg)
