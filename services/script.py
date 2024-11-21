from typing import Union

from lupa.lua54 import LuaRuntime

from models.character import Character
from models.script import Script, ScriptType
from services.room import RoomService
from utils.types import SCRIPT_OBJECT_TYPES


class ScriptService:
    def __init__(self):
        self._runtime = LuaRuntime()

    def run(self, script_id: str, obj: Union[SCRIPT_OBJECT_TYPES]):
        script_object = Script.objects(cId=script_id).first()
        if not script_object:
            return

        options = self._get_options(obj)
        self._execute_scripts(script_object, obj.__class__.__name__, options)

    @staticmethod
    def _get_options(obj: Union[SCRIPT_OBJECT_TYPES]) -> tuple:
        match obj.__class__.__name__:
            case "Character":
                return (
                    obj,
                    obj.inventory,
                    obj.room,
                    Character.objects(room=obj.room, online=True),
                    obj.account,
                    RoomService.exits(obj.room.id),
                )
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
            if script.type.name == class_name:
                self._execute_single_script(script, options)

    def _execute_single_script(self, script: ScriptType, options: tuple):
        try:
            func = self._runtime.eval(script.script)
            result = func(*options)
            self._handle_script_result(result)
        except Exception as e:
            self._handle_script_error(e)

    def _handle_script_result(self, result):
        if isinstance(result, tuple) and len(result) > 0:
            char = result[0]
            if isinstance(char, Character):
                print(char)
        else:
            print(f"Unexpected result format: {result}")

    def _handle_script_error(self, error: Exception):
        print(f"Error executing script: {error}")
        # Add appropriate error handling logic here
