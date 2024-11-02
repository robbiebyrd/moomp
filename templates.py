import os


def format_portal(ext):
    exit_format = "[{color}]{alias}[/{color}]"

    direction_color_map = {"n": "red", "s": "yellow", "e": "blue", "w": "green"}
    direction_color_default = "purple"

    exit_aliases = " "
    for alias in ext["aliasTo"]:
        color = direction_color_map.get(alias[:1], direction_color_default)
        if x := alias.find("*") > 0:
            alias = "[bold]" + alias[:x] + "[/bold]" + alias[x + 1 :]
        exit_aliases += exit_format.format(alias=alias, color=color) + " "

    return f"{ext['name']} ({exit_aliases})"


def format_portals(portals):
    exits_header_format = "[italic]Exits[/italic]: {exits}"
    exits_string = []

    for ext in portals:
        exits_string.append(format_portal(ext))

    if len(exits_string) > 0:
        return exits_header_format.format(exits=comma_separator(exits_string, False))


def comma_separator(sequence, use_and: bool = True):
    if not sequence:
        return ""
    if len(sequence) == 1:
        return sequence[0]
    if use_and:
        return "{} and {}".format(", ".join(sequence[:-1]), sequence[-1])
    return "{}".format(", ".join(sequence))


def format_object(obj):
    return f"{obj['name']}"


def get_objects(objects):
    objects_header_format = "[italic]Objects[/italic]: {objects}"

    obj_string = []
    for obj in objects:
        obj_string.append(format_object(obj))

    if len(obj_string) > 0:
        return objects_header_format.format(objects=comma_separator(obj_string))

    return ""


def get_room(room):
    room_name, room_description = room["name"], room["description"]

    if "/]" not in room_name:
        room_name = "[blue bold]{room_name}[/blue bold]".format(room_name=room_name)

    template_string = f"""
{os.linesep.join([room_name, room_description])}

{os.linesep.join([format_portals(room['exits']), get_objects(room['objects'])])}"""

    return template_string
