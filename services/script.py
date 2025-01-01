import json
import os
from typing import Union

from lupa.lua54 import LuaRuntime
from paho.mqtt import publish

from models.script import Script, ScriptType
from services.character import CharacterService
from services.room import RoomService
from utils.types import SCRIPT_OBJECT_TYPES


class ScriptService:
    def __init__(self, instance_id: str):
        self._runtime = LuaRuntime()
        self._instance_id = instance_id

    def run(self, script_id: str, obj: Union[SCRIPT_OBJECT_TYPES]):
        script_object = Script.objects(id=script_id).first()
        if not script_object:
            return

        options = self._get_options(obj)
        self._execute_scripts(script_object, obj.__class__.__name__, options)

    @staticmethod
    def _get_options(obj: Union[SCRIPT_OBJECT_TYPES]) -> tuple:
        match obj.__class__.__name__:
            case "Character":
                return CharacterService(obj).context()
            case "Room":
                return obj, *RoomService.here(obj.id), RoomService.exits(obj.id)
            case "Object":
                return obj, obj.holder, obj.room
            case "Portal":
                return obj, obj.from_room, obj.to_room
            case _:
                return obj

    def _execute_scripts(self, script_object: Script, class_name: str, options: tuple):
        for script in script_object.scripts:
            self._execute_single_script(script, options)

    def _execute_single_script(self, script: ScriptType, options: tuple):
        try:
            func = self._runtime.eval(script.script)
            result = func(*options)
            return self._handle_script_result(result)
        except Exception as e:
            self._handle_script_error(e)

    def _handle_script_result(self, result):
        for v in dict(result).values():
            [a, b] = list(dict(v).values())

            publish.single(
                f"/{self._instance_id}{a}",
                json.dumps(dict(b)),
                hostname=os.environ.get("MQTT_HOST"),
                port=int(os.environ.get("MQTT_PORT")),
            )

    def _handle_script_error(self, error: Exception):
        print(f"Error executing script: {error}")
        # Add appropriate error handling logic here
