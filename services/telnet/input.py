import contextlib

from ansi_escapes import ansiEscapes as ae
from colored import Style as Sty

from services.session import TextSession
from templates.utils.text.color import ColorTextRenderer
from utils.color import hex_color_complimentary, get_colors_array

renderer = ColorTextRenderer()
ct = renderer.colorize


def parse_input_type(line: str):
    # Try to convert the string to a float
    with contextlib.suppress(ValueError):
        return int(line)
    # If that doesn't work, try to convert the string to an integer
    if "." in line:
        with contextlib.suppress(ValueError):
            return float(line)
    # Finally, try to convert the value to a boolean.
    if line.lower() in {"true", "yes", "y"}:
        return True

    return False if line.lower() in {"false", "no", "n"} else line


async def select(
        session: TextSession,
        options: list[str],
        message: str | None,
        colors: list[str] | None = None,
        bg_colors: list[str] | None = None,
        required: bool = True,
        center: bool = False,
        spacer: str = renderer.sp,
        h_padding: int = 1,
        default_selected: int | None = None,
):
    line = ""

    selected = (default_selected - 1) if isinstance(default_selected, int) else None

    escape_key_seen = False
    ansi_escape_header_key_seen = False

    def create_list(fg, bg, ops, pad):
        session.writer.write(renderer.enc(ct(f"{message}", renderer.color_theme.input) + renderer.nl))
        length = max(map(len, ops)) + (h_padding * 2)

        fg = get_colors_array(len(ops), fg)

        if bg is None:
            bg = [
                hex_color_complimentary(fg[len(fg) - 1 - i]) for i in range(len(fg))
            ]

        session.writer.write(renderer.enc(
            "".join([
                ct(
                    f"{renderer.sp * pad}{i + 1}:"
                    f" {Sty.reverse if selected is not None and i == selected else ''}"
                    f" {x.center(length, spacer) if center else x.ljust(length, spacer)}",
                    [fg[i],
                     bg[i]]
                ) + renderer.nl
                for i, x in enumerate(ops)
            ]),
        ))

    create_list(colors, bg_colors, options, h_padding)

    while True:
        char_input = await session.reader.read(1)

        if len(char_input) == 0:
            continue
        if ord(char_input) == 27:
            escape_key_seen = True
            continue
        if escape_key_seen is True and ansi_escape_header_key_seen is False:
            if char_input == "[":
                ansi_escape_header_key_seen = True
            else:
                ansi_escape_header_key_seen = False
                escape_key_seen = False
            continue
        if escape_key_seen is True and ansi_escape_header_key_seen is True:
            session.writer.write("".join([ae.eraseLines(len(options) + 3)]) + renderer.nl)
            selected = handle_menu_select(char_input, len(options), selected)
            create_list(colors, bg_colors, options, h_padding)
            escape_key_seen, ansi_escape_header_key_seen = False, False
            continue
        if ord(char_input) in {127}:
            line = line[:-1]
            session.writer.write(ae.cursorBackward(1) + ae.eraseEndLine)
            continue
        if ord(char_input) in {10, 13}:
            if required and len(line) == 0:
                if selected is not None:
                    return selected + 1
                session.writer.write(
                    ct(
                        "This value is required",
                        *renderer.color_theme.error)
                    + renderer.nl)
                create_list(colors, bg_colors, options, h_padding)
                continue
            session.writer.write(renderer.nl)
            return parse_input_type(line)
        else:
            session.writer.echo(char_input)
            line += str(char_input)


def handle_menu_select(
        char_input: str,
        length: int,
        selected: int | None,
) -> int | None:
    match char_input:
        case "A":  # Up
            if selected is None:
                selected = 0
            selected += -1 if selected > 0 else 0
        case "B":  # Down
            if selected is None:
                selected = 0
            elif selected < length - 1:
                selected += 1
    return selected


async def input_line(
        session: TextSession,
        message: str | None = None,
        mask_character: str = None,
        required: bool = True,
        on_new_line: bool = True,
):
    line = ""

    if message is not None:
        session.writer.write(message + (renderer.nl if on_new_line else ""))
    while True:
        char_input = await session.reader.read(1)

        if len(char_input) == 0:
            continue
        elif ord(char_input) in {127}:
            line = line[:-1]
            session.writer.write(ae.cursorBackward(1) + ae.eraseEndLine)
        elif ord(char_input) in {10, 13}:
            if required and len(line) == 0:
                session.writer.write(f"This value is required.{renderer.nl}")
                continue
            session.writer.write(renderer.nl)
            return parse_input_type(line)
        else:
            session.writer.echo(
                mask_character if mask_character is not None else char_input
            )
            line += str(char_input)
