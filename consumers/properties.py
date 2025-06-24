import json

from paho.mqtt import client as mqtt_client

from consumers.base import BaseConsumer
from middleware.updater import unpack_topic, mqtt_match, notify_and_create_event
from models.script import ScriptTypesList
from services.session import TextSession
from utils.db import connect_db
from utils.types import SCRIPT_OBJECT_TYPES as SOT

connect_db()


class PropertiesConsumer(BaseConsumer):

    @classmethod
    def on_message(
        cls, mqtt: mqtt_client, session: TextSession, msg: mqtt_client.MQTTMessage
    ):
        [obj_type, obj_id, action] = unpack_topic(
            f"/{session.instance.id}/+/+/Properties/+", msg.topic
        )

        match action:
            case "Update":
                if type_list_index := ScriptTypesList.index(obj_type):
                    obj = SOT[type_list_index].objects(id=obj_id).first()
                    if "properties" in obj:
                        obj.properties.update({**obj.properties, **json.loads(msg.payload)})
                    else:
                        obj["properties"] = json.loads(msg.payload)
                    obj.save()

                    notify_and_create_event(
                        session.instance,
                        obj_type,
                        obj,
                        "Updated",
                    )
            case _:
                return

    @classmethod
    def validate_topic(cls, instance_id: str, topic: str) -> bool:
        return mqtt_match(topic, f"/{instance_id}/+/+/Properties/+")
