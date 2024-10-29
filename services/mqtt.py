import paho.mqtt.client as mqttc

from consumers.base import route_message
from services.session import TextSession


class MQTTService:

    def __init__(self, host: str, port: str, session: TextSession):
        mqtt_client = mqttc.Client(mqttc.CallbackAPIVersion.VERSION2)
        mqtt_client.on_message = route_message
        mqtt_client.user_data_set(session)
        mqtt_client.connect(host, int(port), 60)
        mqtt_client.loop_start()

        self.mqtt_client = mqtt_client

    def client(self):
        return self.mqtt_client
