from colored import Style as Sty

from models.character import Character
from models.room import Room
from services.room import RoomService
from templates.text import BaseTextTemplate as Btt, TextGraphics


class RoomText:
    @classmethod
    def get_exit_aliases(cls, room: Room, lowercase: bool = False, filter_duplicates: bool = False):
        exits = []
        for exit_item in RoomService.exits(room_id=room.id):
            if exit_item.to_room.id == room.id:
                exits += exit_item.alias_to
            else:
                exits += exit_item.alias_from
        if lowercase:
            exits = [x.lower() for x in exits]
        if filter_duplicates:
            exits = list(set(exits))
        return exits

    @classmethod
    def get(cls, room: Room, character: Character):
        exits = []
        for exit_item in RoomService.exits(room_id=room.id):
            if exit_item.to_room.id == room.id:
                exits = exits + exit_item.alias_to
            else:
                exits = exits + exit_item.alias_from
        here = RoomService.here(room.id)

        objs = list(map(lambda x: x.name, here.get("objects")))
        chars = list(
            filter(
                lambda s: s is not None,
                map(lambda x: x.name if x.id != character.id else None, here.get("characters")),
            )
        )

        objects_text = f"Objects: {", ".join(objs)}{Btt.NEWLINE}" if len(objs) > 0 else ""
        characters_text = f"Characters: {", ".join(chars)}{Btt.NEWLINE}" if len(chars) > 0 else ""
        exits_test = f"Exits: {Sty.reset}{", ".join(exits)}{Btt.NEWLINE}" if len(exits) > 0 else ""

        return "".join(
            [
                Btt.LINE_RULE_NEWLINE,
                TextGraphics.box(
                    room.name,
                    center=True,
                    h_padding=2,
                    v_padding=0,
                ),
                Btt.NEWLINE,
                room.description,
                Btt.NEWLINE,
                exits_test,
                objects_text,
                characters_text,
                Btt.LINE_RULE_NEWLINE,
            ]
        )
