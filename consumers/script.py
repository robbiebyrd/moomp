from paho.mqtt import client as mqtt_client

from consumers.base import BaseConsumer
from middleware.updater import mqtt_match
from models.script import Script, ScriptTypesList
from services.script import ScriptService
from services.session import TextSession
from templates.utils.text.color import ColorTextRenderer
from utils.db import connect_db
from utils.types import SCRIPT_OBJECT_TYPES

connect_db()
renderer = ColorTextRenderer()
ct = renderer.colorize


class ScriptConsumer(BaseConsumer):

    @classmethod
    def get_all(cls, select_only: str | None = None):
        if select_only is None:
            return Script.objects.all()
        else:
            return Script.objects.only(select_only)

    @classmethod
    def get_script_topics(cls, instance_id: str):
        return [
            f"/{instance_id}{topic}"
            for script in cls.get_all("scripts.topics")
            for st in script.scripts
            for topic in st.topics
        ]

    @classmethod
    def get_scripts_by_topic(cls, instance_id: str, topic: str):
        return [
            script_def
            for script_def in cls.get_all()
            for script in script_def.scripts
            if any(
                mqtt_match(topic, f"/{instance_id}{topics}") for topics in script.topics
            )
        ]

    @classmethod
    def get_principal_from_topic(cls, topic: str) -> (str, str):
        obj_type, obj_id = topic.split("/")[2:4]

        type_list_index = ScriptTypesList.index(obj_type)
        return SCRIPT_OBJECT_TYPES[type_list_index].objects(id=obj_id).first()

    @classmethod
    def on_message(
        cls, mqtt: mqtt_client, session: TextSession, msg: mqtt_client.MQTTMessage
    ):
        matching_scripts = cls.get_scripts_by_topic(session.instance.id, msg.topic)
        for script in matching_scripts:
            principal_obj = cls.get_principal_from_topic(msg.topic)
            ScriptService(session.instance.id).run(script.id, principal_obj)

    @classmethod
    def validate_topic(cls, instance_id: str, topic: str) -> bool:
        script_assigned_topics = cls.get_script_topics(instance_id)
        return any(mqtt_match(topic, t) for t in script_assigned_topics)
