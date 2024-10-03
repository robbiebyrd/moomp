import contextlib
import os
from datetime import datetime
from typing import List

from Cheetah.Template import Template
from ansi_escapes import ansiEscapes as ae
from colored import Fore as Fg
from colored import Style as Sty
from mongoengine import Q
from telnetlib3 import TelnetReader, TelnetWriter

from commands import base
from models.character import Character
from models.instance import Instance
from models.object import Object
from services.authn import AuthNService
from services.mqtt import MQTTService
from services.session import TextSession
from templates.room.text import RoomText
from templates.utils.text.graphics import BaseTextTemplate as Btt, TextGraphics, TextColors
from utils.colors import ct, hex_color_complimentary
from utils.db import connect_db

connect_db()


class TelnetService:
    nl = Btt.NEWLINE
    lr = Btt.LINE_RULE
    lr_nl = Btt.LINE_RULE_NEWLINE

    writer: TelnetWriter | None = None
    reader: TelnetReader | None = None
    session: TextSession | None = None

    def __init__(self, instance_name, reader, writer, session=None) -> None:
        if reader is None or writer is None:
            return
        self.session = session if session is not None else TextSession()
        self.session.reader = reader
        self.session.writer = writer
        self.session.instance = Instance.objects(name=instance_name).first()

    def write_line(self, message, add_newline: bool = True):
        if not isinstance(message, list):
            message = [message]
        for msg in message:
            self.session.writer.write(str(msg) + (self.nl if add_newline else ""))

    @staticmethod
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
            self,
            options: List[str],
            message: str | None,
            colors: List[str] | None = None,
            bg_colors: List[str] | None = None,
            required: bool = True,
            center: bool = False,
            spacer: str = TextGraphics().space_char,
            h_padding: int = 1,
            default_selected: int | None = None,
    ):
        line = ""

        selected = (default_selected - 1) if isinstance(default_selected, int) else None

        escape_key_seen = False
        ansi_escape_header_key_seen = False

        def create_list(fg, bg, ops, pad):
            self.write_line(ct(f"{message}", *TextColors.color_styles.get("input")))

            length = max(map(len, ops)) + (h_padding * 2)

            fg = TextGraphics.get_colors_array(fg, len(ops))

            if bg is None:
                bg = [
                    hex_color_complimentary(fg[len(fg) - 1 - i]) for i in range(len(fg))
                ]

            self.write_line(
                [
                    ct(
                        f"{TextGraphics().space_char * pad}{i + 1}:"
                        f" {Sty.reverse if selected is not None and i == selected else ""}"
                        f" {x.center(length, spacer) if center else x.ljust(length, spacer)}",
                        fg[i],
                        bg[i],
                    )
                    for i, x in enumerate(ops)
                ],
            )

        create_list(colors, bg_colors, options, h_padding)

        while True:
            char_input = await self.session.reader.read(1)

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
                self.write_line("".join([ae.eraseLines(len(options) + 3)]))
                selected = self.handle_menu_select(char_input, len(options), selected)
                create_list(colors, bg_colors, options, h_padding)
                escape_key_seen, ansi_escape_header_key_seen = False, False
                continue
            if ord(char_input) in {127}:
                line = line[:-1]
                self.session.writer.write(ae.cursorBackward(1) + ae.eraseEndLine)
                continue
            if ord(char_input) in {10, 13}:
                if required and len(line) == 0:
                    if selected is not None:
                        return selected + 1
                    self.write_line(
                        ct(
                            "This value is required",
                            *TextColors.color_styles.get("error")
                        )
                    )
                    create_list(colors, bg_colors, options, h_padding)
                    continue
                self.session.writer.write(self.nl)
                return self.parse_input_type(line)
            else:
                self.session.writer.echo(char_input)
                line += str(char_input)

    @staticmethod
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
            self,
            message: str | None = None,
            mask_character: str = None,
            required: bool = True,
            on_new_line: bool = True,
    ):
        line = ""

        if message is not None:
            self.session.writer.write(message + (self.nl if on_new_line else ""))
        while True:
            char_input = await self.session.reader.read(1)

            if len(char_input) == 0:
                continue
            elif ord(char_input) in {127}:
                line = line[:-1]
                self.session.writer.write(ae.cursorBackward(1) + ae.eraseEndLine)
            elif ord(char_input) in {10, 13}:
                if required and len(line) == 0:
                    self.session.writer.write(f"This value is required.{self.nl}")
                    continue
                self.session.writer.write(self.nl)
                return self.parse_input_type(line)
            else:
                self.session.writer.echo(
                    mask_character if mask_character is not None else char_input
                )
                line += str(char_input)

    async def login(self):
        autologin = ["wizard@yourhost.com", "wizard"]
        while (
                True
        ):  # This should be a count. We should error out after x number of login tries
            if autologin:
                account = AuthNService.authorize(*autologin)
            else:
                email = await self.input_line("Email address: ", on_new_line=False)
                password = await self.input_line("Password: ", "*", on_new_line=False)
                account = AuthNService.authorize(email, password)

            if account is None:
                self.write_line(
                    f"Your email address and password were not accepted. Please try again."
                    f" {self.nl}"
                )
            else:
                break

        while True:
            characters = AuthNService.characters(account)

            character_input = await self.select(
                [f"{x.name}" for x in characters], "Select a Character: "
            )

            character_input = self.parse_input_type(character_input)

            if isinstance(character_input, int) and len(characters) >= character_input:
                character = characters[character_input - 1]
                break

            character = Character.objects(name=character_input, account=account).first()
            if character is None:
                self.session.writer.write(f"I could not find that character. {self.nl}")
            else:
                break

        character.online = True
        character.save()

        self.session.writer.write(
            f"You are logged in as {character.display} ({character.name}).{self.nl}"
        )
        return character

    def logout(self, mqtt_client):
        self.session.writer.write(f"Goodbye! {self.nl}")
        self.session.character.online = False
        self.session.character.save()
        mqtt_client.loop_stop()
        self.session.writer.close()

    # async def register(self):
    #     while True:
    #         email_input = await self.input_line("Email Address: ")
    #         already_emails = Character.objects(email=email_input)
    #         if len(already_emails) > 0:
    #             self.session.writer.write("That email address is already taken, please try another one.")
    #             continue
    #         break
    #
    #     while True:
    #         character_name_input = await self.input_line("Username: ", required=True, on_new_line=True)
    #         already_character_name = Character.objects(name=character_name_input)
    #         if len(already_character_name) > 0:
    #             self.session.writer.write("That character name is already taken, please try another one.")
    #             continue
    #         break
    #
    #     password_input = await self.input_line("Password: ", mask_character="*")
    #     display_name_input = await self.input_line("Display Name: ")
    #
    #     char = CharacterService.register(
    #         user=CharacterCreateDTO(
    #             name=character_name_input,
    #             display=display_name_input,
    #             password=password_input,
    #             email=email_input,
    #         )
    #     )
    #     return char

    def current_subscriptions(self):
        # The character always subscribes to their own events
        subscriptions = [f"/Character/{self.session.character.id}/#"]

        # If a character is in a room, then it subscribes to that room's events
        if self.session.character.room:
            subscriptions.extend((
                f"/Room/{self.session.character.room.id}/#",
                f"/Speech/+/Room/{self.session.character.room.id}/#",
            ))

        # If a user is holding any objects, then receive event updates on those
        subscriptions.extend(
            f"/Object/{obj.id}/#"
            for obj in Object.objects(
                Q(holder=self.session.character.id) | Q(room=self.session.character.room.id)
            ))

        return subscriptions

    @staticmethod
    async def subscribe(mqtt_client, subscriptions):
        if isinstance(subscriptions, str):
            subscriptions = [subscriptions]

        for subscription in subscriptions:
            mqtt_client.subscribe(subscription)

    @staticmethod
    async def unsubscribe(mqtt_client, subscriptions):
        if isinstance(subscriptions, str):
            subscriptions = [subscriptions]

        for subscription in subscriptions:
            mqtt_client.unsubscribe(subscription)

    async def refresh_subscriptions(self, mqtt_client):
        topics_to_subscribe = self.current_subscriptions()
        self.session.message_topics = list(
            set(self.session.message_topics + topics_to_subscribe)
        )

        topics_to_unsubscribe = [
            subscription
            for subscription in self.session.message_topics
            if subscription not in topics_to_subscribe
        ]
        for topic_to_unsubscribe in topics_to_unsubscribe:
            self.session.message_topics.remove(topic_to_unsubscribe)

        await self.subscribe(mqtt_client, topics_to_subscribe)
        await self.unsubscribe(mqtt_client, topics_to_unsubscribe)

    async def thread(self):
        try:
            colors = self.session.colors

            if msg := self.session.instance.properties['msg_connect']:
                t = Template(msg, searchList={"instance": self.session.instance, "fg": Fg})
                self.write_line(str(t))

            # Attempt to log in
            self.session.character = await self.login()
            line = ""

            mqtt_client = MQTTService(
                os.environ.get("MQTT_HOST"), os.environ.get("MQTT_PORT"), self.session
            ).client()
            self.write_line(
                RoomText.get(self.session.character.room, self.session.character),
                add_newline=False
            )
            mqtt_client.loop_start()

            while True:
                await self.refresh_subscriptions(mqtt_client)

                # Get input one character at a time.
                char_input = await self.session.reader.read(1)

                # If the input is empty, assume a network disconnection.
                if len(char_input) == 0:
                    self.logout(mqtt_client)
                    self.session.writer.close()
                    mqtt_client.disconnect()
                    break

                # Set the window's session size.
                self.session.size = [
                    self.session.writer.get_extra_info("cols"),
                    self.session.writer.get_extra_info("rows"),
                ]

                # Match against our control characters
                match ord(char_input):
                    case 27:  # Escape
                        # Reload the character and show the Room text again
                        self.session.character.reload()
                        self.write_line(
                            RoomText.get(
                                self.session.character.room, self.session.character
                            )
                        )
                    case 8 | 127:  # Backspace/Delete
                        # Remove the last entered character from the display and line buffer
                        line = line[:-1]
                        self.write_line(
                            ae.cursorBackward(1) + ae.eraseEndLine, add_newline=False
                        )
                    case 11:  # Vertical Tab
                        # Show session history
                        self.write_line(
                            "\r\n".join(self.session.input_history) + "\r\n"
                        )
                    case 10 | 13:  # Enter
                        # Pressing Enter triggers the processing of the line
                        # Reload the character document to update any changes that have happened.
                        self.session.character.reload()

                        # Add the line to the session history
                        self.session.input_history.append((line, datetime.now()))

                        # Clear the line and reinsert with the line buffer to fix any input issues
                        self.write_line(
                            "".join(
                                [
                                    ae.eraseLine,
                                    ae.cursorTo(0),
                                    ct(line, *colors.get("input")),
                                    Sty.reset,
                                ]
                            ),
                        )

                        # If a valid command prefix isn't found, but an exit has been referenced,
                        # modify the line to include the 'move' command to the line.
                        line = (
                            f"@move {line}"
                            if self.command_is_an_exit(line, self.session)
                            else line
                        )

                        # Look over every command module and attempt to see if the command prefix matches our input.
                        if hasattr(cmd_mod := self.commands(line), "telnet"):
                            await cmd_mod.telnet(
                                self.session.reader,
                                self.session.writer,
                                mqtt_client,
                                line,
                                self.session,
                            )
                        else:
                            self.write_line("I'm sorry, I didn't understand that.")

                        # Clear the line and we start all over again
                        line = ""
                    case _:  # Any other character
                        char = str(char_input)
                        # Any other characters input be added to the line buffer
                        self.session.writer.echo(ct(char, *colors.get("inputActive")))
                        line += char
        finally:
            pass

    @classmethod
    def command_is_an_exit(cls, line, session):
        return not cls.commands(
            line
        ) and line.strip().lower() in RoomText.get_exit_aliases(
            session.character.room, True, True
        )

    @staticmethod
    def commands(line: str):
        stripped_line = line.strip().lower()

        # Get all commands
        command_modules = base.get_command_modules()

        for cmd in command_modules:
            if stripped_line in cmd.command_prefixes or any(
                    stripped_line.startswith(prefix) for prefix in cmd.command_prefixes
            ):
                return cmd
