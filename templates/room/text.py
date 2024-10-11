from Cheetah.Template import Template
from colored import Style as Sty

from models.character import Character
from models.room import Room
from services.room import RoomService
from templates.utils.text.graphics import TextGraphicsRenderer

renderer = TextGraphicsRenderer()
ct = renderer.colorize


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

        objects_text = f'Objects: {", ".join(objs)}{renderer.nl}' if objs else ""
        characters_text = str(
            Template("Characters: $renderer.list($characters, $char_colors)",
                     searchList={'characters': chars,
                                 'char_colors': renderer.color_theme.error,
                                 'colorize_text': ct, 'renderer': renderer})) + renderer.nl if chars else ""
        exits_test = f"Exits: {Sty.reset}{", ".join(exits)}{renderer.nl}" if len(exits) > 0 else ""

        return "".join(
            [
                renderer.lrn,
                renderer.box(
                    room.name,
                    center=True,
                    h_padding=2,
                    v_padding=0,
                ),
                renderer.nl,
                room.description,
                renderer.nl,
                exits_test,
                objects_text,
                characters_text,
                renderer.lrn,
            ]
        )
