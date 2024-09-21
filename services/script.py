from typing import Union

from lupa.lua54 import LuaRuntime

from models.character import Character
from models.script import Script
from services.room import RoomService
from utils.types import SCRIPT_OBJECT_TYPES


class ScriptService:
    def __init__(self):
        self._runtime = LuaRuntime()

    def run(self, script_id: str, obj: Union[SCRIPT_OBJECT_TYPES]):
        script_object = Script.objects(cId=script_id).first()

        class_name = obj.__class__.__name__

        match class_name:
            case "Character":
                options = (obj,
                           obj.inventory,
                           obj.room,
                           Character.objects(room=obj.room, online=True),
                           obj.account,
                           RoomService.exits(obj.room.id))
            case "Room":
                options = (obj,
                           *RoomService.here(obj.id),
                           RoomService.exits(obj.id))
            case "Object":
                options = (obj,
                           obj.holder,
                           obj.room)
            case "Portal":
                options = (obj,
                           obj.from_room,
                           obj.to_room)
            case _:
                options = obj

        if script_object:
            for script in script_object.scripts:
                if script.type.name == class_name:
                    s_text = script.script
                    func = self._runtime.eval(s_text)
                    a = func(*options)
                    char = a[0]
                    print(char)
                    char.save()
